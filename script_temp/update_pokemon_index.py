#!/usr/bin/env python3
"""增量更新 pokemon-index：将 85_Pokemon_Japan 的图片向量化后追加到现有索引。

用法：
  python script_temp/update_pokemon_index.py [--batch 64]

流程：
  1. 加载 pokemon-index/embeddings.npy + ids.json（现有索引）
  2. 扫描 85_Pokemon_Japan/images，跳过已在 ids.json 中的文件
  3. DINOv2 提取新图 embedding（与 build_pokemon_index.py 同一预处理管线）
  4. 追加到现有矩阵，重建 faiss IndexFlatIP
  5. 保存回 pokemon-index/
  6. 自检：随机抽 100 张（含新旧），top-1 命中率 = 100%
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_IMG_DIR = os.path.join(ROOT, "category_cards_search", "85_Pokemon_Japan", "images")
INDEX_DIR = os.path.join(ROOT, "pokemon-index")

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
MODEL_INPUT = (168, 224)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=64, help="batch size")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    # 1. 加载现有索引
    emb_path = os.path.join(INDEX_DIR, "embeddings.npy")
    ids_path = os.path.join(INDEX_DIR, "ids.json")
    if not os.path.isfile(emb_path) or not os.path.isfile(ids_path):
        print("错误：pokemon-index 不存在，请先运行 build_pokemon_index.py", flush=True)
        return

    old_emb = np.load(emb_path)
    with open(ids_path, encoding="utf-8") as f:
        old_ids: list[str] = json.load(f)
    print(f"现有索引: {len(old_ids)} 张, shape={old_emb.shape}", flush=True)

    # 2. 扫描新目录，跳过已存在的
    existing_set = set(old_ids)
    new_names = sorted(
        n for n in os.listdir(NEW_IMG_DIR)
        if n.endswith("_200w.jpg")
    )
    todo = [n for n in new_names if os.path.splitext(n)[0] not in existing_set]
    print(f"85_Pokemon_Japan 总数: {len(new_names)}, 待处理(跳过重复): {len(todo)}", flush=True)

    if not todo:
        print("没有新图片需要处理，索引无变化", flush=True)
        return

    # 3. 提取 embedding
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model().to(device)
    print(f"model loaded on {device}, batch={args.batch}", flush=True)

    t0 = time.time()
    new_feats, new_done = [], []
    skip_log = []
    for i in range(0, len(todo), args.batch):
        batch_names = todo[i:i + args.batch]
        imgs, ok_names = [], []
        for n in batch_names:
            try:
                with Image.open(os.path.join(NEW_IMG_DIR, n)) as im:
                    im.load()
                    img = orientation_first(im)
                    imgs.append(img.convert("RGB").resize(MODEL_INPUT, Image.BICUBIC))
                ok_names.append(n)
            except Exception as e:
                skip_log.append(f"{n}: {e}")
        if imgs:
            new_feats.append(embed_batch(model, device, imgs))
            new_done.extend(ok_names)
        if (i // args.batch) % 20 == 0 or i + args.batch >= len(todo):
            dt = time.time() - t0
            print(f"  进度 {len(new_done)}/{len(todo)}  速度 {len(new_done)/max(dt,1e-9):.1f}/s  用时 {dt/60:.1f} 分钟", flush=True)

    M_new = np.concatenate(new_feats) if new_feats else np.zeros((0, 768), dtype=np.float32)
    new_card_ids = [os.path.splitext(n)[0] for n in new_done]
    print(f"新图 embedding: {M_new.shape}  ({(time.time()-t0)/60:.1f} 分钟)", flush=True)

    # 4. 合并
    M_all = np.concatenate([old_emb, M_new], axis=0).astype(np.float32)
    all_ids = old_ids + new_card_ids
    print(f"合并后索引: {len(all_ids)} 张, shape={M_all.shape}", flush=True)

    import faiss
    index = faiss.IndexFlatIP(M_all.shape[1])
    index.add(M_all)
    print(f"faiss index size: {index.ntotal}", flush=True)

    # 5. 保存
    np.save(emb_path, M_all)
    with open(ids_path, "w", encoding="utf-8") as f:
        json.dump(all_ids, f, ensure_ascii=False)
    print(f"已保存: {emb_path}, {ids_path}", flush=True)

    # self-check：100 张随机图（含新旧），top-1 必须命中自己
    sample = rng.sample(range(len(all_ids)), min(100, len(all_ids)))
    hits = 0
    for idx in sample:
        scores, indices = index.search(M_all[idx:idx + 1], 3)
        if indices[0, 0] == idx:
            hits += 1
        else:
            print(f"  MISMATCH: query={all_ids[idx]} top1={all_ids[indices[0,0]]} "
                  f"score={scores[0,0]:.4f}", flush=True)
    print(f"self-check: {hits}/{len(sample)} top-1 hits ({100 * hits / len(sample):.0f}%)", flush=True)

    if skip_log:
        with open(os.path.join(INDEX_DIR, "skipped_85_images.log"), "w", encoding="utf-8") as f:
            f.write("\n".join(skip_log))
        print(f"跳过损坏图片 {len(skip_log)} 张，见 skipped_85_images.log", flush=True)

    # 更新 version.txt
    build_time = time.time() - t0
    with open(os.path.join(INDEX_DIR, "version.txt"), "w", encoding="utf-8") as f:
        f.write(f"build_time_s: {build_time:.1f}\n")
        f.write(f"embedding_count: {M_all.shape[0]}\n")
        f.write(f"embedding_dim: {M_all.shape[1]}\n")
        f.write(f"index_type: IndexFlatIP\n")
        f.write(f"source: category_cards_search/03_Pokemon/images + 85_Pokemon_Japan/images\n")
    print("=== Update Complete ===", flush=True)


if __name__ == "__main__":
    main()
