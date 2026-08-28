#!/usr/bin/env python3
"""用搜索 API 按系列分页枚举 TCG 单卡并下载 200w 小图（通用版）

为什么不用 fetch_cards_new.py 的暴力 productId 扫描：
  - productId 是流水号，280000~715000 里 85% 是空洞/别的游戏；
  - 搜索 API 按 productLineName 命中，只返回目标游戏商品，且自带分页。
  - 但搜索后端 (Elasticsearch) 限制了 from 偏移（约 <10000），总数几万张翻不到底，
    所以按「系列 setName」分桶逐套拉（每套最多 ~2000 张，远低于上限）。

productTypeName=Cards 过滤掉卡盒等 sealed 产品。

用法（不同 --out 写到不同目录，可多个进程同时跑）：
  python3 fetch_cards_search.py --lines 3,85 --out category_cards_pokemon   # 宝可梦 英文+日文
  python3 fetch_cards_search.py --lines 1    --out category_cards_magic     # 万智牌
  python3 fetch_cards_search.py --metadata-only                            # 只写 jsonl，不下图
  python3 fetch_cards_search.py --images-only                              # 只补缺失小图
  python3 fetch_cards_search.py --limit 1000                               # 只写前 1000 张（验证）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "category_cards_search")

SEARCH_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"
PAGE_SIZE = 50
IMAGE_URL = "https://tcgplayer-cdn.tcgplayer.com/product/{pid}_200w.jpg"

CONCURRENCY = 4
IMAGE_RETRIES = 8
REQUEST_TIMEOUT = 15
IMAGE_TIMEOUT = 12
MIN_SIZE = 5000
MPFEV = 5489

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# productLineId -> (搜索匹配用 productLineName, 输出文件夹名, 单卡过滤用 productTypeName)
# 搜索名/类型必须与接口完全一致；文件夹名要与 category_cards 现有目录对齐（Magic 是简称）。
# 绝大多数游戏单卡 productTypeName="Cards"，唯独 Heroclix 是 "Heroclix"。
LINES = {
    1: ("Magic: The Gathering", "Magic", "Cards"),
    2: ("YuGiOh", "YuGiOh", "Cards"),
    3: ("Pokemon", "Pokemon", "Cards"),
    8: ("Heroclix", "Heroclix", "Heroclix"),
    13: ("WoW", "WoW", "Cards"),
    16: ("Cardfight Vanguard", "Cardfight Vanguard", "Cards"),
    17: ("Force of Will", "Force of Will", "Cards"),
    18: ("Dice Masters", "Dice Masters", "Cards"),
    19: ("Future Card BuddyFight", "Future Card BuddyFight", "Cards"),
    20: ("Weiss Schwarz", "Weiss Schwarz", "Cards"),
    23: ("Dragon Ball Z TCG", "Dragon Ball Z TCG", "Cards"),
    28: ("Dragoborne", "Dragoborne", "Cards"),
    30: ("MetaX TCG", "MetaX TCG", "Cards"),
    36: ("Zombie World Order TCG", "Zombie World Order TCG", "Cards"),
    37: ("The Caster Chronicles", "The Caster Chronicles", "Cards"),
    47: ("Exodus TCG", "Exodus TCG", "Cards"),
    48: ("Lightseekers TCG", "Lightseekers TCG", "Cards"),
    53: ("Munchkin CCG", "Munchkin CCG", "Cards"),
    54: ("Warhammer Age of Sigmar Champions TCG", "Warhammer Age of Sigmar Champions TCG", "Cards"),
    57: ("Transformers TCG", "Transformers TCG", "Cards"),
    58: ("Bakugan TCG", "Bakugan TCG", "Cards"),
    60: ("Chrono Clash System", "Chrono Clash System", "Cards"),
    61: ("Argent Saga TCG", "Argent Saga TCG", "Cards"),
    62: ("Flesh and Blood TCG", "Flesh and Blood TCG", "Cards"),
    63: ("Digimon Card Game", "Digimon Card Game", "Cards"),
    65: ("Gate Ruler", "Gate Ruler", "Cards"),
    66: ("MetaZoo", "MetaZoo", "Cards"),
    67: ("WIXOSS", "WIXOSS", "Cards"),
    68: ("One Piece Card Game", "One Piece Card Game", "Cards"),
    71: ("Disney Lorcana", "Disney Lorcana", "Cards"),
    72: ("Battle Spirits Saga", "Battle Spirits Saga", "Cards"),
    73: ("Shadowverse: Evolve", "Shadowverse: Evolve", "Cards"),
    74: ("Grand Archive TCG", "Grand Archive TCG", "Cards"),
    75: ("Akora TCG", "Akora TCG", "Cards"),
    76: ("Kryptik TCG", "Kryptik TCG", "Cards"),
    77: ("Sorcery: Contested Realm", "Sorcery: Contested Realm", "Cards"),
    78: ("Alpha Clash", "Alpha Clash", "Cards"),
    79: ("Star Wars: Unlimited", "Star Wars: Unlimited", "Cards"),
    80: ("Dragon Ball Super: Fusion World", "Dragon Ball Super: Fusion World", "Cards"),
    81: ("Union Arena", "Union Arena", "Cards"),
    83: ("Elestrals", "Elestrals", "Cards"),
    85: ("Pokemon Japan", "Pokemon Japan", "Cards"),
    86: ("Gundam Card Game", "Gundam Card Game", "Cards"),
    87: ("hololive OFFICIAL CARD GAME", "hololive OFFICIAL CARD GAME", "Cards"),
    88: ("Godzilla Card Game", "Godzilla Card Game", "Cards"),
    89: ("Riftbound: League of Legends Trading Card Game", "Riftbound: League of Legends Trading Card Game", "Cards"),
    90: ("CookieRun: Braverse TCG", "CookieRun: Braverse TCG", "Cards"),
}
DEFAULT_LINES = "3,85"

_write_lock = threading.Lock()
_name_lock = threading.Lock()
_line_names: dict[int, str] = {}


def safe_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", (s or "Unknown")).strip("_")


def cat_dir(line_id: int, name: str) -> str:
    with _name_lock:
        if line_id not in _line_names:
            _line_names[line_id] = safe_name(name)
    return os.path.join(OUTPUT_DIR, f"{line_id:02d}_{_line_names[line_id]}")


def search_request(match: dict, frm: int, size: int = PAGE_SIZE):
    body = {"filters": {"match": match}, "mpfev": MPFEV, "from": frm, "size": size}
    for _ in range(3):
        try:
            r = subprocess.run(
                ["curl", "-s", "--max-time", str(REQUEST_TIMEOUT),
                 "-X", "POST", SEARCH_URL,
                 "-H", "Content-Type: application/json",
                 "-H", f"User-Agent: {UA}",
                 "-H", "Origin: https://www.tcgplayer.com",
                 "-H", "Referer: https://www.tcgplayer.com/",
                 "-d", json.dumps(body)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=REQUEST_TIMEOUT + 3)
            if r.returncode == 0 and r.stdout.strip():
                data = json.loads(r.stdout)
                if data.get("results") and "results" not in data.get("errors", []):
                    return data
        except Exception:
            pass
        time.sleep(0.6)
    return None


def get_sets(line_name: str, card_type: str) -> list[tuple[str, str, int]]:
    """返回 [(setName 过滤值, 显示名, 单卡数)]。

    setName 是模糊匹配，urlValue 只是 URL slug，很多系列用它过滤会命中 0 张
    （如 "Panini: Heroes & Villains" 的 slug "panini-heroes-and-villains"）。
    产品的 setName 字段存的是显示名，所以用显示名过滤才不会漏系列。
    """
    match = {"productLineName": [line_name], "productTypeName": [card_type]}
    data = search_request(match, 0, 1)
    if not data:
        return []
    inner = data["results"][0]
    agg = inner.get("aggregations", {}).get("setName", [])
    out = []
    for x in agg:
        val = x.get("value") or x["urlValue"]
        out.append((val, val, int(x["count"])))
    return out


def clean_product(p: dict, card_type: str) -> dict:
    out = {k: v for k, v in p.items() if k != "listings"}
    out["productTypeName"] = card_type
    for k in ("productId", "productLineId", "setId"):
        if k in out and isinstance(out[k], float):
            out[k] = int(out[k])
    return out


def enumerate_set(line_name: str, card_type: str, set_url: str, count: int) -> list[dict]:
    match = {"productLineName": [line_name],
             "productTypeName": [card_type],
             "setName": [set_url]}
    out = []
    frm = 0
    while True:
        data = search_request(match, frm, PAGE_SIZE)
        if not data:
            break
        inner = data["results"][0]
        results = inner.get("results", [])
        for p in results:
            out.append(clean_product(p, card_type))
        total = int(inner.get("totalResults", 0))
        frm += len(results)
        # 用实际 totalResults 翻页（聚合 count 与模糊命中数可能不一致）；
        # 后端 from 上限约 10000，越大直接 400，这里兜底停住避免死循环。
        if not results or frm >= total or frm >= 9990:
            break
    return out


def load_seen_dir(d: str) -> set[int]:
    jf = os.path.join(d, "products.jsonl")
    pids = set()
    if os.path.isfile(jf):
        with open(jf, encoding="utf-8") as f:
            for line in f:
                try:
                    pids.add(int(json.loads(line).get("productId")))
                except Exception:
                    pass
    return pids


def save_record(d: str, product: dict) -> None:
    os.makedirs(d, exist_ok=True)
    with _write_lock:
        with open(os.path.join(d, "products.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(product, ensure_ascii=False) + "\n")


def download_image(imgdir: str, pid: int) -> bool:
    dest = os.path.join(imgdir, f"{pid}_200w.jpg")
    if os.path.exists(dest) and os.path.getsize(dest) >= MIN_SIZE:
        return True
    tmp = dest + ".tmp"
    url = IMAGE_URL.format(pid=pid)
    for attempt in range(IMAGE_RETRIES):
        try:
            r = subprocess.run(
                ["curl", "-s", "-o", tmp, "-w", "%{http_code}",
                 "--max-time", str(IMAGE_TIMEOUT), url,
                 "-H", f"User-Agent: {UA}",
                 "-H", "Referer: https://www.tcgplayer.com/"],
                capture_output=True, timeout=IMAGE_TIMEOUT + 3)
            code = (r.stdout or b"").strip().decode()
            if code in ("403", "404"):
                if os.path.exists(tmp):
                    os.remove(tmp)
                return False
            if code == "200" and os.path.exists(tmp) and os.path.getsize(tmp) > MIN_SIZE:
                os.replace(tmp, dest)
                return True
        except Exception:
            pass
        time.sleep(min(0.6 * (2 ** attempt), 8))
    if os.path.exists(tmp):
        os.remove(tmp)
    return False


def metadata_phase(lines_to_do: list, limit: int, mconcurrency: int) -> None:
    """并行枚举所有产品线的所有系列，写 products.jsonl（幂等，重复 pid 跳过）。"""
    seen_map: dict[int, set] = {}
    tasks: list[tuple] = []
    for lid, search_name, folder_name, card_type in lines_to_do:
        d = cat_dir(lid, folder_name)
        seen_map[lid] = load_seen_dir(d)
        sets = get_sets(search_name, card_type)
        print(f"\n[{lid} {search_name}] 共 {len(sets)} 个系列 -> {os.path.relpath(d, OUTPUT_DIR) if d.startswith(OUTPUT_DIR) else d}", flush=True)
        for su, sd, cnt in sets:
            tasks.append((lid, search_name, folder_name, card_type, su, sd, cnt))

    counter = [0]
    stats_lock = threading.Lock()
    done = [0]
    t0 = time.time()

    def work(task):
        lid, search_name, folder_name, card_type, set_url, set_disp, cnt = task
        products = enumerate_set(search_name, card_type, set_url, cnt)
        d = cat_dir(lid, folder_name)
        seen = seen_map[lid]
        fresh = 0
        for p in products:
            if limit and counter[0] >= limit:
                break
            with stats_lock:
                if p["productId"] in seen:
                    continue
                seen.add(p["productId"])
                counter[0] += 1
            save_record(d, p)
            fresh += 1
        with stats_lock:
            done[0] += 1
        return set_disp, cnt, fresh

    total_expected = sum(c for *_, c in tasks)
    print(f"  系列任务 {len(tasks)} 个，预期单卡 {total_expected}，并行度 {mconcurrency}", flush=True)
    with ThreadPoolExecutor(max_workers=mconcurrency) as pool:
        futures = [pool.submit(work, t) for t in tasks]
        for fut in as_completed(futures):
            sd, cnt, fresh = fut.result()
            if done[0] % 20 == 0:
                print(f"  已完成系列 {done[0]}/{len(tasks)}  累计单卡 {counter[0]}  "
                      f"用时 {(time.time()-t0)/60:.1f} 分钟", flush=True)

    print(f"  元数据完成：{len(tasks)} 个系列，共写入单卡 {counter[0]}  "
          f"用时 {(time.time()-t0)/60:.1f} 分钟", flush=True)


def images_phase(dirs: list[str], concurrency: int) -> None:
    """补下给定目录里所有缺失/损坏的 200w 小图（只处理 --lines 对应的文件夹）。"""
    jobs: list[tuple[str, int]] = []
    for d in dirs:
        jf = os.path.join(d, "products.jsonl")
        if not os.path.isfile(jf):
            continue
        imgdir = os.path.join(d, "images")
        os.makedirs(imgdir, exist_ok=True)
        with open(jf, encoding="utf-8") as f:
            for line in f:
                try:
                    pid = int(json.loads(line)["productId"])
                except Exception:
                    continue
                img = os.path.join(imgdir, f"{pid}_200w.jpg")
                if not os.path.exists(img) or os.path.getsize(img) < MIN_SIZE:
                    jobs.append((imgdir, pid))
    if not jobs:
        print("\n无缺失小图。", flush=True)
        return
    print(f"\n开始补图：{len(jobs)} 张（并发 {concurrency}）", flush=True)
    ok = fail = done = 0
    lock = threading.Lock()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(download_image, d, p) for d, p in jobs]
        for fut in as_completed(futures):
            with lock:
                done += 1
                if fut.result():
                    ok += 1
                else:
                    fail += 1
            if done % 500 == 0:
                print(f"  进度 {done}/{len(jobs)}  速度 {done/(time.time()-t0):.1f}/s  "
                      f"成功 {ok}  失败 {fail}", flush=True)
    print(f"补图完成：成功 {ok}  失败 {fail}  用时 {(time.time()-t0)/60:.1f} 分钟", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", default=DEFAULT_LINES, help="productLineId 逗号分隔（默认 3,85）")
    ap.add_argument("--out", default="category_cards_search", help="输出目录名（不同 --out 可并行跑）")
    ap.add_argument("--limit", type=int, default=0, help="每行最多写多少单卡（0=不限）")
    ap.add_argument("--concurrency", type=int, default=CONCURRENCY)
    ap.add_argument("--metadata-concurrency", type=int, default=10)
    ap.add_argument("--metadata-only", action="store_true")
    ap.add_argument("--images-only", action="store_true")
    args = ap.parse_args()

    global OUTPUT_DIR
    OUTPUT_DIR = os.path.join(BASE_DIR, args.out)

    target = set(LINES) if args.lines.strip().lower() == "all" else \
        {int(x) for x in args.lines.split(",") if x.strip()}

    lines_to_do = []
    for lid in sorted(target):
        entry = LINES.get(lid)
        if not entry:
            print(f"未知 productLineId {lid}，跳过（可用：{sorted(LINES)}）", flush=True)
            continue
        search_name, folder_name, card_type = entry
        lines_to_do.append((lid, search_name, folder_name, card_type))

    dirs = [cat_dir(lid, folder_name) for lid, _sn, folder_name, _ct in lines_to_do]

    if not args.images_only:
        if lines_to_do:
            metadata_phase(lines_to_do, args.limit, args.metadata_concurrency)
        print(f"\n元数据完成，输出目录 {OUTPUT_DIR}", flush=True)

    if not args.metadata_only:
        images_phase(dirs, args.concurrency)

    print("\n各产品线单卡数：", flush=True)
    for d in dirs:
        jf = os.path.join(d, "products.jsonl")
        if not os.path.isfile(jf):
            continue
        n = sum(1 for _ in open(jf, encoding="utf-8"))
        img = os.path.join(d, "images")
        imgs = len(os.listdir(img)) if os.path.isdir(img) else 0
        print(f"   {os.path.basename(d):24s} 单卡 {n:6d}  图片 {imgs:6d}", flush=True)


if __name__ == "__main__":
    main()