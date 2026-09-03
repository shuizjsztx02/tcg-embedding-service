import io
import time
import logging

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from PIL import Image

from app.models.schemas import OcrMatchResponse, OcrMatchResult
from app.services.ocr_service import OCRService
from app.services.text_service import TextService
from app.services.index_service import IndexService

log = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024


def _init_route(ocr_service: OCRService, text_service: TextService, index_service: IndexService):
    """Inject dependencies (called from main.py on startup)."""
    router.ocr_service = ocr_service
    router.text_service = text_service
    router.index_service = index_service


@router.post("/v1/ocr-match", response_model=OcrMatchResponse)
async def ocr_match(
    file: UploadFile = File(...),
    category: str = Form("pokemon"),
    top_k: int = Form(5),
):
    t0 = time.time()

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(400, "Empty file")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files are supported")
    try:
        img = Image.open(io.BytesIO(contents))
        img.load()
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")

    ocr = getattr(router, "ocr_service", None)
    text = getattr(router, "text_service", None)
    index = getattr(router, "index_service", None)
    if ocr is None or text is None or index is None:
        raise HTTPException(503, "Service not ready")

    if category not in index.text_indexes:
        raise HTTPException(400, f"Category '{category}' not found or has no text index")

    blocks, full_text, query_text, warnings = ocr.read(img)

    if not query_text:
        elapsed = (time.time() - t0) * 1000
        return OcrMatchResponse(
            status="ok", category=category, query_text="", full_text=full_text,
            query_time_ms=round(elapsed, 1), warnings=warnings, results=[],
        )

    q_emb = text.encode(query_text)
    results = index.search_text(category, q_emb, top_k)
    if results is None:
        raise HTTPException(503, f"Text index for '{category}' is not ready")

    elapsed = (time.time() - t0) * 1000
    log.info(f"OCR-MATCH [{category}] top1={results[0]['product_id']} score={results[0]['score']:.4f} ({elapsed:.0f}ms)")

    return OcrMatchResponse(
        status="ok", category=category, query_text=query_text, full_text=full_text,
        query_time_ms=round(elapsed, 1), warnings=warnings,
        results=[OcrMatchResult(**r) for r in results],
    )