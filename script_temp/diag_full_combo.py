"""Full server-like combo: DINOv2(torch) + 2x faiss + paddle + bge, then OCR + encode loop."""
import json, os, sys, time

import numpy as np
import torch
import faiss
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script_temp"))
from preprocess import preprocess_for_ocr, orientation_candidates, to_model_input
from ppocr_v4_engine import PPOCRv4Engine
from sentence_transformers import SentenceTransformer

img_path = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images", "100508_200w.jpg")
img = Image.open(img_path)
img.load()

print("[1] DINOv2...", flush=True)
m = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14"); m.eval()

print("[2] faiss pokemon-index...", flush=True)
e1 = np.load(os.path.join(ROOT, "pokemon-index", "embeddings.npy"))
i1 = faiss.IndexFlatIP(e1.shape[1]); i1.add(e1)

print("[3] paddle engine...", flush=True)
eng = PPOCRv4Engine(threads=2)

print("[4] faiss text-index (AFTER engine, as in server)...", flush=True)
e2 = np.load(os.path.join(ROOT, "text-index", "embeddings.npy"))
i2 = faiss.IndexFlatIP(e2.shape[1]); i2.add(e2)

print("[5] bge...", flush=True)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

for n in range(3):
    print(f"[6.{n}] OCR...", flush=True)
    img_p, meta = preprocess_for_ocr(img)
    arr = np.ascontiguousarray(np.asarray(img_p, dtype=np.uint8)[:, :, ::-1])
    results, el = eng.read(arr)
    print(f"    {len(results)} blocks ({el:.2f}s)", flush=True)
    qtext = "\n".join(r.text for r in results)
    q = model.encode([qtext], normalize_embeddings=True).astype(np.float32)
    s, idx = i2.search(q, 5)
    print(f"    top1 score={s[0,0]:.4f}", flush=True)

print("SURVIVED all iterations", flush=True)
