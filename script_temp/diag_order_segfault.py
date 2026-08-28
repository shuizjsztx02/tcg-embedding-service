"""Order bisect: torch + faiss + paddle.
A: torch, paddle engine, inference            (no faiss at all)
B: torch, faiss add, paddle engine, inference  (old server order)
C: torch, paddle engine, faiss add, inference  (current server order - suspected bad)"""
import os, sys, time

import numpy as np
import torch
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))

VARIANT = sys.argv[1]

from preprocess import preprocess_for_ocr
from ppocr_v4_engine import PPOCRv4Engine

img_path = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images", "100508_200w.jpg")
img = Image.open(img_path)
img.load()
img_p, meta = preprocess_for_ocr(img)
arr = np.ascontiguousarray(np.asarray(img_p, dtype=np.uint8)[:, :, ::-1])

if VARIANT == "A":
    eng = PPOCRv4Engine(threads=2)
    print("[A] OCR (no faiss)...", flush=True)
    results, el = eng.read(arr)
    print(f"    {len(results)} blocks ({el:.2f}s) SURVIVED", flush=True)
elif VARIANT in ("B", "C"):
    import faiss
    emb = np.load(os.path.join(ROOT, "text-index", "embeddings.npy"))
    index = faiss.IndexFlatIP(emb.shape[1])
    if VARIANT == "B":
        index.add(emb)
        eng = PPOCRv4Engine(threads=2)
        print("[B] OCR (faiss BEFORE engine)...", flush=True)
    else:
        eng = PPOCRv4Engine(threads=2)
        index.add(emb)
        print("[C] OCR (faiss AFTER engine)...", flush=True)
    results, el = eng.read(arr)
    print(f"    {len(results)} blocks ({el:.2f}s) SURVIVED", flush=True)
