from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
import json
from io import BytesIO
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
        raise HTTPException(status_code=500, detail="Kashrut AI Engine is not available. Check configuration.")
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
    kashrut_engine: KashrutEngine = Depends(get_engine),
    off_service: OpenFoodFactsClient = Depends(get_off_client)
):
    """
    Main endpoint for scanning a product.
    Accepts multiple images, an optional barcode, and user preferences.
    """
    print(f"Received scan request. Barcode: {barcode}, Images: {len(images) if images else 0}")
    
    # Parse preferences if provided
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
        for img in images:
            content = await img.read()
            try:
                loaded_images.append(Image.open(BytesIO(content)))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
            
    if not loaded_images and not barcode:
        raise HTTPException(status_code=400, detail="Must provide at least one image or a barcode")

    # Flow
    detected_barcode = barcode
    off_data = None
    
    # 1. Try to extract barcode from image if not provided
    if not detected_barcode and loaded_images:
        detected_barcode = kashrut_engine.extract_barcode(loaded_images[0])
        
    # 2. Get data from OpenFoodFacts if we have a barcode
    if detected_barcode:
        try:
            off_data = off_service.get_product(detected_barcode)
        except Exception as e:
            print(f"Warning: Failed to fetch from OpenFoodFacts: {e}")

    extra_context = off_data.get('ingredients_text') if off_data else None
    
    # 3. Analyze
    try:
        if extra_context and not loaded_images:
            # Only text analysis if we just got a barcode and no images
            result = kashrut_engine.analyze_text(extra_context, preferences=prefs)
        else:
            # Full image + context analysis
            result = kashrut_engine.analyze_product(
                loaded_images, 
                extra_context=extra_context,
                preferences=prefs
            )
            
        # Optional: Add the OpenFoodFacts data to the result for the frontend
        if off_data:
            result['off_data'] = {
                'product_name': off_data.get('product_name'),
                'brands': off_data.get('brands'),
                'quantity': off_data.get('quantity'),
                'barcode': detected_barcode
            }
            
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# This ensures that when running locally with uvicorn directly, it still works.
if __name__ == "__main__":
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
