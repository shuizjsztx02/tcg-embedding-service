"""Test fix: disable paddle mkldnn (oneDNN) to avoid segfault with torch/bge loaded."""
import json, os, sys

import numpy as np
import torch
import faiss
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))

import paddle
# --- the fix: no-op mkldnn enable ---
paddle.inference.Config.enable_mkldnn = lambda self, *a, **k: None

from preprocess import preprocess_for_ocr
from ppocr_v4_engine import PPOCRv4Engine
from sentence_transformers import SentenceTransformer

img_path = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images", "100508_200w.jpg")
img = Image.open(img_path)
img.load()

print("[1] init paddle OCR engine (mkldnn disabled)...", flush=True)
eng = PPOCRv4Engine(threads=2)

emb = np.load(os.path.join(ROOT, "text-index", "embeddings.npy"))
with open(os.path.join(ROOT, "text-index", "ids.json"), encoding="utf-8") as f:
    ids = json.load(f)
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)
print(f"[2] faiss: {index.ntotal} vectors", flush=True)

print("[3] load bge...", flush=True)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

print("[4] OCR (mkldnn off)...", flush=True)
img_p, meta = preprocess_for_ocr(img)
arr_rgb = np.asarray(img_p, dtype=np.uint8)
t0 = __import__("time").time()
results, elapsed = eng.read(np.ascontiguousarray(arr_rgb[:, :, ::-1]))
print(f"    {len(results)} blocks ({elapsed:.2f}s)", flush=True)
for r in results[:5]:
    print("   ", repr(r.text), r.confidence)

print("[5] bge encode + faiss search...", flush=True)
qtext = "\n".join(r.text for r in results)
q = model.encode([qtext], normalize_embeddings=True).astype(np.float32)
scores, idxs = index.search(q, 5)
for k in range(5):
    pid = ids[int(idxs[0, k])]
    print(f"    #{k+1} {pid} score={scores[0,k]:.4f}", flush=True)

print("[6] second OCR pass...", flush=True)
results2, e2 = eng.read(np.ascontiguousarray(arr_rgb[:, :, ::-1]))
print(f"    {len(results2)} blocks ({e2:.2f}s)", flush=True)

print("ALL OK - no segfault with mkldnn disabled", flush=True)
