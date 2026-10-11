#!/usr/bin/env python3
"""校验 seriesToLogo.md 里所有 logo URL 是否真的能取到图。

并发发 HEAD 请求，统计每个来源的可用率，并把失效 URL 单独列出。
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
MD = os.path.join(BASE, "doc", "seriesToLogo.md")


def check(url: str) -> tuple[str, int, str]:
    """两种客户端都要试——不同图床拦截策略相反：
    wikia/fabtcg 只能 curl_cffi，archives.bulbagarden.net 只能普通 requests。"""
    last = (url, 0, "")
    clients = []
    try:
        from curl_cffi import requests as cr
        clients.append(lambda: (lambda r: (r.status_code, r.headers.get("content-type", "")))(
            cr.get(url, impersonate="chrome", timeout=25, allow_redirects=True)))
    except ImportError:
        pass
    try:
        import requests as rq
        clients.append(lambda: (lambda r: (r.status_code, r.headers.get("content-type", "")))(
            rq.get(url, timeout=25, allow_redirects=True,
                   headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})))
    except ImportError:
        pass
    for _ in range(2):
        for fn in clients:
            try:
                code, ctype = fn()
                code, ctype = int(code), (ctype or "").strip()
                if code == 200:
                    return url, code, ctype
                last = (url, code, ctype)
            except Exception:
                pass
    return last


def main() -> None:
    rows = json.load(open(os.path.join(OUT, "series_logo_rows.json"), encoding="utf-8"))
    items = [(line, r["setName"], r["logo"], r["source"])
             for line, rs in rows.items() for r in rs if r["logo"]]
    print(f"待校验 {len(items)} 条", flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(lambda it: check(it[2]), items))
    stat = defaultdict(Counter)
    dead = []
    for (line, name, url, source), (u, code, ctype) in zip(items, res):
        ok = code == 200 and ctype.startswith(("image/", "text/xml", "application/xml",
                                              "binary/octet-stream"))
        stat[source][("ok" if ok else "bad")] += 1
        if not ok:
            dead.append((source, line, name, url, code, ctype))
    for source, c in stat.items():
        tot = sum(c.values())
        print(f"{source:20s} {c['ok']:5d}/{tot:5d} 可用  ({c['ok'] / tot * 100:.1f}%)")
    print(f"\n失效 {len(dead)} 条：")
    for d in dead[:40]:
        print(f"  [{d[0]}] {d[1][:14]:14s} {d[2][:38]:38s} http={d[4]} {d[5]} {d[3]}")
    with open(os.path.join(OUT, "dead_logos.json"), "w", encoding="utf-8") as f:
        json.dump(dead, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()