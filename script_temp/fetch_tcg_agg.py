#!/usr/bin/env python3
"""抓取 TCGPlayer 搜索聚合的 setName 分布，用于校验本地卡片数据的完整性。

只读接口：POST mp-search-api.tcgplayer.com/v1/search/request，size=1 只取聚合。
结果存 script_temp/out/agg_<slug>.json。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
URL = "https://mp-search-api.tcgplayer.com/v1/search/request"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

LINES = {
    "pokemon": ("Pokemon", "Cards"),
    "pokemon_japan": ("Pokemon Japan", "Cards"),
    "magic": ("Magic: The Gathering", "Cards"),
    "yugioh": ("YuGiOh", "Cards"),
    "one_piece": ("One Piece Card Game", "Cards"),
    "lorcana": ("Disney Lorcana", "Cards"),
    "fab": ("Flesh and Blood TCG", "Cards"),
    "dbsc": ("Dragon Ball Super: Masters", "Cards"),
}


def fetch(line: str, ctype: str):
    body = {"filters": {"match": {"productLineName": [line], "productTypeName": [ctype]}},
            "mpfev": 5489, "from": 0, "size": 1}
    r = subprocess.run(
        ["curl", "-s", "--max-time", "30", "-X", "POST", URL,
         "-H", "Content-Type: application/json", "-H", f"User-Agent: {UA}",
         "-H", "Origin: https://www.tcgplayer.com", "-H", "Referer: https://www.tcgplayer.com/",
         "-d", json.dumps(body)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=40)
    return json.loads(r.stdout)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    for slug, (line, ctype) in LINES.items():
        if only and slug not in only:
            continue
        try:
            d = fetch(line, ctype)
            r = d["results"][0]
            agg = r["aggregations"]["setName"]
        except Exception as e:
            print(f"{slug:16s} FAILED {e}", flush=True)
            continue
        out = {"productLineName": line,
               "totalResults": r.get("totalResults"),
               "sets": {x["value"]: int(x["count"]) for x in agg}}
        with open(os.path.join(OUT, f"agg_{slug}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"{slug:16s} sets={len(agg):4d} total={r.get('totalResults')}", flush=True)
        time.sleep(1.2)


if __name__ == "__main__":
    main()