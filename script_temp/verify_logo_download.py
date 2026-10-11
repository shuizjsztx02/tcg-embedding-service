# -*- coding: utf-8 -*-
"""独立核对：doc/seriesToLogo.md 的 logo URL 与 logo-set/ 下文件是否一一对应。

不复用下载脚本的清单，只读 md + 文件系统。
用法：python script_temp/verify_logo_download.py
"""
import hashlib
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "doc", "seriesToLogo.md")
OUT = os.path.join(ROOT, "logo-set")

ILLEGAL = {":": "：", "?": "？", "*": "＊", '"': "＂",
           "<": "＜", ">": "＞", "|": "｜", "/": "／", "\\": "＼"}


def sanitize(name):
    out = "".join(ILLEGAL.get(ch, ch) for ch in name)
    out = "".join(ch for ch in out if ord(ch) >= 32).strip().rstrip(". ")
    return out + "_" if out.upper() in {"CON", "PRN", "AUX", "NUL"} else out


def parse():
    lines = open(MD, encoding="utf-8").read().splitlines()
    sec2 = next(i for i, l in enumerate(lines) if l.startswith("## 二、"))
    sec3 = next(i for i, l in enumerate(lines) if l.startswith("## 三、"))
    recs = []
    for ln in lines[sec2:sec3]:
        if not ln.startswith("|"):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) < 5 or set(c[0]) <= set("- ") or c[1] == "系列":
            continue
        url = c[2].split()[0] if c[2].strip() else ""
        recs.append({"cat": c[0], "series": c[1], "url": url, "src": c[4]})
    return recs


MAGIC = {b"\xff\xd8\xff": "jpeg", b"\x89PNG": "png", b"GIF8": "gif",
         b"RIFF": "webp", b"BM": "bmp", b"<svg": "svg", b"<?xml": "svg"}


def kind(path):
    with open(path, "rb") as f:
        head = f.read(64)
    for m, k in MAGIC.items():
        if head.startswith(m):
            return k
    if re.match(rb"\s*<(\?xml|svg)", head):
        return "svg"
    if head.lstrip()[:1] == b"<":
        return "html_or_xml"
    return "unknown"


def main():
    recs = parse()
    with_url = [r for r in recs if r["url"]]
    no_url = [r for r in recs if not r["url"]]
    print(f"md 主表：{len(recs)} 行；有 URL {len(with_url)}；无 URL {len(no_url)}")

    missing, mismatched = [], []
    kind_cnt = defaultdict(int)
    url_bytes = defaultdict(set)
    ext_mismatch = []
    for r in with_url:
        d = os.path.join(OUT, sanitize(r["cat"]))
        base = sanitize(r["series"])
        cands = [base + e for e in (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".bmp")]
        hit = [c for c in cands if os.path.isfile(os.path.join(d, c))]
        if not hit:
            missing.append(r)
            continue
        if len(hit) > 1:
            mismatched.append((r, hit))
        p = os.path.join(d, hit[0])
        size = os.path.getsize(p)
        k = kind(p)
        kind_cnt[k] += 1
        if size < 200 and k != "svg":
            kind_cnt["tiny"] += 1
        # URL 扩展名 vs 实际格式
        uext = os.path.splitext(r["url"].split("?")[0])[1].lower().lstrip(".")
        if uext and k not in (uext, "jpeg" if uext == "jpg" else uext) and not (
                uext == "jpg" and k == "jpeg"):
            ext_mismatch.append((r, hit[0], uext, k))
        with open(p, "rb") as f:
            url_bytes[r["url"]].add(hashlib.md5(f.read()).hexdigest())

    print(f"\n按 md 逐行核对：命中 {len(with_url) - len(missing)} / {len(with_url)}")
    print(f"缺失：{len(missing)}")
    for r in missing[:40]:
        print(f"  [{r['cat']}] {r['series']}  <- {r['url']}")
    print(f"\n同品类内同系列名多文件：{len(mismatched)}")
    for r, hit in mismatched[:10]:
        print(f"  [{r['cat']}] {r['series']} -> {hit}")
    print(f"\n文件真实格式：{dict(kind_cnt)}")
    print(f"URL 扩展名与真实格式不符：{len(ext_mismatch)}")
    for r, fn, ue, k in ext_mismatch[:15]:
        print(f"  [{r['cat']}] {fn}  URL是 .{ue}，实际 {k}")

    dup = {u: v for u, v in url_bytes.items() if len(v) > 1}
    print(f"\n同一 URL 下载出不同内容：{len(dup)}")
    for u, v in list(dup.items())[:10]:
        print(f"  {u} -> {len(v)} 种内容")

    # 磁盘总览
    total = 0
    print("\n各品类目录文件数：")
    for cat in dict.fromkeys(r["cat"] for r in recs):
        d = os.path.join(OUT, sanitize(cat))
        n = sum(1 for x in os.listdir(d) if os.path.isfile(os.path.join(d, x))) if os.path.isdir(d) else 0
        exp = sum(1 for r in with_url if r["cat"] == cat)
        flag = "" if n == exp else "  <== 不一致"
        print(f"  {cat}: 磁盘 {n} / md 期望 {exp}{flag}")
        total += n
    print(f"  合计 {total}（另 _mapping.csv 不计入）")

    print(f"\nmd 中无 logo 的系列：{len(no_url)} 个（无文件，符合预期）")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()