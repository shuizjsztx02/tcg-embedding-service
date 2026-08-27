"""
Quick test: PP-OCRv4 with limit_side_len=480, threads=4, batch_num=12
"""
import sys, time, json
from pathlib import Path
import cv2
_HERE = Path(__file__).resolve().parent
_PROJ = _HERE.parent
if str(_PROJ) not in sys.path:
    sys.path.insert(0, str(_PROJ))
from script_temp.preprocess_ocr import OCRPreprocessor
from script_temp.ppocr_v4_engine import PPOCRv4Engine

pp = OCRPreprocessor(max_dim=640)
eng = PPOCRv4Engine(limit_side_len=480, batch_num=12, threads=4)

imgs = sorted(Path(_PROJ / "test-images").glob("*.jpg"))[:5]
if not imgs:
    print("No images found")
    sys.exit(1)

print("Testing 5 images with limit_side_len=480, threads=4, batch_num=12\n")
records = []
for p in imgs:
    raw = cv2.imread(str(p))
    if raw is None:
        continue
    t0 = time.perf_counter()
    proc = pp(raw)
    t1 = time.perf_counter()
    res, _ = eng.read(proc)
    t2 = time.perf_counter()
    prep = t1 - t0
    ocr = t2 - t1
    total = t2 - t0
    under = total < 2.0
    icon = "+" if under else "-"
    print(f"  [{icon}] {p.name}")
    print(f"      prep={prep:.3f}s ocr={ocr:.3f}s total={total:.3f}s blocks={len(res)}")
    for r in res[:3]:
        print(f"        [{r.confidence:.2f}] {r.text}")
    records.append(total)

avg = sum(records) / len(records)
under2 = sum(1 for r in records if r < 2.0)
print(f"\nAvg total: {avg:.3f}s, under 2s: {under2}/{len(records)}")
Path(_PROJ / "csv" / "ppocr_v4_quick_results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
print("Done")
