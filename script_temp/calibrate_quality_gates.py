"""Calibrate quality-gate thresholds (blur / glare / card-area) on real photos.

Usage:
    python script_temp/calibrate_quality_gates.py [--n 60] [--dir test-images]

Outputs percentile stats so thresholds are grounded in real phone photos,
per the preprocessing guideline: do not copy fixed Laplacian numbers blindly.
"""
import argparse
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from preprocess import detect_card, order_points


def warp_card(img, quad, out_w=504, out_h=704):
    dst = np.array(
        [[0, 0], [out_w - 1, 0], [out_w - 1, out_h - 1], [0, out_h - 1]],
        dtype=np.float32,
    )
    M = cv2.getPerspectiveTransform(quad, dst)
    arr = np.array(img.convert("RGB"))
    return cv2.warpPerspective(arr, M, (out_w, out_h), flags=cv2.INTER_CUBIC)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test-images"))
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    files = [f for f in os.listdir(args.dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.Random(args.seed).shuffle(files)
    files = files[: args.n]

    n_found, n_total = 0, 0
    area_ratios, blurs, glares = [], [], []

    for name in files:
        path = os.path.join(args.dir, name)
        try:
            img = Image.open(path)
            img.load()
        except Exception as e:
            print(f"skip {name}: {e}")
            continue
        n_total += 1
        img_rgb = img.convert("RGB")
        quad = detect_card(img_rgb)
        if quad is None:
            print(f"NOQUAD {name} size={img.size}")
            continue
        n_found += 1
        h, w = np.array(img_rgb).shape[:2]
        area_ratios.append(cv2.contourArea(quad) / (h * w))
        card = warp_card(img_rgb, quad)
        gray = cv2.cvtColor(card, cv2.COLOR_RGB2GRAY)
        blurs.append(cv2.Laplacian(gray, cv2.CV_64F).var())
        glares.append(float(np.all(card >= 240, axis=2).mean()))

    def pct(xs, p):
        return float(np.percentile(np.array(xs), p)) if xs else float("nan")

    print(f"\nsamples={n_total} quad_found={n_found} ({100*n_found/max(n_total,1):.0f}%)")
    for label, xs in [("area_ratio", area_ratios), ("laplacian_var", blurs), ("glare_ratio", glares)]:
        row = " ".join(f"p{p}={pct(xs, p):.4f}" for p in (5, 10, 25, 50, 75, 90, 95))
        print(f"{label:14s} {row}")


if __name__ == "__main__":
    main()
