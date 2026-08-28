"""Diagnose current preprocessing on real test photos (read-only, no model)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cv2
import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
from preprocess import preprocess_for_search, preprocess_for_ocr, detect_card, normalize_orientation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "test-images")
OUT_DIR = os.path.join(ROOT, "script_temp", "_diag_out")
os.makedirs(OUT_DIR, exist_ok=True)

files = sorted(f for f in os.listdir(IMG_DIR) if f.lower().endswith(".jpg"))
# deterministic sample across the set
step = max(1, len(files) // 12)
sample = files[::step][:12]

print(f"total={len(files)} sample={len(sample)}")
print(f"{'file':<46} {'quad':<5} {'area_r':<7} {'blur':<7} {'glare':<7} out_size")
for name in sample:
    path = os.path.join(IMG_DIR, name)
    img = Image.open(path)
    img.load()
    raw_size = img.size
    norm = normalize_orientation(img)
    quad = detect_card(norm)
    card_s, meta_s = preprocess_for_search(img)
    print(f"{name:<46} {str(meta_s['quad_found']):<5} "
          f"{meta_s['quad_area_ratio']!s:<7} {meta_s['blur_var']:<7} {meta_s['glare_ratio']:<7} "
          f"{raw_size}->{card_s.size}")
    # save side-by-side: original (thumbnail) vs search-preprocessed
    th = norm.copy()
    th.thumbnail((300, 300))
    cs = card_s.copy()
    cs.thumbnail((300, 300))
    h = max(th.size[1], cs.size[1])
    canvas = np.full((h, th.size[0] + cs.size[0] + 10, 3), 40, np.uint8)
    canvas[0:th.size[1], 0:th.size[0]] = np.array(th.convert("RGB"))
    canvas[0:cs.size[1], th.size[0] + 10:] = np.array(cs.convert("RGB"))
    cv2.imwrite(os.path.join(OUT_DIR, name), cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR))
print(f"\nside-by-side images -> {OUT_DIR}")
