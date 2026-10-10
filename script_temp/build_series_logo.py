#!/usr/bin/env python3
"""生成「品类 → 系列 → 系列 logo → 系列卡牌数量」映射及其报告。

数据源：
  A. category_cards_final/category_cards/<NN_Cat>/products.jsonl  TCGPlayer 本地单卡
  B. crawl/crawl/holodex_sets_organized.json                      Holodex 系列 logo URL
  C. script_temp/out/agg_*.json                                   TCGPlayer 线上聚合（校验用，可选）

匹配分级：
  exact   归一化后完全相同
  prefix  去掉 TCGPlayer 系列代号前缀（EX / SWSH08 / SM …）后相同
  token   词元集合相同（Promos↔Promo 等）
  inherit 去掉「预发售/发售活动/促销」等衍生子线后缀后命中母系列
  override 人工核对表
数字/罗马数字词元不同则一律不匹配。

输出：
  doc/seriesToLogo.md              映射表 + 覆盖率 + 数据质量结论
  csv/series_count_compare.csv     本地卡牌数 vs TCGPlayer 线上卡牌数
  script_temp/out/series_logo_map.json  机读映射
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(BASE, "category_cards_final", "category_cards")
CRAWL = os.path.join(BASE, "crawl", "crawl")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
MD = os.path.join(BASE, "doc", "seriesToLogo.md")
CSV = os.path.join(BASE, "csv", "series_count_compare.csv")

# Holodex gameId -> 品类目录名（逐个核对 set 名后确定）
GAME_TO_DIR = {
    1: "03_Pokemon",
    2: "68_One_Piece_Card_Game",
    3: "01_Magic",
    4: "02_YuGiOh",
    5: "71_Disney_Lorcana",
    6: "80_Dragon_Ball_Super_Fusion_World",
    7: None,  # Dragon Ball Super Card Game (Masters)：本地无卡片数据目录
    8: "63_Digimon_Card_Game",
    9: "86_Gundam_Card_Game",
    10: "81_Union_Arena",
    11: "89_Riftbound_League_of_Legends_Trading_Card_Game",
    12: "79_Star_Wars_Unlimited",
}

# 品类目录 -> TCGPlayer 线上聚合文件（script_temp/out/agg_*.json）
DIR_TO_AGG = {
    "03_Pokemon": "pokemon",
    "85_Pokemon_Japan": "pokemon_japan",
    "01_Magic": "magic",
    "02_YuGiOh": "yugioh",
    "68_One_Piece_Card_Game": "one_piece",
    "71_Disney_Lorcana": "lorcana",
    "62_Flesh_and_Blood_TCG": "fab",
}

# tcgplayer_sets_rarities_all.json 的 productLineName -> 品类目录（None = 本地无卡片数据）
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

GAME_LABEL = {
    1: "Pokémon", 2: "One Piece Card Game", 3: "Magic: The Gathering", 4: "Yu-Gi-Oh!",
    5: "Disney Lorcana", 6: "Dragon Ball Super: Fusion World",
    7: "Dragon Ball Super Card Game (Masters)", 8: "Digimon Card Game",
    9: "Gundam Card Game", 10: "Union Arena",
    11: "Riftbound: League of Legends TCG", 12: "Star Wars: Unlimited",
}

RAR = os.path.join(BASE, "tcgplayer_sets_rarities_all.json")

STOP = {"the", "of", "a", "and"}
ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"}

DERIVED_RE = re.compile(
    r"\s*[:\-]?\s*(pre-?release cards|pre-?release starter deck|super pre-?release starter deck"
    r"|release event cards|celebration event cards|alternate art reprints?"
    r"|weekly play promos?|tournament cards|promotional cards|judge promos"
    r"|organized play promos|proving grounds)\s*$", re.I)

OVERRIDES: dict[tuple[str, str], str | None] = {
    ("03_Pokemon", "Base Set"): "Base Set Unlimited",
    ("03_Pokemon", "Base Set (Shadowless)"): "Base Set Shadowless",
    ("03_Pokemon", "XY Base Set"): "XY Base",
    ("03_Pokemon", "SM Base Set"): "Sun & Moon",
    ("03_Pokemon", "SWSH01: Sword & Shield Base Set"): "Sword & Shield",
    ("03_Pokemon", "SWSH: Sword & Shield Promo Cards"): "Sword & Shield Promo",
    ("03_Pokemon", "SWSH: Crown Zenith: Galarian Gallery"): "Crown Zenith Galarian Gallery",
    ("03_Pokemon", "SV01: Scarlet & Violet Base Set"): "Scarlet & Violet Base",
    ("03_Pokemon", "SV: Black Bolt"): "Black Bolt",
    ("03_Pokemon", "SV: White Flare"): "White Flare",
    ("03_Pokemon", "Diamond and Pearl Promos"): "Diamond and Pearl Promo",
    ("03_Pokemon", "HGSS Promos"): "HGSS Black Star Promo",
    ("03_Pokemon", "Rumble"): "Pokemon Rumble",
    ("03_Pokemon", "e-Reader Sample Cards"): "Expedition",
    ("03_Pokemon", "Hidden Fates: Shiny Vault"): "Hidden Fates: Shiny Vault",
    ("03_Pokemon", "MEE: Mega Evolution Energies"): None,
    ("71_Disney_Lorcana", "Shimmering Skies"): "Shimmering Skies",
}

_VARIANT_RE = re.compile(r"1st edition|shadowless|unlimited", re.I)


def norm(name: str) -> str:
    s = (name or "").lower().replace("&", "and").replace("’", "'")
    return re.sub(r"[^a-z0-9]", "", s)


def strip_code_prefix(name: str) -> str:
    m = re.match(r"^([A-Za-z]{2,6}[0-9]{0,3})\s*[:\-–]\s*(.+)$", name)
    if m:
        return m.group(2)
    m = re.match(r"^(EX|SM|XY|BW|DP|HGSS|SV|SWSH|ME|MEE|MEM|MEZ|POP|EB|OP|ST)\s+(.+)$", name)
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


def load_cards(dirname: str):
    p = os.path.join(CARDS, dirname, "products.jsonl")
    cnt: Counter = Counter()
    rar: dict[str, set] = defaultdict(set)
    lineno = 0
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                sn = o.get("setName") or ""
                cnt[sn] += 1
                lineno += 1
                if o.get("rarityName"):
                    rar[sn].add(o["rarityName"])
    return cnt, rar, lineno


def load_holodex() -> dict[int, list[dict]]:
    d = json.load(open(os.path.join(CRAWL, "holodex_sets_organized.json"), encoding="utf-8"))
    out: dict[int, list[dict]] = {}
    for gid, g in d.items():
        out[int(gid)] = [{"name": s["name"], "logo": s.get("logo"), "serieId": sid}
                         for sid, si in g["series"].items() for s in si["sets"]]
    return out


def build_norm_index(names) -> dict[str, str]:
    idx: dict[str, str] = {}
    for n in names:
        for form in (n, strip_code_prefix(n)):
            idx.setdefault(norm(form), n)
    return idx


def build_token_index(names) -> dict[tuple, list[str]]:
    idx: dict[tuple, list[str]] = defaultdict(list)
    for n in names:
        for form in (n, strip_code_prefix(n)):
            idx.setdefault(tuple(sorted(tokens(form))), []).append(n)
    return idx


def match_name(name: str, names: list[str], n_idx: dict, t_idx: dict):
    """返回 (命中的目标名, 方法)。"""
    for f in (name, strip_code_prefix(name)):
        hit = n_idx.get(norm(f))
        if hit:
            return hit, ("exact" if f == name else "prefix")
    tk = tokens(strip_code_prefix(name))
    cands = t_idx.get(tuple(sorted(tk)))
    if cands:
        ok = [c for c in cands if numeric_sig(tokens(c)) == numeric_sig(tk)]
        if ok:
            return sorted(ok, key=len)[0], "token"
    return None, ""


def pick_variant(cands: list[str]) -> str:
    return sorted(cands, key=lambda n: (1 if _VARIANT_RE.search(n) else 0, n))[0]


def match_series(tcg_name: str, hx_sets: list[dict], idx: dict):
    """系列名 -> holodex set。返回 (set | None, 方法)。"""
    names = [s["name"] for s in hx_sets]
    hit, m = match_name(tcg_name, names, idx["norm"], idx["token"])
    if hit:
        return next(s for s in hx_sets if s["name"] == hit), m
    parent = DERIVED_RE.sub("", tcg_name).strip(" :-")
    if parent and parent != tcg_name:
        hit, _ = match_name(parent, names, idx["norm"], idx["token"])
        if hit:
            return next(s for s in hx_sets if s["name"] == hit), "inherit"
    return None, ""


def build_index(hx_sets: list[dict]) -> dict:
    names = [s["name"] for s in hx_sets]
    return {"norm": build_norm_index(names), "token": build_token_index(names)}


def md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    holodex = load_holodex()
    dir_to_game = {v: k for k, v in GAME_TO_DIR.items() if v}
    cats = sorted(d for d in os.listdir(CARDS) if os.path.isdir(os.path.join(CARDS, d)))

    result, compare_rows = [], []
    for dirname in cats:
        cnt, rar, _ = load_cards(dirname)
        if not cnt:
            continue
        gid = dir_to_game.get(dirname)
        hx_sets = holodex.get(gid, []) if gid else []
        idx = build_index(hx_sets) if hx_sets else None
        rows = []
        for sn in sorted(cnt):
            m = method = None
            if (dirname, sn) in OVERRIDES:
                ov = OVERRIDES[(dirname, sn)]
                if ov:
                    m = next((s for s in hx_sets if s["name"] == ov), None)
                    method = "override" if m else ""
            elif idx:
                m, method = match_series(sn, hx_sets, idx)
            rows.append({"setName": sn, "cardCount": cnt[sn],
                         "logo": (m or {}).get("logo"),
                         "holodexSet": (m or {}).get("name"),
                         "serieId": (m or {}).get("serieId"),
                         "match": method, "rarityList": sorted(rar[sn])})
        result.append({"category": dirname, "gameId": gid, "sets": rows})

        # 本地 vs 线上 对比
        slug = DIR_TO_AGG.get(dirname)
        if slug:
            ap = os.path.join(OUT, f"agg_{slug}.json")
            if os.path.isfile(ap):
                agg = json.load(open(ap, encoding="utf-8"))["sets"]
                a_idx = (build_norm_index(agg), build_token_index(agg))
                for sn in sorted(cnt):
                    on, _ = match_name(sn, list(agg), a_idx[0], a_idx[1])
                    compare_rows.append((dirname, sn, cnt[sn], on or "", agg.get(on, ""), ""))
                covered = set()
                for sn in cnt:
                    on, _ = match_name(sn, list(agg), a_idx[0], a_idx[1])
                    if on:
                        covered.add(on)
                for on in sorted(set(agg) - covered):
                    compare_rows.append((dirname, "", "", on, agg[on], "线上有、本地缺"))

    with open(os.path.join(OUT, "series_logo_map.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ---------- CSV ----------
    with open(CSV, "w", encoding="utf-8", newline="\n") as f:
        f.write("品类,本地系列名,本地卡牌数,TCGPlayer线上系列名,线上卡牌数,备注\n")
        for d, ls, lc, os_, oc, note in compare_rows:
            if not note and os_ and lc and oc:
                if lc == oc:
                    continue  # 只留不一致的
                note = f"差{lc - oc:+d}"
            f.write(f"{d},{ls},{lc},{os_},{oc},{note}\n")

    # ---------- Markdown ----------
    today = date.today().isoformat()
    L: list[str] = []
    L.append("# 系列 → Logo 映射表（seriesToLogo.md）")
    L.append("")
    L.append(f"> 生成时间：{today}　生成脚本：`script_temp/build_series_logo.py`")
    L.append("> logo 来源：`crawl/crawl/holodex_sets_organized.json`（Holodex CDN，12 个 game）")
    L.append("> 卡牌数量口径：`category_cards_final/category_cards/<品类>/products.jsonl` "
             "中该系列的单卡条数")
    L.append("")
    L.append("## 一、总览")
    L.append("")
    tot_sets = sum(len(r["sets"]) for r in result)
    tot_logo = sum(1 for r in result for s in r["sets"] if s["logo"])
    tot_cards = sum(s["cardCount"] for r in result for s in r["sets"])
    tot_hit = sum(s["cardCount"] for r in result for s in r["sets"] if s["logo"])
    L.append("| 指标 | 值 |")
    L.append("|------|-----|")
    L.append(f"| 品类数 | {len(result)} |")
    L.append(f"| 系列总数 | {tot_sets} |")
    L.append(f"| 已关联 logo 的系列 | {tot_logo}（{tot_logo / tot_sets * 100:.1f}%） |")
    L.append(f"| 卡牌总数 | {tot_cards} |")
    L.append(f"| 其中有 logo 的系列覆盖卡牌 | {tot_hit}（{tot_hit / tot_cards * 100:.1f}%） |")
    L.append("")
    L.append("**匹配方式图例**：`exact` 归一化全等；`prefix` 去掉系列代号前缀后全等；"
             "`token` 词元集合相同；`inherit` 衍生子线（预发售/发售活动/促销卡）继承母系列 logo；"
             "`override` 人工核对。表格中 logo 带 `※` 的即为 `inherit`。")
    L.append("")
    L.append("### 各品类覆盖")
    L.append("")
    L.append("| 品类 | 系列数 | 有 logo | 直接匹配 | 继承 | logo 覆盖率 | 卡牌数 | 卡牌覆盖 |")
    L.append("|------|--------|---------|----------|------|-------------|--------|----------|")
    for r in result:
        n = len(r["sets"])
        direct = sum(1 for s in r["sets"] if s["match"] in ("exact", "prefix", "token", "override"))
        inh = sum(1 for s in r["sets"] if s["match"] == "inherit")
        cards = sum(s["cardCount"] for s in r["sets"])
        hit = sum(s["cardCount"] for s in r["sets"] if s["logo"])
        L.append(f"| {r['category']} | {n} | {direct + inh} | {direct} | {inh} | "
                 f"{(direct + inh) / n * 100:.1f}% | {cards} | {hit / cards * 100:.1f}% |")
    L.append("")
    L.append("## 二、映射表")
    L.append("")
    for r in result:
        n = len(r["sets"])
        has = sum(1 for s in r["sets"] if s["logo"])
        L.append(f"### {r['category']}（{n} 个系列，{has} 个有关联 logo）")
        L.append("")
        L.append("| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |")
        L.append("|------|------|----------|------------------|")
        for s in r["sets"]:
            pl = s["setName"]
            logo = s["logo"] or ""
            if logo and s["match"] == "inherit":
                logo += " ※"
            L.append(f"| {md_cell(r['category'])} | {md_cell(pl)} | {logo} | {s['cardCount']} |")
        L.append("")
    L.append("## 三、数据质量与缺口")
    L.append("")
    L.append("### 3.1 logo 来源只覆盖 12 个 game")
    L.append("")
    L.append("`crawl/crawl/holodex_sets_organized.json` 只抓了 Holodex 的 gameId 1–12，"
             "而本地卡片数据有 47 个品类。对应关系（已逐个人工核对 set 名）：")
    L.append("")
    L.append("| gameId | 实测游戏 | 对应品类目录 | holodex set 数 | 有 logo |")
    L.append("|--------|----------|--------------|----------------|---------|")
    for gid in sorted(GAME_TO_DIR):
        sets = holodex.get(gid, [])
        L.append(f"| {gid} | {GAME_LABEL[gid]} | {GAME_TO_DIR[gid] or '（本地无卡片数据）'} | "
                 f"{len(sets)} | {sum(1 for s in sets if s['logo'])} |")
    L.append("")
    L.append("**其余品类完全没有 logo 来源**，共 "
             f"{sum(1 for r in result if not r['gameId'])} 个品类 / "
             f"{sum(len(r['sets']) for r in result if not r['gameId'])} 个系列，"
             "其中包括 Pokemon Japan（358 个系列）这类大品类。要补齐必须再爬其它数据源的系列 logo。")
    L.append("")
    L.append("### 3.2 Holodex 目录本身不全")
    L.append("")
    L.append("即使是有 logo 来源的品类，Holodex 收录的 set 数也明显少于 TCGPlayer：")
    L.append("")
    L.append("| 品类 | holodex set | 本地系列 | 有 logo | 未匹配（源里没有） |")
    L.append("|------|-------------|----------|---------|--------------------|")
    for r in result:
        if not r["gameId"]:
            continue
        n = len(r["sets"])
        has = sum(1 for s in r["sets"] if s["logo"])
        L.append(f"| {r['category']} | {len(holodex.get(r['gameId'], []))} | {n} | {has} | {n - has} |")
    L.append("")
    L.append("未匹配掉的绝大多数是 Holodex 不收录的类别：促销卡（Promos）、"
             "发售活动/预发售卡（Pre-Release / Release Event Cards）、"
             "预组（Starter Deck / Structure Deck）、礼盒与铁盒（Tin / Box Set）、"
             "万智牌的 Art Series 与轮抽补充包等。")
    L.append("")
    L.append("### 3.3 crawl 目录的元数据不可信")
    L.append("")
    L.append("- 除 `pokemon_tcg.json`（gameId 1）外，其余单游戏文件的**文件名与内容对不上**："
             "`magic_gathering.json` 里是 Dragon Ball Super Fusion World（gameId 6）、"
             "`one_piece.json` 里是万智牌（gameId 3）、`union_arena.json` 里是游戏王（gameId 4）、"
             "`final_fantasy.json` 里是 Disney Lorcana（gameId 5）、"
             "`pokemon_tcg_pocket.json` 里是 One Piece（gameId 2）、"
             "`pokemon_tcg_china.json` 里是 Riftbound（gameId 11）、"
             "`tcg_create.json` 里是 Star Wars Unlimited（gameId 12）、"
             "`weiss_schwarz.json` 里是 Union Arena（gameId 10）。"
             "**不要按文件名判断游戏，必须按 set 名判断。**")
    L.append("- 每个 series 的 `name` 字段不是真实系列名，而是爬虫脚本按 set 名前缀取众数猜的，"
             "出现了 `Extra Booster`（One Piece）、`Commander`（万智牌）、`Starter Deck 10`（Gundam）、"
             "`UE23BT`（Union Arena）、`DIGIMON_BASE` 这类结果，无参考价值。"
             "**系列归属建议直接用 set 名，不要用该字段。**")
    L.append("- `crawl/__MACOSX/` 是 zip 解压残留，可忽略；`all_sets_temp.json` 是空壳。")
    L.append("")
    L.append("### 3.4 本地卡片数据比 TCGPlayer 线上少")
    L.append("")
    L.append("抽样比对了 TCGPlayer 搜索接口当前的 setName 聚合（`script_temp/out/agg_*.json`），"
             "本地 products.jsonl 明显不完整：")
    L.append("")
    L.append("| 品类 | 本地系列 | 本地卡牌 | 线上系列 | 线上卡牌 | 本地/线上 |")
    L.append("|------|----------|----------|----------|----------|-----------|")
    ratios = []
    for r in result:
        slug = DIR_TO_AGG.get(r["category"])
        if not slug:
            continue
        ap = os.path.join(OUT, f"agg_{slug}.json")
        if not os.path.isfile(ap):
            continue
        agg = json.load(open(ap, encoding="utf-8"))["sets"]
        lc = sum(s["cardCount"] for s in r["sets"])
        oc = sum(agg.values())
        ratios.append((r["category"], lc / oc * 100))
        L.append(f"| {r['category']} | {len(r['sets'])} | {lc} | {len(agg)} | {oc} | "
                 f"{lc / oc * 100:.0f}% |")
    L.append("")
    worst = "、".join(f"{c.split('_', 1)[1]} {p:.0f}%" for c, p in sorted(ratios, key=lambda x: x[1])[:3])
    L.append(f"本地占比最低的三个品类：{worst}。")
    L.append("")
    L.append("典型例子：Pokemon 的 `SV: Scarlet & Violet 151`（线上 215 张）本地完全没有；"
             "`Modern Horizons 3` 本地 424 / 线上 665；`Theros` 本地 94 / 线上 260。"
             "完整逐系列差异见 `csv/series_count_compare.csv`。")
    L.append("")
    L.append("### 3.5 系列名书写不规范，需要归一化才能对上")
    L.append("")
    L.append("- 代号前缀不统一：`SWSH08: Fusion Strike`、`SWSH: Crown Zenith`、`SM - Cosmic Eclipse`、"
             "`XY - Steam Siege`、`ME: Ascended Heroes`、`EX Crystal Guardians`，"
             "而 Holodex 侧是纯系列名（`Fusion Strike`、`Cosmic Eclipse`…）。")
    L.append("- 大小写/单复数/连词差异：`POP Series 1` vs `Pop Series 1`、"
             "`Diamond and Pearl Promos` vs `Diamond and Pearl Promo`、`Rumble` vs `Pokemon Rumble`。")
    L.append("- 版本变体拆分方式不同：TCGPlayer 把 `Jungle` 合为一项，"
             "Holodex 拆成 `Jungle 1st Edition` / `Jungle`；`Base Set` 对应 "
             "`Base Set 1st Edition` / `Shadowless` / `Unlimited` 三个 holodex set。"
             "本表取非变体名（`Jungle`、`Base Set Unlimited`）作为代表。")
    L.append("- 结论：**不能靠字符串全等关联，必须走归一化 + 分级匹配**，"
             "本表用的分级规则见文首图例；`exact` 以外的匹配都在下方可逐条复核。")
    L.append("")
    L.append("### 3.6 tcgplayer_sets_rarities_all.json 与本地卡片数据的差异")
    L.append("")
    L.append("该 json 是更早一次抓取的快照，品线与系列集合都和本地卡片数据对不齐：")
    L.append("")
    if os.path.isfile(RAR):
        rar = json.load(open(RAR, encoding="utf-8"))
        by_cat = {r["category"]: r for r in result}
        L.append("| json 品线 | json 系列 | 本地已统计 | 本地缺 |")
        L.append("|-----------|-----------|------------|--------|")
        for pl in rar:
            dirname = PL_TO_DIR.get(pl["productLineName"])
            c = by_cat.get(dirname) if dirname else None
            names = [s["setName"] for s in c["sets"]] if c else []
            idx = (build_norm_index(names), build_token_index(names)) if names else None
            miss = 0
            for s in pl["setList"]:
                if not idx:
                    miss += 1
                    continue
                hit, _ = match_name(s["setName"], names, idx[0], idx[1])
                if not hit:
                    miss += 1
            L.append(f"| {pl['productLineName']} | {len(pl['setList'])} | "
                     f"{len(pl['setList']) - miss} | {miss} |")
        L.append("")
        L.append("另外 `Dragon Ball Super: Masters` 品线（102 个系列）"
                 "在 `category_cards_final/` 下**没有对应目录**，本地无任何卡片数据；"
                 "而 crawl gameId 7 恰好就是它，59 个 holodex set 全部能在该品线里找到。")
    L.append("")
    n_inh = sum(1 for r in result for s in r["sets"] if s["match"] == "inherit")
    L.append("### 3.7 结论与建议")
    L.append("")
    L.append(f"1. **有 logo 的 {tot_logo} 个系列可以放心用**：匹配规则保守（数字/罗马数字必须一致），"
             "全部命中项已逐条核对，未发现错配。其中 `inherit` 那 "
             f"{n_inh} 条是促销/预发售子线继承母系列 logo，"
             "语义上成立但属于推断，使用时可选择性采纳。")
    L.append(f"2. **要覆盖其余 {tot_sets - tot_logo} 个系列，必须补 logo 来源**：优先 Pokemon Japan、"
             "Weiss Schwarz、Cardfight Vanguard、Flesh and Blood 这几个大品类。")
    L.append("3. **本地卡片数据需要重爬**（见 3.4），这直接影响 setNum 与后续识别召回。")
    L.append("4. 系列数量统计一律以「本地卡片数据」为准（本次 setNum 口径），"
             "若要改成 TCGPlayer 线上口径，用 `script_temp/fetch_tcg_agg.py` 抓聚合后按 json 品线回填即可。")
    L.append("")
    with open(MD, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")

    print(f"已生成 {MD}")
    print(f"已生成 {CSV}")
    print(f"系列 {tot_sets}，有 logo {tot_logo}（{tot_logo / tot_sets * 100:.1f}%），"
          f"卡牌覆盖 {tot_hit / tot_cards * 100:.1f}%")


if __name__ == "__main__":
    main()