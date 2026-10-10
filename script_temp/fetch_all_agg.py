#!/usr/bin/env python3
"""抓取全部 47 个品类的 TCGPlayer setName 聚合，量出「线上权威系列名录」与本地卡片数据的缺口。

两步走：先用 productLineName 单条件查出该品线可用的 productTypeName，
再用「品线 + 单卡类型」查出 setName 分布。

结果写 script_temp/out/all_agg.json。
"""
from __future__ import annotations

import json
import os
import subprocess
import time

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
URL = "https://mp-search-api.tcgplayer.com/v1/search/request"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# productLineName（接口值） -> 本地品类目录
LINES = {
    "Magic: The Gathering": "01_Magic",
    "YuGiOh": "02_YuGiOh",
    "Pokemon": "03_Pokemon",
    "Heroclix": "08_Heroclix",
    "WoW": "13_WoW",
    "Cardfight Vanguard": "16_Cardfight_Vanguard",
    "Force of Will": "17_Force_of_Will",
    "Dice Masters": "18_Dice_Masters",
    "Future Card BuddyFight": "19_Future_Card_BuddyFight",
    "Weiss Schwarz": "20_Weiss_Schwarz",
    "Dragon Ball Z TCG": "23_Dragon_Ball_Z_TCG",
    "Dragoborne": "28_Dragoborne",
    "MetaX TCG": "30_MetaX_TCG",
    "Zombie World Order TCG": "36_Zombie_World_Order_TCG",
    "The Caster Chronicles": "37_The_Caster_Chronicles",
    "Exodus TCG": "47_Exodus_TCG",
    "Lightseekers TCG": "48_Lightseekers_TCG",
    "Munchkin CCG": "53_Munchkin_CCG",
    "Warhammer Age of Sigmar Champions TCG": "54_Warhammer_Age_of_Sigmar_Champions_TCG",
    "Transformers TCG": "57_Transformers_TCG",
    "Bakugan TCG": "58_Bakugan_TCG",
    "Chrono Clash System": "60_Chrono_Clash_System",
    "Argent Saga TCG": "61_Argent_Saga_TCG",
    "Flesh and Blood TCG": "62_Flesh_and_Blood_TCG",
    "Digimon Card Game": "63_Digimon_Card_Game",
    "Gate Ruler": "65_Gate_Ruler",
    "MetaZoo": "66_MetaZoo",
    "WIXOSS": "67_WIXOSS",
    "One Piece Card Game": "68_One_Piece_Card_Game",
    "Disney Lorcana": "71_Disney_Lorcana",
    "Battle Spirits Saga": "72_Battle_Spirits_Saga",
    "Shadowverse: Evolve": "73_Shadowverse_Evolve",
    "Grand Archive TCG": "74_Grand_Archive_TCG",
    "Akora TCG": "75_Akora_TCG",
    "Kryptik TCG": "76_Kryptik_TCG",
    "Sorcery: Contested Realm": "77_Sorcery_Contested_Realm",
    "Alpha Clash": "78_Alpha_Clash",
    "Star Wars: Unlimited": "79_Star_Wars_Unlimited",
    "Dragon Ball Super: Fusion World": "80_Dragon_Ball_Super_Fusion_World",
    "Union Arena": "81_Union_Arena",
    "Elestrals": "83_Elestrals",
    "Pokemon Japan": "85_Pokemon_Japan",
    "Gundam Card Game": "86_Gundam_Card_Game",
    "hololive OFFICIAL CARD GAME": "87_hololive_OFFICIAL_CARD_GAME",
    "Godzilla Card Game": "88_Godzilla_Card_Game",
    "Riftbound: League of Legends Trading Card Game": "89_Riftbound_League_of_Legends_Trading_Card_Game",
    "CookieRun: Braverse TCG": "90_CookieRun_Braverse_TCG",
    # 额外：本地没有目录但 json 里有的品线
    "Dragon Ball Super: Masters": None,
}


def call(match: dict):
    body = {"filters": {"match": match}, "mpfev": 5489, "from": 0, "size": 1}
    for _ in range(3):
        try:
            r = subprocess.run(
                ["curl", "-s", "--max-time", "30", "-X", "POST", URL,
                 "-H", "Content-Type: application/json", "-H", f"User-Agent: {UA}",
                 "-H", "Origin: https://www.tcgplayer.com",
                 "-H", "Referer: https://www.tcgplayer.com/",
                 "-d", json.dumps(body)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=40)
            if r.returncode == 0 and r.stdout.strip():
                d = json.loads(r.stdout)
                if d.get("results"):
                    return d["results"][0]
        except Exception:
            pass
        time.sleep(1.0)
    return None


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    out = {}
    for line, dirname in LINES.items():
        r = call({"productLineName": [line]})
        if not r:
            print(f"{line:46s} FAILED", flush=True)
            continue
        types = {x["value"]: int(x["count"]) for x in r["aggregations"]["productTypeName"]}
        pick = None
        for t in types:
            if t == "Cards":
                pick = t
                break
        if not pick:
            for t in types:
                if "Single" in t:
                    pick = t
                    break
        if not pick and types:
            pick = max(types, key=lambda k: types[k])
        r2 = call({"productLineName": [line], "productTypeName": [pick]}) if pick else None
        sets = {}
        if r2:
            sets = {x["value"]: int(x["count"]) for x in r2["aggregations"]["setName"]}
        out[line] = {"dir": dirname, "productTypeName": pick, "cardTypes": types,
                     "setCount": len(sets), "cardTotal": sum(sets.values()), "sets": sets}
        print(f"{line:46s} type={pick} 系列={len(sets):4d} 单卡={sum(sets.values()):7d}",
              flush=True)
        time.sleep(0.8)

    with open(os.path.join(OUT, "all_agg.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n已写 {os.path.join(OUT, 'all_agg.json')}")


if __name__ == "__main__":
    main()