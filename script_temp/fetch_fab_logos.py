#!/usr/bin/env python3
"""抓取 Flesh and Blood 官方站（fabtcg.com）的系列 logo。

fabtcg.com 被 Cloudflare 挡普通请求（403），这里用 curl_cffi 伪装 Chrome TLS 指纹直连。
抓两类页面：
  /products/...        产品页（booster-set / armory-deck / blitz-deck / 其它）
  /digital-assets/...  官方营销素材页，里面放的是真正的系列 logo
    （如 arcane-rising -> ARC-1.png，armory-deck-arakni -> arakni_name.png）

选图优先级：文件名含 logo / _name / 形如 SETCODE-1 的 > 产品封面图。

输出 script_temp/out/src_fab.json
"""
from __future__ import annotations

import html
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

from curl_cffi import requests as cr

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
BASE = "https://fabtcg.com"
INDEX_PAGES = [f"{BASE}/products/", f"{BASE}/booster-sets/", f"{BASE}/other-products/",
               f"{BASE}/digital-assets/"]

SKIP = re.compile(r"favicon|FAB_Colour|LSS_LOGO|webtexture|slippy|slider|banner-?bg", re.I)
# 强 logo 信号：xxx_logo / xxx_name / 形如 ARC-1 的三字母代号
LOGO_HINT = re.compile(r"(logo|_name\.|-name\.|^[A-Z]{2,4}-\d+\.)", re.I)
COVER_HINT = re.compile(r"display|booster.?box|mock|mockup|dropshadow|_box|_pack|cover|banner", re.I)


def get(url: str) -> str:
    for _ in range(3):
        try:
            r = cr.get(url, impersonate="chrome", timeout=30)
            if r.status_code == 200:
                return r.text
        except Exception:
            pass
        time.sleep(1.2)
    return ""


def collect_urls() -> list[str]:
    urls: set[str] = set()
    idx = get(f"{BASE}/sitemap_index.xml")
    for sub in re.findall(r"<loc>([^<]+)</loc>", idx):
        for u in re.findall(r"<loc>([^<]+)</loc>", get(sub)):
            if "/products/" in u or "/digital-assets/" in u:
                urls.add(u.split("?")[0])
    for p in INDEX_PAGES:
        h = get(p)
        for u in re.findall(r'href="(' + BASE + r'/(?:products|digital-assets)/[^"#]*)"', h):
            urls.add(u.split("?")[0])
    return sorted(u for u in urls if u.rstrip("/") not in (BASE + "/products", BASE + "/digital-assets"))


def candidates(h: str) -> list[str]:
    imgs = re.findall(r'(https://cdn\.fabtcg\.com/[^"\'\s]+\.(?:png|jpg|jpeg|webp))', h, re.I)
    out = []
    for i in dict.fromkeys(imgs):
        name = i.split("/")[-1]
        if SKIP.search(i) or re.search(r"-\d+x\d+\.", name):  # 跳过缩略图尺寸变体
            continue
        out.append(i)
    return out


def pick(imgs: list[str]) -> str | None:
    for i in imgs:
        if LOGO_HINT.search(i.split("/")[-1]):
            return i
    for i in imgs:
        if COVER_HINT.search(i.split("/")[-1]):
            return i
    return imgs[0] if imgs else None


def one(url: str) -> dict | None:
    h = get(url)
    if not h:
        return None
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    title = html.unescape(re.sub(r"\s+", " ", t.group(1)).strip()) if t else ""
    title = re.sub(r"\s*[-|]\s*(Flesh and Blood|FAB|Card Gallery).*$", "", title, flags=re.I).strip()
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    head = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h1.group(1)))).strip() if h1 else ""
    imgs = candidates(h)
    return {"url": url, "name": head or title, "logo": pick(imgs), "images": imgs[:20]}


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    urls = collect_urls()
    print(f"待抓 {len(urls)} 页", flush=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        rows = [r for r in ex.map(one, urls) if r]
    with open(os.path.join(OUT, "src_fab.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(f"抓到 {len(rows)} 页，有图 {sum(1 for r in rows if r['logo'])}")
    for r in rows[:8]:
        print(f"  {r['name'][:40]:40s} -> {r['logo']}")


if __name__ == "__main__":
    main()