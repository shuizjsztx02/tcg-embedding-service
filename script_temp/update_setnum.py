#!/usr/bin/env python3
"""给 tcgplayer_sets_rarities_all.json 的每个系列补 setNum（从卡片数据统计）。

setNum 口径：category_cards_final/category_cards/<品类>/products.jsonl 中
             setName 命中该系列的**单卡条数**（每条 = 一个 TCGPlayer 单卡商品，productId 唯一）。
             卡片数据里找不到对应系列时写 null，并在报告里列出。

用法：
  python update_setnum.py            # dry-run，只打印报告
  python update_setnum.py --write    # 实际写回 json
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(BASE, "category_cards_final", "category_cards")
RAR = os.path.join(BASE, "tcgplayer_sets_rarities_all.json")

# json 里的 productLineName -> 卡片数据目录（game 7 的 Dragon Ball Super: Masters 无对应目录）
PL_TO_DIR = {
    "Pokémon": "03_Pokemon",
    "Pokémon Japan": "85_Pokemon_Japan",
    "Magic: The Gathering": "01_Magic",
    "Yu-Gi-Oh!": "02_YuGiOh",
    "One Piece Card Game": "68_One_Piece_Card_Game",
    "Disney Lorcana": "71_Disney_Lorcana",
    "Flesh and Blood TCG": "62_Flesh_and_Blood_TCG",
    "Dragon Ball Super: Masters": None,
}

STOP = {"the", "of", "a", "and"}
ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"}


def norm(s: str) -> str:
    s = (s or "").lower().replace("&", "and").replace("’", "'")
    return re.sub(r"[^a-z0-9]", "", s)


def strip_code_prefix(name: str) -> str:
    m = re.match(r"^([A-Za-z]{2,6}[0-9]{0,3})\s*[:\-–]\s*(.+)$", name)
    if m:
        return m.group(2)
    m = re.match(r"^(EX|SM|XY|BW|DP|HGSS|SV|SWSH|ME|MEE|POP|EB|OP|ST)\s+(.+)$", name)
    if m:
        return m.group(2)
    return name


def tokens(name: str) -> list[str]:
    s = (name or "").lower().replace("&", " and ").replace("’", "'")
    out = []
    for t in re.findall(r"[a-z0-9]+", s):
        if t in STOP:
            continue
        if t.endswith("s") and len(t) > 3 and not t.endswith("ss"):
            t = t[:-1]
        out.append(t)
    return out


def numeric_sig(toks: list[str]) -> Counter:
    return Counter(t for t in toks if t.isdigit() or t in ROMAN)


# 人工核对：json 系列名 -> 卡片数据里的 setName
OVERRIDES: dict[tuple[str, str], str] = {
    ("Pokémon", "Base Set"): "Base Set",
    ("Pokémon", "Crystal Guardians"): "EX Crystal Guardians",
    ("Pokémon", "Delta Species"): "EX Delta Species",
    ("Pokémon", "Deoxys"): "EX Deoxys",
    ("Pokémon", "Dragon"): "EX Dragon",
    ("Pokémon", "Dragon Frontiers"): "EX Dragon Frontiers",
    ("Pokémon", "Emerald"): "EX Emerald",
    ("Pokémon", "Hidden Legends"): "EX Hidden Legends",
    ("Pokémon", "Holon Phantoms"): "EX Holon Phantoms",
    ("Pokémon", "Legend Maker"): "EX Legend Maker",
    ("Pokémon", "Power Keepers"): "EX Power Keepers",
    ("Pokémon", "Ruby and Sapphire"): "EX Ruby and Sapphire",
    ("Pokémon", "Sandstorm"): "EX Sandstorm",
    ("Pokémon", "FireRed & LeafGreen"): None,
    ("Pokémon", "Diamond and Pearl Promos"): "Diamond and Pearl Promos",
    ("Pokémon Japan", "M6: Storm Emeralda"): "M6: Storm Emeralda",
}


def load_cards(dirname: str) -> Counter:
    p = os.path.join(CARDS, dirname, "products.jsonl")
    cnt: Counter = Counter()
    if not os.path.isfile(p):
        return cnt
    with open(p, encoding="utf-8") as f:
        for line in f:
            try:
                cnt[json.loads(line).get("setName") or ""] += 1
            except Exception:
                continue
    return cnt


def build_card_index(cnt: Counter) -> dict:
    n_idx: dict[str, str] = {}
    t_idx: dict[tuple, list[str]] = {}
    for sn in cnt:
        for form in (sn, strip_code_prefix(sn)):
            n_idx.setdefault(norm(form), sn)
        key = tuple(sorted(tokens(sn)))
        t_idx.setdefault(key, []).append(sn)
        sp = strip_code_prefix(sn)
        if sp != sn:
            t_idx.setdefault(tuple(sorted(tokens(sp))), []).append(sn)
    return {"norm": n_idx, "token": t_idx}


def match_one(name: str, cnt: Counter, idx: dict):
    for f in (name, strip_code_prefix(name)):
        hit = idx["norm"].get(norm(f))
        if hit:
            return hit, "exact" if f == name else "prefix"
    tk = tokens(strip_code_prefix(name))
    cands = idx["token"].get(tuple(sorted(tk)))
    if cands:
        ok = [c for c in cands if numeric_sig(tokens(c)) == numeric_sig(tk)]
        if ok:
            return sorted(ok, key=len)[0], "token"
    return None, ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="实际写回 json（默认 dry-run）")
    args = ap.parse_args()

    data = json.load(open(RAR, encoding="utf-8"))
    cache: dict[str, tuple[Counter, dict]] = {}
    report = []
    new_data = []
    for pl in data:
        plname = pl["productLineName"]
        dirname = PL_TO_DIR.get(plname)
        if dirname:
            if dirname not in cache:
                c = load_cards(dirname)
                cache[dirname] = (c, build_card_index(c))
            cnt, idx = cache[dirname]
        else:
            cnt, idx = Counter(), {"norm": {}, "token": {}}

        sets = []
        miss = []
        for s in pl["setList"]:
            sn = s["setName"]
            card_name = method = None
            if (plname, sn) in OVERRIDES:
                ov = OVERRIDES[(plname, sn)]
                if ov and ov in cnt:
                    card_name, method = ov, "override"
            elif dirname:
                card_name, method = match_one(sn, cnt, idx)
            n = cnt.get(card_name, 0) if card_name else None
            if card_name is None and dirname:
                miss.append(sn)
            sets.append({"setName": sn, "setNum": n, "rarityList": s["rarityList"],
                         "_cardSetName": card_name, "_match": method})
        report.append((plname, dirname, len(sets), miss))
        new_data.append({"productLineName": plname, "allRarityList": pl["allRarityList"],
                         "_sets": sets})

    # 报告
    for plname, dirname, tot, miss in report:
        print(f"\n=== {plname} -> {dirname}  共 {tot} 个系列，未统计到 {len(miss)} 个")
        if miss:
            print("    " + " | ".join(miss[:40]) + (" ..." if len(miss) > 40 else ""))

    if args.write:
        out = []
        for pl, src in zip(new_data, data):
            out.append({
                "productLineName": pl["productLineName"],
                "allRarityList": pl["allRarityList"],
                "setList": [{"setName": s["setName"], "setNum": s["setNum"],
                             "rarityList": s["rarityList"]} for s in pl["_sets"]],
            })
        with open(RAR, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\n已写入 {RAR}")
    else:
        print("\n(dry-run，未写文件；加 --write 生效)")


if __name__ == "__main__":
    main()