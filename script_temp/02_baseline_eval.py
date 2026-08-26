"""Baseline eval: native DINOv2 ViT-B/14 top-1 retrieval under simulated real-photo queries.

Index  = every library scan (landscape scans added under both rotations).
Query  = augmented copy of a sampled scan (perspective/glare/blur/... to mimic a phone photo).
Unknown = held-out ids masked from the index; their top-1 score is the impostor distribution.
"""
import argparse
import csv
import os
import random
import sys

import numpy as np
import torch
from PIL import Image, ImageEnhance, ImageFilter
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import orientation_candidates, to_model_input

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")
CSV_OUT = os.path.join(ROOT, "csv", "baseline_eval.csv")

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
    return f / np.linalg.norm(f, axis=1, keepdims=True)


def persp_coeffs(src_quad, out_size):
    # coeffs for PIL PERSPECTIVE so the 4 corners of out_size map onto src_quad
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = src_quad
    W, H = out_size
    A = np.array([
        [0, 0, 1, 0, 0, 0, 0, 0],
        [W, 0, 1, 0, 0, 0, -x1 * W, 0],
        [W, H, 1, 0, 0, 0, -x2 * W, -x2 * H],
        [0, H, 1, 0, 0, 0, 0, -x3 * H],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, W, 0, 1, -y1 * W, 0],
        [0, 0, 0, W, H, 1, -y2 * W, -y2 * H],
        [0, 0, 0, 0, H, 1, 0, -y3 * H],
    ], dtype=np.float64)
    b = np.array([x0, x1, x2, x3, y0, y1, y2, y3], dtype=np.float64)
    return np.linalg.solve(A, b).tolist()


def augment(img, rng):
    """Simulate a phone photo of the card: tilt, warp, glare, blur, color shift."""
    w, h = img.size
    m = 0.06
    quad = [
        (rng.uniform(-m, m) * w, rng.uniform(-m, m) * h),
        (w * (1 + rng.uniform(-m, m)), rng.uniform(-m, m) * h),
        (w * (1 + rng.uniform(-m, m)), h * (1 + rng.uniform(-m, m))),
        (rng.uniform(-m, m) * w, h * (1 + rng.uniform(-m, m))),
    ]
    bg = rng.randint(90, 200)
    img = img.transform((w, h), Image.PERSPECTIVE, persp_coeffs(quad, (w, h)),
                        Image.BICUBIC, fillcolor=(bg, bg, bg))
    if rng.random() < 0.6:
        img = img.rotate(rng.uniform(-4, 4), expand=False, fillcolor=(bg, bg, bg))
    if rng.random() < 0.35:  # glare streak
        # cheap diagonal band via rotated rectangle
        band = Image.new("L", (int(w * 1.5), int(h * 1.5)), 0)
        bw = int(rng.uniform(0.10, 0.25) * w)
        px = band.load()
        x0 = rng.randint(0, band.width - 1)
        for y in range(band.height):
            for x in range(max(0, x0 - bw), min(band.width, x0 + bw)):
                px[x, y] = rng.randint(50, 110)
        band = band.rotate(rng.uniform(-35, 35), expand=False)
        cx, cy = (w - band.width) // 2, (h - band.height) // 2
        img = Image.composite(Image.new("RGB", (w, h), (255, 255, 255)), img,
                              band.crop((max(0, -cx), max(0, -cy),
                                         max(0, -cx) + w, max(0, -cy) + h)))
    if rng.random() < 0.5:
        img = img.filter(ImageFilter.GaussianBlur(rng.uniform(0.4, 1.1)))
    img = ImageEnhance.Brightness(img).enhance(rng.uniform(0.8, 1.25))
    img = ImageEnhance.Contrast(img).enhance(rng.uniform(0.85, 1.15))
    img = ImageEnhance.Color(img).enhance(rng.uniform(0.75, 1.15))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-query", type=int, default=500)
    ap.add_argument("--n-unknown", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--batch", type=int, default=16)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    # Read valid file list from metadata.csv (skips corrupt files like 153316_200w.jpg)
    METADATA_CSV = os.path.join(ROOT, "csv", "metadata.csv")
    valid_names = []
    with open(METADATA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            valid_names.append(row["name"])
    names = sorted(valid_names)
    ids = [os.path.splitext(n)[0] for n in names]
    print(f"valid images: {len(names)}", flush=True)

    model = load_model()
    print("model loaded", flush=True)

    # index: every scan, landscape scans under both rotations
    rows, row_ids = [], []
    for n, cid in zip(names, ids):
        with Image.open(os.path.join(IMG_DIR, n)) as im:
            im.load()
            for cand in orientation_candidates(im):
                rows.append(to_model_input(cand))
                row_ids.append(cid)
    print(f"index rows: {len(rows)}", flush=True)
    M = embed_images(model, rows, args.batch)
    print(f"index embeddings: {M.shape}", flush=True)

    qs = rng.sample(ids, args.n_query + args.n_unknown)
    query_ids, unknown_ids = qs[:args.n_query], qs[args.n_query:]

    results = []
    qimgs = []
    for cid in query_ids:
        with Image.open(os.path.join(IMG_DIR, cid + ".jpg")) as im:
            im.load()
            cands = list(orientation_candidates(im))
            qimgs.append(to_model_input(augment(cands[0], rng)))
    Q = embed_images(model, qimgs, args.batch)
    sim = Q @ M.T
    for cid, s in zip(query_ids, sim):
        order = np.argsort(-s)
        results.append(["query", cid, row_ids[order[0]], float(s[order[0]]),
                        float(s[order[1]]), row_ids[order[0]] == cid])

    unknown_mask = np.array([r in set(unknown_ids) for r in row_ids])
    uimgs = []
    for cid in unknown_ids:
        with Image.open(os.path.join(IMG_DIR, cid + ".jpg")) as im:
            im.load()
            cands = list(orientation_candidates(im))
            uimgs.append(to_model_input(augment(cands[0], rng)))
    U = embed_images(model, uimgs, args.batch)
    usim = U @ M.T
    usim[:, unknown_mask] = -1.0
    for cid, s in zip(unknown_ids, usim):
        order = np.argsort(-s)
        results.append(["unknown", cid, row_ids[order[0]], float(s[order[0]]),
                        float(s[order[1]]), False])

    os.makedirs(os.path.dirname(CSV_OUT), exist_ok=True)
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "id", "top1_id", "top1_score", "top2_score", "hit"])
        wr.writerows(results)

    qr = [r for r in results if r[0] == "query"]
    ur = [r for r in results if r[0] == "unknown"]
    acc = np.mean([r[5] for r in qr])
    hit_scores = np.array([r[3] for r in qr if r[5]])
    miss_scores = np.array([r[3] for r in qr if not r[5]])
    imp_scores = np.array([r[3] for r in ur])
    print(f"top1 accuracy: {acc:.4f} ({int(acc * len(qr))}/{len(qr)})")
    print(f"genuine top1 score  p5/p50/p95: {np.percentile(hit_scores, [5, 50, 95]).round(3) if len(hit_scores) else 'n/a'}")
    if len(miss_scores):
        print(f"miss top1 score     p5/p50/p95: {np.percentile(miss_scores, [5, 50, 95]).round(3)}")
    print(f"impostor top1 score p5/p50/p95: {np.percentile(imp_scores, [5, 50, 95]).round(3)}")
    print("=== Baseline Eval Complete ===")


if __name__ == "__main__":
    main()
