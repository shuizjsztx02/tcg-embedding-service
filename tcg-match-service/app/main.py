import os
import time
import logging

import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import ImageFile

from app.config import settings
from app.models.schemas import HealthResponse
from app.services.dino_service import DINOv2Service
from app.services.ocr_service import OCRService
from app.services.text_service import TextService
from app.services.index_service import IndexService
from app.services.llm_service import LLMService
from app.routes import dino_match, ocr_match, recognize

ImageFile.LOAD_TRUNCATED_IMAGES = True

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s %(message)s")
log = logging.getLogger(__name__)

# ---- Global services (set during startup) ----
dino_service: DINOv2Service = None
ocr_service: OCRService = None
text_service: TextService = None
index_service: IndexService = None
llm_service: LLMService = None

# ---- FastAPI app ----
app = FastAPI(title="TCG Match Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")


@app.on_event("startup")
async def startup():
    global dino_service, ocr_service, text_service, index_service, llm_service
    t0 = time.time()

    device = "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
    log.info(f"Device: {device}")

    # 1. DINOv2
    log.info("Loading DINOv2 model...")
    dino_service = DINOv2Service(device=device)
    log.info(f"DINOv2 loaded ({time.time()-t0:.1f}s)")

    # 2. PP-OCRv4
    log.info("Loading PP-OCRv4 engine...")
    ocr_service = OCRService(threads=2)
    log.info(f"PP-OCRv4 loaded ({time.time()-t0:.1f}s)")

    # 3. BGE
    log.info("Loading BGE text model...")
    text_service = TextService(device=device)
    log.info(f"BGE loaded ({time.time()-t0:.1f}s)")

    # 4. Per-category indexes
    log.info("Loading per-category indexes...")
    index_service = IndexService()
    categories = index_service.load_all_categories()
    log.info(f"Categories loaded: {categories} ({time.time()-t0:.1f}s total)")

    # 5. LLM service (no heavy load, just config-driven HTTP client)
    log.info("Initializing LLM service...")
    llm_service = LLMService()
    log.info(f"LLM service ready ({time.time()-t0:.1f}s)")

    # Inject dependencies into route handlers
    dino_match._init_route(dino_service, index_service)
    ocr_match._init_route(ocr_service, text_service, index_service)
    recognize._init_route(dino_service, index_service, llm_service)

    log.info(f"Startup complete ({time.time()-t0:.1f}s)")


# Register routes (at module level, before startup)
app.include_router(dino_match.router)
app.include_router(ocr_match.router)
app.include_router(recognize.router)


@app.get("/")
async def root():
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/v1/health", response_model=HealthResponse)
async def health():
    idx = index_service or IndexService()
    return HealthResponse(
        status="ok",
        categories=idx.categories,
        dino_index_sizes=idx.dino_index_sizes,
        text_index_sizes=idx.text_index_sizes,
    )


@app.get("/v1/images/{category}/{card_id}")
async def get_image(category: str, card_id: str):
    if ".." in card_id or "/" in card_id or "\\" in card_id:
        raise HTTPException(400, "Invalid card_id")
    card_fname = card_id if card_id.endswith(".jpg") else card_id + ".jpg"
    img_dir = settings.get_image_dir(category)
    img_path = os.path.join(img_dir, card_fname)
    if not os.path.exists(img_path):
        raise HTTPException(404, f"Image not found: {card_id}")
    return FileResponse(img_path, media_type="image/jpeg")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)