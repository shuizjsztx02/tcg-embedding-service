"""
test_ppocr_v4_pipeline.py - 测试 PP-OCRv4 + OpenCV 预处理流水线

流程: OpenCV 预处理 -> PP-OCRv4 文字检测 -> PP-OCRv4 文字识别

对比两种配置:
  1. Baseline: 原图 -> PP-OCRv4 (默认 736 limit_side_len)
  2. Optimized: 预处理 -> PP-OCRv4 (800 max_dim + 640 limit_side_len)

测试 test-images/ 前 5 张, 目标 <2s/张。
"""

import sys
import time
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np

_HERE = Path(__file__).resolve().parent
_PROJ = _HERE.parent
if str(_PROJ) not in sys.path:
    sys.path.insert(0, str(_PROJ))

from script_temp.preprocess_ocr import OCRPreprocessor
from script_temp.ppocr_v4_engine import PPOCRv4Engine
from script_temp.ocr_engine import OCRResult


@dataclass
class PipelineConfig:
    name: str
    preprocess: bool
    max_dim: int = 1200
    limit_side_len: int = 736
    batch_num: int = 6
    det_thresh: float = 0.3
    ir_optim: bool = False
    threads: int = 4


CONFIGS = [
    PipelineConfig(
        name="Baseline: 原图 -> PP-OCRv4",
        preprocess=False,
        limit_side_len=736,
        batch_num=6,
        ir_optim=False,
        threads=4,
    ),
    PipelineConfig(
        name="Optimized: 预处理 -> PP-OCRv4",
        preprocess=True,
        max_dim=800,
        limit_side_len=640,
        batch_num=8,
        ir_optim=False,
        threads=4,
    ),
    PipelineConfig(
        name="Aggressive: 预处理 -> PP-OCRv4 (480)",
        preprocess=True,
        max_dim=640,
        limit_side_len=480,
        batch_num=12,
        ir_optim=False,
        threads=6,
    ),
]


def run_pipeline(
    img: np.ndarray,
    config: PipelineConfig,
    preprocessor: OCRPreprocessor,
    engine: PPOCRv4Engine,
) -> Tuple[List[OCRResult], float, float]:
    """执行流水线: (可选预处理) -> PP-OCRv4, 返回 (results, prep_time, ocr_time)."""
    prep_time = 0.0
    input_img = img

    if config.preprocess:
        t0 = time.perf_counter()
        input_img = preprocessor(img)
        prep_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    results, _ = engine.read(input_img)
    ocr_time = time.perf_counter() - t0

    return results, prep_time, ocr_time


def main():
    test_dir = _PROJ / "test-images"
    images = sorted(test_dir.glob("*.jpg"))[:5]

    if not images:
        print("错误: test-images/ 下未找到图片")
        return

    print(f"测试 {len(images)} 张图片, {len(CONFIGS)} 种配置")
    print(f"{'='*70}")

    all_max_dim = max(c.max_dim for c in CONFIGS if c.preprocess)
    preprocessor = OCRPreprocessor(max_dim=all_max_dim) if all_max_dim else None

    engines = []
    for config in CONFIGS:
        eng = PPOCRv4Engine(
            limit_side_len=config.limit_side_len,
            batch_num=config.batch_num,
            det_thresh=config.det_thresh,
            ir_optim=config.ir_optim,
            threads=config.threads,
        )
        engines.append(eng)

    all_records = []

    for img_idx, img_path in enumerate(images):
        print(f"\n{'='*70}")
        print(f"图片 {img_idx+1}: {img_path.name}")
        print(f"{'='*70}")

        raw = cv2.imread(str(img_path))
        if raw is None:
            print(f"  [错误] 无法读取图片")
            continue

        raw_h, raw_w = raw.shape[:2]
        print(f"  原始尺寸: {raw_w}x{raw_h}")

        for config, engine in zip(CONFIGS, engines):
            results, prep_time, ocr_time = run_pipeline(raw.copy(), config, preprocessor, engine)
            total = prep_time + ocr_time
            under_2s = total < 2.0

            icon = "+" if under_2s else "-"
            print(f"\n  [{icon}] {config.name}")
            print(f"      预处理: {prep_time:.3f}s | OCR: {ocr_time:.3f}s | 总计: {total:.3f}s")
            print(f"      文本块: {len(results)}")
            for r in results[:5]:
                print(f"        [{r.confidence:.2f}] {r.text}")
            if len(results) > 5:
                print(f"        ... 还有 {len(results)-5} 个")

            all_records.append({
                "image": img_path.name,
                "config": config.name,
                "preprocess_s": round(prep_time, 3),
                "ocr_s": round(ocr_time, 3),
                "total_s": round(total, 3),
                "under_2s": under_2s,
                "blocks": len(results),
                "texts": [r.text for r in results[:10]],
            })

    print(f"\n{'='*70}")
    print("汇总")
    print(f"{'='*70}")
    for config_name in [c.name for c in CONFIGS]:
        records = [r for r in all_records if r["config"] == config_name]
        if not records:
            continue
        avg_total = sum(r["total_s"] for r in records) / len(records)
        avg_prep = sum(r["preprocess_s"] for r in records) / len(records)
        avg_ocr = sum(r["ocr_s"] for r in records) / len(records)
        under_2s = sum(1 for r in records if r["under_2s"])
        total_blocks = sum(r["blocks"] for r in records)
        print(f"\n  {config_name}")
        print(f"    平均预处理: {avg_prep:.3f}s | 平均OCR: {avg_ocr:.3f}s | 平均总计: {avg_total:.3f}s")
        print(f"    <2s: {under_2s}/{len(records)}")
        print(f"    总文本块: {total_blocks}")

    import json
    out_path = _PROJ / "csv" / "ppocr_v4_pipeline_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存至 {out_path}")


if __name__ == "__main__":
    main()
