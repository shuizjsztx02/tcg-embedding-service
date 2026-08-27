#!/usr/bin/env python3
"""全量 Pokemon 单卡采集 —— 优化版 v3

相对于 v2 的改进：
  - PID 范围扩宽到 40000~720000（覆盖实际 Pokemon 的 PID 跨度）
  - --from 可指定任意起始值，不再受默认起始值限制
  - checkpoint 按区间隔离，避免不同区间互相干扰
  - 输出统计更清晰

用法：
  python fetch_cards_full_pokeman_v2.py                         # 全量 40000~720000
  python fetch_cards_full_pokeman_v2.py --from 40000 --range-end 100000 --reset  # 低区
  python fetch_cards_full_pokeman_v2.py --from 500000 --range-end 720000 --reset  # 高区
"""
from __future__ import annotations

import argparse
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "pokemon_cards")

PRODUCT_ID_RANGE = (40000, 720000)
CONCURRENCY = 50
REQUEST_TIMEOUT = 10
IMAGE_TIMEOUT = 15
MAX_RETRIES = 3
BATCH_SIZE = 5000

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

POKEMON_LINE_ID = 3
CARD_TYPES = {"Cards", "Heroclix"}

_write_lock = threading.Lock()
_seen_lock = threading.Lock()
_session = None
_session_lock = threading.Lock()


def get_session() -> requests.Session:
    global _session
    if _session is None:
        with _session_lock:
            if _session is None:
                s = requests.Session()
                s.headers.update({"User-Agent": UA, "Accept": "application/json"})
                adapter = requests.adapters.HTTPAdapter(
                    pool_connections=100, pool_maxsize=100, max_retries=0
                )
                s.mount("https://", adapter)
                _session = s
    return _session


def fetch_one(pid: int) -> dict | None:
    url = f"https://mp-search-api.tcgplayer.com/v2/product/{pid}/details?mpfev=5489"
    session = get_session()
    for attempt in range(MAX_RETRIES):
        try:
            r = session.get(url, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return None
        except (requests.ConnectionError, requests.Timeout):
            if attempt == MAX_RETRIES - 1:
                return None
            time.sleep(1.0 * (attempt + 1))
    return None


def download_image(url: str, path: str) -> bool:
    if not url:
        return False
    session = get_session()
    for attempt in range(MAX_RETRIES):
        try:
            r = session.get(url, timeout=IMAGE_TIMEOUT, stream=True)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(path, "wb") as f:
                    f.write(r.content)
                return True
        except Exception:
            pass
        time.sleep(0.5 * (attempt + 1))
    return False


def save_product(pid: int, product: dict) -> None:
    img_dir = os.path.join(OUTPUT_DIR, "images")
    os.makedirs(img_dir, exist_ok=True)

    with _write_lock:
        with open(os.path.join(OUTPUT_DIR, "products.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(product, ensure_ascii=False) + "\n")

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
    ap = argparse.ArgumentParser(description="全量 Pokemon 单卡采集（优化版 v3）")
    ap.add_argument("--scan", type=int, default=0, help="最多扫描多少个 pid（0=全量）")
    ap.add_argument("--concurrency", type=int, default=CONCURRENCY)
    ap.add_argument("--from", dest="from_pid", type=int, default=0, help="起始 PID（覆盖默认值）")
    ap.add_argument("--reset", action="store_true", help="忽略 checkpoint，从头扫描")
    ap.add_argument("--range-end", type=int, default=PRODUCT_ID_RANGE[1],
                    help=f"PID 扫描上限（默认 {PRODUCT_ID_RANGE[1]}）")
    args = ap.parse_args()

    # --from 指定实际起始 PID，不再受 PRODUCT_ID_RANGE[0] 限制
    start = args.from_pid if args.from_pid > 0 else PRODUCT_ID_RANGE[0]
    end = args.range_end
    total_pids = args.scan if args.scan > 0 else (end - start)
    total_pids = min(total_pids, end - start)
    actual_end = start + total_pids

    # checkpoint 按区间隔离
    checkpoint_file = os.path.join(OUTPUT_DIR, "_checkpoint.json")
    scan_from = start
    if not args.from_pid and not args.reset and os.path.exists(checkpoint_file):
        try:
            cp = json.load(open(checkpoint_file))
            if cp.get("range_start") == start and cp.get("range_end") == actual_end:
                scan_from = int(cp.get("next_pid", start))
        except Exception:
            pass
    scan_from = max(start, min(scan_from, actual_end))
    if scan_from >= actual_end:
        print("[完成] 已扫描完毕（checkpoint 已在末尾），无需重跑", flush=True)
        return

    seen = load_seen()

    print(f"[Pokemon] 全量单卡采集（v3）", flush=True)
    print(f"   并发: {args.concurrency}  输出: {OUTPUT_DIR}", flush=True)
    print(f"   ID 范围: {start} ~ {end}（共 {total_pids} 个 PID）", flush=True)
    if scan_from > start:
        print(f"   [续传] 从 pid {scan_from} 继续（跳过 {scan_from - start} 个）", flush=True)
    if seen:
        print(f"   已有 Pokemon 单卡: {len(seen)}", flush=True)
    print(f"   启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    stats = {"card": 0, "skip": 0}
    stats_lock = threading.Lock()
    t0 = time.time()
    scanned = 0

    def process(pid: int) -> str:
        with _seen_lock:
            if pid in seen:
                return "skip"

        product = fetch_one(pid)
        if product is None:
            return "skip"
        line_id = int(product.get("productLineId", -1))
        if line_id != POKEMON_LINE_ID:
            return "skip"
        if product.get("productTypeName") not in CARD_TYPES:
            return "skip"

        product["productId"] = pid
        product["_image_small_url"] = f"https://tcgplayer-cdn.tcgplayer.com/product/{pid}_200w.jpg"
        product["_image_url"] = f"https://product-images.tcgplayer.com/{pid}.jpg"
        save_product(pid, product)
        with _seen_lock:
            seen.add(pid)
        return "card"

    try:
        for batch_start in range(scan_from, actual_end, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, actual_end)
            with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
                futures = [pool.submit(process, p) for p in range(batch_start, batch_end)]
                for fut in as_completed(futures):
                    tag = fut.result()
                    with stats_lock:
                        stats[tag] = stats.get(tag, 0) + 1
                    scanned += 1
                    if scanned % 3000 == 0:
                        elapsed = time.time() - t0
                        rate = scanned / elapsed if elapsed > 0 else 0
                        done = scan_from - start + scanned
                        pct = done / total_pids * 100
                        print(f"   [{done}/{total_pids} {pct:.1f}%] pid {batch_start} | "
                              f"{rate:.0f}/s | Pokémon {stats['card']} 跳过 {stats['skip']}",
                              flush=True)
            with open(checkpoint_file, "w") as f:
                json.dump({"range_start": start, "range_end": actual_end, "next_pid": batch_end}, f)
    except KeyboardInterrupt:
        print("\n[中断] 手动中断，已落盘数据 + checkpoint 保留，重启从断点继续", flush=True)

    el = time.time() - t0
    print(f"\n[完成] 扫描完成，用时 {el/60:.1f} 分钟", flush=True)
    print(f"   PID 范围: {start} ~ {actual_end}", flush=True)
    print(f"   扫描总数: {scanned}", flush=True)
    print(f"   Pokemon 单卡: {stats['card']}  跳过: {stats['skip']}", flush=True)

    jf = os.path.join(OUTPUT_DIR, "products.jsonl")
    n = sum(1 for _ in open(jf, encoding="utf-8")) if os.path.exists(jf) else 0
    img_dir = os.path.join(OUTPUT_DIR, "images")
    imgs = len(os.listdir(img_dir)) if os.path.isdir(img_dir) else 0
    print(f"\n   最终统计: 商品 {n}  图片 {imgs}", flush=True)


if __name__ == "__main__":
    main()
