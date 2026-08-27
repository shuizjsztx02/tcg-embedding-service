#!/usr/bin/env python3
"""全量单卡采集 —— 9 类 TCG 单卡，只存信息 + 200w 小图（无大图、无价格明细）

与 fetch_categories.py 的区别：
  - 不限 10000，扫完全部 productId（约 18 万）为止
  - 只落盘单卡：productTypeName ∈ {Cards, Heroclix}（排除 Sealed Products 包装盒）
  - 只下载 200w 小图，不下载原图大图（省 ~一半空间）
  - 输出到新目录 category_cards/（不污染旧 category_batch/）
  - 断点续传：启动时读各分类已有 pid，重跑跳过（不重复写入）

用法：
  python3 fetch_cards_full.py                 # 全量
  python3 fetch_cards_full.py --scan 2000     # 只扫前 2000 个 pid（快速验证）
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
OUTPUT_DIR = os.path.join(BASE_DIR, "category_cards")

PRODUCT_ID_RANGE = (100000, 280000)   # 已实测该区间全部有效，共 18 万
CONCURRENCY = 20
REQUEST_TIMEOUT = 8
IMAGE_TIMEOUT = 12
MAX_RETRIES = 3
BATCH_SIZE = 2000

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# productLineId -> 文件夹名（9 个 TCG 分类）
TARGETS = {
    1: "Magic",
    2: "YuGiOh",
    3: "Pokemon",
    8: "Heroclix",
    16: "Cardfight_Vanguard",
    17: "Force_of_Will",
    18: "Dice_Masters",
    20: "Weiss_Schwarz",
    23: "Dragon_Ball_Z_TCG",
}

CARD_TYPES = {"Cards", "Heroclix"}

_write_lock = threading.Lock()
_seen_lock = threading.Lock()


def cat_dir(line_id: int) -> str:
    return os.path.join(OUTPUT_DIR, f"{line_id:02d}_{TARGETS[line_id]}")


def fetch_json(url: str):
    for _ in range(MAX_RETRIES):
        try:
            r = subprocess.run(
                ["curl", "-s", "--max-time", str(REQUEST_TIMEOUT), url,
                 "-H", f"User-Agent: {UA}"],
                capture_output=True, text=True, timeout=REQUEST_TIMEOUT + 2)
            if r.returncode == 0:
                return json.loads(r.stdout)
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


def save_product(line_id: int, pid: int, product: dict) -> None:
    d = cat_dir(line_id)
    img_dir = os.path.join(d, "images")
    os.makedirs(img_dir, exist_ok=True)

    with _write_lock:
        with open(os.path.join(d, "products.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(product, ensure_ascii=False) + "\n")

    # 只下小图（200w）
    small = os.path.join(img_dir, f"{pid}_200w.jpg")
    if not os.path.exists(small):
        download_image(product.get("_image_small_url", ""), small)


def load_seen() -> dict[int, set]:
    seen = {}
    for line_id in TARGETS:
        jf = os.path.join(cat_dir(line_id), "products.jsonl")
        pids = set()
        if os.path.exists(jf):
            with open(jf, encoding="utf-8") as f:
                for line in f:
                    try:
                        pids.add(int(json.loads(line).get("productId")))
                    except Exception:
                        pass
        seen[line_id] = pids
    return seen


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
            scan_from = int(json.load(open(checkpoint_file)).get("next_pid", start))
        except Exception:
            scan_from = start
    scan_from = max(start, min(scan_from, start + total_pids))
    if scan_from >= start + total_pids:
        print("✅ 已扫描完毕（checkpoint 已在末尾），无需重跑", flush=True)
        return

    print(f"🃏 全量单卡采集（只单卡 + 200w 小图）", flush=True)
    print(f"   目标分类: {len(TARGETS)} 个  并发: {args.concurrency}", flush=True)
    print(f"   ID 范围: {start}~{start + total_pids}  输出: {OUTPUT_DIR}", flush=True)
    if scan_from > start:
        print(f"   ♻️  断点续传：从 pid {scan_from} 继续（跳过前 {scan_from - start} 个 pid）", flush=True)
    print(f"   启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    seen = load_seen()
    for line_id in TARGETS:
        print(f"   {line_id:2d} {TARGETS[line_id]:20s} 已有单卡 {len(seen[line_id])}",
              flush=True)

    stats = {"nf": 0, "other": 0, "nocard": 0, "card": 0}
    stats_lock = threading.Lock()
    t0 = time.time()
    scanned = 0

    def process(pid: int) -> str:
        product = fetch_one(pid)
        if product is None:
            return "nf"
        line_id = int(product.get("productLineId", -1))
        if line_id not in TARGETS:
            return "other"
        if product.get("productTypeName") not in CARD_TYPES:
            return "nocard"
        with _seen_lock:
            if pid in seen[line_id]:
                return "skip"
        product["productId"] = pid
        product["_image_small_url"] = f"https://tcgplayer-cdn.tcgplayer.com/product/{pid}_200w.jpg"
        product["_image_url"] = f"https://product-images.tcgplayer.com/{pid}.jpg"
        save_product(line_id, pid, product)
        with _seen_lock:
            seen[line_id].add(pid)
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
                              f"单卡 {stats['card']} 非单卡 {stats['nocard']} 其他分类 {stats['other']} "
                              f"无数据 {stats['nf']}", flush=True)
            # 整批完成后写 checkpoint，供中断后从下一批续跑
            with open(checkpoint_file, "w") as f:
                json.dump({"next_pid": batch_end}, f)
    except KeyboardInterrupt:
        print("\n⚠️  手动中断，已落盘数据 + checkpoint 保留，重启从断点继续", flush=True)

    el = time.time() - t0
    print(f"\n✅ 扫描完成，用时 {el/60:.1f} 分钟", flush=True)
    print(f"   单卡: {stats['card']}  非单卡: {stats['nocard']}  "
          f"其他分类: {stats['other']}  无数据: {stats['nf']}", flush=True)
    print("\n各分类最终单卡数量：", flush=True)
    for line_id in TARGETS:
        jf = os.path.join(cat_dir(line_id), "products.jsonl")
        n = sum(1 for _ in open(jf, encoding="utf-8")) if os.path.exists(jf) else 0
        img = os.path.join(cat_dir(line_id), "images")
        imgs = len(os.listdir(img)) if os.path.isdir(img) else 0
        print(f"   {line_id:2d} {TARGETS[line_id]:20s} 商品 {n:6d}  图片 {imgs:6d}",
              flush=True)


if __name__ == "__main__":
    main()