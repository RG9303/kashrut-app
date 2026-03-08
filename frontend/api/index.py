from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
import json
from io import BytesIO
import hashlib
import os
import time
from PIL import Image

from engine.kashrut_engine import KashrutEngine
from engine.off_client import OpenFoodFactsClient

app = FastAPI(
    title="KosherScan API",
    description="Backend API for KosherScan application",
    version="1.0.0"
)

# CORS configuration to allow requests from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
try:
    engine = KashrutEngine()
    off_client = OpenFoodFactsClient()
except Exception as e:
    print(f"Error initializing engines: {e}")
    engine = None
    off_client = None

def get_engine():
    if not engine:
        raise HTTPException(
            status_code=500, 
            detail="Kashrut AI Engine init failed: GOOGLE_API_KEY environment variable is missing in Vercel. Please add it to your project settings."
        )
    return engine

def get_off_client():
    if not off_client:
        raise HTTPException(status_code=500, detail="OpenFoodFacts Client is not available. Check configuration.")
    return off_client

@app.get("/")
def read_root():
    return {"status": "ok", "message": "KosherScan API is running (Vercel Serverless)"}

@app.get("/api")
def read_api_root():
    return {"status": "ok", "message": "KosherScan API is running (Vercel Serverless)"}

@app.post("/api/scan")
async def scan_product(
    barcode: Optional[str] = Form(None),
    preferences: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    phase: Optional[str] = Query("detailed"),
    kashrut_engine: KashrutEngine = Depends(get_engine),
    off_service: OpenFoodFactsClient = Depends(get_off_client)
):
    """
    Main endpoint for scanning a product.
    Accepts multiple images, an optional barcode, and user preferences.
    """
    overall_start = time.time()
    print(f"[API] POST /api/scan started. Barcode: {barcode}, Images: {len(images) if images else 0}")
    
    form_data_start = time.time()
    prefs = {
        "jalav_stam": "Permitido",
        "pesaj_tradicion": "Sefaradí (Kitniyot OK)",
        "rigor": "Regular"
    }
    if preferences:
        try:
            parsed_prefs = json.loads(preferences)
            prefs.update(parsed_prefs)
        except json.JSONDecodeError:
            pass # Use defaults if invalid JSON

    # Load images
    loaded_images = []
    if images:
        print(f"[API] Loading {len(images)} images into memory...")
        for img in images:
            content = await img.read()
            try:
                loaded_images.append(Image.open(BytesIO(content)))
            except Exception as e:
                print(f"[API] Image load error: {e}")
                raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
            
    form_data_end = time.time()
    print(f"[API] ⏱️ FormData & Image Parse Time: {form_data_end - form_data_start:.2f}s")
    print(f"[API] Successfully loaded {len(loaded_images)} valid images. Checking for barcode...")
    
    if not loaded_images and not barcode:
        raise HTTPException(status_code=400, detail="Must provide at least one image or a barcode")

    # ----- CACHE LAYER -----
    # Create a unique hash for this scan based on barcode + preferences + images + phase
    cache_dir = "/tmp/kashrut_cache"
    os.makedirs(cache_dir, exist_ok=True)
    
    hash_input = str(barcode) + json.dumps(prefs) + phase
    if images:
        for img in images:
            # Re-read position for hashing without losing stream
            await img.seek(0)
            chunk = await img.read(8192) # just hash first 8k for speed
            hash_input += chunk.hex()
            await img.seek(0) # reset for PIL
            
    req_hash = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
    cache_file = os.path.join(cache_dir, f"{req_hash}.json")
    
    if os.path.exists(cache_file):
        print(f"[API] Cache HIT for hash {req_hash}! Returning instant result.")
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception:
            pass # fallback to processing if cache is corrupted
            
    print(f"[API] Cache MISS for hash {req_hash}. Proceeding to AI...")
    # -----------------------

    # Flow
    detected_barcode = barcode
    off_data = None
    
    # 1. Try to extract barcode from image if not provided
    if not detected_barcode and loaded_images:
        print("[API] No barcode provided. Attempting to extract from image...")
        detected_barcode = kashrut_engine.extract_barcode(loaded_images[0])
        print(f"[API] Extracted barcode: {detected_barcode}")
        
    # 2. Get data from OpenFoodFacts if we have a barcode
    if detected_barcode:
        print(f"[API] Fetching OpenFoodFacts data for barcode {detected_barcode}...")
        try:
            off_data = off_service.get_product(detected_barcode)
            print("[API] OpenFoodFacts data retrieved successfully.")
        except Exception as e:
            print(f"[API] Warning: Failed to fetch from OpenFoodFacts: {e}")

    extra_context = off_data.get('ingredients_text') if off_data else None
    
    # 3. Analyze
    print(f"[API] Starting AI Analysis (Phase: {phase})...")
    ai_start = time.time()
    try:
        if phase == "fast":
            print("[API] Executing FAST phase analysis")
            result = kashrut_engine.analyze_fast(loaded_images, extra_context=extra_context)
        else:
            if extra_context and not loaded_images:
                # Only text analysis if we just got a barcode and no images
                print("[API] Executing text-only analysis (barcode but no images)")
                result = kashrut_engine.analyze_text(extra_context, preferences=prefs)
            else:
                # Full image + context analysis
                print("[API] Executing full image + context analysis")
                result = kashrut_engine.analyze_product(
                    loaded_images, 
                    extra_context=extra_context,
                    preferences=prefs
                )
            
        ai_end = time.time()
        print(f"[API] ⏱️ AI Request Time: {ai_end - ai_start:.2f}s")
        print("[API] AI Analysis Complete. Formatting response...")
        
        res_start = time.time()
        # Optional: Add the OpenFoodFacts data to the result for the frontend
        if off_data:
            result['off_data'] = {
                'product_name': off_data.get('product_name'),
                'brands': off_data.get('brands'),
                'quantity': off_data.get('quantity'),
                'barcode': detected_barcode
            }
            
        # Save to cache before returning
        try:
            with open(cache_file, 'w') as f:
                json.dump(result, f)
        except Exception as e:
            print(f"[API] Failed to write cache: {e}")
            
        res_end = time.time()
        print(f"[API] ⏱️ Response Generation Time: {res_end - res_start:.2f}s")
        print(f"[API] ⏱️ Total /api/scan Execution Time: {time.time() - overall_start:.2f}s")
            
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# This ensures that when running locally with uvicorn directly, it still works.
if __name__ == "__main__":
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
