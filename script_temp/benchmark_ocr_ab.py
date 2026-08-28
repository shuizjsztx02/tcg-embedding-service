"""A/B: old OCR path (search preprocess) vs new path (OCR preprocess + 180 fallback)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
from preprocess import preprocess_query, preprocess_for_ocr
from ppocr_v4_engine import PPOCRv4Engine

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "test-images")

files = sorted(f for f in os.listdir(IMG_DIR) if f.lower().endswith(".jpg"))
step = max(1, len(files) // 8)
sample = files[::step][:8]

engine = PPOCRv4Engine(threads=2)


def run(arr_rgb):
    return engine.read(np.ascontiguousarray(arr_rgb[:, :, ::-1]))


def quality(res):
    return sum(r.confidence for r in res)


print(f"{'file':<20} {'OLD blk/conf/s':>22} {'NEW blk/conf/s':>22} flipped")
old_total = new_total = 0.0
for name in sample:
    img = Image.open(os.path.join(IMG_DIR, name))
    img.load()

    old_img = preprocess_query(img)
    r_old, t_old = run(np.asarray(old_img, dtype=np.uint8))

    new_img, meta = preprocess_for_ocr(img)
    arr = np.asarray(new_img, dtype=np.uint8)
    r_new, t_new = run(arr)
    flipped = ""
    if quality(r_new) < 5.0:
        r2, t2 = run(arr[::-1, ::-1])
        t_new += t2
        if quality(r2) > quality(r_new):
            r_new = r2
            flipped = " <-- 180deg"

    old_total += quality(r_old)
    new_total += quality(r_new)
    print(f"{name[:18]:<20} {len(r_old):>4}blk {quality(r_old):>6.2f} {t_old:>5.2f}s "
          f"{len(r_new):>6}blk {quality(r_new):>6.2f} {t_new:>5.2f}s{flipped}")

print(f"\ntotal sum_conf  old={old_total:.2f}  new={new_total:.2f}")
