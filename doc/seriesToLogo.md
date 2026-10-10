# 系列 → Logo 映射表（seriesToLogo.md）

> 生成时间：2026-10-10　生成脚本：`script_temp/build_series_logo_v2.py`
> 范围：`tcgplayer_sets_rarities_all.json` 里的 8 个品线（其它品类暂不处理）
> 系列名录：TCGPlayer 搜索接口 setName 聚合（实时权威）
> 卡牌数量：`本地 / 线上`，本地取自 `category_cards_final/.../products.jsonl`，线上取自 TCGPlayer 聚合

## 一、总览

| 品线 | 系列数 | 有 logo | 覆盖率 | logo 来源 |
|------|--------|---------|--------|-----------|
| Pokémon | 216 | 187 | 87% | tcgdex 132、holodex 55 |
| Pokémon Japan | 455 | 177 | 39% | bulbapedia 177 |
| Magic: The Gathering | 445 | 421 | 95% | scryfall 411、holodex 10 |
| Yu-Gi-Oh! | 613 | 514 | 84% | ygoprodeck 512、holodex 2 |
| One Piece Card Game | 85 | 42 | 49% | holodex 35、onepiece-official 7 |
| Disney Lorcana | 20 | 15 | 75% | holodex 15 |
| Flesh and Blood TCG | 105 | 88 | 84% | fab-official 88 |
| Dragon Ball Super: Masters | 100 | 59 | 59% | holodex 59 |
| **合计** | **2039** | **1503** | **73.7%** | |

**logo 字段含义**：Scryfall 是印在卡面上的系列符号（SVG）；ygoprodeck 是官方系列图；TCGdex / Holodex / FAB 官方站 / ONE PIECE 官方站是各自来源的系列 logo 或产品封面；Bulbapedia 是日文系列的 logo，没有 logo 素材时退化为包装图。

## 二、映射表

### Pokémon（216 个系列，187 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Pokémon | Alternate Art Promos | https://holodex-prod-bucket.b-cdn.net/sets/smpr/logo.webp | 56 / 56 | holodex |
| Pokémon | Aquapolis | https://assets.tcgdex.net/en/ecard/ecard2/logo.webp | 186 / 186 | tcgdex |
| Pokémon | Arceus | https://assets.tcgdex.net/en/pl/pl4/logo.png | 111 / 111 | tcgdex |
| Pokémon | BW Trainer Kit: Excadrill & Zoroark |  | 0 / 60 | — |
| Pokémon | Base Set | https://holodex-prod-bucket.b-cdn.net/sets/baseu/logo.webp | 83 / 102 | holodex |
| Pokémon | Base Set (Shadowless) | https://holodex-prod-bucket.b-cdn.net/sets/basesl/logo.webp | 101 / 102 | holodex |
| Pokémon | Base Set 2 | https://assets.tcgdex.net/en/base/base4/logo.webp | 130 / 130 | tcgdex |
| Pokémon | Battle Academy | https://holodex-prod-bucket.b-cdn.net/sets/ba20/logo.webp | 136 / 139 | holodex |
| Pokémon | Battle Academy 2022 | https://holodex-prod-bucket.b-cdn.net/sets/ba22/logo.webp | 139 / 139 | holodex |
| Pokémon | Battle Academy 2024 | https://holodex-prod-bucket.b-cdn.net/sets/ba24/logo.webp | 139 / 139 | holodex |
| Pokémon | Best of Promos |  | 15 / 15 | — |
| Pokémon | Black and White | https://assets.tcgdex.net/en/bw/bw1/logo.webp | 97 / 122 | tcgdex |
| Pokémon | Black and White Promos | https://holodex-prod-bucket.b-cdn.net/sets/bwp/logo.webp | 148 / 148 | holodex |
| Pokémon | Blister Exclusives |  | 140 / 144 | — |
| Pokémon | Boundaries Crossed | https://assets.tcgdex.net/en/bw/bw7/logo.webp | 156 / 156 | tcgdex |
| Pokémon | Burger King Promos |  | 24 / 24 | — |
| Pokémon | Call of Legends | https://assets.tcgdex.net/en/col/col1/logo.webp | 105 / 106 | tcgdex |
| Pokémon | Celebrations | https://assets.tcgdex.net/en/swsh/cel25/logo.webp | 36 / 39 | tcgdex |
| Pokémon | Celebrations: Classic Collection | https://holodex-prod-bucket.b-cdn.net/sets/swsh10/logo.webp | 25 / 25 | holodex |
| Pokémon | Champion's Path | https://assets.tcgdex.net/en/swsh/swsh3.5/logo.webp | 87 / 93 | tcgdex |
| Pokémon | Countdown Calendar Promos |  | 24 / 24 | — |
| Pokémon | DP Trainer Kit: Manaphy & Lucario |  | 0 / 23 | — |
| Pokémon | Dark Explorers | https://assets.tcgdex.net/en/bw/bw5/logo.webp | 112 / 112 | tcgdex |
| Pokémon | Deck Exclusives |  | 470 / 506 | — |
| Pokémon | Detective Pikachu | https://assets.tcgdex.net/en/sm/det1/logo.webp | 25 / 26 | tcgdex |
| Pokémon | Diamond and Pearl | https://assets.tcgdex.net/en/dp/dp1/logo.webp | 112 / 130 | tcgdex |
| Pokémon | Diamond and Pearl Promos | https://holodex-prod-bucket.b-cdn.net/sets/dppromo/logo.webp | 66 / 66 | holodex |
| Pokémon | Double Crisis | https://assets.tcgdex.net/en/xy/dc1/logo.webp | 36 / 36 | tcgdex |
| Pokémon | Dragon Majesty | https://holodex-prod-bucket.b-cdn.net/sets/sm9/logo.webp | 86 / 86 | holodex |
| Pokémon | Dragon Vault | https://assets.tcgdex.net/en/bw/dv1/logo.webp | 22 / 22 | tcgdex |
| Pokémon | Dragons Exalted | https://assets.tcgdex.net/en/bw/bw6/logo.webp | 129 / 129 | tcgdex |
| Pokémon | EX Battle Stadium | https://assets.tcgdex.net/en/swsh/swsh5/logo.webp | 49 / 49 | tcgdex |
| Pokémon | EX Crystal Guardians | https://assets.tcgdex.net/en/ex/ex14/logo.webp | 100 / 100 | tcgdex |
| Pokémon | EX Delta Species | https://assets.tcgdex.net/en/ex/ex11/logo.webp | 114 / 114 | tcgdex |
| Pokémon | EX Deoxys | https://assets.tcgdex.net/en/ex/ex8/logo.webp | 108 / 108 | tcgdex |
| Pokémon | EX Dragon | https://assets.tcgdex.net/en/ex/ex3/logo.webp | 45 / 100 | tcgdex |
| Pokémon | EX Dragon Frontiers | https://assets.tcgdex.net/en/ex/ex15/logo.webp | 101 / 101 | tcgdex |
| Pokémon | EX Emerald | https://assets.tcgdex.net/en/ex/ex9/logo.webp | 106 / 107 | tcgdex |
| Pokémon | EX FireRed & LeafGreen | https://assets.tcgdex.net/en/ex/ex6/logo.webp | 0 / 116 | tcgdex |
| Pokémon | EX Hidden Legends | https://assets.tcgdex.net/en/ex/ex5/logo.webp | 102 / 102 | tcgdex |
| Pokémon | EX Holon Phantoms | https://assets.tcgdex.net/en/ex/ex13/logo.webp | 111 / 111 | tcgdex |
| Pokémon | EX Legend Maker | https://assets.tcgdex.net/en/ex/ex12/logo.webp | 93 / 93 | tcgdex |
| Pokémon | EX Power Keepers | https://assets.tcgdex.net/en/ex/ex16/logo.webp | 108 / 108 | tcgdex |
| Pokémon | EX Ruby and Sapphire | https://assets.tcgdex.net/en/ex/ex1/logo.webp | 109 / 109 | tcgdex |
| Pokémon | EX Sandstorm | https://assets.tcgdex.net/en/ex/ex2/logo.webp | 100 / 100 | tcgdex |
| Pokémon | EX Team Magma vs Team Aqua | https://assets.tcgdex.net/en/ex/ex4/logo.webp | 97 / 97 | tcgdex |
| Pokémon | EX Team Rocket Returns | https://assets.tcgdex.net/en/ex/ex7/logo.webp | 111 / 111 | tcgdex |
| Pokémon | EX Trainer Kit 1: Latias & Latios |  | 0 / 20 | — |
| Pokémon | EX Trainer Kit 2: Plusle & Minun |  | 0 / 24 | — |
| Pokémon | EX Unseen Forces | https://assets.tcgdex.net/en/ex/ex10/logo.webp | 145 / 145 | tcgdex |
| Pokémon | Emerging Powers | https://assets.tcgdex.net/en/bw/bw2/logo.webp | 107 / 107 | tcgdex |
| Pokémon | Expedition | https://assets.tcgdex.net/en/ecard/ecard1/logo.webp | 165 / 165 | tcgdex |
| Pokémon | First Partner Collection 2026 |  | 3 / 3 | — |
| Pokémon | First Partner Pack |  | 24 / 24 | — |
| Pokémon | Fossil | https://assets.tcgdex.net/en/base/base3/logo.webp | 61 / 62 | tcgdex |
| Pokémon | Generations | https://assets.tcgdex.net/en/xy/g1/logo.webp | 101 / 101 | tcgdex |
| Pokémon | Generations: Radiant Collection | https://holodex-prod-bucket.b-cdn.net/sets/xy12/logo.webp | 32 / 32 | holodex |
| Pokémon | Great Encounters | https://assets.tcgdex.net/en/dp/dp4/logo.webp | 106 / 106 | tcgdex |
| Pokémon | Gym Challenge | https://assets.tcgdex.net/en/gym/gym2/logo.webp | 132 / 132 | tcgdex |
| Pokémon | Gym Heroes | https://assets.tcgdex.net/en/gym/gym1/logo.webp | 132 / 132 | tcgdex |
| Pokémon | HGSS Promos | https://holodex-prod-bucket.b-cdn.net/sets/hgss1/logo.webp | 38 / 38 | holodex |
| Pokémon | HGSS Trainer Kit: Gyarados & Raichu |  | 0 / 60 | — |
| Pokémon | HeartGold SoulSilver | https://assets.tcgdex.net/en/hgss/hgss1/logo.png | 124 / 124 | tcgdex |
| Pokémon | Hidden Fates | https://assets.tcgdex.net/en/sm/sm115/logo.webp | 72 / 78 | tcgdex |
| Pokémon | Hidden Fates: Shiny Vault | https://assets.tcgdex.net/en/sm/sm115/logo.webp | 94 / 94 | tcgdex |
| Pokémon | Jumbo Cards |  | 342 / 345 | — |
| Pokémon | Jungle | https://assets.tcgdex.net/en/base/base2/logo.webp | 64 / 64 | tcgdex |
| Pokémon | Kalos Starter Set | https://assets.tcgdex.net/en/xy/xy0/logo.webp | 44 / 44 | tcgdex |
| Pokémon | Kids WB Promos |  | 5 / 5 | — |
| Pokémon | League & Championship Cards |  | 514 / 620 | — |
| Pokémon | Legendary Collection | https://assets.tcgdex.net/en/lc/lc/logo.webp | 110 / 110 | tcgdex |
| Pokémon | Legendary Treasures | https://assets.tcgdex.net/en/bw/bw11/logo.webp | 116 / 116 | tcgdex |
| Pokémon | Legendary Treasures: Radiant Collection | https://holodex-prod-bucket.b-cdn.net/sets/bw13/logo.webp | 25 / 25 | holodex |
| Pokémon | Legends Awakened | https://assets.tcgdex.net/en/dp/dp6/logo.webp | 146 / 146 | tcgdex |
| Pokémon | ME01: Mega Evolution | https://assets.tcgdex.net/en/me/me01/logo.png | 194 / 194 | tcgdex |
| Pokémon | ME02: Phantasmal Flames | https://assets.tcgdex.net/en/me/me02/logo.webp | 134 / 134 | tcgdex |
| Pokémon | ME03: Perfect Order | https://assets.tcgdex.net/en/me/me03/logo.webp | 132 / 132 | tcgdex |
| Pokémon | ME04: Chaos Rising | https://assets.tcgdex.net/en/me/me04/logo.webp | 127 / 127 | tcgdex |
| Pokémon | ME05: Pitch Black | https://assets.tcgdex.net/en/me/me05/logo.webp | 125 / 125 | tcgdex |
| Pokémon | ME: 30th Celebration | https://holodex-prod-bucket.b-cdn.net/sets/me_30th24722/logo.webp | 40 / 170 | holodex |
| Pokémon | ME: 30th Celebration Classic Collection | https://holodex-prod-bucket.b-cdn.net/sets/me_30thcc24837/logo.webp | 0 / 30 | holodex |
| Pokémon | ME: Ascended Heroes | https://assets.tcgdex.net/en/me/me02.5/logo.webp | 550 / 580 | tcgdex |
| Pokémon | ME: Mega Evolution Promo | https://holodex-prod-bucket.b-cdn.net/sets/mep/logo.webp | 120 / 141 | holodex |
| Pokémon | MEE: Mega Evolution Energies |  | 8 / 16 | — |
| Pokémon | Majestic Dawn | https://assets.tcgdex.net/en/dp/dp5/logo.webp | 100 / 100 | tcgdex |
| Pokémon | McDonald's 25th Anniversary Promos | https://holodex-prod-bucket.b-cdn.net/sets/mc10/logo.webp | 25 / 25 | holodex |
| Pokémon | McDonald's Promos 2011 | https://holodex-prod-bucket.b-cdn.net/sets/mc1/logo.webp | 0 / 12 | holodex |
| Pokémon | McDonald's Promos 2012 | https://holodex-prod-bucket.b-cdn.net/sets/mc2/logo.webp | 0 / 12 | holodex |
| Pokémon | McDonald's Promos 2014 | https://holodex-prod-bucket.b-cdn.net/sets/mc3/logo.webp | 12 / 12 | holodex |
| Pokémon | McDonald's Promos 2015 | https://holodex-prod-bucket.b-cdn.net/sets/mc4/logo.webp | 12 / 12 | holodex |
| Pokémon | McDonald's Promos 2016 | https://holodex-prod-bucket.b-cdn.net/sets/mc5/logo.webp | 12 / 12 | holodex |
| Pokémon | McDonald's Promos 2017 | https://holodex-prod-bucket.b-cdn.net/sets/mc6/logo.webp | 12 / 12 | holodex |
| Pokémon | McDonald's Promos 2018 | https://holodex-prod-bucket.b-cdn.net/sets/mc7/logo.webp | 12 / 12 | holodex |
| Pokémon | McDonald's Promos 2019 | https://holodex-prod-bucket.b-cdn.net/sets/mc8/logo.webp | 7 / 12 | holodex |
| Pokémon | McDonald's Promos 2022 | https://holodex-prod-bucket.b-cdn.net/sets/mc11/logo.webp | 0 / 15 | holodex |
| Pokémon | McDonald's Promos 2023 | https://holodex-prod-bucket.b-cdn.net/sets/mc12/logo.webp | 0 / 15 | holodex |
| Pokémon | McDonald's Promos 2024 | https://holodex-prod-bucket.b-cdn.net/sets/mc13/logo.webp | 0 / 15 | holodex |
| Pokémon | Miscellaneous Cards & Products | https://holodex-prod-bucket.b-cdn.net/sets/mcap/logo.webp | 293 / 883 | holodex |
| Pokémon | My First Battle | https://holodex-prod-bucket.b-cdn.net/sets/sv1723330/logo.webp | 48 / 48 | holodex |
| Pokémon | Mysterious Treasures | https://assets.tcgdex.net/en/dp/dp2/logo.webp | 124 / 124 | tcgdex |
| Pokémon | Neo Destiny | https://assets.tcgdex.net/en/neo/neo4/logo.webp | 113 / 113 | tcgdex |
| Pokémon | Neo Discovery | https://assets.tcgdex.net/en/neo/neo2/logo.webp | 75 / 75 | tcgdex |
| Pokémon | Neo Genesis | https://assets.tcgdex.net/en/neo/neo1/logo.webp | 111 / 111 | tcgdex |
| Pokémon | Neo Revelation | https://assets.tcgdex.net/en/neo/neo3/logo.webp | 66 / 66 | tcgdex |
| Pokémon | Next Destinies | https://assets.tcgdex.net/en/bw/bw4/logo.webp | 111 / 111 | tcgdex |
| Pokémon | Nintendo Promos | https://holodex-prod-bucket.b-cdn.net/sets/ninpro/logo.webp | 95 / 95 | holodex |
| Pokémon | Noble Victories | https://assets.tcgdex.net/en/bw/bw3/logo.webp | 110 / 110 | tcgdex |
| Pokémon | POP Series 1 | https://assets.tcgdex.net/en/pop/pop1/logo.webp | 19 / 19 | tcgdex |
| Pokémon | POP Series 2 | https://assets.tcgdex.net/en/pop/pop2/logo.webp | 18 / 18 | tcgdex |
| Pokémon | POP Series 3 | https://assets.tcgdex.net/en/pop/pop3/logo.webp | 18 / 18 | tcgdex |
| Pokémon | POP Series 4 | https://assets.tcgdex.net/en/pop/pop4/logo.webp | 17 / 17 | tcgdex |
| Pokémon | POP Series 5 | https://assets.tcgdex.net/en/pop/pop5/logo.webp | 17 / 17 | tcgdex |
| Pokémon | POP Series 6 | https://assets.tcgdex.net/en/pop/pop6/logo.webp | 18 / 18 | tcgdex |
| Pokémon | POP Series 7 | https://assets.tcgdex.net/en/pop/pop7/logo.webp | 17 / 17 | tcgdex |
| Pokémon | POP Series 8 | https://assets.tcgdex.net/en/pop/pop8/logo.webp | 18 / 18 | tcgdex |
| Pokémon | POP Series 9 | https://assets.tcgdex.net/en/pop/pop9/logo.webp | 18 / 18 | tcgdex |
| Pokémon | Pikachu World Collection Promos |  | 19 / 19 | — |
| Pokémon | Plasma Blast | https://assets.tcgdex.net/en/bw/bw10/logo.webp | 109 / 109 | tcgdex |
| Pokémon | Plasma Freeze | https://assets.tcgdex.net/en/bw/bw9/logo.webp | 123 / 123 | tcgdex |
| Pokémon | Plasma Storm | https://assets.tcgdex.net/en/bw/bw8/logo.webp | 141 / 141 | tcgdex |
| Pokémon | Platinum | https://assets.tcgdex.net/en/pl/pl1/logo.webp | 133 / 133 | tcgdex |
| Pokémon | Player Placement Trainer Promos |  | 4 / 4 | — |
| Pokémon | Pokemon GO | https://assets.tcgdex.net/en/swsh/swsh10.5/logo.webp | 108 / 108 | tcgdex |
| Pokémon | Prize Pack Series Cards | https://holodex-prod-bucket.b-cdn.net/sets/swsh1822880/logo.webp | 830 / 882 | holodex |
| Pokémon | Professor Program Promos |  | 56 / 70 | — |
| Pokémon | Rising Rivals | https://assets.tcgdex.net/en/pl/pl2/logo.webp | 120 / 120 | tcgdex |
| Pokémon | Rumble | https://holodex-prod-bucket.b-cdn.net/sets/pl5/logo.webp | 16 / 16 | holodex |
| Pokémon | SM - Burning Shadows | https://assets.tcgdex.net/en/sm/sm3/logo.webp | 188 / 188 | tcgdex |
| Pokémon | SM - Celestial Storm | https://assets.tcgdex.net/en/sm/sm7/logo.webp | 199 / 199 | tcgdex |
| Pokémon | SM - Cosmic Eclipse | https://assets.tcgdex.net/en/sm/sm12/logo.webp | 280 / 281 | tcgdex |
| Pokémon | SM - Crimson Invasion | https://assets.tcgdex.net/en/sm/sm4/logo.webp | 140 / 140 | tcgdex |
| Pokémon | SM - Forbidden Light | https://assets.tcgdex.net/en/sm/sm6/logo.webp | 158 / 158 | tcgdex |
| Pokémon | SM - Guardians Rising | https://assets.tcgdex.net/en/sm/sm2/logo.webp | 202 / 202 | tcgdex |
| Pokémon | SM - Lost Thunder | https://assets.tcgdex.net/en/sm/sm8/logo.webp | 251 / 251 | tcgdex |
| Pokémon | SM - Team Up | https://assets.tcgdex.net/en/sm/sm9/logo.webp | 222 / 222 | tcgdex |
| Pokémon | SM - Ultra Prism | https://assets.tcgdex.net/en/sm/sm5/logo.webp | 189 / 189 | tcgdex |
| Pokémon | SM - Unbroken Bonds | https://assets.tcgdex.net/en/sm/sm10/logo.webp | 250 / 250 | tcgdex |
| Pokémon | SM - Unified Minds | https://assets.tcgdex.net/en/sm/sm11/logo.webp | 274 / 274 | tcgdex |
| Pokémon | SM Base Set | https://holodex-prod-bucket.b-cdn.net/sets/sm1/logo.webp | 184 / 184 | holodex |
| Pokémon | SM Promos | https://assets.tcgdex.net/en/sm/smp/logo.webp | 333 / 333 | tcgdex |
| Pokémon | SM Trainer Kit: Alolan Sandslash & Alolan Ninetales |  | 58 / 60 | — |
| Pokémon | SM Trainer Kit: Lycanroc & Alolan Raichu |  | 56 / 61 | — |
| Pokémon | SV01: Scarlet & Violet Base Set | https://holodex-prod-bucket.b-cdn.net/sets/sv1/logo.webp | 35 / 273 | holodex |
| Pokémon | SV02: Paldea Evolved | https://assets.tcgdex.net/en/sv/sv02/logo.webp | 238 / 288 | tcgdex |
| Pokémon | SV03: Obsidian Flames | https://assets.tcgdex.net/en/sv/sv03/logo.webp | 238 / 238 | tcgdex |
| Pokémon | SV04: Paradox Rift | https://assets.tcgdex.net/en/sv/sv04/logo.webp | 226 / 278 | tcgdex |
| Pokémon | SV05: Temporal Forces | https://holodex-prod-bucket.b-cdn.net/sets/sv7/logo.webp | 231 / 231 | holodex |
| Pokémon | SV06: Twilight Masquerade | https://assets.tcgdex.net/en/sv/sv06/logo.webp | 238 / 238 | tcgdex |
| Pokémon | SV07: Stellar Crown | https://assets.tcgdex.net/en/sv/sv07/logo.webp | 187 / 187 | tcgdex |
| Pokémon | SV08: Surging Sparks | https://assets.tcgdex.net/en/sv/sv08/logo.webp | 262 / 262 | tcgdex |
| Pokémon | SV09: Journey Together | https://assets.tcgdex.net/en/sv/sv09/logo.webp | 199 / 201 | tcgdex |
| Pokémon | SV10: Destined Rivals | https://assets.tcgdex.net/en/sv/sv10/logo.webp | 256 / 256 | tcgdex |
| Pokémon | SV: Black Bolt | https://holodex-prod-bucket.b-cdn.net/sets/sv15/logo.webp | 281 / 331 | holodex |
| Pokémon | SV: Paldean Fates | https://assets.tcgdex.net/en/sv/sv04.5/logo.webp | 258 / 258 | tcgdex |
| Pokémon | SV: Prismatic Evolutions | https://assets.tcgdex.net/en/sv/sv08.5/logo.webp | 255 / 355 | tcgdex |
| Pokémon | SV: Scarlet & Violet 151 | https://assets.tcgdex.net/en/sv/sv03.5/logo.webp | 0 / 215 | tcgdex |
| Pokémon | SV: Scarlet & Violet Promo Cards | https://holodex-prod-bucket.b-cdn.net/sets/svp/logo.webp | 0 / 280 | holodex |
| Pokémon | SV: Shrouded Fable | https://assets.tcgdex.net/en/sv/sv06.5/logo.webp | 114 / 114 | tcgdex |
| Pokémon | SV: White Flare | https://holodex-prod-bucket.b-cdn.net/sets/sv16/logo.webp | 330 / 330 | holodex |
| Pokémon | SVE: Scarlet & Violet Energies |  | 0 / 40 | — |
| Pokémon | SWSH01: Sword & Shield Base Set | https://holodex-prod-bucket.b-cdn.net/sets/swsh1/logo.webp | 221 / 246 | holodex |
| Pokémon | SWSH02: Rebel Clash | https://assets.tcgdex.net/en/swsh/swsh2/logo.webp | 224 / 224 | tcgdex |
| Pokémon | SWSH03: Darkness Ablaze | https://assets.tcgdex.net/en/swsh/swsh3/logo.webp | 216 / 216 | tcgdex |
| Pokémon | SWSH04: Vivid Voltage | https://assets.tcgdex.net/en/swsh/swsh4/logo.webp | 220 / 220 | tcgdex |
| Pokémon | SWSH05: Battle Styles | https://assets.tcgdex.net/en/swsh/swsh5/logo.webp | 202 / 202 | tcgdex |
| Pokémon | SWSH06: Chilling Reign | https://assets.tcgdex.net/en/swsh/swsh6/logo.webp | 248 / 248 | tcgdex |
| Pokémon | SWSH07: Evolving Skies | https://assets.tcgdex.net/en/swsh/swsh7/logo.webp | 255 / 255 | tcgdex |
| Pokémon | SWSH08: Fusion Strike | https://assets.tcgdex.net/en/swsh/swsh8/logo.webp | 296 / 296 | tcgdex |
| Pokémon | SWSH09: Brilliant Stars | https://assets.tcgdex.net/en/swsh/swsh9/logo.webp | 206 / 206 | tcgdex |
| Pokémon | SWSH09: Brilliant Stars Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh12TG/logo.webp | 30 / 30 | holodex |
| Pokémon | SWSH10: Astral Radiance | https://assets.tcgdex.net/en/swsh/swsh10/logo.webp | 225 / 225 | tcgdex |
| Pokémon | SWSH10: Astral Radiance Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh13TG/logo.webp | 30 / 30 | holodex |
| Pokémon | SWSH11: Lost Origin | https://assets.tcgdex.net/en/swsh/swsh11/logo.webp | 227 / 233 | tcgdex |
| Pokémon | SWSH11: Lost Origin Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh15TG/logo.webp | 30 / 30 | holodex |
| Pokémon | SWSH12: Silver Tempest | https://assets.tcgdex.net/en/swsh/swsh12/logo.webp | 220 / 227 | tcgdex |
| Pokémon | SWSH12: Silver Tempest Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh16TG/logo.webp | 30 / 30 | holodex |
| Pokémon | SWSH: Crown Zenith | https://assets.tcgdex.net/en/swsh/swsh12.5/logo.webp | 141 / 181 | tcgdex |
| Pokémon | SWSH: Crown Zenith: Galarian Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh17GG/logo.webp | 70 / 70 | holodex |
| Pokémon | SWSH: Sword & Shield Promo Cards | https://holodex-prod-bucket.b-cdn.net/sets/swshp/logo.webp | 256 / 343 | holodex |
| Pokémon | Secret Wonders | https://assets.tcgdex.net/en/dp/dp3/logo.webp | 132 / 132 | tcgdex |
| Pokémon | Shining Fates | https://assets.tcgdex.net/en/swsh/swsh4.5/logo.webp | 86 / 88 | tcgdex |
| Pokémon | Shining Fates: Shiny Vault | https://holodex-prod-bucket.b-cdn.net/sets/swsh6/logo.webp | 122 / 122 | holodex |
| Pokémon | Shining Legends | https://holodex-prod-bucket.b-cdn.net/sets/sm4/logo.webp | 87 / 87 | holodex |
| Pokémon | Skyridge | https://assets.tcgdex.net/en/ecard/ecard3/logo.webp | 181 / 182 | tcgdex |
| Pokémon | Southeast Asia Exclusives |  | 0 / 35 | — |
| Pokémon | Southern Islands | https://assets.tcgdex.net/en/neo/si1/logo.webp | 18 / 18 | tcgdex |
| Pokémon | Stormfront | https://assets.tcgdex.net/en/dp/dp7/logo.webp | 106 / 106 | tcgdex |
| Pokémon | Supreme Victors | https://assets.tcgdex.net/en/pl/pl3/logo.png | 153 / 153 | tcgdex |
| Pokémon | Team Rocket | https://assets.tcgdex.net/en/base/base5/logo.webp | 83 / 83 | tcgdex |
| Pokémon | Trading Card Game Classic | https://holodex-prod-bucket.b-cdn.net/sets/cl/logo.webp | 102 / 102 | holodex |
| Pokémon | Trick or Trade BOOster Bundle | https://holodex-prod-bucket.b-cdn.net/sets/tot1/logo.webp | 15 / 30 | holodex |
| Pokémon | Trick or Trade BOOster Bundle 2023 | https://holodex-prod-bucket.b-cdn.net/sets/tot2/logo.webp | 30 / 30 | holodex |
| Pokémon | Trick or Trade BOOster Bundle 2024 | https://holodex-prod-bucket.b-cdn.net/sets/tot3/logo.webp | 30 / 30 | holodex |
| Pokémon | Triumphant | https://assets.tcgdex.net/en/hgss/hgss4/logo.webp | 104 / 104 | tcgdex |
| Pokémon | Undaunted | https://assets.tcgdex.net/en/hgss/hgss3/logo.png | 90 / 91 | tcgdex |
| Pokémon | Unleashed | https://assets.tcgdex.net/en/hgss/hgss2/logo.png | 96 / 96 | tcgdex |
| Pokémon | WoTC Promo | https://holodex-prod-bucket.b-cdn.net/sets/svp/logo.webp | 70 / 70 | holodex |
| Pokémon | World Championship Decks |  | 1662 / 1964 | — |
| Pokémon | XY - Ancient Origins | https://assets.tcgdex.net/en/xy/xy7/logo.webp | 116 / 116 | tcgdex |
| Pokémon | XY - BREAKpoint | https://assets.tcgdex.net/en/xy/xy9/logo.webp | 137 / 137 | tcgdex |
| Pokémon | XY - BREAKthrough | https://assets.tcgdex.net/en/xy/xy8/logo.webp | 192 / 192 | tcgdex |
| Pokémon | XY - Evolutions | https://assets.tcgdex.net/en/xy/xy12/logo.webp | 140 / 140 | tcgdex |
| Pokémon | XY - Fates Collide | https://assets.tcgdex.net/en/xy/xy10/logo.webp | 142 / 142 | tcgdex |
| Pokémon | XY - Flashfire | https://assets.tcgdex.net/en/xy/xy2/logo.webp | 126 / 126 | tcgdex |
| Pokémon | XY - Furious Fists | https://assets.tcgdex.net/en/xy/xy3/logo.png | 133 / 133 | tcgdex |
| Pokémon | XY - Phantom Forces | https://assets.tcgdex.net/en/xy/xy4/logo.webp | 137 / 137 | tcgdex |
| Pokémon | XY - Primal Clash | https://assets.tcgdex.net/en/xy/xy5/logo.webp | 178 / 178 | tcgdex |
| Pokémon | XY - Roaring Skies | https://assets.tcgdex.net/en/xy/xy6/logo.webp | 126 / 126 | tcgdex |
| Pokémon | XY - Steam Siege | https://assets.tcgdex.net/en/xy/xy11/logo.webp | 134 / 134 | tcgdex |
| Pokémon | XY Base Set | https://holodex-prod-bucket.b-cdn.net/sets/xy1/logo.webp | 169 / 169 | holodex |
| Pokémon | XY Promos | https://holodex-prod-bucket.b-cdn.net/sets/xyp/logo.webp | 260 / 269 | holodex |
| Pokémon | XY Trainer Kit: Bisharp & Wigglytuff |  | 0 / 61 | — |
| Pokémon | XY Trainer Kit: Latias & Latios |  | 0 / 61 | — |
| Pokémon | XY Trainer Kit: Pikachu Libre & Suicune |  | 59 / 61 | — |
| Pokémon | XY Trainer Kit: Sylveon & Noivern |  | 0 / 61 | — |
| Pokémon | e-Reader Sample Cards |  | 1 / 1 | — |

### Pokémon Japan（455 个系列，177 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Pokémon Japan | 10th Movie Commemoration Set |  | 11 / 11 | — |
| Pokémon Japan | 11th Movie Commemoration Set |  | 9 / 9 | — |
| Pokémon Japan | 64 Mario Stadium Best Photo Contest |  | 5 / 5 | — |
| Pokémon Japan | ADV Expansion Pack |  | 55 / 55 | — |
| Pokémon Japan | ADV-P Promotional cards |  | 63 / 63 | — |
| Pokémon Japan | Aqua Deck Kit |  | 33 / 33 | — |
| Pokémon Japan | Arceus LV.X Deck: Grass & Fire |  | 0 / 17 | — |
| Pokémon Japan | Arceus LV.X Deck: Lightning & Psychic |  | 0 / 17 | — |
| Pokémon Japan | Awakening Legends |  | 57 / 57 | — |
| Pokémon Japan | BK: Cobalion Battle Strength Deck |  | 16 / 16 | — |
| Pokémon Japan | BK: Terrakion Battle Strength Deck |  | 17 / 17 | — |
| Pokémon Japan | BK: Virizion Battle Strength Deck |  | 17 / 17 | — |
| Pokémon Japan | BKB: Black Kyurem-EX Battle Strength Deck |  | 18 / 18 | — |
| Pokémon Japan | BKR: Reshiram-EX Battle Strength Deck |  | 18 / 18 | — |
| Pokémon Japan | BKW: White Kyurem-EX Battle Strength Deck |  | 18 / 18 | — |
| Pokémon Japan | BKZ: Zekrom-EX Battle Strength Deck |  | 18 / 18 | — |
| Pokémon Japan | BREAK Starter Pack | https://archives.bulbagarden.net/media/upload/8/8b/20th_Anniversary_logo.png | 77 / 77 | bulbapedia |
| Pokémon Japan | BW-P Promotional cards |  | 250 / 250 | — |
| Pokémon Japan | BW1: Black Collection | https://archives.bulbagarden.net/media/upload/1/1e/BW1_Black_Collection_Box.jpg | 56 / 56 | bulbapedia |
| Pokémon Japan | BW1: White Collection | https://archives.bulbagarden.net/media/upload/3/34/BW1_White_Collection_Box.jpg | 55 / 55 | bulbapedia |
| Pokémon Japan | BW2: Red Collection | https://archives.bulbagarden.net/media/upload/1/1e/BW2_Red_Collection_Box.jpg | 71 / 72 | bulbapedia |
| Pokémon Japan | BW3: Hail Blizzard | https://archives.bulbagarden.net/media/upload/3/35/BW3_Hail_Blizzard_Box.jpg | 57 / 57 | bulbapedia |
| Pokémon Japan | BW3: Psycho Drive | https://archives.bulbagarden.net/media/upload/0/0f/BW3_Psycho_Drive_Box.jpg | 57 / 57 | bulbapedia |
| Pokémon Japan | BW4: Dark Rush | https://archives.bulbagarden.net/media/upload/4/48/BW4_Dark_Rush_Box.jpg | 76 / 76 | bulbapedia |
| Pokémon Japan | BW5: Dragon Blade | https://archives.bulbagarden.net/media/upload/b/bb/BW5_Dragon_Blade_Box.jpg | 55 / 55 | bulbapedia |
| Pokémon Japan | BW5: Dragon Blast | https://archives.bulbagarden.net/media/upload/0/0c/BW5_Dragon_Blast_Box.jpg | 55 / 55 | bulbapedia |
| Pokémon Japan | BW6: Cold Flare | https://archives.bulbagarden.net/media/upload/9/90/BW6_Cold_Flare_Box.jpg | 65 / 65 | bulbapedia |
| Pokémon Japan | BW6: Freeze Bolt | https://archives.bulbagarden.net/media/upload/e/e7/BW6_Freeze_Bolt_Box.jpg | 65 / 65 | bulbapedia |
| Pokémon Japan | BW7: Plasma Gale | https://archives.bulbagarden.net/media/upload/0/07/BW7_Plasma_Gale_Box.jpg | 79 / 79 | bulbapedia |
| Pokémon Japan | BW8: Spiral Force | https://archives.bulbagarden.net/media/upload/6/63/BW8_Spiral_Force_Box.jpg | 58 / 58 | bulbapedia |
| Pokémon Japan | BW8: Thunder Knuckle | https://archives.bulbagarden.net/media/upload/b/b2/BW8_Thunder_Knuckle_Box.jpg | 58 / 58 | bulbapedia |
| Pokémon Japan | BW9: Megalo Cannon | https://archives.bulbagarden.net/media/upload/3/3d/BW9_Megalo_Cannon_Box.jpg | 86 / 86 | bulbapedia |
| Pokémon Japan | BW: Extra Regulation Box | https://archives.bulbagarden.net/media/upload/5/57/Extra_Regulation_Box.jpg | 48 / 48 | bulbapedia |
| Pokémon Japan | Base Expansion Pack |  | 131 / 131 | — |
| Pokémon Japan | Bastiodon the Defender Half Deck | https://archives.bulbagarden.net/media/upload/1/1c/DP2_Logo_EN.png | 14 / 14 | bulbapedia |
| Pokémon Japan | Battle Academy | https://archives.bulbagarden.net/media/upload/thumb/7/76/Pokemon_TCG_Battle_Academy_Logo.png/600px-Pokemon_TCG_Battle_Academy_Logo.png | 74 / 74 | bulbapedia |
| Pokémon Japan | Battle Gift Set: Thundurus vs Tornadus |  | 20 / 20 | — |
| Pokémon Japan | Battle Road |  | 22 / 22 | — |
| Pokémon Japan | Battle Starter Deck (Blastoise) |  | 0 / 10 | — |
| Pokémon Japan | Battle Starter Deck (Magmortar) |  | 0 / 9 | — |
| Pokémon Japan | Battle Starter Deck (Raichu) |  | 0 / 11 | — |
| Pokémon Japan | Battle Starter Deck (Torterra) |  | 0 / 10 | — |
| Pokémon Japan | Battle Theme Deck: Victini |  | 21 / 21 | — |
| Pokémon Japan | Black Deck Kit |  | 20 / 20 | — |
| Pokémon Japan | Blastoise + Kyurem-EX Combo Deck |  | 0 / 18 | — |
| Pokémon Japan | CP1: Magma Gang vs Aqua Gang: Double Crisis | https://archives.bulbagarden.net/media/upload/f/f0/CP1_Logo.png | 34 / 34 | bulbapedia |
| Pokémon Japan | CP2: Legendary Shine Collection | https://archives.bulbagarden.net/media/upload/d/d6/CP2_Legendary_Shine_Collection_pack_1.jpg | 27 / 27 | bulbapedia |
| Pokémon Japan | CP3: PokeKyun Collection | https://archives.bulbagarden.net/media/upload/9/92/CP3_Pok%C3%A9Kyun_Collection_pack.jpg | 32 / 32 | bulbapedia |
| Pokémon Japan | CP4: Premium Champion Pack | https://archives.bulbagarden.net/media/upload/a/a3/CP4_Premium_Champion_Pack_pack.jpg | 140 / 140 | bulbapedia |
| Pokémon Japan | CP5: Mythical & Legendary Dream Shine Collection | https://archives.bulbagarden.net/media/upload/9/90/CP5_Mythical_Legendary_Dream_Shine_Collection_pack.jpg | 0 / 38 | bulbapedia |
| Pokémon Japan | CP6: Expansion Pack 20th Anniversary | https://archives.bulbagarden.net/media/upload/6/61/CP6_Expansion_Pack_20th_Anniversary_Box.jpg | 103 / 103 | bulbapedia |
| Pokémon Japan | CS1: Journey Partners Collection Sheet | https://archives.bulbagarden.net/media/upload/7/79/CS1.5_logo.png | 9 / 9 | bulbapedia |
| Pokémon Japan | Challenge from the Darkness |  | 99 / 99 | — |
| Pokémon Japan | Champion Road |  | 2 / 6 | — |
| Pokémon Japan | City Gym Decks |  | 124 / 124 | — |
| Pokémon Japan | Clash of the Blue Sky |  | 82 / 82 | — |
| Pokémon Japan | CoroCoro Promotional Cards |  | 51 / 51 | — |
| Pokémon Japan | Crossing the Ruins... |  | 0 / 57 | — |
| Pokémon Japan | DP-P Promotional cards |  | 126 / 127 | — |
| Pokémon Japan | DP1: Space-Time Creation | https://archives.bulbagarden.net/media/upload/0/00/DP1_Logo_BR.png | 121 / 121 | bulbapedia |
| Pokémon Japan | DP2: Secret of the Lakes | https://archives.bulbagarden.net/media/upload/1/1c/DP2_Logo_EN.png | 123 / 123 | bulbapedia |
| Pokémon Japan | DP3: Shining Darkness | https://archives.bulbagarden.net/media/upload/8/81/DP3_Logo_BR.png | 119 / 119 | bulbapedia |
| Pokémon Japan | DP4: Dawn Dash | https://archives.bulbagarden.net/media/upload/c/cc/DP4_Logo_EN.png | 65 / 65 | bulbapedia |
| Pokémon Japan | DP4: Moonlit Pursuit | https://archives.bulbagarden.net/media/upload/c/cc/DP4_Logo_EN.png | 70 / 70 | bulbapedia |
| Pokémon Japan | DP5: Cry from the Mysterious | https://archives.bulbagarden.net/media/upload/d/de/DP5_Logo_EN.png | 65 / 65 | bulbapedia |
| Pokémon Japan | DP5: Temple of Anger | https://archives.bulbagarden.net/media/upload/d/de/DP5_Logo_EN.png | 65 / 65 | bulbapedia |
| Pokémon Japan | DPt Gift Box (Chimchar) |  | 0 / 13 | — |
| Pokémon Japan | DPt Gift Box (Pikachu) |  | 0 / 10 | — |
| Pokémon Japan | DPt Gift Box (Piplup) |  | 0 / 12 | — |
| Pokémon Japan | DPt Gift Box (Turtwig) |  | 0 / 12 | — |
| Pokémon Japan | DPt-P Promotional cards |  | 51 / 51 | — |
| Pokémon Japan | Darkness, and to Light... |  | 0 / 113 | — |
| Pokémon Japan | Deoxys Constructed Starter Deck |  | 16 / 16 | — |
| Pokémon Japan | Dialga LV.X Constructed Standard Deck |  | 0 / 18 | — |
| Pokémon Japan | Dragon Selection | https://archives.bulbagarden.net/media/upload/b/b6/DS_Dragon_Selection_pack.jpg | 20 / 20 | bulbapedia |
| Pokémon Japan | EX Battle Boost | https://archives.bulbagarden.net/media/upload/b/b2/EBB_EX_Battle_Boost_Box.jpg | 186 / 187 | bulbapedia |
| Pokémon Japan | Earth's Groudon ex Constructed Starter Deck |  | 0 / 16 | — |
| Pokémon Japan | Elementary School Competition |  | 4 / 4 | — |
| Pokémon Japan | Emerald Gift Box (Deoxys) |  | 0 / 19 | — |
| Pokémon Japan | Emerald Gift Box (Rayquaza) |  | 0 / 19 | — |
| Pokémon Japan | Entry Pack | https://archives.bulbagarden.net/media/upload/0/00/DP1_Logo_BR.png | 12 / 28 | bulbapedia |
| Pokémon Japan | Entry Pack '08 | https://archives.bulbagarden.net/media/upload/3/3c/DP-DS-box.png | 24 / 42 | bulbapedia |
| Pokémon Japan | Entry Pack DPt (Dialga) |  | 3 / 13 | — |
| Pokémon Japan | Entry Pack DPt (Giratina) |  | 5 / 13 | — |
| Pokémon Japan | Entry Pack DPt (Palkia) |  | 6 / 13 | — |
| Pokémon Japan | Everyone's Exciting Battle |  | 0 / 47 | — |
| Pokémon Japan | Expansion Pack |  | 93 / 102 | — |
| Pokémon Japan | Expansion Pack (No Rarity) |  | 1 / 96 | — |
| Pokémon Japan | Feraligatr Constructed Starter Deck |  | 16 / 16 | — |
| Pokémon Japan | Fighting Quick Construction Pack |  | 15 / 15 | — |
| Pokémon Japan | Fire Quick Construction Pack |  | 15 / 15 | — |
| Pokémon Japan | Flight of Legends |  | 82 / 82 | — |
| Pokémon Japan | Flygon Constructed Starter Deck |  | 20 / 20 | — |
| Pokémon Japan | Garchomp Half Deck |  | 15 / 15 | — |
| Pokémon Japan | Garchomp vs Charizard SP Deck Kit (Charizard) |  | 16 / 16 | — |
| Pokémon Japan | Garchomp vs Charizard SP Deck Kit (Garchomp) |  | 13 / 13 | — |
| Pokémon Japan | Gift Box (Latias) |  | 0 / 18 | — |
| Pokémon Japan | Gift Box (Latios) |  | 0 / 18 | — |
| Pokémon Japan | Gift Box Mew - Lucario (Crawdaunt Quarter Deck) |  | 0 / 15 | — |
| Pokémon Japan | Gift Box Mew - Lucario (Lucario Quarter Deck) |  | 0 / 15 | — |
| Pokémon Japan | Gift Box Mew - Lucario (Mew Quarter Deck) |  | 0 / 15 | — |
| Pokémon Japan | Gift Box Mew - Lucario (Mightyena Quarter Deck) |  | 0 / 15 | — |
| Pokémon Japan | Gift Box Mew - Lucario (Pokemon Star) |  | 0 / 2 | — |
| Pokémon Japan | Giratina vs Dialga Deck Kit (Dialga) |  | 14 / 14 | — |
| Pokémon Japan | Giratina vs Dialga Deck Kit (Giratina) |  | 14 / 14 | — |
| Pokémon Japan | Gold, Silver, to a New World... |  | 0 / 96 | — |
| Pokémon Japan | Golden Sky, Silvery Ocean |  | 106 / 106 | — |
| Pokémon Japan | Grass Quick Construction Pack |  | 15 / 15 | — |
| Pokémon Japan | Gym Challenge | https://archives.bulbagarden.net/media/upload/thumb/e/e0/Gym_Challenge_Logo.png/600px-Gym_Challenge_Logo.png | 21 / 21 | bulbapedia |
| Pokémon Japan | HS: Beginning Set |  | 0 / 1 | — |
| Pokémon Japan | HSP: Beginning Set Pikachu Version |  | 0 / 1 | — |
| Pokémon Japan | HSZ: National Beginning Set |  | 0 / 34 | — |
| Pokémon Japan | Heatran vs Regigigas Deck Kit | https://archives.bulbagarden.net/media/upload/d/de/DP5_Logo_EN.png | 23 / 23 | bulbapedia |
| Pokémon Japan | Holon Phantom |  | 52 / 52 | — |
| Pokémon Japan | Holon Research Tower |  | 74 / 86 | — |
| Pokémon Japan | Holon Research Tower Fire Quarter Deck |  | 15 / 15 | — |
| Pokémon Japan | Holon Research Tower Lightning Quarter Deck |  | 14 / 14 | — |
| Pokémon Japan | Holon Research Tower Water Quarter Deck |  | 15 / 15 | — |
| Pokémon Japan | How I Became a Pokemon Card |  | 6 / 6 | — |
| Pokémon Japan | Hydreigon Half Deck |  | 15 / 15 | — |
| Pokémon Japan | Imprison! Gardevoir ex Constructed Standard Deck |  | 0 / 24 | — |
| Pokémon Japan | Infernape vs Gallade SP Deck Kit (Gallade) |  | 12 / 12 | — |
| Pokémon Japan | Infernape vs Gallade SP Deck Kit (Infernape) |  | 18 / 18 | — |
| Pokémon Japan | Intense Fight in the Destroyed Sky |  | 42 / 92 | — |
| Pokémon Japan | Intro Pack (Bulbasaur) |  | 0 / 41 | — |
| Pokémon Japan | Intro Pack (Squirtle) |  | 0 / 41 | — |
| Pokémon Japan | Intro Pack Neo (Chikorita) |  | 0 / 40 | — |
| Pokémon Japan | Intro Pack Neo (Totodile) |  | 0 / 40 | — |
| Pokémon Japan | J Promotional cards |  | 2 / 2 | — |
| Pokémon Japan | Japanese CD Promo |  | 4 / 4 | — |
| Pokémon Japan | Keldeo Battle Strength Deck |  | 15 / 15 | — |
| Pokémon Japan | L-P: Legends Promos |  | 79 / 79 | — |
| Pokémon Japan | L1: HeartGold Collection |  | 143 / 141 | — |
| Pokémon Japan | L1: SoulSilver Collection |  | 141 / 141 | — |
| Pokémon Japan | L2: Revival Legends | https://archives.bulbagarden.net/media/upload/6/64/L2_Logo.png | 160 / 161 | bulbapedia |
| Pokémon Japan | L2: Steelix Constructed Standard Deck | https://archives.bulbagarden.net/media/upload/6/64/L2_Logo.png | 19 / 19 | bulbapedia |
| Pokémon Japan | L2: Tyranitar Constructed Standard Deck | https://archives.bulbagarden.net/media/upload/6/64/L2_Logo.png | 19 / 19 | bulbapedia |
| Pokémon Japan | L3: Clash at the Summit | https://archives.bulbagarden.net/media/upload/5/59/L3_Logo.png | 161 / 161 | bulbapedia |
| Pokémon Japan | LEGEND Era Unnumbered Energies |  | 0 / 8 | — |
| Pokémon Japan | LL: Lost Link | https://archives.bulbagarden.net/media/upload/0/03/LL_Lost_Link_pack.jpg | 40 / 40 | bulbapedia |
| Pokémon Japan | Leaders' Stadium |  | 0 / 96 | — |
| Pokémon Japan | Leafeon vs Metagross Expert Deck (Leafeon) | https://archives.bulbagarden.net/media/upload/6/62/E-Reader_logo.png | 15 / 15 | bulbapedia |
| Pokémon Japan | Leafeon vs Metagross Expert Deck (Metagross) | https://archives.bulbagarden.net/media/upload/6/62/E-Reader_logo.png | 14 / 14 | bulbapedia |
| Pokémon Japan | Lightning Quick Construction Pack |  | 15 / 15 | — |
| Pokémon Japan | M Master Deck Build Box Power Style | https://archives.bulbagarden.net/media/upload/thumb/3/31/M_Master_Deck_Build_Box_Power_Style.jpg/600px-M_Master_Deck_Build_Box_Power_Style.jpg | 58 / 58 | bulbapedia |
| Pokémon Japan | M Master Deck Build Box Speed Style | https://archives.bulbagarden.net/media/upload/thumb/8/87/M_Master_Deck_Build_Box_Speed_Style.jpg/600px-M_Master_Deck_Build_Box_Speed_Style.jpg | 57 / 57 | bulbapedia |
| Pokémon Japan | M-P Promotional Cards |  | 60 / 67 | — |
| Pokémon Japan | M2: Inferno X | https://archives.bulbagarden.net/media/upload/e/e0/M2_Inferno_X_pack.png | 116 / 116 | bulbapedia |
| Pokémon Japan | M2a: High Class Pack: MEGA Dream ex | https://archives.bulbagarden.net/media/upload/2/28/M2a_Logo_JP.png | 485 / 486 | bulbapedia |
| Pokémon Japan | M3: Nihil Zero | https://archives.bulbagarden.net/media/upload/9/92/M3_Nihil_Zero_pack.png | 117 / 117 | bulbapedia |
| Pokémon Japan | M4: Ninja Spinner | https://archives.bulbagarden.net/media/upload/5/5b/M4_Ninja_Spinner_pack.png | 120 / 120 | bulbapedia |
| Pokémon Japan | M5: Abyss Eye | https://archives.bulbagarden.net/media/upload/4/4a/M5_Abyss_Eye_pack.png | 118 / 118 | bulbapedia |
| Pokémon Japan | M6: Storm Emeralda | https://archives.bulbagarden.net/media/upload/4/4f/M6_Storm_Emeralda_pack.png | 116 / 116 | bulbapedia |
| Pokémon Japan | M6a: MEGA Expansion 30th Celebration |  | 0 / 176 | — |
| Pokémon Japan | MBD: MEGA Starter Set Mega Diancie ex | https://archives.bulbagarden.net/media/upload/9/91/MEGA_Starter_Set_Mega_Diancie_ex_box.jpg | 22 / 22 | bulbapedia |
| Pokémon Japan | MBG: MEGA Starter Set Mega Gengar ex | https://archives.bulbagarden.net/media/upload/f/f6/MEGA_Starter_Set_Mega_Gengar_ex_box.jpg | 22 / 22 | bulbapedia |
| Pokémon Japan | MEE: Starter Set ex Eevee ex |  | 20 / 20 | — |
| Pokémon Japan | MEM: Starter Set ex Meowscarada ex |  | 18 / 18 | — |
| Pokémon Japan | MEZ: Starter Set ex Zoroark ex |  | 20 / 20 | — |
| Pokémon Japan | MF: 30th CELEBRATION Premium Deck Set Espeon & Umbreon |  | 0 / 49 | — |
| Pokémon Japan | MP1: Start Deck 100 Battle Collection CoroCiao Version |  | 23 / 23 | — |
| Pokémon Japan | Magma Deck Kit |  | 33 / 33 | — |
| Pokémon Japan | Magma VS Aqua: Two Ambitions |  | 80 / 80 | — |
| Pokémon Japan | Magmortar vs Electivire Deck Kit | https://archives.bulbagarden.net/media/upload/c/cc/DP4_Logo_EN.png | 26 / 26 | bulbapedia |
| Pokémon Japan | Master Deck Build Box EX | https://archives.bulbagarden.net/media/upload/thumb/a/a9/MasterDeckBuildBoxEX.jpg/600px-MasterDeckBuildBoxEX.jpg | 46 / 46 | bulbapedia |
| Pokémon Japan | Master Kit (Bulbasaur) |  | 0 / 9 | — |
| Pokémon Japan | Master Kit (Side Deck) |  | 0 / 10 | — |
| Pokémon Japan | Master Kit (Torchic) |  | 0 / 11 | — |
| Pokémon Japan | McDonald's Pokémon-e Minimum Pack |  | 0 / 24 | — |
| Pokémon Japan | Mega Evolution Era Unnumbered Energies |  | 0 / 4 | — |
| Pokémon Japan | Meganium Constructed Starter Deck |  | 16 / 16 | — |
| Pokémon Japan | Melee! Pokemon Scramble |  | 0 / 19 | — |
| Pokémon Japan | Metagross Constructed Starter Deck |  | 19 / 19 | — |
| Pokémon Japan | Mewtwo vs Genesect Deck Kit (Genesect) |  | 16 / 16 | — |
| Pokémon Japan | Mewtwo vs Genesect Deck Kit (Mewtwo) |  | 16 / 16 | — |
| Pokémon Japan | Miracle Crystal |  | 75 / 75 | — |
| Pokémon Japan | Miracle of the Desert |  | 53 / 53 | — |
| Pokémon Japan | Mirage Forest |  | 86 / 86 | — |
| Pokémon Japan | Mirage's Mew Constructed Starter Deck |  | 0 / 17 | — |
| Pokémon Japan | Movie Commemoration Random Pack |  | 22 / 22 | — |
| Pokémon Japan | Movie Commemoration VS Pack | https://archives.bulbagarden.net/media/upload/4/49/Lucario_Movie_Commemoration_VS_Pack.jpg | 11 / 19 | bulbapedia |
| Pokémon Japan | Movie Commemoration VS Pack: Aura's Lucario | https://archives.bulbagarden.net/media/upload/4/49/Lucario_Movie_Commemoration_VS_Pack.jpg | 16 / 20 | bulbapedia |
| Pokémon Japan | Movie Commemoration VS Pack: Sea's Manaphy | https://archives.bulbagarden.net/media/upload/5/56/Manaphy_Movie_Commemoration_VS_Pack.jpg | 12 / 19 | bulbapedia |
| Pokémon Japan | Movie Commemoration VS Pack: Sky-Splitting Deoxys | https://archives.bulbagarden.net/media/upload/6/6f/Deoxys_Movie_Commemoration_VS_Pack.jpg | 20 / 20 | bulbapedia |
| Pokémon Japan | Mudkip Constructed Starter Deck |  | 20 / 20 | — |
| Pokémon Japan | Mysterious Mountains |  | 91 / 91 | — |
| Pokémon Japan | Mystery of the Fossils |  | 48 / 48 | — |
| Pokémon Japan | Neo Premium File 1 |  | 9 / 9 | — |
| Pokémon Japan | Neo Premium File 2 |  | 9 / 9 | — |
| Pokémon Japan | Neo Premium File 3 |  | 9 / 9 | — |
| Pokémon Japan | Ocean's Kyogre ex Constructed Starter Deck |  | 0 / 16 | — |
| Pokémon Japan | Offense and Defense of the Furthest Ends |  | 68 / 68 | — |
| Pokémon Japan | P Promotional cards |  | 1 / 47 | — |
| Pokémon Japan | PCG-P Promotional cards |  | 155 / 155 | — |
| Pokémon Japan | PLAY Promotional cards |  | 32 / 32 | — |
| Pokémon Japan | PPP Promotional cards |  | 7 / 7 | — |
| Pokémon Japan | Palkia LV.X Constructed Standard Deck |  | 0 / 19 | — |
| Pokémon Japan | Player Placement Trainer Promos |  | 2 / 2 | — |
| Pokémon Japan | PokePark Blue |  | 9 / 9 | — |
| Pokémon Japan | PokePark Forest |  | 9 / 9 | — |
| Pokémon Japan | Pokemon Card Design Contest |  | 6 / 6 | — |
| Pokémon Japan | Pokemon Card Fan Club |  | 10 / 10 | — |
| Pokémon Japan | Pokemon Card Information Promotional cards |  | 3 / 3 | — |
| Pokémon Japan | Pokemon Jungle |  | 48 / 48 | — |
| Pokémon Japan | Pokemon TCG Classic: Blastoise |  | 34 / 34 | — |
| Pokémon Japan | Pokemon TCG Classic: Charizard |  | 34 / 34 | — |
| Pokémon Japan | Pokemon TCG Classic: Venusaur |  | 34 / 34 | — |
| Pokémon Japan | Pokemon VS |  | 151 / 152 | — |
| Pokémon Japan | Pokemon Web |  | 47 / 47 | — |
| Pokémon Japan | Pokemon-e Starter Deck |  | 29 / 29 | — |
| Pokémon Japan | Psychic Quick Construction Pack |  | 15 / 15 | — |
| Pokémon Japan | Pt1: Galactic's Conquest |  | 0 / 96 | — |
| Pokémon Japan | Pt2: Bonds to the End of Time |  | 90 / 90 | — |
| Pokémon Japan | Pt3: Beat of the Frontier |  | 100 / 100 | — |
| Pokémon Japan | Pt4: Advent of Arceus |  | 90 / 90 | — |
| Pokémon Japan | PtM: Mewtwo LV.X Collection Pack |  | 0 / 12 | — |
| Pokémon Japan | PtR: Regigigas LV.X Collection Pack |  | 0 / 12 | — |
| Pokémon Japan | PtS: Shaymin LV.X Collection Pack |  | 0 / 12 | — |
| Pokémon Japan | Quick Starter Gift Set (Green Deck) |  | 0 / 26 | — |
| Pokémon Japan | Quick Starter Gift Set (Red Deck) |  | 0 / 24 | — |
| Pokémon Japan | Rampardos the Attacker Constructed Half Deck | https://archives.bulbagarden.net/media/upload/1/1c/DP2_Logo_EN.png | 15 / 15 | bulbapedia |
| Pokémon Japan | Random Constructed Starter Decks (Venusaur/Charizard/Blastoise) |  | 0 / 52 | — |
| Pokémon Japan | Rayquaza Constructed Starter Deck |  | 16 / 16 | — |
| Pokémon Japan | Rocket Gang |  | 65 / 65 | — |
| Pokémon Japan | Rocket Gang Strikes Back |  | 85 / 85 | — |
| Pokémon Japan | Rulers of the Heavens |  | 54 / 54 | — |
| Pokémon Japan | S-P: Sword & Shield Promos |  | 0 / 344 | — |
| Pokémon Japan | S10D: Time Gazer | https://archives.bulbagarden.net/media/upload/1/1a/S10D_Time_Gazer_Booster_Chinese.png | 87 / 88 | bulbapedia |
| Pokémon Japan | S10P: Space Juggler | https://archives.bulbagarden.net/media/upload/6/68/S10P_Space_Juggler_Booster_Chinese.png | 87 / 88 | bulbapedia |
| Pokémon Japan | S10a: Dark Phantasma | https://archives.bulbagarden.net/media/upload/f/f7/S10a_Dark_Phantasma_Logo.png | 147 / 148 | bulbapedia |
| Pokémon Japan | S10b: Pokemon GO | https://archives.bulbagarden.net/media/upload/1/1f/S10b_Pok%C3%A9mon_GO_Booster_Chinese.jpg | 104 / 104 | bulbapedia |
| Pokémon Japan | S11: Lost Abyss | https://archives.bulbagarden.net/media/upload/6/66/S11_Lost_Abyss_Booster_Chinese.png | 127 / 127 | bulbapedia |
| Pokémon Japan | S11a: Incandescent Arcana | https://archives.bulbagarden.net/media/upload/6/60/S11a_Incandescent_Arcana_Logo.png | 140 / 140 | bulbapedia |
| Pokémon Japan | S12: Paradigm Trigger | https://archives.bulbagarden.net/media/upload/a/a7/S12_Paradigm_Trigger_Booster_Chinese.png | 125 / 125 | bulbapedia |
| Pokémon Japan | S12a: VSTAR Universe | https://archives.bulbagarden.net/media/upload/4/42/S12a_VSTAR_Universe_Logo.png | 349 / 351 | bulbapedia |
| Pokémon Japan | S1H: Shield | https://archives.bulbagarden.net/media/upload/8/87/S1H_Shield_pack.jpg | 75 / 75 | bulbapedia |
| Pokémon Japan | S1W: Sword | https://archives.bulbagarden.net/media/upload/8/8e/S1W_Sword_pack.jpg | 75 / 75 | bulbapedia |
| Pokémon Japan | S1a: VMAX Rising | https://archives.bulbagarden.net/media/upload/b/ba/S1a_VMAX_Rising_Box.jpg | 86 / 86 | bulbapedia |
| Pokémon Japan | S2: Rebellion Crash | https://archives.bulbagarden.net/media/upload/7/75/S2_Rebellion_Crash_pack.jpg | 113 / 115 | bulbapedia |
| Pokémon Japan | S2a: Explosive Walker | https://archives.bulbagarden.net/media/upload/b/b9/S2a_Explosive_Walker_pack.jpg | 86 / 86 | bulbapedia |
| Pokémon Japan | S3: Infinity Zone | https://archives.bulbagarden.net/media/upload/9/9d/S3_Infinity_Zone_pack.jpg | 116 / 119 | bulbapedia |
| Pokémon Japan | S3a: Legendary Heartbeat | https://archives.bulbagarden.net/media/upload/f/f7/S3a_Legendary_Heartbeat_pack.jpg | 94 / 94 | bulbapedia |
| Pokémon Japan | S4: Amazing Volt Tackle | https://archives.bulbagarden.net/media/upload/e/e4/S4_Amazing_Volt_Tackle_Booster_Chinese.jpg | 121 / 121 | bulbapedia |
| Pokémon Japan | S4a: Shiny Star V | https://archives.bulbagarden.net/media/upload/c/ca/S4a_Shiny_Star_V_Booster_Chinese.jpg | 433 / 454 | bulbapedia |
| Pokémon Japan | S5I: Single Strike Master | https://archives.bulbagarden.net/media/upload/9/95/S5I_Single_Strike_Master_Booster_Chinese.jpg | 91 / 91 | bulbapedia |
| Pokémon Japan | S5R: Rapid Strike Master | https://archives.bulbagarden.net/media/upload/b/bf/S5R_Rapid_Strike_Master_Booster_Chinese.jpg | 91 / 91 | bulbapedia |
| Pokémon Japan | S5a: Peerless Fighters | https://archives.bulbagarden.net/media/upload/5/50/S5a_Peerless_Fighters_Logo.png | 95 / 96 | bulbapedia |
| Pokémon Japan | S6H: Silver Lance | https://archives.bulbagarden.net/media/upload/3/30/S6H_Silver_Lance_Booster_Indonesian.png | 95 / 95 | bulbapedia |
| Pokémon Japan | S6K: Jet-Black Spirit | https://archives.bulbagarden.net/media/upload/2/26/S6K_Jet-Black_Spirit_Booster_Indonesian.png | 93 / 95 | bulbapedia |
| Pokémon Japan | S6a: Eevee Heroes | https://archives.bulbagarden.net/media/upload/1/1f/S6a_Eevee_Heroes_Logo.png | 101 / 101 | bulbapedia |
| Pokémon Japan | S7D: Skyscraping Perfection | https://archives.bulbagarden.net/media/upload/0/06/S7D_Skyscraping_Perfection_Booster_Chinese.png | 90 / 90 | bulbapedia |
| Pokémon Japan | S7R: Blue Sky Stream | https://archives.bulbagarden.net/media/upload/e/eb/S7R_Blue_Sky_Stream_Booster_Chinese.png | 50 / 90 | bulbapedia |
| Pokémon Japan | S8: Fusion Arts | https://archives.bulbagarden.net/media/upload/e/e6/S8_Fusion_Arts_Booster_Chinese.png | 128 / 129 | bulbapedia |
| Pokémon Japan | S8a: 25th Anniversary Collection | https://archives.bulbagarden.net/media/upload/a/a3/S8a_25th_Anniversary_Collection_Logo.png | 55 / 55 | bulbapedia |
| Pokémon Japan | S8b: VMAX Climax | https://archives.bulbagarden.net/media/upload/4/4d/S8b_VMAX_Climax_Logo.png | 396 / 403 | bulbapedia |
| Pokémon Japan | S9: Star Birth | https://archives.bulbagarden.net/media/upload/8/8e/S9_Star_Birth_Booster_Chinese.png | 126 / 127 | bulbapedia |
| Pokémon Japan | S9a: Battle Region | https://archives.bulbagarden.net/media/upload/c/cb/S9a_Battle_Region_Logo.png | 137 / 138 | bulbapedia |
| Pokémon Japan | SI: Start Deck 100 |  | 513 / 522 | — |
| Pokémon Japan | SM-P: Sun & Moon Promos |  | 0 / 413 | — |
| Pokémon Japan | SM0: Pikachu's New Friends |  | 0 / 4 | — |
| Pokémon Japan | SM1+: Sun & Moon |  | 0 / 1 | — |
| Pokémon Japan | SM10: Double Blaze | https://archives.bulbagarden.net/media/upload/c/cd/SM10_Double_Blaze_pack.jpg | 116 / 116 | bulbapedia |
| Pokémon Japan | SM10a: GG End | https://archives.bulbagarden.net/media/upload/5/51/SM10a_GG_End_Box.jpg | 69 / 69 | bulbapedia |
| Pokémon Japan | SM10b: Sky Legend | https://archives.bulbagarden.net/media/upload/f/f9/SM10b_Sky_Legend_Box.jpg | 69 / 69 | bulbapedia |
| Pokémon Japan | SM11: Miracle Twin | https://archives.bulbagarden.net/media/upload/4/46/SM11_Miracle_Twin_Box.jpg | 115 / 115 | bulbapedia |
| Pokémon Japan | SM11a: Remix Bout | https://archives.bulbagarden.net/media/upload/a/a7/SM11a_Remix_Bout_Box.jpg | 80 / 80 | bulbapedia |
| Pokémon Japan | SM11b: Dream League | https://archives.bulbagarden.net/media/upload/9/98/SM11b_Dream_League_Box.jpg | 75 / 75 | bulbapedia |
| Pokémon Japan | SM12: Alter Genesis | https://archives.bulbagarden.net/media/upload/0/07/SM12_Alter_Genesis_Box.jpg | 117 / 117 | bulbapedia |
| Pokémon Japan | SM12a: TAG TEAM GX: Tag All Stars | https://archives.bulbagarden.net/media/upload/4/44/SM12a_Logo.png | 342 / 353 | bulbapedia |
| Pokémon Japan | SM1M: Collection Moon |  | 73 / 73 | — |
| Pokémon Japan | SM1S: Collection Sun |  | 73 / 73 | — |
| Pokémon Japan | SM2+: Facing a New Trial |  | 0 / 70 | — |
| Pokémon Japan | SM2K: Islands Await You | https://archives.bulbagarden.net/media/upload/3/31/SM2K_Islands_Await_You_Box.jpg | 62 / 62 | bulbapedia |
| Pokémon Japan | SM2L: Alolan Moonlight | https://archives.bulbagarden.net/media/upload/3/3d/SM2L_Alolan_Moonlight_Box.jpg | 62 / 62 | bulbapedia |
| Pokémon Japan | SM3+: Shining Legends |  | 0 / 82 | — |
| Pokémon Japan | SM3H: To Have Seen the Battle Rainbow | https://archives.bulbagarden.net/media/upload/7/72/SM3H_To_Have_Seen_the_Battle_Rainbow_Box.jpg | 64 / 64 | bulbapedia |
| Pokémon Japan | SM3N: Darkness that Consumes Light | https://archives.bulbagarden.net/media/upload/5/54/SM3N_Darkness_that_Consumes_Light_Box.jpg | 64 / 64 | bulbapedia |
| Pokémon Japan | SM4+: GX Battle Boost |  | 0 / 125 | — |
| Pokémon Japan | SM4A: Ultradimensional Beasts | https://archives.bulbagarden.net/media/upload/9/91/SM4A_Ultradimensional_Beasts_Box.jpg | 62 / 62 | bulbapedia |
| Pokémon Japan | SM4S: Awakened Heroes | https://archives.bulbagarden.net/media/upload/d/db/SM4S_Awakened_Heroes_Box.jpg | 62 / 62 | bulbapedia |
| Pokémon Japan | SM5+: Ultra Force |  | 0 / 68 | — |
| Pokémon Japan | SM5M: Ultra Moon | https://archives.bulbagarden.net/media/upload/7/7c/SM5M_Ultra_Moon_Box.jpg | 78 / 78 | bulbapedia |
| Pokémon Japan | SM5S: Ultra Sun | https://archives.bulbagarden.net/media/upload/d/d9/SM5S_Ultra_Sun_Box.jpg | 78 / 78 | bulbapedia |
| Pokémon Japan | SM6: Forbidden Light | https://archives.bulbagarden.net/media/upload/2/2f/SM6_Forbidden_Light_Box.jpg | 108 / 110 | bulbapedia |
| Pokémon Japan | SM6a: Dragon Storm | https://archives.bulbagarden.net/media/upload/8/87/SM6a_Dragon_Storm_pack.jpg | 66 / 66 | bulbapedia |
| Pokémon Japan | SM6b: Champion Road | https://archives.bulbagarden.net/media/upload/6/6f/SM6b_Champion_Road_Box.jpg | 86 / 86 | bulbapedia |
| Pokémon Japan | SM7: Sky-Splitting Charisma | https://archives.bulbagarden.net/media/upload/5/50/SM7_Sky-Splitting_Charisma_Box.jpg | 112 / 112 | bulbapedia |
| Pokémon Japan | SM7a: Thunderclap Spark | https://archives.bulbagarden.net/media/upload/8/8e/SM7a_Thunderclap_Spark_Box.jpg | 73 / 73 | bulbapedia |
| Pokémon Japan | SM7b: Fairy Rise | https://archives.bulbagarden.net/media/upload/9/9e/SM7b_Fairy_Rise_Box.jpg | 63 / 63 | bulbapedia |
| Pokémon Japan | SM8: Super-Burst Impact | https://archives.bulbagarden.net/media/upload/9/91/SM8_Super-Burst_Impact_Box.jpg | 111 / 111 | bulbapedia |
| Pokémon Japan | SM8a: Dark Order | https://archives.bulbagarden.net/media/upload/5/50/SM8a_Dark_Order_pack.jpg | 65 / 65 | bulbapedia |
| Pokémon Japan | SM8b: GX Ultra Shiny | https://archives.bulbagarden.net/media/upload/3/3b/SM8b_GX_Ultra_Shiny_Box.jpg | 371 / 375 | bulbapedia |
| Pokémon Japan | SM9: Tag Bolt | https://archives.bulbagarden.net/media/upload/9/93/SM9_Tag_Bolt_Box.jpg | 118 / 118 | bulbapedia |
| Pokémon Japan | SM9a: Night Unison | https://archives.bulbagarden.net/media/upload/9/9b/SM9a_Night_Unison_Box.jpg | 70 / 70 | bulbapedia |
| Pokémon Japan | SM9b: Full Metal Wall | https://archives.bulbagarden.net/media/upload/3/32/SM9b_Full_Metal_Wall_Box.jpg | 69 / 69 | bulbapedia |
| Pokémon Japan | SM: The Best of XY | https://archives.bulbagarden.net/media/upload/b/b5/The_Best_of_XY_Logo.png | 315 / 323 | bulbapedia |
| Pokémon Japan | SNP: Noivern BREAK Evolution Pack | https://archives.bulbagarden.net/media/upload/thumb/8/85/Noivern_BREAK_Evolution_Pack.jpg/600px-Noivern_BREAK_Evolution_Pack.jpg | 10 / 10 | bulbapedia |
| Pokémon Japan | SNP: Raichu BREAK Evolution Pack | https://archives.bulbagarden.net/media/upload/thumb/d/d5/Raichu_BREAK_Evolution_Pack.jpg/600px-Raichu_BREAK_Evolution_Pack.jpg | 10 / 10 | bulbapedia |
| Pokémon Japan | SS: Gengar VMAX High-Class Deck |  | 20 / 20 | — |
| Pokémon Japan | SS: Inteleon VMAX High-Class Deck |  | 23 / 23 | — |
| Pokémon Japan | SS: Silver Lance & Jet-Black Spirit Jumbo Pack Set | https://archives.bulbagarden.net/media/upload/8/86/SS_Era_Logo_C.png | 0 / 6 | bulbapedia |
| Pokémon Japan | SV-P Promotional Cards |  | 225 / 235 | — |
| Pokémon Japan | SV10: The Glory of Team Rocket | https://archives.bulbagarden.net/media/upload/a/ab/SV10.5_BLK_Logo_EN.png | 132 / 132 | bulbapedia |
| Pokémon Japan | SV11B: Black Bolt | https://archives.bulbagarden.net/media/upload/0/04/SV11B_Logo_JP.png | 322 / 326 | bulbapedia |
| Pokémon Japan | SV11W: White Flare | https://archives.bulbagarden.net/media/upload/5/51/SV11W_Logo_JP.png | 319 / 326 | bulbapedia |
| Pokémon Japan | SV1S: Scarlet ex | https://archives.bulbagarden.net/media/upload/f/fb/SV1S_Logo_JP.png | 106 / 108 | bulbapedia |
| Pokémon Japan | SV1V: Violet ex | https://archives.bulbagarden.net/media/upload/a/a6/SV1V_Logo_JP.png | 108 / 108 | bulbapedia |
| Pokémon Japan | SV1a: Triplet Beat | https://archives.bulbagarden.net/media/upload/7/70/SV1a_Triplet_Beat_Logo.png | 102 / 103 | bulbapedia |
| Pokémon Japan | SV2D: Clay Burst | https://archives.bulbagarden.net/media/upload/e/ee/SV2D_Clay_Burst_pack.png | 99 / 99 | bulbapedia |
| Pokémon Japan | SV2P: Snow Hazard | https://archives.bulbagarden.net/media/upload/4/49/SV2P_Snow_Hazard_pack.png | 99 / 99 | bulbapedia |
| Pokémon Japan | SV2a: Pokemon Card 151 | https://archives.bulbagarden.net/media/upload/1/12/SV2a_Pok%C3%A9mon_Card_151_Logo.png | 513 / 516 | bulbapedia |
| Pokémon Japan | SV3: Ruler of the Black Flame | https://archives.bulbagarden.net/media/upload/2/26/SV3.5_Logo_EN.png | 141 / 141 | bulbapedia |
| Pokémon Japan | SV3a: Raging Surf | https://archives.bulbagarden.net/media/upload/8/8f/SV3a_Raging_Surf_Logo.png | 92 / 92 | bulbapedia |
| Pokémon Japan | SV4K: Ancient Roar | https://archives.bulbagarden.net/media/upload/7/78/SV4K_Ancient_Roar_pack.png | 95 / 95 | bulbapedia |
| Pokémon Japan | SV4M: Future Flash | https://archives.bulbagarden.net/media/upload/5/55/SV4M_Future_Flash_pack.png | 95 / 95 | bulbapedia |
| Pokémon Japan | SV4a: Shiny Treasure ex | https://archives.bulbagarden.net/media/upload/f/fa/SV4a_Shiny_Treasure_ex_Logo.png | 480 / 484 | bulbapedia |
| Pokémon Japan | SV5K: Wild Force | https://archives.bulbagarden.net/media/upload/8/80/SV5K_Wild_Force_pack.png | 100 / 100 | bulbapedia |
| Pokémon Japan | SV5M: Cyber Judge | https://archives.bulbagarden.net/media/upload/0/08/SV5M_Cyber_Judge_pack.png | 100 / 100 | bulbapedia |
| Pokémon Japan | SV5a: Crimson Haze | https://archives.bulbagarden.net/media/upload/9/96/SV5a_Crimson_Haze_Logo.png | 96 / 96 | bulbapedia |
| Pokémon Japan | SV6: Transformation Mask | https://archives.bulbagarden.net/media/upload/8/83/SV6_Transformation_Mask_pack.png | 133 / 133 | bulbapedia |
| Pokémon Japan | SV6a: Night Wanderer | https://archives.bulbagarden.net/media/upload/5/5e/SV6a_Night_Wanderer_Logo.png | 94 / 94 | bulbapedia |
| Pokémon Japan | SV7: Stellar Miracle | https://archives.bulbagarden.net/media/upload/8/8d/SV7_Stellar_Miracle_pack.png | 135 / 135 | bulbapedia |
| Pokémon Japan | SV7a: Paradise Dragona | https://archives.bulbagarden.net/media/upload/1/1c/SV7a_Paradise_Dragona_Logo.png | 94 / 94 | bulbapedia |
| Pokémon Japan | SV8: Super Electric Breaker | https://archives.bulbagarden.net/media/upload/f/f8/SV8_Super_Electric_Breaker_pack.png | 138 / 138 | bulbapedia |
| Pokémon Japan | SV8a: Terastal Fest ex | https://archives.bulbagarden.net/media/upload/9/9c/SV8a_Terastal_Fest_ex_Logo.png | 480 / 485 | bulbapedia |
| Pokémon Japan | SV9: Battle Partners | https://archives.bulbagarden.net/media/upload/7/7b/SV9_Battle_Partners_pack.png | 132 / 132 | bulbapedia |
| Pokémon Japan | SV9a: Heat Wave Arena | https://archives.bulbagarden.net/media/upload/a/a6/SV9a_Hot_Wind_Arena_Logo.png | 92 / 92 | bulbapedia |
| Pokémon Japan | SV: Ancient Koraidon ex Starter Deck & Build Set |  | 0 / 53 | — |
| Pokémon Japan | SV: Ceruledge ex Stellar Tera Type Starter Set |  | 21 / 21 | — |
| Pokémon Japan | SV: Chien-Pao ex Battle Master Deck |  | 19 / 19 | — |
| Pokémon Japan | SV: Future Miraidon ex Starter Deck & Build Set |  | 0 / 51 | — |
| Pokémon Japan | SV: Mewtwo ex Terastal Starter Set |  | 20 / 20 | — |
| Pokémon Japan | SV: Premium Trainer Box ex | https://archives.bulbagarden.net/media/upload/thumb/4/4c/Premium_Trainer_Box_ex.jpg/600px-Premium_Trainer_Box_ex.jpg | 28 / 28 | bulbapedia |
| Pokémon Japan | SV: Ruler of the Black Flame Deck Build Box | https://archives.bulbagarden.net/media/upload/thumb/6/6f/Ruler_of_the_Black_Flame_Deck_Build_Box.jpg/600px-Ruler_of_the_Black_Flame_Deck_Build_Box.jpg | 38 / 38 | bulbapedia |
| Pokémon Japan | SV: Skeledirge ex Terastal Starter Set |  | 20 / 20 | — |
| Pokémon Japan | SV: Stellar Miracle Deck Build Box | https://archives.bulbagarden.net/media/upload/thumb/4/42/Stellar_Miracle_Deck_Build_Box.png/600px-Stellar_Miracle_Deck_Build_Box.png | 45 / 45 | bulbapedia |
| Pokémon Japan | SV: Sylveon ex Stellar Tera Type Starter Set |  | 22 / 22 | — |
| Pokémon Japan | SV: Terastal Charizard ex Battle Master Deck |  | 21 / 21 | — |
| Pokémon Japan | SV: Venusaur, Charizard & Blastoise Special Deck Set |  | 0 / 52 | — |
| Pokémon Japan | SV: ex Special Set |  | 7 / 7 | — |
| Pokémon Japan | SV: ex Start Decks |  | 138 / 139 | — |
| Pokémon Japan | SV: ex Starter Set Fuecoco & Ampharos ex |  | 0 / 21 | — |
| Pokémon Japan | SV: ex Starter Set Marnie's Morpeko & Grimmsnarl ex | https://archives.bulbagarden.net/media/upload/thumb/5/5e/Ex_Starter_Set_Marnie_Morpeko_Grimmsnarl_ex_box.jpg/600px-Ex_Starter_Set_Marnie_Morpeko_Grimmsnarl_ex_box.jpg | 0 / 20 | bulbapedia |
| Pokémon Japan | SV: ex Starter Set Pikachu ex & Pawmot |  | 0 / 16 | — |
| Pokémon Japan | SV: ex Starter Set Quaxly & Mimikyu ex |  | 0 / 23 | — |
| Pokémon Japan | SV: ex Starter Set Sprigatito & Lucario ex |  | 0 / 23 | — |
| Pokémon Japan | SV: ex Starter Set Steven's Beldum & Metagross ex | https://archives.bulbagarden.net/media/upload/thumb/0/08/Ex_Starter_Set_Steven_Beldum_Metagross_ex_box.jpg/600px-Ex_Starter_Set_Steven_Beldum_Metagross_ex_box.jpg | 0 / 19 | bulbapedia |
| Pokémon Japan | SVM: Generations Start Decks | https://archives.bulbagarden.net/media/upload/f/ff/SVM_Generations_Start_Decks_logo.png | 175 / 175 | bulbapedia |
| Pokémon Japan | SVN: Battle Partners Deck Build Box | https://archives.bulbagarden.net/media/upload/thumb/e/e4/Battle_Partners_Deck_Build_Box_Contents.jpg/600px-Battle_Partners_Deck_Build_Box_Contents.jpg | 45 / 45 | bulbapedia |
| Pokémon Japan | Salamence Constructed Starter Deck |  | 20 / 20 | — |
| Pokémon Japan | Scarlet & Violet Era Unnumbered Energies |  | 0 / 16 | — |
| Pokémon Japan | Shiny Collection | https://archives.bulbagarden.net/media/upload/8/80/SC_Shiny_Collection_pack.jpg | 25 / 25 | bulbapedia |
| Pokémon Japan | Shockwave! Tyranitar ex Constructed Standard Deck |  | 0 / 24 | — |
| Pokémon Japan | Silver Deck Kit |  | 20 / 20 | — |
| Pokémon Japan | Southern Island | https://archives.bulbagarden.net/media/upload/thumb/c/c4/SouthernIslandsLogo.png/600px-SouthernIslandsLogo.png | 18 / 18 | bulbapedia |
| Pokémon Japan | Split Earth |  | 91 / 91 | — |
| Pokémon Japan | Start Deck 100 Battle Collection |  | 850 / 916 | — |
| Pokémon Japan | Sun & Moon Era Unnumbered Energies |  | 0 / 18 | — |
| Pokémon Japan | Sword & Shield Era Unnumbered Energies |  | 0 / 17 | — |
| Pokémon Japan | T Promotional cards |  | 24 / 24 | — |
| Pokémon Japan | Team Plasma Battle Gift Set |  | 16 / 16 | — |
| Pokémon Japan | Team Plasma's Powered Half Deck |  | 0 / 17 | — |
| Pokémon Japan | The Town on No Map |  | 92 / 92 | — |
| Pokémon Japan | Theater Limited VS Pack |  | 18 / 18 | — |
| Pokémon Japan | Torchic Constructed Starter Deck |  | 20 / 20 | — |
| Pokémon Japan | Trainer Prize Cards |  | 3 / 3 | — |
| Pokémon Japan | Treecko Constructed Starter Deck |  | 20 / 20 | — |
| Pokémon Japan | Typhlosion Constructed Starter Deck |  | 16 / 16 | — |
| Pokémon Japan | Undone Seal |  | 83 / 83 | — |
| Pokémon Japan | Unnumbered Promotional cards |  | 81 / 81 | — |
| Pokémon Japan | Unnumbered World Championships |  | 6 / 6 | — |
| Pokémon Japan | Vending Machine cards Series 1 (Blue) |  | 0 / 36 | — |
| Pokémon Japan | Vending Machine cards Series 2 (Red) |  | 0 / 36 | — |
| Pokémon Japan | Vending Machine cards Series 3 (Green) |  | 0 / 52 | — |
| Pokémon Japan | WCS23: 2023 World Championships Yokohama Deck: Pikachu | https://archives.bulbagarden.net/media/upload/9/96/WCS23_Deckbox.jpg | 30 / 30 | bulbapedia |
| Pokémon Japan | Water Quick Construction Pack |  | 15 / 15 | — |
| Pokémon Japan | Wind from the Sea |  | 90 / 90 | — |
| Pokémon Japan | World Champions Pack |  | 102 / 102 | — |
| Pokémon Japan | World Hobby Fair |  | 8 / 8 | — |
| Pokémon Japan | XY Beginning Set |  | 41 / 41 | — |
| Pokémon Japan | XY Era Unnumbered Energies |  | 0 / 9 | — |
| Pokémon Japan | XY-Bx: Collection X |  | 63 / 64 | — |
| Pokémon Japan | XY-By: Collection Y |  | 63 / 63 | — |
| Pokémon Japan | XY-P: XY Promos |  | 302 / 304 | — |
| Pokémon Japan | XY10: Awakening Psychic King | https://archives.bulbagarden.net/media/upload/9/96/XY10_Awakening_Psychic_King_Box.jpg | 88 / 88 | bulbapedia |
| Pokémon Japan | XY11-Bb: Fever-Burst Fighter |  | 59 / 59 | — |
| Pokémon Japan | XY11-Br: Cruel Traitor |  | 59 / 59 | — |
| Pokémon Japan | XY2: Wild Blaze | https://archives.bulbagarden.net/media/upload/b/b7/XY2_Wild_Blaze_Booster_Korean.jpg | 90 / 90 | bulbapedia |
| Pokémon Japan | XY3: Rising Fist | https://archives.bulbagarden.net/media/upload/f/f2/XY3_Rising_Fist_Booster_Korean.jpg | 105 / 105 | bulbapedia |
| Pokémon Japan | XY4: Phantom Gate | https://archives.bulbagarden.net/media/upload/d/d1/XY4_Phantom_Gate_Logo_KO.png | 97 / 97 | bulbapedia |
| Pokémon Japan | XY5-Bg: Gaia Volcano |  | 80 / 80 | — |
| Pokémon Japan | XY5-Bt: Tidal Storm |  | 80 / 80 | — |
| Pokémon Japan | XY6: Emerald Break | https://archives.bulbagarden.net/media/upload/3/34/XY6_Emerald_Break_Box.jpg | 91 / 91 | bulbapedia |
| Pokémon Japan | XY7: Bandit Ring | https://archives.bulbagarden.net/media/upload/6/62/XY7_Bandit_Ring_Booster_Korean.jpg | 97 / 97 | bulbapedia |
| Pokémon Japan | XY8-Bb: Blue Shock |  | 65 / 65 | — |
| Pokémon Japan | XY8-Br: Red Flash |  | 65 / 65 | — |
| Pokémon Japan | XY9: Rage of the Broken Heavens | https://archives.bulbagarden.net/media/upload/f/f2/XY9_Rage_of_the_Broken_Heavens_Box.jpg | 88 / 89 | bulbapedia |
| Pokémon Japan | XYA: M Charizard-EX Mega Battle Deck |  | 22 / 22 | — |
| Pokémon Japan | XYB: Dialga-EX + Aegislash-EX Hyper Metal Chain Deck |  | 0 / 20 | — |
| Pokémon Japan | XYC: Super Legend Set: Xerneas-EX & Yveltal-EX | https://archives.bulbagarden.net/media/upload/d/da/XYC_Legend_Battle_Deck_Logo_KO.png | 0 / 23 | bulbapedia |
| Pokémon Japan | XYD: M Rayquaza-EX Mega Battle Deck |  | 18 / 18 | — |
| Pokémon Japan | XYE: Emboar-EX vs Togekiss-EX Deck Kit |  | 22 / 22 | — |
| Pokémon Japan | XYF: Golduck BREAK + Palkia-EX Combo Deck |  | 0 / 17 | — |
| Pokémon Japan | XYG: Zygarde-EX Perfect Battle Deck |  | 19 / 19 | — |
| Pokémon Japan | XYH: M Audino-EX Mega Battle Deck |  | 26 / 26 | — |
| Pokémon Japan | Xerneas Half Deck |  | 15 / 15 | — |
| Pokémon Japan | Yveltal Half Deck |  | 15 / 15 | — |
| Pokémon Japan | m1L: Mega Brave |  | 93 / 93 | — |
| Pokémon Japan | m1S: Mega Symphonia |  | 92 / 92 | — |
| Pokémon Japan | s0: Charizard VSTAR vs Rayquaza VMAX Special Deck Set |  | 30 / 30 | — |
| Pokémon Japan | s8a-G: 25th Anniversary Golden Box |  | 16 / 16 | — |
| Pokémon Japan | s8a-P: Promo Card Pack 25th Anniversary Edition | https://archives.bulbagarden.net/media/upload/e/eb/S8a-P_Promo_Card_Pack_25th_Anniversary_Edition.jpg | 25 / 25 | bulbapedia |
| Pokémon Japan | sA: Fighting Starter Set V |  | 46 / 46 | — |
| Pokémon Japan | sA: Fire Starter Set V |  | 45 / 45 | — |
| Pokémon Japan | sA: Grass Starter Set V |  | 45 / 45 | — |
| Pokémon Japan | sA: Lightning Starter Set V |  | 46 / 46 | — |
| Pokémon Japan | sA: Water Starter Set V |  | 45 / 45 | — |
| Pokémon Japan | sB: Sword & Shield Premium Trainer Box | https://archives.bulbagarden.net/media/upload/thumb/7/7b/Sword_Shield_Premium_Trainer_Box.jpg/600px-Sword_Shield_Premium_Trainer_Box.jpg | 0 / 24 | bulbapedia |
| Pokémon Japan | sC2: Charizard Starter Set VMAX 2 |  | 21 / 21 | — |
| Pokémon Japan | sC: Charizard Starter Set VMAX |  | 21 / 21 | — |
| Pokémon Japan | sC: Grimmsnarl Starter Set VMAX |  | 20 / 20 | — |
| Pokémon Japan | sD: V Starter Decks |  | 127 / 127 | — |
| Pokémon Japan | sEF: Venusaur Starter Set VMAX |  | 21 / 21 | — |
| Pokémon Japan | sEK: Blastoise Starter Set VMAX |  | 20 / 20 | — |
| Pokémon Japan | sF: Single Strike & Rapid Strike Premium Trainer Boxes | https://archives.bulbagarden.net/media/upload/thumb/1/14/Single_Strike_Rapid_Strike_Premium_Trainer_Boxes.jpg/600px-Single_Strike_Rapid_Strike_Premium_Trainer_Boxes.jpg | 0 / 33 | bulbapedia |
| Pokémon Japan | sH: Sword & Shield Family Pokemon Card Game |  | 0 / 78 | — |
| Pokémon Japan | sJ: Zacian & Zamazenta vs Eternatus Special Deck Set |  | 0 / 30 | — |
| Pokémon Japan | sK: VSTAR Premium Trainer Box | https://archives.bulbagarden.net/media/upload/thumb/8/83/VSTAR_Premium_Trainer_Box.jpg/600px-VSTAR_Premium_Trainer_Box.jpg | 30 / 30 | bulbapedia |
| Pokémon Japan | sLD: Darkrai Starter Set VSTAR |  | 20 / 20 | — |
| Pokémon Japan | sLL: Lucario Starter Set VSTAR |  | 21 / 21 | — |
| Pokémon Japan | sN: Start Deck 100 CoroCoro Comic Version |  | 24 / 24 | — |
| Pokémon Japan | sPD: Deoxys VSTAR & VMAX High-Class Deck |  | 0 / 20 | — |
| Pokémon Japan | sPZ: Zeraora VSTAR & VMAX High-Class Deck |  | 0 / 20 | — |
| Pokémon Japan | sm1+: Enhanced Expansion Pack Sun & Moon |  | 1 / 73 | — |
| Pokémon Japan | smA: Sun & Moon Starter Set |  | 0 / 59 | — |
| Pokémon Japan | smB: Premium Trainer Box | https://archives.bulbagarden.net/media/upload/thumb/4/4c/Premium_Trainer_Box_ex.jpg/600px-Premium_Trainer_Box_ex.jpg | 18 / 18 | bulbapedia |
| Pokémon Japan | smC: Tapu Bulu-GX Enhanced Starter Set |  | 21 / 21 | — |
| Pokémon Japan | smD: Ash vs Team Rocket Deck Kit |  | 30 / 30 | — |
| Pokémon Japan | smE: Solgaleo-GX & Lunala-GX Legendary Starter Set |  | 0 / 21 | — |
| Pokémon Japan | smF: Ultra Sun & Ultra Moon Premium Trainer Box | https://archives.bulbagarden.net/media/upload/thumb/7/75/Ultra_Sun_Ultra_Moon_Premium_Trainer_Box.jpg/600px-Ultra_Sun_Ultra_Moon_Premium_Trainer_Box.jpg | 0 / 20 | bulbapedia |
| Pokémon Japan | smG: Ultra Sun & Ultra Moon Deck Build Boxes | https://archives.bulbagarden.net/media/upload/thumb/0/0e/Ultra_Sun_Ultra_Moon_Deck_Build_Boxes.jpg/600px-Ultra_Sun_Ultra_Moon_Deck_Build_Boxes.jpg | 0 / 41 | bulbapedia |
| Pokémon Japan | smH: GX Starter Decks |  | 131 / 131 | — |
| Pokémon Japan | smI: Flareon-GX, Vaporeon-GX & Jolteon-GX Starter Sets |  | 0 / 76 | — |
| Pokémon Japan | smJ: Tag Team GX Premium Trainer Box | https://archives.bulbagarden.net/media/upload/thumb/4/49/TAG_TEAM_GX_Premium_Trainer_Box.jpg/600px-TAG_TEAM_GX_Premium_Trainer_Box.jpg | 35 / 35 | bulbapedia |
| Pokémon Japan | smK: Trainer Battle Decks |  | 31 / 31 | — |
| Pokémon Japan | smL: Sun & Moon Family Pokemon Card Game |  | 0 / 86 | — |
| Pokémon Japan | smM: Tag Team GX Starter Sets |  | 31 / 31 | — |
| Pokémon Japan | smN: Tag Team GX Deck Build Box | https://archives.bulbagarden.net/media/upload/thumb/5/59/TAG_TEAM_GX_Deck_Build_Box.jpg/600px-TAG_TEAM_GX_Deck_Build_Box.jpg | 29 / 29 | bulbapedia |
| Pokémon Japan | smP1: Rockruff Full Power Deck |  | 13 / 13 | — |
| Pokémon Japan | smP2: Great Detective Pikachu |  | 25 / 25 | — |
| Pokémon Japan | sp1: Zacian + Zamazenta Box | https://archives.bulbagarden.net/media/upload/thumb/9/9c/Zacian_Zamazenta_Box.jpg/600px-Zacian_Zamazenta_Box.jpg | 0 / 7 | bulbapedia |
| Pokémon Japan | sp2: VMAX Special Set |  | 8 / 8 | — |
| Pokémon Japan | sp4: Eevee Heroes VMAX Special Set |  | 4 / 4 | — |
| Pokémon Japan | sp5: V-UNION Special Card Sets |  | 13 / 13 | — |
| Pokémon Japan | sp6: VSTAR Special Set |  | 6 / 6 | — |

### Magic: The Gathering（445 个系列，421 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Magic: The Gathering | 10th Edition | https://svgs.scryfall.io/sets/10e.svg?1791172800 | 388 / 389 | scryfall |
| Magic: The Gathering | 30th Anniversary Edition | https://svgs.scryfall.io/sets/30a.svg?1791172800 | 579 / 610 | scryfall |
| Magic: The Gathering | 30th Anniversary Promos |  | 43 / 43 | — |
| Magic: The Gathering | 7th Edition | https://svgs.scryfall.io/sets/7ed.svg?1791172800 | 347 / 350 | scryfall |
| Magic: The Gathering | 8th Edition | https://svgs.scryfall.io/sets/8ed.svg?1791172800 | 357 / 357 | scryfall |
| Magic: The Gathering | 9th Edition | https://svgs.scryfall.io/sets/9ed.svg?1791172800 | 356 / 359 | scryfall |
| Magic: The Gathering | AFR Ampersand Promos |  | 80 / 80 | — |
| Magic: The Gathering | APAC Lands |  | 15 / 15 | — |
| Magic: The Gathering | Adventures in the Forgotten Realms | https://svgs.scryfall.io/sets/afr.svg?1791172800 | 460 / 464 | scryfall |
| Magic: The Gathering | Aether Revolt | https://svgs.scryfall.io/sets/aer.svg?1791172800 | 199 / 199 | scryfall |
| Magic: The Gathering | Aetherdrift | https://svgs.scryfall.io/sets/dft.svg?1791172800 | 404 / 558 | scryfall |
| Magic: The Gathering | Alara Reborn | https://svgs.scryfall.io/sets/arb.svg?1791172800 | 149 / 149 | scryfall |
| Magic: The Gathering | Alliances | https://svgs.scryfall.io/sets/all.svg?1791172800 | 150 / 199 | scryfall |
| Magic: The Gathering | Alpha Edition | https://svgs.scryfall.io/sets/lea.svg?1791172800 | 293 / 294 | scryfall |
| Magic: The Gathering | Amonkhet | https://svgs.scryfall.io/sets/akh.svg?1791172800 | 329 / 331 | scryfall |
| Magic: The Gathering | Anthologies | https://svgs.scryfall.io/sets/ath.svg?1791172800 | 35 / 85 | scryfall |
| Magic: The Gathering | Antiquities | https://svgs.scryfall.io/sets/atq.svg?1791172800 | 100 / 100 | scryfall |
| Magic: The Gathering | Apocalypse | https://svgs.scryfall.io/sets/apc.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | Arabian Nights | https://svgs.scryfall.io/sets/arn.svg?1791172800 | 89 / 89 | scryfall |
| Magic: The Gathering | Archenemy | https://svgs.scryfall.io/sets/arc.svg?1791172800 | 56 / 150 | scryfall |
| Magic: The Gathering | Archenemy: Duskmourn |  | 40 / 40 | — |
| Magic: The Gathering | Archenemy: Nicol Bolas | https://svgs.scryfall.io/sets/e01.svg?1791172800 | 110 / 110 | scryfall |
| Magic: The Gathering | Arena Promos | https://svgs.scryfall.io/sets/mtga.svg?1791172800 | 86 / 86 | scryfall |
| Magic: The Gathering | Art Series: Adventures in the Forgotten Realms | https://svgs.scryfall.io/sets/afr.svg?1791172800 | 162 / 162 | scryfall |
| Magic: The Gathering | Art Series: Aetherdrift | https://svgs.scryfall.io/sets/dft.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Art Series: Avatar: The Last Airbender | https://svgs.scryfall.io/sets/tla.svg?1791172800 | 120 / 120 | scryfall |
| Magic: The Gathering | Art Series: Bloomburrow | https://svgs.scryfall.io/sets/blb.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Art Series: Commander Legends: Battle for Baldur's Gate | https://svgs.scryfall.io/sets/clb.svg?1791172800 ※ | 156 / 162 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: Commander Masters | https://svgs.scryfall.io/sets/cmm.svg?1791172800 | 159 / 162 | scryfall |
| Magic: The Gathering | Art Series: Dominaria United | https://svgs.scryfall.io/sets/dmu.svg?1791172800 | 160 / 162 | scryfall |
| Magic: The Gathering | Art Series: Duskmourn: House of Horror | https://svgs.scryfall.io/sets/dsk.svg?1791172800 | 107 / 108 | scryfall |
| Magic: The Gathering | Art Series: Edge of Eternities | https://svgs.scryfall.io/sets/eoe.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Art Series: FINAL FANTASY | https://svgs.scryfall.io/sets/fin.svg?1791172800 | 130 / 130 | scryfall |
| Magic: The Gathering | Art Series: Foundations | https://svgs.scryfall.io/sets/fdn.svg?1791172800 | 109 / 109 | scryfall |
| Magic: The Gathering | Art Series: Innistrad Remastered | https://svgs.scryfall.io/sets/inr.svg?1791172800 | 40 / 50 | scryfall |
| Magic: The Gathering | Art Series: Innistrad: Crimson Vow | https://svgs.scryfall.io/sets/vow.svg?1791172800 ※ | 159 / 162 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: Innistrad: Midnight Hunt | https://svgs.scryfall.io/sets/mid.svg?1791172800 ※ | 162 / 162 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: Kaldheim | https://svgs.scryfall.io/sets/khm.svg?1791172800 | 160 / 162 | scryfall |
| Magic: The Gathering | Art Series: Kamigawa: Neon Dynasty | https://svgs.scryfall.io/sets/neo.svg?1791172800 ※ | 160 / 162 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: Lorwyn Eclipsed | https://svgs.scryfall.io/sets/ecl.svg?1791172800 | 107 / 108 | scryfall |
| Magic: The Gathering | Art Series: March of the Machine | https://svgs.scryfall.io/sets/mom.svg?1791172800 | 160 / 162 | scryfall |
| Magic: The Gathering | Art Series: Marvel Super Heroes | https://svgs.scryfall.io/sets/msh.svg?1791172800 | 110 / 111 | scryfall |
| Magic: The Gathering | Art Series: Marvel's Spider-Man | https://svgs.scryfall.io/sets/spm.svg?1791172800 | 0 / 115 | scryfall |
| Magic: The Gathering | Art Series: Modern Horizons | https://svgs.scryfall.io/sets/mh1.svg?1791172800 | 54 / 54 | scryfall |
| Magic: The Gathering | Art Series: Modern Horizons 2 | https://svgs.scryfall.io/sets/mh2.svg?1791172800 | 162 / 162 | scryfall |
| Magic: The Gathering | Art Series: Modern Horizons 3 | https://svgs.scryfall.io/sets/mh3.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Art Series: Murders at Karlov Manor | https://svgs.scryfall.io/sets/mkm.svg?1791172800 | 98 / 98 | scryfall |
| Magic: The Gathering | Art Series: Outlaws of Thunder Junction | https://svgs.scryfall.io/sets/otj.svg?1791172800 | 107 / 108 | scryfall |
| Magic: The Gathering | Art Series: Phyrexia: All Will Be One | https://svgs.scryfall.io/sets/one.svg?1791172800 | 162 / 162 | scryfall |
| Magic: The Gathering | Art Series: Reality Fracture | https://svgs.scryfall.io/sets/fra.svg?1791172800 ※ | 0 / 108 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: Secrets of Strixhaven | https://svgs.scryfall.io/sets/sos.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Art Series: Streets of New Capenna | https://svgs.scryfall.io/sets/snc.svg?1791172800 ※ | 162 / 162 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: Strixhaven | https://svgs.scryfall.io/sets/stx.svg?1791172800 | 159 / 162 | scryfall |
| Magic: The Gathering | Art Series: Tarkir: Dragonstorm | https://svgs.scryfall.io/sets/tdm.svg?1791172800 | 58 / 108 | scryfall |
| Magic: The Gathering | Art Series: Teenage Mutant Ninja Turtles | https://svgs.scryfall.io/sets/tmt.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Art Series: The Brothers' War | https://svgs.scryfall.io/sets/bro.svg?1791172800 | 0 / 162 | scryfall |
| Magic: The Gathering | Art Series: The Hobbit | https://svgs.scryfall.io/sets/hob.svg?1791172800 ※ | 120 / 120 | scryfall（继承父系列） |
| Magic: The Gathering | Art Series: The Lost Caverns of Ixalan | https://svgs.scryfall.io/sets/lci.svg?1791172800 | 162 / 162 | scryfall |
| Magic: The Gathering | Art Series: Universes Beyond: Assassin's Creed | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23446/logo.webp ※ | 0 / 40 | holodex（继承父系列） |
| Magic: The Gathering | Art Series: Universes Beyond: The Lord of the Rings: Tales of Middle-earth | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23019/logo.webp ※ | 136 / 186 | holodex（继承父系列） |
| Magic: The Gathering | Art Series: Wilds of Eldraine | https://svgs.scryfall.io/sets/woe.svg?1791172800 | 158 / 162 | scryfall |
| Magic: The Gathering | Art Series: Zendikar Rising | https://svgs.scryfall.io/sets/znr.svg?1791172800 | 153 / 162 | scryfall |
| Magic: The Gathering | Avacyn Restored | https://svgs.scryfall.io/sets/avr.svg?1791172800 | 252 / 252 | scryfall |
| Magic: The Gathering | Avatar: The Last Airbender | https://svgs.scryfall.io/sets/tla.svg?1791172800 | 324 / 475 | scryfall |
| Magic: The Gathering | Avatar: The Last Airbender: Eternal-Legal | https://svgs.scryfall.io/sets/tle.svg?1791172800 | 318 / 318 | scryfall |
| Magic: The Gathering | Battle Royale Box Set | https://svgs.scryfall.io/sets/brb.svg?1791172800 | 133 / 136 | scryfall |
| Magic: The Gathering | Battle for Zendikar | https://svgs.scryfall.io/sets/bfz.svg?1791172800 | 313 / 313 | scryfall |
| Magic: The Gathering | Battlebond | https://svgs.scryfall.io/sets/bbd.svg?1791172800 | 264 / 264 | scryfall |
| Magic: The Gathering | Beatdown Box Set | https://svgs.scryfall.io/sets/btd.svg?1791172800 | 90 / 90 | scryfall |
| Magic: The Gathering | Beta Edition | https://svgs.scryfall.io/sets/leb.svg?1791172800 | 300 / 301 | scryfall |
| Magic: The Gathering | Betrayers of Kamigawa | https://svgs.scryfall.io/sets/bok.svg?1791172800 | 165 / 165 | scryfall |
| Magic: The Gathering | Bloomburrow | https://svgs.scryfall.io/sets/blb.svg?1791172800 | 249 / 450 | scryfall |
| Magic: The Gathering | Born of the Gods | https://svgs.scryfall.io/sets/bng.svg?1791172800 | 175 / 176 | scryfall |
| Magic: The Gathering | Buy-A-Box Promos |  | 92 / 92 | — |
| Magic: The Gathering | Champions of Kamigawa | https://svgs.scryfall.io/sets/chk.svg?1791172800 | 256 / 307 | scryfall |
| Magic: The Gathering | Champs Promos | https://svgs.scryfall.io/sets/default.svg?1791172800 | 12 / 12 | scryfall |
| Magic: The Gathering | Chronicles | https://svgs.scryfall.io/sets/chr.svg?1791172800 | 125 / 125 | scryfall |
| Magic: The Gathering | Classic Sixth Edition | https://svgs.scryfall.io/sets/6ed.svg?1791172800 | 348 / 348 | scryfall |
| Magic: The Gathering | Coldsnap | https://svgs.scryfall.io/sets/csp.svg?1791172800 | 147 / 155 | scryfall |
| Magic: The Gathering | Coldsnap Theme Deck Reprints | https://svgs.scryfall.io/sets/csp.svg?1791172800 ※ | 62 / 62 | scryfall（继承父系列） |
| Magic: The Gathering | Collector's Edition | https://svgs.scryfall.io/sets/ced.svg?1791172800 | 0 / 301 | scryfall |
| Magic: The Gathering | Commander |  | 0 / 318 | — |
| Magic: The Gathering | Commander 2013 | https://svgs.scryfall.io/sets/c13.svg?1791172800 | 356 / 356 | scryfall |
| Magic: The Gathering | Commander 2014 | https://svgs.scryfall.io/sets/c14.svg?1791172800 | 361 / 361 | scryfall |
| Magic: The Gathering | Commander 2015 | https://svgs.scryfall.io/sets/c15.svg?1791172800 | 368 / 368 | scryfall |
| Magic: The Gathering | Commander 2016 | https://svgs.scryfall.io/sets/c16.svg?1791172800 | 369 / 369 | scryfall |
| Magic: The Gathering | Commander 2017 | https://svgs.scryfall.io/sets/c17.svg?1791172800 | 321 / 321 | scryfall |
| Magic: The Gathering | Commander 2018 | https://svgs.scryfall.io/sets/c18.svg?1791172800 | 331 / 331 | scryfall |
| Magic: The Gathering | Commander 2019 | https://svgs.scryfall.io/sets/c19.svg?1791172800 | 323 / 323 | scryfall |
| Magic: The Gathering | Commander 2020 | https://svgs.scryfall.io/sets/c20.svg?1791172800 | 341 / 341 | scryfall |
| Magic: The Gathering | Commander 2021 | https://svgs.scryfall.io/sets/c21.svg?1791172800 | 435 / 435 | scryfall |
| Magic: The Gathering | Commander Anthology | https://svgs.scryfall.io/sets/cma.svg?1791172800 | 340 / 340 | scryfall |
| Magic: The Gathering | Commander Anthology Volume II | https://svgs.scryfall.io/sets/cm2.svg?1791172800 | 331 / 331 | scryfall |
| Magic: The Gathering | Commander Collection: Black | https://svgs.scryfall.io/sets/cc2.svg?1791172800 | 9 / 9 | scryfall |
| Magic: The Gathering | Commander Collection: Green | https://svgs.scryfall.io/sets/cc1.svg?1791172800 | 8 / 8 | scryfall |
| Magic: The Gathering | Commander Legends | https://svgs.scryfall.io/sets/cmr.svg?1791172800 | 752 / 781 | scryfall |
| Magic: The Gathering | Commander Legends: Battle for Baldur's Gate | https://svgs.scryfall.io/sets/clb.svg?1791172800 | 972 / 996 | scryfall |
| Magic: The Gathering | Commander Masters | https://svgs.scryfall.io/sets/cmm.svg?1791172800 | 1195 / 1370 | scryfall |
| Magic: The Gathering | Commander's Arsenal | https://svgs.scryfall.io/sets/cm1.svg?1791172800 | 0 / 18 | scryfall |
| Magic: The Gathering | Commander: Adventures in the Forgotten Realms | https://svgs.scryfall.io/sets/afc.svg?1791172800 | 349 / 349 | scryfall |
| Magic: The Gathering | Commander: Aetherdrift | https://svgs.scryfall.io/sets/drc.svg?1791172800 | 206 / 206 | scryfall |
| Magic: The Gathering | Commander: Bloomburrow | https://svgs.scryfall.io/sets/blc.svg?1791172800 | 386 / 386 | scryfall |
| Magic: The Gathering | Commander: Dominaria United | https://svgs.scryfall.io/sets/dmc.svg?1791172800 | 264 / 264 | scryfall |
| Magic: The Gathering | Commander: Duskmourn: House of Horror | https://svgs.scryfall.io/sets/dsc.svg?1791172800 | 355 / 355 | scryfall |
| Magic: The Gathering | Commander: Edge of Eternities | https://svgs.scryfall.io/sets/eoc.svg?1791172800 | 213 / 213 | scryfall |
| Magic: The Gathering | Commander: FINAL FANTASY | https://svgs.scryfall.io/sets/fic.svg?1791172800 | 767 / 817 | scryfall |
| Magic: The Gathering | Commander: Foundations | https://svgs.scryfall.io/sets/fdc.svg?1791172800 | 3 / 338 | scryfall |
| Magic: The Gathering | Commander: Innistrad: Crimson Vow | https://svgs.scryfall.io/sets/voc.svg?1791172800 | 194 / 194 | scryfall |
| Magic: The Gathering | Commander: Innistrad: Midnight Hunt | https://svgs.scryfall.io/sets/mic.svg?1791172800 | 199 / 199 | scryfall |
| Magic: The Gathering | Commander: Kaldheim | https://svgs.scryfall.io/sets/khc.svg?1791172800 | 128 / 128 | scryfall |
| Magic: The Gathering | Commander: Kamigawa: Neon Dynasty | https://svgs.scryfall.io/sets/nec.svg?1791172800 | 192 / 192 | scryfall |
| Magic: The Gathering | Commander: Lorwyn Eclipsed | https://svgs.scryfall.io/sets/ecc.svg?1791172800 | 195 / 195 | scryfall |
| Magic: The Gathering | Commander: March of the Machine | https://svgs.scryfall.io/sets/moc.svg?1791172800 | 428 / 428 | scryfall |
| Magic: The Gathering | Commander: Marvel Super Heroes | https://svgs.scryfall.io/sets/msc.svg?1791172800 | 1117 / 1268 | scryfall |
| Magic: The Gathering | Commander: Modern Horizons 3 | https://svgs.scryfall.io/sets/m3c.svg?1791172800 | 715 / 766 | scryfall |
| Magic: The Gathering | Commander: Murders at Karlov Manor | https://svgs.scryfall.io/sets/mkc.svg?1791172800 | 384 / 385 | scryfall |
| Magic: The Gathering | Commander: Outlaws of Thunder Junction | https://svgs.scryfall.io/sets/otc.svg?1791172800 | 379 / 379 | scryfall |
| Magic: The Gathering | Commander: Phyrexia: All Will Be One | https://svgs.scryfall.io/sets/onc.svg?1791172800 | 189 / 189 | scryfall |
| Magic: The Gathering | Commander: Reality Fracture | https://svgs.scryfall.io/sets/frc.svg?1791172800 | 2 / 122 | scryfall |
| Magic: The Gathering | Commander: Secrets of Strixhaven | https://svgs.scryfall.io/sets/soc.svg?1791172800 | 454 / 454 | scryfall |
| Magic: The Gathering | Commander: Star Trek | https://svgs.scryfall.io/sets/trc.svg?1791172800 | 10 / 10 | scryfall |
| Magic: The Gathering | Commander: Streets of New Capenna | https://svgs.scryfall.io/sets/ncc.svg?1791172800 | 483 / 483 | scryfall |
| Magic: The Gathering | Commander: Tarkir: Dragonstorm | https://svgs.scryfall.io/sets/tdc.svg?1791172800 | 444 / 444 | scryfall |
| Magic: The Gathering | Commander: Teenage Mutant Ninja Turtles | https://svgs.scryfall.io/sets/tmc.svg?1791172800 | 200 / 248 | scryfall |
| Magic: The Gathering | Commander: The Brothers' War | https://svgs.scryfall.io/sets/brc.svg?1791172800 | 0 / 227 | scryfall |
| Magic: The Gathering | Commander: The Lord of the Rings: Tales of Middle-earth | https://svgs.scryfall.io/sets/ltc.svg?1791172800 | 509 / 609 | scryfall |
| Magic: The Gathering | Commander: The Lost Caverns of Ixalan | https://svgs.scryfall.io/sets/lcc.svg?1791172800 | 363 / 390 | scryfall |
| Magic: The Gathering | Commander: Wilds of Eldraine | https://svgs.scryfall.io/sets/woc.svg?1791172800 | 185 / 185 | scryfall |
| Magic: The Gathering | Commander: Zendikar Rising | https://svgs.scryfall.io/sets/znc.svg?1791172800 | 149 / 149 | scryfall |
| Magic: The Gathering | Conflux | https://svgs.scryfall.io/sets/con.svg?1791172800 | 147 / 147 | scryfall |
| Magic: The Gathering | Conspiracy | https://svgs.scryfall.io/sets/cns.svg?1791172800 | 72 / 219 | scryfall |
| Magic: The Gathering | Conspiracy: Take the Crown | https://svgs.scryfall.io/sets/cn2.svg?1791172800 | 234 / 234 | scryfall |
| Magic: The Gathering | Core Set 2019 | https://svgs.scryfall.io/sets/m19.svg?1791172800 | 337 / 337 | scryfall |
| Magic: The Gathering | Core Set 2020 | https://svgs.scryfall.io/sets/m20.svg?1791172800 | 354 / 356 | scryfall |
| Magic: The Gathering | Core Set 2021 | https://svgs.scryfall.io/sets/m21.svg?1791172800 | 459 / 461 | scryfall |
| Magic: The Gathering | Dark Ascension | https://svgs.scryfall.io/sets/dka.svg?1791172800 | 161 / 162 | scryfall |
| Magic: The Gathering | Darksteel | https://svgs.scryfall.io/sets/dst.svg?1791172800 | 65 / 165 | scryfall |
| Magic: The Gathering | Deckmasters Garfield vs Finkel | https://svgs.scryfall.io/sets/dkm.svg?1791172800 | 55 / 56 | scryfall |
| Magic: The Gathering | Dissension | https://svgs.scryfall.io/sets/dis.svg?1791172800 | 180 / 180 | scryfall |
| Magic: The Gathering | Dominaria | https://svgs.scryfall.io/sets/dom.svg?1791172800 | 279 / 295 | scryfall |
| Magic: The Gathering | Dominaria Remastered | https://svgs.scryfall.io/sets/dmr.svg?1791172800 | 510 / 510 | scryfall |
| Magic: The Gathering | Dominaria United | https://svgs.scryfall.io/sets/dmu.svg?1791172800 | 329 / 511 | scryfall |
| Magic: The Gathering | Double Masters | https://svgs.scryfall.io/sets/2xm.svg?1791172800 | 495 / 501 | scryfall |
| Magic: The Gathering | Double Masters 2022 | https://svgs.scryfall.io/sets/2x2.svg?1791172800 | 659 / 660 | scryfall |
| Magic: The Gathering | Dragon's Maze | https://svgs.scryfall.io/sets/dgm.svg?1791172800 | 0 / 157 | scryfall |
| Magic: The Gathering | Dragons of Tarkir | https://svgs.scryfall.io/sets/dtk.svg?1791172800 | 272 / 272 | scryfall |
| Magic: The Gathering | Duel Decks: Ajani vs. Nicol Bolas | https://svgs.scryfall.io/sets/ddh.svg?1791172800 | 0 / 82 | scryfall |
| Magic: The Gathering | Duel Decks: Anthology |  | 209 / 260 | — |
| Magic: The Gathering | Duel Decks: Blessed vs. Cursed | https://svgs.scryfall.io/sets/ddq.svg?1791172800 | 72 / 80 | scryfall |
| Magic: The Gathering | Duel Decks: Divine vs. Demonic | https://svgs.scryfall.io/sets/ddc.svg?1791172800 | 0 / 65 | scryfall |
| Magic: The Gathering | Duel Decks: Elspeth vs. Kiora | https://svgs.scryfall.io/sets/ddo.svg?1791172800 | 0 / 67 | scryfall |
| Magic: The Gathering | Duel Decks: Elspeth vs. Tezzeret | https://svgs.scryfall.io/sets/ddf.svg?1791172800 | 0 / 79 | scryfall |
| Magic: The Gathering | Duel Decks: Elves vs. Goblins | https://svgs.scryfall.io/sets/dd1.svg?1791172800 | 0 / 65 | scryfall |
| Magic: The Gathering | Duel Decks: Elves vs. Inventors | https://svgs.scryfall.io/sets/ddu.svg?1791172800 | 69 / 80 | scryfall |
| Magic: The Gathering | Duel Decks: Garruk vs. Liliana | https://svgs.scryfall.io/sets/ddd.svg?1791172800 | 0 / 66 | scryfall |
| Magic: The Gathering | Duel Decks: Heroes vs. Monsters | https://svgs.scryfall.io/sets/ddl.svg?1791172800 | 16 / 83 | scryfall |
| Magic: The Gathering | Duel Decks: Izzet vs. Golgari | https://svgs.scryfall.io/sets/ddj.svg?1791172800 | 0 / 91 | scryfall |
| Magic: The Gathering | Duel Decks: Jace vs. Chandra | https://svgs.scryfall.io/sets/dd2.svg?1791172800 | 2 / 65 | scryfall |
| Magic: The Gathering | Duel Decks: Jace vs. Vraska | https://svgs.scryfall.io/sets/ddm.svg?1791172800 | 0 / 89 | scryfall |
| Magic: The Gathering | Duel Decks: Knights vs. Dragons | https://svgs.scryfall.io/sets/ddg.svg?1791172800 | 0 / 82 | scryfall |
| Magic: The Gathering | Duel Decks: Merfolk vs. Goblins | https://svgs.scryfall.io/sets/ddt.svg?1791172800 | 66 / 66 | scryfall |
| Magic: The Gathering | Duel Decks: Mind vs. Might | https://svgs.scryfall.io/sets/dds.svg?1791172800 | 65 / 72 | scryfall |
| Magic: The Gathering | Duel Decks: Nissa vs. Ob Nixilis | https://svgs.scryfall.io/sets/ddr.svg?1791172800 | 76 / 76 | scryfall |
| Magic: The Gathering | Duel Decks: Phyrexia vs. the Coalition | https://svgs.scryfall.io/sets/dde.svg?1791172800 | 0 / 74 | scryfall |
| Magic: The Gathering | Duel Decks: Sorin vs. Tibalt | https://svgs.scryfall.io/sets/ddk.svg?1791172800 | 0 / 81 | scryfall |
| Magic: The Gathering | Duel Decks: Speed vs. Cunning | https://svgs.scryfall.io/sets/ddn.svg?1791172800 | 0 / 82 | scryfall |
| Magic: The Gathering | Duel Decks: Venser vs. Koth | https://svgs.scryfall.io/sets/ddi.svg?1791172800 | 0 / 79 | scryfall |
| Magic: The Gathering | Duel Decks: Zendikar vs. Eldrazi | https://svgs.scryfall.io/sets/ddp.svg?1791172800 | 80 / 80 | scryfall |
| Magic: The Gathering | Duels of the Planeswalkers | https://svgs.scryfall.io/sets/dpa.svg?1791172800 | 113 / 113 | scryfall |
| Magic: The Gathering | Duskmourn: House of Horror | https://svgs.scryfall.io/sets/dsk.svg?1791172800 | 259 / 460 | scryfall |
| Magic: The Gathering | Edge of Eternities | https://svgs.scryfall.io/sets/eoe.svg?1791172800 | 212 / 407 | scryfall |
| Magic: The Gathering | Edge of Eternities: Stellar Sights | https://svgs.scryfall.io/sets/eos.svg?1791172800 | 180 / 180 | scryfall |
| Magic: The Gathering | Eldritch Moon | https://svgs.scryfall.io/sets/emn.svg?1791172800 | 216 / 216 | scryfall |
| Magic: The Gathering | Eternal Masters | https://svgs.scryfall.io/sets/ema.svg?1791172800 | 265 / 265 | scryfall |
| Magic: The Gathering | European Lands | https://svgs.scryfall.io/sets/peuro.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | Eventide | https://svgs.scryfall.io/sets/eve.svg?1791172800 | 187 / 187 | scryfall |
| Magic: The Gathering | Exodus | https://svgs.scryfall.io/sets/exo.svg?1791172800 | 142 / 143 | scryfall |
| Magic: The Gathering | Explorers of Ixalan | https://svgs.scryfall.io/sets/e02.svg?1791172800 | 49 / 49 | scryfall |
| Magic: The Gathering | FINAL FANTASY | https://svgs.scryfall.io/sets/fin.svg?1791172800 | 309 / 644 | scryfall |
| Magic: The Gathering | FINAL FANTASY: Through the Ages | https://svgs.scryfall.io/sets/fca.svg?1791172800 | 65 / 65 | scryfall |
| Magic: The Gathering | FNM Promos | https://svgs.scryfall.io/sets/default.svg?1791172800 | 233 / 234 | scryfall |
| Magic: The Gathering | Fallen Empires | https://svgs.scryfall.io/sets/fem.svg?1791172800 | 137 / 187 | scryfall |
| Magic: The Gathering | Fate Reforged | https://svgs.scryfall.io/sets/frf.svg?1791172800 | 189 / 189 | scryfall |
| Magic: The Gathering | Fifth Dawn | https://svgs.scryfall.io/sets/5dn.svg?1791172800 | 165 / 165 | scryfall |
| Magic: The Gathering | Fifth Edition | https://svgs.scryfall.io/sets/5ed.svg?1791172800 | 447 / 447 | scryfall |
| Magic: The Gathering | Foundations | https://svgs.scryfall.io/sets/fdn.svg?1791172800 | 506 / 805 | scryfall |
| Magic: The Gathering | Foundations Jumpstart | https://svgs.scryfall.io/sets/j25.svg?1791172800 | 722 / 825 | scryfall |
| Magic: The Gathering | Fourth Edition | https://svgs.scryfall.io/sets/4ed.svg?1791172800 | 331 / 376 | scryfall |
| Magic: The Gathering | Fourth Edition (Foreign Black Border) | https://svgs.scryfall.io/sets/4ed.svg?1791172800 | 376 / 376 | scryfall |
| Magic: The Gathering | Fourth Edition (Foreign White Border) | https://svgs.scryfall.io/sets/4ed.svg?1791172800 ※ | 376 / 376 | scryfall（继承父系列） |
| Magic: The Gathering | From the Vault: Angels | https://svgs.scryfall.io/sets/v15.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Annihilation | https://svgs.scryfall.io/sets/v14.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Dragons | https://svgs.scryfall.io/sets/drb.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Exiled | https://svgs.scryfall.io/sets/v09.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Legends | https://svgs.scryfall.io/sets/v11.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Lore | https://svgs.scryfall.io/sets/v16.svg?1791172800 | 16 / 16 | scryfall |
| Magic: The Gathering | From the Vault: Realms | https://svgs.scryfall.io/sets/v12.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Relics | https://svgs.scryfall.io/sets/v10.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Transform | https://svgs.scryfall.io/sets/v17.svg?1791172800 | 15 / 15 | scryfall |
| Magic: The Gathering | From the Vault: Twenty | https://svgs.scryfall.io/sets/v13.svg?1791172800 | 20 / 20 | scryfall |
| Magic: The Gathering | Future Sight | https://svgs.scryfall.io/sets/fut.svg?1791172800 | 180 / 180 | scryfall |
| Magic: The Gathering | Game Day & Store Championship Promos | https://svgs.scryfall.io/sets/star.svg?1791172800 | 38 / 174 | scryfall |
| Magic: The Gathering | Gatecrash | https://svgs.scryfall.io/sets/gtc.svg?1791172800 | 257 / 257 | scryfall |
| Magic: The Gathering | Gift Boxes and Promos |  | 16 / 16 | — |
| Magic: The Gathering | Global Series Jiang Yanggu & Mu Yanling | https://svgs.scryfall.io/sets/gs1.svg?1791172800 | 37 / 41 | scryfall |
| Magic: The Gathering | Grand Prix Promos | https://svgs.scryfall.io/sets/star.svg?1791172800 | 20 / 20 | scryfall |
| Magic: The Gathering | Guildpact | https://svgs.scryfall.io/sets/gpt.svg?1791172800 | 165 / 165 | scryfall |
| Magic: The Gathering | Guilds of Ravnica | https://svgs.scryfall.io/sets/grn.svg?1791172800 | 270 / 280 | scryfall |
| Magic: The Gathering | Guilds of Ravnica: Guild Kits | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2334/logo.webp | 137 / 137 | holodex |
| Magic: The Gathering | Guru Lands | https://svgs.scryfall.io/sets/pgru.svg?1791172800 | 5 / 5 | scryfall |
| Magic: The Gathering | Hero's Path Promos | https://svgs.scryfall.io/sets/ths.svg?1791172800 | 42 / 66 | scryfall |
| Magic: The Gathering | Homelands | https://svgs.scryfall.io/sets/hml.svg?1791172800 | 139 / 140 | scryfall |
| Magic: The Gathering | Hour of Devastation | https://svgs.scryfall.io/sets/hou.svg?1791172800 | 246 / 246 | scryfall |
| Magic: The Gathering | Ice Age | https://svgs.scryfall.io/sets/ice.svg?1791172800 | 382 / 383 | scryfall |
| Magic: The Gathering | Iconic Masters | https://svgs.scryfall.io/sets/ima.svg?1791172800 | 253 / 256 | scryfall |
| Magic: The Gathering | Ikoria: Lair of Behemoths | https://svgs.scryfall.io/sets/iko.svg?1791172800 | 417 / 417 | scryfall |
| Magic: The Gathering | Innistrad | https://svgs.scryfall.io/sets/isd.svg?1791172800 | 31 / 277 | scryfall |
| Magic: The Gathering | Innistrad Remastered | https://svgs.scryfall.io/sets/inr.svg?1791172800 | 509 / 510 | scryfall |
| Magic: The Gathering | Innistrad: Crimson Vow | https://svgs.scryfall.io/sets/vow.svg?1791172800 | 484 / 487 | scryfall |
| Magic: The Gathering | Innistrad: Double Feature | https://svgs.scryfall.io/sets/star.svg?1791172800 | 534 / 534 | scryfall |
| Magic: The Gathering | Innistrad: Midnight Hunt | https://svgs.scryfall.io/sets/mid.svg?1791172800 | 463 / 472 | scryfall |
| Magic: The Gathering | International Edition |  | 248 / 301 | — |
| Magic: The Gathering | Introductory Two-Player Set | https://svgs.scryfall.io/sets/x2ps.svg?1791172800 | 67 / 67 | scryfall |
| Magic: The Gathering | Invasion | https://svgs.scryfall.io/sets/inv.svg?1791172800 | 350 / 350 | scryfall |
| Magic: The Gathering | Ixalan | https://svgs.scryfall.io/sets/xln.svg?1791172800 | 281 / 303 | scryfall |
| Magic: The Gathering | JingHe Age Token Cards |  | 12 / 12 | — |
| Magic: The Gathering | Journey Into Nyx | https://svgs.scryfall.io/sets/jou.svg?1791172800 | 121 / 171 | scryfall |
| Magic: The Gathering | Judge Promos | https://svgs.scryfall.io/sets/archie.svg?1791172800 | 155 / 177 | scryfall |
| Magic: The Gathering | Judgment | https://svgs.scryfall.io/sets/jud.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | Jumpstart | https://svgs.scryfall.io/sets/jmp.svg?1791172800 | 518 / 541 | scryfall |
| Magic: The Gathering | Jumpstart 2022 | https://svgs.scryfall.io/sets/j22.svg?1791172800 | 814 / 880 | scryfall |
| Magic: The Gathering | Junior Series Promos |  | 42 / 42 | — |
| Magic: The Gathering | Kaladesh | https://svgs.scryfall.io/sets/kld.svg?1791172800 | 288 / 289 | scryfall |
| Magic: The Gathering | Kaldheim | https://svgs.scryfall.io/sets/khm.svg?1791172800 | 489 / 495 | scryfall |
| Magic: The Gathering | Kamigawa: Neon Dynasty | https://svgs.scryfall.io/sets/neo.svg?1791172800 | 561 / 566 | scryfall |
| Magic: The Gathering | Khans of Tarkir | https://svgs.scryfall.io/sets/ktk.svg?1791172800 | 282 / 282 | scryfall |
| Magic: The Gathering | Launch Party & Release Event Promos |  | 66 / 121 | — |
| Magic: The Gathering | League Promos | https://svgs.scryfall.io/sets/parl.svg?1791172800 | 19 / 19 | scryfall |
| Magic: The Gathering | Legends | https://svgs.scryfall.io/sets/leg.svg?1791172800 | 5 / 307 | scryfall |
| Magic: The Gathering | Legions | https://svgs.scryfall.io/sets/lgn.svg?1791172800 | 145 / 145 | scryfall |
| Magic: The Gathering | Lorwyn | https://svgs.scryfall.io/sets/lrw.svg?1791172800 | 19 / 312 | scryfall |
| Magic: The Gathering | Lorwyn Eclipsed | https://svgs.scryfall.io/sets/ecl.svg?1791172800 | 298 / 413 | scryfall |
| Magic: The Gathering | Magic 2010 (M10) | https://svgs.scryfall.io/sets/m10.svg?1791172800 ※ | 0 / 257 | scryfall（继承父系列） |
| Magic: The Gathering | Magic 2011 (M11) | https://svgs.scryfall.io/sets/m11.svg?1791172800 ※ | 0 / 255 | scryfall（继承父系列） |
| Magic: The Gathering | Magic 2012 (M12) | https://svgs.scryfall.io/sets/m12.svg?1791172800 ※ | 0 / 256 | scryfall（继承父系列） |
| Magic: The Gathering | Magic 2013 (M13) | https://svgs.scryfall.io/sets/m13.svg?1791172800 ※ | 0 / 260 | scryfall（继承父系列） |
| Magic: The Gathering | Magic 2014 (M14) | https://svgs.scryfall.io/sets/m14.svg?1791172800 ※ | 0 / 262 | scryfall（继承父系列） |
| Magic: The Gathering | Magic 2015 (M15) | https://svgs.scryfall.io/sets/m15.svg?1791172800 ※ | 0 / 298 | scryfall（继承父系列） |
| Magic: The Gathering | Magic Encyclopedia 2005 (Salvat/Hachette) | https://svgs.scryfall.io/sets/phuk.svg?1791172800 | 1488 / 1674 | scryfall |
| Magic: The Gathering | Magic Encyclopedia 2011 (Salvat) | https://svgs.scryfall.io/sets/psal.svg?1791172800 | 222 / 224 | scryfall |
| Magic: The Gathering | Magic Game Night | https://svgs.scryfall.io/sets/gnt.svg?1791172800 | 68 / 68 | scryfall |
| Magic: The Gathering | Magic Game Night 2019 | https://svgs.scryfall.io/sets/gn2.svg?1791172800 | 70 / 70 | scryfall |
| Magic: The Gathering | Magic Game Night: Free-For-All | https://svgs.scryfall.io/sets/gn3.svg?1791172800 | 142 / 143 | scryfall |
| Magic: The Gathering | Magic Modern Event Deck | https://svgs.scryfall.io/sets/md1.svg?1791172800 | 29 / 29 | scryfall |
| Magic: The Gathering | Magic Origins | https://svgs.scryfall.io/sets/ori.svg?1791172800 | 290 / 303 | scryfall |
| Magic: The Gathering | Magic Player Rewards | https://svgs.scryfall.io/sets/default.svg?1791172800 | 27 / 77 | scryfall |
| Magic: The Gathering | Magic Premiere Shop | https://svgs.scryfall.io/sets/pmps.svg?1791172800 | 1 / 50 | scryfall |
| Magic: The Gathering | MagicFest Cards |  | 41 / 41 | — |
| Magic: The Gathering | March of the Machine | https://svgs.scryfall.io/sets/mom.svg?1791172800 | 229 / 504 | scryfall |
| Magic: The Gathering | March of the Machine: Multiverse Legends | https://svgs.scryfall.io/sets/mul.svg?1791172800 | 262 / 262 | scryfall |
| Magic: The Gathering | March of the Machine: The Aftermath | https://svgs.scryfall.io/sets/mat.svg?1791172800 | 178 / 228 | scryfall |
| Magic: The Gathering | Marvel Super Heroes | https://svgs.scryfall.io/sets/msh.svg?1791172800 | 227 / 469 | scryfall |
| Magic: The Gathering | Marvel Universe Eternal-Legal | https://svgs.scryfall.io/sets/mar.svg?1791172800 | 100 / 100 | scryfall |
| Magic: The Gathering | Marvel's Spider-Man | https://svgs.scryfall.io/sets/spm.svg?1791172800 | 0 / 289 | scryfall |
| Magic: The Gathering | Marvel's Spider-Man: Eternal-Legal | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24246/logo.webp | 0 / 26 | holodex |
| Magic: The Gathering | Masterpiece Series: Amonkhet Invocations | https://svgs.scryfall.io/sets/mp2.svg?1791172800 | 54 / 54 | scryfall |
| Magic: The Gathering | Masterpiece Series: Kaladesh Inventions | https://svgs.scryfall.io/sets/mps.svg?1791172800 | 54 / 54 | scryfall |
| Magic: The Gathering | Masters 25 | https://svgs.scryfall.io/sets/a25.svg?1791172800 | 265 / 265 | scryfall |
| Magic: The Gathering | Media Promos | https://svgs.scryfall.io/sets/pmei.svg?1791172800 | 222 / 255 | scryfall |
| Magic: The Gathering | Mercadian Masques | https://svgs.scryfall.io/sets/mmq.svg?1791172800 | 350 / 350 | scryfall |
| Magic: The Gathering | Mirage | https://svgs.scryfall.io/sets/mir.svg?1791172800 | 350 / 350 | scryfall |
| Magic: The Gathering | Mirrodin | https://svgs.scryfall.io/sets/mrd.svg?1791172800 | 142 / 306 | scryfall |
| Magic: The Gathering | Mirrodin Besieged | https://svgs.scryfall.io/sets/mbs.svg?1791172800 | 161 / 161 | scryfall |
| Magic: The Gathering | Modern Horizons | https://svgs.scryfall.io/sets/mh1.svg?1791172800 | 432 / 444 | scryfall |
| Magic: The Gathering | Modern Horizons 2 | https://svgs.scryfall.io/sets/mh2.svg?1791172800 | 693 / 697 | scryfall |
| Magic: The Gathering | Modern Horizons 3 | https://svgs.scryfall.io/sets/mh3.svg?1791172800 | 424 / 665 | scryfall |
| Magic: The Gathering | Modern Masters | https://svgs.scryfall.io/sets/mma.svg?1791172800 | 67 / 245 | scryfall |
| Magic: The Gathering | Modern Masters 2015 | https://svgs.scryfall.io/sets/mm2.svg?1791172800 | 265 / 265 | scryfall |
| Magic: The Gathering | Modern Masters 2017 | https://svgs.scryfall.io/sets/mm3.svg?1791172800 | 270 / 270 | scryfall |
| Magic: The Gathering | Morningtide | https://svgs.scryfall.io/sets/mor.svg?1791172800 | 153 / 153 | scryfall |
| Magic: The Gathering | Murders at Karlov Manor | https://svgs.scryfall.io/sets/mkm.svg?1791172800 | 256 / 494 | scryfall |
| Magic: The Gathering | Mystery Booster 2 | https://svgs.scryfall.io/sets/mb2.svg?1791172800 | 236 / 264 | scryfall |
| Magic: The Gathering | Mystery Booster 2 Playtest Cards | https://svgs.scryfall.io/sets/mb2.svg?1791172800 ※ | 122 / 122 | scryfall（继承父系列） |
| Magic: The Gathering | Mystery Booster Commander Edition | https://svgs.scryfall.io/sets/mbc.svg?1791172800 | 80 / 80 | scryfall |
| Magic: The Gathering | Mystery Booster: Convention Edition Exclusives | https://svgs.scryfall.io/sets/planeswalker.svg?1791172800 | 239 / 246 | scryfall |
| Magic: The Gathering | Mythic Edition: Guilds of Ravnica | https://svgs.scryfall.io/sets/med.svg?1791172800 | 16 / 16 | scryfall |
| Magic: The Gathering | Mythic Edition: Ravnica Allegiance | https://svgs.scryfall.io/sets/med.svg?1791172800 | 13 / 13 | scryfall |
| Magic: The Gathering | Mythic Edition: War of the Spark | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2444/logo.webp | 11 / 11 | holodex |
| Magic: The Gathering | Nemesis | https://svgs.scryfall.io/sets/nem.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | New Phyrexia | https://svgs.scryfall.io/sets/nph.svg?1791172800 | 179 / 180 | scryfall |
| Magic: The Gathering | Oath of the Gatewatch | https://svgs.scryfall.io/sets/ogw.svg?1791172800 | 197 / 197 | scryfall |
| Magic: The Gathering | Odyssey | https://svgs.scryfall.io/sets/ody.svg?1791172800 | 299 / 350 | scryfall |
| Magic: The Gathering | Onslaught | https://svgs.scryfall.io/sets/ons.svg?1791172800 | 349 / 350 | scryfall |
| Magic: The Gathering | Open House Promos |  | 11 / 11 | — |
| Magic: The Gathering | Outlaws of Thunder Junction | https://svgs.scryfall.io/sets/otj.svg?1791172800 | 252 / 458 | scryfall |
| Magic: The Gathering | Outlaws of Thunder Junction: Breaking News | https://svgs.scryfall.io/sets/otp.svg?1791172800 | 90 / 90 | scryfall |
| Magic: The Gathering | Outlaws of Thunder Junction: The Big Score | https://svgs.scryfall.io/sets/big.svg?1791172800 | 108 / 108 | scryfall |
| Magic: The Gathering | Oversize Cards |  | 497 / 509 | — |
| Magic: The Gathering | Phyrexia: All Will Be One | https://svgs.scryfall.io/sets/one.svg?1791172800 | 396 / 540 | scryfall |
| Magic: The Gathering | Planar Chaos | https://svgs.scryfall.io/sets/plc.svg?1791172800 | 165 / 165 | scryfall |
| Magic: The Gathering | Planechase | https://svgs.scryfall.io/sets/hop.svg?1791172800 | 51 / 169 | scryfall |
| Magic: The Gathering | Planechase 2012 | https://svgs.scryfall.io/sets/pc2.svg?1791172800 | 156 / 156 | scryfall |
| Magic: The Gathering | Planechase Anthology | https://svgs.scryfall.io/sets/pca.svg?1791172800 | 170 / 170 | scryfall |
| Magic: The Gathering | Planechase: March of the Machine |  | 50 / 50 | — |
| Magic: The Gathering | Planechase: Universes Beyond: Doctor Who |  | 40 / 40 | — |
| Magic: The Gathering | Planeshift | https://svgs.scryfall.io/sets/pls.svg?1791172800 | 96 / 146 | scryfall |
| Magic: The Gathering | Planeswalker Event Promos |  | 44 / 48 | — |
| Magic: The Gathering | Play Promos |  | 11 / 11 | — |
| Magic: The Gathering | Ponies: The Galloping | https://svgs.scryfall.io/sets/ptg.svg?1791172800 | 3 / 3 | scryfall |
| Magic: The Gathering | Portal | https://svgs.scryfall.io/sets/por.svg?1791172800 | 145 / 257 | scryfall |
| Magic: The Gathering | Portal Second Age | https://svgs.scryfall.io/sets/p02.svg?1791172800 | 165 / 165 | scryfall |
| Magic: The Gathering | Portal Three Kingdoms | https://svgs.scryfall.io/sets/ptk.svg?1791172800 | 180 / 180 | scryfall |
| Magic: The Gathering | Premium Deck Series: Fire and Lightning | https://svgs.scryfall.io/sets/pd2.svg?1791172800 | 34 / 34 | scryfall |
| Magic: The Gathering | Premium Deck Series: Graveborn | https://svgs.scryfall.io/sets/pd3.svg?1791172800 | 30 / 30 | scryfall |
| Magic: The Gathering | Premium Deck Series: Slivers | https://svgs.scryfall.io/sets/h09.svg?1791172800 | 41 / 41 | scryfall |
| Magic: The Gathering | Prerelease Cards |  | 3691 / 4006 | — |
| Magic: The Gathering | Pro Tour Promos | https://svgs.scryfall.io/sets/star.svg?1791172800 | 26 / 26 | scryfall |
| Magic: The Gathering | Promo Pack: Adventures in the Forgotten Realms | https://svgs.scryfall.io/sets/afr.svg?1791172800 ※ | 88 / 88 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Aetherdrift | https://svgs.scryfall.io/sets/dft.svg?1791172800 ※ | 97 / 97 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Bloomburrow | https://svgs.scryfall.io/sets/blb.svg?1791172800 ※ | 85 / 85 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Core Set 2020 | https://svgs.scryfall.io/sets/m20.svg?1791172800 ※ | 197 / 199 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Core Set 2021 | https://svgs.scryfall.io/sets/m21.svg?1791172800 ※ | 91 / 91 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Dominaria United | https://svgs.scryfall.io/sets/dmu.svg?1791172800 ※ | 97 / 97 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Duskmourn: House of Horror | https://svgs.scryfall.io/sets/dsk.svg?1791172800 ※ | 89 / 89 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Edge of Eternities | https://svgs.scryfall.io/sets/eoe.svg?1791172800 ※ | 99 / 99 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Ikoria | https://svgs.scryfall.io/sets/iko.svg?1791172800 | 89 / 89 | scryfall |
| Magic: The Gathering | Promo Pack: Innistrad: Midnight Hunt | https://svgs.scryfall.io/sets/mid.svg?1791172800 ※ | 75 / 75 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Kaldheim | https://svgs.scryfall.io/sets/khm.svg?1791172800 ※ | 83 / 83 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Kamigawa: Neon Dynasty | https://svgs.scryfall.io/sets/neo.svg?1791172800 ※ | 81 / 81 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Lorwyn Eclipsed | https://svgs.scryfall.io/sets/ecl.svg?1791172800 ※ | 101 / 101 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: March of the Machine | https://svgs.scryfall.io/sets/mom.svg?1791172800 ※ | 60 / 60 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Murders at Karlov Manor | https://svgs.scryfall.io/sets/mkm.svg?1791172800 ※ | 111 / 112 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Outlaws of Thunder Junction | https://svgs.scryfall.io/sets/otj.svg?1791172800 ※ | 45 / 86 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Phyrexia: All Will Be One | https://svgs.scryfall.io/sets/one.svg?1791172800 ※ | 86 / 86 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Reality Fracture | https://svgs.scryfall.io/sets/fra.svg?1791172800 ※ | 0 / 96 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Secrets of Strixhaven | https://svgs.scryfall.io/sets/sos.svg?1791172800 ※ | 97 / 97 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Streets of New Capenna | https://svgs.scryfall.io/sets/snc.svg?1791172800 ※ | 160 / 160 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Strixhaven | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2806/logo.webp ※ | 76 / 81 | holodex（继承父系列） |
| Magic: The Gathering | Promo Pack: Tarkir: Dragonstorm | https://svgs.scryfall.io/sets/tdm.svg?1791172800 ※ | 86 / 86 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: The Brothers' War | https://svgs.scryfall.io/sets/bro.svg?1791172800 ※ | 0 / 89 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: The Lost Caverns of Ixalan | https://svgs.scryfall.io/sets/lci.svg?1791172800 ※ | 35 / 81 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Theros Beyond Death | https://svgs.scryfall.io/sets/thb.svg?1791172800 ※ | 111 / 111 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Throne of Eldraine | https://svgs.scryfall.io/sets/eld.svg?1791172800 ※ | 138 / 138 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Wilds of Eldraine | https://svgs.scryfall.io/sets/woe.svg?1791172800 ※ | 88 / 88 | scryfall（继承父系列） |
| Magic: The Gathering | Promo Pack: Zendikar Rising | https://svgs.scryfall.io/sets/znr.svg?1791172800 ※ | 82 / 82 | scryfall（继承父系列） |
| Magic: The Gathering | Prophecy | https://svgs.scryfall.io/sets/pcy.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | Ravnica Allegiance | https://svgs.scryfall.io/sets/rna.svg?1791172800 | 285 / 285 | scryfall |
| Magic: The Gathering | Ravnica Allegiance: Guild Kits | https://svgs.scryfall.io/sets/rna.svg?1791172800 | 141 / 141 | scryfall |
| Magic: The Gathering | Ravnica Remastered | https://svgs.scryfall.io/sets/rvr.svg?1791172800 | 624 / 625 | scryfall |
| Magic: The Gathering | Ravnica: City of Guilds | https://svgs.scryfall.io/sets/rav.svg?1791172800 | 256 / 306 | scryfall |
| Magic: The Gathering | Ravnica: Clue Edition | https://svgs.scryfall.io/sets/clu.svg?1791172800 | 294 / 294 | scryfall |
| Magic: The Gathering | Reality Fracture | https://svgs.scryfall.io/sets/fra.svg?1791172800 | 42 / 471 | scryfall |
| Magic: The Gathering | Renaissance | https://svgs.scryfall.io/sets/ren.svg?1791172800 | 311 / 311 | scryfall |
| Magic: The Gathering | Return to Ravnica | https://svgs.scryfall.io/sets/rtr.svg?1791172800 | 285 / 286 | scryfall |
| Magic: The Gathering | Revised Edition | https://svgs.scryfall.io/sets/3ed.svg?1791172800 | 304 / 305 | scryfall |
| Magic: The Gathering | Revised Edition (Foreign Black Border) | https://svgs.scryfall.io/sets/3ed.svg?1791172800 ※ | 305 / 305 | scryfall（继承父系列） |
| Magic: The Gathering | Revised Edition (Foreign White Border) | https://svgs.scryfall.io/sets/3ed.svg?1791172800 ※ | 305 / 305 | scryfall（继承父系列） |
| Magic: The Gathering | Rise of the Eldrazi | https://svgs.scryfall.io/sets/roe.svg?1791172800 | 204 / 255 | scryfall |
| Magic: The Gathering | Rivals of Ixalan | https://svgs.scryfall.io/sets/rix.svg?1791172800 | 212 / 212 | scryfall |
| Magic: The Gathering | SLX Cards | https://svgs.scryfall.io/sets/star.svg?1791172800 | 30 / 30 | scryfall |
| Magic: The Gathering | Saviors of Kamigawa | https://svgs.scryfall.io/sets/sok.svg?1791172800 | 115 / 165 | scryfall |
| Magic: The Gathering | Scars of Mirrodin | https://svgs.scryfall.io/sets/som.svg?1791172800 | 259 / 259 | scryfall |
| Magic: The Gathering | Scourge | https://svgs.scryfall.io/sets/scg.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | Secret Lair Countdown Kit | https://svgs.scryfall.io/sets/star.svg?1791172800 | 111 / 111 | scryfall |
| Magic: The Gathering | Secret Lair Drop Series | https://svgs.scryfall.io/sets/star.svg?1791172800 | 3119 / 3356 | scryfall |
| Magic: The Gathering | Secret Lair Series | https://svgs.scryfall.io/sets/star.svg?1791172800 | 16 / 16 | scryfall |
| Magic: The Gathering | Secret Lair Showdown | https://svgs.scryfall.io/sets/star.svg?1791172800 | 52 / 53 | scryfall |
| Magic: The Gathering | Secret Lair x MSCHF: The Zeta Set |  | 0 / 362 | — |
| Magic: The Gathering | Secrets of Strixhaven | https://svgs.scryfall.io/sets/sos.svg?1791172800 | 150 / 380 | scryfall |
| Magic: The Gathering | Secrets of Strixhaven: Mystical Archive | https://svgs.scryfall.io/sets/soa.svg?1791172800 | 195 / 195 | scryfall |
| Magic: The Gathering | Shadowmoor | https://svgs.scryfall.io/sets/shm.svg?1791172800 | 313 / 313 | scryfall |
| Magic: The Gathering | Shadows over Innistrad | https://svgs.scryfall.io/sets/soi.svg?1791172800 | 332 / 332 | scryfall |
| Magic: The Gathering | Shards of Alara | https://svgs.scryfall.io/sets/ala.svg?1791172800 | 209 / 259 | scryfall |
| Magic: The Gathering | Signature Spellbook: Chandra | https://svgs.scryfall.io/sets/ss3.svg?1791172800 | 8 / 8 | scryfall |
| Magic: The Gathering | Signature Spellbook: Gideon | https://svgs.scryfall.io/sets/ss2.svg?1791172800 | 8 / 8 | scryfall |
| Magic: The Gathering | Signature Spellbook: Jace | https://svgs.scryfall.io/sets/ss1.svg?1791172800 | 8 / 8 | scryfall |
| Magic: The Gathering | Special Guests | https://svgs.scryfall.io/sets/spg.svg?1791172800 | 164 / 174 | scryfall |
| Magic: The Gathering | Special Occasion |  | 30 / 30 | — |
| Magic: The Gathering | Standard Showdown Promos | https://svgs.scryfall.io/sets/star.svg?1791172800 | 51 / 51 | scryfall |
| Magic: The Gathering | Star Trek | https://svgs.scryfall.io/sets/trk.svg?1791172800 | 56 / 56 | scryfall |
| Magic: The Gathering | Star Trek: Stardates | https://svgs.scryfall.io/sets/sds.svg?1791172800 | 1 / 1 | scryfall |
| Magic: The Gathering | Starter 1999 | https://svgs.scryfall.io/sets/s99.svg?1791172800 | 173 / 173 | scryfall |
| Magic: The Gathering | Starter 2000 | https://svgs.scryfall.io/sets/s00.svg?1791172800 | 20 / 20 | scryfall |
| Magic: The Gathering | Starter Commander Decks | https://svgs.scryfall.io/sets/scd.svg?1791172800 | 382 / 382 | scryfall |
| Magic: The Gathering | Streets of New Capenna | https://svgs.scryfall.io/sets/snc.svg?1791172800 | 530 / 538 | scryfall |
| Magic: The Gathering | Strixhaven: Mystical Archive | https://svgs.scryfall.io/sets/sta.svg?1791172800 | 250 / 252 | scryfall |
| Magic: The Gathering | Strixhaven: School of Mages | https://svgs.scryfall.io/sets/stx.svg?1791172800 | 419 / 419 | scryfall |
| Magic: The Gathering | Stronghold | https://svgs.scryfall.io/sets/sth.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | Summer Magic | https://svgs.scryfall.io/sets/psum.svg?1791172800 | 305 / 305 | scryfall |
| Magic: The Gathering | Tarkir Dragonfury Promos | https://svgs.scryfall.io/sets/tdm.svg?1791172800 | 4 / 4 | scryfall |
| Magic: The Gathering | Tarkir: Dragonstorm | https://svgs.scryfall.io/sets/tdm.svg?1791172800 | 171 / 431 | scryfall |
| Magic: The Gathering | Teenage Mutant Ninja Turtles | https://svgs.scryfall.io/sets/tmt.svg?1791172800 | 240 / 332 | scryfall |
| Magic: The Gathering | Teenage Mutant Ninja Turtles Source Material | https://svgs.scryfall.io/sets/pza.svg?1791172800 | 20 / 20 | scryfall |
| Magic: The Gathering | Tempest | https://svgs.scryfall.io/sets/tmp.svg?1791172800 | 350 / 350 | scryfall |
| Magic: The Gathering | The Brothers' War | https://svgs.scryfall.io/sets/bro.svg?1791172800 | 0 / 417 | scryfall |
| Magic: The Gathering | The Brothers' War: Retro Frame Artifacts | https://holodex-prod-bucket.b-cdn.net/sets/mtg_17665/logo.webp | 0 / 189 | holodex |
| Magic: The Gathering | The Dark | https://svgs.scryfall.io/sets/drk.svg?1791172800 | 119 / 119 | scryfall |
| Magic: The Gathering | The Hobbit | https://svgs.scryfall.io/sets/hob.svg?1791172800 | 286 / 334 | scryfall |
| Magic: The Gathering | The Hobbit: Eternal-Legal | https://svgs.scryfall.io/sets/hoc.svg?1791172800 | 158 / 158 | scryfall |
| Magic: The Gathering | The List Reprints | https://svgs.scryfall.io/sets/planeswalker.svg?1791172800 | 5025 / 5302 | scryfall |
| Magic: The Gathering | The Lost Caverns of Ixalan | https://svgs.scryfall.io/sets/lci.svg?1791172800 | 223 / 480 | scryfall |
| Magic: The Gathering | Theros | https://svgs.scryfall.io/sets/ths.svg?1791172800 | 94 / 260 | scryfall |
| Magic: The Gathering | Theros Beyond Death | https://svgs.scryfall.io/sets/thb.svg?1791172800 | 387 / 388 | scryfall |
| Magic: The Gathering | Throne of Eldraine | https://svgs.scryfall.io/sets/eld.svg?1791172800 | 459 / 459 | scryfall |
| Magic: The Gathering | Time Spiral | https://svgs.scryfall.io/sets/tsp.svg?1791172800 | 122 / 301 | scryfall |
| Magic: The Gathering | Time Spiral: Remastered | https://svgs.scryfall.io/sets/tsr.svg?1791172800 | 425 / 425 | scryfall |
| Magic: The Gathering | Timeshifted | https://svgs.scryfall.io/sets/tsp.svg?1791172800 | 71 / 121 | scryfall |
| Magic: The Gathering | Torment | https://svgs.scryfall.io/sets/tor.svg?1791172800 | 143 / 143 | scryfall |
| Magic: The Gathering | Ugin's Fate Promos | https://svgs.scryfall.io/sets/frf.svg?1791172800 | 0 / 26 | scryfall |
| Magic: The Gathering | Ultimate Masters | https://svgs.scryfall.io/sets/uma.svg?1791172800 | 270 / 270 | scryfall |
| Magic: The Gathering | Ultimate Masters: Box Toppers | https://svgs.scryfall.io/sets/uma.svg?1791172800 ※ | 40 / 40 | scryfall（继承父系列） |
| Magic: The Gathering | Un-Known Event Playtest Cards | https://svgs.scryfall.io/sets/planeswalker.svg?1791172800 | 396 / 434 | scryfall |
| Magic: The Gathering | Unfinity | https://svgs.scryfall.io/sets/unf.svg?1791172800 | 729 / 734 | scryfall |
| Magic: The Gathering | Unglued | https://svgs.scryfall.io/sets/ugl.svg?1791172800 | 94 / 94 | scryfall |
| Magic: The Gathering | Unhinged | https://svgs.scryfall.io/sets/unh.svg?1791172800 | 159 / 160 | scryfall |
| Magic: The Gathering | Unique and Miscellaneous Promos |  | 327 / 331 | — |
| Magic: The Gathering | Universes Beyond: Assassin's Creed | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23446/logo.webp | 0 / 325 | holodex |
| Magic: The Gathering | Universes Beyond: Doctor Who | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23165/logo.webp | 1188 / 1335 | holodex |
| Magic: The Gathering | Universes Beyond: Fallout | https://svgs.scryfall.io/sets/pip.svg?1791172800 | 1043 / 1151 | scryfall |
| Magic: The Gathering | Universes Beyond: Jurassic World Collection | https://svgs.scryfall.io/sets/rex.svg?1791172800 | 56 / 56 | scryfall |
| Magic: The Gathering | Universes Beyond: The Lord of the Rings: Tales of Middle-earth | https://svgs.scryfall.io/sets/ltr.svg?1791172800 | 772 / 934 | scryfall |
| Magic: The Gathering | Universes Beyond: Transformers | https://svgs.scryfall.io/sets/bot.svg?1791172800 | 31 / 31 | scryfall |
| Magic: The Gathering | Universes Beyond: Warhammer 40,000 | https://svgs.scryfall.io/sets/40k.svg?1791172800 | 649 / 650 | scryfall |
| Magic: The Gathering | Unlimited Edition | https://svgs.scryfall.io/sets/2ed.svg?1791172800 | 251 / 301 | scryfall |
| Magic: The Gathering | Unsanctioned | https://svgs.scryfall.io/sets/und.svg?1791172800 | 100 / 100 | scryfall |
| Magic: The Gathering | Unstable | https://svgs.scryfall.io/sets/ust.svg?1791172800 | 288 / 288 | scryfall |
| Magic: The Gathering | Urza's Destiny | https://svgs.scryfall.io/sets/uds.svg?1791172800 | 0 / 143 | scryfall |
| Magic: The Gathering | Urza's Legacy | https://svgs.scryfall.io/sets/ulg.svg?1791172800 | 0 / 143 | scryfall |
| Magic: The Gathering | Urza's Saga | https://svgs.scryfall.io/sets/usg.svg?1791172800 | 0 / 350 | scryfall |
| Magic: The Gathering | Vanguard | https://holodex-prod-bucket.b-cdn.net/sets/mtg_119/logo.webp | 32 / 32 | holodex |
| Magic: The Gathering | Visions | https://svgs.scryfall.io/sets/vis.svg?1791172800 | 117 / 167 | scryfall |
| Magic: The Gathering | WMCQ Promo Cards | https://svgs.scryfall.io/sets/star.svg?1791172800 | 6 / 6 | scryfall |
| Magic: The Gathering | WPN & Gateway Promos |  | 20 / 121 | — |
| Magic: The Gathering | War of the Spark | https://svgs.scryfall.io/sets/war.svg?1791172800 | 329 / 329 | scryfall |
| Magic: The Gathering | Weatherlight | https://svgs.scryfall.io/sets/wth.svg?1791172800 | 117 / 167 | scryfall |
| Magic: The Gathering | Welcome Deck 2016 | https://svgs.scryfall.io/sets/w16.svg?1791172800 | 16 / 16 | scryfall |
| Magic: The Gathering | Welcome Deck 2017 | https://svgs.scryfall.io/sets/w17.svg?1791172800 | 30 / 30 | scryfall |
| Magic: The Gathering | Wilds of Eldraine | https://svgs.scryfall.io/sets/woe.svg?1791172800 | 242 / 437 | scryfall |
| Magic: The Gathering | Wilds of Eldraine: Enchanting Tales | https://svgs.scryfall.io/sets/wot.svg?1791172800 | 103 / 103 | scryfall |
| Magic: The Gathering | World Championship Decks | https://svgs.scryfall.io/sets/default.svg?1791172800 | 1330 / 1335 | scryfall |
| Magic: The Gathering | Worldwake | https://svgs.scryfall.io/sets/wwk.svg?1791172800 | 151 / 151 | scryfall |
| Magic: The Gathering | Zendikar | https://svgs.scryfall.io/sets/zen.svg?1791172800 | 60 / 280 | scryfall |
| Magic: The Gathering | Zendikar Expeditions | https://svgs.scryfall.io/sets/exp.svg?1791172800 | 45 / 45 | scryfall |
| Magic: The Gathering | Zendikar Rising | https://svgs.scryfall.io/sets/znr.svg?1791172800 | 443 / 446 | scryfall |
| Magic: The Gathering | Zendikar Rising Expeditions | https://svgs.scryfall.io/sets/zne.svg?1791172800 | 30 / 30 | scryfall |

### Yu-Gi-Oh!（613 个系列，514 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Yu-Gi-Oh! | 2-Player Starter Set |  | 88 / 88 | — |
| Yu-Gi-Oh! | 2002 Collectors Tin |  | 6 / 6 | — |
| Yu-Gi-Oh! | 2003 Collectors Tin |  | 6 / 6 | — |
| Yu-Gi-Oh! | 2004 Collectors Tin |  | 6 / 6 | — |
| Yu-Gi-Oh! | 2005 Collectors Tin | https://images.ygoprodeck.com/images/sets/CT2.jpg | 6 / 6 | ygoprodeck |
| Yu-Gi-Oh! | 2006 Collectors Tin | https://images.ygoprodeck.com/images/sets/CT03.jpg | 6 / 6 | ygoprodeck |
| Yu-Gi-Oh! | 2007 Collectors Tin | https://images.ygoprodeck.com/images/sets/CT04.jpg | 6 / 6 | ygoprodeck |
| Yu-Gi-Oh! | 2008 Collectors Tin | https://images.ygoprodeck.com/images/sets/CT05.jpg | 7 / 7 | ygoprodeck |
| Yu-Gi-Oh! | 2009 Collectors Tin | https://images.ygoprodeck.com/images/sets/CT06.jpg | 8 / 8 | ygoprodeck |
| Yu-Gi-Oh! | 2010 Collectors Tins | https://images.ygoprodeck.com/images/sets/CT07.jpg | 25 / 25 | ygoprodeck |
| Yu-Gi-Oh! | 2010 Duelist Pack Collection Tin | https://images.ygoprodeck.com/images/sets/DPCT.jpg | 10 / 10 | ygoprodeck |
| Yu-Gi-Oh! | 2011 Collectors Tins | https://images.ygoprodeck.com/images/sets/CT08.jpg | 18 / 18 | ygoprodeck |
| Yu-Gi-Oh! | 2011 Duelist Pack Tin |  | 4 / 4 | — |
| Yu-Gi-Oh! | 2012 Collectors Tin | https://images.ygoprodeck.com/images/sets/CT09.jpg | 23 / 23 | ygoprodeck |
| Yu-Gi-Oh! | 2012 Premium Collection Tin | https://images.ygoprodeck.com/images/sets/PRC1.jpg | 25 / 25 | ygoprodeck |
| Yu-Gi-Oh! | 2013 Collectors Tins | https://images.ygoprodeck.com/images/sets/CT10.jpg | 18 / 18 | ygoprodeck |
| Yu-Gi-Oh! | 2013 Zexal Collection Tin | https://images.ygoprodeck.com/images/sets/ZTIN.jpg | 24 / 24 | ygoprodeck |
| Yu-Gi-Oh! | 2014 Mega-Tins | https://images.ygoprodeck.com/images/sets/CT11.jpg | 6 / 6 | ygoprodeck |
| Yu-Gi-Oh! | 2014 Mega-Tins Mega Pack | https://images.ygoprodeck.com/images/sets/MP14.jpg | 197 / 247 | ygoprodeck |
| Yu-Gi-Oh! | 2015 Mega-Tins | https://images.ygoprodeck.com/images/sets/CT12.jpg | 6 / 6 | ygoprodeck |
| Yu-Gi-Oh! | 2015 Mega-Tins Mega Pack | https://images.ygoprodeck.com/images/sets/MP15.jpg | 247 / 247 | ygoprodeck |
| Yu-Gi-Oh! | 2016 Mega-Tins | https://images.ygoprodeck.com/images/sets/CT13.jpg | 12 / 12 | ygoprodeck |
| Yu-Gi-Oh! | 2016 Mega-Tins Mega Pack | https://images.ygoprodeck.com/images/sets/MP16.jpg | 239 / 239 | ygoprodeck |
| Yu-Gi-Oh! | 2017 Mega-Tins | https://images.ygoprodeck.com/images/sets/CT14.jpg | 10 / 10 | ygoprodeck |
| Yu-Gi-Oh! | 2017 Mega-Tins Mega Pack | https://images.ygoprodeck.com/images/sets/MP17.jpg | 239 / 239 | ygoprodeck |
| Yu-Gi-Oh! | 2018 Mega-Tins | https://images.ygoprodeck.com/images/sets/CT15.jpg | 10 / 10 | ygoprodeck |
| Yu-Gi-Oh! | 2018 Mega-Tins Mega Pack | https://images.ygoprodeck.com/images/sets/MP18.jpg | 233 / 233 | ygoprodeck |
| Yu-Gi-Oh! | 2019 Gold Sarcophagus Tin | https://images.ygoprodeck.com/images/sets/TN19.jpg | 14 / 14 | ygoprodeck |
| Yu-Gi-Oh! | 2019 Gold Sarcophagus Tin Mega Pack | https://images.ygoprodeck.com/images/sets/MP19.jpg | 270 / 270 | ygoprodeck |
| Yu-Gi-Oh! | 2020 Tin of Lost Memories | https://images.ygoprodeck.com/images/sets/MP20.jpg | 249 / 249 | ygoprodeck |
| Yu-Gi-Oh! | 2021 Tin of Ancient Battles | https://images.ygoprodeck.com/images/sets/MP21.jpg | 258 / 258 | ygoprodeck |
| Yu-Gi-Oh! | 2022 Tin of the Pharaoh's Gods | https://images.ygoprodeck.com/images/sets/MP22.jpg | 0 / 275 | ygoprodeck |
| Yu-Gi-Oh! | 2025 Mega-Pack | https://images.ygoprodeck.com/images/sets/MP25.jpg | 400 / 450 | ygoprodeck |
| Yu-Gi-Oh! | 25th Anniversary Rarity Collection | https://images.ygoprodeck.com/images/sets/RA01.jpg | 263 / 567 | ygoprodeck |
| Yu-Gi-Oh! | 25th Anniversary Rarity Collection II | https://images.ygoprodeck.com/images/sets/RA02.jpg | 467 / 567 | ygoprodeck |
| Yu-Gi-Oh! | 25th Anniversary Tin: Dueling Heroes | https://images.ygoprodeck.com/images/sets/TN23.jpg | 2 / 16 | ygoprodeck |
| Yu-Gi-Oh! | 25th Anniversary Tin: Dueling Heroes Mega Pack | https://images.ygoprodeck.com/images/sets/MP23.jpg | 283 / 283 | ygoprodeck |
| Yu-Gi-Oh! | 25th Anniversary Tin: Dueling Mirrors |  | 400 / 400 | — |
| Yu-Gi-Oh! | 25th Anniversary Ultimate Kaiba Set | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23366/logo.webp | 63 / 63 | holodex |
| Yu-Gi-Oh! | 5D's 2008 Starter Deck | https://images.ygoprodeck.com/images/sets/5DS1.jpg | 46 / 46 | ygoprodeck |
| Yu-Gi-Oh! | 5D's Starter Deck 2009 | https://images.ygoprodeck.com/images/sets/5DS2.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Absolute Powerforce | https://images.ygoprodeck.com/images/sets/ABPF.jpg | 115 / 115 | ygoprodeck |
| Yu-Gi-Oh! | Abyss Rising | https://images.ygoprodeck.com/images/sets/ABYR.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Advanced Demo Deck Extra Pack | https://images.ygoprodeck.com/images/sets/DEM4.jpg | 10 / 10 | ygoprodeck |
| Yu-Gi-Oh! | Advent Calendar 2011 (Adventskalender) |  | 24 / 24 | — |
| Yu-Gi-Oh! | Advent Calendar 2014 (Adventskalender ZEXAL-Edition) |  | 24 / 24 | — |
| Yu-Gi-Oh! | Advent Calendar 2018 | https://images.ygoprodeck.com/images/sets/AC18.jpg | 24 / 24 | ygoprodeck |
| Yu-Gi-Oh! | Advent Calendar 2019 | https://images.ygoprodeck.com/images/sets/AC19.jpg | 24 / 24 | ygoprodeck |
| Yu-Gi-Oh! | Age of Overlord | https://images.ygoprodeck.com/images/sets/AGOV.jpg | 126 / 126 | ygoprodeck |
| Yu-Gi-Oh! | Alliance Insight | https://images.ygoprodeck.com/images/sets/ALIN.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Amazing Defenders | https://images.ygoprodeck.com/images/sets/AMDE.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | Ancient Guardians | https://images.ygoprodeck.com/images/sets/ANGU.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | Ancient Prophecy | https://images.ygoprodeck.com/images/sets/ANPR.jpg | 113 / 113 | ygoprodeck |
| Yu-Gi-Oh! | Ancient Prophecy SE | https://images.ygoprodeck.com/images/sets/ANPR.jpg ※ | 2 / 2 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Ancient Sanctuary | https://images.ygoprodeck.com/images/sets/AST.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Anniversary Pack | https://images.ygoprodeck.com/images/sets/YAP1.jpg | 0 / 8 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 1 | https://images.ygoprodeck.com/images/sets/AP01.jpg | 25 / 25 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 2 | https://images.ygoprodeck.com/images/sets/AP02.jpg | 25 / 25 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 3 | https://images.ygoprodeck.com/images/sets/AP03.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 4 | https://images.ygoprodeck.com/images/sets/AP04.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 5 | https://images.ygoprodeck.com/images/sets/AP05.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 6 | https://images.ygoprodeck.com/images/sets/AP06.jpg | 28 / 28 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 7 | https://images.ygoprodeck.com/images/sets/AP07.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | Astral Pack 8 | https://images.ygoprodeck.com/images/sets/AP08.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | Battle Pack 2: War of the Giants | https://images.ygoprodeck.com/images/sets/BP02.jpg | 367 / 427 | ygoprodeck |
| Yu-Gi-Oh! | Battle Pack 2: War of the Giants Round 2 | https://images.ygoprodeck.com/images/sets/BPW2.jpg | 102 / 103 | ygoprodeck |
| Yu-Gi-Oh! | Battle Pack 3: Monster League | https://images.ygoprodeck.com/images/sets/BP03.jpg | 457 / 457 | ygoprodeck |
| Yu-Gi-Oh! | Battle Pack Tournament Prize Cards | https://images.ygoprodeck.com/images/sets/BATT.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Battle Pack: Epic Dawn | https://images.ygoprodeck.com/images/sets/BP01.jpg | 431 / 440 | ygoprodeck |
| Yu-Gi-Oh! | Battle of Chaos | https://images.ygoprodeck.com/images/sets/BACH.jpg | 107 / 107 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Armageddon | https://images.ygoprodeck.com/images/sets/BLAR.jpg | 94 / 94 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Chapter 1 | https://images.ygoprodeck.com/images/sets/BLC1.jpg | 199 / 199 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Crystal Revenge | https://images.ygoprodeck.com/images/sets/BLCR.jpg | 107 / 107 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Glorious Gallery | https://images.ygoprodeck.com/images/sets/BLGG.jpg | 181 / 181 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Hero's Revenge | https://images.ygoprodeck.com/images/sets/BLHR.jpg | 94 / 94 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Light's Revenge | https://images.ygoprodeck.com/images/sets/BLLR.jpg | 80 / 80 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Monster Mayhem | https://images.ygoprodeck.com/images/sets/BLMM.jpg | 202 / 202 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Monstrous Revenge | https://images.ygoprodeck.com/images/sets/BLMR.jpg | 127 / 127 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Relentless Revenge | https://images.ygoprodeck.com/images/sets/BLRR.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Battles of Legend: Terminal Revenge | https://images.ygoprodeck.com/images/sets/BLTR.jpg | 140 / 140 | ygoprodeck |
| Yu-Gi-Oh! | Beyond the Brave | https://images.ygoprodeck.com/images/sets/BETB.jpg | 0 / 135 | ygoprodeck |
| Yu-Gi-Oh! | Blazing Dominion | https://images.ygoprodeck.com/images/sets/BLZD.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Blazing Vortex | https://images.ygoprodeck.com/images/sets/BLVO.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Bonds Beyond Time Movie Pack | https://images.ygoprodeck.com/images/sets/YMP1.jpg | 11 / 11 | ygoprodeck |
| Yu-Gi-Oh! | Breakers of Shadow | https://images.ygoprodeck.com/images/sets/BOSH.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Brothers of Legend | https://images.ygoprodeck.com/images/sets/BROL.jpg | 95 / 95 | ygoprodeck |
| Yu-Gi-Oh! | Burst Protocol | https://images.ygoprodeck.com/images/sets/BPRO.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Burst of Destiny | https://images.ygoprodeck.com/images/sets/BODE.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 1 | https://images.ygoprodeck.com/images/sets/CP01.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 2 | https://images.ygoprodeck.com/images/sets/CP02.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 3 | https://images.ygoprodeck.com/images/sets/CP03.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 4 | https://images.ygoprodeck.com/images/sets/CP04.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 5 | https://images.ygoprodeck.com/images/sets/CP05.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 6 | https://images.ygoprodeck.com/images/sets/CP06.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 7 | https://images.ygoprodeck.com/images/sets/CP07.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Champion Pack 8 | https://images.ygoprodeck.com/images/sets/CP08.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Chaos Impact | https://images.ygoprodeck.com/images/sets/CHIM.jpg | 109 / 109 | ygoprodeck |
| Yu-Gi-Oh! | Chaos Origins | https://images.ygoprodeck.com/images/sets/CORI.jpg | 136 / 136 | ygoprodeck |
| Yu-Gi-Oh! | Circuit Break | https://images.ygoprodeck.com/images/sets/CIBR.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Clash of Rebellions | https://images.ygoprodeck.com/images/sets/CORE.jpg | 111 / 111 | ygoprodeck |
| Yu-Gi-Oh! | Code of the Duelist | https://images.ygoprodeck.com/images/sets/COTD.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Collector's Boxes |  | 4 / 4 | — |
| Yu-Gi-Oh! | Cosmo Blazer | https://images.ygoprodeck.com/images/sets/CBLZ.jpg | 111 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Cosmo Blazer SE | https://images.ygoprodeck.com/images/sets/CBLZ.jpg ※ | 2 / 2 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Crimson Crisis | https://images.ygoprodeck.com/images/sets/CRMS.jpg | 113 / 113 | ygoprodeck |
| Yu-Gi-Oh! | Crossed Souls | https://images.ygoprodeck.com/images/sets/CROS.jpg | 107 / 107 | ygoprodeck |
| Yu-Gi-Oh! | Crossed Souls: Advanced Edition |  | 4 / 4 | — |
| Yu-Gi-Oh! | Crossover Breakers | https://images.ygoprodeck.com/images/sets/CRBR.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Crossroads of Chaos | https://images.ygoprodeck.com/images/sets/CSOC.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Cyberdark Impact | https://images.ygoprodeck.com/images/sets/CDIP.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Cybernetic Horizon | https://images.ygoprodeck.com/images/sets/CYHO.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Cybernetic Revolution | https://images.ygoprodeck.com/images/sets/CRV.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Cyberstorm Access | https://images.ygoprodeck.com/images/sets/CYAC.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Dark Beginning 1 | https://images.ygoprodeck.com/images/sets/DB1.jpg | 249 / 250 | ygoprodeck |
| Yu-Gi-Oh! | Dark Beginning 2 | https://images.ygoprodeck.com/images/sets/DB2.jpg | 250 / 250 | ygoprodeck |
| Yu-Gi-Oh! | Dark Crisis | https://images.ygoprodeck.com/images/sets/DCR.jpg | 99 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Dark Crisis (25th Anniversary Edition) | https://images.ygoprodeck.com/images/sets/DCR.jpg | 50 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Dark Crisis (Worldwide English) | https://images.ygoprodeck.com/images/sets/DCR.jpg ※ | 7 / 106 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Dark Legends | https://images.ygoprodeck.com/images/sets/DLG1.jpg | 113 / 113 | ygoprodeck |
| Yu-Gi-Oh! | Dark Neostorm | https://images.ygoprodeck.com/images/sets/DANE.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Dark Revelation Volume 1 | https://images.ygoprodeck.com/images/sets/DR1.jpg | 264 / 267 | ygoprodeck |
| Yu-Gi-Oh! | Dark Revelation Volume 2 | https://images.ygoprodeck.com/images/sets/DR2.jpg | 224 / 224 | ygoprodeck |
| Yu-Gi-Oh! | Dark Revelation Volume 3 | https://images.ygoprodeck.com/images/sets/DR3.jpg | 238 / 240 | ygoprodeck |
| Yu-Gi-Oh! | Dark Revelation Volume 4 | https://images.ygoprodeck.com/images/sets/DR04.jpg | 245 / 245 | ygoprodeck |
| Yu-Gi-Oh! | Dark Saviors | https://images.ygoprodeck.com/images/sets/DASA.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Darkwing Blast | https://images.ygoprodeck.com/images/sets/DABL.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Dawn of Destiny Xbox |  | 6 / 6 | — |
| Yu-Gi-Oh! | Dawn of Majesty | https://images.ygoprodeck.com/images/sets/DAMA.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Demo Deck 2015 | https://images.ygoprodeck.com/images/sets/DEM2.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Demo Deck 2016 | https://images.ygoprodeck.com/images/sets/DEM3.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Demo Pack | https://images.ygoprodeck.com/images/sets/DEM1.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Destiny Board Traveler Promo |  | 3 / 3 | — |
| Yu-Gi-Oh! | Destiny Soldiers | https://images.ygoprodeck.com/images/sets/DESO.jpg | 55 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Dimension Force | https://images.ygoprodeck.com/images/sets/DIFO.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Dimension of Chaos | https://images.ygoprodeck.com/images/sets/DOCS.jpg | 111 / 111 | ygoprodeck |
| Yu-Gi-Oh! | Doom of Dimensions | https://images.ygoprodeck.com/images/sets/DOOD.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Dragons of Legend | https://images.ygoprodeck.com/images/sets/DRLG.jpg | 22 / 51 | ygoprodeck |
| Yu-Gi-Oh! | Dragons of Legend 2 | https://images.ygoprodeck.com/images/sets/DRL2.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Dragons of Legend: The Complete Series | https://images.ygoprodeck.com/images/sets/DLCS.jpg | 239 / 240 | ygoprodeck |
| Yu-Gi-Oh! | Dragons of Legend: Unleashed | https://images.ygoprodeck.com/images/sets/DRL3.jpg | 73 / 73 | ygoprodeck |
| Yu-Gi-Oh! | Duel Devastator | https://images.ygoprodeck.com/images/sets/DUDE.jpg | 56 / 56 | ygoprodeck |
| Yu-Gi-Oh! | Duel Master's Guide | https://images.ygoprodeck.com/images/sets/DMG.jpg | 1 / 1 | ygoprodeck |
| Yu-Gi-Oh! | Duel Overload | https://images.ygoprodeck.com/images/sets/DUOV.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Duel Power | https://images.ygoprodeck.com/images/sets/DUPO.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Duel Terminal - Preview |  | 31 / 31 | — |
| Yu-Gi-Oh! | Duel Terminal 1 |  | 100 / 100 | — |
| Yu-Gi-Oh! | Duel Terminal 2 | https://images.ygoprodeck.com/images/sets/DT02.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duel Terminal 3 | https://images.ygoprodeck.com/images/sets/DT03.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duel Terminal 4 | https://images.ygoprodeck.com/images/sets/DT04.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duel Terminal 5 | https://images.ygoprodeck.com/images/sets/DT05.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duel Terminal 6 | https://images.ygoprodeck.com/images/sets/DT06.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duel Terminal 7 | https://images.ygoprodeck.com/images/sets/DT07.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Alliance | https://images.ygoprodeck.com/images/sets/DUEA.jpg | 107 / 107 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Alliance: Deluxe Edition | https://images.ygoprodeck.com/images/sets/DUEA.jpg | 7 / 7 | ygoprodeck |
| Yu-Gi-Oh! | Duelist League Demo 2010 | https://images.ygoprodeck.com/images/sets/DLDI.jpg | 5 / 5 | ygoprodeck |
| Yu-Gi-Oh! | Duelist League Promo |  | 726 / 732 | — |
| Yu-Gi-Oh! | Duelist Nexus | https://images.ygoprodeck.com/images/sets/DUNE.jpg | 125 / 125 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 10: Yusei 3 | https://images.ygoprodeck.com/images/sets/DP10.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 11: Crow | https://images.ygoprodeck.com/images/sets/DP11.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 1: Jaden Yuki | https://images.ygoprodeck.com/images/sets/DP1.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 2: Chazz Princeton | https://images.ygoprodeck.com/images/sets/DP2.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 3: Jaden Yuki 2 | https://images.ygoprodeck.com/images/sets/DP03.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 4: Zane Truesdale | https://images.ygoprodeck.com/images/sets/DP04.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 5: Aster Phoenix | https://images.ygoprodeck.com/images/sets/DP05.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 6: Jaden Yuki 3 | https://images.ygoprodeck.com/images/sets/DP06.jpg | 25 / 25 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 7: Jesse Anderson | https://images.ygoprodeck.com/images/sets/DP07.jpg | 25 / 25 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 8: Yusei Fudo | https://images.ygoprodeck.com/images/sets/DP08.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack 9: Yusei 2 | https://images.ygoprodeck.com/images/sets/DP09.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack Collection Tin |  | 10 / 10 | — |
| Yu-Gi-Oh! | Duelist Pack Special Edition |  | 3 / 3 | — |
| Yu-Gi-Oh! | Duelist Pack: Battle City | https://images.ygoprodeck.com/images/sets/DPBC.jpg | 47 / 47 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack: Dimensional Guardians | https://images.ygoprodeck.com/images/sets/DPDG.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack: Kaiba | https://images.ygoprodeck.com/images/sets/DPKB.jpg | 40 / 40 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack: Rivals of the Pharaoh | https://images.ygoprodeck.com/images/sets/DPRP.jpg | 46 / 46 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Pack: Yugi | https://images.ygoprodeck.com/images/sets/DPYG.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Revolution | https://images.ygoprodeck.com/images/sets/DREV.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Duelist Saga | https://images.ygoprodeck.com/images/sets/DUSA.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Duelist of the Roses |  | 3 / 3 | — |
| Yu-Gi-Oh! | Duelist's Advance | https://images.ygoprodeck.com/images/sets/DUAD.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Early Days Collection Promotional Cards |  | 2 / 2 | — |
| Yu-Gi-Oh! | Egyptian God Deck: Obelisk the Tormentor | https://images.ygoprodeck.com/images/sets/EGO1.jpg | 35 / 35 | ygoprodeck |
| Yu-Gi-Oh! | Egyptian God Deck: Slifer the Sky Dragon | https://images.ygoprodeck.com/images/sets/EGS1.jpg | 38 / 38 | ygoprodeck |
| Yu-Gi-Oh! | Elemental Energy | https://images.ygoprodeck.com/images/sets/EEN.jpg | 90 / 90 | ygoprodeck |
| Yu-Gi-Oh! | Elemental Hero Collection 1 |  | 4 / 4 | — |
| Yu-Gi-Oh! | Elemental Hero Collection 2 |  | 4 / 4 | — |
| Yu-Gi-Oh! | Enemy of Justice | https://images.ygoprodeck.com/images/sets/EOJ.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Eternal Duelist Soul |  | 3 / 3 | — |
| Yu-Gi-Oh! | Eternity Code | https://images.ygoprodeck.com/images/sets/ETCO.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Event Pack Speed Duel | https://images.ygoprodeck.com/images/sets/EVSD.jpg | 7 / 7 | ygoprodeck |
| Yu-Gi-Oh! | Extreme Force | https://images.ygoprodeck.com/images/sets/EXFO.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Extreme Victory | https://images.ygoprodeck.com/images/sets/EXVC.jpg | 111 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Fire Fists Special Editon | https://images.ygoprodeck.com/images/sets/FFSE.jpg | 1 / 1 | ygoprodeck |
| Yu-Gi-Oh! | Fists of the Gadgets | https://images.ygoprodeck.com/images/sets/FIGA.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Flames of Destruction | https://images.ygoprodeck.com/images/sets/FLOD.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Flaming Eternity | https://images.ygoprodeck.com/images/sets/FET.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Forbidden Legacy |  | 3 / 3 | — |
| Yu-Gi-Oh! | Force of the Breaker | https://images.ygoprodeck.com/images/sets/FOTB.jpg | 96 / 96 | ygoprodeck |
| Yu-Gi-Oh! | Fusion Enforcers | https://images.ygoprodeck.com/images/sets/FUEN.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | GX Duel Academy GBA Promo |  | 3 / 3 | — |
| Yu-Gi-Oh! | GX Next Generation Blister Pack Promo | https://images.ygoprodeck.com/images/sets/GXNG.jpg | 1 / 1 | ygoprodeck |
| Yu-Gi-Oh! | GX Spirit Caller Promo |  | 3 / 3 | — |
| Yu-Gi-Oh! | GX Tag Force Promo |  | 3 / 3 | — |
| Yu-Gi-Oh! | GX Ultimate Beginner's Pack 1 |  | 5 / 5 | — |
| Yu-Gi-Oh! | Galactic Overlord | https://images.ygoprodeck.com/images/sets/GAOV.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Generation Force | https://images.ygoprodeck.com/images/sets/GENF.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Genesis Impact | https://images.ygoprodeck.com/images/sets/GEIM.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | Ghosts From the Past | https://images.ygoprodeck.com/images/sets/GFTP.jpg | 132 / 132 | ygoprodeck |
| Yu-Gi-Oh! | Ghosts From the Past: The 2nd Haunting | https://images.ygoprodeck.com/images/sets/GFP2.jpg | 183 / 183 | ygoprodeck |
| Yu-Gi-Oh! | Gladiator's Assault | https://images.ygoprodeck.com/images/sets/GLAS.jpg | 111 / 111 | ygoprodeck |
| Yu-Gi-Oh! | Gladiator's Assault SE | https://images.ygoprodeck.com/images/sets/GLAS.jpg ※ | 2 / 2 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Gold Series 2008 | https://images.ygoprodeck.com/images/sets/GLD1.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Gold Series 2009 | https://images.ygoprodeck.com/images/sets/GLD2.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Gold Series 3 | https://images.ygoprodeck.com/images/sets/GLD3.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Gold Series 4: Pyramids Edition | https://images.ygoprodeck.com/images/sets/GLD4.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Gold Series: Haunted Mine | https://images.ygoprodeck.com/images/sets/GLD5.jpg | 55 / 55 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal | https://images.ygoprodeck.com/images/sets/HA01.jpg | 10 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal 2 | https://images.ygoprodeck.com/images/sets/HA02.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal 3 | https://images.ygoprodeck.com/images/sets/HA03.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal 4 | https://images.ygoprodeck.com/images/sets/HA04.jpg | 62 / 62 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal 5: Steelswarm Invasion | https://images.ygoprodeck.com/images/sets/HA05.jpg | 62 / 62 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal 6: Omega Xyz | https://images.ygoprodeck.com/images/sets/HA06.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal 7: Knight of Stars | https://images.ygoprodeck.com/images/sets/HA07.jpg | 70 / 70 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Arsenal: Chapter 1 | https://images.ygoprodeck.com/images/sets/HAC1.jpg | 316 / 317 | ygoprodeck |
| Yu-Gi-Oh! | Hidden Summoners | https://images.ygoprodeck.com/images/sets/HISU.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | High-Speed Riders | https://images.ygoprodeck.com/images/sets/HSRD.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Hobby League 1 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Hobby League 2 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Hobby League 3 |  | 7 / 7 | — |
| Yu-Gi-Oh! | Hobby League 4 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Hobby League 5 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Hobby League 6 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Hobby League 7 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Ignition Assault | https://images.ygoprodeck.com/images/sets/IGAS.jpg | 109 / 109 | ygoprodeck |
| Yu-Gi-Oh! | Invasion of Chaos | https://images.ygoprodeck.com/images/sets/IOC.jpg | 106 / 116 | ygoprodeck |
| Yu-Gi-Oh! | Invasion of Chaos (25th Anniversary Edition) | https://images.ygoprodeck.com/images/sets/IOC.jpg ※ | 112 / 112 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Invasion of Chaos (Worldwide English) | https://images.ygoprodeck.com/images/sets/IOC.jpg ※ | 8 / 112 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Invasion: Vengeance | https://images.ygoprodeck.com/images/sets/INOV.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Judge Promotional Cards |  | 24 / 25 | — |
| Yu-Gi-Oh! | Judgment of the Light | https://images.ygoprodeck.com/images/sets/JOTL.jpg | 111 / 111 | ygoprodeck |
| Yu-Gi-Oh! | Justice Hunters | https://images.ygoprodeck.com/images/sets/JUSH.jpg | 103 / 103 | ygoprodeck |
| Yu-Gi-Oh! | King of Games: Yugi's Legendary Decks |  | 133 / 133 | — |
| Yu-Gi-Oh! | King of Games: Yugi's Legendary Decks (2020 Date Reprint) |  | 133 / 133 | — |
| Yu-Gi-Oh! | King's Court | https://images.ygoprodeck.com/images/sets/KICO.jpg | 83 / 83 | ygoprodeck |
| Yu-Gi-Oh! | Labyrinth of Nightmare | https://images.ygoprodeck.com/images/sets/LON.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Labyrinth of Nightmare (Worldwide English) | https://images.ygoprodeck.com/images/sets/LON.jpg ※ | 105 / 105 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Legacy of Darkness | https://images.ygoprodeck.com/images/sets/LOD.jpg | 102 / 102 | ygoprodeck |
| Yu-Gi-Oh! | Legacy of Darkness (Worldwide English) | https://images.ygoprodeck.com/images/sets/LOD.jpg ※ | 99 / 101 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Legacy of Destruction | https://images.ygoprodeck.com/images/sets/LEDE.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Legacy of the Valiant | https://images.ygoprodeck.com/images/sets/LVAL.jpg | 111 / 111 | ygoprodeck |
| Yu-Gi-Oh! | Legend of Blue Eyes White Dragon (25th Anniversary Edition) | https://images.ygoprodeck.com/images/sets/LOB.jpg | 126 / 126 | ygoprodeck |
| Yu-Gi-Oh! | Legend of Blue Eyes White Dragon (Worldwide English) | https://images.ygoprodeck.com/images/sets/LOB.jpg ※ | 51 / 126 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Legendary 5D's Decks |  | 118 / 118 | — |
| Yu-Gi-Oh! | Legendary Arc-V Decks | https://images.ygoprodeck.com/images/sets/LAVD.jpg | 108 / 158 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection 1 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Legendary Collection 2 | https://images.ygoprodeck.com/images/sets/LC02.jpg | 279 / 279 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection 3: Yugi's World | https://images.ygoprodeck.com/images/sets/LC03.jpg | 313 / 313 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection 4: Joey's World | https://images.ygoprodeck.com/images/sets/LC04.jpg | 305 / 307 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection 5D's | https://images.ygoprodeck.com/images/sets/LC05.jpg | 0 / 265 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection Kaiba | https://images.ygoprodeck.com/images/sets/LC06.jpg | 115 / 119 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection Kaiba (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/LCKC.jpg | 55 / 119 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Collection: 25th Anniversary Edition | https://images.ygoprodeck.com/images/sets/LC01.jpg | 12 / 12 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Decks II | https://images.ygoprodeck.com/images/sets/LDK2.jpg | 135 / 135 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Decks II (2020 Reprint) | https://images.ygoprodeck.com/images/sets/LDK2.jpg ※ | 135 / 135 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Legendary Dragon Decks | https://images.ygoprodeck.com/images/sets/LEDD.jpg | 99 / 115 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Dragon Decks (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/LEDD.jpg ※ | 42 / 115 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Legendary Duelists | https://images.ygoprodeck.com/images/sets/LEDU.jpg | 51 / 52 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Ancient Millennium | https://images.ygoprodeck.com/images/sets/LED2.jpg | 53 / 53 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Duels From the Deep | https://images.ygoprodeck.com/images/sets/LED9.jpg | 57 / 57 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Immortal Destiny | https://images.ygoprodeck.com/images/sets/LED5.jpg | 58 / 58 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Magical Hero | https://images.ygoprodeck.com/images/sets/LED6.jpg | 57 / 57 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Rage of Ra | https://images.ygoprodeck.com/images/sets/LED7.jpg | 58 / 58 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Season 1 | https://images.ygoprodeck.com/images/sets/LDS1.jpg | 163 / 163 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Season 2 | https://images.ygoprodeck.com/images/sets/LDS2.jpg | 221 / 221 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Season 3 | https://images.ygoprodeck.com/images/sets/LDS3.jpg | 196 / 198 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Sisters of the Rose | https://images.ygoprodeck.com/images/sets/LED4.jpg | 56 / 56 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Soulburning Volcano | https://images.ygoprodeck.com/images/sets/LD10.jpg | 62 / 62 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: Synchro Storm | https://images.ygoprodeck.com/images/sets/LED8.jpg | 57 / 57 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Duelists: White Dragon Abyss | https://images.ygoprodeck.com/images/sets/LED3.jpg | 56 / 56 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Hero Decks | https://images.ygoprodeck.com/images/sets/LEHD.jpg | 120 / 120 | ygoprodeck |
| Yu-Gi-Oh! | Legendary Modern Decks 2026 | https://images.ygoprodeck.com/images/sets/L26D.jpg | 154 / 154 | ygoprodeck |
| Yu-Gi-Oh! | Light and Darkness Power Pack |  | 1 / 1 | — |
| Yu-Gi-Oh! | Light of Destruction | https://images.ygoprodeck.com/images/sets/LODT.jpg | 89 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Light of Destruction (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/LODT.jpg ※ | 61 / 113 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Lightning Overdrive | https://images.ygoprodeck.com/images/sets/LIOV.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Limited Pack World Championship 2025 | https://images.ygoprodeck.com/images/sets/25LP.jpg | 82 / 82 | ygoprodeck |
| Yu-Gi-Oh! | Limited Pack World Championship 2026 | https://images.ygoprodeck.com/images/sets/26LP.jpg | 0 / 87 | ygoprodeck |
| Yu-Gi-Oh! | Lord of the Tachyon Galaxy | https://images.ygoprodeck.com/images/sets/LTGY.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Magic Ruler | https://images.ygoprodeck.com/images/sets/MRL.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | Magician's Force | https://images.ygoprodeck.com/images/sets/MFC.jpg | 109 / 109 | ygoprodeck |
| Yu-Gi-Oh! | Magnificent Mavens | https://images.ygoprodeck.com/images/sets/MAMA.jpg | 139 / 139 | ygoprodeck |
| Yu-Gi-Oh! | Magnificent Monsters | https://images.ygoprodeck.com/images/sets/MAMO.jpg | 0 / 228 | ygoprodeck |
| Yu-Gi-Oh! | Master Collection Volume 1 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Master Collection Volume 2 |  | 6 / 6 | — |
| Yu-Gi-Oh! | Mattel Action Figure Promos: Series 1 |  | 1 / 1 | — |
| Yu-Gi-Oh! | Mattel Action Figure Promos: Series 2 |  | 4 / 4 | — |
| Yu-Gi-Oh! | Mattel Action Figure Promos: Series 3 |  | 11 / 11 | — |
| Yu-Gi-Oh! | Maximum Crisis | https://images.ygoprodeck.com/images/sets/MACR.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Maximum Gold | https://images.ygoprodeck.com/images/sets/MAGO.jpg | 170 / 171 | ygoprodeck |
| Yu-Gi-Oh! | Maximum Gold: El Dorado | https://images.ygoprodeck.com/images/sets/MGED.jpg | 161 / 161 | ygoprodeck |
| Yu-Gi-Oh! | Maze of Memories | https://images.ygoprodeck.com/images/sets/MAZE.jpg | 82 / 82 | ygoprodeck |
| Yu-Gi-Oh! | Maze of Millennia | https://images.ygoprodeck.com/images/sets/MZMI.jpg | 101 / 101 | ygoprodeck |
| Yu-Gi-Oh! | Maze of Muertos | https://images.ygoprodeck.com/images/sets/MZMU.jpg | 142 / 142 | ygoprodeck |
| Yu-Gi-Oh! | Maze of the Master | https://images.ygoprodeck.com/images/sets/MZTM.jpg | 128 / 128 | ygoprodeck |
| Yu-Gi-Oh! | McDonald's Promo | https://images.ygoprodeck.com/images/sets/MP1.jpg | 15 / 15 | ygoprodeck |
| Yu-Gi-Oh! | McDonald's Promo Series 2 | https://images.ygoprodeck.com/images/sets/MDP2.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Metal Raiders | https://images.ygoprodeck.com/images/sets/MRD.jpg | 145 / 145 | ygoprodeck |
| Yu-Gi-Oh! | Metal Raiders (25th Anniversary Edition) | https://images.ygoprodeck.com/images/sets/MRD.jpg | 144 / 144 | ygoprodeck |
| Yu-Gi-Oh! | Metal Raiders (Worldwide English) | https://images.ygoprodeck.com/images/sets/MRD.jpg ※ | 144 / 144 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Millennium Pack | https://images.ygoprodeck.com/images/sets/MIL1.jpg | 48 / 48 | ygoprodeck |
| Yu-Gi-Oh! | Miscellaneous Promotional Cards |  | 21 / 22 | — |
| Yu-Gi-Oh! | Mystic Fighters | https://images.ygoprodeck.com/images/sets/MYFI.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Nintendo DS Nightmare of Troubadour |  | 3 / 3 | — |
| Yu-Gi-Oh! | Noble Knights of the Round Table Box Set | https://images.ygoprodeck.com/images/sets/NKRT.jpg | 44 / 44 | ygoprodeck |
| Yu-Gi-Oh! | Number Hunters | https://images.ygoprodeck.com/images/sets/NUMH.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 1 | https://images.ygoprodeck.com/images/sets/OP01.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 10 | https://images.ygoprodeck.com/images/sets/OP10.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 11 | https://images.ygoprodeck.com/images/sets/OP11.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 12 | https://images.ygoprodeck.com/images/sets/OP12.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 13 | https://images.ygoprodeck.com/images/sets/OP13.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 14 | https://images.ygoprodeck.com/images/sets/OP14.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 15 | https://images.ygoprodeck.com/images/sets/OP15.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 16 | https://images.ygoprodeck.com/images/sets/OP16.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 17 | https://images.ygoprodeck.com/images/sets/OP17.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 18 | https://images.ygoprodeck.com/images/sets/OP18.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 19 | https://images.ygoprodeck.com/images/sets/OP19.jpg | 29 / 29 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 2 | https://images.ygoprodeck.com/images/sets/OP02.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 20 | https://images.ygoprodeck.com/images/sets/OP20.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 21 | https://images.ygoprodeck.com/images/sets/OP21.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 22 | https://images.ygoprodeck.com/images/sets/OP22.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 23 | https://images.ygoprodeck.com/images/sets/OP23.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 24 | https://images.ygoprodeck.com/images/sets/OP24.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 25 | https://images.ygoprodeck.com/images/sets/OP25.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 26 | https://images.ygoprodeck.com/images/sets/OP26.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 27 | https://images.ygoprodeck.com/images/sets/OP27.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 28 | https://images.ygoprodeck.com/images/sets/OP28.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 29 | https://images.ygoprodeck.com/images/sets/OP29.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 3 | https://images.ygoprodeck.com/images/sets/OP03.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 30 | https://images.ygoprodeck.com/images/sets/OP30.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 4 | https://images.ygoprodeck.com/images/sets/OP04.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 5 | https://images.ygoprodeck.com/images/sets/OP05.jpg | 27 / 27 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 6 | https://images.ygoprodeck.com/images/sets/OP06.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 7 | https://images.ygoprodeck.com/images/sets/OP07.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 8 | https://images.ygoprodeck.com/images/sets/OP08.jpg | 26 / 26 | ygoprodeck |
| Yu-Gi-Oh! | OTS Tournament Pack 9 | https://images.ygoprodeck.com/images/sets/OP09.jpg | 28 / 28 | ygoprodeck |
| Yu-Gi-Oh! | Order of Chaos | https://images.ygoprodeck.com/images/sets/ORCS.jpg | 64 / 114 | ygoprodeck |
| Yu-Gi-Oh! | PS2 Yugioh GX The Beginning of Destiny | https://images.ygoprodeck.com/images/sets/GX05.jpg | 1 / 1 | ygoprodeck |
| Yu-Gi-Oh! | Pendulum Evolution | https://images.ygoprodeck.com/images/sets/PEVO.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Phantom Darkness | https://images.ygoprodeck.com/images/sets/PTDN.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Phantom Nightmare | https://images.ygoprodeck.com/images/sets/PHNI.jpg | 126 / 126 | ygoprodeck |
| Yu-Gi-Oh! | Phantom Rage | https://images.ygoprodeck.com/images/sets/PHRA.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Phantom Revenge | https://images.ygoprodeck.com/images/sets/PHRE.jpg | 104 / 104 | ygoprodeck |
| Yu-Gi-Oh! | Pharaoh Tour Promos |  | 6 / 6 | — |
| Yu-Gi-Oh! | Pharaoh's Servant | https://images.ygoprodeck.com/images/sets/PSV.jpg | 42 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Pharaoh's Servant (25th Anniversary Edition) | https://images.ygoprodeck.com/images/sets/PSV.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Pharaoh's Servant (Worldwide English) | https://images.ygoprodeck.com/images/sets/PSV.jpg ※ | 50 / 105 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Pharaonic Guardian | https://images.ygoprodeck.com/images/sets/PGD.jpg | 108 / 108 | ygoprodeck |
| Yu-Gi-Oh! | Photon Hypernova | https://images.ygoprodeck.com/images/sets/PHHY.jpg | 56 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Photon Shockwave | https://images.ygoprodeck.com/images/sets/PHSW.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Power of Chaos: Joey the Passion | https://images.ygoprodeck.com/images/sets/PCJ.jpg | 3 / 3 | ygoprodeck |
| Yu-Gi-Oh! | Power of Chaos: Yugi the Destiny | https://images.ygoprodeck.com/images/sets/PCY.jpg | 5 / 5 | ygoprodeck |
| Yu-Gi-Oh! | Power of the Duelist | https://images.ygoprodeck.com/images/sets/POTD.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Power of the Elements | https://images.ygoprodeck.com/images/sets/POTE.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Premium Gold | https://images.ygoprodeck.com/images/sets/PGLD.jpg | 31 / 90 | ygoprodeck |
| Yu-Gi-Oh! | Premium Gold: Infinite Gold | https://images.ygoprodeck.com/images/sets/PGL3.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Premium Gold: Return of the Bling | https://images.ygoprodeck.com/images/sets/PGL2.jpg | 91 / 91 | ygoprodeck |
| Yu-Gi-Oh! | Premium Pack 1 | https://images.ygoprodeck.com/images/sets/PP01.jpg | 22 / 22 | ygoprodeck |
| Yu-Gi-Oh! | Premium Pack 2 | https://images.ygoprodeck.com/images/sets/PP02.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Primal Origin | https://images.ygoprodeck.com/images/sets/PRIO.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Quarter Century Bonanza | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23656/logo.webp | 963 / 967 | holodex |
| Yu-Gi-Oh! | Quarter Century Stampede | https://images.ygoprodeck.com/images/sets/RA04.jpg | 836 / 986 | ygoprodeck |
| Yu-Gi-Oh! | Ra Yellow Mega Pack | https://images.ygoprodeck.com/images/sets/RYMP.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Rage of the Abyss | https://images.ygoprodeck.com/images/sets/ROTA.jpg | 132 / 132 | ygoprodeck |
| Yu-Gi-Oh! | Raging Battle | https://images.ygoprodeck.com/images/sets/RGBT.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Raging Battle SE | https://images.ygoprodeck.com/images/sets/RGBT.jpg ※ | 3 / 3 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Raging Tempest | https://images.ygoprodeck.com/images/sets/RATE.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Rarity Collection 5 | https://images.ygoprodeck.com/images/sets/RA05.jpg | 696 / 697 | ygoprodeck |
| Yu-Gi-Oh! | Redemption Replacement |  | 9 / 9 | — |
| Yu-Gi-Oh! | Reshef of Destruction |  | 1 / 1 | — |
| Yu-Gi-Oh! | Retro Pack | https://images.ygoprodeck.com/images/sets/RP01.jpg | 1 / 101 | ygoprodeck |
| Yu-Gi-Oh! | Retro Pack (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/RP01.jpg ※ | 65 / 101 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Retro Pack 2 | https://images.ygoprodeck.com/images/sets/RP02.jpg | 57 / 101 | ygoprodeck |
| Yu-Gi-Oh! | Retro Pack 2 (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/RP02.jpg ※ | 101 / 101 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Return of the Duelist | https://images.ygoprodeck.com/images/sets/REDU.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | Return of the Duelist SE | https://images.ygoprodeck.com/images/sets/REDU.jpg ※ | 2 / 2 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Rise of Destiny | https://images.ygoprodeck.com/images/sets/RDS.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Rise of Destiny Special Edition | https://images.ygoprodeck.com/images/sets/RDS.jpg | 4 / 4 | ygoprodeck |
| Yu-Gi-Oh! | Rise of the Duelist | https://images.ygoprodeck.com/images/sets/ROTD.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Rising Rampage | https://images.ygoprodeck.com/images/sets/RIRA.jpg | 109 / 109 | ygoprodeck |
| Yu-Gi-Oh! | Samurai Assault |  | 1 / 1 | — |
| Yu-Gi-Oh! | Savage Strike | https://images.ygoprodeck.com/images/sets/SAST.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Secret Slayers | https://images.ygoprodeck.com/images/sets/SESL.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Secrets of Eternity | https://images.ygoprodeck.com/images/sets/SECE.jpg | 121 / 121 | ygoprodeck |
| Yu-Gi-Oh! | Shadow Specters | https://images.ygoprodeck.com/images/sets/SHSP.jpg | 109 / 109 | ygoprodeck |
| Yu-Gi-Oh! | Shadow of Infinity | https://images.ygoprodeck.com/images/sets/SOI.jpg | 93 / 93 | ygoprodeck |
| Yu-Gi-Oh! | Shadows in Valhalla | https://images.ygoprodeck.com/images/sets/SHVA.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Shining Victories | https://images.ygoprodeck.com/images/sets/SHVI.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Shonen Jump Championship Series Prize Cards | https://images.ygoprodeck.com/images/sets/SJCS.jpg | 2 / 2 | ygoprodeck |
| Yu-Gi-Oh! | Shonen Jump Championship Series Promos |  | 5 / 5 | — |
| Yu-Gi-Oh! | Shonen Jump Magazine Promos |  | 100 / 100 | — |
| Yu-Gi-Oh! | Sneak Preview Series 1 |  | 4 / 4 | — |
| Yu-Gi-Oh! | Sneak Preview Series 2 |  | 4 / 4 | — |
| Yu-Gi-Oh! | Sneak Preview Series 3 |  | 4 / 4 | — |
| Yu-Gi-Oh! | Sneak Preview Series 4 |  | 1 / 1 | — |
| Yu-Gi-Oh! | Sneak Preview Series 5 |  | 1 / 1 | — |
| Yu-Gi-Oh! | Soul Fusion | https://images.ygoprodeck.com/images/sets/SOFU.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | Soul of the Duelist | https://images.ygoprodeck.com/images/sets/SOD.jpg | 85 / 85 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel Decks: Destiny Masters | https://images.ygoprodeck.com/images/sets/SS01.jpg | 64 / 64 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel Decks: Duelists of Tomorrow | https://images.ygoprodeck.com/images/sets/SS02.jpg | 69 / 69 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel Decks: Match of the Millennium | https://images.ygoprodeck.com/images/sets/SS04.jpg | 67 / 67 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel Decks: Twisted Nightmares | https://images.ygoprodeck.com/images/sets/SS05.jpg | 66 / 66 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel Decks: Ultimate Predators | https://images.ygoprodeck.com/images/sets/SS03.jpg | 63 / 63 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel Demo Deck |  | 11 / 11 | — |
| Yu-Gi-Oh! | Speed Duel Demo Deck 2020 |  | 21 / 21 | — |
| Yu-Gi-Oh! | Speed Duel GX: Duel Academy Box | https://images.ygoprodeck.com/images/sets/SGX1.jpg | 242 / 242 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel GX: Duelists of Shadows | https://images.ygoprodeck.com/images/sets/SGX3.jpg | 242 / 242 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel GX: Midterm Destruction |  | 132 / 132 | — |
| Yu-Gi-Oh! | Speed Duel GX: Midterm Paradox | https://images.ygoprodeck.com/images/sets/SGX2.jpg | 122 / 122 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Arena of Lost Souls | https://images.ygoprodeck.com/images/sets/SBLS.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Attack from the Deep | https://images.ygoprodeck.com/images/sets/SBAD.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Battle City Box | https://images.ygoprodeck.com/images/sets/SBCB.jpg | 244 / 244 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Battle City Finals |  | 250 / 250 | — |
| Yu-Gi-Oh! | Speed Duel: Scars of Battle | https://images.ygoprodeck.com/images/sets/SBSC.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Streets of Battle City | https://images.ygoprodeck.com/images/sets/SBC1.jpg | 187 / 237 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 1 |  | 18 / 18 | — |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 2 | https://images.ygoprodeck.com/images/sets/STP2.jpg | 18 / 18 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 3 | https://images.ygoprodeck.com/images/sets/STP3.jpg | 35 / 35 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 4 | https://images.ygoprodeck.com/images/sets/STP4.jpg | 35 / 35 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 5 | https://images.ygoprodeck.com/images/sets/STP5.jpg | 35 / 35 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 6 | https://images.ygoprodeck.com/images/sets/STP6.jpg | 35 / 35 | ygoprodeck |
| Yu-Gi-Oh! | Speed Duel: Tournament Pack 7 |  | 35 / 35 | — |
| Yu-Gi-Oh! | Speed Duel: Trials of the Kingdom | https://images.ygoprodeck.com/images/sets/SBTK.jpg | 61 / 61 | ygoprodeck |
| Yu-Gi-Oh! | Spell Ruler | https://images.ygoprodeck.com/images/sets/SRL.jpg | 104 / 104 | ygoprodeck |
| Yu-Gi-Oh! | Spell Ruler (25th Anniversary Edition) | https://images.ygoprodeck.com/images/sets/SRL.jpg | 104 / 104 | ygoprodeck |
| Yu-Gi-Oh! | Spell Ruler (Worldwide English) | https://images.ygoprodeck.com/images/sets/SRL.jpg ※ | 104 / 104 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Spirit Warriors | https://images.ygoprodeck.com/images/sets/SPWA.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Stairway to the Destined Duel |  | 6 / 6 | — |
| Yu-Gi-Oh! | Star Pack - Battle Royal | https://images.ygoprodeck.com/images/sets/SP17.jpg | 99 / 99 | ygoprodeck |
| Yu-Gi-Oh! | Star Pack 2013 | https://images.ygoprodeck.com/images/sets/SP13.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Star Pack 2014 | https://images.ygoprodeck.com/images/sets/SP14.jpg | 100 / 100 | ygoprodeck |
| Yu-Gi-Oh! | Star Pack ARC-V | https://images.ygoprodeck.com/images/sets/SP15.jpg | 98 / 98 | ygoprodeck |
| Yu-Gi-Oh! | Star Pack VRAINS | https://images.ygoprodeck.com/images/sets/SP18.jpg | 99 / 99 | ygoprodeck |
| Yu-Gi-Oh! | Stardust Accelerator Promos |  | 3 / 3 | — |
| Yu-Gi-Oh! | Stardust Overdrive | https://images.ygoprodeck.com/images/sets/SOVR.jpg | 116 / 116 | ygoprodeck |
| Yu-Gi-Oh! | Starstrike Blast | https://images.ygoprodeck.com/images/sets/STBL.jpg | 110 / 111 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck 2006 | https://images.ygoprodeck.com/images/sets/YSD.jpg | 41 / 41 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Codebreaker | https://images.ygoprodeck.com/images/sets/YS18.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Dark Legion | https://images.ygoprodeck.com/images/sets/YS15.jpg | 29 / 29 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Dawn of the Xyz | https://images.ygoprodeck.com/images/sets/YS11.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Duelist Toolbox | https://images.ygoprodeck.com/images/sets/5DS3.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Jaden Yuki | https://images.ygoprodeck.com/images/sets/YSDJ.jpg | 41 / 41 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Joey | https://images.ygoprodeck.com/images/sets/SDJ.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Kaiba | https://images.ygoprodeck.com/images/sets/SDK.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Kaiba Evolution | https://images.ygoprodeck.com/images/sets/SKE.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Kaiba Reloaded | https://images.ygoprodeck.com/images/sets/YSKR.jpg | 49 / 49 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Link Strike | https://images.ygoprodeck.com/images/sets/YS17.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Pegasus | https://images.ygoprodeck.com/images/sets/SDP.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Saber Force | https://images.ygoprodeck.com/images/sets/YS15.jpg | 28 / 28 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Syrus Truesdale | https://images.ygoprodeck.com/images/sets/YSDS.jpg | 41 / 41 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Xyz Symphony | https://images.ygoprodeck.com/images/sets/YS12.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Yugi | https://images.ygoprodeck.com/images/sets/SDY.jpg | 51 / 51 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Yugi Evolution | https://images.ygoprodeck.com/images/sets/SYE.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Yugi Reloaded | https://images.ygoprodeck.com/images/sets/YSYR.jpg | 47 / 47 | ygoprodeck |
| Yu-Gi-Oh! | Starter Deck: Yuya | https://images.ygoprodeck.com/images/sets/YS16.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Storm of Ragnarok | https://images.ygoprodeck.com/images/sets/STOR.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | Strike of Neos | https://images.ygoprodeck.com/images/sets/STON.jpg | 96 / 96 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Albaz Strike | https://images.ygoprodeck.com/images/sets/SDAZ.jpg | 51 / 51 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Beware of Traptrix | https://images.ygoprodeck.com/images/sets/SDBT.jpg | 46 / 46 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Blaze of Destruction | https://images.ygoprodeck.com/images/sets/SD3.jpg | 31 / 31 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Blue-Eyes White Destiny | https://images.ygoprodeck.com/images/sets/SDWD.jpg | 84 / 84 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Cyber Dragon Revolution | https://images.ygoprodeck.com/images/sets/SDCR.jpg | 39 / 39 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Cyber Strike | https://images.ygoprodeck.com/images/sets/SDCS.jpg | 48 / 48 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Cyberse Link | https://images.ygoprodeck.com/images/sets/SDCL.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Dark World | https://images.ygoprodeck.com/images/sets/SR13.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Deluxe Edition | https://images.ygoprodeck.com/images/sets/SD1.jpg | 2 / 2 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Dinosaur's Rage | https://images.ygoprodeck.com/images/sets/SD09.jpg | 37 / 37 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Dinosmasher's Fury | https://images.ygoprodeck.com/images/sets/SR04.jpg | 40 / 40 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Dragon's Roar | https://images.ygoprodeck.com/images/sets/SD1.jpg | 28 / 28 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Dragons Collide | https://images.ygoprodeck.com/images/sets/SDDC.jpg | 40 / 40 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Dragunity Legion | https://images.ygoprodeck.com/images/sets/SDDL.jpg | 39 / 39 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Emperor of Darkness | https://images.ygoprodeck.com/images/sets/SR01.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Fire Kings | https://images.ygoprodeck.com/images/sets/SR14.jpg | 48 / 48 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Freezing Chains | https://images.ygoprodeck.com/images/sets/SDFC.jpg | 46 / 46 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Fury from the Deep | https://images.ygoprodeck.com/images/sets/SD4.jpg | 32 / 32 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Gates of the Underworld | https://images.ygoprodeck.com/images/sets/SDGU.jpg | 39 / 39 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Geargia Rampage | https://images.ygoprodeck.com/images/sets/SDGR.jpg | 35 / 35 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: HERO Strike | https://images.ygoprodeck.com/images/sets/SDHS.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Invincible Fortress | https://images.ygoprodeck.com/images/sets/SD7.jpg | 32 / 32 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Lair of Darkness | https://images.ygoprodeck.com/images/sets/SR06.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Legend of the Crystal Beasts | https://images.ygoprodeck.com/images/sets/SDCB.jpg | 49 / 49 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Lord of the Storm | https://images.ygoprodeck.com/images/sets/SD8.jpg | 36 / 36 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Lost Sanctuary | https://images.ygoprodeck.com/images/sets/SDLS.jpg | 38 / 38 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Machina Mayhem | https://images.ygoprodeck.com/images/sets/SDMM.jpg | 37 / 37 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Machine Re-Volt | https://images.ygoprodeck.com/images/sets/SD10.jpg | 37 / 37 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Machine Reactor | https://images.ygoprodeck.com/images/sets/SR03.jpg | 40 / 40 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Marik | https://images.ygoprodeck.com/images/sets/SDMA.jpg | 38 / 38 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Master of Pendulum | https://images.ygoprodeck.com/images/sets/SDMP.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Mechanized Madness | https://images.ygoprodeck.com/images/sets/SR10.jpg | 41 / 41 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Onslaught of the Fire Kings | https://images.ygoprodeck.com/images/sets/SDOK.jpg | 39 / 39 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Order of the Spellcasters | https://images.ygoprodeck.com/images/sets/SR08.jpg | 41 / 41 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Pendulum Domination | https://images.ygoprodeck.com/images/sets/SDPD.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Powercode Link | https://images.ygoprodeck.com/images/sets/SDPL.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Realm of Light | https://images.ygoprodeck.com/images/sets/SDLI.jpg | 36 / 36 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Realm of Light (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/SDLI.jpg ※ | 36 / 36 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Structure Deck: Realm of the Sea Emperor | https://images.ygoprodeck.com/images/sets/SDRE.jpg | 39 / 39 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Rise of the Dragon Lords | https://images.ygoprodeck.com/images/sets/SDRL.jpg | 37 / 37 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Rise of the True Dragons | https://images.ygoprodeck.com/images/sets/SR02.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Rokket Revolt | https://images.ygoprodeck.com/images/sets/SDRR.jpg | 46 / 46 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Sacred Beasts | https://images.ygoprodeck.com/images/sets/SDSA.jpg | 48 / 48 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Saga of Blue Eyes White Dragon (2020 Date Reprint) | https://images.ygoprodeck.com/images/sets/SDBE.jpg ※ | 40 / 40 | ygoprodeck（继承父系列） |
| Yu-Gi-Oh! | Structure Deck: Saga of Blue-Eyes White Dragon | https://images.ygoprodeck.com/images/sets/SDBE.jpg | 40 / 40 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Samurai Warlords | https://images.ygoprodeck.com/images/sets/SDWA.jpg | 41 / 41 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Seto Kaiba | https://images.ygoprodeck.com/images/sets/SDKS.jpg | 44 / 44 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Shaddoll Showdown | https://images.ygoprodeck.com/images/sets/SDSH.jpg | 49 / 49 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Soulburner | https://images.ygoprodeck.com/images/sets/SDSB.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Spellcaster's Command | https://images.ygoprodeck.com/images/sets/SDSC.jpg | 39 / 39 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Spellcaster's Judgment | https://images.ygoprodeck.com/images/sets/SD6.jpg | 36 / 36 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Spirit Charmers | https://images.ygoprodeck.com/images/sets/SDCH.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Synchron Extreme | https://images.ygoprodeck.com/images/sets/SDSE.jpg | 43 / 43 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: The Crimson King | https://images.ygoprodeck.com/images/sets/SDCK.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: The Dark Emperor | https://images.ygoprodeck.com/images/sets/SDDE.jpg | 36 / 36 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Warrior's Triumph | https://images.ygoprodeck.com/images/sets/SD5.jpg | 36 / 36 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Warriors' Strike | https://images.ygoprodeck.com/images/sets/SDWS.jpg | 38 / 38 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Wave of Light | https://images.ygoprodeck.com/images/sets/SR05.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Yugi Muto | https://images.ygoprodeck.com/images/sets/SDMY.jpg | 45 / 45 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Zombie Horde | https://images.ygoprodeck.com/images/sets/SR07.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Zombie Madness | https://images.ygoprodeck.com/images/sets/SD2.jpg | 28 / 28 | ygoprodeck |
| Yu-Gi-Oh! | Structure Deck: Zombie World | https://images.ygoprodeck.com/images/sets/SDZW.jpg | 37 / 37 | ygoprodeck |
| Yu-Gi-Oh! | Super Starter: Space-Time Showdown | https://images.ygoprodeck.com/images/sets/YS14.jpg | 40 / 40 | ygoprodeck |
| Yu-Gi-Oh! | Super Starter: Space-Time Showdown Power-Up Pack |  | 15 / 15 | — |
| Yu-Gi-Oh! | Super Starter: V for Victory | https://images.ygoprodeck.com/images/sets/YS13.jpg | 42 / 42 | ygoprodeck |
| Yu-Gi-Oh! | Super Starter: V for Victory Power-Up Pack |  | 15 / 15 | — |
| Yu-Gi-Oh! | Supreme Darkness | https://images.ygoprodeck.com/images/sets/SUDA.jpg | 131 / 131 | ygoprodeck |
| Yu-Gi-Oh! | THE CHRONICLES DECK: Spirit Charmers (All-Foil Edition) | https://images.ygoprodeck.com/images/sets/CH02.jpg | 0 / 62 | ygoprodeck |
| Yu-Gi-Oh! | THE CHRONICLES DECK: The Fallen & The Virtuous (All-Foil Edition) | https://images.ygoprodeck.com/images/sets/CH01.jpg | 0 / 62 | ygoprodeck |
| Yu-Gi-Oh! | Tactical Evolution | https://images.ygoprodeck.com/images/sets/TAEV.jpg | 106 / 106 | ygoprodeck |
| Yu-Gi-Oh! | Tactical Evolution: Special Edition | https://images.ygoprodeck.com/images/sets/TAEV.jpg | 2 / 2 | ygoprodeck |
| Yu-Gi-Oh! | Tactical Masters | https://images.ygoprodeck.com/images/sets/TAMA.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | The Dark Illusion | https://images.ygoprodeck.com/images/sets/TDIL.jpg | 105 / 105 | ygoprodeck |
| Yu-Gi-Oh! | The Dark Side of Dimensions Movie Pack | https://images.ygoprodeck.com/images/sets/MVP1.jpg | 57 / 57 | ygoprodeck |
| Yu-Gi-Oh! | The Dark Side of Dimensions Movie Pack: Gold Edition |  | 63 / 63 | — |
| Yu-Gi-Oh! | The Dark Side of Dimensions Movie Pack: Secret Edition |  | 63 / 63 | — |
| Yu-Gi-Oh! | The Dark Side of Dimensions Movie Pack: Special Edition |  | 4 / 4 | — |
| Yu-Gi-Oh! | The Duelist Genesis | https://images.ygoprodeck.com/images/sets/TDGS.jpg | 114 / 114 | ygoprodeck |
| Yu-Gi-Oh! | The Falsebound Kingdom | https://images.ygoprodeck.com/images/sets/TFK.jpg | 8 / 8 | ygoprodeck |
| Yu-Gi-Oh! | The Grand Creators | https://images.ygoprodeck.com/images/sets/GRCR.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | The Infinite Forbidden | https://images.ygoprodeck.com/images/sets/INFO.jpg | 130 / 130 | ygoprodeck |
| Yu-Gi-Oh! | The Infinity Chasers | https://images.ygoprodeck.com/images/sets/INCH.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | The Legend of Blue Eyes White Dragon | https://images.ygoprodeck.com/images/sets/LOB.jpg | 127 / 127 | ygoprodeck |
| Yu-Gi-Oh! | The Lost Art Promotion | https://images.ygoprodeck.com/images/sets/LART.jpg | 80 / 80 | ygoprodeck |
| Yu-Gi-Oh! | The Lost Millennium | https://images.ygoprodeck.com/images/sets/TLM.jpg | 89 / 89 | ygoprodeck |
| Yu-Gi-Oh! | The New Challengers | https://images.ygoprodeck.com/images/sets/NECH.jpg | 120 / 121 | ygoprodeck |
| Yu-Gi-Oh! | The Pot Collection | https://images.ygoprodeck.com/images/sets/TBC1.jpg | 15 / 15 | ygoprodeck |
| Yu-Gi-Oh! | The Secret Forces | https://images.ygoprodeck.com/images/sets/THSF.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | The Shining Darkness | https://images.ygoprodeck.com/images/sets/TSHD.jpg | 112 / 112 | ygoprodeck |
| Yu-Gi-Oh! | The Valuable Book Volume 5 |  | 1 / 1 | — |
| Yu-Gi-Oh! | Toon Chaos | https://images.ygoprodeck.com/images/sets/TOCH.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 1 | https://images.ygoprodeck.com/images/sets/TP1.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 2 | https://images.ygoprodeck.com/images/sets/TP2.jpg | 18 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 3 | https://images.ygoprodeck.com/images/sets/TP3.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 4 | https://images.ygoprodeck.com/images/sets/TP4.jpg | 13 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 5 | https://images.ygoprodeck.com/images/sets/TP5.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 6 | https://images.ygoprodeck.com/images/sets/TP6.jpg | 14 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 7 | https://images.ygoprodeck.com/images/sets/TP7.jpg | 13 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Tournament Pack 8 | https://images.ygoprodeck.com/images/sets/TP8.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | Toys "R" Us Throwdown Promo |  | 3 / 3 | — |
| Yu-Gi-Oh! | Turbo Pack Booster One Pack | https://images.ygoprodeck.com/images/sets/TU01.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Eight | https://images.ygoprodeck.com/images/sets/TU08.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Five | https://images.ygoprodeck.com/images/sets/TU05.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Four | https://images.ygoprodeck.com/images/sets/TU04.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Seven | https://images.ygoprodeck.com/images/sets/TU07.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Six | https://images.ygoprodeck.com/images/sets/TU06.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Three | https://images.ygoprodeck.com/images/sets/TU03.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Turbo Pack: Booster Two | https://images.ygoprodeck.com/images/sets/TU02.jpg | 21 / 21 | ygoprodeck |
| Yu-Gi-Oh! | Twilight Edition |  | 1 / 1 | — |
| Yu-Gi-Oh! | Ultimate Edition 2 |  | 1 / 1 | — |
| Yu-Gi-Oh! | Ultimate Tournament Pack 1 | https://images.ygoprodeck.com/images/sets/UP01.jpg | 50 / 50 | ygoprodeck |
| Yu-Gi-Oh! | Valiant Smashers | https://images.ygoprodeck.com/images/sets/VASM.jpg | 78 / 78 | ygoprodeck |
| Yu-Gi-Oh! | Wild Survivors | https://images.ygoprodeck.com/images/sets/WISU.jpg | 75 / 75 | ygoprodeck |
| Yu-Gi-Oh! | Wing Raiders | https://images.ygoprodeck.com/images/sets/WIRA.jpg | 60 / 60 | ygoprodeck |
| Yu-Gi-Oh! | Winner's Pack 2026-2027 | https://images.ygoprodeck.com/images/sets/WI26.jpg | 118 / 120 | ygoprodeck |
| Yu-Gi-Oh! | World Championship 2004: GBA Promo |  | 6 / 6 | — |
| Yu-Gi-Oh! | World Championship 2005: 7 Trials to Glory |  | 3 / 3 | — |
| Yu-Gi-Oh! | World Championship 2006: Ultimate Masters | https://images.ygoprodeck.com/images/sets/WC6.jpg | 3 / 3 | ygoprodeck |
| Yu-Gi-Oh! | World Championship 2007 |  | 3 / 3 | — |
| Yu-Gi-Oh! | World Championship 2008 |  | 3 / 3 | — |
| Yu-Gi-Oh! | World Championship 2010 Card Pack | https://images.ygoprodeck.com/images/sets/WCPP.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | World Championship 2011 Card Pack | https://images.ygoprodeck.com/images/sets/WP11.jpg | 20 / 20 | ygoprodeck |
| Yu-Gi-Oh! | World Championship JPP Cards |  | 8 / 10 | — |
| Yu-Gi-Oh! | World Championship Series |  | 8 / 10 | — |
| Yu-Gi-Oh! | World Superstars | https://images.ygoprodeck.com/images/sets/WSUP.jpg | 52 / 52 | ygoprodeck |
| Yu-Gi-Oh! | X-Saber Power-Up |  | 1 / 1 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! 5D's Manga Promotional Cards |  | 9 / 9 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! 5D's Over the Nexus Promo Cards |  | 3 / 3 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! 5D's Tag Force Promotional Cards |  | 3 / 3 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! 5D's Wheelie Breakers Promotional Cards |  | 3 / 3 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! ARC-V Promo Cards | https://images.ygoprodeck.com/images/sets/YA01.jpg | 7 / 7 | ygoprodeck |
| Yu-Gi-Oh! | Yu-Gi-Oh! Championship Series 2025 Prize Cards |  | 13 / 13 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! Championship Series Prize Cards | https://images.ygoprodeck.com/images/sets/YCSW.jpg | 30 / 30 | ygoprodeck |
| Yu-Gi-Oh! | Yu-Gi-Oh! Day Promos | https://images.ygoprodeck.com/images/sets/YDPR.jpg | 5 / 5 | ygoprodeck |
| Yu-Gi-Oh! | Yu-Gi-Oh! Duel Monsters International: Worldwide Edition |  | 6 / 6 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! GX Manga Promotional Cards |  | 8 / 8 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! GX Tag Force Evolution Promo |  | 2 / 2 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! GX Tag Force Promotional Cards |  | 3 / 3 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! Movie Exclusive Pack | https://images.ygoprodeck.com/images/sets/EP1.jpg | 9 / 9 | ygoprodeck |
| Yu-Gi-Oh! | Yu-Gi-Oh! R Manga Promo |  | 4 / 4 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! The Movie Ani-Manga Promo |  | 1 / 1 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! The Movie Promo Set |  | 4 / 4 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! Tokens |  | 129 / 131 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! Value Boxes |  | 4 / 4 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! Video Game Promotional Cards |  | 40 / 40 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! ZEXAL Manga Promotional Cards |  | 9 / 9 | — |
| Yu-Gi-Oh! | Yu-Gi-Oh! ZEXAL World Duel Carnival Promos |  | 3 / 3 | — |
| Yu-Gi-Oh! | eFootball Collaboration Promos | https://images.ygoprodeck.com/images/sets/EFC1.jpg | 2 / 2 | ygoprodeck |

### One Piece Card Game（85 个系列，42 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| One Piece Card Game | 500 Years in the Future | https://holodex-prod-bucket.b-cdn.net/sets/op_23387/logo.webp | 154 / 154 | holodex |
| One Piece Card Game | 500 Years in the Future Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23387/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | A Fist of Divine Speed | https://holodex-prod-bucket.b-cdn.net/sets/op_24241/logo.webp | 159 / 159 | holodex |
| One Piece Card Game | A Fist of Divine Speed Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24241/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | Adventure on Kami's Island | https://holodex-prod-bucket.b-cdn.net/sets/op_24637/logo.webp | 207 / 207 | holodex |
| One Piece Card Game | Adventure on Kami's Island Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24637/logo.webp ※ | 90 / 90 | holodex（继承父系列） |
| One Piece Card Game | Awakening of the New Era | https://holodex-prod-bucket.b-cdn.net/sets/op_23213/logo.webp | 157 / 157 | holodex |
| One Piece Card Game | Awakening of the New Era: 1st Anniversary Tournament Cards |  | 75 / 75 | — |
| One Piece Card Game | Carrying On His Will | https://holodex-prod-bucket.b-cdn.net/sets/op_24303/logo.webp | 177 / 177 | holodex |
| One Piece Card Game | Carrying On His Will: 3rd Anniversary Tournament Cards |  | 79 / 79 | — |
| One Piece Card Game | Emperors in the New World | https://holodex-prod-bucket.b-cdn.net/sets/op_23589/logo.webp | 162 / 162 | holodex |
| One Piece Card Game | Emperors in the New World: 2nd Anniversary Tournament Cards |  | 75 / 75 | — |
| One Piece Card Game | Extra Booster: Anime 25th Collection | https://holodex-prod-bucket.b-cdn.net/sets/op_23834/logo.webp | 50 / 105 | holodex |
| One Piece Card Game | Extra Booster: Memorial Collection | https://holodex-prod-bucket.b-cdn.net/sets/op_23333/logo.webp | 0 / 80 | holodex |
| One Piece Card Game | Extra Booster: One Piece Heroines Edition | https://holodex-prod-bucket.b-cdn.net/sets/op_24545/logo.webp | 102 / 104 | holodex |
| One Piece Card Game | Extra Booster: One Piece Heroines Edition Vol. 2 |  | 0 / 66 | — |
| One Piece Card Game | Kingdoms of Intrigue | https://holodex-prod-bucket.b-cdn.net/sets/op_23024/logo.webp | 50 / 158 | holodex |
| One Piece Card Game | Kingdoms of Intrigue Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23024/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | Learn Together Deck Set |  | 51 / 51 | — |
| One Piece Card Game | Legacy of the Master | https://holodex-prod-bucket.b-cdn.net/sets/op_24302/logo.webp | 158 / 158 | holodex |
| One Piece Card Game | Legacy of the Master Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24302/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | One Piece Demo Deck Cards |  | 26 / 26 | — |
| One Piece Card Game | One Piece Promotion Cards |  | 100 / 1360 | — |
| One Piece Card Game | Paramount War | https://holodex-prod-bucket.b-cdn.net/sets/op_17698/logo.webp | 156 / 156 | holodex |
| One Piece Card Game | Paramount War Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_17698/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | Pillars of Strength | https://holodex-prod-bucket.b-cdn.net/sets/op_22890/logo.webp | 155 / 155 | holodex |
| One Piece Card Game | Pillars of Strength Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_22890/logo.webp ※ | 77 / 77 | holodex（继承父系列） |
| One Piece Card Game | Premium Booster -The Best- | https://holodex-prod-bucket.b-cdn.net/sets/op_23496/logo.webp | 54 / 325 | holodex |
| One Piece Card Game | Premium Booster -The Best- Vol. 2 | https://holodex-prod-bucket.b-cdn.net/sets/op_24305/logo.webp | 146 / 376 | holodex |
| One Piece Card Game | Revision Pack Cards |  | 33 / 33 | — |
| One Piece Card Game | Romance Dawn | https://holodex-prod-bucket.b-cdn.net/sets/op_3188/logo.webp | 156 / 156 | holodex |
| One Piece Card Game | Royal Blood | https://holodex-prod-bucket.b-cdn.net/sets/op_23766/logo.webp | 152 / 152 | holodex |
| One Piece Card Game | Royal Blood Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23766/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | ST-01: Starter Deck 1 Straw Hat Crew |  | 0 / 18 | — |
| One Piece Card Game | ST-01: Starter Deck 1 Straw Hat Crew (Super Pre-Release Edition) |  | 0 / 18 | — |
| One Piece Card Game | ST-02: Starter Deck 2 Worst Generation |  | 0 / 17 | — |
| One Piece Card Game | ST-02: Starter Deck 2 Worst Generation (Super Pre-Release Edition) |  | 0 / 17 | — |
| One Piece Card Game | ST-03: Starter Deck 3 The Seven Warlords of The Sea |  | 0 / 17 | — |
| One Piece Card Game | ST-03: Starter Deck 3 The Seven Warlords of The Sea (Super Pre-Release Edition) |  | 0 / 17 | — |
| One Piece Card Game | ST-04: Starter Deck 4 Animal Kingdom Pirates |  | 0 / 17 | — |
| One Piece Card Game | ST-04: Starter Deck 4 Animal Kingdom Pirates (Super Pre-Release Edition) |  | 0 / 17 | — |
| One Piece Card Game | ST-05: Starter Deck 5 Film Edition |  | 0 / 17 | — |
| One Piece Card Game | ST-06: Starter Deck 6 Absolute Justice |  | 0 / 17 | — |
| One Piece Card Game | ST-07: Starter Deck 7 Big Mom Pirates |  | 0 / 17 | — |
| One Piece Card Game | ST-08: Starter Deck 8 Monkey.D.Luffy |  | 0 / 15 | — |
| One Piece Card Game | ST-09: Starter Deck 9 Yamato |  | 0 / 15 | — |
| One Piece Card Game | ST-10: Ultra Deck The Three Captains |  | 0 / 18 | — |
| One Piece Card Game | ST-11: Starter Deck 11 Uta |  | 0 / 5 | — |
| One Piece Card Game | ST-12: Starter Deck 12 Zoro and Sanji |  | 0 / 17 | — |
| One Piece Card Game | ST-13: Ultra Deck The Three Brothers |  | 0 / 35 | — |
| One Piece Card Game | ST-14: Starter Deck 14 3D2Y |  | 0 / 17 | — |
| One Piece Card Game | ST-15: Starter Deck 15 RED Edward.Newgate |  | 0 / 13 | — |
| One Piece Card Game | ST-16: Starter Deck 16 GREEN Uta |  | 0 / 15 | — |
| One Piece Card Game | ST-17: Starter Deck 17 BLUE Donquixote Doflamingo |  | 0 / 10 | — |
| One Piece Card Game | ST-18: Starter Deck 18 PURPLE Monkey.D.Luffy |  | 0 / 15 | — |
| One Piece Card Game | ST-19: Starter Deck 19 BLACK Smoker |  | 0 / 14 | — |
| One Piece Card Game | ST-20: Starter Deck 20 YELLOW Charlotte Katakuri |  | 0 / 11 | — |
| One Piece Card Game | ST-21: Starter Deck 21 EX Gear 5 |  | 0 / 33 | — |
| One Piece Card Game | ST-22: Starter Deck 22 Ace & Newgate |  | 0 / 31 | — |
| One Piece Card Game | ST-23: Starter Deck 23 RED Shanks | https://en.onepiece-cardgame.com/renewal/images/products/decks/st23/logo.webp | 0 / 15 | onepiece-official |
| One Piece Card Game | ST-24: Starter Deck 24 GREEN Jewelry Bonney | https://en.onepiece-cardgame.com/renewal/images/products/decks/st24/logo.webp | 0 / 15 | onepiece-official |
| One Piece Card Game | ST-25: Starter Deck 25 BLUE Buggy | https://en.onepiece-cardgame.com/renewal/images/products/decks/st25/logo.webp | 0 / 15 | onepiece-official |
| One Piece Card Game | ST-26: Starter Deck 26 PURPLE/BLACK Monkey.D.Luffy | https://en.onepiece-cardgame.com/renewal/images/products/decks/st26/logo.webp | 0 / 15 | onepiece-official |
| One Piece Card Game | ST-27: Starter Deck 27 BLACK Marshall.D.Teach | https://en.onepiece-cardgame.com/renewal/images/products/decks/st27/logo.webp | 0 / 15 | onepiece-official |
| One Piece Card Game | ST-28: Starter Deck 28 GREEN/YELLOW Yamato | https://en.onepiece-cardgame.com/renewal/images/products/decks/st28/logo.webp | 0 / 15 | onepiece-official |
| One Piece Card Game | ST-29: Starter Deck 29 Egghead | https://en.onepiece-cardgame.com/renewal/images/products/decks/st29/logo.webp | 0 / 31 | onepiece-official |
| One Piece Card Game | ST-30: Starter Deck 30 EX Luffy & Ace |  | 0 / 34 | — |
| One Piece Card Game | ST-31: Starter Deck 31 RED Monkey.D.Luffy |  | 0 / 10 | — |
| One Piece Card Game | ST-32: Starter Deck 32 GREEN Roronoa Zoro |  | 0 / 9 | — |
| One Piece Card Game | ST-33: Starter Deck 33 BLUE Kuzan |  | 0 / 9 | — |
| One Piece Card Game | ST-34: Starter Deck 34 PURPLE Charlotte Katakuri |  | 0 / 10 | — |
| One Piece Card Game | ST-35: Starter Deck 35 RED/BLACK Sabo |  | 0 / 9 | — |
| One Piece Card Game | ST-36: Starter Deck 36 YELLOW Eustass"Captain"Kid |  | 0 / 11 | — |
| One Piece Card Game | Set Sail Deck Set |  | 0 / 30 | — |
| One Piece Card Game | The Azure Sea's Seven | https://holodex-prod-bucket.b-cdn.net/sets/op_24537/logo.webp | 150 / 211 | holodex |
| One Piece Card Game | The Azure Sea's Seven Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24537/logo.webp ※ | 89 / 89 | holodex（继承父系列） |
| One Piece Card Game | The Dominance of God |  | 6 / 27 | — |
| One Piece Card Game | The Time of Battle | https://holodex-prod-bucket.b-cdn.net/sets/op_24664/logo.webp | 159 / 159 | holodex |
| One Piece Card Game | The Time of Battle Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24664/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | The World's Strongest Warriors | https://holodex-prod-bucket.b-cdn.net/sets/op_1724736/logo.webp | 177 / 179 | holodex |
| One Piece Card Game | The World's Strongest Warriors Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_1724736/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | Two Legends | https://holodex-prod-bucket.b-cdn.net/sets/op_23462/logo.webp | 50 / 154 | holodex |
| One Piece Card Game | Two Legends Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23462/logo.webp ※ | 75 / 75 | holodex（继承父系列） |
| One Piece Card Game | Wings of the Captain | https://holodex-prod-bucket.b-cdn.net/sets/op_23272/logo.webp | 154 / 154 | holodex |
| One Piece Card Game | Wings of the Captain Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23272/logo.webp ※ | 75 / 75 | holodex（继承父系列） |

### Disney Lorcana（20 个系列，15 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Disney Lorcana | Archazia's Island | https://holodex-prod-bucket.b-cdn.net/sets/dl_24011/logo.webp | 245 / 245 | holodex |
| Disney Lorcana | Attack of the Vine! | https://holodex-prod-bucket.b-cdn.net/sets/dl_24666/logo.webp | 261 / 261 | holodex |
| Disney Lorcana | Azurite Sea | https://holodex-prod-bucket.b-cdn.net/sets/dl_23746/logo.webp | 149 / 232 | holodex |
| Disney Lorcana | D23 Promos | https://holodex-prod-bucket.b-cdn.net/sets/dl_17690/logo.webp | 23 / 23 | holodex |
| Disney Lorcana | Disney Lorcana Promo Cards | https://holodex-prod-bucket.b-cdn.net/sets/dl_23234/logo.webp | 172 / 187 | holodex |
| Disney Lorcana | Disney100 Promos |  | 6 / 6 | — |
| Disney Lorcana | Fabled | https://holodex-prod-bucket.b-cdn.net/sets/dl_24348/logo.webp | 253 / 253 | holodex |
| Disney Lorcana | Hyperia City |  | 0 / 244 | — |
| Disney Lorcana | Illumineer's Quest: Deep Trouble |  | 39 / 39 | — |
| Disney Lorcana | Illumineer's Quest: Palace Heist |  | 43 / 43 | — |
| Disney Lorcana | Illumineer's Quest: The Great Hunny Rescue |  | 5 / 44 | — |
| Disney Lorcana | Into the Inklands | https://holodex-prod-bucket.b-cdn.net/sets/dl_23367/logo.webp | 150 / 228 | holodex |
| Disney Lorcana | Reign of Jafar | https://holodex-prod-bucket.b-cdn.net/sets/dl_24258/logo.webp | 100 / 270 | holodex |
| Disney Lorcana | Rise of the Floodborn | https://holodex-prod-bucket.b-cdn.net/sets/dl_23303/logo.webp | 223 / 223 | holodex |
| Disney Lorcana | Shimmering Skies | https://holodex-prod-bucket.b-cdn.net/sets/dl_23536/logo.webp | 0 / 222 | holodex |
| Disney Lorcana | The First Chapter | https://holodex-prod-bucket.b-cdn.net/sets/dl_22937/logo.webp | 222 / 223 | holodex |
| Disney Lorcana | Ursula's Return | https://holodex-prod-bucket.b-cdn.net/sets/dl_23474/logo.webp | 232 / 232 | holodex |
| Disney Lorcana | Whispers in the Well | https://holodex-prod-bucket.b-cdn.net/sets/dl_24414/logo.webp | 150 / 261 | holodex |
| Disney Lorcana | Wilds Unknown | https://holodex-prod-bucket.b-cdn.net/sets/dl_24617/logo.webp | 200 / 267 | holodex |
| Disney Lorcana | Winterspell | https://holodex-prod-bucket.b-cdn.net/sets/dl_24500/logo.webp | 266 / 266 | holodex |

### Flesh and Blood TCG（105 个系列，88 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Flesh and Blood TCG | 1st Strike | https://cdn.fabtcg.com/uploads/2025/09/1ststrike_blitz_dropshadow.webp | 62 / 62 | fab-official |
| Flesh and Blood TCG | Arcane Rising | https://cdn.fabtcg.com/uploads/2025/11/ARC-1.png | 50 / 284 | fab-official |
| Flesh and Blood TCG | Armory Deck Origins: Hala | https://cdn.fabtcg.com/uploads/2026/03/LO-RES_FR_Hala_ArmoryDeck_Mockup.png | 27 / 27 | fab-official |
| Flesh and Blood TCG | Armory Deck: Arakni | https://cdn.fabtcg.com/uploads/2025/12/arakni_name.png | 31 / 31 | fab-official |
| Flesh and Blood TCG | Armory Deck: Aurora | https://cdn.fabtcg.com/uploads/2025/07/aurora_cover.2e16d0ba.fill-1200x630-1.jpg | 28 / 28 | fab-official |
| Flesh and Blood TCG | Armory Deck: Azalea | https://cdn.fabtcg.com/uploads/2025/07/ad_azalea_dropshadow.webp | 32 / 32 | fab-official |
| Flesh and Blood TCG | Armory Deck: Boltyn | https://cdn.fabtcg.com/uploads/2025/07/ad-boltyn_dropshadow.webp | 28 / 28 | fab-official |
| Flesh and Blood TCG | Armory Deck: Dash | https://cdn.fabtcg.com/uploads/2025/07/ad_dash_dropshadow.webp | 27 / 27 | fab-official |
| Flesh and Blood TCG | Armory Deck: Dr. Mortimer | https://cdn.fabtcg.com/uploads/2026/08/mortimer_name.png | 4 / 4 | fab-official |
| Flesh and Blood TCG | Armory Deck: Gravy Bones | https://cdn.fabtcg.com/uploads/2025/12/gravy_ad_cover-scaled.jpg | 49 / 49 | fab-official |
| Flesh and Blood TCG | Armory Deck: Ira | https://cdn.fabtcg.com/uploads/2025/07/ad_ira_dropshadow.webp | 27 / 27 | fab-official |
| Flesh and Blood TCG | Armory Deck: Jarl Vetreidi |  | 27 / 27 | — |
| Flesh and Blood TCG | Armory Deck: Kayo | https://cdn.fabtcg.com/uploads/2025/07/ad_kayo_dropshadow.webp | 28 / 28 | fab-official |
| Flesh and Blood TCG | Armory Deck: Legends Prism | https://cdn.fabtcg.com/uploads/2025/07/ad_legends_product_dropshadow.webp ※ | 27 / 27 | fab-official（继承父系列） |
| Flesh and Blood TCG | Armory Deck: Legends Viserai | https://cdn.fabtcg.com/uploads/2025/07/ad_legends_product_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Armory Deck: Malice | https://cdn.fabtcg.com/uploads/2026/07/malice_name.png | 8 / 30 | fab-official |
| Flesh and Blood TCG | Armory Deck: Maxx Nitro | https://cdn.fabtcg.com/uploads/2025/07/ad_maxx_dropshadow.webp | 30 / 30 | fab-official |
| Flesh and Blood TCG | Armory Deck: Olympia | https://cdn.fabtcg.com/uploads/2026/04/BDO-01.webp | 29 / 29 | fab-official |
| Flesh and Blood TCG | Armory Deck: Pleiades | https://cdn.fabtcg.com/uploads/2025/12/jp_pleiades_name.png | 32 / 32 | fab-official |
| Flesh and Blood TCG | Armory Deck: Rhinar | https://cdn.fabtcg.com/uploads/2025/12/rhinar_name.png | 30 / 30 | fab-official |
| Flesh and Blood TCG | Armory Deck: Zyggy | https://cdn.fabtcg.com/uploads/2026/02/en_ad_zyggy_mockup_LO-RES.png | 30 / 30 | fab-official |
| Flesh and Blood TCG | Blitz Deck: Heavy Hitters - Betsy | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp ※ | 31 / 31 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Heavy Hitters - Kassai | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Heavy Hitters - Kayo | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Heavy Hitters - Olympia | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Heavy Hitters - Rhinar | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Heavy Hitters - Victor | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Monarch - Boltyn | https://cdn.fabtcg.com/uploads/2025/09/mon_mock_herodeck_box_02_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Monarch - Chane | https://cdn.fabtcg.com/uploads/2025/09/mon_mock_herodeck_box_02_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Monarch - Levia | https://cdn.fabtcg.com/uploads/2025/09/mon_mock_herodeck_box_02_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Monarch - Prism | https://cdn.fabtcg.com/uploads/2025/09/mon_mock_herodeck_box_02_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Outsiders - Arakni | https://cdn.fabtcg.com/uploads/2025/09/outsiders_blitz_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Outsiders - Azalea | https://cdn.fabtcg.com/uploads/2025/09/outsiders_blitz_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Outsiders - Benji | https://cdn.fabtcg.com/uploads/2025/09/outsiders_blitz_dropshadow.webp ※ | 26 / 26 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Outsiders - Katsu | https://cdn.fabtcg.com/uploads/2025/09/outsiders_blitz_dropshadow.webp ※ | 26 / 26 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Outsiders - Riptide | https://cdn.fabtcg.com/uploads/2025/09/outsiders_blitz_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Outsiders - Uzuri | https://cdn.fabtcg.com/uploads/2025/09/outsiders_blitz_dropshadow.webp ※ | 31 / 31 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Part the Mistveil - Enigma | https://cdn.fabtcg.com/uploads/2025/09/mistveil_collection_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Part the Mistveil - Nuu | https://cdn.fabtcg.com/uploads/2025/09/mistveil_collection_dropshadow.webp ※ | 28 / 28 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Part the Mistveil - Zen | https://cdn.fabtcg.com/uploads/2025/09/mistveil_collection_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Rosetta - Aurora | https://cdn.fabtcg.com/uploads/2025/09/rosetta_blitz_collection_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Rosetta - Florian | https://cdn.fabtcg.com/uploads/2025/09/rosetta_blitz_collection_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Rosetta - Oscilio | https://cdn.fabtcg.com/uploads/2025/09/rosetta_blitz_collection_dropshadow.webp ※ | 29 / 29 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Rosetta - Verdance | https://cdn.fabtcg.com/uploads/2025/09/rosetta_blitz_collection_dropshadow.webp ※ | 28 / 28 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Tales of Aria - Briar | https://cdn.fabtcg.com/uploads/2025/07/toa_mock_herodeck_box_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Tales of Aria - Lexi | https://cdn.fabtcg.com/uploads/2025/07/toa_mock_herodeck_box_dropshadow.webp ※ | 30 / 30 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Tales of Aria - Oldhim | https://cdn.fabtcg.com/uploads/2025/07/toa_mock_herodeck_box_dropshadow.webp ※ | 32 / 32 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: The Hunted - Arakni | https://cdn.fabtcg.com/uploads/2025/07/hnt_collection_dropshadow.webp ※ | 26 / 26 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: The Hunted - Arakni, Web of Deceit | https://cdn.fabtcg.com/uploads/2025/07/hnt_collection_dropshadow.webp ※ | 31 / 31 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: The Hunted - Cindra | https://cdn.fabtcg.com/uploads/2025/07/hnt_collection_dropshadow.webp ※ | 28 / 28 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: The Hunted - Fang | https://cdn.fabtcg.com/uploads/2025/07/hnt_collection_dropshadow.webp ※ | 28 / 28 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Uprising - Dromai | https://cdn.fabtcg.com/uploads/2025/07/upr_mock_blitz_display_box_01_Fx5.width-992.format-webp.webp ※ | 28 / 28 | fab-official（继承父系列） |
| Flesh and Blood TCG | Blitz Deck: Uprising - Fai | https://cdn.fabtcg.com/uploads/2025/07/upr_mock_blitz_display_box_01_Fx5.width-992.format-webp.webp ※ | 26 / 26 | fab-official（继承父系列） |
| Flesh and Blood TCG | Bright Lights | https://cdn.fabtcg.com/uploads/2025/08/en_evo_mock_boosterbox.width-992.format-webp.webp | 200 / 261 | fab-official |
| Flesh and Blood TCG | Classic Battles: Rhinar vs Dorinthea | https://cdn.fabtcg.com/uploads/2025/12/cb_logo_1.png | 54 / 55 | fab-official |
| Flesh and Blood TCG | Compendium of Rathe | https://cdn.fabtcg.com/uploads/2026/01/pen-logo-2026.png | 368 / 368 | fab-official |
| Flesh and Blood TCG | Compendium of Rathe - Antiquity Pack |  | 65 / 65 | — |
| Flesh and Blood TCG | Crucible of War | https://cdn.fabtcg.com/uploads/2025/12/cru_logo_stacked.png | 100 / 199 | fab-official |
| Flesh and Blood TCG | Dusk till Dawn | https://cdn.fabtcg.com/uploads/2025/07/dtd_booster_box.width-992.format-webp.webp | 100 / 252 | fab-official |
| Flesh and Blood TCG | Dynasty | https://cdn.fabtcg.com/uploads/2025/07/dyn_mock_booster_box.width-992.format-webp.webp | 100 / 265 | fab-official |
| Flesh and Blood TCG | Everfest | https://cdn.fabtcg.com/uploads/2025/07/evr_paper_booster_dropshadow.webp | 220 / 221 | fab-official |
| Flesh and Blood TCG | Flesh and Blood: Promo Cards |  | 50 / 1233 | — |
| Flesh and Blood TCG | GEM Pack 1 |  | 50 / 50 | — |
| Flesh and Blood TCG | GEM Pack 2 |  | 54 / 54 | — |
| Flesh and Blood TCG | GEM Pack 3 |  | 54 / 54 | — |
| Flesh and Blood TCG | GEM Pack 4 |  | 54 / 54 | — |
| Flesh and Blood TCG | GEM Pack 6 |  | 2 / 35 | — |
| Flesh and Blood TCG | Gem Pack 5 |  | 61 / 61 | — |
| Flesh and Blood TCG | Heavy Hitters | https://cdn.fabtcg.com/uploads/2025/08/en_heavy_hitters_booster_display.width-1200.format-webp.webp | 239 / 262 | fab-official |
| Flesh and Blood TCG | Hero Deck: Bravo |  | 29 / 29 | — |
| Flesh and Blood TCG | Hero Deck: Dorinthea |  | 30 / 30 | — |
| Flesh and Blood TCG | Hero Deck: Katsu |  | 30 / 30 | — |
| Flesh and Blood TCG | Hero Deck: Rhinar |  | 31 / 31 | — |
| Flesh and Blood TCG | High Seas | https://cdn.fabtcg.com/uploads/2025/07/en_sea_display_gravybones.width-1200.format-webp-1.webp | 369 / 375 | fab-official |
| Flesh and Blood TCG | Historic Pack 1 Blitz Deck: Bravo | https://cdn.fabtcg.com/uploads/2025/09/hp1_blitz_dropshadow.webp ※ | 27 / 27 | fab-official（继承父系列） |
| Flesh and Blood TCG | Historic Pack 1 Blitz Deck: Dash | https://cdn.fabtcg.com/uploads/2025/09/hp1_blitz_dropshadow.webp ※ | 28 / 28 | fab-official（继承父系列） |
| Flesh and Blood TCG | Historic Pack 1 Blitz Deck: Dorinthea | https://cdn.fabtcg.com/uploads/2025/09/hp1_blitz_dropshadow.webp ※ | 27 / 27 | fab-official（继承父系列） |
| Flesh and Blood TCG | Historic Pack 1 Blitz Deck: Kano | https://cdn.fabtcg.com/uploads/2025/09/hp1_blitz_dropshadow.webp ※ | 27 / 27 | fab-official（继承父系列） |
| Flesh and Blood TCG | Historic Pack 1 Blitz Deck: Rhinar | https://cdn.fabtcg.com/uploads/2025/09/hp1_blitz_dropshadow.webp ※ | 26 / 26 | fab-official（继承父系列） |
| Flesh and Blood TCG | Historic Pack 1 Blitz Deck: Viserai | https://cdn.fabtcg.com/uploads/2025/09/hp1_blitz_dropshadow.webp ※ | 27 / 27 | fab-official（继承父系列） |
| Flesh and Blood TCG | History Pack Vol.1 | https://cdn.fabtcg.com/uploads/2025/09/1hp_booster_dropshadow.webp | 0 / 427 | fab-official |
| Flesh and Blood TCG | Mastery Pack Assassin | https://cdn.fabtcg.com/uploads/2026/08/mpa-web-logo.webp | 9 / 14 | fab-official |
| Flesh and Blood TCG | Mastery Pack Guardian | https://cdn.fabtcg.com/uploads/2025/07/masterypack_guardian_booster_dropshadow.webp | 0 / 148 | fab-official |
| Flesh and Blood TCG | Mastery Pack Warrior | https://cdn.fabtcg.com/uploads/2026/03/mpw-logo-scaled.webp | 165 / 165 | fab-official |
| Flesh and Blood TCG | Monarch | https://cdn.fabtcg.com/uploads/2025/12/mon_article_cover_standard.jpg | 100 / 313 | fab-official |
| Flesh and Blood TCG | Omens of the Third Age | https://cdn.fabtcg.com/uploads/2026/03/en_omn_display_aurora-2-1.png | 0 / 291 | fab-official |
| Flesh and Blood TCG | Outsiders | https://cdn.fabtcg.com/uploads/2025/09/out_en_mock_booster_box.width-992.format-webp.webp | 96 / 255 | fab-official |
| Flesh and Blood TCG | Part the Mistveil | https://cdn.fabtcg.com/uploads/2025/07/mst_booster_dropshadow.webp | 0 / 265 | fab-official |
| Flesh and Blood TCG | Rosetta | https://cdn.fabtcg.com/uploads/2025/09/rosetta_boosters_dropshadow.webp | 50 / 327 | fab-official |
| Flesh and Blood TCG | Round the Table: TCCxLSS | https://cdn.fabtcg.com/uploads/2025/12/TCC_mkt_release_twtcover2.jpg | 110 / 110 | fab-official |
| Flesh and Blood TCG | Silver Age Chapter 1 |  | 173 / 173 | — |
| Flesh and Blood TCG | Silver Age Chapter 2 |  | 0 / 169 | — |
| Flesh and Blood TCG | Silver Age Chapter 3 | https://cdn.fabtcg.com/uploads/2025/10/en_slv_display_ch2_LO-RES.png | 173 / 175 | fab-official |
| Flesh and Blood TCG | Silver Age: Usurp the Shadow Throne | https://cdn.fabtcg.com/uploads/2025/12/silver_age_logo.png | 34 / 68 | fab-official |
| Flesh and Blood TCG | Smash Palace | https://cdn.fabtcg.com/uploads/2026/04/AD_Olympia_Banner_Background.webp | 32 / 32 | fab-official |
| Flesh and Blood TCG | Smash Palace: Chorus of Steel | https://cdn.fabtcg.com/uploads/2026/07/spw_logo.png | 12 / 12 | fab-official |
| Flesh and Blood TCG | Super Slam | https://cdn.fabtcg.com/uploads/2025/07/sup_tuffnutlyath_booster_dropshadow.webp | 0 / 301 | fab-official |
| Flesh and Blood TCG | Tales of Aria | https://cdn.fabtcg.com/uploads/2025/09/toa_mock_booster_box__first_editi.width-992.format-webp_juJoQmE-1.webp | 236 / 239 | fab-official |
| Flesh and Blood TCG | The Hunted | https://cdn.fabtcg.com/uploads/2025/07/hnt_booster_dropshadow.webp | 297 / 299 | fab-official |
| Flesh and Blood TCG | Uprising | https://cdn.fabtcg.com/uploads/2025/08/upr_mock_booster_box_Fx5.width-992.format-webp.webp | 97 / 243 | fab-official |
| Flesh and Blood TCG | Usurp the Shadow Throne | https://cdn.fabtcg.com/uploads/2026/07/usurp_the_shadow_throne_logo.png | 82 / 287 | fab-official |
| Flesh and Blood TCG | Usurp the Shadow Throne Pre-release Cards | https://cdn.fabtcg.com/uploads/2026/07/usurp_the_shadow_throne_logo.png ※ | 4 / 5 | fab-official（继承父系列） |
| Flesh and Blood TCG | Welcome Deck Bravo |  | 18 / 18 | — |
| Flesh and Blood TCG | Welcome Deck: Ira |  | 12 / 12 | — |
| Flesh and Blood TCG | Welcome to Rathe | https://cdn.fabtcg.com/uploads/2025/09/wtr_alpha_booster_dropshadow-scaled.webp | 302 / 303 | fab-official |

### Dragon Ball Super: Masters（100 个系列，59 个有 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 | logo来源 |
|------|------|----------|------------------|----------|
| Dragon Ball Super: Masters | 5th Anniversary Set |  | 0 / 78 | — |
| Dragon Ball Super: Masters | Assault of the Saiyans | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2473/logo.webp | 0 / 160 | holodex |
| Dragon Ball Super: Masters | Assault of the Saiyans Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2957/logo.webp | 0 / 108 | holodex |
| Dragon Ball Super: Masters | Battle Evolution Booster | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2759/logo.webp | 0 / 125 | holodex |
| Dragon Ball Super: Masters | Beyond Generations | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23325/logo.webp | 0 / 249 | holodex |
| Dragon Ball Super: Masters | Beyond Generations Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23463/logo.webp | 0 / 59 | holodex |
| Dragon Ball Super: Masters | Clash of Fates | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2367/logo.webp | 0 / 77 | holodex |
| Dragon Ball Super: Masters | Collector's Selection Vol. 1 |  | 0 / 18 | — |
| Dragon Ball Super: Masters | Collector's Selection Vol. 2 |  | 0 / 18 | — |
| Dragon Ball Super: Masters | Collector's Selection Vol. 3 |  | 0 / 18 | — |
| Dragon Ball Super: Masters | Colossal Warfare | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2218/logo.webp | 0 / 138 | holodex |
| Dragon Ball Super: Masters | Critical Blow | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23175/logo.webp | 0 / 163 | holodex |
| Dragon Ball Super: Masters | Critical Blow Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23176/logo.webp | 0 / 59 | holodex |
| Dragon Ball Super: Masters | Cross Spirits | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2858/logo.webp | 0 / 178 | holodex |
| Dragon Ball Super: Masters | Cross Spirits Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2949/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Cross Worlds | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2173/logo.webp | 0 / 138 | holodex |
| Dragon Ball Super: Masters | Dawn of the Z-Legends | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_3132/logo.webp | 0 / 184 | holodex |
| Dragon Ball Super: Masters | Dawn of the Z-Legends Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_3168/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Destroyer Kings | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2392/logo.webp | 0 / 147 | holodex |
| Dragon Ball Super: Masters | Destroyer Kings Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2430/logo.webp | 0 / 60 | holodex |
| Dragon Ball Super: Masters | Draft Box 04 - Dragon Brawl | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2515/logo.webp | 0 / 122 | holodex |
| Dragon Ball Super: Masters | Draft Box 05 - Divine Multiverse | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2618/logo.webp | 0 / 178 | holodex |
| Dragon Ball Super: Masters | Draft Box 06 - Giant Force | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2720/logo.webp | 0 / 144 | holodex |
| Dragon Ball Super: Masters | Expansion Deck Box Set 01: Mighty Heroes |  | 0 / 14 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 02: Dark Demon's Villains |  | 0 / 14 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 03: Ultimate Box |  | 0 / 35 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 04: Unity of Saiyans |  | 0 / 4 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 05: Unity of Destruction |  | 0 / 4 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 07: Magnificent Collection - Fusion Hero |  | 0 / 27 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 08: Magnificent Collection - Forsaken Warrior |  | 0 / 25 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 09: Saiyan Surge |  | 0 / 6 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 10: Namekian Surge |  | 0 / 6 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 11: Universe 7 Unison |  | 0 / 7 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 12: Universe 11 Unison |  | 0 / 7 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 14: Battle Advanced |  | 0 / 5 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 15: Battle Enhanced |  | 0 / 5 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 16: Ultimate Deck |  | 0 / 10 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 17: Saiyan Boost |  | 0 / 5 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 18: Namekian Boost |  | 0 / 5 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 20: Ultimate Deck 2022 |  | 0 / 20 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 22: Ultimate Deck 2023 |  | 0 / 27 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 23: Premium Anniversary Box 2023 |  | 0 / 59 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 24: Premium 7th Anniversary Box 2024 |  | 0 / 55 | — |
| Dragon Ball Super: Masters | Expansion Deck Box Set 25: Premium Anniversary Box 2025 |  | 0 / 70 | — |
| Dragon Ball Super: Masters | Fearsome Rivals | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_24565/logo.webp | 0 / 198 | holodex |
| Dragon Ball Super: Masters | Fearsome Rivals Release Event |  | 0 / 73 | — |
| Dragon Ball Super: Masters | Fighter's Ambition |  | 0 / 164 | — |
| Dragon Ball Super: Masters | Galactic Battle | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_1962/logo.webp | 0 / 120 | holodex |
| Dragon Ball Super: Masters | History of Z | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_24166/logo.webp | 0 / 188 | holodex |
| Dragon Ball Super: Masters | History of Z Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_24188/logo.webp | 0 / 59 | holodex |
| Dragon Ball Super: Masters | Impact Beyond Dimensions | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_ibd24670/logo.webp | 0 / 190 | holodex |
| Dragon Ball Super: Masters | Impact Beyond Dimensions Release Event |  | 0 / 74 | — |
| Dragon Ball Super: Masters | Judge Promotion Cards |  | 0 / 224 | — |
| Dragon Ball Super: Masters | Legend of the Dragon Balls | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23415/logo.webp | 0 / 172 | holodex |
| Dragon Ball Super: Masters | Legend of the Dragon Balls Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23530/logo.webp | 0 / 59 | holodex |
| Dragon Ball Super: Masters | Malicious Machinations | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2536/logo.webp | 0 / 163 | holodex |
| Dragon Ball Super: Masters | Malicious Machinations Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2956/logo.webp | 0 / 108 | holodex |
| Dragon Ball Super: Masters | Miraculous Revival | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2285/logo.webp | 0 / 142 | holodex |
| Dragon Ball Super: Masters | Mythic Booster |  | 0 / 126 | — |
| Dragon Ball Super: Masters | Oversized Cards |  | 0 / 13 | — |
| Dragon Ball Super: Masters | Perfect Combination | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23258/logo.webp | 0 / 155 | holodex |
| Dragon Ball Super: Masters | Power Absorbed | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_17696/logo.webp | 0 / 261 | holodex |
| Dragon Ball Super: Masters | Power Absorbed Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_17697/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Prismatic Clash | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_24402/logo.webp | 0 / 197 | holodex |
| Dragon Ball Super: Masters | Prismatic Clash Release Event |  | 0 / 74 | — |
| Dragon Ball Super: Masters | Promotion Cards |  | 0 / 884 | — |
| Dragon Ball Super: Masters | Realm of the Gods | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2986/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Realm of the Gods Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_3003/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Revision Pack 2020 |  | 0 / 30 | — |
| Dragon Ball Super: Masters | Rise of the Unison Warrior | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2647/logo.webp | 0 / 182 | holodex |
| Dragon Ball Super: Masters | Rise of the Unison Warrior (2nd Edition) | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2910/logo.webp | 0 / 182 | holodex |
| Dragon Ball Super: Masters | Rise of the Unison Warrior Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2953/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Saiyan Showdown | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2913/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Saiyan Showdown Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2946/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Special Anniversary Set |  | 0 / 56 | — |
| Dragon Ball Super: Masters | Special Anniversary Set 2020 |  | 0 / 56 | — |
| Dragon Ball Super: Masters | Special Anniversary Set 2021 |  | 0 / 56 | — |
| Dragon Ball Super: Masters | Supreme Rivalry | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2796/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Supreme Rivalry Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2950/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Theme Selection: History of Son Goku |  | 0 / 15 | — |
| Dragon Ball Super: Masters | Theme Selection: History of Vegeta |  | 0 / 15 | — |
| Dragon Ball Super: Masters | Three Glorious Fighters | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_24632/logo.webp | 0 / 199 | holodex |
| Dragon Ball Super: Masters | Three Glorious Fighters Release Event |  | 0 / 74 | — |
| Dragon Ball Super: Masters | Tournament Promotion Cards |  | 0 / 1315 | — |
| Dragon Ball Super: Masters | Tournament of Power | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2217/logo.webp | 0 / 101 | holodex |
| Dragon Ball Super: Masters | Ultimate Advent | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23646/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Ultimate Advent Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23647/logo.webp | 0 / 57 | holodex |
| Dragon Ball Super: Masters | Ultimate Squad | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_3030/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Ultimate Squad Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_3083/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | Union Force | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2070/logo.webp | 0 / 128 | holodex |
| Dragon Ball Super: Masters | Universal Onslaught | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2590/logo.webp | 0 / 163 | holodex |
| Dragon Ball Super: Masters | Universal Onslaught Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2954/logo.webp | 0 / 108 | holodex |
| Dragon Ball Super: Masters | Vermilion Bloodline | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2691/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Vermilion Bloodline (2nd Edition) | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2911/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Vermilion Bloodline Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2952/logo.webp | 0 / 127 | holodex |
| Dragon Ball Super: Masters | Vicious Rejuvenation | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2755/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Vicious Rejuvenation Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2951/logo.webp | 0 / 128 | holodex |
| Dragon Ball Super: Masters | Wild Resurgence | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23115/logo.webp | 0 / 164 | holodex |
| Dragon Ball Super: Masters | Wild Resurgence Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_23116/logo.webp | 0 / 68 | holodex |
| Dragon Ball Super: Masters | World Martial Arts Tournament | https://holodex-prod-bucket.b-cdn.net/sets/dbsc_2297/logo.webp | 0 / 77 | holodex |

> `※` = 该系列是促销/预发售/发售活动等衍生子线，logo 继承自同名的父系列。

## 三、logo 来源与缺口

### 3.1 各来源明细

| 来源 | 是什么 | 数据量 | 接入方式 |
|------|--------|--------|----------|
| Scryfall | 印在卡面上的**系列符号**（SVG） | 1058 个 set | `api.scryfall.com/sets`，先按 `setCode`↔`code`，再按名 |
| ygoprodeck | 官方**系列图**（JPG） | 1035 个 set | `db.ygoprodeck.com/api/v7/cardsets.php`，先按 `setCode`↔`set_code`，再按名 |
| TCGdex | 系列 **logo**（webp/png） | 220 个 set，其中 156 个有 logo | `api.tcgdex.net/v2/en/sets/{id}`，按 `setCode`↔`abbreviation`，再按名 |
| Holodex | 第三方 App 的系列 logo（webp） | 存量 12 个游戏 | `crawl/crawl/holodex_sets_organized.json`，按名 |
| FAB 官方站 | 系列 logo / 产品封面（png/webp），88 条命中 | 275 个页面 | `fabtcg.com`（被 Cloudflare 挡，用 `curl_cffi` 伪装 TLS 指纹），sitemap + products/digital-assets 页 |
| Bulbapedia 图库 | 日文系列 logo / 包装图，177 条命中 | 按代码前缀枚举 | `archives.bulbagarden.net/w/api.php` + `bulbapedia.bulbagarden.net/w/api.php`（opensearch 找条目），文件名形如 `S8b_VMAX_Climax_Logo.png` |
| ONE PIECE 官方站 | 产品 logo（webp），7 条命中 | 187 个产品页 | `en.onepiece-cardgame.com/products/`，按产品代号 `ST-27` 之类 |

**表内所有 logo URL 已逐个校验可访问**（`script_temp/verify_logo_urls.py`，HEAD 请求）。

注意两点：万智牌里有 4 个系列拿到的 Scryfall 图标是通用默认符号（`default.svg`），说明该系列在 Scryfall 没有专属符号；另有 123 条是衍生子线继承父系列 logo（表中标 `※`）、35 条是人工核对指定。

匹配规则上的两道保险：**代号必须在本品线内唯一**（否则 `PR` 这类被 12 个系列共用的促销码会撞车），**词元数少于 2 个不走词元匹配**（否则 `Promos-A` 会撞上 `XY Promos`）。

ygoprodeck 的一个已知局限：它用 `set_code` 拼图片地址，而它自己有 142 个代号被 531 个不同 set 共用（如 `YS15` 同时对应 2-Player Starter Deck、Dark Legion、Saber Force 三副预组），这些系列拿到的是同一张图，未必是该系列专属。

### 3.2 仍然没有 logo 的系列及原因

- **Pokémon**：29 个未覆盖
  - 缺的是 Trainer Kit、各类 Promo、World Championship Decks、Jumbo Cards 等子线，TCGdex / Holodex / Scryfall 三类源都不单独收录。
  - 明细：BW Trainer Kit: Excadrill & Zoroark、Best of Promos、Blister Exclusives、Burger King Promos、Countdown Calendar Promos、DP Trainer Kit: Manaphy & Lucario、Deck Exclusives、EX Trainer Kit 1: Latias & Latios、EX Trainer Kit 2: Plusle & Minun、First Partner Collection 2026、First Partner Pack、HGSS Trainer Kit: Gyarados & Raichu …
- **Pokémon Japan**：278 个未覆盖
  - 已有的 177 条来自 Bulbapedia 图库，按系列代码做前缀枚举命中（Bulbapedia 的 logo 文件名就是 `{代码}_{名称}_Logo.png`）。剩余的没命中，是因为 **TCGPlayer 有 153 个系列根本没给代码**（都是 1996–2009 的老扩展包与预组，如 `Pokemon VS`、`City Gym Decks`），另外 158 个有代码的里多数在 Bulbapedia 上只有卡图、没有包装图或 logo（如 `SM-P`、`XY-P` 这类促销线，前缀查询返回 0 个文件）。TCGdex 的日文 set 没有 logo 字段；官方 `pokemon-card.com` 只在最新产品页放 logo。
  - 明细：10th Movie Commemoration Set、11th Movie Commemoration Set、64 Mario Stadium Best Photo Contest、ADV Expansion Pack、ADV-P Promotional cards、Aqua Deck Kit、Arceus LV.X Deck: Grass & Fire、Arceus LV.X Deck: Lightning & Psychic、Awakening Legends、BK: Cobalion Battle Strength Deck、BK: Terrakion Battle Strength Deck、BK: Virizion Battle Strength Deck …
- **Magic: The Gathering**：24 个未覆盖
  - 缺的是 TCGPlayer 独有的促销聚合线（`Oversize Cards`、`Prerelease Cards`、`Buy-A-Box Promos`、`WPN & Gateway Promos` 等），Scryfall 侧按年度拆开收录、没有与之对应的单一条目；可对应的 20 条已人工核对补上（见 3.3）。
  - 明细：30th Anniversary Promos、AFR Ampersand Promos、APAC Lands、Archenemy: Duskmourn、Buy-A-Box Promos、Commander、Duel Decks: Anthology、Gift Boxes and Promos、International Edition、JingHe Age Token Cards、Junior Series Promos、Launch Party & Release Event Promos …
- **Yu-Gi-Oh!**：99 个未覆盖
  - 缺的是铁盒、收藏盒、活动场次卡等子线，ygoprodeck 对这批 set 只给名录不给图（1035 个 set 里有 125 个没有 `set_image` 字段，且用 `set_code` 拼 URL 也是 404）。
  - 明细：2-Player Starter Set、2002 Collectors Tin、2003 Collectors Tin、2004 Collectors Tin、2011 Duelist Pack Tin、25th Anniversary Tin: Dueling Mirrors、Advent Calendar 2011 (Adventskalender)、Advent Calendar 2014 (Adventskalender ZEXAL-Edition)、Collector's Boxes、Crossed Souls: Advanced Edition、Dawn of Destiny Xbox、Destiny Board Traveler Promo …
- **One Piece Card Game**：43 个未覆盖
  - 缺的绝大多数是 `ST-01`…`ST-20` 早期预组：官方站对应产品页（`decks/st05.php`、`st15-20.php`）只放了卡图，没有预组 logo 或包装图；`optcgapi.com` 只收录 22 个主系列。
  - 明细：Awakening of the New Era: 1st Anniversary Tournament Cards、Carrying On His Will: 3rd Anniversary Tournament Cards、Emperors in the New World: 2nd Anniversary Tournament Cards、Extra Booster: One Piece Heroines Edition Vol. 2、Learn Together Deck Set、One Piece Demo Deck Cards、One Piece Promotion Cards、Revision Pack Cards、ST-01: Starter Deck 1 Straw Hat Crew、ST-01: Starter Deck 1 Straw Hat Crew (Super Pre-Release Edition)、ST-02: Starter Deck 2 Worst Generation、ST-02: Starter Deck 2 Worst Generation (Super Pre-Release Edition) …
- **Disney Lorcana**：5 个未覆盖
  - 缺的是铁盒、收藏盒、活动场次卡等子线，ygoprodeck 对这批 set 只给名录不给图（1035 个 set 里有 125 个没有 `set_image` 字段，且用 `set_code` 拼 URL 也是 404）。
  - 明细：Disney100 Promos、Hyperia City、Illumineer's Quest: Deep Trouble、Illumineer's Quest: Palace Heist、Illumineer's Quest: The Great Hunny Rescue
- **Flesh and Blood TCG**：17 个未覆盖
  - 已通过 `curl_cffi` 绕过 Cloudflare 抓到官方站 275 个页面的系列 logo 与封面图。剩余的是官方站**没有独立素材**的：单副 Blitz Deck（官网只按合集页出售，如 `Blitz Deck: Monarch - Boltyn` 只存在于 `monarch-blitz-decks` 合集里，已按父合集图继承）、`GEM Pack`、`Hero Deck`、`Welcome Deck` / `Flesh and Blood: Promo Cards`。
  - 明细：Armory Deck: Jarl Vetreidi、Compendium of Rathe - Antiquity Pack、Flesh and Blood: Promo Cards、GEM Pack 1、GEM Pack 2、GEM Pack 3、GEM Pack 4、GEM Pack 6、Gem Pack 5、Hero Deck: Bravo、Hero Deck: Dorinthea、Hero Deck: Katsu …
- **Dragon Ball Super: Masters**：41 个未覆盖
  - 缺的主要是 `Expansion Deck Box Set XX`、`Collector's Selection Vol.X` 这类非补充包产品，Holodex 不单独收录；官方站 `dbs-cardgame.com` 的产品页只展示当期产品，没有全量归档。
  - 明细：5th Anniversary Set、Collector's Selection Vol. 1、Collector's Selection Vol. 2、Collector's Selection Vol. 3、Expansion Deck Box Set 01: Mighty Heroes、Expansion Deck Box Set 02: Dark Demon's Villains、Expansion Deck Box Set 03: Ultimate Box、Expansion Deck Box Set 04: Unity of Saiyans、Expansion Deck Box Set 05: Unity of Destruction、Expansion Deck Box Set 07: Magnificent Collection - Fusion Hero、Expansion Deck Box Set 08: Magnificent Collection - Forsaken Warrior、Expansion Deck Box Set 09: Saiyan Surge …

