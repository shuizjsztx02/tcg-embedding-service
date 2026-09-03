# -*- coding: utf-8 -*-
"""P0 验收评估 harness：模拟客户端预处理 → POST /v2/recognize → 对比标注。

指标：
- 总准确率（仅 verdict=ok 行，/v2.product_id == gt.product_id）
- 分 decision_path 准确率与占比
- 误采信率（verdict=bad 行被 matched 的比例）
- 延迟分位（p50 / p95）

用法：
    python script_temp/bench_recognize_v2.py [--limit N] [--server URL]
                                            [--category-hint pokemon] [--no-hint]
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# 让 script_temp 下的 preprocess 可导入
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from preprocess import preprocess_query

from PIL import Image

DATA_DIR = os.path.join(SCRIPT_DIR, "..")
ANNOT_PATH = os.path.join(DATA_DIR, "dino-v3-annotations.jsonl")
TEST_IMG_DIR = os.path.join(DATA_DIR, "test-images-v3")
DONE_FILE = os.path.join(SCRIPT_DIR, "..", "test-results-dino-v3", "bench_recognize_done.json")


def load_annotations(path):
    gt = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            fn = d["filename"]
            gt[fn] = {
                "verdict": d["verdict"],
                "card_id": d["card_id"],
                "product_id": d["card_id"].removesuffix("_200w") if d.get("card_id") else None,
                "score": d.get("score"),
            }
    return gt


def load_done():
    if os.path.exists(DONE_FILE):
        with open(DONE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_done(done):
    os.makedirs(os.path.dirname(DONE_FILE), exist_ok=True)
    with open(DONE_FILE, "w") as f:
        json.dump(sorted(done), f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=300, help="测试样本数")
    ap.add_argument("--server", default="http://localhost:8056", help="服务地址")
    ap.add_argument("--category-hint", default=None, help="品类提示（如 pokemon）")
    ap.add_argument("--no-hint", action="store_true", help="不使用 category_hint（测试 LLM 品类判断）")
    ap.add_argument("--workers", type=int, default=1, help="并行数（P0 单线程就够了）")
    args = ap.parse_args()

    gt = load_annotations(ANNOT_PATH)
    done = load_done()
    url = args.server.rstrip("/") + "/v2/recognize"

    # 构建待测列表：有标注的文件
    items = []
    for fn in sorted(os.listdir(TEST_IMG_DIR)):
        if fn in done:
            continue
        if fn in gt:
            items.append(fn)
    items = items[:args.limit]

    if not items:
        print("All done or no items to test.")
        return

    print(f"Testing {len(items)} items (limit={args.limit}, hint={args.category_hint or 'auto'})...")

    results = []
    n_total = len(items)

    def work(fn):
        path = os.path.join(TEST_IMG_DIR, fn)
        try:
            # 模拟客户端预处理
            img = preprocess_query(Image.open(path))
            # 转为 bytes 上传
            import io
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=90)
            files = {"file": (fn, buf.getvalue(), "image/jpeg")}
            data = {}
            if args.category_hint and not args.no_hint:
                data["category_hint"] = args.category_hint
            t0 = time.time()
            resp = requests.post(url, files=files, data=data, timeout=120)
            elapsed = (time.time() - t0) * 1000
            resp.raise_for_status()
            result = resp.json()
            return {
                "filename": fn,
                "ok": True,
                "status": result.get("status"),
                "decision_path": result.get("decision_path", ""),
                "pred_product_id": result.get("product_id"),
                "latency_ms": result.get("latency_ms", round(elapsed)),
                "gt": gt.get(fn),
            }
        except Exception as e:
            return {"filename": fn, "ok": False, "error": str(e)[:150], "gt": gt.get(fn)}

    with ThreadPoolExecutor(args.workers) as ex:
        futures = {ex.submit(work, fn): fn for fn in items}
        for i, future in enumerate(as_completed(futures), 1):
            r = future.result()
            results.append(r)
            done.add(r["filename"])
            if i % 50 == 0:
                save_done(done)
                print(f"  {i}/{n_total} done...")
    save_done(done)

    # ---- 统计 ----
    ok_samples = [r for r in results if r["gt"] and r["gt"]["verdict"] == "ok"]
    bad_samples = [r for r in results if r["gt"] and r["gt"]["verdict"] == "bad"]
    errors = [r for r in results if not r["ok"] or r.get("status") == "error"]

    # 准确率（仅 ok 行）
    correct = sum(1 for r in ok_samples
                  if r.get("status") == "matched" and r.get("pred_product_id") == r["gt"]["product_id"])
    total_ok = len(ok_samples)
    acc = correct / total_ok if total_ok else 0

    # 误采信率（bad 行中被 matched 的）
    bad_matched = sum(1 for r in bad_samples
                      if r.get("status") == "matched")
    total_bad = len(bad_samples)

    # 分 decision_path 统计
    from collections import Counter
    path_counts = Counter(r.get("decision_path", "unknown") for r in results if r.get("ok"))
    path_correct = Counter()
    for r in ok_samples:
        if r.get("status") == "matched" and r.get("pred_product_id") == r["gt"]["product_id"]:
            path_correct[r.get("decision_path", "unknown")] += 1

    # 延迟
    lats = sorted([r.get("latency_ms", 0) for r in results if r.get("ok")])
    p50 = lats[len(lats) // 2] if lats else 0
    p95 = lats[int(len(lats) * 0.95)] if lats else 0

    # ---- 输出 ----
    print(f"\n{'='*60}")
    print(f"P0 验收报告")
    print(f"{'='*60}")
    print(f"样本: {len(results)} (ok={total_ok}, bad={total_bad}, error={len(errors)})")
    print(f"端到端准确率: {correct}/{total_ok} = {acc:.1%}")
    print(f"误采信率: {bad_matched}/{total_bad} = {bad_matched/total_bad:.1%}" if total_bad else "误采信率: N/A")
    print(f"延迟 p50: {p50:.0f}ms, p95: {p95:.0f}ms")
    print(f"\n--- 分路径 ---")
    for path in sorted(path_counts):
        c = path_counts[path]
        ok_c = path_correct.get(path, 0)
        e = ok_c / c if c else 0
        print(f"  {path:25s}: {c:4d} ({c/len(results):5.1%}) 准确率={ok_c}/{c if total_ok else 0}={e:.1%}" if total_ok else f"  {path:25s}: {c:4d}")

    if errors:
        print(f"\n--- 错误明细（前 10）---")
        for r in errors[:10]:
            print(f"  {r['filename']}: {r.get('error', r.get('status',''))}")

    # 保存详细结果
    out_path = os.path.join(SCRIPT_DIR, "..", "test-results-dino-v3", "bench_recognize_v2_results.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n详细结果: {out_path}")
    print(f"Done.")


if __name__ == "__main__":
    main()