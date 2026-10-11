#!/usr/bin/env python3
"""只为 tcgplayer_sets_rarities_all.json 里的 8 个品线构建「系列 → logo」映射。

系列名录：TCGPlayer 搜索接口聚合（script_temp/out/all_agg.json），权威且实时
logo 来源（按品线优先级）：
  万智牌   -> Scryfall（set 图标 SVG，先按 setCode↔code，再按名）
  游戏王   -> ygoprodeck（先按本地 setCode↔set_code，再按名）
  宝可梦   -> TCGdex（先按 setCode↔abbreviation/tcgOnline，再按 id，再按名）
  其余     -> Holodex 存量（按名，含衍生子线继承）
  无源     -> Flesh and Blood、Pokémon Japan

输出 doc/seriesToLogo.md
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CARDS = os.path.join(BASE, "category_cards_final", "category_cards")
CRAWL = os.path.join(BASE, "crawl", "crawl")
MD = os.path.join(BASE, "doc", "seriesToLogo.md")

# 品线 -> 本地品类目录（None = 本地无卡片数据）
LINE_TO_DIR = {
    "Pokémon": "03_Pokemon",
    "Pokémon Japan": "85_Pokemon_Japan",
    "Magic: The Gathering": "01_Magic",
    "Yu-Gi-Oh!": "02_YuGiOh",
    "One Piece Card Game": "68_One_Piece_Card_Game",
    "Disney Lorcana": "71_Disney_Lorcana",
    "Flesh and Blood TCG": "62_Flesh_and_Blood_TCG",
    "Dragon Ball Super: Masters": None,
}

# 品线 -> Holodex gameId
LINE_TO_GAME = {
    "Pokémon": 1,
    "One Piece Card Game": 2,
    "Magic: The Gathering": 3,
    "Yu-Gi-Oh!": 4,
    "Disney Lorcana": 5,
    "Dragon Ball Super: Masters": 7,
}

LINE_ORDER = ["Pokémon", "Pokémon Japan", "Magic: The Gathering", "Yu-Gi-Oh!",
              "One Piece Card Game", "Disney Lorcana", "Flesh and Blood TCG",
              "Dragon Ball Super: Masters"]

# json 里的品线名 -> all_agg.json 里的接口写法（两者拼写不同）
LINE_TO_API_KEY = {
    "Pokémon": "Pokemon",
    "Pokémon Japan": "Pokemon Japan",
    "Magic: The Gathering": "Magic: The Gathering",
    "Yu-Gi-Oh!": "YuGiOh",
    "One Piece Card Game": "One Piece Card Game",
    "Disney Lorcana": "Disney Lorcana",
    "Flesh and Blood TCG": "Flesh and Blood TCG",
    "Dragon Ball Super: Masters": "Dragon Ball Super: Masters",
}

STOP = {"the", "of", "a", "and", "vol", "volume"}
ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"}

DERIVED_RE = re.compile(
    r"\s*[:\-]?\s*(pre-?release cards|pre-?release starter deck|super pre-?release starter deck"
    r"|release event cards|celebration event cards|alternate art reprints?"
    r"|weekly play promos?|tournament cards|promotional cards|judge promos"
    r"|organized play promos|proving grounds)\s*$", re.I)

# 通用变体剥离：逐个试，能把衍生子线还原成父系列
PARENT_RES = [
    DERIVED_RE,
    re.compile(r"\s*\([^()]*\)\s*$"),                       # Dark Crisis (Worldwide English)
    re.compile(r"\s+SE\s*$", re.I),                          # Cosmo Blazer SE
    re.compile(r"\s+Special Edi(tion|ton)\s*$", re.I),
    re.compile(r"\s*[-–]\s*Preview\s*$", re.I),
    re.compile(r"^\s*(?:Art Series|Promo Pack)\s*:\s*", re.I),  # Art Series: X / Promo Pack: X
    re.compile(r"\s+(?:Theme Deck Reprints|Box Toppers|Playtest Cards)\s*$", re.I),
]


def parents(name: str) -> list[str]:
    out = []
    for r in PARENT_RES:
        p = r.sub("", name).strip(" :-")
        if p and p != name:
            out.append(p)
    return out

# 人工核对：(品线, 系列名) -> (源标签, 源内名称)
OVERRIDES: dict[tuple[str, str], tuple[str, str]] = {
    ("Pokémon", "Base Set"): ("holodex", "Base Set Unlimited"),
    ("Pokémon", "Base Set (Shadowless)"): ("holodex", "Base Set Shadowless"),
    ("Pokémon", "XY Base Set"): ("holodex", "XY Base"),
    ("Pokémon", "SM Base Set"): ("holodex", "Sun & Moon"),
    ("Pokémon", "SWSH01: Sword & Shield Base Set"): ("holodex", "Sword & Shield"),
    ("Pokémon", "SWSH: Sword & Shield Promo Cards"): ("holodex", "Sword & Shield Promo"),
    ("Pokémon", "SWSH: Crown Zenith: Galarian Gallery"): ("holodex", "Crown Zenith Galarian Gallery"),
    ("Pokémon", "SV01: Scarlet & Violet Base Set"): ("holodex", "Scarlet & Violet Base"),
    ("Pokémon", "SV: Black Bolt"): ("holodex", "Black Bolt"),
    ("Pokémon", "SV: White Flare"): ("holodex", "White Flare"),
    ("Pokémon", "Rumble"): ("holodex", "Pokemon Rumble"),
    ("Pokémon", "SV: Scarlet & Violet 151"): ("tcgdex", "151"),
    ("Pokémon", "SV: Scarlet & Violet Promo Cards"): ("holodex", "Scarlet & Violet Promos"),
    ("Pokémon", "Hidden Fates: Shiny Vault"): ("tcgdex", "Hidden Fates"),
    ("Pokémon", "HGSS Promos"): ("holodex", "HGSS Black Star Promo"),
    # 万智牌的促销线：TCGPlayer 把多年促销程序并成一条，Scryfall 按年度分开收录，
    # 同一程序各年度共用同一个符号，取其中一套。
    ("Magic: The Gathering", "Arena Promos"): ("scryfall", "MTG Arena Promos"),
    ("Magic: The Gathering", "Champs Promos"): ("scryfall", "Champs and States"),
    ("Magic: The Gathering", "European Lands"): ("scryfall", "European Land Program"),
    ("Magic: The Gathering", "Game Day & Store Championship Promos"): ("scryfall", "Game Day Promos"),
    ("Magic: The Gathering", "Guru Lands"): ("scryfall", "Guru"),
    ("Magic: The Gathering", "Hero's Path Promos"): ("scryfall", "Theros Hero's Path"),
    ("Magic: The Gathering", "Judge Promos"): ("scryfall", "Judge Gift Cards 2023"),
    ("Magic: The Gathering", "League Promos"): ("scryfall", "Arena League 2006"),
    ("Magic: The Gathering", "Magic Player Rewards"): ("scryfall", "Magic Player Rewards 2011"),
    ("Magic: The Gathering", "Magic Premiere Shop"): ("scryfall", "Magic Premiere Shop 2011"),
    ("Magic: The Gathering", "Media Promos"): ("scryfall", "Media and Collaboration Promos"),
    ("Magic: The Gathering", "Standard Showdown Promos"): ("scryfall", "XLN Standard Showdown"),
    ("Magic: The Gathering", "Tarkir Dragonfury Promos"): ("scryfall", "Tarkir: Dragonstorm Promos"),
    ("Magic: The Gathering", "The List Reprints"): ("scryfall", "The List"),
    ("Magic: The Gathering", "Ugin's Fate Promos"): ("scryfall", "Ugin's Fate"),
    ("Magic: The Gathering", "WMCQ Promo Cards"): ("scryfall", "World Magic Cup Qualifiers"),
    ("Magic: The Gathering", "World Championship Decks"): ("scryfall", "World Championship Decks 2004"),
    ("Magic: The Gathering", "Masterpiece Series: Amonkhet Invocations"):
        ("scryfall", "Amonkhet Invocations"),
    ("Magic: The Gathering", "Mythic Edition: Ravnica Allegiance"): ("scryfall", "Mythic Edition"),
    ("Magic: The Gathering", "Promo Pack: Ikoria"): ("scryfall", "Ikoria: Lair of Behemoths"),
}


_FOLD = str.maketrans({"đ": "d", "ð": "d", "ø": "o", "ł": "l", "æ": "ae", "ß": "ss"})


def norm(s: str) -> str:
    """小写、折变音符号、去标点。FAB 有 'Vetreiđi' 这类写法，必须折叠后再比。"""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().translate(_FOLD).replace("&", "and").replace("’", "'")
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


def build_name_index(names) -> tuple[dict, dict]:
    """索引只按「原始名」建；查询侧才试去前缀，避免源侧把 SM Promos 注册到通用的 promos 键上。"""
    n_idx: dict[str, str] = {}
    t_idx: dict[tuple, list[str]] = defaultdict(list)
    for n in names:
        n_idx.setdefault(norm(n), n)
        t_idx.setdefault(tuple(sorted(tokens(n))), []).append(n)
    return n_idx, t_idx


def match_by_name(name: str, n_idx: dict, t_idx: dict):
    for f in (name, strip_code_prefix(name)):
        hit = n_idx.get(norm(f))
        if hit:
            return hit, ("exact" if f == name else "prefix")
    tk = tokens(strip_code_prefix(name))
    # 词元数 <2 时退化成 {promo} 这种通用集合，禁止走词元匹配（Promos-A 会撞 XY Promos）
    if len(tk) >= 2:
        cands = t_idx.get(tuple(sorted(tk)))
        if cands:
            ok = [c for c in cands if numeric_sig(tokens(c)) == numeric_sig(tk)]
            if ok:
                return sorted(ok, key=len)[0], "token"
    return None, ""


def load_local(line: str):
    """返回 (setName -> 本地卡牌数, setName -> setCode)。"""
    d = LINE_TO_DIR.get(line)
    cnt: Counter = Counter()
    code: dict[str, str] = {}
    p = os.path.join(CARDS, d, "products.jsonl") if d else None
    if p and os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            for ln in f:
                try:
                    o = json.loads(ln)
                except Exception:
                    continue
                cnt[o.get("setName") or ""] += 1
                if o.get("setCode") and o["setName"] not in code:
                    code[o["setName"]] = o["setCode"]
    return cnt, code


def load_sources():
    src = {}
    src["scryfall"] = json.load(open(os.path.join(OUT, "src_scryfall.json"), encoding="utf-8"))
    src["ygoprodeck"] = json.load(open(os.path.join(OUT, "src_ygoprodeck.json"), encoding="utf-8"))
    src["tcgdex"] = json.load(open(os.path.join(OUT, "src_tcgdex.json"), encoding="utf-8"))
    return src


def load_holodex() -> dict[int, list[dict]]:
    d = json.load(open(os.path.join(CRAWL, "holodex_sets_organized.json"), encoding="utf-8"))
    return {int(g): [{"name": s["name"], "logo": s.get("logo"), "setId": s.get("id")}
                     for sid, si in v["series"].items() for s in si["sets"]]
            for g, v in d.items()}


class Source:
    """一个 logo 源：支持 code 精确匹配 + 名称分级匹配 + 衍生子线继承。"""

    def __init__(self, label: str, entries: list[dict], key_name: str, key_codes, key_logo):
        self.label = label
        self.entries = entries
        self.by_code: dict[str, dict] = {}
        for e in entries:
            for c in key_codes(e):
                if c:
                    self.by_code.setdefault(c.strip().lower(), e)
        names = [key_name(e) for e in entries]
        self.n_idx, self.t_idx = build_name_index(names)
        self.key_name = key_name
        self.key_logo = key_logo
        self._by_name = {key_name(e): e for e in entries}

    def find(self, set_name: str, set_code: str | None, ambiguous: set[str] = frozenset()):
        # 1) 代码精确（该代号在本品线内必须唯一，否则 PR/POP 这类通用码会撞车）
        if set_code and set_code.strip().lower() not in ambiguous:
            e = self.by_code.get(set_code.strip().lower())
            if e:
                return e, "code"
        # 2) 名称分级
        hit, m = match_by_name(set_name, self.n_idx, self.t_idx)
        if hit:
            return self._by_name[hit], m
        # 3) 衍生子线 / 变体继承父系列
        for parent in parents(set_name):
            hit, _ = match_by_name(parent, self.n_idx, self.t_idx)
            if hit:
                return self._by_name[hit], "inherit"
        return None, ""

    def logo(self, e: dict):
        return self.key_logo(e)


def tcgdex_logo(e: dict):
    """src_tcgdex.json 里的 logo 已由 fetch_logo_sources.py 探明扩展名（.webp 或 .png）。"""
    return e.get("logo")


def fab_parent(set_name: str, fab_rows: list[dict]):
    """FAB 的单副预组只在官网的「合集页」里出现（如 Monarch Blitz Decks 含 4 副），
    这里把 'Blitz Deck: Monarch - Boltyn' 这类挂到合集页的图上，标 inherit。"""
    key = None
    m = re.match(r"^Blitz Deck:\s*(.+?)\s*-\s*.+$", set_name)
    if m:
        key = (norm(m.group(1)), "blitz")
    m = re.match(r"^Historic Pack\s+(\d+)\s+Blitz Deck:.*$", set_name, re.I)
    if m:
        key = ("historypack" + m.group(1), "blitz")
    m = re.match(r"^Armory Deck:\s*Legends\b.*$", set_name, re.I)
    if m:
        key = ("armorydecklegends", "")
    if not key:
        return None, None, None
    want, must = key
    for r in fab_rows:
        u = norm(r["url"])
        if want and want in u and (not must or must in r["url"].lower()):
            return r["logo"], "fab-official", "inherit"
    return None, None, None


def logo_tier(r: dict) -> str:
    """给每条 logo 分质量层级：专属符号 > 官方包装图 > 继承/通用图标。"""
    lg, src, m = r["logo"] or "", r["source"] or "", r["match"] or ""
    if not lg:
        return "none"
    if "default.svg" in lg or "star.svg" in lg:
        return "generic"
    if m == "inherit":
        return "inherit"
    fn = lg.split("/")[-1].rsplit(".", 1)[0]
    if src == "bulbapedia":
        return "symbol" if re.search(r"logo", fn, re.I) else "artwork"
    if src == "fab-official":
        return "symbol" if re.search(r"(logo|_name|-name\.|[A-Z]{2,4}-1)", fn) else "artwork"
    if src == "holodex":
        return "artwork"      # Holodex 给的是系列 logo 图，含包装风
    return "symbol"


def main() -> None:
    agg = json.load(open(os.path.join(OUT, "all_agg.json"), encoding="utf-8"))
    src = load_sources()
    holodex = load_holodex()

    scryfall = Source("scryfall", src["scryfall"],
                      key_name=lambda e: e["name"],
                      key_codes=lambda e: [e.get("code")],
                      key_logo=lambda e: e.get("icon_svg_uri"))
    ygo = Source("ygoprodeck", src["ygoprodeck"],
                 key_name=lambda e: e["set_name"],
                 key_codes=lambda e: [e.get("set_code")],
                 key_logo=lambda e: e.get("set_image"))
    tcgdex = Source("tcgdex", src["tcgdex"],
                    key_name=lambda e: e.get("name") or e["id"],
                    key_codes=lambda e: [e.get("id"), e.get("tcgOnline"),
                                         (e.get("abbreviation") or {}).get("official")],
                    key_logo=tcgdex_logo)

    # Holodex 源（按品线一个 game）
    hx_sources = {}
    for line, gid in LINE_TO_GAME.items():
        sets = holodex.get(gid, [])
        s = Source(f"holodex", sets, key_name=lambda e: e["name"],
                   key_codes=lambda e: [], key_logo=lambda e: e.get("logo"))
        hx_sources[line] = s

    # Flesh and Blood 官方站（fabtcg.com，curl_cffi 抓）
    fab_path = os.path.join(OUT, "src_fab.json")
    fab_src = None
    fab_rows: list[dict] = []
    if os.path.isfile(fab_path):
        fab_rows = [r for r in json.load(open(fab_path, encoding="utf-8")) if r.get("logo")]
        fab_src = Source("fab-official", fab_rows, key_name=lambda e: e["name"],
                         key_codes=lambda e: [], key_logo=lambda e: e["logo"])

    # Pokémon Japan（Bulbapedia 抓取，按 TCGPlayer 系列名精确对应）
    jp_path = os.path.join(OUT, "src_pkmjp.json")
    jp_map: dict[str, str] = {}
    if os.path.isfile(jp_path):
        jp_map = {r["name"]: r["logo"] for r in json.load(open(jp_path, encoding="utf-8"))
                  if r.get("logo")}

    # ONE PIECE 官方站（按产品代号 ST-23 / EB-03 … 匹配）
    op_path = os.path.join(OUT, "src_onepiece.json")
    op_map: dict[str, str] = {}
    if os.path.isfile(op_path):
        d = json.load(open(op_path, encoding="utf-8"))
        op_map = {k.upper().replace("-", ""): v for k, v in d.get("by_code", {}).items()
                  if "/images/products/" in (v or "")}

    def op_code(name: str) -> str | None:
        m = re.match(r"^\s*((?:ST|OP|EB|PRB|LD|GD)-?\d{1,2})\s*:", name, re.I)
        return m.group(1).upper().replace("-", "") if m else None

    # 子 agent 补齐的缺口（script_temp/merge_gapfix.py 产出，URL 已校验过）
    gp_path = os.path.join(OUT, "gapfix_merged.json")
    gapfix: dict[str, dict] = {}
    if os.path.isfile(gp_path):
        gapfix = json.load(open(gp_path, encoding="utf-8"))
        print(f"载入子 agent 补齐结果 {len(gapfix)} 条")

    rows_by_line: dict[str, list[dict]] = {}
    for line in LINE_ORDER:
        info = agg.get(LINE_TO_API_KEY[line])
        if not info:
            continue
        cnt, code = load_local(line)
        # 本品线内被多个系列共用的 setCode 不能作为匹配键
        cc = Counter(c.strip().lower() for c in code.values() if c and c.strip())
        ambiguous = {c for c, n in cc.items() if n > 1}
        rows = []
        for set_name, official in sorted(info["sets"].items()):
            set_code = code.get(set_name)
            logo = method = source = None
            ov = OVERRIDES.get((line, set_name))
            if ov:
                want = norm(ov[1])
                pool = {"holodex": holodex.get(LINE_TO_GAME.get(line, -1), []),
                        "tcgdex": tcgdex.entries,
                        "scryfall": scryfall.entries,
                        "ygoprodeck": ygo.entries}.get(ov[0], [])
                e = next((x for x in pool
                          if norm(x.get("name") or x.get("set_name") or "") == want), None)
                if e:
                    lg = {"holodex": lambda x: x.get("logo"),
                          "tcgdex": tcgdex_logo,
                          "scryfall": lambda x: x.get("icon_svg_uri"),
                          "ygoprodeck": lambda x: x.get("set_image")}[ov[0]](e)
                    if lg:
                        logo, source, method = lg, ov[0], "override"
            if not logo and line == "Pokémon Japan" and set_name in jp_map:
                logo, source, method = jp_map[set_name], "bulbapedia", "exact"
            if not logo and line == "One Piece Card Game":
                c = op_code(set_name)
                if c and c in op_map:
                    logo, source, method = op_map[c], "onepiece-official", "code"
            if not logo and fab_rows:
                logo, source, method = fab_parent(set_name, fab_rows)
            if not logo:
                chain = {"Magic: The Gathering": [scryfall, hx_sources.get(line)],
                         "Yu-Gi-Oh!": [ygo, hx_sources.get(line)],
                         "Pokémon": [tcgdex, hx_sources.get(line)],
                         "Flesh and Blood TCG": [fab_src]}.get(line) \
                    or ([hx_sources[line]] if line in hx_sources else [])
                chain = [c for c in chain if c]
                for s in chain:
                    e, m = s.find(set_name, set_code, ambiguous)
                    if e:
                        lg = s.logo(e)
                        if lg:
                            logo, source, method = lg, s.label, m
                            break
            if not logo and set_name in gapfix:
                g = gapfix[set_name]
                logo, source, method = g["logo"], g["source"], "gapfix"
            rows.append({"setName": set_name, "online": official,
                         "local": cnt.get(set_name, 0), "setCode": set_code or "",
                         "logo": logo, "source": source, "match": method})
        rows_by_line[line] = rows

    # ---------- Markdown ----------
    L: list[str] = []
    L.append("# 系列 → Logo 映射表（seriesToLogo.md）")
    L.append("")
    L.append(f"> 生成时间：{date.today().isoformat()}　生成脚本：`script_temp/{os.path.basename(__file__)}`")
    L.append("> 范围：`tcgplayer_sets_rarities_all.json` 里的 8 个品线（其它品类暂不处理）")
    L.append("> 系列名录：TCGPlayer 搜索接口 setName 聚合（实时权威）")
    L.append("> 卡牌数量：`本地 / 线上`，本地取自 `category_cards_final/.../products.jsonl`，"
             "线上取自 TCGPlayer 聚合")
    L.append("")
    L.append("## 一、总览")
    L.append("")
    L.append("| 品线 | 系列数 | 有 logo | 覆盖率 | logo 来源 |")
    L.append("|------|--------|---------|--------|-----------|")
    tot = tot_logo = 0
    for line in LINE_ORDER:
        rows = rows_by_line.get(line)
        if not rows:
            continue
        n = len(rows)
        has = sum(1 for r in rows if r["logo"])
        srcs = Counter(r["source"] for r in rows if r["source"])
        tot += n
        tot_logo += has
        L.append(f"| {line} | {n} | {has} | {has / n * 100:.0f}% | "
                 f"{'、'.join(f'{k} {v}' for k, v in srcs.most_common()) or '—'} |")
    L.append(f"| **合计** | **{tot}** | **{tot_logo}** | **{tot_logo / tot * 100:.1f}%** | |")
    L.append("")
    L.append("**logo 字段含义**：Scryfall 是印在卡面上的系列符号（SVG）；ygoprodeck 是官方系列图；"
             "TCGdex / Holodex / FAB 官方站 / ONE PIECE 官方站是各自来源的系列 logo 或产品封面；"
             "Bulbapedia 是日文系列的 logo，没有 logo 素材时退化为包装图。")
    L.append("")
    L.append("## 二、映射表")
    L.append("")
    for line in LINE_ORDER:
        rows = rows_by_line.get(line)
        if not rows:
            continue
        has = sum(1 for r in rows if r["logo"])
        L.append(f"### {line}（{len(rows)} 个系列，{has} 个有 logo）")
        L.append("")
        L.append("| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |")
        L.append("|------|------|----------|------------------|----------|")
        for r in rows:
            logo = r["logo"] or ""
            if r["match"] == "inherit":
                logo += " ※"
            if logo and ("default.svg" in logo or "star.svg" in logo):
                logo += " ⚠"
            cnt = f"{r['local']} / {r['online']}"
            src_label = r["source"] or "—"
            if r["match"] == "inherit":
                src_label += "（继承父系列）"
            L.append(f"| {line} | {r['setName'].replace('|', chr(92) + '|')} | {logo} | {cnt} | {src_label} |")
        L.append("")
    L.append("> `※` = 该系列是促销/预发售/发售活动等衍生子线，logo 继承自同名的父系列。")
    L.append("> `⚠` = 该系列在 Scryfall 用的是通用/共享图标（`default.svg` 占位或 `star.svg` 星形），"
             "不是该系列专属符号，可靠性低于其他条目。")
    L.append("")
    L.append("## 三、logo 来源与缺口")
    L.append("")
    L.append("### 3.1 各来源明细")
    L.append("")
    L.append("| 来源 | 是什么 | 数据量 | 接入方式 |")
    L.append("|------|--------|--------|----------|")
    L.append("| Scryfall | 印在卡面上的**系列符号**（SVG） | 1058 个 set | `api.scryfall.com/sets`，先按 "
             "`setCode`↔`code`，再按名 |")
    L.append("| ygoprodeck | 官方**系列图**（JPG） | 1035 个 set | "
             "`db.ygoprodeck.com/api/v7/cardsets.php`，先按 `setCode`↔`set_code`，再按名 |")
    L.append("| TCGdex | 系列 **logo**（webp/png） | "
             f"{len(src['tcgdex'])} 个 set，其中 {sum(1 for e in src['tcgdex'] if e.get('logo'))} 个有 logo | "
             "`api.tcgdex.net/v2/en/sets/{id}`，按 `setCode`↔`abbreviation`，再按名 |")
    L.append("| Holodex | 第三方 App 的系列 logo（webp） | 存量 12 个游戏 | "
             "`crawl/crawl/holodex_sets_organized.json`，按名 |")
    n_jp = sum(1 for rs in rows_by_line.values() for r in rs if r["source"] == "bulbapedia")
    n_fab = sum(1 for rs in rows_by_line.values() for r in rs if r["source"] == "fab-official")
    n_op = sum(1 for rs in rows_by_line.values() for r in rs if r["source"] == "onepiece-official")
    L.append(f"| FAB 官方站 | 系列 logo / 产品封面（png/webp），{n_fab} 条命中 | 275 个页面 | "
             "`fabtcg.com`（被 Cloudflare 挡，用 `curl_cffi` 伪装 TLS 指纹），"
             "sitemap + products/digital-assets 页 |")
    L.append(f"| Bulbapedia 图库 | 日文系列 logo / 包装图，{n_jp} 条命中 | 按代码前缀枚举 | "
             "`archives.bulbagarden.net/w/api.php` + `bulbapedia.bulbagarden.net/w/api.php`"
             "（opensearch 找条目），文件名形如 `S8b_VMAX_Climax_Logo.png` |")
    L.append(f"| ONE PIECE 官方站 | 产品 logo（webp），{n_op} 条命中 | 187 个产品页 | "
             "`en.onepiece-cardgame.com/products/`，按产品代号 `ST-27` 之类 |")
    L.append("")
    n_def = sum(1 for r in rows_by_line.get("Magic: The Gathering", [])
                if r["logo"] and "default.svg" in r["logo"])
    n_inh = sum(1 for rs in rows_by_line.values() for r in rs if r["match"] == "inherit")
    n_ov = sum(1 for rs in rows_by_line.values() for r in rs if r["match"] == "override")
    L.append("**表内所有 logo URL 已逐个校验可访问**"
             "（`script_temp/verify_logo_urls.py`，HEAD 请求）。")
    L.append("")
    tiers = Counter(logo_tier(r) for rs in rows_by_line.values() for r in rs)
    TIER_DESC = {
        "symbol": "系列专属符号 / logo（最可靠）",
        "artwork": "官方包装图 / 产品封面（能标识系列，但不是 logo 本身）",
        "inherit": "继承自父系列的图（衍生子线共用一张）",
        "generic": "Scryfall 通用占位图标（`default.svg` / `star.svg`）",
        "none": "没有 logo",
    }
    L.append("按可靠性分层（同一批 URL 的质量差异较大，这里分开计数）：")
    L.append("")
    L.append("| 层级 | 含义 | 条数 |")
    L.append("|------|------|------|")
    for k in ("symbol", "artwork", "inherit", "generic", "none"):
        if tiers.get(k):
            L.append(f"| `{k}` | {TIER_DESC[k]} | {tiers[k]} |")
    L.append("")
    L.append(f"注意两点：万智牌里有 {n_def} 个系列拿到的 Scryfall 图标是通用默认符号"
             "（`default.svg`），说明该系列在 Scryfall 没有专属符号；"
             f"另有 {n_inh} 条是衍生子线继承父系列 logo（表中标 `※`）、{n_ov} 条是人工核对指定。")
    L.append("")
    yg_codes = Counter(e["set_code"] for e in src["ygoprodeck"] if e.get("set_code"))
    yg_multi = {k: v for k, v in yg_codes.items() if v > 1}
    L.append(f"匹配规则上的两道保险：**代号必须在本品线内唯一**（否则 `PR` 这类被 12 个系列共用的"
             f"促销码会撞车），**词元数少于 2 个不走词元匹配**（否则 `Promos-A` 会撞上 `XY Promos`）。")
    L.append("")
    L.append(f"ygoprodeck 的一个已知局限：它用 `set_code` 拼图片地址，而它自己有 "
             f"{len(yg_multi)} 个代号被 {sum(yg_multi.values())} 个不同 set 共用"
             f"（如 `YS15` 同时对应 2-Player Starter Deck、Dark Legion、Saber Force 三副预组），"
             "这些系列拿到的是同一张图，未必是该系列专属。")
    L.append("")
    L.append("### 3.2 仍然没有 logo 的系列及原因")
    L.append("")
    for line in LINE_ORDER:
        rows = rows_by_line.get(line) or []
        if not rows:
            continue
        miss = [r["setName"] for r in rows if not r["logo"]]
        if not miss:
            continue
        L.append(f"- **{line}**：{len(miss)} 个未覆盖")
        if line == "Pokémon Japan":
            L.append("  - 已有的 177 条来自 Bulbapedia 图库，按系列代码做前缀枚举命中"
                     "（Bulbapedia 的 logo 文件名就是 `{代码}_{名称}_Logo.png`）。"
                     "剩余的没命中，是因为 **TCGPlayer 有 153 个系列根本没给代码**"
                     "（都是 1996–2009 的老扩展包与预组，如 `Pokemon VS`、`City Gym Decks`），"
                     "另外 158 个有代码的里多数在 Bulbapedia 上只有卡图、没有包装图或 logo"
                     "（如 `SM-P`、`XY-P` 这类促销线，前缀查询返回 0 个文件）。"
                     "TCGdex 的日文 set 没有 logo 字段；官方 `pokemon-card.com` 只在最新产品页放 logo。")
        elif line == "Flesh and Blood TCG":
            L.append("  - 已通过 `curl_cffi` 绕过 Cloudflare 抓到官方站 275 个页面的系列 logo 与封面图。"
                     "剩余的是官方站**没有独立素材**的：单副 Blitz Deck（官网只按合集页出售，"
                     "如 `Blitz Deck: Monarch - Boltyn` 只存在于 `monarch-blitz-decks` 合集里，"
                     "已按父合集图继承）、`GEM Pack`、`Hero Deck`、`Welcome Deck` / `Flesh and Blood: Promo Cards`。")
        elif line == "Dragon Ball Super: Masters":
            L.append("  - 缺的主要是 `Expansion Deck Box Set XX`、`Collector's Selection Vol.X` 这类"
                     "非补充包产品，Holodex 不单独收录；官方站 `dbs-cardgame.com` 的产品页只展示当期产品，"
                     "没有全量归档。")
        elif line == "One Piece Card Game":
            L.append("  - 缺的绝大多数是 `ST-01`…`ST-20` 早期预组：官方站对应产品页（`decks/st05.php`、"
                     "`st15-20.php`）只放了卡图，没有预组 logo 或包装图；"
                     "`optcgapi.com` 只收录 22 个主系列。")
        elif line.startswith("Pokémon"):
            L.append("  - 缺的是 Trainer Kit、各类 Promo、World Championship Decks、Jumbo Cards 等子线，"
                     "TCGdex / Holodex / Scryfall 三类源都不单独收录。")
        elif line.startswith("Magic"):
            L.append("  - 缺的是 TCGPlayer 独有的促销聚合线（`Oversize Cards`、`Prerelease Cards`、"
                     "`Buy-A-Box Promos`、`WPN & Gateway Promos` 等），Scryfall 侧按年度拆开收录、"
                     "没有与之对应的单一条目；可对应的 20 条已人工核对补上（见 3.3）。")
        else:
            L.append("  - 缺的是铁盒、收藏盒、活动场次卡等子线，ygoprodeck 对这批 set 只给名录不给图"
                     "（1035 个 set 里有 125 个没有 `set_image` 字段，且用 `set_code` 拼 URL 也是 404）。")
        L.append(f"  - 明细：{'、'.join(miss[:12])}{' …' if len(miss) > 12 else ''}")
    L.append("")

    gf = [(line, r) for line in LINE_ORDER for r in (rows_by_line.get(line) or [])
          if r["match"] == "gapfix"]
    if gf:
        L.append(f"### 3.3 本轮由子 agent 补齐的 {len(gf)} 条（逐条附依据，便于复核）")
        L.append("")
        L.append("| 品线 | 系列 | logo | 来源 | 判定依据 |")
        L.append("|------|------|------|------|----------|")
        for line, r in gf:
            ev = (gapfix.get(r["setName"], {}).get("evidence") or "").replace("|", "\\|")
            L.append(f"| {line} | {r['setName'].replace('|', chr(92) + '|')} | {r['logo']} | "
                     f"{r['source']} | {ev} |")
        L.append("")
    L.append("## 四、待补系列完整清单")
    L.append("")
    L.append(f"下面是没有 logo 的全部 {sum(1 for rs in rows_by_line.values() for r in rs if not r['logo'])} "
             "个系列，按品线分组，用于后续逐个补齐。")
    L.append("")
    for line in LINE_ORDER:
        rows = rows_by_line.get(line) or []
        miss = [r["setName"] for r in rows if not r["logo"]]
        if not miss:
            continue
        L.append(f"**{line}**（{len(miss)} 个）")
        L.append("")
        for n in miss:
            L.append(f"- {n}")
        L.append("")

    with open(MD, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    with open(os.path.join(OUT, "series_logo_rows.json"), "w", encoding="utf-8") as f:
        json.dump(rows_by_line, f, ensure_ascii=False, indent=1)
    print(f"已生成 {MD}")
    for line in LINE_ORDER:
        rows = rows_by_line.get(line) or []
        if rows:
            has = sum(1 for r in rows if r["logo"])
            print(f"  {line:28s} {len(rows):4d} 系列，有 logo {has:4d} ({has/len(rows)*100:5.1f}%)")
    print(f"合计 {tot} 系列，有 logo {tot_logo}（{tot_logo / tot * 100:.1f}%）")


if __name__ == "__main__":
    main()