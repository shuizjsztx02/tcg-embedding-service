"""
benchmark_ocr.py — Compare RapidOCR (PP-OCRv3) vs PP-OCRv4 on test images.

Usage:
    python script_temp\benchmark_ocr.py
"""

import json
import sys
import time
from pathlib import Path

import cv2

_HERE = Path(__file__).resolve().parent
_PROJ = _HERE.parent
if str(_PROJ) not in sys.path:
    sys.path.insert(0, str(_PROJ))

from script_temp.preprocess_ocr import OCRPreprocessor
from script_temp.ocr_engine import create_engine
from script_temp.ppocr_v4_engine import PPOCRv4Engine


def main():
    # Test images (first 5)
    test_dir = _PROJ / "test-images"
    images = sorted(test_dir.glob("*.jpg"))[:5]

    if not images:
        print("No test images found!")
        return

    print(f"Testing {len(images)} images\n")

    # Preprocessor
    preprocessor = OCRPreprocessor(max_dim=1200)

    # Engines
    v3_engine = create_engine("rapidocr")
    v4_engine = PPOCRv4Engine()

    all_results = []

    for idx, img_path in enumerate(images):
        print(f"{'='*60}")
        print(f"Image {idx+1}: {img_path.name}")
        print(f"{'='*60}")

        raw = cv2.imread(str(img_path))
        if raw is None:
            print(f"  Cannot read {img_path.name}")
            continue

        # Preprocess
        processed = preprocessor(raw)

        # --- RapidOCR (PP-OCRv3) ---
        t0 = time.perf_counter()
        v3_results, v3_elapsed = v3_engine.read(processed)
        v3_time = time.perf_counter() - t0

        # --- PP-OCRv4 ---
        t0 = time.perf_counter()
        # Note: PP-OCRv4 engine does its own preprocessing internally (det resize + norm)
        # We pass the raw image so it can crop from original resolution
        v4_results, v4_elapsed = v4_engine.read(raw)
        v4_time = time.perf_counter() - t0

        print(f"  RapidOCR (PP-OCRv3): {v3_time:.3f}s, {len(v3_results)} blocks")
        print(f"  PP-OCRv4:            {v4_time:.3f}s, {len(v4_results)} blocks")
        print(f"  Speedup:             {v3_time/v4_time:.1f}x" if v4_time > 0 else "")

        # Print first 5 texts from each
        print(f"\n  RapidOCR texts:")
        for r in v3_results[:5]:
            print(f"    [{r.confidence:.2f}] {r.text}")
        print(f"  PP-OCRv4 texts:")
        for r in v4_results[:5]:
            print(f"    [{r.confidence:.2f}] {r.text}")
        print()

        all_results.append({
            "image": img_path.name,
            "rapidocr": {"time_s": v3_time, "blocks": len(v3_results), "texts": [r.text for r in v3_results[:10]]},
            "ppocrv4": {"time_s": v4_time, "blocks": len(v4_results), "texts": [r.text for r in v4_results[:10]]},
        })

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    v3_times = [r["rapidocr"]["time_s"] for r in all_results]
    v4_times = [r["ppocrv4"]["time_s"] for r in all_results]
    print(f"  RapidOCR avg: {sum(v3_times)/len(v3_times):.3f}s")
    print(f"  PP-OCRv4 avg: {sum(v4_times)/len(v4_times):.3f}s")
    if v4_times:
        print(f"  Avg speedup:  {sum(v3_times)/sum(v4_times):.1f}x")

    # Save JSON
    out_path = _PROJ / "csv" / "ocr_benchmark_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()