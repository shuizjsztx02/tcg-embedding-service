#!/usr/bin/env python3
"""Build per-category FAISS indexes (visual + text).

Usage:
    python scripts/build_index.py --category pokemon --type all
    python scripts/build_index.py --category pokemon --type visual
    python scripts/build_index.py --category pokemon --type text
    python scripts/build_index.py --category all --type all       # all categories
"""
import argparse
import os
import sys
import time
import json

import numpy as np
import torch
from PIL import Image, ImageFile
from sentence_transformers import SentenceTransformer

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Add project root to path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.config import settings

# DINOv2 constants
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
DINO_INPUT_SIZE = (168, 224)  # (W, H)
BATCH_SIZE = 64


def load_dinov2(device="cpu"):
    try:
        model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
    except Exception:
        from transformers import AutoModel
        model = AutoModel.from_pretrained("facebook/dinov2-base")
    model.eval().to(device)
    return model


def orientation_first(img):
    """Landscape images are rotated -90 degrees (card is portrait)."""
    w, h = img.size
    if w > h:
        return img.rotate(-90, expand=True)
    return img


def to_tensor(img):
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = (arr - MEAN) / STD
    return torch.from_numpy(arr.transpose(2, 0, 1)[None]).float()


@torch.no_grad()
def embed_batch(model, device, imgs):
    x = torch.cat([to_tensor(im) for im in imgs]).to(device)
    out = model(x)
    if out.dim() == 3:
        out = out[:, 0]
    f = out.cpu().numpy().astype(np.float32)
    norms = np.linalg.norm(f, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return f / norms


def build_visual_index(category: str, device: str = "cpu"):
    """Build DINOv2 visual index for a category."""
    image_dir = settings.get_image_dir(category)
    output_dir = settings.get_visual_index_dir(category)
    os.makedirs(output_dir, exist_ok=True)

    names = sorted(n for n in os.listdir(image_dir) if n.lower().endswith((".jpg", ".jpeg", ".png")))
    if not names:
        print(f"  [{category}] No images found in {image_dir}")
        return False

    print(f"  [{category}] Building visual index: {len(names)} images")
    model = load_dinov2(device)
    model_loaded = time.time()

    all_feats, card_ids = [], []
    t0 = time.time()
    for i in range(0, len(names), BATCH_SIZE):
        batch = names[i:i + BATCH_SIZE]
        imgs = []
        for n in batch:
            try:
                with Image.open(os.path.join(image_dir, n)) as im:
                    im.load()
                    imgs.append(orientation_first(im).convert("RGB").resize(
                        DINO_INPUT_SIZE, Image.BICUBIC))
                card_ids.append(os.path.splitext(n)[0])
            except Exception as e:
                print(f"    skip {n}: {e}")
        if imgs:
            all_feats.append(embed_batch(model, device, imgs))
        if (i // BATCH_SIZE) % 20 == 0:
            print(f"    progress {min(i + BATCH_SIZE, len(names))}/{len(names)}  "
                  f"({(time.time()-t0)/60:.1f} min)", flush=True)

    M = np.concatenate(all_feats) if all_feats else np.zeros((0, 768), dtype=np.float32)
    print(f"  [{category}] embeddings: {M.shape} ({(time.time()-model_loaded)/60:.1f} min)")

    import faiss
    index = faiss.IndexFlatIP(M.shape[1])
    index.add(M)
    print(f"  [{category}] faiss index: {index.ntotal} vectors")

    np.save(os.path.join(output_dir, "embeddings.npy"), M)
    with open(os.path.join(output_dir, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(card_ids, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "version.txt"), "w", encoding="utf-8") as f:
        f.write(f"build_time_s: {time.time()-t0:.1f}\n")
        f.write(f"embedding_count: {M.shape[0]}\n")
        f.write(f"embedding_dim: {M.shape[1]}\n")
        f.write(f"source: {image_dir}\n")
    print(f"  [{category}] visual index saved to {output_dir}")

    # Self-check
    if M.shape[0] > 0:
        rng = __import__("random").Random(42)
        sample = rng.sample(range(len(card_ids)), min(100, len(card_ids)))
        hits = 0
        for idx in sample:
            scores, indices = index.search(M[idx:idx + 1], 3)
            if indices[0, 0] == idx:
                hits += 1
        print(f"  [{category}] self-check: {hits}/{len(sample)} top-1 hits")
    return True


def build_text_index(category: str):
    """Build BGE text index for a category."""
    products_path = settings.get_products_path(category)
    output_dir = settings.get_text_index_dir(category)
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(products_path):
        print(f"  [{category}] products.jsonl not found: {products_path}")
        return False

    import re
    ENERGY_SYMBOL = re.compile(r"\[[^\]]*\]")

    def build_doc(r):
        ca = r.get("customAttributes") or {}
        parts = [str(r.get("productName") or "")]
        if ca.get("stage"):
            parts.append(str(ca["stage"]))
        card_type = ca.get("cardTypeB") or ca.get("energyType")
        if card_type:
            parts.append(str(card_type))
        if ca.get("hp"):
            parts.append(f"HP {ca['hp']}")
        attacks = []
        for i in range(1, 5):
            a = ca.get(f"attack{i}")
            if a:
                attacks.append(ENERGY_SYMBOL.sub("", str(a)).strip())
        if attacks:
            parts.append("Attacks: " + "; ".join(attacks))
        for k in ("description", "flavorText", "number"):
            if ca.get(k):
                parts.append(str(ca[k]))
        if r.get("setName"):
            parts.append(str(r["setName"]))
        if r.get("rarityName"):
            parts.append(str(r["rarityName"]))
        return "; ".join(p.strip() for p in parts if p.strip())

    recs = []
    with open(products_path, encoding="utf-8") as f:
        for line in f:
            recs.append(json.loads(line))
    print(f"  [{category}] Building text index: {len(recs)} records")

    docs, ids = [], []
    for r in recs:
        if r.get("productId") is None:
            continue
        docs.append(build_doc(r))
        ids.append(str(int(r["productId"])))

    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    t0 = time.time()
    M = model.encode(docs, batch_size=128, normalize_embeddings=True, show_progress_bar=True).astype(np.float32)
    print(f"  [{category}] embeddings: {M.shape} ({time.time()-t0:.0f}s)")

    import faiss
    index = faiss.IndexFlatIP(M.shape[1])
    index.add(M)

    # Self-check
    rng = __import__("random").Random(42)
    hits = 0
    for i in rng.sample(range(len(ids)), min(20, len(ids))):
        q = M[i:i + 1]
        if int(index.search(q, 1)[1][0, 0]) == i:
            hits += 1
    print(f"  [{category}] self-check: {hits}/{min(20, len(ids))} top-1 hits")

    np.save(os.path.join(output_dir, "embeddings.npy"), M)
    with open(os.path.join(output_dir, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "version.txt"), "w", encoding="utf-8") as f:
        f.write(f"model: BAAI/bge-small-en-v1.5\n")
        f.write(f"embedding_count: {M.shape[0]}\n")
        f.write(f"embedding_dim: {M.shape[1]}\n")
        f.write(f"build_time_s: {time.time()-t0:.1f}\n")
        f.write(f"source: {products_path}\n")
    print(f"  [{category}] text index saved to {output_dir}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Build per-category FAISS indexes")
    ap.add_argument("--category", default="all", help="Category name or 'all'")
    ap.add_argument("--type", default="all", choices=["all", "visual", "text"])
    ap.add_argument("--device", default="", help="Device: 'cpu', 'cuda', or empty for auto")
    args = ap.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    if args.category == "all":
        # Scan DATA_DIR for category directories
        categories = sorted(os.listdir(settings.DATA_DIR)) if os.path.isdir(settings.DATA_DIR) else []
        if not categories:
            print(f"No categories found in {settings.DATA_DIR}")
            return
    else:
        categories = [args.category]

    for cat in categories:
        print(f"\n=== Processing: {cat} ===")
        if args.type in ("all", "visual"):
            build_visual_index(cat, device)
        if args.type in ("all", "text"):
            build_text_index(cat)
    print("\n=== Done ===")


if __name__ == "__main__":
    main()