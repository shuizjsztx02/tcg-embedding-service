#!/usr/bin/env python3
"""全量 Pokemon 单卡采集 —— 只爬 Pokemon 品类，只存信息 + 200w 小图

基于 fetch_cards_full.py 改造，只保留 productLineId=3 (Pokemon)：
  - 只扫 Pokemon 单卡，跳过其他 8 个分类
  - 输出到 pokemon_cards/ 目录（不分层，直接 products.jsonl + images/）
  - 断点续传：启动时读已有 pid，重跑跳过

用法：
  python3 fetch_cards_full_pokeman.py                 # 全量
  python3 fetch_cards_full_pokeman.py --scan 2000     # 只扫前 2000 个 pid（快速验证）
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "pokemon_cards")

PRODUCT_ID_RANGE = (40000, 720000)    # 全量扫描范围，覆盖 Pokemon US 所有 PID
CONCURRENCY = 20
REQUEST_TIMEOUT = 8
IMAGE_TIMEOUT = 12
MAX_RETRIES = 3
BATCH_SIZE = 2000

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

POKEMON_LINE_ID = 3
CARD_TYPES = {"Cards", "Heroclix"}

_write_lock = threading.Lock()
_seen_lock = threading.Lock()


def fetch_json(url: str):
    for _ in range(MAX_RETRIES):
        try:
            r = subprocess.run(
                ["curl", "-s", "--max-time", str(REQUEST_TIMEOUT), url,
                 "-H", f"User-Agent: {UA}"],
                capture_output=True, timeout=REQUEST_TIMEOUT + 2)
            if r.returncode == 0 and r.stdout:
                return json.loads(r.stdout.decode("utf-8"))
        except Exception:
            pass
        time.sleep(0.5)
    return None


def download_image(url: str, path: str) -> bool:
    if not url:
        return False
    for _ in range(MAX_RETRIES):
        try:
            r = subprocess.run(
                ["curl", "-sf", "--max-time", str(IMAGE_TIMEOUT), url,
                 "-H", "User-Agent: Mozilla/5.0",
                 "-H", "Referer: https://www.tcgplayer.com/",
                 "-o", path],
                capture_output=True, timeout=IMAGE_TIMEOUT + 2)
            if r.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 5000:
                return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def fetch_one(pid: int):
    url = f"https://mp-search-api.tcgplayer.com/v2/product/{pid}/details?mpfev=5489"
    detail = fetch_json(url)
    if detail is None or "productLineId" not in detail:
        return None
    return detail


def save_product(pid: int, product: dict) -> None:
    img_dir = os.path.join(OUTPUT_DIR, "images")
    os.makedirs(img_dir, exist_ok=True)

    with _write_lock:
        with open(os.path.join(OUTPUT_DIR, "products.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(product, ensure_ascii=False) + "\n")

    # 只下小图（200w）
    small = os.path.join(img_dir, f"{pid}_200w.jpg")
    if not os.path.exists(small):
        download_image(product.get("_image_small_url", ""), small)


def load_seen() -> set[int]:
    jf = os.path.join(OUTPUT_DIR, "products.jsonl")
    pids = set()
    if os.path.exists(jf):
        with open(jf, encoding="utf-8") as f:
            for line in f:
                try:
                    pids.add(int(json.loads(line).get("productId")))
                except Exception:
                    pass
    return pids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", type=int, default=0, help="最多扫描多少个 pid（0=全量）")
    ap.add_argument("--concurrency", type=int, default=CONCURRENCY)
    ap.add_argument("--from", dest="from_pid", type=int, default=0, help="从指定 productId 开始（覆盖 checkpoint）")
    ap.add_argument("--reset", action="store_true", help="忽略 checkpoint，从头扫描")
    args = ap.parse_args()

    start, end = PRODUCT_ID_RANGE
    total_pids = args.scan or (end - start)
    total_pids = min(total_pids, end - start)

    checkpoint_file = os.path.join(OUTPUT_DIR, "_checkpoint.json")
    scan_from = start
    if args.from_pid:
        scan_from = args.from_pid
    elif not args.reset and os.path.exists(checkpoint_file):
        try:
            cp = json.load(open(checkpoint_file))
            cp_start = cp.get("range_start", start)
            cp_end = cp.get("range_end", end)
            if cp_start == start and cp_end == end:
                scan_from = int(cp.get("next_pid", start))
            else:
                print("   [续传] 检测到扫描范围变更（原 %d~%d，现 %d~%d），重置 checkpoint" % (cp_start, cp_end, start, end), flush=True)
        except Exception:
            scan_from = start
    scan_from = max(start, min(scan_from, start + total_pids))
    if scan_from >= start + total_pids:
        print("[完成] 已扫描完毕（checkpoint 已在末尾），无需重跑", flush=True)
        return

    print(f"[Pokemon] 全量单卡采集（只单卡 + 200w 小图）", flush=True)
    print(f"   并发: {args.concurrency}  输出: {OUTPUT_DIR}", flush=True)
    print(f"   ID 范围: {start}~{start + total_pids}", flush=True)
    if scan_from > start:
        print(f"   [续传] 从 pid {scan_from} 继续（跳过前 {scan_from - start} 个 pid）", flush=True)
    print(f"   启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    seen = load_seen()
    print(f"   Pokemon 已有单卡 {len(seen)}", flush=True)

    stats = {"nf": 0, "nocard": 0, "card": 0}
    stats_lock = threading.Lock()
    t0 = time.time()
    scanned = 0

    def process(pid: int) -> str:
        product = fetch_one(pid)
        if product is None:
            return "nf"
        line_id = int(product.get("productLineId", -1))
        if line_id != POKEMON_LINE_ID:
            return "nf"   # 非 Pokemon 等同于无数据，不区分统计
        if product.get("productTypeName") not in CARD_TYPES:
            return "nocard"
        with _seen_lock:
            if pid in seen:
                return "skip"
        product["productId"] = pid
        product["_image_small_url"] = f"https://tcgplayer-cdn.tcgplayer.com/product/{pid}_200w.jpg"
        product["_image_url"] = f"https://product-images.tcgplayer.com/{pid}.jpg"
        save_product(pid, product)
        with _seen_lock:
            seen.add(pid)
        return "card"

    try:
        for batch_start in range(scan_from, start + total_pids, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, start + total_pids)
            with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
                futures = [pool.submit(process, p) for p in range(batch_start, batch_end)]
                for fut in as_completed(futures):
                    tag = fut.result()
                    with stats_lock:
                        stats[tag] = stats.get(tag, 0) + 1
                    scanned += 1
                    if scanned % 2000 == 0:
                        rate = scanned / (time.time() - t0)
                        done = scan_from - start + scanned
                        print(f"   进度 {done}/{total_pids} (pid {batch_start}) | 速度 {rate:.0f}/s | "
                              f"单卡 {stats['card']} 非单卡 {stats['nocard']} 无数据 {stats['nf']}",
                              flush=True)
            # 整批完成后写 checkpoint
            with open(checkpoint_file, "w") as f:
                json.dump({"range_start": start, "range_end": end, "next_pid": batch_end}, f)
    except KeyboardInterrupt:
        print("\n[中断] 手动中断，已落盘数据 + checkpoint 保留，重启从断点继续", flush=True)

    el = time.time() - t0
    print(f"\n[完成] 扫描完成，用时 {el/60:.1f} 分钟", flush=True)
    print(f"   单卡: {stats['card']}  非单卡: {stats['nocard']}  无数据: {stats['nf']}", flush=True)

    # 最终统计
    jf = os.path.join(OUTPUT_DIR, "products.jsonl")
    n = sum(1 for _ in open(jf, encoding="utf-8")) if os.path.exists(jf) else 0
    img_dir = os.path.join(OUTPUT_DIR, "images")
    imgs = len(os.listdir(img_dir)) if os.path.isdir(img_dir) else 0
    print(f"\n   Pokemon 最终: 商品 {n}  图片 {imgs}", flush=True)


if __name__ == "__main__":
    main()