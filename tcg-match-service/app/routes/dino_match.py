import io
import time
import logging

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from PIL import Image

from app.models.schemas import DinoMatchResponse, SearchResult
from app.services.dino_service import DINOv2Service
from app.services.index_service import IndexService

log = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024


def _validate_image_bytes(contents: bytes, content_type: str | None) -> Image.Image:
    if len(contents) == 0:
        raise HTTPException(400, "Empty file")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
    if content_type and not content_type.startswith("image/"):
        raise HTTPException(400, "Only image files are supported")
    try:
        img = Image.open(io.BytesIO(contents))
        img.load()
        return img
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")


def _init_route(dino_service: DINOv2Service, index_service: IndexService):
    """Inject dependencies (called from main.py on startup)."""
    router.dino_service = dino_service
    router.index_service = index_service


@router.post("/v1/dino-match", response_model=DinoMatchResponse)
async def dino_match(
    file: UploadFile = File(...),
    category: str = Form("pokemon"),
    top_k: int = Form(5),
):
    t0 = time.time()
    contents = await file.read()
    img = _validate_image_bytes(contents, file.content_type)

    dino = getattr(router, "dino_service", None)
    index = getattr(router, "index_service", None)
    if dino is None or index is None:
        raise HTTPException(503, "Service not ready")

    if category not in index.visual_indexes:
        raise HTTPException(400, f"Category '{category}' not found or has no visual index")

    feat = dino.embed(img)
    results = index.search_visual(category, feat, top_k)
    if results is None:
        raise HTTPException(503, f"Visual index for '{category}' is not ready")

    elapsed = (time.time() - t0) * 1000
    log.info(f"DINO-MATCH [{category}] top1={results[0]['card_id']} score={results[0]['score']:.4f} ({elapsed:.0f}ms)")

    return DinoMatchResponse(
        status="ok",
        category=category,
        query_time_ms=round(elapsed, 1),
        results=[SearchResult(**r) for r in results],
    )