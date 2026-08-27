"""
run_ocr_pipeline.py — Pipeline: OpenCV preprocess → EasyOCR.

Usage:
    python script_temp\run_ocr_pipeline.py <image_path> [options]

Examples:
    python script_temp\run_ocr_pipeline.py test-images\f52ee7479b6-20260722-22fecf*.jpg
    python script_temp\run_ocr_pipeline.py test-images\\*.jpg --batch --max-dim 1600
    python script_temp\run_ocr_pipeline.py test-images\f52ee7479b6-20260722-22fecf*.jpg --binarize
"""

import argparse
import json
import sys
import time
from pathlib import Path

import cv2

# Add project root so script_temp/ imports work regardless of CWD
_HERE = Path(__file__).resolve().parent
_PROJ = _HERE.parent
if str(_PROJ) not in sys.path:
    sys.path.insert(0, str(_PROJ))

from script_temp.preprocess_ocr import OCRPreprocessor  # noqa: E402
from script_temp.ocr_engine import create_engine  # noqa: E402


def process_one(
    path: Path,
    preprocessor: OCRPreprocessor,
    engine: object,
    *,
    binarize: bool = False,
    verbose: bool = True,
) -> dict:
    """Run preprocess → OCR on a single image and return results dict."""
    img = cv2.imread(str(path))
    if img is None:
        return {"path": str(path), "error": f"cannot read image"}

    # --- Step 1: Preprocess ---
    t0 = time.perf_counter()
    processed = preprocessor(img, binarize=binarize)
    t1 = time.perf_counter()
    prep_time = t1 - t0

    # --- Step 2: OCR ---
    results, ocr_time = engine.read(processed)

    out = {
        "path": str(path),
        "shape": [int(v) for v in img.shape],
        "preprocess_time_s": round(prep_time, 3),
        "ocr_time_s": round(ocr_time, 3),
        "total_time_s": round(prep_time + ocr_time, 3),
        "num_text_blocks": len(results),
        "text_blocks": [
            {
                "text": r.text,
                "confidence": round(r.confidence, 3),
                "bbox": [[round(float(v), 1) for v in pt] for pt in r.bbox],
            }
            for r in results
        ],
    }

    if verbose:
        print(f"\n{'='*60}")
        print(f"File: {path.name}")
        print(f"{'='*60}")
        print(f"  Preprocess: {prep_time:.3f}s | OCR: {ocr_time:.3f}s | Total: {out['total_time_s']:.3f}s")
        print(f"  Text blocks found: {len(results)}")
        for r in results:
            print(f"  [{r.confidence:.2f}] {r.text}")
        print()

    return out


def main():
    p = argparse.ArgumentParser(
        description="OpenCV preprocess → EasyOCR pipeline for card images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("input", nargs="+", help="Image path(s) or glob pattern")
    p.add_argument("--max-dim", type=int, default=1200, help="Max image dimension (default: 1200)")
    p.add_argument("--binarize", action="store_true", help="Apply adaptive threshold binarization")
    p.add_argument("--json", action="store_true", help="Output JSON to stdout")
    p.add_argument("--batch", action="store_true", help="Process multiple images (overrides --json)")
    args = p.parse_args()

    # Resolve paths
    paths = []
    for pat in args.input:
        expanded = list(Path(_PROJ).glob(pat)) if "*" in pat or "?" in pat else [Path(pat).resolve()]
        paths.extend(expanded)
    paths = sorted(set(p for p in paths if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")))

    if not paths:
        print("No matching image files found.", file=sys.stderr)
        sys.exit(1)

    auto_batch = len(paths) > 1
    if auto_batch:
        args.batch = True
        args.json = True

    print(f"Processing {len(paths)} image(s) ...")
    print(f"  Preprocessor: max_dim={args.max_dim}, binarize={args.binarize}")
    print(f"  OCR: RapidOCR (ONNX, PaddleOCR models)")

    preprocessor = OCRPreprocessor(max_dim=args.max_dim)
    engine = create_engine("rapidocr")

    all_results = []
    for path in paths:
        result = process_one(
            path,
            preprocessor,
            engine,
            binarize=args.binarize,
            verbose=not args.json,
        )
        all_results.append(result)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))

    # Summary
    success = [r for r in all_results if "error" not in r]
    failed = [r for r in all_results if "error" in r]
    if success:
        avg_time = sum(r["total_time_s"] for r in success) / len(success)
        total_text = sum(r["num_text_blocks"] for r in success)
        print(f"\nSummary: {len(success)} ok, {len(failed)} failed")
        print(f"  Avg total time per image: {avg_time:.3f}s")
        print(f"  Total text blocks found: {total_text}")


if __name__ == "__main__":
    main()
