#!/usr/bin/env python3
"""抓取外部系列的 logo 源，缓存到 script_temp/out/src_*.json。

源：
  scryfall   https://api.scryfall.com/sets                 万智牌，1058 set，带 icon_svg_uri
  ygoprodeck https://db.ygoprodeck.com/api/v7/cardsets.php 游戏王，1035 set，带 set_image
  tcgdex     https://api.tcgdex.net/v2/en/sets (+ 逐个详情) 宝可梦，220 set，详情带 logo/symbol

用法：
  python fetch_logo_sources.py               # 全部
  python fetch_logo_sources.py tcgdex        # 只刷 TCGdex
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"


def get(url: str):
    r = subprocess.run(["curl", "-s", "--max-time", "40", "-A", UA, url],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=50)
    return json.loads(r.stdout)


def head_ok(url: str) -> bool:
    try:
        r = subprocess.run(["curl", "-s", "-o", os.devnull, "-w", "%{http_code}",
                            "--max-time", "15", url],
                           capture_output=True, text=True, timeout=22)
        return (r.stdout or "").strip() == "200"
    except Exception:
        return False


def do_scryfall() -> None:
    sc = get("https://api.scryfall.com/sets")["data"]
    with open(os.path.join(OUT, "src_scryfall.json"), "w", encoding="utf-8") as f:
        json.dump(sc, f, ensure_ascii=False, indent=1)
    print(f"scryfall {len(sc)} sets")


def do_ygoprodeck() -> None:
    yg = get("https://db.ygoprodeck.com/api/v7/cardsets.php")
    with open(os.path.join(OUT, "src_ygoprodeck.json"), "w", encoding="utf-8") as f:
        json.dump(yg, f, ensure_ascii=False, indent=1)
    print(f"ygoprodeck {len(yg)} sets")


def do_tcgdex() -> None:
    td_list = get("https://api.tcgdex.net/v2/en/sets")
    print(f"tcgdex list {len(td_list)} sets，取详情…", flush=True)

    def detail(s):
        for _ in range(3):
            try:
                d = get(f"https://api.tcgdex.net/v2/en/sets/{s['id']}")
                d.pop("cards", None)
                return d
            except Exception:
                time.sleep(1.0)
        return {"id": s["id"], "name": s.get("name"), "_error": True}

    with ThreadPoolExecutor(max_workers=5) as ex:
        details = list(ex.map(detail, td_list))

    # TCGdex 的 logo 字段不带扩展名，且部分 set 只有 .png 没有 .webp，逐个探明
    def resolve(d):
        lg = d.get("logo")
        if not lg:
            return d
        for ext in (".webp", ".png"):
            if head_ok(lg + ext):
                d["logo"] = lg + ext
                return d
        d["logo"] = None
        return d

    print("探测 logo 扩展名…", flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        details = list(ex.map(resolve, details))
    with open(os.path.join(OUT, "src_tcgdex.json"), "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=1)
    print(f"tcgdex 详情 {len(details)} 条，带 logo {sum(1 for d in details if d.get('logo'))}")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    only = [a.lower() for a in sys.argv[1:]]
    if not only or "scryfall" in only:
        do_scryfall()
    if not only or "ygoprodeck" in only:
        do_ygoprodeck()
    if not only or "tcgdex" in only:
        do_tcgdex()


if __name__ == "__main__":
    main()