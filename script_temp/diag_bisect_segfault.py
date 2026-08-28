"""Bisect which part of the bge/sentence_transformers import chain breaks paddle inference.
Usage: python diag_bisect_segfault.py [none|import_st|import_tf|load_model]"""
import json, os, sys, time

import numpy as np
import torch
import faiss
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))

VARIANT = sys.argv[1] if len(sys.argv) > 1 else "none"

from preprocess import preprocess_for_ocr
from ppocr_v4_engine import PPOCRv4Engine

img_path = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images", "100508_200w.jpg")
img = Image.open(img_path)
img.load()

print(f"[1] variant={VARIANT}; init paddle engine", flush=True)
eng = PPOCRv4Engine(threads=2)

emb = np.load(os.path.join(ROOT, "text-index", "embeddings.npy"))
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)
print("[2] faiss loaded", flush=True)

if VARIANT == "import_st":
    print("[3] import sentence_transformers only", flush=True)
    import sentence_transformers  # noqa
elif VARIANT == "import_tf":
    print("[3] import transformers only", flush=True)
    import transformers  # noqa
elif VARIANT == "load_model":
    print("[3] load bge model", flush=True)
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

print("[4] paddle OCR inference...", flush=True)
img_p, meta = preprocess_for_ocr(img)
arr_rgb = np.asarray(img_p, dtype=np.uint8)
results, elapsed = eng.read(np.ascontiguousarray(arr_rgb[:, :, ::-1]))
print(f"    {len(results)} blocks ({elapsed:.2f}s)", flush=True)
print("SURVIVED", flush=True)
