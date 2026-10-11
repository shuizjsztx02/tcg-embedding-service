#!/usr/bin/env python3
"""合并各子 agent 产出的 gapfix_*.json，并逐个校验。

做四件事：
  1. setName 必须确实出现在 series_logo_rows.json 对应品线的待补清单里（防拼错/防覆盖已有结果）
  2. 每个 URL 实际发请求，必须是 200 且 content-type 是图片（fabtcg CDN 的
     binary/octet-stream 也算）
  3. 同一 setName 被多个 agent 报不同 URL 时报冲突，只保留第一个
  4. 输出 script_temp/out/gapfix_merged.json（供 build_series_logo_v2.py 消费）
     和被拒清单 script_temp/out/gapfix_rejected.json
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
OK_TYPES = ("image/", "text/xml", "application/xml", "binary/octet-stream")
STOP = {"the", "of", "a", "and", "vol", "volume", "set", "deck", "pack", "box",
        "cards", "card", "edition"}
ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def check(url: str) -> tuple[int, str]:
    """校验 URL 可取到图。

    必须同时试 curl_cffi 与普通 requests，任一成功即可用——不同图床的拦截策略正好相反：
      · static.wikia.nocookie.net / cdn.fabtcg.com：curl_cffi 能过，普通 curl 403
      · archives.bulbagarden.net：普通 requests 能过，curl_cffi 反而 403
    只试一种会把另一类的好链接批量误判成失效。
    """
    last = (0, "")
    clients = []
    try:
        from curl_cffi import requests as cr
        clients.append(("cffi", lambda: (cr.get(url, impersonate="chrome", timeout=25,
                                                allow_redirects=True).status_code,
                                         cr.get(url, impersonate="chrome", timeout=25,
                                                allow_redirects=True)
                                         .headers.get("content-type", ""))))
    except ImportError:
        pass
    try:
        import requests as rq
        clients.append(("requests", lambda: (lambda r: (r.status_code,
                                                        r.headers.get("content-type", "")))(
            rq.get(url, timeout=25, allow_redirects=True,
                   headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}))))
    except ImportError:
        pass

    for _ in range(2):
        for _, fn in clients:
            try:
                code, ctype = fn()
                code, ctype = int(code), (ctype or "").strip()
                if code == 200:
                    return code, ctype
                last = (code, ctype)
            except Exception:
                pass
    if last[0]:
        return last
    try:
        r = subprocess.run(["curl", "-s", "-o", os.devnull, "-w", "%{http_code} %{content_type}",
                            "--max-time", "25",
                            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", url],
                           capture_output=True, text=True, timeout=32)
        code, _, ctype = (r.stdout or "0 ").partition(" ")
        return int(code.strip() or 0), ctype.strip()
    except Exception:
        return 0, ""


def toks(s: str) -> set[str]:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    out = set()
    for t in re.findall(r"[a-z0-9]+", s.lower()):
        if t in STOP or len(t) < 3:
            continue
        out.add(t[:-1] if t.endswith("s") and len(t) > 4 else t)
    return out


def score_url(set_name: str, url: str) -> int:
    """给候选 URL 打分，用于同名冲突时择优。

    关键规则（都是踩过的坑）：
      · 数字必须一致——Neo Premium File 2 不能配 Premium_File_1_back
      · 文件名多出系列名里没有的词要扣分——'SI: Start Deck 100' 不该配
        'Start_Deck_100_Battle_Collection'（那是另一个系列）
    """
    from urllib.parse import unquote
    fn = unquote(url.split("/")[-1].rsplit(".", 1)[0])
    nt, nf = toks(set_name), toks(fn)
    num_t = {t for t in nt if t.isdigit() or t in ROMAN}
    num_f = {t for t in nf if t.isdigit() or t in ROMAN}
    s = 2 * len(nt & nf)
    if num_t != num_f:
        s -= 10
    s -= 2 * len(nf - nt)          # 文件名里多出来的词
    if norm(set_name) and norm(set_name) in norm(fn):
        s += 3
    return s


def main() -> None:
    rows = json.load(open(os.path.join(OUT, "series_all_names.json"), encoding="utf-8"))
    gaps = {line: {r["setName"] for r in rs if not r["logo"]}
            for line, rs in json.load(open(os.path.join(OUT, "series_logo_rows.json"),
                                           encoding="utf-8")).items()}
    all_gaps = {n for s in gaps.values() for n in s}
    # 归属校验用「品线全量系列名单」而非「当前待补清单」——否则补过一轮重建后，
    # 已补上的条目会被误判成"不在待补清单里"
    lines_of: dict[str, list[str]] = {}
    for line, names in rows.items():
        for n in names:
            lines_of.setdefault(n, []).append(line)
    ambiguous = {n for n, ls in lines_of.items() if len(ls) > 1}
    known = set(lines_of)
    # 真正会出问题的是「在多个品线里都还没 logo」的同名系列——builder 按名兜底会同时套到两行；
    # 只在一个品线缺的（另一个品线已有 logo）不会串，靠优先级自然处理
    gap_lines: dict[str, list[str]] = {}
    for line, s in gaps.items():
        for n in s:
            gap_lines.setdefault(n, []).append(line)
    ambiguous = {n for n, ls in gap_lines.items() if len(ls) > 1}
    if ambiguous:
        print(f"注意：{len(ambiguous)} 个系列名在多个品线里都缺 logo，将拒绝其归属不明的产出："
              f"{'、'.join(sorted(ambiguous))}")

    files = [f for f in sorted(glob.glob(os.path.join(OUT, "gapfix_*.json")))
             if os.path.basename(f) not in ("gapfix_merged.json", "gapfix_rejected.json")]
    print(f"发现 {len(files)} 个 gapfix 文件")
    entries, rejected = [], []
    for f in files:
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print(f"  !! {os.path.basename(f)} 解析失败：{e}")
            continue
        if not isinstance(data, list):
            print(f"  !! {os.path.basename(f)} 不是数组（{type(data).__name__}），跳过")
            continue
        not_found = []
        for e in data:
            e["_file"] = os.path.basename(f)
            if not e.get("setName"):
                rejected.append({**e, "_why": "没有 setName，无法归属"})
            elif not e.get("logo"):
                # agent 明确记录的「拿不到」条目，不是错误
                not_found.append(e)
            elif e["setName"] not in known:
                rejected.append({**e, "_why": "setName 不属于这 8 个品线的任何系列（拼错）"})
            elif e["setName"] in ambiguous:
                rejected.append({**e, "_why": f"同名跨品线（{'/'.join(lines_of[e['setName']])}），"
                                              "无法确定归属，需人工指定"})
            else:
                entries.append(e)
    print(f"候选 {len(entries)} 条；agent 自报拿不到 {len(not_found)} 条；"
          f"格式/归属被拒 {len(rejected)} 条")

    # 同名额冲突：按文件名与系列名的吻合度打分择优，而不是"先到先得"
    # （agent 的最终版会把 Neo Premium File 2/3 都写成 Premium_File_1_back，
    #   单纯取先到的就会把好的一条丢掉）
    by_name: dict[str, dict] = {}
    conflicts = []
    for e in entries:
        n = e["setName"]
        if n not in by_name:
            by_name[n] = e
            continue
        old = by_name[n]
        if old["logo"] == e["logo"]:
            continue
        so, sn = score_url(n, old["logo"]), score_url(n, e["logo"])
        conflicts.append((n, old["logo"], e["logo"], so, sn, old["_file"], e["_file"]))
        if sn > so:
            by_name[n] = e
    if conflicts:
        print(f"⚠️  {len(conflicts)} 条同名不同 URL，按吻合度择优：")
        for n, uo, un, so, sn, fo, fn_ in conflicts:
            win = "新" if sn > so else ("旧" if so > sn else "旧(平手)")
            print(f"   {n[:40]:40s} 留{win} 旧({so:+d}) {uo.split('/')[-1][:34]:34s} "
                  f"[{fo[:18]}] | 新({sn:+d}) {un.split('/')[-1][:34]:34s} [{fn_[:18]}]")

    # 逐个校验 URL
    print(f"校验 {len(by_name)} 个 URL…")
    names = sorted(by_name)
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(lambda n: check(by_name[n]["logo"]), names))
    ok, bad = {}, []
    for n, (code, ctype) in zip(names, res):
        if code == 200 and ctype.startswith(OK_TYPES):
            e = by_name[n]
            ok[n] = {"logo": e["logo"], "source": e.get("source") or "gapfix",
                     "evidence": e.get("evidence") or ""}
        else:
            bad.append({**by_name[n], "_why": f"URL 不可用 http={code} type={ctype}"})
    rejected += bad

    with open(os.path.join(OUT, "gapfix_merged.json"), "w", encoding="utf-8") as f:
        json.dump(ok, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "gapfix_rejected.json"), "w", encoding="utf-8") as f:
        json.dump(rejected, f, ensure_ascii=False, indent=1)

    print(f"\n可用 {len(ok)} 条，被拒 {len(rejected)} 条")
    src = Counter(v["source"] for v in ok.values())
    print("来源分布:", dict(src.most_common()))
    gap_total = len(all_gaps)
    print(f"待补总量 {gap_total}，本次补齐 {len(ok)} "
          f"→ 补齐后剩余 {gap_total - len(ok)}")
    if rejected:
        print("\n被拒明细（前 15）：")
        for r in rejected[:15]:
            print(f"  {r.get('setName', '?')[:40]:40s} {r.get('_why')}")


if __name__ == "__main__":
    main()