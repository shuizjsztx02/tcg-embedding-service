#!/usr/bin/env python3
"""Build pokemon-index from category_cards_search/03_Pokemon/images.

与 script_temp/build_index.py 同一套约定（供 app/main.py 直接加载）：
  - DINOv2 ViT-B/14 CLS token (768-d)，L2 归一化
  - 输入 resize 到 168x224；横图取第一个方向候选 rotate(-90)
  - 输出 embeddings.npy + ids.json（id 为文件名去掉 .jpg，如 "100503_200w"）

差异：图片 2.8 万张，改为分批流式处理（不全量载入内存），
并每 2000 张写 checkpoint，中断后重跑可续。

用法：
  python build_pokemon_index.py                # 默认 GPU（无则 CPU）
  python build_pokemon_index.py --batch 32     # 调 batch size
"""
from __future__ import annotations

import argparse
import json
import os
import random
import time

import numpy as np
import torch
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "category_cards_search", "03_Pokemon", "images")
INDEX_DIR = os.path.join(ROOT, "pokemon-index")

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

MODEL_INPUT = (168, 224)  # (W, H) 14 的倍数，对齐 DINOv2 ViT-B/14 patch grid
CKPT_EVERY = 2000


def load_model():
    try:
        model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
    except Exception:
        from transformers import AutoModel
        model = AutoModel.from_pretrained("facebook/dinov2-base")
    model.eval()
    return model


def orientation_first(img):
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


def save_ckpt(names_done: list[str], feats: list[np.ndarray]):
    np.save(os.path.join(INDEX_DIR, "_ckpt_emb.npy"),
            np.concatenate(feats) if feats else np.zeros((0, 768), dtype=np.float32))
    with open(os.path.join(INDEX_DIR, "_ckpt_ids.json"), "w", encoding="utf-8") as f:
        json.dump(names_done, f)


def load_ckpt() -> tuple[list[str], list[np.ndarray]] | None:
    ep = os.path.join(INDEX_DIR, "_ckpt_emb.npy")
    ip = os.path.join(INDEX_DIR, "_ckpt_ids.json")
    if os.path.isfile(ep) and os.path.isfile(ip):
        emb = np.load(ep)
        with open(ip, encoding="utf-8") as f:
            ids = json.load(f)
        if len(ids) == emb.shape[0] and ids:
            print(f"从 checkpoint 恢复：已处理 {len(ids)} 张", flush=True)
            return ids, [emb]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=64, help="batch size")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    names = sorted(n for n in os.listdir(IMG_DIR) if n.endswith("_200w.jpg"))
    print(f"图片总数: {len(names)}  目录: {IMG_DIR}", flush=True)

    os.makedirs(INDEX_DIR, exist_ok=True)
    ckpt = load_ckpt()
    if ckpt:
        done_ids, feats = ckpt
        done_set = set(done_ids)
        names_todo = [n for n in names if n not in done_set]
    else:
        done_ids, feats, names_todo = [], [], list(names)
    print(f"待处理: {len(names_todo)} 张", flush=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model().to(device)
    print(f"model loaded on {device}, batch={args.batch}", flush=True)

    t0 = time.time()
    start_count = len(done_ids)
    skip_log = []
    for i in range(0, len(names_todo), args.batch):
        batch_names = names_todo[i:i + args.batch]
        imgs, ok_names = [], []
        for n in batch_names:
            try:
                with Image.open(os.path.join(IMG_DIR, n)) as im:
                    im.load()
                    img = orientation_first(im)
                    imgs.append(img.convert("RGB").resize(MODEL_INPUT, Image.BICUBIC))
                ok_names.append(n)
            except Exception as e:
                skip_log.append(f"{n}: {e}")
        if imgs:
            feats.append(embed_batch(model, device, imgs))
            done_ids.extend(ok_names)
        if (i // args.batch) % 20 == 0 or i + args.batch >= len(names_todo):
            dt = time.time() - t0
            processed = len(done_ids) - start_count
            print(f"  进度 {len(done_ids)}/{len(names)}  "
                  f"速度 {processed/max(dt,1e-9):.1f}/s  "
                  f"用时 {dt/60:.1f} 分钟", flush=True)
        if len(done_ids) % CKPT_EVERY < args.batch and feats:
            save_ckpt(done_ids, feats)

    M = np.concatenate(feats) if feats else np.zeros((0, 768), dtype=np.float32)
    card_ids = [os.path.splitext(n)[0] for n in done_ids]
    print(f"gallery embeddings: {M.shape}  ({(time.time()-t0)/60:.1f} 分钟)", flush=True)

    import faiss
    index = faiss.IndexFlatIP(M.shape[1])
    index.add(M)
    print(f"faiss index size: {index.ntotal}", flush=True)

    np.save(os.path.join(INDEX_DIR, "embeddings.npy"), M)
    with open(os.path.join(INDEX_DIR, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(card_ids, f, ensure_ascii=False)

    # self-check：100 张随机图，top-1 必须命中自己
    sample = rng.sample(range(len(card_ids)), min(100, len(card_ids)))
    hits = 0
    for idx in sample:
        scores, indices = index.search(M[idx:idx + 1], 3)
        if indices[0, 0] == idx:
            hits += 1
        else:
            print(f"  MISMATCH: query={card_ids[idx]} top1={card_ids[indices[0,0]]} "
                  f"score={scores[0,0]:.4f}", flush=True)
    print(f"self-check: {hits}/{len(sample)} top-1 hits", flush=True)

    if skip_log:
        with open(os.path.join(INDEX_DIR, "skipped_images.log"), "w", encoding="utf-8") as f:
            f.write("\n".join(skip_log))
        print(f"跳过损坏图片 {len(skip_log)} 张，见 skipped_images.log", flush=True)

    with open(os.path.join(INDEX_DIR, "version.txt"), "w", encoding="utf-8") as f:
        f.write(f"build_time_s: {time.time()-t0:.1f}\n")
        f.write(f"embedding_count: {M.shape[0]}\n")
        f.write(f"embedding_dim: {M.shape[1]}\n")
        f.write(f"index_type: IndexFlatIP\n")
        f.write(f"source: category_cards_search/03_Pokemon/images\n")

    # 清理 checkpoint
    for p in ("_ckpt_emb.npy", "_ckpt_ids.json"):
        fp = os.path.join(INDEX_DIR, p)
        if os.path.isfile(fp):
            os.remove(fp)
    print("=== Pokemon Index Build Complete ===", flush=True)


if __name__ == "__main__":
    main()
