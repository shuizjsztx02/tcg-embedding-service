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
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
OK_TYPES = ("image/", "text/xml", "application/xml", "binary/octet-stream")


def check(url: str) -> tuple[int, str]:
    for _ in range(2):
        try:
            r = subprocess.run(
                ["curl", "-s", "-o", os.devnull, "-w", "%{http_code} %{content_type}",
                 "--max-time", "25", url],
                capture_output=True, text=True, timeout=32)
            code, _, ctype = (r.stdout or "0 ").partition(" ")
            code = int(code.strip() or 0)
            if code:
                return code, ctype.strip()
        except Exception:
            pass
    return 0, ""


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
        for e in data:
            e["_file"] = os.path.basename(f)
            if not e.get("setName") or not e.get("logo"):
                rejected.append({**e, "_why": "缺 setName 或 logo"})
            elif e["setName"] not in known:
                rejected.append({**e, "_why": "setName 不属于这 8 个品线的任何系列（拼错）"})
            elif e["setName"] in ambiguous:
                rejected.append({**e, "_why": f"同名跨品线（{'/'.join(lines_of[e['setName']])}），"
                                              "无法确定归属，需人工指定"})
            else:
                entries.append(e)
    print(f"候选 {len(entries)} 条，格式/归属被拒 {len(rejected)} 条")

    # 同名额冲突
    by_name: dict[str, dict] = {}
    conflicts = []
    for e in entries:
        n = e["setName"]
        if n in by_name:
            if by_name[n]["logo"] != e["logo"]:
                conflicts.append((n, by_name[n]["logo"], e["logo"], by_name[n]["_file"], e["_file"]))
            continue
        by_name[n] = e
    if conflicts:
        print(f"⚠️  {len(conflicts)} 条同名不同 URL 的冲突，保留先到的：")
        for c in conflicts[:10]:
            print(f"   {c[0][:44]:44s} 留 {c[1][:60]}（{c[3]}） 弃 {c[2][:60]}（{c[4]}）")

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