#!/usr/bin/env python3
"""对已生成的映射做质量审计，专找"看着配上了、其实是错的"。

检查项：
  A. 同一个 logo URL 被多个品线/不同系列共用（继承是允许的，但跨品线共用一定是错）
  B. 系列名与源侧名称几乎没有共同词元（靠代码硬配的情况要人工确认）
  C. Magic 里落到通用 default.svg 的
  D. 同一品线内，一个 URL 被 >=5 个不同系列共用
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
STOP = {"the", "of", "a", "and", "vol", "volume", "set", "deck", "pack", "box", "cards", "card"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def toks(s: str) -> set[str]:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    out = set()
    for t in re.findall(r"[a-z0-9]+", s.lower()):
        if t in STOP or len(t) < 3:
            continue
        if t.endswith("s") and len(t) > 4:
            t = t[:-1]
        out.add(t)
    return out


def main() -> None:
    rows = json.load(open(os.path.join(OUT, "series_logo_rows.json"), encoding="utf-8"))

    url_lines: dict[str, set] = defaultdict(set)
    url_names: dict[str, list] = defaultdict(list)
    for line, rs in rows.items():
        for r in rs:
            if r["logo"]:
                url_lines[r["logo"]].add(line)
                url_names[r["logo"]].append((line, r["setName"], r["source"], r["match"]))

    print("=== A. 跨品线共用一个 logo（必为错配） ===")
    bad = 0
    for url, lines in url_lines.items():
        if len(lines) > 1:
            bad += 1
            print(f"  {url[:78]}")
            for line, name, src, m in url_names[url]:
                print(f"      [{line[:20]:20s}] {name[:44]:44s} {src}/{m}")
    if not bad:
        print("  无")

    print("\n=== B. 系列名与来源名称几乎无共同词元（高风险，需人工确认） ===")
    risky = []
    for line, rs in rows.items():
        for r in rs:
            if not r["logo"] or r["match"] in ("override", "gapfix"):
                continue
            tcg = toks(r["setName"])
            fn = toks(r["logo"].split("/")[-1].rsplit(".", 1)[0])
            if tcg and fn and not (tcg & fn):
                risky.append((line, r["setName"], r["source"], r["match"], r["logo"].split("/")[-1]))
    print(f"  共 {len(risky)} 条（这些是靠编号/代码对上的，词元不通是正常的，仅列出抽查）")
    for x in risky[:20]:
        print(f"  [{x[0][:18]:18s}] {x[1][:40]:40s} {x[2]}/{x[3]:8s} {x[4][:44]}")

    print("\n=== C. Magic 落到通用 default.svg ===")
    n = 0
    for line, rs in rows.items():
        for r in rs:
            if r["logo"] and "default.svg" in r["logo"]:
                n += 1
                if n <= 10:
                    print(f"  {r['setName'][:50]:50s} {r['logo']}")
    print(f"  共 {n} 条")

    print("\n=== D. 同一品线内一个 URL 被 >=5 个系列共用 ===")
    for line, rs in rows.items():
        c = Counter(r["logo"] for r in rs if r["logo"])
        for url, k in c.items():
            if k >= 5:
                names = [r["setName"] for r in rs if r["logo"] == url]
                print(f"  [{line[:22]:22s}] {k:3d} 个系列共用 {url.split('/')[-1][:46]}")
                print(f"      例：{'、'.join(n[:26] for n in names[:4])}")

    print("\n=== E. 匹配方式分布 ===")
    c = Counter((r["source"], r["match"]) for rs in rows.values() for r in rs if r["logo"])
    for k, v in c.most_common():
        print(f"  {k[0]:22s} {k[1]:10s} {v}")


if __name__ == "__main__":
    main()