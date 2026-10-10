#!/usr/bin/env python3
"""抓取 ONE PIECE 官方站的产品 logo。

列表页 https://en.onepiece-cardgame.com/products/?subcategory=all&page=N（N=1..18）
-> 各产品详情页 -> 取 <title> 里的产品代号（ST-22 / OP-11 / EB-02 / PRB-01 …）
   与该页的 logo 图（形如 /onepiececg/bccard/en/product/.../logo.webp）

输出 script_temp/out/src_onepiece.json：{代号: logo_url}
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
BASE = "https://en.onepiece-cardgame.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
CODE_RE = re.compile(r"\b((?:ST|OP|EB|PRB|LD|GD|EX|P)\s?-?\s?\d{1,2})\b", re.I)
LOGO_RE = re.compile(r"[\"']([^\"']*?/logo\.webp)[\"']")
IMG_RE = re.compile(r"[\"']([^\"']*?(?:img_main|img_package|main)[^\"']*?\.(?:webp|png|jpg))[\"']", re.I)


def fetch(url: str) -> str:
    for _ in range(3):
        try:
            r = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=40)
            if r.returncode == 0 and r.stdout:
                return r.stdout
        except Exception:
            pass
        time.sleep(1.0)
    return ""


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    pages = []
    for n in range(1, 19):
        h = fetch(f"{BASE}/products/?subcategory=all&page={n}")
        ls = re.findall(r'href="(' + BASE + r'/products/[^"]+)"', h)
        ls = [u for u in ls if "subcategory" not in u]
        pages += ls
        print(f"list page {n}: +{len(set(ls))} (累计 {len(set(pages))})", flush=True)
        time.sleep(0.4)
    pages = sorted(set(pages))

    def one(url: str):
        h = fetch(url)
        if not h:
            return None
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        title = re.sub(r"\s+", " ", t.group(1)).strip() if t else ""
        logo = None
        m = LOGO_RE.search(h)
        if m:
            logo = m.group(1)
        else:
            m = IMG_RE.search(h)
            if m:
                logo = m.group(1)
        if logo and logo.startswith("//"):
            logo = "https:" + logo
        elif logo and logo.startswith("/"):
            logo = BASE + logo
        codes = CODE_RE.findall(title)
        return {"url": url, "title": title, "logo": logo,
                "codes": [c.upper().replace(" ", "") for c in codes]}

    with ThreadPoolExecutor(max_workers=4) as ex:
        rows = [r for r in ex.map(one, pages) if r]
    by_code = {}
    for r in rows:
        if not r["logo"]:
            continue
        for c in r["codes"] or []:
            by_code.setdefault(c, r["logo"])
    with open(os.path.join(OUT, "src_onepiece.json"), "w", encoding="utf-8") as f:
        json.dump({"by_code": by_code, "pages": rows}, f, ensure_ascii=False, indent=1)
    print(f"产品页 {len(rows)}，有 logo {sum(1 for r in rows if r['logo'])}，"
          f"代号映射 {len(by_code)}")


if __name__ == "__main__":
    main()