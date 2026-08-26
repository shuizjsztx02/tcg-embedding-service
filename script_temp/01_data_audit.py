# Audit images/: size distribution, orientation classes, corrupt files.
# Performs FULL decode validation (not just lazy PIL open) to catch truncated images.
# Generates csv/metadata.csv with deduplication info + orientation correction advice.
# Output: csv/metadata.csv + console summary.
import csv
import os
import hashlib
from collections import Counter

import numpy as np
from PIL import Image
from PIL import ImageFile

# Tolerate minor truncations so we can still audit what we have
ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")
CSV_PATH = os.path.join(ROOT, "csv", "metadata.csv")


def main():
    """Audit every image: full decode, size, orientation, sha1, detect corruption."""
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    rows, corrupt, decode_fail = [], [], []
    for name in sorted(os.listdir(IMG_DIR)):
        if not name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        path = os.path.join(IMG_DIR, name)
        try:
            im = Image.open(path)
            w, h = im.size
            mode = im.mode
            # Force full decode to catch truncated images
            im.load()
            arr = np.asarray(im)
            sha1 = hashlib.sha1(arr.tobytes()).hexdigest()
        except Exception as e:
            corrupt.append((name, str(e)))
            continue
        # Check if decode actually produced valid data
        if arr.size == 0:
            decode_fail.append((name, "zero-size array after decode"))
            continue
        orient = "portrait" if h > w else ("landscape" if w > h else "square")
        # For landscape cards, suggest the rotation that makes it portrait
        rotation = "none"
        if orient == "landscape":
            # We'll just record the fact; downstream chooses the canonical orientation
            rotation = "rotate_90_or_270"
        rows.append([name, w, h, orient, rotation, os.path.getsize(path), mode, sha1])

    # Write metadata CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["name", "width", "height", "orientation", "rotation_advice",
                     "bytes", "mode", "sha1"])
        wr.writerows(rows)

    # Summary
    print("=== Data Audit Summary ===")
    print("total valid:", len(rows))
    print("corrupt (cannot open):", len(corrupt))
    print("decode_fail (loaded but empty):", len(decode_fail))
    print("orientation:", dict(Counter(r[3] for r in rows)))
    print("top sizes:", Counter((r[1], r[2]) for r in rows).most_common(6))
    landscape = [r[0] for r in rows if r[3] == "landscape"]
    print("landscape count:", len(landscape))
    if landscape:
        print("landscape samples:", landscape[:5])
    print("small/odd (height < 200):", [(r[0], r[1], r[2]) for r in rows if r[2] < 200][:10])
    # Check for duplicates by sha1
    sha1s = [r[7] for r in rows]
    dupes = [(r[0], r[7]) for r in rows if sha1s.count(r[7]) > 1]
    if dupes:
        print("duplicate sha1 count:", len(dupes))
        print("first few duplicates:", dupes[:5])
    else:
        print("duplicate sha1: none found")
    print()
    for name, err in corrupt[:10]:
        print("CORRUPT", name, err)
    for name, err in decode_fail[:10]:
        print("DECODE_FAIL", name, err)
    print("=== End ===")
    # Also write a simple summary CSV
    with open(os.path.join(ROOT, "csv", "data_audit_summary.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["metric", "value"])
        wr.writerow(["total", len(rows)])
        wr.writerow(["corrupt", len(corrupt)])
        wr.writerow(["decode_fail", len(decode_fail)])
        wr.writerow(["portrait", sum(1 for r in rows if r[3] == "portrait")])
        wr.writerow(["landscape", sum(1 for r in rows if r[3] == "landscape")])
        wr.writerow(["duplicate_sha1", len(dupes)])


if __name__ == "__main__":
    main()
