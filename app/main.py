import os
import sys
import io
import json
import time
import logging
import base64

import numpy as np
import torch
import faiss
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageFile
from sentence_transformers import SentenceTransformer
import uvicorn

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))
from preprocess import to_model_input, preprocess_query, preprocess_for_ocr, preprocess_for_search
from dino_search import search_image
from preprocess_ocr import OCRPreprocessor
from ppocr_v4_engine import PPOCRv4Engine

# ---- Logging ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ---- Constants ----
MAX_FILE_SIZE = 10 * 1024 * 1024

TAU = float(os.environ.get("MATCH_TAU", "0.775"))
MARGIN = float(os.environ.get("MATCH_MARGIN", "0.02"))

# ---- BGE text embedding constants ----
BGE_MODEL_NAME = "D:/Code2026/tcg-embedding-service/script_temp/bge_model"
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# ---- OCR retry config ----
OCR_RETRY_CONF = {"min_blocks": 2, "retry_180": True}

# ---- Pokemon data paths ----
POKEMON_IMAGES_DIR = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images")
POKEMON_INDEX_DIR = os.path.join(ROOT, "pokemon-index")
TEXT_INDEX_DIR = os.path.join(ROOT, "text-index")
PRODUCTS_JSONL = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "products.jsonl")

# ---- Global state ----
model = None
faiss_index = None
index_ids = None
index_version = ""
ocr_engine = None
text_model = None
text_index = None
text_ids = None
products = None

# ---- Pydantic models ----
class HealthResponse(BaseModel):
    status: str
    index_size: int
    embedding_dim: int
    version: str

class MatchResponse(BaseModel):
    status: str
    card_id: str | None = None
    score: float | None = None
    margin: float | None = None
    top2_id: str | None = None
    top2_score: float | None = None
    warnings: list[str] = []
    preprocessing: dict | None = None

class SearchResult(BaseModel):
    rank: int
    card_id: str
    score: float
    product_name: str = ""
    product: dict | None = None

class SearchResponse(BaseModel):
    status: str
    query_time_ms: float
    results: list[SearchResult]
    preprocessed_image: str | None = None
    warnings: list[str] = []
    preprocessing: dict | None = None

class OCRBlock(BaseModel):
    text: str
    confidence: float
    bbox: list[list[float]]

class OCRResponse(BaseModel):
    status: str
    ocr_time_ms: float
    total_blocks: int
    blocks: list[OCRBlock]
    full_text: str
    preprocessed_image: str | None = None
    warnings: list[str] = []

class OcrMatchResult(BaseModel):
    rank: int
    product_id: str
    product_name: str
    set_name: str
    number: str
    rarity: str
    score: float
    has_image: bool
    product: dict | None = None

class OcrMatchResponse(BaseModel):
    status: str
    query_text: str
    query_time_ms: float
    preprocessed_image: str | None = None
    warnings: list[str] = []
    results: list[OcrMatchResult]

# ---- DINOv2 helpers ----
def load_model():
    try:
        m = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
    except Exception:
        from transformers import AutoModel
        m = AutoModel.from_pretrained("facebook/dinov2-base")
    m.eval()
    return m

def run_ocr(img_pil):
    """Run OCR with 180-deg rotation retry fallback."""
    warnings = []
    img_np = np.array(img_pil)
    if img_np.ndim == 2:
        img_bgr = np.stack([img_np] * 3, axis=-1)
    elif img_np.shape[2] == 4:
        img_bgr = img_np[:, :, :3][:, :, ::-1]
    elif img_np.shape[2] == 3:
        img_bgr = img_np[:, :, ::-1]
    else:
        img_bgr = img_np
    img_pp = ocr_preprocessor.preprocess(img_bgr)
    results, elapsed = ocr_engine.read(img_pp)
    full_text = "\n".join(r.text for r in results)
    blocks = [{"text": r.text, "confidence": r.confidence, "bbox": r.bbox} for r in results]
    if len(results) < OCR_RETRY_CONF["min_blocks"] and OCR_RETRY_CONF["retry_180"]:
        from PIL import Image as PILImage
        img_rot = PILImage.fromarray(img_bgr[:, :, ::-1]).rotate(180, expand=True)
        img_rot_np = np.array(img_rot)[:, :, ::-1]
        img_rot_pp = ocr_preprocessor.preprocess(img_rot_np)
        results2, elapsed2 = ocr_engine.read(img_rot_pp)
        if len(results2) > len(results):
            results = results2; elapsed = elapsed2
            full_text = "\n".join(r.text for r in results)
            blocks = [{"text": r.text, "confidence": r.confidence, "bbox": r.bbox} for r in results]
            warnings.append("Applied 180-deg rotation fallback for OCR")
        else:
            warnings.append("Low OCR text count, 180-deg rotation did not improve")
    return blocks, full_text, elapsed, warnings

# ---- FastAPI app ----
app = FastAPI(title="TCG Card Matching Service", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")

@app.on_event("startup")
async def startup():
    global model, faiss_index, index_ids, index_version
    global ocr_engine, ocr_preprocessor
    global text_model, text_index, text_ids, products
    t0 = time.time()
    log.info("Loading DINOv2 model...")
    model = load_model()
    log.info(f"Model loaded in {time.time()-t0:.1f}s")
    index_dir = POKEMON_INDEX_DIR
    index_emb = np.load(os.path.join(index_dir, "embeddings.npy"))
    with open(os.path.join(index_dir, "ids.json"), "r", encoding="utf-8") as f:
        index_ids = json.load(f)
    d = index_emb.shape[1]
    faiss_index = faiss.IndexFlatIP(d)
    faiss_index.add(index_emb)
    index_emb = None
    version_path = os.path.join(index_dir, "version.txt")
    if os.path.exists(version_path):
        with open(version_path, "r", encoding="utf-8") as f:
            index_version = f.readline().strip()
    else:
        index_version = "unknown"
    log.info(f"Gallery index loaded: {faiss_index.ntotal} vectors, dim={d} ({time.time()-t0:.1f}s total)")
    log.info("Loading OCR preprocessor...")
    ocr_preprocessor = OCRPreprocessor(max_dim=1200)
    log.info("OCR preprocessor loaded")
    log.info("Loading PP-OCRv4 engine...")
    ocr_engine = PPOCRv4Engine(threads=2)
    log.info("PP-OCRv4 engine loaded")
    t1 = time.time()
    log.info("Loading BGE text embedding model...")
    text_model = SentenceTransformer(BGE_MODEL_NAME, device="cpu", model_kwargs={"use_safetensors": False})
    log.info(f"BGE model loaded ({time.time()-t1:.1f}s)")
    t2 = time.time()
    log.info("Loading text index...")
    text_emb = np.load(os.path.join(TEXT_INDEX_DIR, "embeddings.npy"))
    with open(os.path.join(TEXT_INDEX_DIR, "ids.json"), "r", encoding="utf-8") as f:
        text_ids = json.load(f)
    text_d = text_emb.shape[1]
    text_index = faiss.IndexFlatIP(text_d)
    text_index.add(text_emb)
    text_emb = None
    log.info(f"Text index loaded: {text_index.ntotal} vectors, dim={text_d} ({time.time()-t2:.1f}s)")
    t3 = time.time()
    log.info("Loading products.jsonl...")
    products = {}
    with open(PRODUCTS_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            products[str(d["productId"])] = d
    log.info(f"Products loaded: {len(products)} records ({time.time()-t3:.1f}s)")
    log.info(f"Total startup: {time.time()-t0:.1f}s")

@app.get("/")
async def root():
    return FileResponse(INDEX_HTML, media_type="text/html")

@app.get("/v1/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", index_size=faiss_index.ntotal if faiss_index is not None else 0, embedding_dim=faiss_index.d if faiss_index is not None else 0, version=index_version)

@app.post("/v1/match", response_model=MatchResponse)
async def match(file: UploadFile = File(...)):
    t0 = time.time()
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files are supported")
        img = Image.open(io.BytesIO(contents))
        img.load()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")
    if model is None or faiss_index is None or faiss_index.ntotal < 2:
        raise HTTPException(503, "DINO index is not ready for matching")
    ranked, _, meta = search_image(img, model, faiss_index, index_ids)
    top1_id = ranked[0]["card_id"]; top2_id = ranked[1]["card_id"]
    best_score = ranked[0]["score"]; best_top2_score = ranked[1]["score"]
    margin = best_score - best_top2_score
    if best_score >= TAU and margin >= MARGIN:
        log.info(f"MATCH {top1_id} score={best_score:.4f} margin={margin:.4f} ({time.time()-t0:.2f}s)")
        return MatchResponse(status="matched", card_id=top1_id, score=round(best_score, 4), margin=round(margin, 4), top2_id=top2_id, top2_score=round(best_top2_score, 4), warnings=meta["warnings"], preprocessing=meta)
    log.info(f"REJECT score={best_score:.4f} margin={margin:.4f} ({time.time()-t0:.2f}s)")
    return MatchResponse(status="rejected", score=round(best_score, 4), margin=round(margin, 4), top2_id=top2_id if best_score >= TAU else None, top2_score=round(best_top2_score, 4) if best_score >= TAU else None, warnings=meta["warnings"], preprocessing=meta)

@app.get("/v1/images/{card_id}")
async def get_image(card_id: str):
    if ".." in card_id or "/" in card_id or "\\" in card_id:
        raise HTTPException(400, "Invalid card_id")
    card_fname = card_id if card_id.endswith(".jpg") else card_id + ".jpg"
    img_path = os.path.join(POKEMON_IMAGES_DIR, card_fname)
    if not os.path.exists(img_path):
        img_path = os.path.join(ROOT, "images", card_fname)
    if not os.path.exists(img_path):
        raise HTTPException(404, f"Image not found: {card_id}")
    return FileResponse(img_path, media_type="image/jpeg")

@app.post("/v1/search", response_model=SearchResponse)
async def search(file: UploadFile = File(...)):
    t0 = time.time()
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files are supported")
        img = Image.open(io.BytesIO(contents))
        img.load()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")
    if model is None or faiss_index is None or faiss_index.ntotal == 0:
        raise HTTPException(503, "DINO index is not ready for searching")
    ranked, best_cand, meta = search_image(img, model, faiss_index, index_ids)
    _buf = io.BytesIO()
    to_model_input(best_cand).save(_buf, format="JPEG", quality=95)
    preprocessed_b64 = base64.b64encode(_buf.getvalue()).decode()
    elapsed = (time.time() - t0) * 1000
    results = []
    for k, row in enumerate(ranked):
        card_id = row["card_id"]
        pid = card_id.removesuffix("_200w")
        product = products.get(pid)
        product_name = product.get("productName", card_id) if product else card_id
        results.append(SearchResult(
            rank=k + 1,
            card_id=card_id,
            score=round(row["score"], 4),
            product_name=product_name,
            product=product,
        ))
    log.info(f"SEARCH top1={results[0].card_id} score={results[0].score:.4f} ({elapsed:.0f}ms)")
    return SearchResponse(status="ok", query_time_ms=round(elapsed, 1), results=results, preprocessed_image=preprocessed_b64, warnings=meta["warnings"], preprocessing=meta)

@app.post("/v1/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile = File(...)):
    t0 = time.time()
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files are supported")
        img = Image.open(io.BytesIO(contents))
        img.load()
        img = preprocess_query(img)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")
    blocks, full_text, ocr_elapsed, warnings = run_ocr(img)
    _buf = io.BytesIO()
    img.save(_buf, format="JPEG", quality=85)
    preprocessed_b64 = base64.b64encode(_buf.getvalue()).decode()
    ocr_blocks = [OCRBlock(text=b["text"], confidence=b["confidence"], bbox=b["bbox"]) for b in blocks]
    log.info(f"OCR {len(blocks)} blocks ({ocr_elapsed*1000:.0f}ms)")
    return OCRResponse(status="ok", ocr_time_ms=round(ocr_elapsed * 1000, 1), total_blocks=len(blocks), blocks=ocr_blocks, full_text=full_text, preprocessed_image=preprocessed_b64, warnings=warnings)

@app.post("/v1/ocr-match", response_model=OcrMatchResponse)
async def ocr_match(file: UploadFile = File(...)):
    t0 = time.time()
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files are supported")
        img = Image.open(io.BytesIO(contents))
        img.load()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")
    img_pp, _ = preprocess_for_ocr(img)
    _buf = io.BytesIO()
    img_pp.save(_buf, format="JPEG", quality=85)
    preprocessed_b64 = base64.b64encode(_buf.getvalue()).decode()
    blocks, full_text, ocr_elapsed, warnings = run_ocr(img_pp)
    if not full_text.strip():
        return OcrMatchResponse(status="ok", query_text="", query_time_ms=round((time.time() - t0) * 1000, 1), preprocessed_image=preprocessed_b64, warnings=["OCR returned no text"], results=[])
    query_text = BGE_QUERY_PREFIX + full_text.strip()
    q_emb = text_model.encode(query_text, normalize_embeddings=True).astype(np.float32)
    scores, indices = text_index.search(q_emb.reshape(1, -1), 5)
    results = []
    for k in range(5):
        pid = text_ids[int(indices[0, k])]
        score = float(scores[0, k])
        prod = products.get(pid, {})
        prod_name = prod.get("productName", pid)
        set_name = prod.get("setName", "")
        number = prod.get("customAttributes", {}).get("number", "") if prod.get("customAttributes") else ""
        rarity = prod.get("rarityName", "")
        has_image = os.path.exists(os.path.join(POKEMON_IMAGES_DIR, f"{pid}_200w.jpg"))
        results.append(OcrMatchResult(rank=k + 1, product_id=pid, product_name=prod_name, set_name=set_name, number=number, rarity=rarity, score=score, has_image=has_image, product=prod if prod else None))
    elapsed = (time.time() - t0) * 1000
    log.info(f"OCR-MATCH top1={results[0].product_id} score={results[0].score:.4f} ({elapsed:.0f}ms)")
    return OcrMatchResponse(status="ok", query_text=full_text.strip(), query_time_ms=round(elapsed, 1), preprocessed_image=preprocessed_b64, warnings=warnings, results=results)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8056)
