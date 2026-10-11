#!/usr/bin/env python3
"""重新取回宝可梦日文的「系列符号」（SetSymbol）图片。

子 agent 一度把 10 个系列符号单列在 gapfix_pkmjp_setsymbols.json，后来又把它清空了。
这些是印在卡面上的系列标记，比包装图更贴切，重新按名匹配取回。

做法：枚举 archives 上所有 `SetSymbol` 开头的文件，再按系列名择优匹配。
"""
from __future__ import annotations

import json
import os
import re
import time
import unicodedata

import requests

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
ARCH = "https://archives.bulbagarden.net/w/api.php"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 需要补的系列（来自子 agent 的报告）
TARGETS = [
    "10th Movie Commemoration Set",
    "11th Movie Commemoration Set",
    "Arceus LV.X Deck: Grass & Fire",
    "Arceus LV.X Deck: Lightning & Psychic",
    "Movie Commemoration Random Pack",
    "PokePark Blue",
    "PokePark Forest",
    "Team Plasma's Powered Half Deck",
    "sH: Sword & Shield Family Pokemon Card Game",
    "sN: Start Deck 100 CoroCoro Comic Version",
]
STOP = {"the", "of", "a", "and", "set", "deck", "pack", "box", "cards", "card"}


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
        out.add(t[:-1] if t.endswith("s") and len(t) > 4 else t)
    return out


def all_setsymbols() -> list[dict]:
    out, cont = [], {}
    for _ in range(10):
        p = {"action": "query", "list": "allimages", "aiprefix": "SetSymbol",
             "ailimit": 500, "format": "json"}
        p.update(cont)
        d = requests.get(ARCH, params=p, timeout=30, headers=H).json()
        out += d.get("query", {}).get("allimages", [])
        cont = d.get("continue") or {}
        if not cont:
            break
        time.sleep(0.3)
    return out


def main() -> None:
    files = all_setsymbols()
    print(f"archives 上 SetSymbol* 文件 {len(files)} 个")

    rows = []
    for name in TARGETS:
        nt = toks(name)
        best, best_score = None, 0
        for f in files:
            fn = f["name"]
            base = re.sub(r"\.(png|jpg|jpeg|webp)$", "", fn, flags=re.I)
            if not base.lower().startswith("setsymbol"):
                continue
            body = base[len("SetSymbol"):]
            nf = toks(body)
            # 系列名的每个词都要出现在文件名里，多出来的词要少
            if nt and not nt.issubset(nf):
                continue
            score = 3 * len(nt) - len(nf - nt)
            if score > best_score:
                best, best_score = f["url"], score
        rows.append({"setName": name, "logo": best, "source": "bulbapedia-setsymbol",
                     "evidence": f"Bulbapedia 系列符号文件 {best.split('/')[-1]}"
                                 if best else "未找到对应系列符号"})
        print(f"  {'OK ' if best else 'MISS'} {name[:44]:44s} -> "
              f"{best.split('/')[-1] if best else '-'}")

    rows = [r for r in rows if r["logo"]]
    with open(os.path.join(OUT, "gapfix_pkmjp_setsymbols.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(f"写入 {len(rows)} 条")


if __name__ == "__main__":
    main()