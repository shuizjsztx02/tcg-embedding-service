"""Full server-like combo with fix knobs, to find a stable no-segfault configuration.

Variants (arg 1):
  plain   - as-is (server current behavior)
  kmp     - KMP_DUPLICATE_LIB_OK=TRUE set before any import
  threads - kmp + faiss/torch/paddle all single-threaded
  reorder - kmp + load text-index faiss & bge BEFORE paddle engine creation
Usage: python diag_combo_variants.py <variant> <runs>
"""
import os, sys

VARIANT = sys.argv[1] if len(sys.argv) > 1 else "plain"
RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 3

if VARIANT in ("kmp", "threads", "reorder"):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import json, time
import numpy as np
import torch
import faiss
from PIL import Image

if VARIANT == "threads":
    torch.set_num_threads(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))
from preprocess import preprocess_for_ocr
from ppocr_v4_engine import PPOCRv4Engine
from sentence_transformers import SentenceTransformer

if VARIANT == "threads":
    faiss.omp_set_num_threads(1)
    OCR_THREADS = 1
else:
    OCR_THREADS = 2

img_path = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images", "100508_200w.jpg")
img = Image.open(img_path)
img.load()


def load_dinov2():
    m = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
    m.eval()
    return m


def load_pokemon_faiss():
    e = np.load(os.path.join(ROOT, "pokemon-index", "embeddings.npy"))
    i = faiss.IndexFlatIP(e.shape[1]); i.add(e)
    return i


def load_text_faiss():
    e = np.load(os.path.join(ROOT, "text-index", "embeddings.npy"))
    i = faiss.IndexFlatIP(e.shape[1]); i.add(e)
    return i


def load_bge():
    return SentenceTransformer("BAAI/bge-small-en-v1.5")


print(f"[0] variant={VARIANT} runs={RUNS}", flush=True)
dinov2 = load_dinov2()
faiss1 = load_pokemon_faiss()

if VARIANT == "reorder":
    faiss2 = load_text_faiss()
    bge = load_bge()
    eng = PPOCRv4Engine(threads=OCR_THREADS)
else:
    eng = PPOCRv4Engine(threads=OCR_THREADS)
    faiss2 = load_text_faiss()
    bge = load_bge()

img_p, meta = preprocess_for_ocr(img)
arr = np.ascontiguousarray(np.asarray(img_p, dtype=np.uint8)[:, :, ::-1])

for n in range(RUNS):
    results, el = eng.read(arr)
    qtext = "\n".join(r.text for r in results)
    q = bge.encode([qtext], normalize_embeddings=True).astype(np.float32)
    s, idx = faiss2.search(q, 5)
    print(f"run{n}: {len(results)} blocks ({el:.2f}s) top1={s[0,0]:.4f}", flush=True)

print("SURVIVED", flush=True)
