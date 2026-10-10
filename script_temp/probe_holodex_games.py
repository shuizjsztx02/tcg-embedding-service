#!/usr/bin/env python3
"""用 Holodex CDN 探针判断它是否收录某个游戏。

原理：https://holodex-prod-bucket.b-cdn.net/sets/{prefix}_{setId}/logo.webp
     存在返回 200，不存在返回 403。
Holodex 的 set id 对多数游戏就是 TCGPlayer 的 setId（Pokémon 用旧 set code）。
"""
from __future__ import annotations

import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

CDN = "https://holodex-prod-bucket.b-cdn.net/sets/{}/logo.webp"

# 目标品类 -> (本地 setId 样本, 候选前缀)
TARGETS = {
    "Flesh and Blood": ([2732, 23540, 24266], ["fab", "fabtcg", "fnt", "flesh", "fleshblood", "fob"]),
    "Pokemon Japan": ([23644, 23708, 23859], ["pj", "jp", "pkmjp", "pokemonjp", "ja", "pkm", "pkmn", "jp_pkm"]),
    "Weiss Schwarz": ([1603, 1601, 1604], ["ws", "weiss", "wsc", "weissschwarz", "wsr"]),
    "Cardfight Vanguard": ([1573, 1120, 1549], ["vg", "vng", "cfv", "vanguard", "cardfight"]),
    "Dragon Ball Super Masters": ([1962, 2070, 2173], ["dbsc", "dbs", "dbstcg"]),
}


def probe(url: str) -> int:
    for _ in range(2):
        try:
            r = subprocess.run(["curl", "-s", "-o", os.devnull, "-w", "%{http_code}",
                                "--max-time", "12", url],
                               capture_output=True, text=True, timeout=18)
            return int((r.stdout or "0").strip() or 0)
        except Exception:
            pass
    return 0


def main() -> None:
    jobs = []
    for game, (ids, prefixes) in TARGETS.items():
        for p in prefixes:
            for i in ids:
                jobs.append((game, p, i, CDN.format(f"{p}_{i}")))
    with ThreadPoolExecutor(max_workers=8) as ex:
        codes = list(ex.map(lambda j: probe(j[3]), jobs))
    hits = {}
    for (game, p, i, url), c in zip(jobs, codes):
        if c == 200:
            hits.setdefault(game, []).append(f"{p}_{i}")
    for game in TARGETS:
        print(f"{game:28s} -> {hits.get(game) or '无 200 命中（该游戏不在 Holodex）'}")


if __name__ == "__main__":
    main()