# -*- coding: utf-8 -*-
"""按 doc/seriesToLogo.md 下载全部系列 logo，按 8 个品类分目录存放。

用法：
    python script_temp/download_series_logos.py --dry-run
    python script_temp/download_series_logos.py --download
    python script_temp/download_series_logos.py --verify

对应关系写入 logo-set/_mapping.csv（品类, 系列名, 文件名, URL, 来源）。
"""
import argparse
import csv
import io
import os
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(ROOT, "doc", "seriesToLogo.md")
OUT_DIR = os.path.join(ROOT, "logo-set")
MAPPING_CSV = os.path.join(OUT_DIR, "_mapping.csv")

# Windows 文件名非法字符 → 全角等价字符（保持可读性，对应关系见 _mapping.csv）
ILLEGAL = {
    ":": "：", "?": "？", "*": "＊", '"': "＂",
    "<": "＜", ">": "＞", "|": "｜", "/": "／", "\\": "＼",
}
RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
# Cloudflare 对这些站点只放行 requests 默认 UA，浏览器 UA 反而 403
PLAIN_UA_HOSTS = {"archives.bulbagarden.net"}
RETRY_FIRST_UA_HOSTS = {"cdn.fabtcg.com"}

MAGIC = [
    (b"\xff\xd8\xff", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"GIF8", ".gif"),
    (b"RIFF", ".webp"),          # RIFF....WEBP
    (b"<svg", ".svg"),
    (b"<?xml", ".svg"),
    (b"BM", ".bmp"),
]


def sanitize(name):
    """系列名 → Windows 合法文件名（不含扩展名）。"""
    out = "".join(ILLEGAL.get(ch, ch) for ch in name)
    out = "".join(ch for ch in out if ord(ch) >= 32)
    out = out.strip().rstrip(". ")
    if out.upper() in RESERVED:
        out += "_"
    return out


def cat_dir(cat):
    """品类名 → 子目录名（Windows 合法）。"""
    return sanitize(cat)


def parse_md():
    """返回 (主表行, 3.3 补充表行)。每行为 dict(category, series, url, counts, source)。"""
    with open(MD_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()

    sec2_start = sec3_start = sec4_start = None
    for i, ln in enumerate(lines):
        if ln.startswith("## 二、"):
            sec2_start = i
        elif ln.startswith("## 三、"):
            sec3_start = i
        elif ln.startswith("## 四、"):
            sec4_start = i
    sec3_3 = None
    for i, ln in enumerate(lines):
        if ln.startswith("### 3.3"):
            sec3_3 = i
            break

    def rows(a, b, layout):
        out = []
        for ln in lines[a:b]:
            if not ln.startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < len(layout) or set(cells[0]) <= set("- "):
                continue
            rec = dict(zip(layout, cells))
            rec["url"] = rec["url"].split()[0] if rec["url"].strip() else ""
            if rec["series"] and rec["series"] != "系列":
                out.append(rec)
        return out

    main_layout = ["category", "series", "url", "counts", "source"]
    main = rows(sec2_start, sec3_start, main_layout)
    extra = rows(sec3_3, sec4_start, ["category", "series", "url", "source", "why"])
    return main, extra


def ext_from_url(url):
    path = url.split("?")[0].split("#")[0]
    ext = os.path.splitext(path)[1].lower()
    return ext if re.fullmatch(r"\.[a-z0-9]{2,5}", ext) else ""


def build_plan(main):
    """生成下载计划：category -> [(series, filename, url, source)]，并报告冲突。"""
    plan = defaultdict(list)
    seen = defaultdict(list)
    for rec in main:
        if not rec["url"]:
            continue
        cat = rec["category"]
        base = sanitize(rec["series"])
        seen[(cat, base)].append(rec["series"])
        plan[cat].append({
            "series": rec["series"],
            "base": base,
            "url": rec["url"],
            "source": rec["source"],
            "ext": ext_from_url(rec["url"]),
        })
    collisions = {k: v for k, v in seen.items() if len(v) > 1}
    return plan, collisions


def cmd_dry_run(main, extra):
    plan, collisions = build_plan(main)
    print(f"主表行数：{len(main)}；其中有 URL：{sum(1 for r in main if r['url'])}")
    print(f"无 URL：{sum(1 for r in main if not r['url'])}")
    print()
    total = 0
    for cat, items in plan.items():
        urls = {it["url"] for it in items}
        maxlen = max(len(os.path.join(OUT_DIR, cat_dir(cat), it["base"])) for it in items)
        noext = sum(1 for it in items if not it["ext"])
        print(f"  {cat}: {len(items)} 条 / {len(urls)} 个唯一 URL；最长路径 {maxlen}；无扩展名 {noext}")
        total += len(items)
    print(f"\n合计待下载 {total} 个文件，唯一 URL {len({r['url'] for r in main if r['url']})} 个")

    print(f"\n文件名冲突（同品类内系列名清洗后重名）：{len(collisions)}")
    for (cat, base), names in collisions.items():
        print(f"  [{cat}] {base} <- {names}")

    bad = [r for r in main if r["url"] and any(c in r["series"] for c in ILLEGAL)]
    print(f"\n系列名含非法字符需替换：{len(bad)}")
    for r in bad[:8]:
        print(f"  {r['series']}  ->  {sanitize(r['series'])}")

    longpath = [it for cat, items in plan.items() for it in items
                if len(os.path.join(OUT_DIR, cat_dir(cat), it["base"])) > 240]
    print(f"\n路径超 240 字符：{len(longpath)}")
    for it in longpath[:5]:
        print(f"  {it['base']}")

    # 3.3 补充表是否已被主表覆盖
    main_pairs = {(r["category"], r["series"], r["url"]) for r in main}
    miss33 = [r for r in extra if (r["category"], r["series"], r["url"]) not in main_pairs]
    print(f"\n3.3 表共 {len(extra)} 条，主表未覆盖的 {len(miss33)} 条")
    for r in miss33[:10]:
        print(f"  [{r['category']}] {r['series']} {r['url']}")

    exts = Counter(ext_from_url(r["url"]) or "(无)" for r in main if r["url"])
    print(f"\n扩展名分布：{dict(exts)}")
    hosts = Counter(r["url"].split("/")[2] for r in main if r["url"])
    print(f"域名分布：{dict(hosts)}")


def sniff_ext(content):
    head = content[:64]
    for magic, ext in MAGIC:
        if head.startswith(magic):
            if magic == b"RIFF":
                return ".webp" if content[8:12] == b"WEBP" else ".webp"
            if magic in (b"<svg", b"<?xml"):
                return ".svg"
            return ext
    return ""


def session_for(url, pool):
    """按域名返回会话：部分站点必须用 requests 默认 UA。"""
    host = url.split("/")[2]
    if host not in pool:
        s = requests.Session()
        if host not in PLAIN_UA_HOSTS:
            s.headers.update({"User-Agent": UA})
        pool[host] = s
    return pool[host]


def fetch(url, session):
    """返回 (content, ext, err)。先 requests，失败再用 curl_cffi 伪装 TLS。"""
    last = ""
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200 and r.content:
                return r.content, sniff_ext(r.content), ""
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
        time.sleep(1 + attempt)
    if url.split("/")[2] in PLAIN_UA_HOSTS:
        return None, "", last
    try:
        from curl_cffi import requests as creq
        r = creq.get(url, impersonate="chrome", timeout=30)
        if r.status_code == 200 and r.content:
            return r.content, sniff_ext(r.content), ""
        last = f"HTTP {r.status_code} (curl_cffi)"
    except Exception as e:  # noqa: BLE001
        last = f"{last} | curl_cffi {type(e).__name__}: {e}"
    return None, "", last


def write_file(cat, base, url, content, sniffed, url_ext):
    ext = sniffed or url_ext or ".png"
    fname = base + ext
    path = os.path.join(OUT_DIR, cat_dir(cat), fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)
    return fname, len(content)


def cmd_retry_failed(workers):
    """只重试 _mapping.csv 中 FAILED 的行，成功后回写清单。"""
    with open(MAPPING_CSV, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    failed = [r for r in rows if r["状态"] == "FAILED"]
    print(f"待重试 {len(failed)} 条")
    if not failed:
        return
    pool = {}
    urls = sorted({r["URL"] for r in failed})
    cache = {}
    print(f"唯一 URL {len(urls)}，并发 {workers}")
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch, u, session_for(u, pool)): u for u in urls}
        for fut in as_completed(futs):
            u = futs[fut]
            cache[u] = fut.result()
            done += 1
            if done % 100 == 0:
                print(f"  ... {done}/{len(urls)}")

    ok = still = 0
    for r in rows:
        if r["状态"] != "FAILED":
            continue
        content, sniffed, err = cache[r["URL"]]
        if content is None:
            still += 1
            r["备注"] = err
            continue
        fname, size = write_file(r["品类"], os.path.splitext(r["文件名"])[0] if r["文件名"]
                                 else sanitize(r["系列"]), r["URL"], content, sniffed,
                                 ext_from_url(r["URL"]))
        r["文件名"] = fname
        r["状态"] = "OK" if size >= 1024 else f"SUSPECT_SMALL({size}B)"
        r["备注"] = ""
        ok += 1
    with open(MAPPING_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"重试完成：成功 {ok}，仍失败 {still}")
    for r in rows:
        if r["状态"] == "FAILED":
            print(f"  [{r['品类']}] {r['系列']} {r['URL']} {r['备注']}")


def cmd_download(main, workers):
    plan, collisions = build_plan(main)
    os.makedirs(OUT_DIR, exist_ok=True)
    pool = {}

    # URL 缓存：同一 URL 只下载一次
    cache = {}
    jobs = []
    for cat, items in plan.items():
        for it in items:
            jobs.append((cat, it))

    def work(job):
        cat, it = job
        return it["url"], fetch(it["url"], session_for(it["url"], pool))

    print(f"开始下载 {len(jobs)} 个文件（唯一 URL {len({it['url'] for _, it in jobs})}），并发 {workers}")
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(work, j): j for j in jobs}
        for fut in as_completed(futs):
            url, (content, ext, err) = fut.result()
            cache[url] = (content, ext, err)
            done += 1
            if done % 200 == 0:
                print(f"  ... {done}/{len(jobs)}")

    ok = skipped = failed = 0
    rows = []
    for cat, items in plan.items():
        cdir = os.path.join(OUT_DIR, cat_dir(cat))
        os.makedirs(cdir, exist_ok=True)
        for it in items:
            content, sniffed, err = cache[it["url"]]
            if content is None:
                failed += 1
                rows.append([cat, cat_dir(cat), it["series"], "", it["url"],
                             it["source"], "FAILED", err])
                continue
            ext = sniffed or it["ext"] or ".png"
            fname = it["base"] + ext
            path = os.path.join(cdir, fname)
            with open(path, "wb") as f:
                f.write(content)
            size = len(content)
            note = "OK" if size >= 1024 else f"SUSPECT_SMALL({size}B)"
            if size >= 1024:
                ok += 1
            else:
                skipped += 1
            rows.append([cat, cat_dir(cat), it["series"], fname, it["url"],
                         it["source"], note, ""])

    with open(MAPPING_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["品类", "目录", "系列", "文件名", "URL", "来源", "状态", "备注"])
        w.writerows(rows)
    print(f"\n完成：正常 {ok}，可疑小文件 {skipped}，失败 {failed}；清单 {MAPPING_CSV}")

    print("\n失败明细：")
    for r in rows:
        if r[6] == "FAILED":
            print(f"  [{r[0]}] {r[2]} -> {r[4]}  {r[7]}")
    print("\n可疑小文件（<1KB）：")
    for r in rows:
        if r[6].startswith("SUSPECT"):
            print(f"  [{r[0]}] {r[2]} -> {r[3]} {r[6]}  {r[4]}")


def cmd_verify(main):
    plan, _ = build_plan(main)
    if not os.path.exists(MAPPING_CSV):
        print("缺少 _mapping.csv，请先 --download")
        return
    with open(MAPPING_CSV, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    by_cat = defaultdict(lambda: [0, 0, 0])
    missing = []
    for r in rows:
        cat = r["品类"]
        if r["状态"] == "FAILED":
            by_cat[cat][2] += 1
            continue
        p = os.path.join(OUT_DIR, r["目录"], r["文件名"])
        if os.path.exists(p) and os.path.getsize(p) > 0:
            by_cat[cat][0] += 1
        else:
            by_cat[cat][1] += 1
            missing.append(r)
    print(f"{'品类':<28}{'期望':>6}{'已下载':>8}{'缺失':>6}")
    exp = {cat: len(items) for cat, items in plan.items()}
    tot = [0, 0, 0]
    for cat in plan:
        e = exp[cat]
        g, m, f = by_cat[cat]
        print(f"{cat:<28}{e:>6}{g:>8}{m + f:>6}")
        tot = [tot[0] + e, tot[1] + g, tot[2] + m + f]
    print(f"{'合计':<28}{tot[0]:>6}{tot[1]:>8}{tot[2]:>6}")
    if missing:
        print("\n缺失明细：")
        for r in missing:
            print(f"  [{r['品类']}] {r['系列']} {r['URL']} {r['备注']}")
    # 磁盘上多余文件
    on_disk = 0
    for cat in plan:
        d = os.path.join(OUT_DIR, cat_dir(cat))
        if os.path.isdir(d):
            on_disk += sum(1 for n in os.listdir(d) if os.path.isfile(os.path.join(d, n)))
    print(f"\n磁盘上文件总数（8 个品类目录）：{on_disk}")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--download", action="store_true")
    g.add_argument("--verify", action="store_true")
    g.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    if args.retry_failed:
        cmd_retry_failed(args.workers)
        return
    main_rows, extra_rows = parse_md()
    if args.dry_run:
        cmd_dry_run(main_rows, extra_rows)
    elif args.download:
        cmd_download(main_rows, args.workers)
    else:
        cmd_verify(main_rows)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()