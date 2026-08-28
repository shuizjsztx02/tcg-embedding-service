#!/usr/bin/env python3
"""Build text embedding index from category_cards_search/03_Pokemon/products.jsonl.

与 build_pokemon_index.py 同一输出约定，供 app/main.py 加载：
  - BAAI/bge-small-en-v1.5 (384-d)，normalize_embeddings=True（余弦相似度）
  - 输出 text-index/embeddings.npy + ids.json（productId 字符串，与行对齐）+ version.txt

doc 构造：productName + 卡面可读字段（stage/type/hp/attacks/description/number/set/rarity），
能量符号 [L] 之类剔除只留文字。

用法：
  python build_text_index.py [--batch 128]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import time

import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = os.path.dirname(os.path.abspath(__file__))
JSONL_PATH = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "products.jsonl")
INDEX_DIR = os.path.join(ROOT, "text-index")
MODEL_NAME = "BAAI/bge-small-en-v1.5"

ENERGY_SYMBOL = re.compile(r"\[[^\]]*\]")


def build_doc(r: dict) -> str:
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=128)
    args = ap.parse_args()

    recs = []
    with open(JSONL_PATH, encoding="utf-8") as f:
        for line in f:
            recs.append(json.loads(line))
    print(f"records: {len(recs)}  <- {JSONL_PATH}", flush=True)

    docs, ids = [], []
    for r in recs:
        if r.get("productId") is None:
            continue
        docs.append(build_doc(r))
        ids.append(str(int(r["productId"])))
    print(f"docs: {len(docs)}  sample: {docs[0][:120]!r}", flush=True)

    model = SentenceTransformer(MODEL_NAME)
    print(f"model loaded: {MODEL_NAME}", flush=True)

    t0 = time.time()
    M = model.encode(
        docs, batch_size=args.batch, normalize_embeddings=True, show_progress_bar=True
    ).astype(np.float32)
    print(f"embeddings: {M.shape}  ({time.time()-t0:.0f}s)", flush=True)

    import faiss
    index = faiss.IndexFlatIP(M.shape[1])
    index.add(M)

    # self-check: 20 条原始 doc 查询，top-1 必须命中自身
    rng = random.Random(42)
    hits = 0
    for i in rng.sample(range(len(ids)), 20):
        q = M[i:i + 1]
        if int(index.search(q, 1)[1][0, 0]) == i:
            hits += 1
    print(f"self-check: {hits}/20 top-1 hits", flush=True)
    assert hits == 20, f"self-check failed: {hits}/20"

    os.makedirs(INDEX_DIR, exist_ok=True)
    np.save(os.path.join(INDEX_DIR, "embeddings.npy"), M)
    with open(os.path.join(INDEX_DIR, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False)
    with open(os.path.join(INDEX_DIR, "version.txt"), "w", encoding="utf-8") as f:
        f.write(f"model: {MODEL_NAME}\n")
        f.write(f"embedding_count: {M.shape[0]}\n")
        f.write(f"embedding_dim: {M.shape[1]}\n")
        f.write(f"build_time_s: {time.time()-t0:.1f}\n")
        f.write(f"source: {os.path.relpath(JSONL_PATH, ROOT)}\n")
    print("=== Text Index Build Complete ===", flush=True)


if __name__ == "__main__":
    main()
