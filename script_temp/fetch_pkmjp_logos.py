#!/usr/bin/env python3
"""从 Bulbapedia 图库（archives.bulbagarden.net）抓日本宝可梦系列的 logo。

Bulbapedia 的扩展包 logo 文件名形如 `{系列代码}_{名称}_Logo.png`（如 S8b_VMAX_Climax_Logo.png），
系列代码正好等于 TCGPlayer 的 setCode —— 所以按代码做 allimages 前缀枚举即可命中。
没有代码的系列，退回「Bulbapedia 条目搜索 + prop=images」。

分两阶段运行（避免一次跑太久看不到进度）：
  python fetch_pkmjp_logos.py prefix   # 仅按代码前缀（快）
  python fetch_pkmjp_logos.py article  # 仅条目搜索（慢，补无代码的）

结果合并写 script_temp/out/src_pkmjp.json，进度写 script_temp/out/pkmjp.log
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor

import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
ARCH = "https://archives.bulbagarden.net/w/api.php"
BULBA = "https://bulbapedia.bulbagarden.net/w/api.php"
SRC = os.path.join(OUT, "src_pkmjp.json")
LOG = os.path.join(OUT, "pkmjp.log")
LOGO_RE = re.compile(r"logo.*\.(png|jpg|jpeg|webp)$", re.I)
PACK_RE = re.compile(r"(pack|box|booster|display)", re.I)
GENERIC_RE = re.compile(r"(energy|coin|sleeve|playmat|binder|damage|marker|token|backpack|shirt|bag)", re.I)


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def api(url: str, params: dict):
    for _ in range(3):
        try:
            r = requests.get(url, params=params, timeout=25,
                             headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(0.8)
    return {}


def norm(s: str) -> str:
    """折变音符号后再去标点：Bulbapedia 的 'Pokémon' 与 TCGPlayer 的 'Pokemon' 要能对上。"""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def files_by_prefix(prefix: str) -> list[dict]:
    out, cont = [], {}
    for _ in range(3):
        p = {"action": "query", "list": "allimages", "aiprefix": prefix,
             "ailimit": 100, "format": "json"}
        p.update(cont)
        d = api(ARCH, p)
        out += d.get("query", {}).get("allimages", [])
        cont = d.get("continue") or {}
        if not cont:
            break
    return out


def code_hit(base: str, code: str) -> bool:
    """完整且大小写敏感：'SV' 不算命中 'SV10.5_BLK_Logo'，'sH' 不算命中 'SHFiguarts_Logo'，
    'sC' 不算命中 'SC_Shiny_Collection'。"""
    if not code or not base.startswith(code):
        return False
    rest = base[len(code):]
    return not rest or not rest[0].isalnum()


def pick_logo(files: list[dict], code: str, name: str) -> tuple[str | None, int]:
    """Bulbapedia 上不是每个系列都有 _Logo 文件，很多只有 _pack / _Box 包装图，
    按 logo > 包装图 的优先级挑；代码必须是完整匹配，名称吻合再加分。"""
    code_n, name_n = norm(code), norm(name)
    best, best_score = None, 0
    for f in files:
        fn = f["name"]
        base = re.sub(r"\.(png|jpg|jpeg|webp)$", "", fn, flags=re.I)
        nb = norm(base)
        score = 0
        if LOGO_RE.search(fn):
            score += 2
        elif PACK_RE.search(fn):
            score += 1
        else:
            score -= 2
        if GENERIC_RE.search(fn):
            score -= 3
        if code_hit(base, code):
            score += 3    # 大小写敏感：sC（喷火龙预组）与 SC（闪色收藏）是不同系列
        if name_n and name_n in nb:
            score += 3
        if score > best_score:
            best, best_score = f["url"], score
    return best, best_score


def article_logo(name: str, plain: str = "") -> str | None:
    """无代码时的兜底：opensearch 找条目（比 list=search 准得多）-> 取主图 / 条目图片里的 logo。"""
    key = norm(plain or name)
    titles: list[str] = []
    for q in [x for x in (plain, name) if x]:
        d = api(BULBA, {"action": "opensearch", "search": q, "limit": 5, "format": "json"})
        if isinstance(d, list) and len(d) > 1:
            titles += d[1]
    seen = set()
    for title in titles:
        if title in seen:
            continue
        seen.add(title)
        if key and key not in norm(title):
            continue
        # 1) 信息框主图
        d1 = api(BULBA, {"action": "query", "titles": title, "prop": "pageimages",
                         "pithumbsize": 600, "format": "json"})
        for pg in ((d1.get("query") or {}).get("pages") or {}).values():
            src = ((pg.get("thumbnail") or {}).get("source") or "")
            fn = src.split("/")[-1]
            head = next((w for w in re.split(r"[\s:,-]+", plain or name) if len(w) >= 5), "")
            if (src and (LOGO_RE.search(fn) or PACK_RE.search(fn)) and not GENERIC_RE.search(fn)
                    and (key in norm(fn) or (head and norm(head) in norm(fn)))):
                return src
        # 2) 条目图片里带 logo 的
        d2 = api(BULBA, {"action": "query", "titles": title, "prop": "images",
                         "imlimit": 200, "format": "json"})
        for pg in ((d2.get("query") or {}).get("pages") or {}).values():
            for im in pg.get("images", []):
                fn = im["title"].replace("File:", "")
                if LOGO_RE.search(fn) and key and key in norm(fn):
                    d3 = api(ARCH, {"action": "query", "titles": "File:" + fn,
                                    "prop": "imageinfo", "iiprop": "url", "format": "json"})
                    for p3 in ((d3.get("query") or {}).get("pages") or {}).values():
                        for ii in p3.get("imageinfo", []):
                            return ii["url"]
    return None


def load_items() -> list[dict]:
    agg = json.load(open(os.path.join(OUT, "all_agg.json"), encoding="utf-8"))
    series = list(agg["Pokemon Japan"]["sets"])
    code = {}
    for line in open(os.path.join(BASE, "category_cards_final", "category_cards",
                                  "85_Pokemon_Japan", "products.jsonl"), encoding="utf-8"):
        o = json.loads(line)
        code.setdefault(o["setName"], o.get("setCode") or "")

    def parse_code(n: str) -> str:
        m = re.match(r"^\s*([A-Za-z0-9.\-]{1,8})\s*:\s*", n)
        return m.group(1) if m else ""

    items = []
    for n in series:
        c = (code.get(n) or parse_code(n)).strip()
        plain = re.sub(r"^\s*[A-Za-z0-9.\-]{1,8}\s*:\s*", "", n).strip()
        items.append({"name": n, "code": c, "plain": plain})
    return items


def save(rows: list[dict]) -> None:
    with open(SRC, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "prefix"
    items = load_items()
    rows = json.load(open(SRC, encoding="utf-8")) if os.path.isfile(SRC) else [
        {**i, "logo": None} for i in items]
    by_name = {r["name"]: r for r in rows}
    log(f"[{mode}] 系列 {len(items)}，带代码 {sum(1 for i in items if i['code'])}")

    if mode == "prefix":
        codes = sorted({i["code"] for i in items if i["code"]})

        def work(c):
            return c, files_by_prefix(c)

        pf = {}
        with ThreadPoolExecutor(max_workers=6) as ex:
            for i, (c, files) in enumerate(ex.map(work, codes)):
                pf[c] = files
                if (i + 1) % 50 == 0:
                    log(f"  prefix 探测 {i + 1}/{len(codes)}")
        hit = 0
        for it in items:
            if not it["code"]:
                continue
            url, score = pick_logo(pf.get(it["code"], []), it["code"], it["plain"])
            if url and score >= 3:
                by_name[it["name"]]["logo"] = url
                hit += 1
        log(f"  prefix 命中 {hit}")
        save(rows)
    else:
        todo = [it for it in items if not by_name[it["name"]].get("logo")]
        log(f"  article 待补 {len(todo)}")
        def work(it):
            return it["name"], article_logo(it["name"], it.get("plain", ""))
        with ThreadPoolExecutor(max_workers=6) as ex:
            for i, (nm, url) in enumerate(ex.map(work, todo)):
                if url:
                    by_name[nm]["logo"] = url
                if (i + 1) % 25 == 0:
                    log(f"  article {i + 1}/{len(todo)}")
                    save(rows)

    save(rows)
    hit = sum(1 for r in rows if r.get("logo"))
    log(f"[{mode}] 完成，累计命中 {hit}/{len(rows)}")
    print(f"命中 {hit}/{len(rows)}")


if __name__ == "__main__":
    main()