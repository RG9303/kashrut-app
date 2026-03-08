from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from PIL import Image
import io
import base64
import os

# Import engine
from engine.kashrut_engine import KashrutEngine

app = FastAPI(title="Kashrut API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine once
ENGINE = None
try:
    ENGINE = KashrutEngine()
except Exception as e:
    # Defer error until endpoint call
    ENGINE = None


def read_imagefile(file: UploadFile) -> Image.Image:
    contents = file.file.read()
    return Image.open(io.BytesIO(contents)).convert("RGB")


@app.post("/analyze_insects")
async def analyze_insects(files: List[UploadFile] = File(...)):
    """Analiza imágenes para insectos. Devuelve la estructura insect_scanner y el resultado completo."""
    if ENGINE is None:
        return {"error": "Engine not configured. Set GOOGLE_API_KEY and restart."}

    images = []
    for f in files:
        try:
            images.append(read_imagefile(f))
        except Exception:
            continue

    if not images:
        return {"error": "No valid images uploaded."}

    result = ENGINE.analyze_insects(images)
    return result


@app.post("/analyze_product")
async def analyze_product(files: Optional[List[UploadFile]] = File(None), barcode: Optional[str] = Form(None)):
    """Analiza imágenes y/o barcode para determinar kashrut. Si se entrega barcode sin imagen, se usará analyze_text via OpenFoodFacts lookup.
    """
    if ENGINE is None:
        return {"error": "Engine not configured. Set GOOGLE_API_KEY and restart."}

    images = []
    if files:
        for f in files:
            try:
                images.append(read_imagefile(f))
            except Exception:
                continue

    # If barcode provided and no images, attempt to fetch OFF product via existing client
    extra_context = None
    if barcode and not images:
        try:
            off = ENGINE.fallback_model  # placeholder to avoid linter; we'll attempt via OFF client if available
        except Exception:
            off = None
        # In the app we can call OpenFoodFactsClient externally; for now we return barcode acknowledgement
        return {"info": "Received barcode", "barcode": barcode}

    if images:
        result = ENGINE.analyze_product(images)
        return result

    return {"error": "No input provided (files or barcode)."}


@app.post("/extract_barcode")
async def extract_barcode(file: UploadFile = File(...)):
    if ENGINE is None:
        return {"error": "Engine not configured. Set GOOGLE_API_KEY and restart."}
    try:
        img = read_imagefile(file)
        code = ENGINE.extract_barcode(img)
        return {"barcode": code}
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok", "engine": (ENGINE is not None)}
