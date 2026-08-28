#!/usr/bin/env python3
"""增量更新 text-index：将 85_Pokemon_Japan 的 products.jsonl 追加到现有索引。

用法：
  python script_temp/update_text_index.py [--batch 128]

流程：
  1. 加载 text-index/embeddings.npy + ids.json（现有索引）
  2. 读取 85_Pokemon_Japan/products.jsonl，跳过已在 ids.json 中的 productId
  3. BGE 编码新 doc（与 build_text_index.py 同一 doc 构建逻辑）
  4. 追加到现有矩阵，重建 faiss IndexFlatIP
  5. 保存回 text-index/
  6. 自检：随机抽 20 条，top-1 命中率 = 100%
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSONL_PATH = os.path.join(ROOT, "category_cards_search", "85_Pokemon_Japan", "products.jsonl")
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

    # 1. 加载现有索引
    emb_path = os.path.join(INDEX_DIR, "embeddings.npy")
    ids_path = os.path.join(INDEX_DIR, "ids.json")
    if not os.path.isfile(emb_path) or not os.path.isfile(ids_path):
        print("错误：text-index 不存在，请先运行 build_text_index.py", flush=True)
        return

    old_emb = np.load(emb_path)
    with open(ids_path, encoding="utf-8") as f:
        old_ids: list[str] = json.load(f)
    print(f"现有索引: {len(old_ids)} 条, shape={old_emb.shape}", flush=True)

    # 2. 读取新数据，跳过已存在的 productId
    existing_set = set(old_ids)
    recs = []
    with open(JSONL_PATH, encoding="utf-8") as f:
        for line in f:
            recs.append(json.loads(line))
    print(f"85_Pokemon_Japan 记录总数: {len(recs)}", flush=True)

    new_docs, new_ids = [], []
    for r in recs:
        pid = str(int(r["productId"]))
        if pid in existing_set:
            continue
        new_docs.append(build_doc(r))
        new_ids.append(pid)
    print(f"待处理(跳过重复): {len(new_docs)}", flush=True)

    if not new_docs:
        print("没有新记录需要处理，索引无变化", flush=True)
        return

    # 3. 编码
    model = SentenceTransformer(MODEL_NAME)
    print(f"model loaded: {MODEL_NAME}", flush=True)

    t0 = time.time()
    M_new = model.encode(
        new_docs, batch_size=args.batch, normalize_embeddings=True, show_progress_bar=True
    ).astype(np.float32)
    print(f"新 embedding: {M_new.shape}  ({time.time()-t0:.0f}s)", flush=True)

    # 4. 合并
    M_all = np.concatenate([old_emb, M_new], axis=0).astype(np.float32)
    all_ids = old_ids + new_ids
    print(f"合并后索引: {len(all_ids)} 条, shape={M_all.shape}", flush=True)

    import faiss
    index = faiss.IndexFlatIP(M_all.shape[1])
    index.add(M_all)

    # self-check：20 条随机，top-1 必须命中自身
    rng = random.Random(42)
    hits = 0
    for i in rng.sample(range(len(all_ids)), 20):
        q = M_all[i:i + 1]
        if int(index.search(q, 1)[1][0, 0]) == i:
            hits += 1
    print(f"self-check: {hits}/20 top-1 hits", flush=True)

    # 5. 保存
    np.save(emb_path, M_all)
    with open(ids_path, "w", encoding="utf-8") as f:
        json.dump(all_ids, f, ensure_ascii=False)
    with open(os.path.join(INDEX_DIR, "version.txt"), "w", encoding="utf-8") as f:
        f.write(f"model: {MODEL_NAME}\n")
        f.write(f"embedding_count: {M_all.shape[0]}\n")
        f.write(f"embedding_dim: {M_all.shape[1]}\n")
        f.write(f"build_time_s: {time.time()-t0:.1f}\n")
        f.write(f"source: 03_Pokemon/products.jsonl + 85_Pokemon_Japan/products.jsonl\n")
    print("=== Update Complete ===", flush=True)


if __name__ == "__main__":
    main()
