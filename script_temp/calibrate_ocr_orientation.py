"""Calibrate OCR orientation-fallback threshold on real photos.

Runs PP-OCRv4 on the preprocessed card at 0 and 180 degrees and compares
sum(confidence), so the "retry other orientation" cutoff is data-driven.

Usage:
    python script_temp/calibrate_ocr_orientation.py [--n 4]
"""
import argparse
import os
import random

import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from preprocess import preprocess_for_ocr
from ppocr_v4_engine import PPOCRv4Engine

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(ROOT, "test-images"))
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    files = sorted(f for f in os.listdir(args.dir) if f.lower().endswith(".jpg"))
    random.Random(args.seed).shuffle(files)
    files = files[: args.n]

    engine = PPOCRv4Engine(threads=4)

    for name in files:
        img = Image.open(os.path.join(args.dir, name))
        img.load()
        card, meta = preprocess_for_ocr(img)
        print(f"\n{name} size={card.size} quad={meta['quad_found']} warnings={meta['warnings']}")
        arr = np.asarray(card.convert("RGB"))[:, :, ::-1].copy()
        for label, cand in [("0deg", arr), ("180deg", arr[::-1, ::-1].copy())]:
            results, elapsed = engine.read(cand)
            quality = sum(r.confidence for r in results)
            print(f"  {label:6s} blocks={len(results):2d} sum_conf={quality:6.2f} elapsed={elapsed:.2f}s")


if __name__ == "__main__":
    main()
