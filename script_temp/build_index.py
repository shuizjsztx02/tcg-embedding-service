#!/usr/bin/env python3
"""Build the full faiss index from all 9434 valid gallery images.

1. Read metadata.csv for valid image list (excludes corrupt 153316_200w.jpg)
2. For each image: extract DINOv2 CLS token (768-d), L2 normalize
   - portrait: use as-is
   - landscape: use first orientation candidate (rotate(-90))
3. Build faiss IndexFlatIP (cosine similarity via L2-normalized vectors)
4. Save to index/embeddings.npy + index/ids.json
5. Self-check: 100 random images, verify top-1 hit rate = 100%
"""

import argparse
import csv
import json
import os
import random
import sys
import time

import numpy as np
import torch
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import orientation_candidates, to_model_input

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")
INDEX_DIR = os.path.join(ROOT, "index")

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def load_model():
    try:
        model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
    except Exception:
        from transformers import AutoModel
        model = AutoModel.from_pretrained("facebook/dinov2-base")
    model.eval()
    return model


def to_tensor(img):
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = (arr - MEAN) / STD
    return torch.from_numpy(arr.transpose(2, 0, 1)[None]).float()


@torch.no_grad()
def embed_images(model, imgs, batch=16):
    feats = []
    for i in range(0, len(imgs), batch):
        if i % (batch * 50) == 0:
            print(f"  embedding {i}/{len(imgs)}", flush=True)
        x = torch.cat([to_tensor(im) for im in imgs[i:i + batch]])
        out = model(x)
        if out.dim() == 3:
            out = out[:, 0]
        feats.append(out.numpy())
    f = np.concatenate(feats).astype(np.float32)
    norms = np.linalg.norm(f, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return f / norms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=16, help="batch size for DINOv2")
    ap.add_argument("--seed", type=int, default=42, help="random seed for self-check")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    metadata_csv = os.path.join(ROOT, "csv", "metadata.csv")
    names = []
    with open(metadata_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.append(row["name"])
    names = sorted(names)
    card_ids = [os.path.splitext(n)[0] for n in names]
    print(f"valid images: {len(names)}", flush=True)

    model = load_model()
    print("model loaded", flush=True)

    rows = []
    for n in names:
        with Image.open(os.path.join(IMG_DIR, n)) as im:
            im.load()
            cand = next(orientation_candidates(im))
            rows.append(to_model_input(cand))

    t0 = time.time()
    M = embed_images(model, rows, args.batch)
    build_time = time.time() - t0
    print(f"gallery embeddings: {M.shape}  ({build_time:.1f}s)", flush=True)

    import faiss
    d = M.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(M)
    print(f"faiss index size: {index.ntotal}", flush=True)

    os.makedirs(INDEX_DIR, exist_ok=True)
    emb_path = os.path.join(INDEX_DIR, "embeddings.npy")
    ids_path = os.path.join(INDEX_DIR, "ids.json")
    np.save(emb_path, M)
    with open(ids_path, "w", encoding="utf-8") as f:
        json.dump(card_ids, f, ensure_ascii=False)
    print(f"saved: {emb_path}, {ids_path}", flush=True)

    sample_ids = rng.sample(range(len(card_ids)), 100)
    hits = 0
    for idx in sample_ids:
        q = M[idx:idx + 1]
        scores, indices = index.search(q, 3)
        top1 = indices[0, 0]
        if card_ids[top1] == card_ids[idx]:
            hits += 1
        else:
            print(f"  MISMATCH: query={card_ids[idx]} top1={card_ids[top1]} "
                  f"score={scores[0,0]:.4f} top2={card_ids[indices[0,1]]} "
                  f"score={scores[0,1]:.4f}", flush=True)
    print(f"self-check: {hits}/100 top-1 hits ({100 * hits / 100:.0f}%)", flush=True)
    assert hits == 100, f"self-check failed: {hits}/100"

    version_path = os.path.join(INDEX_DIR, "version.txt")
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(f"build_time_s: {build_time:.1f}\n")
        f.write(f"embedding_count: {M.shape[0]}\n")
        f.write(f"embedding_dim: {M.shape[1]}\n")
        f.write(f"index_type: IndexFlatIP\n")
    print(f"version info saved to {version_path}", flush=True)
    print("=== Index Build Complete ===", flush=True)


if __name__ == "__main__":
    main()
