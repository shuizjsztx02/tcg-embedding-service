import os
import sys
import io
import json
import time
import logging

import numpy as np
import torch
import faiss
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))
from preprocess import orientation_candidates, to_model_input
from ppocr_v4_engine import PPOCRv4Engine

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---- Constants ----
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Thresholds: configurable via env vars
# From baseline-report.md: tau=0.775 -> 88.1% recall, 82.1% precision, 78 FP/200 unknown
TAU = float(os.environ.get("MATCH_TAU", "0.775"))
MARGIN = float(os.environ.get("MATCH_MARGIN", "0.02"))

# ---- Global state ----
model = None
faiss_index = None
index_ids = None
index_version = ""
ocr_engine = None

# ---- Pydantic schemas ----
class HealthResponse(BaseModel):
    status: str
    index_size: int
    embedding_dim: int
    version: str

class MatchResponse(BaseModel):
    status: str  # "matched" | "rejected"
    card_id: str | None = None
    score: float | None = None
    margin: float | None = None
    top2_id: str | None = None
    top2_score: float | None = None


class SearchResult(BaseModel):
    rank: int
    card_id: str
    score: float


class SearchResponse(BaseModel):
    status: str
    query_time_ms: float
    results: list[SearchResult]


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


# ---- DINOv2 helpers ----
def load_model():
    try:
        m = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
    except Exception:
        from transformers import AutoModel
        m = AutoModel.from_pretrained("facebook/dinov2-base")
    m.eval()
    return m

def to_tensor(img):
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = (arr - MEAN) / STD
    return torch.from_numpy(arr.transpose(2, 0, 1)[None]).float()

@torch.no_grad()
def embed_single(model, img):
    x = to_tensor(img)
    out = model(x)
    if out.dim() == 3:
        out = out[:, 0]
    f = out.numpy().astype(np.float32)
    n = np.linalg.norm(f)
    return f / n if n > 0 else f


# ---- FastAPI app ----
app = FastAPI(title="TCG Card Matching Service", version="0.1.0")

# CORS: allow same-origin and file:// requests for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")


@app.on_event("startup")
async def startup():
    global model, faiss_index, index_ids, index_version
    global ocr_engine
    t0 = time.time()

    log.info("Loading DINOv2 model...")
    model = load_model()
    log.info(f"Model loaded in {time.time()-t0:.1f}s")

    # Load index numpy array
    index_dir = os.path.join(ROOT, "index")
    index_emb = np.load(os.path.join(index_dir, "embeddings.npy"))  # (9434, 768)
    with open(os.path.join(index_dir, "ids.json"), "r", encoding="utf-8") as f:
        index_ids = json.load(f)

    # Build faiss IndexFlatIP from the numpy array
    d = index_emb.shape[1]
    faiss_index = faiss.IndexFlatIP(d)
    faiss_index.add(index_emb)
    index_emb = None  # allow GC

    # Read version
    version_path = os.path.join(index_dir, "version.txt")
    if os.path.exists(version_path):
        with open(version_path, "r", encoding="utf-8") as f:
            index_version = f.readline().strip()
    else:
        index_version = "unknown"

    log.info(
        f"Index loaded: {faiss_index.ntotal} vectors, dim={d} "
        f"({time.time()-t0:.1f}s total)"
    )

    log.info("Loading PP-OCRv4 engine...")
    ocr_engine = PPOCRv4Engine(threads=2)
    log.info("PP-OCRv4 engine loaded")


@app.get("/")
async def root():
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/v1/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        index_size=faiss_index.ntotal if faiss_index is not None else 0,
        embedding_dim=faiss_index.d if faiss_index is not None else 0,
        version=index_version,
    )


@app.post("/v1/match", response_model=MatchResponse)
async def match(file: UploadFile = File(...)):
    """Upload card image -> preprocess -> DINOv2 -> faiss search -> threshold decision."""
    t0 = time.time()

    # Read & validate
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)"
            )
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files are supported")
        img = Image.open(io.BytesIO(contents))
        img.load()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")

    # Preprocess: try all orientation candidates, pick the best match
    cands = list(orientation_candidates(img))
    best_score = -1.0
    best_idx = -1
    best_top2_score = -1.0
    best_top2_idx = -1

    for cand in cands:
        inp = to_model_input(cand)
        feat = embed_single(model, inp)
        scores, indices = faiss_index.search(feat.reshape(1, -1), 3)
        s0 = float(scores[0, 0])
        s1 = float(scores[0, 1])
        if s0 > best_score:
            best_score = s0
            best_idx = int(indices[0, 0])
            best_top2_score = s1
            best_top2_idx = int(indices[0, 1])

    top1_id = index_ids[best_idx]
    top2_id = index_ids[best_top2_idx]
    margin = best_score - best_top2_score

    # Threshold decision: score >= tau AND margin >= min_margin
    if best_score >= TAU and margin >= MARGIN:
        log.info(
            f"MATCH {top1_id} score={best_score:.4f} margin={margin:.4f} "
            f"({time.time()-t0:.2f}s)"
        )
        return MatchResponse(
            status="matched",
            card_id=top1_id,
            score=round(best_score, 4),
            margin=round(margin, 4),
            top2_id=top2_id,
            top2_score=round(best_top2_score, 4),
        )

    log.info(
        f"REJECT score={best_score:.4f} margin={margin:.4f} "
        f"({time.time()-t0:.2f}s)"
    )
    return MatchResponse(
        status="rejected",
        score=round(best_score, 4),
        margin=round(margin, 4),
        top2_id=top2_id if best_score >= TAU else None,
        top2_score=round(best_top2_score, 4) if best_score >= TAU else None,
    )



@app.get("/v1/images/{card_id}")
async def get_image(card_id: str):
    """Serve a card image from the gallery."""
    if ".." in card_id or "/" in card_id or "\\" in card_id:
        raise HTTPException(400, "Invalid card_id")
    img_path = os.path.join(ROOT, "images", card_id + ".jpg")
    if not os.path.exists(img_path):
        raise HTTPException(404, f"Image not found: {card_id}")
    return FileResponse(img_path, media_type="image/jpeg")

@app.post("/v1/search", response_model=SearchResponse)
async def search(file: UploadFile = File(...)):
    """Upload card image -> return top-5 matches without threshold filtering."""
    t0 = time.time()

    # Read & validate
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

    # Preprocess: try all orientation candidates, pick the best score
    cands = list(orientation_candidates(img))
    best_score = -1.0
    best_feat = None

    for cand in cands:
        inp = to_model_input(cand)
        feat = embed_single(model, inp)
        scores, indices = faiss_index.search(feat.reshape(1, -1), 5)
        s0 = float(scores[0, 0])
        if s0 > best_score:
            best_score = s0
            best_feat = feat

    # Search with the best orientation
    scores, indices = faiss_index.search(best_feat.reshape(1, -1), 5)
    elapsed = (time.time() - t0) * 1000

    results = []
    for k in range(5):
        results.append(SearchResult(
            rank=k + 1,
            card_id=index_ids[int(indices[0, k])],
            score=round(float(scores[0, k]), 4),
        ))

    log.info(f"SEARCH top1={results[0].card_id} score={results[0].score:.4f} ({elapsed:.0f}ms)")
    return SearchResponse(
        status="ok",
        query_time_ms=round(elapsed, 1),
        results=results,
    )


@app.post("/v1/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile = File(...)):
    """Upload card image -> extract text using PP-OCRv4."""
    t0 = time.time()

    # Read & validate
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

    # Convert PIL (RGB) to BGR numpy array for OpenCV
    img_np = np.array(img)
    if img_np.ndim == 2:
        img_bgr = np.stack([img_np] * 3, axis=-1)
    elif img_np.shape[2] == 4:
        img_bgr = img_np[:, :, :3][:, :, ::-1]
    elif img_np.shape[2] == 3:
        img_bgr = img_np[:, :, ::-1]
    else:
        img_bgr = img_np

    results, elapsed = ocr_engine.read(img_bgr)

    blocks = [
        OCRBlock(text=r.text, confidence=r.confidence, bbox=r.bbox)
        for r in results
    ]
    full_text = "\n".join(r.text for r in results)

    log.info(f"OCR {len(results)} blocks ({elapsed*1000:.0f}ms)")
    return OCRResponse(
        status="ok",
        ocr_time_ms=round(elapsed * 1000, 1),
        total_blocks=len(results),
        blocks=blocks,
        full_text=full_text,
    )
