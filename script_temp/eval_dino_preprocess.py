"""Offline A/B retrieval on labeled photos or a small synthetic gallery sample.

CSV columns: image_path,card_id. Use manually verified IDs for real accuracy.
--synthetic N samples N gallery cards, never loads the entire image library.
--legacy-file may point to a saved pre-change preprocess.py for reproducibility.
"""
import argparse
import csv
import importlib.util
import json
import os
import random
import time

import cv2
import faiss
import numpy as np
import torch
from PIL import Image, ImageEnhance, ImageFilter

from dino_search import embed_candidates, search_image


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gallery_path(card_id):
    for category in ("03_Pokemon", "85_Pokemon_Japan"):
        path = os.path.join(ROOT, "category_cards_search", category, "images", card_id + ".jpg")
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(card_id)


def synthetic_photo(card, mode):
    if mode == "clean":
        return card.copy()
    arr = np.asarray(card.resize((210, 294)))
    canvas = np.full((520, 540, 3), (60, 70, 80), dtype=np.uint8)
    src = np.array([[0, 0], [209, 0], [209, 293], [0, 293]], np.float32)
    dst = np.array([[149, 80], [375, 110], [340, 430], [120, 389]], np.float32)
    transform = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(arr, transform, (540, 520))
    mask = cv2.warpPerspective(np.full((294, 210), 255, np.uint8), transform, (540, 520)) > 0
    canvas[mask] = warped[mask]
    photo = Image.fromarray(canvas)
    if mode == "sideways":
        photo = photo.rotate(90, expand=True)
    elif mode == "upside_down":
        photo = photo.rotate(180)
    elif mode == "dark":
        photo = ImageEnhance.Brightness(photo).enhance(.5)
    elif mode == "bright":
        photo = ImageEnhance.Brightness(photo).enhance(1.45)
    elif mode == "blur":
        photo = photo.filter(ImageFilter.GaussianBlur(1.2))
    elif mode == "glare":
        arr = np.asarray(photo).copy()
        yy, xx = np.mgrid[:520, :540]
        alpha = (.85 * np.exp(-((xx - 265) ** 2 / 1000 + (yy - 220) ** 2 / 9000)))[:, :, None]
        photo = Image.fromarray(np.clip(arr * (1 - alpha) + 255 * alpha, 0, 255).astype(np.uint8))
    return photo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest")
    parser.add_argument("--synthetic", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--legacy-file", default=os.path.join(ROOT, "script_temp", "preprocess.py"))
    parser.add_argument("--hub-dir", default=os.path.join(torch.hub.get_dir(), "facebookresearch_dinov2_main"))
    parser.add_argument("--output-dir", default=os.path.join(ROOT, "script_temp", "temp", "dino_preprocess", "evaluation"))
    args = parser.parse_args()
    if not args.manifest and args.synthetic <= 0:
        parser.error("provide --manifest or --synthetic")
    os.makedirs(args.output_dir, exist_ok=True)
    torch.set_num_threads(args.threads)
    cv2.setNumThreads(1)
    faiss.omp_set_num_threads(args.threads)
    model = torch.hub.load(args.hub_dir, "dinov2_vitb14", source="local", pretrained=True).eval()
    ids_path = os.path.join(ROOT, "pokemon-index", "ids.json")
    with open(ids_path, encoding="utf-8") as f:
        ids = json.load(f)
    embeddings = np.load(os.path.join(ROOT, "pokemon-index", "embeddings.npy"))
    if len(ids) != len(embeddings):
        raise ValueError("index IDs and vectors differ in length")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    spec = importlib.util.spec_from_file_location("legacy_preprocess", args.legacy_file)
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    samples = []
    if args.manifest:
        with open(args.manifest, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                path = row["image_path"]
                if not os.path.isabs(path):
                    path = os.path.join(ROOT, path)
                with Image.open(path) as im:
                    samples.append((os.path.basename(path), row["card_id"], im.copy()))
    for card_id in random.Random(args.seed).sample(ids, args.synthetic):
        with Image.open(gallery_path(card_id)) as card:
            for mode in ("clean", "perspective", "sideways", "upside_down", "dark", "bright", "blur", "glare"):
                samples.append((card_id + "_" + mode, card_id, synthetic_photo(card.convert("RGB"), mode)))
    # Warm-up excludes first inference initialization from the comparison.
    embed_candidates(model, [Image.new("RGB", (168, 224))])
    rows = []
    for name, expected, photo in samples:
        start = time.perf_counter()
        legacy_image = legacy.preprocess_query(photo)
        legacy_cands = list(legacy.orientation_candidates(legacy_image))
        features = embed_candidates(model, legacy_cands)
        scores, indices = index.search(features, 5)
        winner = int(np.argmax(scores[:, 0]))
        old_ids = [ids[int(i)] for i in indices[winner]]
        old_ms = (time.perf_counter() - start) * 1000
        ranked, selected, meta = search_image(photo, model, index, ids)
        row = {"sample": name, "expected": expected, "in_index": expected in ids,
               "old_top1": old_ids[0], "new_top1": ranked[0]["card_id"],
               "old_top1_correct": old_ids[0] == expected, "new_top1_correct": ranked[0]["card_id"] == expected,
               "old_top5_correct": expected in old_ids, "new_top5_correct": expected in [r["card_id"] for r in ranked],
               "old_score": round(float(scores[winner, 0]), 4), "new_score": round(ranked[0]["score"], 4),
               "old_ms": round(old_ms, 1), "new_ms": meta["total_ms"], "preprocessing": meta}
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "preprocessing"}), flush=True)
        if len(samples) <= 10:
            photo.save(os.path.join(args.output_dir, name + "_input.png"))
            legacy_cands[winner].save(os.path.join(args.output_dir, name + "_before.png"))
            selected.save(os.path.join(args.output_dir, name + "_after.png"))
        with open(os.path.join(args.output_dir, "results.jsonl"), "a" if len(rows) > 1 else "w", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = {"samples": len(rows), "synthetic_gallery_cards": args.synthetic, "index_size": len(ids)}
    for version in ("old", "new"):
        summary[version] = {"top1": sum(r[version + "_top1_correct"] for r in rows),
                            "top5": sum(r[version + "_top5_correct"] for r in rows),
                            "median_ms": round(float(np.median([r[version + "_ms"] for r in rows])), 1)}
    with open(os.path.join(args.output_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
