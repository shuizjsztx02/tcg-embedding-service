# 系列 → Logo 映射表（seriesToLogo.md）

> 生成时间：2026-10-10　生成脚本：`script_temp/build_series_logo.py`
> logo 来源：`crawl/crawl/holodex_sets_organized.json`（Holodex CDN，12 个 game）
> 卡牌数量口径：`category_cards_final/category_cards/<品类>/products.jsonl` 中该系列的单卡条数

## 一、总览

| 指标 | 值 |
|------|-----|
| 品类数 | 47 |
| 系列总数 | 3279 |
| 已关联 logo 的系列 | 730（22.3%） |
| 卡牌总数 | 364136 |
| 其中有 logo 的系列覆盖卡牌 | 122331（33.6%） |

**匹配方式图例**：`exact` 归一化全等；`prefix` 去掉系列代号前缀后全等；`token` 词元集合相同；`inherit` 衍生子线（预发售/发售活动/促销卡）继承母系列 logo；`override` 人工核对。表格中 logo 带 `※` 的即为 `inherit`。

### 各品类覆盖

| 品类 | 系列数 | 有 logo | 直接匹配 | 继承 | logo 覆盖率 | 卡牌数 | 卡牌覆盖 |
|------|--------|---------|----------|------|-------------|--------|----------|
| 01_Magic | 405 | 197 | 197 | 0 | 48.6% | 97047 | 57.9% |
| 02_YuGiOh | 605 | 148 | 148 | 0 | 24.5% | 43524 | 39.4% |
| 03_Pokemon | 197 | 177 | 177 | 0 | 89.8% | 26635 | 86.4% |
| 08_Heroclix | 184 | 0 | 0 | 0 | 0.0% | 7995 | 0.0% |
| 13_WoW | 41 | 0 | 0 | 0 | 0.0% | 4587 | 0.0% |
| 16_Cardfight_Vanguard | 260 | 0 | 0 | 0 | 0.0% | 24168 | 0.0% |
| 17_Force_of_Will | 99 | 0 | 0 | 0 | 0.0% | 13171 | 0.0% |
| 18_Dice_Masters | 27 | 0 | 0 | 0 | 0.0% | 2638 | 0.0% |
| 19_Future_Card_BuddyFight | 92 | 0 | 0 | 0 | 0.0% | 7241 | 0.0% |
| 20_Weiss_Schwarz | 163 | 0 | 0 | 0 | 0.0% | 27902 | 0.0% |
| 23_Dragon_Ball_Z_TCG | 9 | 0 | 0 | 0 | 0.0% | 1754 | 0.0% |
| 28_Dragoborne | 11 | 0 | 0 | 0 | 0.0% | 670 | 0.0% |
| 30_MetaX_TCG | 5 | 0 | 0 | 0 | 0.0% | 752 | 0.0% |
| 36_Zombie_World_Order_TCG | 2 | 0 | 0 | 0 | 0.0% | 69 | 0.0% |
| 37_The_Caster_Chronicles | 12 | 0 | 0 | 0 | 0.0% | 835 | 0.0% |
| 47_Exodus_TCG | 8 | 0 | 0 | 0 | 0.0% | 685 | 0.0% |
| 48_Lightseekers_TCG | 3 | 0 | 0 | 0 | 0.0% | 1856 | 0.0% |
| 53_Munchkin_CCG | 4 | 0 | 0 | 0 | 0.0% | 588 | 0.0% |
| 54_Warhammer_Age_of_Sigmar_Champions_TCG | 5 | 0 | 0 | 0 | 0.0% | 1158 | 0.0% |
| 57_Transformers_TCG | 8 | 0 | 0 | 0 | 0.0% | 713 | 0.0% |
| 58_Bakugan_TCG | 4 | 0 | 0 | 0 | 0.0% | 1112 | 0.0% |
| 60_Chrono_Clash_System | 2 | 0 | 0 | 0 | 0.0% | 98 | 0.0% |
| 61_Argent_Saga_TCG | 10 | 0 | 0 | 0 | 0.0% | 971 | 0.0% |
| 62_Flesh_and_Blood_TCG | 99 | 0 | 0 | 0 | 0.0% | 5990 | 0.0% |
| 63_Digimon_Card_Game | 88 | 48 | 29 | 19 | 54.5% | 6100 | 75.8% |
| 65_Gate_Ruler | 11 | 0 | 0 | 0 | 0.0% | 1158 | 0.0% |
| 66_MetaZoo | 39 | 0 | 0 | 0 | 0.0% | 2763 | 0.0% |
| 67_WIXOSS | 29 | 0 | 0 | 0 | 0.0% | 4199 | 0.0% |
| 68_One_Piece_Card_Game | 83 | 34 | 21 | 13 | 41.0% | 5008 | 77.7% |
| 71_Disney_Lorcana | 18 | 14 | 14 | 0 | 77.8% | 2739 | 96.6% |
| 72_Battle_Spirits_Saga | 18 | 0 | 0 | 0 | 0.0% | 1205 | 0.0% |
| 73_Shadowverse_Evolve | 46 | 0 | 0 | 0 | 0.0% | 5740 | 0.0% |
| 74_Grand_Archive_TCG | 42 | 0 | 0 | 0 | 0.0% | 3676 | 0.0% |
| 75_Akora_TCG | 8 | 0 | 0 | 0 | 0.0% | 2219 | 0.0% |
| 76_Kryptik_TCG | 5 | 0 | 0 | 0 | 0.0% | 2929 | 0.0% |
| 77_Sorcery_Contested_Realm | 7 | 0 | 0 | 0 | 0.0% | 2780 | 0.0% |
| 78_Alpha_Clash | 17 | 0 | 0 | 0 | 0.0% | 2061 | 0.0% |
| 79_Star_Wars_Unlimited | 29 | 16 | 8 | 8 | 55.2% | 6069 | 89.3% |
| 80_Dragon_Ball_Super_Fusion_World | 48 | 31 | 29 | 2 | 64.6% | 3696 | 86.9% |
| 81_Union_Arena | 63 | 47 | 21 | 26 | 74.6% | 4393 | 90.7% |
| 83_Elestrals | 52 | 0 | 0 | 0 | 0.0% | 2580 | 0.0% |
| 85_Pokemon_Japan | 358 | 0 | 0 | 0 | 0.0% | 26016 | 0.0% |
| 86_Gundam_Card_Game | 22 | 18 | 18 | 0 | 81.8% | 1470 | 89.5% |
| 87_hololive_OFFICIAL_CARD_GAME | 17 | 0 | 0 | 0 | 0.0% | 1462 | 0.0% |
| 88_Godzilla_Card_Game | 6 | 0 | 0 | 0 | 0.0% | 523 | 0.0% |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | 9 | 5 | 4 | 1 | 55.6% | 1126 | 79.0% |
| 90_CookieRun_Braverse_TCG | 9 | 0 | 0 | 0 | 0.0% | 2065 | 0.0% |

## 二、映射表

### 01_Magic（405 个系列，195 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 01_Magic | 10th Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1/logo.webp | 388 |
| 01_Magic | 30th Anniversary Edition |  | 579 |
| 01_Magic | 30th Anniversary Promos |  | 43 |
| 01_Magic | 7th Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2/logo.webp | 347 |
| 01_Magic | 8th Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3/logo.webp | 357 |
| 01_Magic | 9th Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_4/logo.webp | 356 |
| 01_Magic | AFR Ampersand Promos |  | 80 |
| 01_Magic | APAC Lands |  | 15 |
| 01_Magic | Adventures in the Forgotten Realms | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2823/logo.webp | 460 |
| 01_Magic | Aether Revolt | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1857/logo.webp | 199 |
| 01_Magic | Aetherdrift | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23874/logo.webp | 404 |
| 01_Magic | Alara Reborn | https://holodex-prod-bucket.b-cdn.net/sets/mtg_5/logo.webp | 149 |
| 01_Magic | Alliances | https://holodex-prod-bucket.b-cdn.net/sets/mtg_6/logo.webp | 150 |
| 01_Magic | Alpha Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_7/logo.webp | 293 |
| 01_Magic | Amonkhet | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1882/logo.webp | 329 |
| 01_Magic | Anthologies | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1275/logo.webp | 35 |
| 01_Magic | Antiquities | https://holodex-prod-bucket.b-cdn.net/sets/mtg_8/logo.webp | 100 |
| 01_Magic | Apocalypse | https://holodex-prod-bucket.b-cdn.net/sets/mtg_10/logo.webp | 143 |
| 01_Magic | Arabian Nights | https://holodex-prod-bucket.b-cdn.net/sets/mtg_11/logo.webp | 89 |
| 01_Magic | Archenemy | https://holodex-prod-bucket.b-cdn.net/sets/mtg_12/logo.webp | 56 |
| 01_Magic | Archenemy: Duskmourn |  | 40 |
| 01_Magic | Archenemy: Nicol Bolas |  | 110 |
| 01_Magic | Arena Promos |  | 86 |
| 01_Magic | Art Series: Adventures in the Forgotten Realms |  | 162 |
| 01_Magic | Art Series: Aetherdrift |  | 108 |
| 01_Magic | Art Series: Avatar: The Last Airbender | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24527/logo.webp | 120 |
| 01_Magic | Art Series: Bloomburrow |  | 108 |
| 01_Magic | Art Series: Commander Legends: Battle for Baldur's Gate |  | 156 |
| 01_Magic | Art Series: Commander Masters |  | 159 |
| 01_Magic | Art Series: Dominaria United |  | 160 |
| 01_Magic | Art Series: Duskmourn: House of Horror | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23749/logo.webp | 107 |
| 01_Magic | Art Series: Edge of Eternities |  | 108 |
| 01_Magic | Art Series: FINAL FANTASY |  | 130 |
| 01_Magic | Art Series: Foundations |  | 109 |
| 01_Magic | Art Series: Innistrad Remastered |  | 40 |
| 01_Magic | Art Series: Innistrad: Crimson Vow |  | 159 |
| 01_Magic | Art Series: Innistrad: Midnight Hunt |  | 162 |
| 01_Magic | Art Series: Kaldheim |  | 160 |
| 01_Magic | Art Series: Kamigawa: Neon Dynasty |  | 160 |
| 01_Magic | Art Series: Lorwyn Eclipsed |  | 107 |
| 01_Magic | Art Series: March of the Machine |  | 160 |
| 01_Magic | Art Series: Marvel Super Heroes |  | 110 |
| 01_Magic | Art Series: Modern Horizons |  | 54 |
| 01_Magic | Art Series: Modern Horizons 2 |  | 162 |
| 01_Magic | Art Series: Modern Horizons 3 |  | 108 |
| 01_Magic | Art Series: Murders at Karlov Manor |  | 98 |
| 01_Magic | Art Series: Outlaws of Thunder Junction |  | 107 |
| 01_Magic | Art Series: Phyrexia: All Will Be One |  | 162 |
| 01_Magic | Art Series: Secrets of Strixhaven |  | 108 |
| 01_Magic | Art Series: Streets of New Capenna |  | 162 |
| 01_Magic | Art Series: Strixhaven |  | 159 |
| 01_Magic | Art Series: Tarkir: Dragonstorm |  | 58 |
| 01_Magic | Art Series: Teenage Mutant Ninja Turtles | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24626/logo.webp | 108 |
| 01_Magic | Art Series: The Hobbit |  | 120 |
| 01_Magic | Art Series: The Lost Caverns of Ixalan |  | 162 |
| 01_Magic | Art Series: Universes Beyond: The Lord of the Rings: Tales of Middle-earth |  | 136 |
| 01_Magic | Art Series: Wilds of Eldraine |  | 158 |
| 01_Magic | Art Series: Zendikar Rising |  | 153 |
| 01_Magic | Avacyn Restored | https://holodex-prod-bucket.b-cdn.net/sets/mtg_362/logo.webp | 252 |
| 01_Magic | Avatar: The Last Airbender | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24421/logo.webp | 324 |
| 01_Magic | Avatar: The Last Airbender: Eternal-Legal | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24422/logo.webp | 318 |
| 01_Magic | Battle Royale Box Set |  | 133 |
| 01_Magic | Battle for Zendikar | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1645/logo.webp | 313 |
| 01_Magic | Battlebond |  | 264 |
| 01_Magic | Beatdown Box Set | https://holodex-prod-bucket.b-cdn.net/sets/mtg_16/logo.webp | 90 |
| 01_Magic | Beta Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_17/logo.webp | 300 |
| 01_Magic | Betrayers of Kamigawa | https://holodex-prod-bucket.b-cdn.net/sets/mtg_18/logo.webp | 165 |
| 01_Magic | Bloomburrow | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23447/logo.webp | 249 |
| 01_Magic | Born of the Gods | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1276/logo.webp | 175 |
| 01_Magic | Buy-A-Box Promos |  | 92 |
| 01_Magic | Champions of Kamigawa | https://holodex-prod-bucket.b-cdn.net/sets/mtg_20/logo.webp | 256 |
| 01_Magic | Champs Promos |  | 12 |
| 01_Magic | Chronicles | https://holodex-prod-bucket.b-cdn.net/sets/mtg_22/logo.webp | 125 |
| 01_Magic | Classic Sixth Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23/logo.webp | 348 |
| 01_Magic | Coldsnap | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24/logo.webp | 147 |
| 01_Magic | Coldsnap Theme Deck Reprints |  | 62 |
| 01_Magic | Commander 2013 |  | 356 |
| 01_Magic | Commander 2014 |  | 361 |
| 01_Magic | Commander 2015 |  | 368 |
| 01_Magic | Commander 2016 |  | 369 |
| 01_Magic | Commander 2017 |  | 321 |
| 01_Magic | Commander 2018 |  | 331 |
| 01_Magic | Commander 2019 |  | 323 |
| 01_Magic | Commander 2020 |  | 341 |
| 01_Magic | Commander 2021 |  | 435 |
| 01_Magic | Commander Anthology |  | 340 |
| 01_Magic | Commander Anthology Volume II |  | 331 |
| 01_Magic | Commander Collection: Black |  | 9 |
| 01_Magic | Commander Collection: Green |  | 8 |
| 01_Magic | Commander Legends |  | 752 |
| 01_Magic | Commander Legends: Battle for Baldur's Gate | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3047/logo.webp | 972 |
| 01_Magic | Commander Masters | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23020/logo.webp | 1195 |
| 01_Magic | Commander: Adventures in the Forgotten Realms | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2870/logo.webp | 349 |
| 01_Magic | Commander: Aetherdrift |  | 206 |
| 01_Magic | Commander: Bloomburrow |  | 386 |
| 01_Magic | Commander: Dominaria United | https://www.cardkingdom.com/media/upload/about/DMU.png | 264 |
| 01_Magic | Commander: Duskmourn: House of Horror | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23551/logo.webp | 355 |
| 01_Magic | Commander: Edge of Eternities |  | 213 |
| 01_Magic | Commander: FINAL FANTASY |  | 767 |
| 01_Magic | Commander: Foundations |  | 3 |
| 01_Magic | Commander: Innistrad: Crimson Vow | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2900/logo.webp | 194 |
| 01_Magic | Commander: Innistrad: Midnight Hunt | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2893/logo.webp | 199 |
| 01_Magic | Commander: Kaldheim |  | 128 |
| 01_Magic | Commander: Kamigawa: Neon Dynasty | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2967/logo.webp | 192 |
| 01_Magic | Commander: Lorwyn Eclipsed | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24464/logo.webp | 195 |
| 01_Magic | Commander: March of the Machine | https://holodex-prod-bucket.b-cdn.net/sets/mtg_22979/logo.webp | 428 |
| 01_Magic | Commander: Marvel Super Heroes | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24554/logo.webp | 1117 |
| 01_Magic | Commander: Modern Horizons 3 |  | 715 |
| 01_Magic | Commander: Murders at Karlov Manor |  | 384 |
| 01_Magic | Commander: Outlaws of Thunder Junction |  | 379 |
| 01_Magic | Commander: Phyrexia: All Will Be One |  | 189 |
| 01_Magic | Commander: Reality Fracture |  | 2 |
| 01_Magic | Commander: Secrets of Strixhaven |  | 454 |
| 01_Magic | Commander: Star Trek |  | 10 |
| 01_Magic | Commander: Streets of New Capenna | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3031/logo.webp | 483 |
| 01_Magic | Commander: Tarkir: Dragonstorm |  | 444 |
| 01_Magic | Commander: Teenage Mutant Ninja Turtles | https://i.ibb.co/NMRW4NR/Teenage-Mutant-Ninja-Turtles.png | 200 |
| 01_Magic | Commander: The Lord of the Rings: Tales of Middle-earth |  | 509 |
| 01_Magic | Commander: The Lost Caverns of Ixalan |  | 363 |
| 01_Magic | Commander: Wilds of Eldraine |  | 185 |
| 01_Magic | Commander: Zendikar Rising | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2716/logo.webp | 149 |
| 01_Magic | Conflux | https://holodex-prod-bucket.b-cdn.net/sets/mtg_26/logo.webp | 147 |
| 01_Magic | Conspiracy | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1312/logo.webp | 72 |
| 01_Magic | Conspiracy: Take the Crown |  | 234 |
| 01_Magic | Core Set 2019 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2250/logo.webp | 337 |
| 01_Magic | Core Set 2020 | https://www.cardkingdom.com/media/upload/about/m20.png | 354 |
| 01_Magic | Core Set 2021 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2653/logo.webp | 459 |
| 01_Magic | Dark Ascension | https://holodex-prod-bucket.b-cdn.net/sets/mtg_125/logo.webp | 161 |
| 01_Magic | Darksteel | https://holodex-prod-bucket.b-cdn.net/sets/mtg_27/logo.webp | 65 |
| 01_Magic | Deckmasters Garfield vs Finkel |  | 55 |
| 01_Magic | Dissension | https://holodex-prod-bucket.b-cdn.net/sets/mtg_28/logo.webp | 180 |
| 01_Magic | Dominaria | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2199/logo.webp | 279 |
| 01_Magic | Dominaria Remastered | https://holodex-prod-bucket.b-cdn.net/sets/mtg_17670/logo.webp | 510 |
| 01_Magic | Dominaria United | https://www.cardkingdom.com/media/upload/about/DMU.png | 329 |
| 01_Magic | Double Masters | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2655/logo.webp | 495 |
| 01_Magic | Double Masters 2022 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3070/logo.webp | 659 |
| 01_Magic | Dragons of Tarkir | https://upload.wikimedia.org/wikipedia/it/2/2f/MtG_Dragons_of_Tarkir_Logo.png | 272 |
| 01_Magic | Duel Decks: Anthology |  | 209 |
| 01_Magic | Duel Decks: Blessed vs. Cursed |  | 72 |
| 01_Magic | Duel Decks: Elves vs. Inventors |  | 69 |
| 01_Magic | Duel Decks: Heroes vs. Monsters |  | 16 |
| 01_Magic | Duel Decks: Jace vs. Chandra |  | 2 |
| 01_Magic | Duel Decks: Merfolk vs. Goblins |  | 66 |
| 01_Magic | Duel Decks: Mind vs. Might |  | 65 |
| 01_Magic | Duel Decks: Nissa vs. Ob Nixilis |  | 76 |
| 01_Magic | Duel Decks: Zendikar vs. Eldrazi |  | 80 |
| 01_Magic | Duels of the Planeswalkers | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1274/logo.webp | 113 |
| 01_Magic | Duskmourn: House of Horror | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23550/logo.webp | 259 |
| 01_Magic | Edge of Eternities | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24233/logo.webp | 212 |
| 01_Magic | Edge of Eternities: Stellar Sights |  | 180 |
| 01_Magic | Eldritch Moon | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1790/logo.webp | 216 |
| 01_Magic | Eternal Masters | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1740/logo.webp | 265 |
| 01_Magic | European Lands |  | 15 |
| 01_Magic | Eventide | https://holodex-prod-bucket.b-cdn.net/sets/mtg_39/logo.webp | 187 |
| 01_Magic | Exodus | https://holodex-prod-bucket.b-cdn.net/sets/mtg_40/logo.webp | 142 |
| 01_Magic | Explorers of Ixalan |  | 49 |
| 01_Magic | FINAL FANTASY | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24219/logo.webp | 309 |
| 01_Magic | FINAL FANTASY: Through the Ages |  | 65 |
| 01_Magic | FNM Promos |  | 233 |
| 01_Magic | Fallen Empires | https://holodex-prod-bucket.b-cdn.net/sets/mtg_41/logo.webp | 137 |
| 01_Magic | Fate Reforged | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1497/logo.webp | 189 |
| 01_Magic | Fifth Dawn | https://holodex-prod-bucket.b-cdn.net/sets/mtg_43/logo.webp | 165 |
| 01_Magic | Fifth Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_44/logo.webp | 447 |
| 01_Magic | Foundations | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23556/logo.webp | 506 |
| 01_Magic | Foundations Jumpstart | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23792/logo.webp | 722 |
| 01_Magic | Fourth Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_46/logo.webp | 331 |
| 01_Magic | Fourth Edition (Foreign Black Border) |  | 376 |
| 01_Magic | Fourth Edition (Foreign White Border) |  | 376 |
| 01_Magic | From the Vault: Angels | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1577/logo.webp | 15 |
| 01_Magic | From the Vault: Annihilation |  | 15 |
| 01_Magic | From the Vault: Dragons |  | 15 |
| 01_Magic | From the Vault: Exiled |  | 15 |
| 01_Magic | From the Vault: Legends |  | 15 |
| 01_Magic | From the Vault: Lore |  | 16 |
| 01_Magic | From the Vault: Realms |  | 15 |
| 01_Magic | From the Vault: Relics |  | 15 |
| 01_Magic | From the Vault: Transform |  | 15 |
| 01_Magic | From the Vault: Twenty |  | 20 |
| 01_Magic | Future Sight | https://holodex-prod-bucket.b-cdn.net/sets/mtg_51/logo.webp | 180 |
| 01_Magic | Game Day & Store Championship Promos |  | 38 |
| 01_Magic | Gatecrash | https://holodex-prod-bucket.b-cdn.net/sets/mtg_569/logo.webp | 257 |
| 01_Magic | Gift Boxes and Promos |  | 16 |
| 01_Magic | Global Series Jiang Yanggu & Mu Yanling |  | 37 |
| 01_Magic | Grand Prix Promos |  | 20 |
| 01_Magic | Guildpact | https://holodex-prod-bucket.b-cdn.net/sets/mtg_55/logo.webp | 165 |
| 01_Magic | Guilds of Ravnica | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2290/logo.webp | 270 |
| 01_Magic | Guilds of Ravnica: Guild Kits | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2334/logo.webp | 137 |
| 01_Magic | Guru Lands |  | 5 |
| 01_Magic | Hero's Path Promos |  | 42 |
| 01_Magic | Homelands | https://holodex-prod-bucket.b-cdn.net/sets/mtg_57/logo.webp | 139 |
| 01_Magic | Hour of Devastation | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1934/logo.webp | 246 |
| 01_Magic | Ice Age | https://holodex-prod-bucket.b-cdn.net/sets/mtg_58/logo.webp | 382 |
| 01_Magic | Iconic Masters | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2050/logo.webp | 253 |
| 01_Magic | Ikoria: Lair of Behemoths | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2603/logo.webp | 417 |
| 01_Magic | Innistrad | https://holodex-prod-bucket.b-cdn.net/sets/mtg_59/logo.webp | 31 |
| 01_Magic | Innistrad Remastered | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23848/logo.webp | 509 |
| 01_Magic | Innistrad: Crimson Vow | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2862/logo.webp | 484 |
| 01_Magic | Innistrad: Double Feature | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2942/logo.webp | 534 |
| 01_Magic | Innistrad: Midnight Hunt | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2864/logo.webp | 463 |
| 01_Magic | International Edition |  | 248 |
| 01_Magic | Introductory Two-Player Set |  | 67 |
| 01_Magic | Invasion | https://holodex-prod-bucket.b-cdn.net/sets/mtg_60/logo.webp | 350 |
| 01_Magic | Ixalan | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2043/logo.webp | 281 |
| 01_Magic | JingHe Age Token Cards |  | 12 |
| 01_Magic | Journey Into Nyx |  | 121 |
| 01_Magic | Judge Promos |  | 155 |
| 01_Magic | Judgment | https://holodex-prod-bucket.b-cdn.net/sets/mtg_63/logo.webp | 143 |
| 01_Magic | Jumpstart | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2654/logo.webp | 518 |
| 01_Magic | Jumpstart 2022 |  | 814 |
| 01_Magic | Junior Series Promos |  | 42 |
| 01_Magic | Kaladesh | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1791/logo.webp | 288 |
| 01_Magic | Kaldheim | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2750/logo.webp | 489 |
| 01_Magic | Kamigawa: Neon Dynasty | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2965/logo.webp | 561 |
| 01_Magic | Khans of Tarkir | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1356/logo.webp | 282 |
| 01_Magic | Launch Party & Release Event Promos |  | 66 |
| 01_Magic | League Promos |  | 19 |
| 01_Magic | Legends | https://holodex-prod-bucket.b-cdn.net/sets/mtg_65/logo.webp | 5 |
| 01_Magic | Legions | https://holodex-prod-bucket.b-cdn.net/sets/mtg_66/logo.webp | 145 |
| 01_Magic | Lorwyn | https://holodex-prod-bucket.b-cdn.net/sets/mtg_67/logo.webp | 19 |
| 01_Magic | Lorwyn Eclipsed | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24463/logo.webp | 298 |
| 01_Magic | Magic Encyclopedia 2005 (Salvat/Hachette) |  | 1488 |
| 01_Magic | Magic Encyclopedia 2011 (Salvat) |  | 222 |
| 01_Magic | Magic Game Night | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2359/logo.webp | 68 |
| 01_Magic | Magic Game Night 2019 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2562/logo.webp | 70 |
| 01_Magic | Magic Game Night: Free-For-All |  | 142 |
| 01_Magic | Magic Modern Event Deck |  | 29 |
| 01_Magic | Magic Origins | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1512/logo.webp | 290 |
| 01_Magic | Magic Player Rewards |  | 27 |
| 01_Magic | Magic Premiere Shop |  | 1 |
| 01_Magic | MagicFest Cards |  | 41 |
| 01_Magic | March of the Machine | https://holodex-prod-bucket.b-cdn.net/sets/mtg_22875/logo.webp | 229 |
| 01_Magic | March of the Machine: Multiverse Legends |  | 262 |
| 01_Magic | March of the Machine: The Aftermath |  | 178 |
| 01_Magic | Marvel Super Heroes | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24553/logo.webp | 227 |
| 01_Magic | Marvel Universe Eternal-Legal | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24432/logo.webp | 100 |
| 01_Magic | Masterpiece Series: Amonkhet Invocations |  | 54 |
| 01_Magic | Masterpiece Series: Kaladesh Inventions |  | 54 |
| 01_Magic | Masters 25 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2189/logo.webp | 265 |
| 01_Magic | Media Promos |  | 222 |
| 01_Magic | Mercadian Masques | https://holodex-prod-bucket.b-cdn.net/sets/mtg_73/logo.webp | 350 |
| 01_Magic | Mirage | https://holodex-prod-bucket.b-cdn.net/sets/mtg_74/logo.webp | 350 |
| 01_Magic | Mirrodin | https://holodex-prod-bucket.b-cdn.net/sets/mtg_75/logo.webp | 142 |
| 01_Magic | Mirrodin Besieged | https://holodex-prod-bucket.b-cdn.net/sets/mtg_76/logo.webp | 161 |
| 01_Magic | Modern Horizons | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2422/logo.webp | 432 |
| 01_Magic | Modern Horizons 2 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2822/logo.webp | 693 |
| 01_Magic | Modern Horizons 3 |  | 424 |
| 01_Magic | Modern Masters |  | 67 |
| 01_Magic | Modern Masters 2015 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1503/logo.webp | 265 |
| 01_Magic | Modern Masters 2017 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1879/logo.webp | 270 |
| 01_Magic | Morningtide | https://holodex-prod-bucket.b-cdn.net/sets/mtg_77/logo.webp | 153 |
| 01_Magic | Murders at Karlov Manor | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23361/logo.webp | 256 |
| 01_Magic | Mystery Booster 2 |  | 236 |
| 01_Magic | Mystery Booster 2 Playtest Cards |  | 122 |
| 01_Magic | Mystery Booster Commander Edition |  | 80 |
| 01_Magic | Mystery Booster: Convention Edition Exclusives |  | 239 |
| 01_Magic | Mythic Edition: Guilds of Ravnica | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2326/logo.webp | 16 |
| 01_Magic | Mythic Edition: Ravnica Allegiance |  | 13 |
| 01_Magic | Mythic Edition: War of the Spark | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2444/logo.webp | 11 |
| 01_Magic | Nemesis | https://holodex-prod-bucket.b-cdn.net/sets/mtg_78/logo.webp | 143 |
| 01_Magic | New Phyrexia | https://holodex-prod-bucket.b-cdn.net/sets/mtg_79/logo.webp | 179 |
| 01_Magic | Oath of the Gatewatch | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1693/logo.webp | 197 |
| 01_Magic | Odyssey | https://holodex-prod-bucket.b-cdn.net/sets/mtg_80/logo.webp | 299 |
| 01_Magic | Onslaught | https://holodex-prod-bucket.b-cdn.net/sets/mtg_81/logo.webp | 349 |
| 01_Magic | Open House Promos |  | 11 |
| 01_Magic | Outlaws of Thunder Junction | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23439/logo.webp | 252 |
| 01_Magic | Outlaws of Thunder Junction: Breaking News |  | 90 |
| 01_Magic | Outlaws of Thunder Junction: The Big Score |  | 108 |
| 01_Magic | Oversize Cards |  | 497 |
| 01_Magic | Phyrexia: All Will Be One | https://holodex-prod-bucket.b-cdn.net/sets/mtg_17684/logo.webp | 396 |
| 01_Magic | Planar Chaos | https://holodex-prod-bucket.b-cdn.net/sets/mtg_83/logo.webp | 165 |
| 01_Magic | Planechase |  | 51 |
| 01_Magic | Planechase 2012 |  | 156 |
| 01_Magic | Planechase Anthology |  | 170 |
| 01_Magic | Planechase: March of the Machine |  | 50 |
| 01_Magic | Planechase: Universes Beyond: Doctor Who |  | 40 |
| 01_Magic | Planeshift | https://holodex-prod-bucket.b-cdn.net/sets/mtg_85/logo.webp | 96 |
| 01_Magic | Planeswalker Event Promos |  | 44 |
| 01_Magic | Play Promos |  | 11 |
| 01_Magic | Ponies: The Galloping |  | 3 |
| 01_Magic | Portal | https://holodex-prod-bucket.b-cdn.net/sets/mtg_86/logo.webp | 145 |
| 01_Magic | Portal Second Age | https://holodex-prod-bucket.b-cdn.net/sets/mtg_87/logo.webp | 165 |
| 01_Magic | Portal Three Kingdoms | https://holodex-prod-bucket.b-cdn.net/sets/mtg_88/logo.webp | 180 |
| 01_Magic | Premium Deck Series: Fire and Lightning |  | 34 |
| 01_Magic | Premium Deck Series: Graveborn |  | 30 |
| 01_Magic | Premium Deck Series: Slivers |  | 41 |
| 01_Magic | Prerelease Cards |  | 3691 |
| 01_Magic | Pro Tour Promos |  | 26 |
| 01_Magic | Promo Pack: Adventures in the Forgotten Realms | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2868/logo.webp | 88 |
| 01_Magic | Promo Pack: Aetherdrift |  | 97 |
| 01_Magic | Promo Pack: Bloomburrow |  | 85 |
| 01_Magic | Promo Pack: Core Set 2020 |  | 197 |
| 01_Magic | Promo Pack: Core Set 2021 |  | 91 |
| 01_Magic | Promo Pack: Dominaria United |  | 97 |
| 01_Magic | Promo Pack: Duskmourn: House of Horror | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23735/logo.webp | 89 |
| 01_Magic | Promo Pack: Edge of Eternities |  | 99 |
| 01_Magic | Promo Pack: Ikoria |  | 89 |
| 01_Magic | Promo Pack: Innistrad: Midnight Hunt |  | 75 |
| 01_Magic | Promo Pack: Kaldheim |  | 83 |
| 01_Magic | Promo Pack: Kamigawa: Neon Dynasty |  | 81 |
| 01_Magic | Promo Pack: Lorwyn Eclipsed | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24465/logo.webp | 101 |
| 01_Magic | Promo Pack: March of the Machine |  | 60 |
| 01_Magic | Promo Pack: Murders at Karlov Manor |  | 111 |
| 01_Magic | Promo Pack: Outlaws of Thunder Junction |  | 45 |
| 01_Magic | Promo Pack: Phyrexia: All Will Be One |  | 86 |
| 01_Magic | Promo Pack: Secrets of Strixhaven |  | 97 |
| 01_Magic | Promo Pack: Streets of New Capenna | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3033/logo.webp | 160 |
| 01_Magic | Promo Pack: Strixhaven |  | 76 |
| 01_Magic | Promo Pack: Tarkir: Dragonstorm |  | 86 |
| 01_Magic | Promo Pack: The Lost Caverns of Ixalan |  | 35 |
| 01_Magic | Promo Pack: Theros Beyond Death | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2599/logo.webp | 111 |
| 01_Magic | Promo Pack: Throne of Eldraine |  | 138 |
| 01_Magic | Promo Pack: Wilds of Eldraine |  | 88 |
| 01_Magic | Promo Pack: Zendikar Rising |  | 82 |
| 01_Magic | Prophecy | https://holodex-prod-bucket.b-cdn.net/sets/mtg_94/logo.webp | 143 |
| 01_Magic | Ravnica Allegiance | https://www.cardkingdom.com/media/upload/about/rna.png | 285 |
| 01_Magic | Ravnica Allegiance: Guild Kits |  | 141 |
| 01_Magic | Ravnica Remastered | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23319/logo.webp | 624 |
| 01_Magic | Ravnica: City of Guilds | https://holodex-prod-bucket.b-cdn.net/sets/mtg_95/logo.webp | 256 |
| 01_Magic | Ravnica: Clue Edition |  | 294 |
| 01_Magic | Reality Fracture |  | 42 |
| 01_Magic | Renaissance | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2379/logo.webp | 311 |
| 01_Magic | Return to Ravnica | https://holodex-prod-bucket.b-cdn.net/sets/mtg_370/logo.webp | 285 |
| 01_Magic | Revised Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_97/logo.webp | 304 |
| 01_Magic | Revised Edition (Foreign Black Border) | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1689/logo.webp | 305 |
| 01_Magic | Revised Edition (Foreign White Border) | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1690/logo.webp | 305 |
| 01_Magic | Rise of the Eldrazi | https://holodex-prod-bucket.b-cdn.net/sets/mtg_98/logo.webp | 204 |
| 01_Magic | Rivals of Ixalan | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2098/logo.webp | 212 |
| 01_Magic | SLX Cards |  | 30 |
| 01_Magic | Saviors of Kamigawa | https://holodex-prod-bucket.b-cdn.net/sets/mtg_99/logo.webp | 115 |
| 01_Magic | Scars of Mirrodin | https://holodex-prod-bucket.b-cdn.net/sets/mtg_100/logo.webp | 259 |
| 01_Magic | Scourge | https://holodex-prod-bucket.b-cdn.net/sets/mtg_101/logo.webp | 143 |
| 01_Magic | Secret Lair Countdown Kit | https://holodex-prod-bucket.b-cdn.net/sets/mtg_17667/logo.webp | 111 |
| 01_Magic | Secret Lair Drop Series | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2576/logo.webp | 3119 |
| 01_Magic | Secret Lair Series | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2632/logo.webp | 16 |
| 01_Magic | Secret Lair Showdown |  | 52 |
| 01_Magic | Secrets of Strixhaven |  | 150 |
| 01_Magic | Secrets of Strixhaven: Mystical Archive |  | 195 |
| 01_Magic | Shadowmoor | https://holodex-prod-bucket.b-cdn.net/sets/mtg_102/logo.webp | 313 |
| 01_Magic | Shadows over Innistrad | https://holodex-prod-bucket.b-cdn.net/sets/mtg_1708/logo.webp | 332 |
| 01_Magic | Shards of Alara | https://holodex-prod-bucket.b-cdn.net/sets/mtg_103/logo.webp | 209 |
| 01_Magic | Signature Spellbook: Chandra | https://www.cardkingdom.com/media/upload/about/ss3.png | 8 |
| 01_Magic | Signature Spellbook: Gideon |  | 8 |
| 01_Magic | Signature Spellbook: Jace |  | 8 |
| 01_Magic | Special Guests |  | 164 |
| 01_Magic | Special Occasion |  | 30 |
| 01_Magic | Standard Showdown Promos |  | 51 |
| 01_Magic | Star Trek |  | 56 |
| 01_Magic | Star Trek: Stardates |  | 1 |
| 01_Magic | Starter 1999 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_105/logo.webp | 173 |
| 01_Magic | Starter 2000 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_106/logo.webp | 20 |
| 01_Magic | Starter Commander Decks |  | 382 |
| 01_Magic | Streets of New Capenna | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3026/logo.webp | 530 |
| 01_Magic | Strixhaven: Mystical Archive |  | 250 |
| 01_Magic | Strixhaven: School of Mages | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2773/logo.webp | 419 |
| 01_Magic | Stronghold | https://holodex-prod-bucket.b-cdn.net/sets/mtg_107/logo.webp | 143 |
| 01_Magic | Summer Magic |  | 305 |
| 01_Magic | Tarkir Dragonfury Promos |  | 4 |
| 01_Magic | Tarkir: Dragonstorm | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24232/logo.webp | 171 |
| 01_Magic | Teenage Mutant Ninja Turtles | https://i.ibb.co/NMRW4NR/Teenage-Mutant-Ninja-Turtles.png | 240 |
| 01_Magic | Teenage Mutant Ninja Turtles Source Material |  | 20 |
| 01_Magic | Tempest | https://holodex-prod-bucket.b-cdn.net/sets/mtg_108/logo.webp | 350 |
| 01_Magic | The Dark | https://holodex-prod-bucket.b-cdn.net/sets/mtg_109/logo.webp | 119 |
| 01_Magic | The Hobbit | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24683/logo.webp | 286 |
| 01_Magic | The Hobbit: Eternal-Legal | https://holodex-prod-bucket.b-cdn.net/sets/mtg_24691/logo.webp | 158 |
| 01_Magic | The List Reprints |  | 5025 |
| 01_Magic | The Lost Caverns of Ixalan | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23316/logo.webp | 223 |
| 01_Magic | Theros |  | 94 |
| 01_Magic | Theros Beyond Death | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2568/logo.webp | 387 |
| 01_Magic | Throne of Eldraine | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2494/logo.webp | 459 |
| 01_Magic | Time Spiral | https://holodex-prod-bucket.b-cdn.net/sets/mtg_110/logo.webp | 122 |
| 01_Magic | Time Spiral: Remastered | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2772/logo.webp | 425 |
| 01_Magic | Timeshifted |  | 71 |
| 01_Magic | Torment | https://holodex-prod-bucket.b-cdn.net/sets/mtg_112/logo.webp | 143 |
| 01_Magic | Ultimate Masters | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2360/logo.webp | 270 |
| 01_Magic | Ultimate Masters: Box Toppers |  | 40 |
| 01_Magic | Un-Known Event Playtest Cards |  | 396 |
| 01_Magic | Unfinity | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2958/logo.webp | 729 |
| 01_Magic | Unglued | https://www.cardkingdom.com/images/About/UngluedLogo.jpg | 94 |
| 01_Magic | Unhinged |  | 159 |
| 01_Magic | Unique and Miscellaneous Promos |  | 327 |
| 01_Magic | Universes Beyond: Doctor Who | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23165/logo.webp | 1188 |
| 01_Magic | Universes Beyond: Fallout | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23337/logo.webp | 1043 |
| 01_Magic | Universes Beyond: Jurassic World Collection | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23317/logo.webp | 56 |
| 01_Magic | Universes Beyond: The Lord of the Rings: Tales of Middle-earth | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23019/logo.webp | 772 |
| 01_Magic | Universes Beyond: Transformers |  | 31 |
| 01_Magic | Universes Beyond: Warhammer 40,000 | https://holodex-prod-bucket.b-cdn.net/sets/mtg_3079/logo.webp | 649 |
| 01_Magic | Unlimited Edition | https://holodex-prod-bucket.b-cdn.net/sets/mtg_115/logo.webp | 251 |
| 01_Magic | Unsanctioned |  | 100 |
| 01_Magic | Unstable |  | 288 |
| 01_Magic | Vanguard | https://holodex-prod-bucket.b-cdn.net/sets/mtg_119/logo.webp | 32 |
| 01_Magic | Visions | https://holodex-prod-bucket.b-cdn.net/sets/mtg_120/logo.webp | 117 |
| 01_Magic | WMCQ Promo Cards |  | 6 |
| 01_Magic | WPN & Gateway Promos |  | 20 |
| 01_Magic | War of the Spark | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2418/logo.webp | 329 |
| 01_Magic | Weatherlight | https://holodex-prod-bucket.b-cdn.net/sets/mtg_121/logo.webp | 117 |
| 01_Magic | Welcome Deck 2016 |  | 16 |
| 01_Magic | Welcome Deck 2017 |  | 30 |
| 01_Magic | Wilds of Eldraine | https://holodex-prod-bucket.b-cdn.net/sets/mtg_23163/logo.webp | 242 |
| 01_Magic | Wilds of Eldraine: Enchanting Tales |  | 103 |
| 01_Magic | World Championship Decks |  | 1330 |
| 01_Magic | Worldwake | https://holodex-prod-bucket.b-cdn.net/sets/mtg_122/logo.webp | 151 |
| 01_Magic | Zendikar | https://holodex-prod-bucket.b-cdn.net/sets/mtg_124/logo.webp | 60 |
| 01_Magic | Zendikar Expeditions |  | 45 |
| 01_Magic | Zendikar Rising | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2648/logo.webp | 443 |
| 01_Magic | Zendikar Rising Expeditions | https://holodex-prod-bucket.b-cdn.net/sets/mtg_2713/logo.webp | 30 |

### 02_YuGiOh（605 个系列，145 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 02_YuGiOh | 2-Player Starter Set |  | 88 |
| 02_YuGiOh | 2002 Collectors Tin |  | 6 |
| 02_YuGiOh | 2003 Collectors Tin |  | 6 |
| 02_YuGiOh | 2004 Collectors Tin |  | 6 |
| 02_YuGiOh | 2005 Collectors Tin |  | 6 |
| 02_YuGiOh | 2006 Collectors Tin |  | 6 |
| 02_YuGiOh | 2007 Collectors Tin |  | 6 |
| 02_YuGiOh | 2008 Collectors Tin |  | 7 |
| 02_YuGiOh | 2009 Collectors Tin |  | 8 |
| 02_YuGiOh | 2010 Collectors Tins |  | 25 |
| 02_YuGiOh | 2010 Duelist Pack Collection Tin |  | 10 |
| 02_YuGiOh | 2011 Collectors Tins |  | 18 |
| 02_YuGiOh | 2011 Duelist Pack Tin |  | 4 |
| 02_YuGiOh | 2012 Collectors Tin |  | 23 |
| 02_YuGiOh | 2012 Premium Collection Tin |  | 25 |
| 02_YuGiOh | 2013 Collectors Tins |  | 18 |
| 02_YuGiOh | 2013 Zexal Collection Tin |  | 24 |
| 02_YuGiOh | 2014 Mega-Tins |  | 6 |
| 02_YuGiOh | 2014 Mega-Tins Mega Pack |  | 197 |
| 02_YuGiOh | 2015 Mega-Tins |  | 6 |
| 02_YuGiOh | 2015 Mega-Tins Mega Pack |  | 247 |
| 02_YuGiOh | 2016 Mega-Tins |  | 12 |
| 02_YuGiOh | 2016 Mega-Tins Mega Pack |  | 239 |
| 02_YuGiOh | 2017 Mega-Tins |  | 10 |
| 02_YuGiOh | 2017 Mega-Tins Mega Pack |  | 239 |
| 02_YuGiOh | 2018 Mega-Tins |  | 10 |
| 02_YuGiOh | 2018 Mega-Tins Mega Pack |  | 233 |
| 02_YuGiOh | 2019 Gold Sarcophagus Tin |  | 14 |
| 02_YuGiOh | 2019 Gold Sarcophagus Tin Mega Pack |  | 270 |
| 02_YuGiOh | 2020 Tin of Lost Memories |  | 249 |
| 02_YuGiOh | 2021 Tin of Ancient Battles |  | 258 |
| 02_YuGiOh | 2025 Mega-Pack |  | 400 |
| 02_YuGiOh | 25th Anniversary Rarity Collection | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23233/logo.webp | 263 |
| 02_YuGiOh | 25th Anniversary Rarity Collection II |  | 467 |
| 02_YuGiOh | 25th Anniversary Tin: Dueling Heroes |  | 2 |
| 02_YuGiOh | 25th Anniversary Tin: Dueling Heroes Mega Pack |  | 283 |
| 02_YuGiOh | 25th Anniversary Tin: Dueling Mirrors |  | 400 |
| 02_YuGiOh | 25th Anniversary Ultimate Kaiba Set | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23366/logo.webp | 63 |
| 02_YuGiOh | 5D's 2008 Starter Deck |  | 46 |
| 02_YuGiOh | 5D's Starter Deck 2009 |  | 43 |
| 02_YuGiOh | Absolute Powerforce | https://holodex-prod-bucket.b-cdn.net/sets/ygo_141/logo.webp | 115 |
| 02_YuGiOh | Abyss Rising | https://holodex-prod-bucket.b-cdn.net/sets/ygo_573/logo.webp | 114 |
| 02_YuGiOh | Advanced Demo Deck Extra Pack |  | 10 |
| 02_YuGiOh | Advent Calendar 2011 (Adventskalender) |  | 24 |
| 02_YuGiOh | Advent Calendar 2014 (Adventskalender ZEXAL-Edition) |  | 24 |
| 02_YuGiOh | Advent Calendar 2018 |  | 24 |
| 02_YuGiOh | Advent Calendar 2019 |  | 24 |
| 02_YuGiOh | Age of Overlord |  | 126 |
| 02_YuGiOh | Alliance Insight | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23995/logo.webp | 131 |
| 02_YuGiOh | Amazing Defenders | https://holodex-prod-bucket.b-cdn.net/sets/ygo_17663/logo.webp | 75 |
| 02_YuGiOh | Ancient Guardians | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2767/logo.webp | 75 |
| 02_YuGiOh | Ancient Prophecy | https://holodex-prod-bucket.b-cdn.net/sets/ygo_144/logo.webp | 113 |
| 02_YuGiOh | Ancient Prophecy SE | https://holodex-prod-bucket.b-cdn.net/sets/ygo_145/logo.webp | 2 |
| 02_YuGiOh | Ancient Sanctuary | https://holodex-prod-bucket.b-cdn.net/sets/ygo_146/logo.webp | 112 |
| 02_YuGiOh | Astral Pack 1 |  | 25 |
| 02_YuGiOh | Astral Pack 2 |  | 25 |
| 02_YuGiOh | Astral Pack 3 |  | 26 |
| 02_YuGiOh | Astral Pack 4 |  | 26 |
| 02_YuGiOh | Astral Pack 5 |  | 26 |
| 02_YuGiOh | Astral Pack 6 |  | 28 |
| 02_YuGiOh | Astral Pack 7 |  | 27 |
| 02_YuGiOh | Astral Pack 8 |  | 27 |
| 02_YuGiOh | Battle Pack 2: War of the Giants |  | 367 |
| 02_YuGiOh | Battle Pack 2: War of the Giants Round 2 |  | 102 |
| 02_YuGiOh | Battle Pack 3: Monster League |  | 457 |
| 02_YuGiOh | Battle Pack Tournament Prize Cards |  | 20 |
| 02_YuGiOh | Battle Pack: Epic Dawn |  | 431 |
| 02_YuGiOh | Battle of Chaos | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2969/logo.webp | 107 |
| 02_YuGiOh | Battles of Legend: Armageddon | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2660/logo.webp | 94 |
| 02_YuGiOh | Battles of Legend: Chapter 1 |  | 199 |
| 02_YuGiOh | Battles of Legend: Crystal Revenge | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3155/logo.webp | 107 |
| 02_YuGiOh | Battles of Legend: Glorious Gallery | https://holodex-prod-bucket.b-cdn.net/sets/tgo_24621/logo.webp | 181 |
| 02_YuGiOh | Battles of Legend: Hero's Revenge |  | 94 |
| 02_YuGiOh | Battles of Legend: Light's Revenge |  | 80 |
| 02_YuGiOh | Battles of Legend: Monster Mayhem | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24263/logo.webp | 202 |
| 02_YuGiOh | Battles of Legend: Monstrous Revenge | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23031/logo.webp | 127 |
| 02_YuGiOh | Battles of Legend: Relentless Revenge |  | 105 |
| 02_YuGiOh | Battles of Legend: Terminal Revenge | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23441/logo.webp | 140 |
| 02_YuGiOh | Blazing Dominion | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24581/logo.webp | 131 |
| 02_YuGiOh | Blazing Vortex | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2749/logo.webp | 106 |
| 02_YuGiOh | Bonds Beyond Time Movie Pack |  | 11 |
| 02_YuGiOh | Breakers of Shadow | https://holodex-prod-bucket.b-cdn.net/sets/ygo_1698/logo.webp | 105 |
| 02_YuGiOh | Brothers of Legend | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2877/logo.webp | 95 |
| 02_YuGiOh | Burst Protocol | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24558/logo.webp | 131 |
| 02_YuGiOh | Burst of Destiny | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2879/logo.webp | 106 |
| 02_YuGiOh | Champion Pack 1 |  | 20 |
| 02_YuGiOh | Champion Pack 2 |  | 20 |
| 02_YuGiOh | Champion Pack 3 |  | 20 |
| 02_YuGiOh | Champion Pack 4 |  | 20 |
| 02_YuGiOh | Champion Pack 5 |  | 20 |
| 02_YuGiOh | Champion Pack 6 |  | 20 |
| 02_YuGiOh | Champion Pack 7 |  | 20 |
| 02_YuGiOh | Champion Pack 8 |  | 20 |
| 02_YuGiOh | Chaos Impact | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2527/logo.webp | 109 |
| 02_YuGiOh | Chaos Origins | https://holodex-prod-bucket.b-cdn.net/sets/tgo_24675/logo.webp | 136 |
| 02_YuGiOh | Circuit Break | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2056/logo.webp | 105 |
| 02_YuGiOh | Clash of Rebellions | https://ibb.co/Kj0d1gcQ | 111 |
| 02_YuGiOh | Code of the Duelist | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1989/logo.webp | 105 |
| 02_YuGiOh | Collector's Boxes |  | 4 |
| 02_YuGiOh | Cosmo Blazer | https://holodex-prod-bucket.b-cdn.net/sets/tgo_576/logo.webp | 111 |
| 02_YuGiOh | Cosmo Blazer SE |  | 2 |
| 02_YuGiOh | Crimson Crisis | https://holodex-prod-bucket.b-cdn.net/sets/tgo_157/logo.webp | 113 |
| 02_YuGiOh | Crossed Souls | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1537/logo.webp | 107 |
| 02_YuGiOh | Crossed Souls: Advanced Edition |  | 4 |
| 02_YuGiOh | Crossover Breakers | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23653/logo.webp | 105 |
| 02_YuGiOh | Crossroads of Chaos | https://holodex-prod-bucket.b-cdn.net/sets/tgo_158/logo.webp | 114 |
| 02_YuGiOh | Cyberdark Impact | https://holodex-prod-bucket.b-cdn.net/sets/ygo_159/logo.webp | 85 |
| 02_YuGiOh | Cybernetic Horizon | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2267/logo.webp | 105 |
| 02_YuGiOh | Cybernetic Revolution | https://holodex-prod-bucket.b-cdn.net/sets/ygo_160/logo.webp | 85 |
| 02_YuGiOh | Cyberstorm Access | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22896/logo.webp | 106 |
| 02_YuGiOh | Dark Beginning 1 |  | 249 |
| 02_YuGiOh | Dark Beginning 2 |  | 250 |
| 02_YuGiOh | Dark Crisis | https://holodex-prod-bucket.b-cdn.net/sets/tgo_165/logo.webp | 99 |
| 02_YuGiOh | Dark Crisis (25th Anniversary Edition) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23055/logo.webp | 50 |
| 02_YuGiOh | Dark Crisis (Worldwide English) |  | 7 |
| 02_YuGiOh | Dark Legends |  | 113 |
| 02_YuGiOh | Dark Neostorm | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2421/logo.webp | 105 |
| 02_YuGiOh | Dark Revelation Volume 1 |  | 264 |
| 02_YuGiOh | Dark Revelation Volume 2 |  | 224 |
| 02_YuGiOh | Dark Revelation Volume 3 |  | 238 |
| 02_YuGiOh | Dark Revelation Volume 4 |  | 245 |
| 02_YuGiOh | Dark Saviors |  | 60 |
| 02_YuGiOh | Darkwing Blast | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3111/logo.webp | 106 |
| 02_YuGiOh | Dawn of Destiny Xbox |  | 6 |
| 02_YuGiOh | Dawn of Majesty | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2843/logo.webp | 106 |
| 02_YuGiOh | Demo Deck 2015 |  | 20 |
| 02_YuGiOh | Demo Deck 2016 |  | 20 |
| 02_YuGiOh | Demo Pack |  | 20 |
| 02_YuGiOh | Destiny Board Traveler Promo |  | 3 |
| 02_YuGiOh | Destiny Soldiers |  | 55 |
| 02_YuGiOh | Dimension Force | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3029/logo.webp | 106 |
| 02_YuGiOh | Dimension of Chaos | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1660/logo.webp | 111 |
| 02_YuGiOh | Doom of Dimensions | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24357/logo.webp | 131 |
| 02_YuGiOh | Dragons of Legend |  | 22 |
| 02_YuGiOh | Dragons of Legend 2 |  | 45 |
| 02_YuGiOh | Dragons of Legend: The Complete Series |  | 239 |
| 02_YuGiOh | Dragons of Legend: Unleashed |  | 73 |
| 02_YuGiOh | Duel Devastator |  | 56 |
| 02_YuGiOh | Duel Master's Guide |  | 1 |
| 02_YuGiOh | Duel Overload |  | 106 |
| 02_YuGiOh | Duel Power |  | 106 |
| 02_YuGiOh | Duel Terminal - Preview |  | 31 |
| 02_YuGiOh | Duel Terminal 1 |  | 100 |
| 02_YuGiOh | Duel Terminal 2 |  | 100 |
| 02_YuGiOh | Duel Terminal 3 |  | 100 |
| 02_YuGiOh | Duel Terminal 4 |  | 100 |
| 02_YuGiOh | Duel Terminal 5 |  | 100 |
| 02_YuGiOh | Duel Terminal 6 |  | 100 |
| 02_YuGiOh | Duel Terminal 7 |  | 100 |
| 02_YuGiOh | Duelist Alliance | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1480/logo.webp | 107 |
| 02_YuGiOh | Duelist Alliance: Deluxe Edition |  | 7 |
| 02_YuGiOh | Duelist League Demo 2010 |  | 5 |
| 02_YuGiOh | Duelist League Promo |  | 726 |
| 02_YuGiOh | Duelist Nexus | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23086/logo.webp | 125 |
| 02_YuGiOh | Duelist Pack 10: Yusei 3 |  | 30 |
| 02_YuGiOh | Duelist Pack 11: Crow |  | 30 |
| 02_YuGiOh | Duelist Pack 1: Jaden Yuki |  | 30 |
| 02_YuGiOh | Duelist Pack 2: Chazz Princeton |  | 30 |
| 02_YuGiOh | Duelist Pack 3: Jaden Yuki 2 |  | 30 |
| 02_YuGiOh | Duelist Pack 4: Zane Truesdale |  | 30 |
| 02_YuGiOh | Duelist Pack 5: Aster Phoenix |  | 30 |
| 02_YuGiOh | Duelist Pack 6: Jaden Yuki 3 |  | 25 |
| 02_YuGiOh | Duelist Pack 7: Jesse Anderson |  | 25 |
| 02_YuGiOh | Duelist Pack 8: Yusei Fudo |  | 30 |
| 02_YuGiOh | Duelist Pack 9: Yusei 2 |  | 30 |
| 02_YuGiOh | Duelist Pack Collection Tin |  | 10 |
| 02_YuGiOh | Duelist Pack Special Edition |  | 3 |
| 02_YuGiOh | Duelist Pack: Battle City |  | 47 |
| 02_YuGiOh | Duelist Pack: Dimensional Guardians |  | 45 |
| 02_YuGiOh | Duelist Pack: Kaiba |  | 40 |
| 02_YuGiOh | Duelist Pack: Rivals of the Pharaoh |  | 46 |
| 02_YuGiOh | Duelist Pack: Yugi |  | 30 |
| 02_YuGiOh | Duelist Revolution | https://holodex-prod-bucket.b-cdn.net/sets/tgo_198/logo.webp | 114 |
| 02_YuGiOh | Duelist Saga |  | 100 |
| 02_YuGiOh | Duelist of the Roses |  | 3 |
| 02_YuGiOh | Duelist's Advance | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24265/logo.webp | 131 |
| 02_YuGiOh | Early Days Collection Promotional Cards |  | 2 |
| 02_YuGiOh | Egyptian God Deck: Obelisk the Tormentor |  | 35 |
| 02_YuGiOh | Egyptian God Deck: Slifer the Sky Dragon |  | 38 |
| 02_YuGiOh | Elemental Energy | https://holodex-prod-bucket.b-cdn.net/sets/ygo_200/logo.webp | 90 |
| 02_YuGiOh | Elemental Hero Collection 1 |  | 4 |
| 02_YuGiOh | Elemental Hero Collection 2 |  | 4 |
| 02_YuGiOh | Enemy of Justice | https://holodex-prod-bucket.b-cdn.net/sets/ygo_201/logo.webp | 85 |
| 02_YuGiOh | Eternal Duelist Soul |  | 3 |
| 02_YuGiOh | Eternity Code | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2625/logo.webp | 106 |
| 02_YuGiOh | Event Pack Speed Duel |  | 7 |
| 02_YuGiOh | Extreme Force | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2151/logo.webp | 105 |
| 02_YuGiOh | Extreme Victory | https://holodex-prod-bucket.b-cdn.net/sets/tgo_203/logo.webp | 111 |
| 02_YuGiOh | Fire Fists Special Editon |  | 1 |
| 02_YuGiOh | Fists of the Gadgets |  | 60 |
| 02_YuGiOh | Flames of Destruction | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2212/logo.webp | 105 |
| 02_YuGiOh | Flaming Eternity | https://holodex-prod-bucket.b-cdn.net/sets/ygo_204/logo.webp | 85 |
| 02_YuGiOh | Forbidden Legacy |  | 3 |
| 02_YuGiOh | Force of the Breaker | https://holodex-prod-bucket.b-cdn.net/sets/ygo_208/logo.webp | 96 |
| 02_YuGiOh | Fusion Enforcers |  | 60 |
| 02_YuGiOh | GX Duel Academy GBA Promo |  | 3 |
| 02_YuGiOh | GX Next Generation Blister Pack Promo |  | 1 |
| 02_YuGiOh | GX Spirit Caller Promo |  | 3 |
| 02_YuGiOh | GX Tag Force Promo |  | 3 |
| 02_YuGiOh | GX Ultimate Beginner's Pack 1 |  | 5 |
| 02_YuGiOh | Galactic Overlord | https://holodex-prod-bucket.b-cdn.net/sets/tgo_578/logo.webp | 112 |
| 02_YuGiOh | Generation Force | https://holodex-prod-bucket.b-cdn.net/sets/tgo_209/logo.webp | 114 |
| 02_YuGiOh | Genesis Impact | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2679/logo.webp | 75 |
| 02_YuGiOh | Ghosts From the Past |  | 132 |
| 02_YuGiOh | Ghosts From the Past: The 2nd Haunting | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3011/logo.webp | 183 |
| 02_YuGiOh | Gladiator's Assault | https://holodex-prod-bucket.b-cdn.net/sets/tgo_210/logo.webp | 111 |
| 02_YuGiOh | Gladiator's Assault SE |  | 2 |
| 02_YuGiOh | Gold Series 2008 |  | 45 |
| 02_YuGiOh | Gold Series 2009 |  | 50 |
| 02_YuGiOh | Gold Series 3 |  | 50 |
| 02_YuGiOh | Gold Series 4: Pyramids Edition |  | 50 |
| 02_YuGiOh | Gold Series: Haunted Mine |  | 55 |
| 02_YuGiOh | Hidden Arsenal |  | 10 |
| 02_YuGiOh | Hidden Arsenal 2 |  | 60 |
| 02_YuGiOh | Hidden Arsenal 3 |  | 60 |
| 02_YuGiOh | Hidden Arsenal 4 |  | 62 |
| 02_YuGiOh | Hidden Arsenal 5: Steelswarm Invasion |  | 62 |
| 02_YuGiOh | Hidden Arsenal 6: Omega Xyz |  | 60 |
| 02_YuGiOh | Hidden Arsenal 7: Knight of Stars |  | 70 |
| 02_YuGiOh | Hidden Arsenal: Chapter 1 |  | 316 |
| 02_YuGiOh | Hidden Summoners |  | 60 |
| 02_YuGiOh | High-Speed Riders |  | 60 |
| 02_YuGiOh | Hobby League 1 |  | 6 |
| 02_YuGiOh | Hobby League 2 |  | 6 |
| 02_YuGiOh | Hobby League 3 |  | 7 |
| 02_YuGiOh | Hobby League 4 |  | 6 |
| 02_YuGiOh | Hobby League 5 |  | 6 |
| 02_YuGiOh | Hobby League 6 |  | 6 |
| 02_YuGiOh | Hobby League 7 |  | 6 |
| 02_YuGiOh | Ignition Assault | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2578/logo.webp | 109 |
| 02_YuGiOh | Invasion of Chaos | https://holodex-prod-bucket.b-cdn.net/sets/ygo_237/logo.webp | 106 |
| 02_YuGiOh | Invasion of Chaos (25th Anniversary Edition) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23056/logo.webp | 112 |
| 02_YuGiOh | Invasion of Chaos (Worldwide English) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22887/logo.webp | 8 |
| 02_YuGiOh | Invasion: Vengeance | https://ibb.co/LDBNZ95r | 105 |
| 02_YuGiOh | Judge Promotional Cards |  | 24 |
| 02_YuGiOh | Judgment of the Light | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1142/logo.webp | 111 |
| 02_YuGiOh | Justice Hunters | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24320/logo.webp | 103 |
| 02_YuGiOh | King of Games: Yugi's Legendary Decks |  | 133 |
| 02_YuGiOh | King of Games: Yugi's Legendary Decks (2020 Date Reprint) |  | 133 |
| 02_YuGiOh | King's Court | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2808/logo.webp | 83 |
| 02_YuGiOh | Labyrinth of Nightmare | https://holodex-prod-bucket.b-cdn.net/sets/ygo_241/logo.webp | 105 |
| 02_YuGiOh | Labyrinth of Nightmare (Worldwide English) |  | 105 |
| 02_YuGiOh | Legacy of Darkness |  | 102 |
| 02_YuGiOh | Legacy of Darkness (Worldwide English) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22885/logo.webp | 99 |
| 02_YuGiOh | Legacy of Destruction |  | 131 |
| 02_YuGiOh | Legacy of the Valiant | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1286/logo.webp | 111 |
| 02_YuGiOh | Legend of Blue Eyes White Dragon (25th Anniversary Edition) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23050/logo.webp | 126 |
| 02_YuGiOh | Legend of Blue Eyes White Dragon (Worldwide English) |  | 51 |
| 02_YuGiOh | Legendary 5D's Decks |  | 118 |
| 02_YuGiOh | Legendary Arc-V Decks |  | 108 |
| 02_YuGiOh | Legendary Collection 1 |  | 6 |
| 02_YuGiOh | Legendary Collection 2 |  | 279 |
| 02_YuGiOh | Legendary Collection 3: Yugi's World |  | 313 |
| 02_YuGiOh | Legendary Collection 4: Joey's World |  | 305 |
| 02_YuGiOh | Legendary Collection Kaiba |  | 115 |
| 02_YuGiOh | Legendary Collection Kaiba (2020 Date Reprint) |  | 55 |
| 02_YuGiOh | Legendary Collection: 25th Anniversary Edition | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22895/logo.webp | 12 |
| 02_YuGiOh | Legendary Decks II |  | 135 |
| 02_YuGiOh | Legendary Decks II (2020 Reprint) |  | 135 |
| 02_YuGiOh | Legendary Dragon Decks |  | 99 |
| 02_YuGiOh | Legendary Dragon Decks (2020 Date Reprint) |  | 42 |
| 02_YuGiOh | Legendary Duelists |  | 51 |
| 02_YuGiOh | Legendary Duelists: Ancient Millennium |  | 53 |
| 02_YuGiOh | Legendary Duelists: Duels From the Deep | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3013/logo.webp | 57 |
| 02_YuGiOh | Legendary Duelists: Immortal Destiny |  | 58 |
| 02_YuGiOh | Legendary Duelists: Magical Hero |  | 57 |
| 02_YuGiOh | Legendary Duelists: Rage of Ra |  | 58 |
| 02_YuGiOh | Legendary Duelists: Season 1 |  | 163 |
| 02_YuGiOh | Legendary Duelists: Season 2 |  | 221 |
| 02_YuGiOh | Legendary Duelists: Season 3 |  | 196 |
| 02_YuGiOh | Legendary Duelists: Sisters of the Rose |  | 56 |
| 02_YuGiOh | Legendary Duelists: Soulburning Volcano | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23111/logo.webp | 62 |
| 02_YuGiOh | Legendary Duelists: Synchro Storm | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2829/logo.webp | 57 |
| 02_YuGiOh | Legendary Duelists: White Dragon Abyss |  | 56 |
| 02_YuGiOh | Legendary Hero Decks |  | 120 |
| 02_YuGiOh | Legendary Modern Decks 2026 |  | 154 |
| 02_YuGiOh | Light and Darkness Power Pack |  | 1 |
| 02_YuGiOh | Light of Destruction | https://holodex-prod-bucket.b-cdn.net/sets/tgo_247/logo.webp | 89 |
| 02_YuGiOh | Light of Destruction (2020 Date Reprint) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23579/logo.webp | 61 |
| 02_YuGiOh | Lightning Overdrive | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2779/logo.webp | 106 |
| 02_YuGiOh | Limited Pack World Championship 2025 |  | 82 |
| 02_YuGiOh | Lord of the Tachyon Galaxy | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1112/logo.webp | 112 |
| 02_YuGiOh | Magic Ruler | https://holodex-prod-bucket.b-cdn.net/sets/tgo_249/logo.webp | 131 |
| 02_YuGiOh | Magician's Force | https://holodex-prod-bucket.b-cdn.net/sets/tgo_250/logo.webp | 109 |
| 02_YuGiOh | Magnificent Mavens | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3154/logo.webp | 139 |
| 02_YuGiOh | Master Collection Volume 1 |  | 6 |
| 02_YuGiOh | Master Collection Volume 2 |  | 6 |
| 02_YuGiOh | Mattel Action Figure Promos: Series 1 |  | 1 |
| 02_YuGiOh | Mattel Action Figure Promos: Series 2 |  | 4 |
| 02_YuGiOh | Mattel Action Figure Promos: Series 3 |  | 11 |
| 02_YuGiOh | Maximum Crisis |  | 105 |
| 02_YuGiOh | Maximum Gold | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2693/logo.webp | 170 |
| 02_YuGiOh | Maximum Gold: El Dorado |  | 161 |
| 02_YuGiOh | Maze of Memories | https://holodex-prod-bucket.b-cdn.net/sets/ygo_17701/logo.webp | 82 |
| 02_YuGiOh | Maze of Millennia | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23315/logo.webp | 101 |
| 02_YuGiOh | Maze of Muertos | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24559/logo.webp | 142 |
| 02_YuGiOh | Maze of the Master | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23849/logo.webp | 128 |
| 02_YuGiOh | McDonald's Promo |  | 15 |
| 02_YuGiOh | McDonald's Promo Series 2 |  | 20 |
| 02_YuGiOh | Metal Raiders | https://holodex-prod-bucket.b-cdn.net/sets/ygo_255/logo.webp | 145 |
| 02_YuGiOh | Metal Raiders (25th Anniversary Edition) |  | 144 |
| 02_YuGiOh | Metal Raiders (Worldwide English) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22882/logo.webp | 144 |
| 02_YuGiOh | Millennium Pack |  | 48 |
| 02_YuGiOh | Miscellaneous Promotional Cards |  | 21 |
| 02_YuGiOh | Mystic Fighters |  | 60 |
| 02_YuGiOh | Nintendo DS Nightmare of Troubadour |  | 3 |
| 02_YuGiOh | Noble Knights of the Round Table Box Set |  | 44 |
| 02_YuGiOh | Number Hunters |  | 60 |
| 02_YuGiOh | OTS Tournament Pack 1 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 10 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 11 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 12 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 13 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 14 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 15 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 16 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 17 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 18 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 19 |  | 29 |
| 02_YuGiOh | OTS Tournament Pack 2 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 20 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 21 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 22 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 23 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 24 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 25 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 26 |  | 30 |
| 02_YuGiOh | OTS Tournament Pack 27 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 28 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 29 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 3 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 30 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 4 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 5 |  | 27 |
| 02_YuGiOh | OTS Tournament Pack 6 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 7 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 8 |  | 26 |
| 02_YuGiOh | OTS Tournament Pack 9 |  | 28 |
| 02_YuGiOh | Order of Chaos | https://holodex-prod-bucket.b-cdn.net/sets/tgo_257/logo.webp | 64 |
| 02_YuGiOh | PS2 Yugioh GX The Beginning of Destiny |  | 1 |
| 02_YuGiOh | Pendulum Evolution |  | 60 |
| 02_YuGiOh | Phantom Darkness | https://holodex-prod-bucket.b-cdn.net/sets/tgo_258/logo.webp | 114 |
| 02_YuGiOh | Phantom Nightmare | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23321/logo.webp | 126 |
| 02_YuGiOh | Phantom Rage | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2694/logo.webp | 106 |
| 02_YuGiOh | Phantom Revenge | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24475/logo.webp | 104 |
| 02_YuGiOh | Pharaoh Tour Promos |  | 6 |
| 02_YuGiOh | Pharaoh's Servant | https://holodex-prod-bucket.b-cdn.net/sets/ygo_259/logo.webp | 42 |
| 02_YuGiOh | Pharaoh's Servant (25th Anniversary Edition) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23054/logo.webp | 105 |
| 02_YuGiOh | Pharaoh's Servant (Worldwide English) |  | 50 |
| 02_YuGiOh | Pharaonic Guardian |  | 108 |
| 02_YuGiOh | Photon Hypernova | https://holodex-prod-bucket.b-cdn.net/sets/ygo_17680/logo.webp | 56 |
| 02_YuGiOh | Photon Shockwave | https://holodex-prod-bucket.b-cdn.net/sets/tgo_261/logo.webp | 112 |
| 02_YuGiOh | Power of Chaos: Joey the Passion |  | 3 |
| 02_YuGiOh | Power of Chaos: Yugi the Destiny |  | 5 |
| 02_YuGiOh | Power of the Duelist | https://holodex-prod-bucket.b-cdn.net/sets/ygo_265/logo.webp | 85 |
| 02_YuGiOh | Power of the Elements | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3104/logo.webp | 106 |
| 02_YuGiOh | Premium Gold |  | 31 |
| 02_YuGiOh | Premium Gold: Infinite Gold |  | 100 |
| 02_YuGiOh | Premium Gold: Return of the Bling |  | 91 |
| 02_YuGiOh | Premium Pack 1 |  | 22 |
| 02_YuGiOh | Premium Pack 2 |  | 30 |
| 02_YuGiOh | Primal Origin | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1353/logo.webp | 112 |
| 02_YuGiOh | Quarter Century Bonanza | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23656/logo.webp | 963 |
| 02_YuGiOh | Quarter Century Stampede | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23891/logo.webp | 836 |
| 02_YuGiOh | Ra Yellow Mega Pack |  | 114 |
| 02_YuGiOh | Rage of the Abyss | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23539/logo.webp | 132 |
| 02_YuGiOh | Raging Battle | https://holodex-prod-bucket.b-cdn.net/sets/tgo_270/logo.webp | 112 |
| 02_YuGiOh | Raging Battle SE |  | 3 |
| 02_YuGiOh | Raging Tempest | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1880/logo.webp | 105 |
| 02_YuGiOh | Rarity Collection 5 | https://holodex-prod-bucket.b-cdn.net/sets/ygo_24555/logo.webp | 696 |
| 02_YuGiOh | Redemption Replacement |  | 9 |
| 02_YuGiOh | Reshef of Destruction |  | 1 |
| 02_YuGiOh | Retro Pack |  | 1 |
| 02_YuGiOh | Retro Pack (2020 Date Reprint) |  | 65 |
| 02_YuGiOh | Retro Pack 2 |  | 57 |
| 02_YuGiOh | Retro Pack 2 (2020 Date Reprint) |  | 101 |
| 02_YuGiOh | Return of the Duelist | https://holodex-prod-bucket.b-cdn.net/sets/tgo_587/logo.webp | 112 |
| 02_YuGiOh | Return of the Duelist SE |  | 2 |
| 02_YuGiOh | Rise of Destiny | https://holodex-prod-bucket.b-cdn.net/sets/ygo_274/logo.webp | 85 |
| 02_YuGiOh | Rise of Destiny Special Edition | https://holodex-prod-bucket.b-cdn.net/sets/ygo_275/logo.webp | 4 |
| 02_YuGiOh | Rise of the Duelist | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2674/logo.webp | 106 |
| 02_YuGiOh | Rising Rampage | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2462/logo.webp | 109 |
| 02_YuGiOh | Samurai Assault |  | 1 |
| 02_YuGiOh | Savage Strike | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2380/logo.webp | 105 |
| 02_YuGiOh | Secret Slayers |  | 60 |
| 02_YuGiOh | Secrets of Eternity | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1505/logo.webp | 121 |
| 02_YuGiOh | Shadow Specters | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1156/logo.webp | 109 |
| 02_YuGiOh | Shadow of Infinity | https://holodex-prod-bucket.b-cdn.net/sets/ygo_277/logo.webp | 93 |
| 02_YuGiOh | Shadows in Valhalla |  | 60 |
| 02_YuGiOh | Shining Victories | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1761/logo.webp | 105 |
| 02_YuGiOh | Shonen Jump Championship Series Prize Cards |  | 2 |
| 02_YuGiOh | Shonen Jump Championship Series Promos |  | 5 |
| 02_YuGiOh | Shonen Jump Magazine Promos |  | 100 |
| 02_YuGiOh | Sneak Preview Series 1 |  | 4 |
| 02_YuGiOh | Sneak Preview Series 2 |  | 4 |
| 02_YuGiOh | Sneak Preview Series 3 |  | 4 |
| 02_YuGiOh | Sneak Preview Series 4 |  | 1 |
| 02_YuGiOh | Sneak Preview Series 5 |  | 1 |
| 02_YuGiOh | Soul Fusion | https://holodex-prod-bucket.b-cdn.net/sets/tgo_2327/logo.webp | 105 |
| 02_YuGiOh | Soul of the Duelist | https://holodex-prod-bucket.b-cdn.net/sets/ygo_285/logo.webp | 85 |
| 02_YuGiOh | Speed Duel Decks: Destiny Masters |  | 64 |
| 02_YuGiOh | Speed Duel Decks: Duelists of Tomorrow |  | 69 |
| 02_YuGiOh | Speed Duel Decks: Match of the Millennium |  | 67 |
| 02_YuGiOh | Speed Duel Decks: Twisted Nightmares |  | 66 |
| 02_YuGiOh | Speed Duel Decks: Ultimate Predators |  | 63 |
| 02_YuGiOh | Speed Duel Demo Deck |  | 11 |
| 02_YuGiOh | Speed Duel Demo Deck 2020 |  | 21 |
| 02_YuGiOh | Speed Duel GX: Duel Academy Box |  | 242 |
| 02_YuGiOh | Speed Duel GX: Duelists of Shadows |  | 242 |
| 02_YuGiOh | Speed Duel GX: Midterm Destruction |  | 132 |
| 02_YuGiOh | Speed Duel GX: Midterm Paradox |  | 122 |
| 02_YuGiOh | Speed Duel: Arena of Lost Souls |  | 50 |
| 02_YuGiOh | Speed Duel: Attack from the Deep |  | 50 |
| 02_YuGiOh | Speed Duel: Battle City Box |  | 244 |
| 02_YuGiOh | Speed Duel: Battle City Finals |  | 250 |
| 02_YuGiOh | Speed Duel: Scars of Battle |  | 50 |
| 02_YuGiOh | Speed Duel: Streets of Battle City |  | 187 |
| 02_YuGiOh | Speed Duel: Tournament Pack 1 |  | 18 |
| 02_YuGiOh | Speed Duel: Tournament Pack 2 |  | 18 |
| 02_YuGiOh | Speed Duel: Tournament Pack 3 |  | 35 |
| 02_YuGiOh | Speed Duel: Tournament Pack 4 |  | 35 |
| 02_YuGiOh | Speed Duel: Tournament Pack 5 |  | 35 |
| 02_YuGiOh | Speed Duel: Tournament Pack 6 |  | 35 |
| 02_YuGiOh | Speed Duel: Tournament Pack 7 |  | 35 |
| 02_YuGiOh | Speed Duel: Trials of the Kingdom |  | 61 |
| 02_YuGiOh | Spell Ruler |  | 104 |
| 02_YuGiOh | Spell Ruler (25th Anniversary Edition) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23053/logo.webp | 104 |
| 02_YuGiOh | Spell Ruler (Worldwide English) | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22905/logo.webp | 104 |
| 02_YuGiOh | Spirit Warriors |  | 60 |
| 02_YuGiOh | Stairway to the Destined Duel |  | 6 |
| 02_YuGiOh | Star Pack - Battle Royal |  | 99 |
| 02_YuGiOh | Star Pack 2013 |  | 100 |
| 02_YuGiOh | Star Pack 2014 |  | 100 |
| 02_YuGiOh | Star Pack ARC-V |  | 98 |
| 02_YuGiOh | Star Pack VRAINS |  | 99 |
| 02_YuGiOh | Stardust Accelerator Promos |  | 3 |
| 02_YuGiOh | Stardust Overdrive | https://holodex-prod-bucket.b-cdn.net/sets/tgo_289/logo.webp | 116 |
| 02_YuGiOh | Starstrike Blast | https://holodex-prod-bucket.b-cdn.net/sets/tgo_290/logo.webp | 110 |
| 02_YuGiOh | Starter Deck 2006 |  | 41 |
| 02_YuGiOh | Starter Deck: Codebreaker |  | 45 |
| 02_YuGiOh | Starter Deck: Dark Legion |  | 29 |
| 02_YuGiOh | Starter Deck: Dawn of the Xyz |  | 43 |
| 02_YuGiOh | Starter Deck: Duelist Toolbox |  | 42 |
| 02_YuGiOh | Starter Deck: Jaden Yuki |  | 41 |
| 02_YuGiOh | Starter Deck: Joey |  | 50 |
| 02_YuGiOh | Starter Deck: Kaiba | https://holodex-prod-bucket.b-cdn.net/sets/tgo_294/logo.webp | 50 |
| 02_YuGiOh | Starter Deck: Kaiba Evolution |  | 50 |
| 02_YuGiOh | Starter Deck: Kaiba Reloaded |  | 49 |
| 02_YuGiOh | Starter Deck: Link Strike |  | 43 |
| 02_YuGiOh | Starter Deck: Pegasus |  | 50 |
| 02_YuGiOh | Starter Deck: Saber Force |  | 28 |
| 02_YuGiOh | Starter Deck: Syrus Truesdale |  | 41 |
| 02_YuGiOh | Starter Deck: Xyz Symphony |  | 43 |
| 02_YuGiOh | Starter Deck: Yugi |  | 51 |
| 02_YuGiOh | Starter Deck: Yugi Evolution |  | 50 |
| 02_YuGiOh | Starter Deck: Yugi Reloaded |  | 47 |
| 02_YuGiOh | Starter Deck: Yuya |  | 43 |
| 02_YuGiOh | Storm of Ragnarok | https://holodex-prod-bucket.b-cdn.net/sets/tgo_302/logo.webp | 114 |
| 02_YuGiOh | Strike of Neos | https://holodex-prod-bucket.b-cdn.net/sets/ygo_304/logo.webp | 96 |
| 02_YuGiOh | Structure Deck: Albaz Strike |  | 51 |
| 02_YuGiOh | Structure Deck: Beware of Traptrix |  | 46 |
| 02_YuGiOh | Structure Deck: Blaze of Destruction |  | 31 |
| 02_YuGiOh | Structure Deck: Blue-Eyes White Destiny |  | 84 |
| 02_YuGiOh | Structure Deck: Cyber Dragon Revolution |  | 39 |
| 02_YuGiOh | Structure Deck: Cyber Strike |  | 48 |
| 02_YuGiOh | Structure Deck: Cyberse Link |  | 43 |
| 02_YuGiOh | Structure Deck: Dark World |  | 45 |
| 02_YuGiOh | Structure Deck: Deluxe Edition |  | 2 |
| 02_YuGiOh | Structure Deck: Dinosaur's Rage |  | 37 |
| 02_YuGiOh | Structure Deck: Dinosmasher's Fury |  | 40 |
| 02_YuGiOh | Structure Deck: Dragon's Roar |  | 28 |
| 02_YuGiOh | Structure Deck: Dragons Collide |  | 40 |
| 02_YuGiOh | Structure Deck: Dragunity Legion |  | 39 |
| 02_YuGiOh | Structure Deck: Emperor of Darkness |  | 42 |
| 02_YuGiOh | Structure Deck: Fire Kings |  | 48 |
| 02_YuGiOh | Structure Deck: Freezing Chains |  | 46 |
| 02_YuGiOh | Structure Deck: Fury from the Deep |  | 32 |
| 02_YuGiOh | Structure Deck: Gates of the Underworld |  | 39 |
| 02_YuGiOh | Structure Deck: Geargia Rampage |  | 35 |
| 02_YuGiOh | Structure Deck: HERO Strike |  | 45 |
| 02_YuGiOh | Structure Deck: Invincible Fortress |  | 32 |
| 02_YuGiOh | Structure Deck: Lair of Darkness |  | 42 |
| 02_YuGiOh | Structure Deck: Legend of the Crystal Beasts |  | 49 |
| 02_YuGiOh | Structure Deck: Lord of the Storm |  | 36 |
| 02_YuGiOh | Structure Deck: Lost Sanctuary |  | 38 |
| 02_YuGiOh | Structure Deck: Machina Mayhem |  | 37 |
| 02_YuGiOh | Structure Deck: Machine Re-Volt |  | 37 |
| 02_YuGiOh | Structure Deck: Machine Reactor |  | 40 |
| 02_YuGiOh | Structure Deck: Marik |  | 38 |
| 02_YuGiOh | Structure Deck: Master of Pendulum |  | 43 |
| 02_YuGiOh | Structure Deck: Mechanized Madness |  | 41 |
| 02_YuGiOh | Structure Deck: Onslaught of the Fire Kings |  | 39 |
| 02_YuGiOh | Structure Deck: Order of the Spellcasters |  | 41 |
| 02_YuGiOh | Structure Deck: Pendulum Domination |  | 43 |
| 02_YuGiOh | Structure Deck: Powercode Link |  | 42 |
| 02_YuGiOh | Structure Deck: Realm of Light |  | 36 |
| 02_YuGiOh | Structure Deck: Realm of Light (2020 Date Reprint) |  | 36 |
| 02_YuGiOh | Structure Deck: Realm of the Sea Emperor |  | 39 |
| 02_YuGiOh | Structure Deck: Rise of the Dragon Lords |  | 37 |
| 02_YuGiOh | Structure Deck: Rise of the True Dragons |  | 42 |
| 02_YuGiOh | Structure Deck: Rokket Revolt |  | 46 |
| 02_YuGiOh | Structure Deck: Sacred Beasts |  | 48 |
| 02_YuGiOh | Structure Deck: Saga of Blue Eyes White Dragon (2020 Date Reprint) |  | 40 |
| 02_YuGiOh | Structure Deck: Saga of Blue-Eyes White Dragon |  | 40 |
| 02_YuGiOh | Structure Deck: Samurai Warlords |  | 41 |
| 02_YuGiOh | Structure Deck: Seto Kaiba |  | 44 |
| 02_YuGiOh | Structure Deck: Shaddoll Showdown |  | 49 |
| 02_YuGiOh | Structure Deck: Soulburner |  | 45 |
| 02_YuGiOh | Structure Deck: Spellcaster's Command |  | 39 |
| 02_YuGiOh | Structure Deck: Spellcaster's Judgment |  | 36 |
| 02_YuGiOh | Structure Deck: Spirit Charmers |  | 50 |
| 02_YuGiOh | Structure Deck: Synchron Extreme |  | 43 |
| 02_YuGiOh | Structure Deck: The Crimson King |  | 50 |
| 02_YuGiOh | Structure Deck: The Dark Emperor |  | 36 |
| 02_YuGiOh | Structure Deck: Warrior's Triumph |  | 36 |
| 02_YuGiOh | Structure Deck: Warriors' Strike |  | 38 |
| 02_YuGiOh | Structure Deck: Wave of Light |  | 42 |
| 02_YuGiOh | Structure Deck: Yugi Muto |  | 45 |
| 02_YuGiOh | Structure Deck: Zombie Horde |  | 42 |
| 02_YuGiOh | Structure Deck: Zombie Madness |  | 28 |
| 02_YuGiOh | Structure Deck: Zombie World |  | 37 |
| 02_YuGiOh | Super Starter: Space-Time Showdown |  | 40 |
| 02_YuGiOh | Super Starter: Space-Time Showdown Power-Up Pack |  | 15 |
| 02_YuGiOh | Super Starter: V for Victory |  | 42 |
| 02_YuGiOh | Super Starter: V for Victory Power-Up Pack |  | 15 |
| 02_YuGiOh | Supreme Darkness | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23758/logo.webp | 131 |
| 02_YuGiOh | Tactical Evolution | https://holodex-prod-bucket.b-cdn.net/sets/ygo_325/logo.webp | 106 |
| 02_YuGiOh | Tactical Evolution: Special Edition | https://holodex-prod-bucket.b-cdn.net/sets/ygo_326/logo.webp | 2 |
| 02_YuGiOh | Tactical Masters | https://holodex-prod-bucket.b-cdn.net/sets/ygo_3066/logo.webp | 75 |
| 02_YuGiOh | The Dark Illusion | https://holodex-prod-bucket.b-cdn.net/sets/ygo_1807/logo.webp | 105 |
| 02_YuGiOh | The Dark Side of Dimensions Movie Pack |  | 57 |
| 02_YuGiOh | The Dark Side of Dimensions Movie Pack: Gold Edition |  | 63 |
| 02_YuGiOh | The Dark Side of Dimensions Movie Pack: Secret Edition |  | 63 |
| 02_YuGiOh | The Dark Side of Dimensions Movie Pack: Special Edition |  | 4 |
| 02_YuGiOh | The Duelist Genesis | https://holodex-prod-bucket.b-cdn.net/sets/ygo_328/logo.webp | 114 |
| 02_YuGiOh | The Falsebound Kingdom |  | 8 |
| 02_YuGiOh | The Grand Creators | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2964/logo.webp | 75 |
| 02_YuGiOh | The Infinite Forbidden | https://holodex-prod-bucket.b-cdn.net/sets/ygo_23458/logo.webp | 130 |
| 02_YuGiOh | The Infinity Chasers |  | 60 |
| 02_YuGiOh | The Legend of Blue Eyes White Dragon | https://holodex-prod-bucket.b-cdn.net/sets/ygo_330/logo.webp | 127 |
| 02_YuGiOh | The Lost Art Promotion |  | 80 |
| 02_YuGiOh | The Lost Millennium | https://holodex-prod-bucket.b-cdn.net/sets/ygo_248/logo.webp | 89 |
| 02_YuGiOh | The New Challengers | https://holodex-prod-bucket.b-cdn.net/sets/ygo_1493/logo.webp | 120 |
| 02_YuGiOh | The Pot Collection |  | 15 |
| 02_YuGiOh | The Secret Forces | https://holodex-prod-bucket.b-cdn.net/sets/ygo_1513/logo.webp | 60 |
| 02_YuGiOh | The Shining Darkness | https://holodex-prod-bucket.b-cdn.net/sets/ygo_332/logo.webp | 112 |
| 02_YuGiOh | The Valuable Book Volume 5 |  | 1 |
| 02_YuGiOh | Toon Chaos | https://holodex-prod-bucket.b-cdn.net/sets/ygo_2652/logo.webp | 75 |
| 02_YuGiOh | Tournament Pack 1 |  | 30 |
| 02_YuGiOh | Tournament Pack 2 |  | 18 |
| 02_YuGiOh | Tournament Pack 3 |  | 20 |
| 02_YuGiOh | Tournament Pack 4 |  | 13 |
| 02_YuGiOh | Tournament Pack 5 |  | 20 |
| 02_YuGiOh | Tournament Pack 6 |  | 14 |
| 02_YuGiOh | Tournament Pack 7 |  | 13 |
| 02_YuGiOh | Tournament Pack 8 |  | 20 |
| 02_YuGiOh | Toys "R" Us Throwdown Promo |  | 3 |
| 02_YuGiOh | Turbo Pack Booster One Pack |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Eight |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Five |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Four |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Seven |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Six |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Three |  | 21 |
| 02_YuGiOh | Turbo Pack: Booster Two |  | 21 |
| 02_YuGiOh | Twilight Edition |  | 1 |
| 02_YuGiOh | Ultimate Edition 2 |  | 1 |
| 02_YuGiOh | Ultimate Tournament Pack 1 |  | 50 |
| 02_YuGiOh | Valiant Smashers |  | 78 |
| 02_YuGiOh | Wild Survivors | https://holodex-prod-bucket.b-cdn.net/sets/ygo_22955/logo.webp | 75 |
| 02_YuGiOh | Wing Raiders | https://holodex-prod-bucket.b-cdn.net/sets/tgo_1707/logo.webp | 60 |
| 02_YuGiOh | Winner's Pack 2026-2027 |  | 118 |
| 02_YuGiOh | World Championship 2004: GBA Promo |  | 6 |
| 02_YuGiOh | World Championship 2005: 7 Trials to Glory |  | 3 |
| 02_YuGiOh | World Championship 2006: Ultimate Masters |  | 3 |
| 02_YuGiOh | World Championship 2007 |  | 3 |
| 02_YuGiOh | World Championship 2008 |  | 3 |
| 02_YuGiOh | World Championship 2010 Card Pack |  | 20 |
| 02_YuGiOh | World Championship 2011 Card Pack |  | 20 |
| 02_YuGiOh | World Championship JPP Cards |  | 8 |
| 02_YuGiOh | World Championship Series |  | 8 |
| 02_YuGiOh | World Superstars |  | 52 |
| 02_YuGiOh | X-Saber Power-Up |  | 1 |
| 02_YuGiOh | Yu-Gi-Oh! 5D's Manga Promotional Cards |  | 9 |
| 02_YuGiOh | Yu-Gi-Oh! 5D's Over the Nexus Promo Cards |  | 3 |
| 02_YuGiOh | Yu-Gi-Oh! 5D's Tag Force Promotional Cards |  | 3 |
| 02_YuGiOh | Yu-Gi-Oh! 5D's Wheelie Breakers Promotional Cards |  | 3 |
| 02_YuGiOh | Yu-Gi-Oh! ARC-V Promo Cards |  | 7 |
| 02_YuGiOh | Yu-Gi-Oh! Championship Series 2025 Prize Cards |  | 13 |
| 02_YuGiOh | Yu-Gi-Oh! Championship Series Prize Cards |  | 30 |
| 02_YuGiOh | Yu-Gi-Oh! Day Promos |  | 5 |
| 02_YuGiOh | Yu-Gi-Oh! Duel Monsters International: Worldwide Edition |  | 6 |
| 02_YuGiOh | Yu-Gi-Oh! GX Manga Promotional Cards |  | 8 |
| 02_YuGiOh | Yu-Gi-Oh! GX Tag Force Evolution Promo |  | 2 |
| 02_YuGiOh | Yu-Gi-Oh! GX Tag Force Promotional Cards |  | 3 |
| 02_YuGiOh | Yu-Gi-Oh! Movie Exclusive Pack |  | 9 |
| 02_YuGiOh | Yu-Gi-Oh! R Manga Promo |  | 4 |
| 02_YuGiOh | Yu-Gi-Oh! The Movie Ani-Manga Promo |  | 1 |
| 02_YuGiOh | Yu-Gi-Oh! The Movie Promo Set |  | 4 |
| 02_YuGiOh | Yu-Gi-Oh! Tokens |  | 129 |
| 02_YuGiOh | Yu-Gi-Oh! Value Boxes |  | 4 |
| 02_YuGiOh | Yu-Gi-Oh! Video Game Promotional Cards |  | 40 |
| 02_YuGiOh | Yu-Gi-Oh! ZEXAL Manga Promotional Cards |  | 9 |
| 02_YuGiOh | Yu-Gi-Oh! ZEXAL World Duel Carnival Promos |  | 3 |
| 02_YuGiOh | eFootball Collaboration Promos |  | 2 |

### 03_Pokemon（197 个系列，177 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 03_Pokemon | Alternate Art Promos | https://holodex-prod-bucket.b-cdn.net/sets/smpr/logo.webp | 56 |
| 03_Pokemon | Aquapolis | https://holodex-prod-bucket.b-cdn.net/sets/ecard2/logo.webp | 186 |
| 03_Pokemon | Arceus | https://holodex-prod-bucket.b-cdn.net/sets/pl4/logo.webp | 111 |
| 03_Pokemon | Base Set | https://holodex-prod-bucket.b-cdn.net/sets/baseu/logo.webp | 83 |
| 03_Pokemon | Base Set (Shadowless) | https://holodex-prod-bucket.b-cdn.net/sets/basesl/logo.webp | 101 |
| 03_Pokemon | Base Set 2 | https://holodex-prod-bucket.b-cdn.net/sets/base4/logo.webp | 130 |
| 03_Pokemon | Battle Academy | https://holodex-prod-bucket.b-cdn.net/sets/ba20/logo.webp | 136 |
| 03_Pokemon | Battle Academy 2022 | https://holodex-prod-bucket.b-cdn.net/sets/ba22/logo.webp | 139 |
| 03_Pokemon | Battle Academy 2024 | https://holodex-prod-bucket.b-cdn.net/sets/ba24/logo.webp | 139 |
| 03_Pokemon | Best of Promos |  | 15 |
| 03_Pokemon | Black and White | https://holodex-prod-bucket.b-cdn.net/sets/bw1/logo.webp | 97 |
| 03_Pokemon | Black and White Promos | https://holodex-prod-bucket.b-cdn.net/sets/bwp/logo.webp | 148 |
| 03_Pokemon | Blister Exclusives |  | 140 |
| 03_Pokemon | Boundaries Crossed | https://holodex-prod-bucket.b-cdn.net/sets/bw7/logo.webp | 156 |
| 03_Pokemon | Burger King Promos |  | 24 |
| 03_Pokemon | Call of Legends | https://holodex-prod-bucket.b-cdn.net/sets/col/logo.webp | 105 |
| 03_Pokemon | Celebrations | https://holodex-prod-bucket.b-cdn.net/sets/swsh10c/logo.webp | 36 |
| 03_Pokemon | Celebrations: Classic Collection | https://holodex-prod-bucket.b-cdn.net/sets/swsh10/logo.webp | 25 |
| 03_Pokemon | Champion's Path | https://holodex-prod-bucket.b-cdn.net/sets/swsh4/logo.webp | 87 |
| 03_Pokemon | Countdown Calendar Promos |  | 24 |
| 03_Pokemon | Dark Explorers | https://holodex-prod-bucket.b-cdn.net/sets/bw5/logo.webp | 112 |
| 03_Pokemon | Deck Exclusives |  | 470 |
| 03_Pokemon | Detective Pikachu | https://holodex-prod-bucket.b-cdn.net/sets/sm12/logo.webp | 25 |
| 03_Pokemon | Diamond and Pearl | https://holodex-prod-bucket.b-cdn.net/sets/dp1/logo.webp | 112 |
| 03_Pokemon | Diamond and Pearl Promos | https://holodex-prod-bucket.b-cdn.net/sets/dppromo/logo.webp | 66 |
| 03_Pokemon | Double Crisis | https://holodex-prod-bucket.b-cdn.net/sets/xy6/logo.webp | 36 |
| 03_Pokemon | Dragon Majesty | https://holodex-prod-bucket.b-cdn.net/sets/sm9/logo.webp | 86 |
| 03_Pokemon | Dragon Vault | https://holodex-prod-bucket.b-cdn.net/sets/bw8/logo.webp | 22 |
| 03_Pokemon | Dragons Exalted | https://holodex-prod-bucket.b-cdn.net/sets/bw6/logo.webp | 129 |
| 03_Pokemon | EX Battle Stadium |  | 49 |
| 03_Pokemon | EX Crystal Guardians | https://holodex-prod-bucket.b-cdn.net/sets/ex14/logo.webp | 100 |
| 03_Pokemon | EX Delta Species | https://holodex-prod-bucket.b-cdn.net/sets/ex11/logo.webp | 114 |
| 03_Pokemon | EX Deoxys | https://holodex-prod-bucket.b-cdn.net/sets/ex8/logo.webp | 108 |
| 03_Pokemon | EX Dragon | https://holodex-prod-bucket.b-cdn.net/sets/ex2/logo.webp | 45 |
| 03_Pokemon | EX Dragon Frontiers | https://holodex-prod-bucket.b-cdn.net/sets/ex15/logo.webp | 101 |
| 03_Pokemon | EX Emerald | https://holodex-prod-bucket.b-cdn.net/sets/ex9/logo.webp | 106 |
| 03_Pokemon | EX Hidden Legends | https://holodex-prod-bucket.b-cdn.net/sets/ex5/logo.webp | 102 |
| 03_Pokemon | EX Holon Phantoms | https://holodex-prod-bucket.b-cdn.net/sets/ex13/logo.webp | 111 |
| 03_Pokemon | EX Legend Maker | https://holodex-prod-bucket.b-cdn.net/sets/ex12/logo.webp | 93 |
| 03_Pokemon | EX Power Keepers | https://holodex-prod-bucket.b-cdn.net/sets/ex16/logo.webp | 108 |
| 03_Pokemon | EX Ruby and Sapphire | https://holodex-prod-bucket.b-cdn.net/sets/ex1/logo.webp | 109 |
| 03_Pokemon | EX Sandstorm | https://holodex-prod-bucket.b-cdn.net/sets/ex3/logo.webp | 100 |
| 03_Pokemon | EX Team Magma vs Team Aqua | https://holodex-prod-bucket.b-cdn.net/sets/ex4/logo.webp | 97 |
| 03_Pokemon | EX Team Rocket Returns | https://holodex-prod-bucket.b-cdn.net/sets/ex7/logo.webp | 111 |
| 03_Pokemon | EX Unseen Forces | https://holodex-prod-bucket.b-cdn.net/sets/ex10/logo.webp | 145 |
| 03_Pokemon | Emerging Powers | https://holodex-prod-bucket.b-cdn.net/sets/bw2/logo.webp | 107 |
| 03_Pokemon | Expedition | https://holodex-prod-bucket.b-cdn.net/sets/ecard1/logo.webp | 165 |
| 03_Pokemon | First Partner Collection 2026 |  | 3 |
| 03_Pokemon | First Partner Pack |  | 24 |
| 03_Pokemon | Fossil | https://holodex-prod-bucket.b-cdn.net/sets/base3/logo.webp | 61 |
| 03_Pokemon | Generations | https://holodex-prod-bucket.b-cdn.net/sets/xy11/logo.webp | 101 |
| 03_Pokemon | Generations: Radiant Collection | https://holodex-prod-bucket.b-cdn.net/sets/xy12/logo.webp | 32 |
| 03_Pokemon | Great Encounters | https://holodex-prod-bucket.b-cdn.net/sets/dp4/logo.webp | 106 |
| 03_Pokemon | Gym Challenge | https://holodex-prod-bucket.b-cdn.net/sets/gym2/logo.webp | 132 |
| 03_Pokemon | Gym Heroes | https://holodex-prod-bucket.b-cdn.net/sets/gym1/logo.webp | 132 |
| 03_Pokemon | HGSS Promos | https://holodex-prod-bucket.b-cdn.net/sets/hgss1/logo.webp | 38 |
| 03_Pokemon | HeartGold SoulSilver | https://holodex-prod-bucket.b-cdn.net/sets/hgss2/logo.webp | 124 |
| 03_Pokemon | Hidden Fates | https://holodex-prod-bucket.b-cdn.net/sets/sm15/logo.webp | 72 |
| 03_Pokemon | Hidden Fates: Shiny Vault |  | 94 |
| 03_Pokemon | Jumbo Cards |  | 342 |
| 03_Pokemon | Jungle | https://holodex-prod-bucket.b-cdn.net/sets/base2/logo.webp | 64 |
| 03_Pokemon | Kalos Starter Set | https://holodex-prod-bucket.b-cdn.net/sets/kss/logo.webp | 44 |
| 03_Pokemon | Kids WB Promos |  | 5 |
| 03_Pokemon | League & Championship Cards |  | 514 |
| 03_Pokemon | Legendary Collection | https://holodex-prod-bucket.b-cdn.net/sets/lc/logo.webp | 110 |
| 03_Pokemon | Legendary Treasures | https://holodex-prod-bucket.b-cdn.net/sets/bw12/logo.webp | 116 |
| 03_Pokemon | Legendary Treasures: Radiant Collection | https://holodex-prod-bucket.b-cdn.net/sets/bw13/logo.webp | 25 |
| 03_Pokemon | Legends Awakened | https://holodex-prod-bucket.b-cdn.net/sets/dp6/logo.webp | 146 |
| 03_Pokemon | ME01: Mega Evolution | https://holodex-prod-bucket.b-cdn.net/sets/me1/logo.webp | 194 |
| 03_Pokemon | ME02: Phantasmal Flames | https://holodex-prod-bucket.b-cdn.net/sets/me2/logo.webp | 134 |
| 03_Pokemon | ME03: Perfect Order | https://holodex-prod-bucket.b-cdn.net/sets/me324587/logo.webp | 132 |
| 03_Pokemon | ME04: Chaos Rising | https://holodex-prod-bucket.b-cdn.net/sets/me424655/logo.webp | 127 |
| 03_Pokemon | ME05: Pitch Black | https://holodex-prod-bucket.b-cdn.net/sets/me0524688/logo.webp | 125 |
| 03_Pokemon | ME: 30th Celebration | https://holodex-prod-bucket.b-cdn.net/sets/me_30th24722/logo.webp | 40 |
| 03_Pokemon | ME: Ascended Heroes | https://holodex-prod-bucket.b-cdn.net/sets/me3/logo.webp | 550 |
| 03_Pokemon | ME: Mega Evolution Promo | https://holodex-prod-bucket.b-cdn.net/sets/mep/logo.webp | 120 |
| 03_Pokemon | MEE: Mega Evolution Energies |  | 8 |
| 03_Pokemon | Majestic Dawn | https://holodex-prod-bucket.b-cdn.net/sets/dp5/logo.webp | 100 |
| 03_Pokemon | McDonald's 25th Anniversary Promos | https://holodex-prod-bucket.b-cdn.net/sets/mc10/logo.webp | 25 |
| 03_Pokemon | McDonald's Promos 2014 | https://holodex-prod-bucket.b-cdn.net/sets/mc3/logo.webp | 12 |
| 03_Pokemon | McDonald's Promos 2015 | https://holodex-prod-bucket.b-cdn.net/sets/mc4/logo.webp | 12 |
| 03_Pokemon | McDonald's Promos 2016 | https://holodex-prod-bucket.b-cdn.net/sets/mc5/logo.webp | 12 |
| 03_Pokemon | McDonald's Promos 2017 | https://holodex-prod-bucket.b-cdn.net/sets/mc6/logo.webp | 12 |
| 03_Pokemon | McDonald's Promos 2018 | https://holodex-prod-bucket.b-cdn.net/sets/mc7/logo.webp | 12 |
| 03_Pokemon | McDonald's Promos 2019 | https://holodex-prod-bucket.b-cdn.net/sets/mc8/logo.webp | 7 |
| 03_Pokemon | Miscellaneous Cards & Products | https://holodex-prod-bucket.b-cdn.net/sets/mcap/logo.webp | 293 |
| 03_Pokemon | My First Battle | https://holodex-prod-bucket.b-cdn.net/sets/sv1723330/logo.webp | 48 |
| 03_Pokemon | Mysterious Treasures | https://holodex-prod-bucket.b-cdn.net/sets/dp2/logo.webp | 124 |
| 03_Pokemon | Neo Destiny | https://holodex-prod-bucket.b-cdn.net/sets/neo4/logo.webp | 113 |
| 03_Pokemon | Neo Discovery | https://holodex-prod-bucket.b-cdn.net/sets/neo2/logo.webp | 75 |
| 03_Pokemon | Neo Genesis | https://holodex-prod-bucket.b-cdn.net/sets/neo1/logo.webp | 111 |
| 03_Pokemon | Neo Revelation | https://holodex-prod-bucket.b-cdn.net/sets/neo3/logo.webp | 66 |
| 03_Pokemon | Next Destinies | https://holodex-prod-bucket.b-cdn.net/sets/bw4/logo.webp | 111 |
| 03_Pokemon | Nintendo Promos | https://holodex-prod-bucket.b-cdn.net/sets/ninpro/logo.webp | 95 |
| 03_Pokemon | Noble Victories | https://holodex-prod-bucket.b-cdn.net/sets/bw3/logo.webp | 110 |
| 03_Pokemon | POP Series 1 | https://holodex-prod-bucket.b-cdn.net/sets/pop1/logo.webp | 19 |
| 03_Pokemon | POP Series 2 | https://holodex-prod-bucket.b-cdn.net/sets/pop2/logo.webp | 18 |
| 03_Pokemon | POP Series 3 | https://holodex-prod-bucket.b-cdn.net/sets/pop3/logo.webp | 18 |
| 03_Pokemon | POP Series 4 | https://holodex-prod-bucket.b-cdn.net/sets/pop4/logo.webp | 17 |
| 03_Pokemon | POP Series 5 | https://holodex-prod-bucket.b-cdn.net/sets/pop5/logo.webp | 17 |
| 03_Pokemon | POP Series 6 | https://holodex-prod-bucket.b-cdn.net/sets/pop6/logo.webp | 18 |
| 03_Pokemon | POP Series 7 | https://holodex-prod-bucket.b-cdn.net/sets/pop7/logo.webp | 17 |
| 03_Pokemon | POP Series 8 | https://holodex-prod-bucket.b-cdn.net/sets/pop8/logo.webp | 18 |
| 03_Pokemon | POP Series 9 | https://holodex-prod-bucket.b-cdn.net/sets/pop9/logo.webp | 18 |
| 03_Pokemon | Pikachu World Collection Promos |  | 19 |
| 03_Pokemon | Plasma Blast | https://holodex-prod-bucket.b-cdn.net/sets/bw11/logo.webp | 109 |
| 03_Pokemon | Plasma Freeze | https://holodex-prod-bucket.b-cdn.net/sets/bw10/logo.webp | 123 |
| 03_Pokemon | Plasma Storm | https://holodex-prod-bucket.b-cdn.net/sets/bw9/logo.webp | 141 |
| 03_Pokemon | Platinum | https://holodex-prod-bucket.b-cdn.net/sets/pl1/logo.webp | 133 |
| 03_Pokemon | Player Placement Trainer Promos |  | 4 |
| 03_Pokemon | Pokemon GO | https://holodex-prod-bucket.b-cdn.net/sets/swsh14/logo.webp | 108 |
| 03_Pokemon | Prize Pack Series Cards | https://holodex-prod-bucket.b-cdn.net/sets/swsh1822880/logo.webp | 830 |
| 03_Pokemon | Professor Program Promos |  | 56 |
| 03_Pokemon | Rising Rivals | https://holodex-prod-bucket.b-cdn.net/sets/pl2/logo.webp | 120 |
| 03_Pokemon | Rumble | https://holodex-prod-bucket.b-cdn.net/sets/pl5/logo.webp | 16 |
| 03_Pokemon | SM - Burning Shadows | https://holodex-prod-bucket.b-cdn.net/sets/sm3/logo.webp | 188 |
| 03_Pokemon | SM - Celestial Storm | https://holodex-prod-bucket.b-cdn.net/sets/sm8/logo.webp | 199 |
| 03_Pokemon | SM - Cosmic Eclipse | https://holodex-prod-bucket.b-cdn.net/sets/sm16/logo.webp | 280 |
| 03_Pokemon | SM - Crimson Invasion | https://holodex-prod-bucket.b-cdn.net/sets/sm5/logo.webp | 140 |
| 03_Pokemon | SM - Forbidden Light | https://holodex-prod-bucket.b-cdn.net/sets/sm7/logo.webp | 158 |
| 03_Pokemon | SM - Guardians Rising | https://holodex-prod-bucket.b-cdn.net/sets/sm2/logo.webp | 202 |
| 03_Pokemon | SM - Lost Thunder | https://holodex-prod-bucket.b-cdn.net/sets/sm10/logo.webp | 251 |
| 03_Pokemon | SM - Team Up | https://holodex-prod-bucket.b-cdn.net/sets/sm11/logo.webp | 222 |
| 03_Pokemon | SM - Ultra Prism | https://holodex-prod-bucket.b-cdn.net/sets/sm6/logo.webp | 189 |
| 03_Pokemon | SM - Unbroken Bonds | https://holodex-prod-bucket.b-cdn.net/sets/sm13/logo.webp | 250 |
| 03_Pokemon | SM - Unified Minds | https://holodex-prod-bucket.b-cdn.net/sets/sm14/logo.webp | 274 |
| 03_Pokemon | SM Base Set | https://holodex-prod-bucket.b-cdn.net/sets/sm1/logo.webp | 184 |
| 03_Pokemon | SM Promos | https://holodex-prod-bucket.b-cdn.net/sets/smp/logo.webp | 333 |
| 03_Pokemon | SM Trainer Kit: Alolan Sandslash & Alolan Ninetales |  | 58 |
| 03_Pokemon | SM Trainer Kit: Lycanroc & Alolan Raichu |  | 56 |
| 03_Pokemon | SV01: Scarlet & Violet Base Set | https://holodex-prod-bucket.b-cdn.net/sets/sv1/logo.webp | 35 |
| 03_Pokemon | SV02: Paldea Evolved | https://holodex-prod-bucket.b-cdn.net/sets/sv2/logo.webp | 238 |
| 03_Pokemon | SV03: Obsidian Flames | https://holodex-prod-bucket.b-cdn.net/sets/sv3/logo.webp | 238 |
| 03_Pokemon | SV04: Paradox Rift | https://holodex-prod-bucket.b-cdn.net/sets/sv5/logo.webp | 226 |
| 03_Pokemon | SV05: Temporal Forces | https://holodex-prod-bucket.b-cdn.net/sets/sv7/logo.webp | 231 |
| 03_Pokemon | SV06: Twilight Masquerade | https://holodex-prod-bucket.b-cdn.net/sets/sv8/logo.webp | 238 |
| 03_Pokemon | SV07: Stellar Crown | https://holodex-prod-bucket.b-cdn.net/sets/sv10/logo.webp | 187 |
| 03_Pokemon | SV08: Surging Sparks | https://holodex-prod-bucket.b-cdn.net/sets/sv11/logo.webp | 262 |
| 03_Pokemon | SV09: Journey Together | https://holodex-prod-bucket.b-cdn.net/sets/sv13/logo.webp | 199 |
| 03_Pokemon | SV10: Destined Rivals | https://holodex-prod-bucket.b-cdn.net/sets/sv14/logo.webp | 256 |
| 03_Pokemon | SV: Black Bolt | https://holodex-prod-bucket.b-cdn.net/sets/sv15/logo.webp | 281 |
| 03_Pokemon | SV: Paldean Fates | https://holodex-prod-bucket.b-cdn.net/sets/sv6/logo.webp | 258 |
| 03_Pokemon | SV: Prismatic Evolutions | https://holodex-prod-bucket.b-cdn.net/sets/sv12/logo.webp | 255 |
| 03_Pokemon | SV: Shrouded Fable | https://holodex-prod-bucket.b-cdn.net/sets/sv9/logo.webp | 114 |
| 03_Pokemon | SV: White Flare | https://holodex-prod-bucket.b-cdn.net/sets/sv16/logo.webp | 330 |
| 03_Pokemon | SWSH01: Sword & Shield Base Set | https://holodex-prod-bucket.b-cdn.net/sets/swsh1/logo.webp | 221 |
| 03_Pokemon | SWSH02: Rebel Clash | https://holodex-prod-bucket.b-cdn.net/sets/swsh2/logo.webp | 224 |
| 03_Pokemon | SWSH03: Darkness Ablaze | https://holodex-prod-bucket.b-cdn.net/sets/swsh3/logo.webp | 216 |
| 03_Pokemon | SWSH04: Vivid Voltage | https://holodex-prod-bucket.b-cdn.net/sets/swsh5/logo.webp | 220 |
| 03_Pokemon | SWSH05: Battle Styles | https://holodex-prod-bucket.b-cdn.net/sets/swsh7/logo.webp | 202 |
| 03_Pokemon | SWSH06: Chilling Reign | https://holodex-prod-bucket.b-cdn.net/sets/swsh8/logo.webp | 248 |
| 03_Pokemon | SWSH07: Evolving Skies | https://holodex-prod-bucket.b-cdn.net/sets/swsh9/logo.webp | 255 |
| 03_Pokemon | SWSH08: Fusion Strike | https://holodex-prod-bucket.b-cdn.net/sets/swsh11/logo.webp | 296 |
| 03_Pokemon | SWSH09: Brilliant Stars | https://holodex-prod-bucket.b-cdn.net/sets/swsh12/logo.webp | 206 |
| 03_Pokemon | SWSH09: Brilliant Stars Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh12TG/logo.webp | 30 |
| 03_Pokemon | SWSH10: Astral Radiance | https://holodex-prod-bucket.b-cdn.net/sets/swsh13/logo.webp | 225 |
| 03_Pokemon | SWSH10: Astral Radiance Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh13TG/logo.webp | 30 |
| 03_Pokemon | SWSH11: Lost Origin | https://holodex-prod-bucket.b-cdn.net/sets/swsh15/logo.webp | 227 |
| 03_Pokemon | SWSH11: Lost Origin Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh15TG/logo.webp | 30 |
| 03_Pokemon | SWSH12: Silver Tempest | https://holodex-prod-bucket.b-cdn.net/sets/swsh16/logo.webp | 220 |
| 03_Pokemon | SWSH12: Silver Tempest Trainer Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh16TG/logo.webp | 30 |
| 03_Pokemon | SWSH: Crown Zenith | https://holodex-prod-bucket.b-cdn.net/sets/swsh17/logo.webp | 141 |
| 03_Pokemon | SWSH: Crown Zenith: Galarian Gallery | https://holodex-prod-bucket.b-cdn.net/sets/swsh17GG/logo.webp | 70 |
| 03_Pokemon | SWSH: Sword & Shield Promo Cards | https://holodex-prod-bucket.b-cdn.net/sets/swshp/logo.webp | 256 |
| 03_Pokemon | Secret Wonders | https://holodex-prod-bucket.b-cdn.net/sets/dp3/logo.webp | 132 |
| 03_Pokemon | Shining Fates | https://holodex-prod-bucket.b-cdn.net/sets/swsh6/logo.webp | 86 |
| 03_Pokemon | Shining Fates: Shiny Vault | https://holodex-prod-bucket.b-cdn.net/sets/swsh6/logo.webp | 122 |
| 03_Pokemon | Shining Legends | https://holodex-prod-bucket.b-cdn.net/sets/sm4/logo.webp | 87 |
| 03_Pokemon | Skyridge | https://holodex-prod-bucket.b-cdn.net/sets/ecard3/logo.webp | 181 |
| 03_Pokemon | Southern Islands | https://holodex-prod-bucket.b-cdn.net/sets/neosi/logo.webp | 18 |
| 03_Pokemon | Stormfront | https://holodex-prod-bucket.b-cdn.net/sets/dp7/logo.webp | 106 |
| 03_Pokemon | Supreme Victors | https://holodex-prod-bucket.b-cdn.net/sets/pl3/logo.webp | 153 |
| 03_Pokemon | Team Rocket | https://holodex-prod-bucket.b-cdn.net/sets/base5/logo.webp | 83 |
| 03_Pokemon | Trading Card Game Classic | https://holodex-prod-bucket.b-cdn.net/sets/cl/logo.webp | 102 |
| 03_Pokemon | Trick or Trade BOOster Bundle | https://holodex-prod-bucket.b-cdn.net/sets/tot1/logo.webp | 15 |
| 03_Pokemon | Trick or Trade BOOster Bundle 2023 | https://holodex-prod-bucket.b-cdn.net/sets/tot2/logo.webp | 30 |
| 03_Pokemon | Trick or Trade BOOster Bundle 2024 | https://holodex-prod-bucket.b-cdn.net/sets/tot3/logo.webp | 30 |
| 03_Pokemon | Triumphant | https://holodex-prod-bucket.b-cdn.net/sets/hgss5/logo.webp | 104 |
| 03_Pokemon | Undaunted | https://holodex-prod-bucket.b-cdn.net/sets/hgss4/logo.webp | 90 |
| 03_Pokemon | Unleashed | https://holodex-prod-bucket.b-cdn.net/sets/hgss3/logo.webp | 96 |
| 03_Pokemon | WoTC Promo | https://holodex-prod-bucket.b-cdn.net/sets/svp/logo.webp | 70 |
| 03_Pokemon | World Championship Decks |  | 1662 |
| 03_Pokemon | XY - Ancient Origins | https://holodex-prod-bucket.b-cdn.net/sets/xy8/logo.webp | 116 |
| 03_Pokemon | XY - BREAKpoint | https://holodex-prod-bucket.b-cdn.net/sets/xy10/logo.webp | 137 |
| 03_Pokemon | XY - BREAKthrough | https://holodex-prod-bucket.b-cdn.net/sets/xy9/logo.webp | 192 |
| 03_Pokemon | XY - Evolutions | https://holodex-prod-bucket.b-cdn.net/sets/xy15/logo.webp | 140 |
| 03_Pokemon | XY - Fates Collide | https://holodex-prod-bucket.b-cdn.net/sets/xy13/logo.webp | 142 |
| 03_Pokemon | XY - Flashfire | https://holodex-prod-bucket.b-cdn.net/sets/xy2/logo.webp | 126 |
| 03_Pokemon | XY - Furious Fists | https://holodex-prod-bucket.b-cdn.net/sets/xy3/logo.webp | 133 |
| 03_Pokemon | XY - Phantom Forces | https://holodex-prod-bucket.b-cdn.net/sets/xy4/logo.webp | 137 |
| 03_Pokemon | XY - Primal Clash | https://holodex-prod-bucket.b-cdn.net/sets/xy5/logo.webp | 178 |
| 03_Pokemon | XY - Roaring Skies | https://holodex-prod-bucket.b-cdn.net/sets/xy7/logo.webp | 126 |
| 03_Pokemon | XY - Steam Siege | https://holodex-prod-bucket.b-cdn.net/sets/xy14/logo.webp | 134 |
| 03_Pokemon | XY Base Set | https://holodex-prod-bucket.b-cdn.net/sets/xy1/logo.webp | 169 |
| 03_Pokemon | XY Promos | https://holodex-prod-bucket.b-cdn.net/sets/xyp/logo.webp | 260 |
| 03_Pokemon | XY Trainer Kit: Pikachu Libre & Suicune |  | 59 |
| 03_Pokemon | e-Reader Sample Cards | https://holodex-prod-bucket.b-cdn.net/sets/ecard1/logo.webp | 1 |

### 08_Heroclix（184 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 08_Heroclix | 15th Anniversary Elseworlds |  | 58 |
| 08_Heroclix | 15th Anniversary What If? |  | 58 |
| 08_Heroclix | 2099 |  | 7 |
| 08_Heroclix | Age of Ultron: Storyline Organized Play |  | 62 |
| 08_Heroclix | Amazing Spider-Man |  | 75 |
| 08_Heroclix | Arkham Asylum |  | 68 |
| 08_Heroclix | Armor Wars |  | 117 |
| 08_Heroclix | Assassin's Creed Brotherhood |  | 6 |
| 08_Heroclix | Assassin's Creed Revelations |  | 6 |
| 08_Heroclix | Avengers |  | 70 |
| 08_Heroclix | Avengers Assemble |  | 86 |
| 08_Heroclix | Avengers Infinity |  | 82 |
| 08_Heroclix | Avengers Movie |  | 54 |
| 08_Heroclix | Avengers Movie Starter |  | 6 |
| 08_Heroclix | Avengers Quick-Start Kit |  | 2 |
| 08_Heroclix | Avengers vs. X-Men |  | 26 |
| 08_Heroclix | Avengers/Defenders War |  | 74 |
| 08_Heroclix | Avengers: Age of Ultron |  | 24 |
| 08_Heroclix | Batman |  | 88 |
| 08_Heroclix | Batman Classic TV |  | 9 |
| 08_Heroclix | Batman The Animated Series |  | 88 |
| 08_Heroclix | Batman v Superman: Dawn of Justice |  | 12 |
| 08_Heroclix | Batman: Alpha |  | 31 |
| 08_Heroclix | Batman: Arkham Origins |  | 21 |
| 08_Heroclix | Batman: Arkham Origins Quick-Start Kit |  | 2 |
| 08_Heroclix | Batman: Gotham City Strategy Game |  | 5 |
| 08_Heroclix | Batman: Streets of Gotham |  | 60 |
| 08_Heroclix | BioShock Infinite |  | 20 |
| 08_Heroclix | Blackest Night |  | 7 |
| 08_Heroclix | Brave and the Bold |  | 63 |
| 08_Heroclix | Brightest Day |  | 7 |
| 08_Heroclix | Captain America |  | 79 |
| 08_Heroclix | Captain America - The Winter Soldier |  | 24 |
| 08_Heroclix | Captain America: Civil War |  | 10 |
| 08_Heroclix | Captain America: Civil War Starter |  | 6 |
| 08_Heroclix | Captain Marvel Movie |  | 22 |
| 08_Heroclix | Chaos War |  | 77 |
| 08_Heroclix | City of Heroes |  | 4 |
| 08_Heroclix | City of Villains |  | 4 |
| 08_Heroclix | Civil War: Storyline Organized Play |  | 55 |
| 08_Heroclix | Classics |  | 18 |
| 08_Heroclix | Clobberin Time |  | 116 |
| 08_Heroclix | Collateral Damage |  | 120 |
| 08_Heroclix | Cosmic Justice |  | 119 |
| 08_Heroclix | Crisis |  | 73 |
| 08_Heroclix | Critical Mass |  | 119 |
| 08_Heroclix | DC 75th Anniversary |  | 77 |
| 08_Heroclix | DC Heroclix 10th Anniversary |  | 24 |
| 08_Heroclix | DOTA 2 |  | 5 |
| 08_Heroclix | Danger Room |  | 6 |
| 08_Heroclix | Days of Future Past |  | 4 |
| 08_Heroclix | Deadpool |  | 101 |
| 08_Heroclix | Deadpool and X-Force |  | 82 |
| 08_Heroclix | Earth X |  | 78 |
| 08_Heroclix | Fantastic Forces |  | 105 |
| 08_Heroclix | Fast Forces: Avengers/Defenders War |  | 6 |
| 08_Heroclix | Fast Forces: Batman |  | 6 |
| 08_Heroclix | Fast Forces: Batman and His Greatest Foes |  | 7 |
| 08_Heroclix | Fast Forces: Batman v Superman: Dawn of Justice |  | 6 |
| 08_Heroclix | Fast Forces: Chaos War |  | 8 |
| 08_Heroclix | Fast Forces: Deadpool |  | 6 |
| 08_Heroclix | Fast Forces: Deadpool and X-Force |  | 12 |
| 08_Heroclix | Fast Forces: Galactic Guardians Annihilators |  | 6 |
| 08_Heroclix | Fast Forces: Giant-Size X-Men |  | 6 |
| 08_Heroclix | Fast Forces: Green Lantern |  | 6 |
| 08_Heroclix | Fast Forces: Hammer of Thor |  | 6 |
| 08_Heroclix | Fast Forces: Harley Quinn and the Gotham Girls |  | 6 |
| 08_Heroclix | Fast Forces: Incredible Hulk |  | 6 |
| 08_Heroclix | Fast Forces: Justice League |  | 6 |
| 08_Heroclix | Fast Forces: Original Avengers |  | 7 |
| 08_Heroclix | Fast Forces: Rogues |  | 6 |
| 08_Heroclix | Fast Forces: Secret Wars – Battleworld |  | 6 |
| 08_Heroclix | Fast Forces: Spider-Man and His Greatest Foes |  | 6 |
| 08_Heroclix | Fast Forces: Streets of Gotham |  | 6 |
| 08_Heroclix | Fast Forces: Superman |  | 6 |
| 08_Heroclix | Fast Forces: Teen Titans |  | 6 |
| 08_Heroclix | Fast Forces: Teenage Mutant Ninja Turtles: Heroes in a Half Shell |  | 6 |
| 08_Heroclix | Fast Forces: Teenage Mutant Ninja Turtles: Shredder's Return |  | 6 |
| 08_Heroclix | Fast Forces: The Crime Syndicate |  | 7 |
| 08_Heroclix | Fast Forces: The Inhumans |  | 6 |
| 08_Heroclix | Fast Forces: The Legion of Doom |  | 6 |
| 08_Heroclix | Fast Forces: Uncanny X-Men |  | 6 |
| 08_Heroclix | Fast Forces: War of the Light |  | 6 |
| 08_Heroclix | Fast Forces: Watchmen |  | 6 |
| 08_Heroclix | Fast Forces: World's Finest |  | 7 |
| 08_Heroclix | Fast Forces: X-Men Xavier's School |  | 6 |
| 08_Heroclix | Fear Itself |  | 42 |
| 08_Heroclix | Fellowship of the Ring |  | 33 |
| 08_Heroclix | Galactic Guardians |  | 71 |
| 08_Heroclix | Gears of War |  | 10 |
| 08_Heroclix | Giant-Size X-Men |  | 79 |
| 08_Heroclix | Giants |  | 7 |
| 08_Heroclix | Green Lantern Corps |  | 7 |
| 08_Heroclix | Green Lantern: Gravity Feed |  | 10 |
| 08_Heroclix | Guardians of the Galaxy |  | 97 |
| 08_Heroclix | Guardians of the Galaxy Movie |  | 24 |
| 08_Heroclix | Guardians of the Galaxy Movie 2 |  | 16 |
| 08_Heroclix | Halo |  | 45 |
| 08_Heroclix | Hammer of Thor |  | 70 |
| 08_Heroclix | Harley Quinn and the Gotham Girls |  | 74 |
| 08_Heroclix | Hellboy and the B.P.R.D. |  | 7 |
| 08_Heroclix | Hypertime |  | 143 |
| 08_Heroclix | Icons |  | 63 |
| 08_Heroclix | Incredible Hulk |  | 66 |
| 08_Heroclix | Indy |  | 137 |
| 08_Heroclix | Infinity Gauntlet |  | 10 |
| 08_Heroclix | Infinity challenge |  | 176 |
| 08_Heroclix | Invincible |  | 7 |
| 08_Heroclix | Iron Maiden |  | 9 |
| 08_Heroclix | Iron Man 3 |  | 25 |
| 08_Heroclix | Jonah Hex |  | 3 |
| 08_Heroclix | Justice League |  | 70 |
| 08_Heroclix | Justice League 52 |  | 21 |
| 08_Heroclix | Justice League Strategy Game |  | 5 |
| 08_Heroclix | Justice League Trinity War |  | 87 |
| 08_Heroclix | Kick Ass 2 |  | 18 |
| 08_Heroclix | Large Promo Figures |  | 1 |
| 08_Heroclix | Legacy |  | 114 |
| 08_Heroclix | Legion of Super Heroes |  | 8 |
| 08_Heroclix | Lord of the Rings |  | 34 |
| 08_Heroclix | Lord of the Rings: The Two Towers |  | 38 |
| 08_Heroclix | MVID Promos |  | 6 |
| 08_Heroclix | Mage Knight: Resurrection |  | 31 |
| 08_Heroclix | Man of Steel |  | 23 |
| 08_Heroclix | Marvel Heroclix 10th Anniversary |  | 24 |
| 08_Heroclix | Mutant Mayhem |  | 119 |
| 08_Heroclix | Mutations and Monsters |  | 67 |
| 08_Heroclix | Nick Fury, Agent of S.H.I.E.L.D. |  | 96 |
| 08_Heroclix | No Man's Land |  | 8 |
| 08_Heroclix | Origin |  | 114 |
| 08_Heroclix | Pacific Rim |  | 10 |
| 08_Heroclix | SDCC Combo-Pack |  | 4 |
| 08_Heroclix | Secret Invasion |  | 80 |
| 08_Heroclix | Secret Wars – Battleworld |  | 71 |
| 08_Heroclix | Sinister |  | 115 |
| 08_Heroclix | Star Trek Away Team: The Original Series |  | 56 |
| 08_Heroclix | Star Trek: Mini-Game |  | 2 |
| 08_Heroclix | Star Trek: Tactics |  | 33 |
| 08_Heroclix | Star Trek: Tactics Away Team |  | 7 |
| 08_Heroclix | Star Trek: Tactics II |  | 36 |
| 08_Heroclix | Star Trek: Tactics III |  | 15 |
| 08_Heroclix | Star Trek: Tactics IV |  | 32 |
| 08_Heroclix | Street Fighter |  | 33 |
| 08_Heroclix | Superior Foes of Spider-Man |  | 140 |
| 08_Heroclix | Superman |  | 64 |
| 08_Heroclix | Superman Quick-Start Kit |  | 2 |
| 08_Heroclix | Superman and the Legion of Super-Heroes |  | 84 |
| 08_Heroclix | Superman/Wonder Woman |  | 77 |
| 08_Heroclix | Supernova |  | 121 |
| 08_Heroclix | TabApp |  | 15 |
| 08_Heroclix | TabApp Elite |  | 8 |
| 08_Heroclix | Teen Titans |  | 101 |
| 08_Heroclix | Teenage Mutant Ninja Turtles |  | 39 |
| 08_Heroclix | Teenage Mutant Ninja Turtles: Heroes in a Half Shell |  | 35 |
| 08_Heroclix | Teenage Mutant Ninja Turtles: Shredder's Return |  | 35 |
| 08_Heroclix | Teenage Mutant Ninja Turtles: Unplugged |  | 38 |
| 08_Heroclix | The Dark Knight Rises |  | 46 |
| 08_Heroclix | The Flash |  | 79 |
| 08_Heroclix | The Hobbit: An Unexpected Journey |  | 38 |
| 08_Heroclix | The Hobbit: The Battle of the Five Armies |  | 12 |
| 08_Heroclix | The Invincible Iron Man |  | 74 |
| 08_Heroclix | The Joker's Wild! |  | 143 |
| 08_Heroclix | The Lone Ranger |  | 4 |
| 08_Heroclix | The Mighty Thor |  | 112 |
| 08_Heroclix | Thor: Ragnarok |  | 16 |
| 08_Heroclix | Thor: The Dark World |  | 26 |
| 08_Heroclix | Ultimates |  | 118 |
| 08_Heroclix | Uncanny X-Men |  | 71 |
| 08_Heroclix | Undead |  | 19 |
| 08_Heroclix | Universe |  | 126 |
| 08_Heroclix | Unleashed |  | 119 |
| 08_Heroclix | War of Light |  | 113 |
| 08_Heroclix | Watchmen |  | 26 |
| 08_Heroclix | Web of Spider-Man |  | 70 |
| 08_Heroclix | WizKids |  | 34 |
| 08_Heroclix | Wolverine and the X-Men |  | 103 |
| 08_Heroclix | Wonder Woman |  | 15 |
| 08_Heroclix | World's Finest |  | 100 |
| 08_Heroclix | X-Men Days of Future Past |  | 26 |
| 08_Heroclix | X-Men Xavier's School |  | 98 |
| 08_Heroclix | Xplosion |  | 116 |
| 08_Heroclix | Yu-Gi-Oh! HeroClix: Series One |  | 62 |
| 08_Heroclix | Yu-Gi-Oh! HeroClix: Series Three |  | 20 |
| 08_Heroclix | Yu-Gi-Oh! HeroClix: Series Two |  | 21 |

### 13_WoW（41 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 13_WoW | Arena Grand Melee |  | 11 |
| 13_WoW | Assault on Icecrown Citadel |  | 30 |
| 13_WoW | Blood of Gladiators |  | 206 |
| 13_WoW | BoJ |  | 1 |
| 13_WoW | CAT Promos |  | 2 |
| 13_WoW | CRP |  | 35 |
| 13_WoW | Class Starter Decks |  | 8 |
| 13_WoW | Dark Portal |  | 298 |
| 13_WoW | Darkmoon Faire Collector's Set |  | 5 |
| 13_WoW | Death Knight Starter |  | 27 |
| 13_WoW | Drums of War |  | 263 |
| 13_WoW | Drums of War Starter |  | 8 |
| 13_WoW | Dungeon Treasure |  | 1 |
| 13_WoW | Feast of Winter Veil |  | 10 |
| 13_WoW | Fields of Honor |  | 206 |
| 13_WoW | Fires of Outland |  | 235 |
| 13_WoW | Giveaway |  | 1 |
| 13_WoW | Heroes of Azeroth |  | 344 |
| 13_WoW | Icecrown |  | 212 |
| 13_WoW | Loot Cards |  | 33 |
| 13_WoW | Magtheridon's Lair |  | 41 |
| 13_WoW | Magtheridon's Lair Treasure |  | 20 |
| 13_WoW | March of the Legion |  | 314 |
| 13_WoW | Molten Core |  | 62 |
| 13_WoW | Molten Core Treasure |  | 30 |
| 13_WoW | Naxxramas Treasure |  | 30 |
| 13_WoW | Onyxia's Lair |  | 63 |
| 13_WoW | Onyxia's Lair Treasure |  | 33 |
| 13_WoW | Scourgewar |  | 264 |
| 13_WoW | Servants of the Betrayer |  | 259 |
| 13_WoW | TBC Promo |  | 3 |
| 13_WoW | The Black Temple |  | 23 |
| 13_WoW | The Black Temple Treasure |  | 12 |
| 13_WoW | The Hunt for Illidan |  | 250 |
| 13_WoW | Throne of the Tides |  | 258 |
| 13_WoW | Timewalkers Heroes |  | 60 |
| 13_WoW | Twilight of the Dragons |  | 219 |
| 13_WoW | War of the Elements |  | 219 |
| 13_WoW | Worldbreaker |  | 270 |
| 13_WoW | Wrath of the Lich King Promo |  | 2 |
| 13_WoW | Wrathgate |  | 219 |

### 16_Cardfight_Vanguard（260 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 16_Cardfight_Vanguard | BT01: Descent of the King of Knights |  | 92 |
| 16_Cardfight_Vanguard | BT02: Onslaught of Dragon Souls |  | 92 |
| 16_Cardfight_Vanguard | BT03: Demonic Lord Invasion |  | 94 |
| 16_Cardfight_Vanguard | BT04: Eclipse of Illusionary Shadows |  | 94 |
| 16_Cardfight_Vanguard | BT05: Awakening of Twin Blades |  | 94 |
| 16_Cardfight_Vanguard | BT06: Breaker of Limits |  | 125 |
| 16_Cardfight_Vanguard | BT07: Rampage of the Beast King |  | 114 |
| 16_Cardfight_Vanguard | BT08: Blue Storm Armada |  | 114 |
| 16_Cardfight_Vanguard | BT10: Triumphant Return of the King of Knights |  | 113 |
| 16_Cardfight_Vanguard | BT11: Seal Dragons Unleashed |  | 114 |
| 16_Cardfight_Vanguard | BT12: Binding Force of the Black Rings |  | 113 |
| 16_Cardfight_Vanguard | BT13: Catastrophic Outbreak |  | 114 |
| 16_Cardfight_Vanguard | BT14: Brilliant Strike |  | 114 |
| 16_Cardfight_Vanguard | BT15: Infinite Rebirth |  | 114 |
| 16_Cardfight_Vanguard | BT16: Legion of Dragons and Blades ver.E |  | 100 |
| 16_Cardfight_Vanguard | BT17: Blazing Perdition ver.E |  | 162 |
| 16_Cardfight_Vanguard | Bushiroad Event Cards |  | 130 |
| 16_Cardfight_Vanguard | Clan Cards |  | 14 |
| 16_Cardfight_Vanguard | D Promo Cards |  | 969 |
| 16_Cardfight_Vanguard | D-BT01: Genesis of the Five Greats |  | 213 |
| 16_Cardfight_Vanguard | D-BT02: A Brush with the Legends |  | 219 |
| 16_Cardfight_Vanguard | D-BT03: Advance of Intertwined Stars |  | 212 |
| 16_Cardfight_Vanguard | D-BT04: Awakening of Chakrabarthi |  | 229 |
| 16_Cardfight_Vanguard | D-BT05: Triumphant Return of the Brave Heroes |  | 213 |
| 16_Cardfight_Vanguard | D-BT06: Blazing Dragon Reborn |  | 160 |
| 16_Cardfight_Vanguard | D-BT07: Raging Flames Against Emerald Storm |  | 158 |
| 16_Cardfight_Vanguard | D-BT08: Minerva Rising |  | 152 |
| 16_Cardfight_Vanguard | D-BT09: Dragontree Invasion |  | 169 |
| 16_Cardfight_Vanguard | D-BT10: Dragon Masquerade |  | 164 |
| 16_Cardfight_Vanguard | D-BT11: Clash of the Heroes |  | 235 |
| 16_Cardfight_Vanguard | D-BT12: Evenfall Onslaught |  | 160 |
| 16_Cardfight_Vanguard | D-BT13: Flight of Chakrabarthi |  | 180 |
| 16_Cardfight_Vanguard | D-CS01: Deluxe Collector's Set 01: Vanguard Deluxe |  | 8 |
| 16_Cardfight_Vanguard | D-LBT01: Lyrical Melody |  | 230 |
| 16_Cardfight_Vanguard | D-LBT02: Lyrical Monasterio ~It's a New School Term!~ |  | 172 |
| 16_Cardfight_Vanguard | D-LBT04: Lyrical Monasterio ~Trick or Trick!~ |  | 161 |
| 16_Cardfight_Vanguard | D-LTD01: Ahoy! Lyrical Monasterio! |  | 27 |
| 16_Cardfight_Vanguard | D-PS01: P Clan Collection 2022 |  | 144 |
| 16_Cardfight_Vanguard | D-PV01: History Collection |  | 367 |
| 16_Cardfight_Vanguard | D-SD01: Yu-yu Kondo -Holy Dragon- |  | 16 |
| 16_Cardfight_Vanguard | D-SD02: Danji Momoyama -Tyrant Tiger- |  | 16 |
| 16_Cardfight_Vanguard | D-SD03: Tohya Ebata -Apex Ruler- |  | 16 |
| 16_Cardfight_Vanguard | D-SD04: Megumi Okura -Sylvan King- |  | 16 |
| 16_Cardfight_Vanguard | D-SD05: Tomari Seto -Aurora Valkyrie- |  | 16 |
| 16_Cardfight_Vanguard | D-SD06: Mirei Minae -Sealed Blaze Maiden- |  | 16 |
| 16_Cardfight_Vanguard | D-SS01: Festival Collection 2021 |  | 85 |
| 16_Cardfight_Vanguard | D-SS02: Festival Collection 2022 |  | 57 |
| 16_Cardfight_Vanguard | D-SS03: Stride Deckset -Chronojet- |  | 30 |
| 16_Cardfight_Vanguard | D-SS04: Stride Deckset - Messiah |  | 31 |
| 16_Cardfight_Vanguard | D-SS05: Festival Booster 2023 |  | 125 |
| 16_Cardfight_Vanguard | D-SS06: Stand Up Deckset "Gramgrace" |  | 23 |
| 16_Cardfight_Vanguard | D-SS07: Stand Up Deckset "Favrneel" |  | 23 |
| 16_Cardfight_Vanguard | D-SS08: Stand Up Deckset "Orfist" |  | 24 |
| 16_Cardfight_Vanguard | D-SS09: Special Series 09 Stride Deckset -Shiranui- |  | 31 |
| 16_Cardfight_Vanguard | D-SS10: Special Series 10 Stride Deckset -Luard- |  | 31 |
| 16_Cardfight_Vanguard | D-SS11: Malevolent Masques Supply Gift Set |  | 8 |
| 16_Cardfight_Vanguard | D-SS12: Triple Drive Booster |  | 183 |
| 16_Cardfight_Vanguard | D-TB01: Touken Ranbu -ONLINE- 2021 |  | 209 |
| 16_Cardfight_Vanguard | D-TB02: Record of Ragnarok |  | 167 |
| 16_Cardfight_Vanguard | D-TB03: Shaman King |  | 363 |
| 16_Cardfight_Vanguard | D-TB04: Touken Ranbu ONLINE 2023 |  | 205 |
| 16_Cardfight_Vanguard | D-TD01: Urara Haneyama -Bandmaster of Blossoming Bonds- |  | 29 |
| 16_Cardfight_Vanguard | D-TD02: Michiru Hazama -Demonic Jewel Dragon of the Four Flames- |  | 29 |
| 16_Cardfight_Vanguard | D-TD03: Raika Koshiba -Skyfall Executors- |  | 29 |
| 16_Cardfight_Vanguard | D-TTD01: Touken Ranbu -ONLINE- 2021 |  | 34 |
| 16_Cardfight_Vanguard | D-TTD02: Record of Ragnarok |  | 34 |
| 16_Cardfight_Vanguard | D-TTD03: Shaman King |  | 35 |
| 16_Cardfight_Vanguard | D-VS01: V Clan Collection Vol.1 |  | 100 |
| 16_Cardfight_Vanguard | D-VS02: V Clan Collection Vol.2 |  | 95 |
| 16_Cardfight_Vanguard | D-VS03: V Clan Collection Vol.3 |  | 99 |
| 16_Cardfight_Vanguard | D-VS04: V Clan Collection Vol.4 |  | 99 |
| 16_Cardfight_Vanguard | D-VS05: V Clan Collection Vol.5 |  | 99 |
| 16_Cardfight_Vanguard | DZ-BT01: Fated Clash |  | 311 |
| 16_Cardfight_Vanguard | DZ-BT02: Illusionless Strife |  | 264 |
| 16_Cardfight_Vanguard | DZ-BT03: Dimensional Transcendence |  | 339 |
| 16_Cardfight_Vanguard | DZ-BT04: Destined Showdown |  | 197 |
| 16_Cardfight_Vanguard | DZ-BT05: Omniscient Awakening |  | 243 |
| 16_Cardfight_Vanguard | DZ-BT06: Generation Dragenesis |  | 262 |
| 16_Cardfight_Vanguard | DZ-BT07: Moon Fangs & Cerulean Blaze |  | 199 |
| 16_Cardfight_Vanguard | DZ-BT08: Knights 0f Rebirth |  | 268 |
| 16_Cardfight_Vanguard | DZ-BT09: Super Brave Detonation |  | 280 |
| 16_Cardfight_Vanguard | DZ-BT10: Dragonsoul Resonance |  | 237 |
| 16_Cardfight_Vanguard | DZ-BT12: Chasm of Lost Souls |  | 337 |
| 16_Cardfight_Vanguard | DZ-BT13: Parallactic Clash |  | 325 |
| 16_Cardfight_Vanguard | DZ-BT14: Envoys of the Crimson Moon |  | 252 |
| 16_Cardfight_Vanguard | DZ-LBT01: Lyrical Monasterio Sparkling Stars! |  | 100 |
| 16_Cardfight_Vanguard | DZ-LBT02: Lyrical Monasterio Season of Wonders |  | 212 |
| 16_Cardfight_Vanguard | DZ-PS01: Premium Deckset “Jewel Knight” |  | 37 |
| 16_Cardfight_Vanguard | DZ-PS02: Premium Deckset “Revenger” |  | 37 |
| 16_Cardfight_Vanguard | DZ-PS03: Premium Deckset “Musketeer” |  | 38 |
| 16_Cardfight_Vanguard | DZ-SS01: Festival Booster 2024 |  | 125 |
| 16_Cardfight_Vanguard | DZ-SS02: Stride Deckset -Harri- |  | 31 |
| 16_Cardfight_Vanguard | DZ-SS03: Stride Deckset -Nightrose- |  | 31 |
| 16_Cardfight_Vanguard | DZ-SS04: Special Series Stardust Blade |  | 25 |
| 16_Cardfight_Vanguard | DZ-SS05: CoroCoro Start Deck Pack |  | 180 |
| 16_Cardfight_Vanguard | DZ-SS06: Master Deckset -Urara Haneyama- |  | 21 |
| 16_Cardfight_Vanguard | DZ-SS07: Master Deckset -Michiru Hazama- |  | 20 |
| 16_Cardfight_Vanguard | DZ-SS08: Festival Booster 2025 |  | 124 |
| 16_Cardfight_Vanguard | DZ-SS09: Zero Tendo Start Deck |  | 41 |
| 16_Cardfight_Vanguard | DZ-SS10: Shiki Otei Start Deck |  | 45 |
| 16_Cardfight_Vanguard | DZ-SS11: Master Deckset -Hikari Myodo- |  | 20 |
| 16_Cardfight_Vanguard | DZ-SS12: Master Deckset -Erika Myojo- |  | 20 |
| 16_Cardfight_Vanguard | DZ-SS13: Blaster Blade Start Deck |  | 40 |
| 16_Cardfight_Vanguard | DZ-SS14: Dragonic Overlord Start Deck |  | 40 |
| 16_Cardfight_Vanguard | DZ-SS15: The Legendary Vanguards |  | 263 |
| 16_Cardfight_Vanguard | DZ-TB01: Future Card Buddyfight |  | 259 |
| 16_Cardfight_Vanguard | DZ-TB02: Touken Ranbu Online |  | 356 |
| 16_Cardfight_Vanguard | DZ-TD01: Start Up Trial Deck "Dragon Empire" |  | 39 |
| 16_Cardfight_Vanguard | DZ-TD02: Start Up Trial Deck "Dark States" |  | 39 |
| 16_Cardfight_Vanguard | DZ-TD03: Start Up Trial Deck "Brandt Gate" |  | 39 |
| 16_Cardfight_Vanguard | DZ-TD04: Start Up Trial Deck "Keter Sanctuary" |  | 39 |
| 16_Cardfight_Vanguard | DZ-TD05: Start Up Trial Deck "Stoicheia" |  | 39 |
| 16_Cardfight_Vanguard | DZ-TD06: Start Up Trial Deck "Lyrical Monasterio" |  | 39 |
| 16_Cardfight_Vanguard | EB01 - Comic Style Vol. 1 |  | 36 |
| 16_Cardfight_Vanguard | EB02 - Banquet of Divas |  | 37 |
| 16_Cardfight_Vanguard | EB03 - Cavalry of Black Steel |  | 53 |
| 16_Cardfight_Vanguard | EB04 - Infinite Phantom Legion |  | 37 |
| 16_Cardfight_Vanguard | EB05 - Celestial Valkyries |  | 37 |
| 16_Cardfight_Vanguard | EB06 - Dazzling Divas |  | 41 |
| 16_Cardfight_Vanguard | EB07 - Mystical Magus |  | 39 |
| 16_Cardfight_Vanguard | EB08 - Champions of the Cosmos |  | 39 |
| 16_Cardfight_Vanguard | EB09 - Divine Dragon Progression |  | 39 |
| 16_Cardfight_Vanguard | EB10 - Divas Duet |  | 86 |
| 16_Cardfight_Vanguard | EB11 - Requiem at Dusk |  | 43 |
| 16_Cardfight_Vanguard | EB12 - Waltz of the Goddess |  | 43 |
| 16_Cardfight_Vanguard | FC02: Fighter's Collection 2014 |  | 37 |
| 16_Cardfight_Vanguard | G-BT01: Generation Stride |  | 114 |
| 16_Cardfight_Vanguard | G-BT03: Sovereign Star Dragon |  | 116 |
| 16_Cardfight_Vanguard | G-BT04: Soul Strike Against The Supreme |  | 122 |
| 16_Cardfight_Vanguard | G-BT06: Transcension of Blade & Blossom |  | 121 |
| 16_Cardfight_Vanguard | G-BT07: Glorious Bravery of Radiant Sword |  | 141 |
| 16_Cardfight_Vanguard | G-BT08: Absolute Judgment |  | 143 |
| 16_Cardfight_Vanguard | G-BT09: Divine Dragon Caper |  | 137 |
| 16_Cardfight_Vanguard | G-BT10: Raging Clash of the Blade Fangs |  | 131 |
| 16_Cardfight_Vanguard | G-BT11: Demonic Advent |  | 145 |
| 16_Cardfight_Vanguard | G-BT12: Dragon King's Awakening |  | 119 |
| 16_Cardfight_Vanguard | G-BT13: Ultimate Stride |  | 126 |
| 16_Cardfight_Vanguard | G-BT14: Divine Dragon Apocrypha |  | 121 |
| 16_Cardfight_Vanguard | G-CB01: Academy of Divas |  | 75 |
| 16_Cardfight_Vanguard | G-CB02: Commander of the Incessant Waves |  | 46 |
| 16_Cardfight_Vanguard | G-CB03: Blessing of Divas |  | 77 |
| 16_Cardfight_Vanguard | G-CB04: Gear of Fate |  | 63 |
| 16_Cardfight_Vanguard | G-CB05: Prismatic Divas |  | 126 |
| 16_Cardfight_Vanguard | G-CB06: Rondeau of Chaos and Salvation |  | 59 |
| 16_Cardfight_Vanguard | G-CB07: Divas' Festa |  | 67 |
| 16_Cardfight_Vanguard | G-CHB01: TRY3 NEXT |  | 99 |
| 16_Cardfight_Vanguard | G-CHB02: We ARE!!! Trinity Dragon |  | 109 |
| 16_Cardfight_Vanguard | G-CHB03: Rummy Labyrinth Under the Moonlight |  | 78 |
| 16_Cardfight_Vanguard | G-CMB01: Vanguard & Deletor |  | 51 |
| 16_Cardfight_Vanguard | G-EB01: Cosmic Roar |  | 39 |
| 16_Cardfight_Vanguard | G-EB02: The AWAKENING ZOO |  | 91 |
| 16_Cardfight_Vanguard | G-EB03: The GALAXY STAR GATE |  | 91 |
| 16_Cardfight_Vanguard | G-FC02: Fighter's Collection 2015 Winter |  | 48 |
| 16_Cardfight_Vanguard | G-FC03: Fighter's Collection 2016 |  | 51 |
| 16_Cardfight_Vanguard | G-FC04: Fighters Collection 2017 |  | 75 |
| 16_Cardfight_Vanguard | G-Legend Deck Vol.1: The Dark |  | 30 |
| 16_Cardfight_Vanguard | G-Legend Deck Vol.2: The Overlord Blaze |  | 32 |
| 16_Cardfight_Vanguard | G-Legend Deck Vol.3: The Blaster |  | 35 |
| 16_Cardfight_Vanguard | G-RC01: Revival Collection |  | 62 |
| 16_Cardfight_Vanguard | G-RC02: Revival Collection |  | 79 |
| 16_Cardfight_Vanguard | G-Start Deck 1: Odyssey of the Interspatial Dragon |  | 18 |
| 16_Cardfight_Vanguard | G-Start Deck 2: Knight of the Sun |  | 21 |
| 16_Cardfight_Vanguard | G-TB01: Touken Ranbu (ONLINE) |  | 47 |
| 16_Cardfight_Vanguard | G-TB02: Touken Ranbu (ONLINE) |  | 51 |
| 16_Cardfight_Vanguard | G-TCB01: The RECKLESS RAMPAGE |  | 87 |
| 16_Cardfight_Vanguard | G-TCB02: The GENIUS STRATEGY |  | 90 |
| 16_Cardfight_Vanguard | G-TD01: Awakening Of The Interdimensional Dragon |  | 24 |
| 16_Cardfight_Vanguard | G-TD02: Divine Swordsman of the Shiny Star |  | 24 |
| 16_Cardfight_Vanguard | G-TD03: Flower Maiden of Purity |  | 24 |
| 16_Cardfight_Vanguard | G-TD04: Blue Cavalry of the Divine Marine Spirits |  | 23 |
| 16_Cardfight_Vanguard | G-TD05: Fateful Star Messiah |  | 24 |
| 16_Cardfight_Vanguard | G-TD06: Rallying Call of the Interspectral Dragon |  | 23 |
| 16_Cardfight_Vanguard | G-TD07: Illusionist of the Crescent Moon |  | 24 |
| 16_Cardfight_Vanguard | G-TD08: Vampire Princess of the Nether Hour |  | 24 |
| 16_Cardfight_Vanguard | G-TD09: True Zodiac Time Beasts |  | 33 |
| 16_Cardfight_Vanguard | G-TD10: Ritual of Dragon Sorcery |  | 23 |
| 16_Cardfight_Vanguard | G-TD11: Divine Knight of Heavenly Decree |  | 23 |
| 16_Cardfight_Vanguard | G-TD12: Flower Princess of Abundant Blooming |  | 23 |
| 16_Cardfight_Vanguard | G-TD13: Evil Eye Sovereign |  | 23 |
| 16_Cardfight_Vanguard | G-TD14: Debut of the Divas |  | 24 |
| 16_Cardfight_Vanguard | G-TD15: Messiah Dragon of Rebirth |  | 22 |
| 16_Cardfight_Vanguard | G-TTD01: Touken Ranbu (ONLINE) |  | 20 |
| 16_Cardfight_Vanguard | Gift Markers |  | 221 |
| 16_Cardfight_Vanguard | Kero Kero Ace Pack |  | 16 |
| 16_Cardfight_Vanguard | Mega Trial Deck 1: Rise to Royalty |  | 18 |
| 16_Cardfight_Vanguard | Moonlit Dragonfang |  | 121 |
| 16_Cardfight_Vanguard | Promo Cards |  | 256 |
| 16_Cardfight_Vanguard | Trial Deck 10: Purgatory Revenger |  | 18 |
| 16_Cardfight_Vanguard | Trial Deck 11: Star-vader Invasion |  | 18 |
| 16_Cardfight_Vanguard | Trial Deck 12: Dimensional Brave Kaiser |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 13: Successor of the Sacred Regalia |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 14: Seeker of Hope |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 16: Divine Judgement of the Bluish Flames |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 17: Will of the Locked Dragon |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 1: Blaster Blade |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 2: Dragonic Overlord |  | 18 |
| 16_Cardfight_Vanguard | Trial Deck 3: Golden Mechanical Soldier |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 4: Maiden Princess of the Cherry Blossom |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 5: Slash of Silver Wolf |  | 19 |
| 16_Cardfight_Vanguard | Trial Deck 6: Resonance of Thunder Dragon |  | 19 |
| 16_Cardfight_Vanguard | Trial Deck 7: Descendants of the Marine Emperor |  | 19 |
| 16_Cardfight_Vanguard | Trial Deck 8: Liberator of the Sanctuary |  | 17 |
| 16_Cardfight_Vanguard | Trial Deck 9: Eradicator of the Empire |  | 18 |
| 16_Cardfight_Vanguard | V Promo Cards |  | 344 |
| 16_Cardfight_Vanguard | V Start Deck 01: 2018 Free Experience Deck "Royal Paladin" |  | 14 |
| 16_Cardfight_Vanguard | V Start Deck 02: 2018 Free Experience Deck "Kagero" |  | 14 |
| 16_Cardfight_Vanguard | V Start Deck 03: 2020 Demo Deck "Gear Chronicle" |  | 14 |
| 16_Cardfight_Vanguard | V-BT01: Unite! Team Q4 |  | 93 |
| 16_Cardfight_Vanguard | V-BT02 : Strongest! Team AL4 |  | 86 |
| 16_Cardfight_Vanguard | V-BT03: Miyaji Academy CF Club |  | 98 |
| 16_Cardfight_Vanguard | V-BT04: Vilest! Deletor |  | 107 |
| 16_Cardfight_Vanguard | V-BT05: Aerial Steed Liberation |  | 99 |
| 16_Cardfight_Vanguard | V-BT06: Phantasmal Steed Restoration |  | 103 |
| 16_Cardfight_Vanguard | V-BT07: Infinideity Cradle |  | 94 |
| 16_Cardfight_Vanguard | V-BT08: Silverdust Blaze |  | 123 |
| 16_Cardfight_Vanguard | V-BT09: Butterfly d'Moonlight |  | 131 |
| 16_Cardfight_Vanguard | V-BT10: Phantom Dragon Aeon |  | 132 |
| 16_Cardfight_Vanguard | V-BT11: Storm of the Blue Cavalry |  | 126 |
| 16_Cardfight_Vanguard | V-BT12: Divine Lightning Radiance |  | 134 |
| 16_Cardfight_Vanguard | V-CS01: Q4 vs. AL4 |  | 16 |
| 16_Cardfight_Vanguard | V-CS02: Memoir of Vanguard Koshien |  | 16 |
| 16_Cardfight_Vanguard | V-EB01: The Destructive Roar |  | 72 |
| 16_Cardfight_Vanguard | V-EB02: Champions of the Asia Circuit |  | 64 |
| 16_Cardfight_Vanguard | V-EB03: ULTRARARE MIRACLE COLLECTION |  | 81 |
| 16_Cardfight_Vanguard | V-EB04: The Answer of Truth |  | 74 |
| 16_Cardfight_Vanguard | V-EB05: Primary Melody |  | 87 |
| 16_Cardfight_Vanguard | V-EB06: Light of Salvation, Logic of Destruction |  | 61 |
| 16_Cardfight_Vanguard | V-EB07: The Heroic Evolution |  | 84 |
| 16_Cardfight_Vanguard | V-EB08: My Glorious Justice |  | 76 |
| 16_Cardfight_Vanguard | V-EB09: The Raging Tactics |  | 78 |
| 16_Cardfight_Vanguard | V-EB10: The Mysterious Fortune |  | 86 |
| 16_Cardfight_Vanguard | V-EB11: Crystal Melody |  | 61 |
| 16_Cardfight_Vanguard | V-EB12: Team Dragon's Vanity |  | 78 |
| 16_Cardfight_Vanguard | V-EB13: The Astral Force |  | 77 |
| 16_Cardfight_Vanguard | V-EB14: The Next Stage |  | 94 |
| 16_Cardfight_Vanguard | V-EB15: Twinkle Melody |  | 84 |
| 16_Cardfight_Vanguard | V-MB01: PSYqualia Strife |  | 72 |
| 16_Cardfight_Vanguard | V-SS01: Premium Collection 2019 |  | 108 |
| 16_Cardfight_Vanguard | V-SS02: Colorful Pastorale Supply Gift Set |  | 10 |
| 16_Cardfight_Vanguard | V-SS03: Festival Collection |  | 132 |
| 16_Cardfight_Vanguard | V-SS04: Majesty Lord Blaster |  | 22 |
| 16_Cardfight_Vanguard | V-SS05: Premium Collection 2020 |  | 82 |
| 16_Cardfight_Vanguard | V-SS06: Valiant Sanctuary |  | 8 |
| 16_Cardfight_Vanguard | V-SS07: Clan Selection Plus Vol.1 |  | 97 |
| 16_Cardfight_Vanguard | V-SS08: Clan Selection Plus Vol.2 |  | 97 |
| 16_Cardfight_Vanguard | V-SS09: Revival Selection |  | 192 |
| 16_Cardfight_Vanguard | V-SS10 Premium Battle Deckset 2023 |  | 96 |
| 16_Cardfight_Vanguard | V-TB01: BanG Dream! FILM LIVE |  | 196 |
| 16_Cardfight_Vanguard | V-TD01: Aichi Sendou |  | 19 |
| 16_Cardfight_Vanguard | V-TD02: Toshiki Kai |  | 19 |
| 16_Cardfight_Vanguard | V-TD03: Leon Soryu |  | 19 |
| 16_Cardfight_Vanguard | V-TD04: Ren Suzugamori |  | 19 |
| 16_Cardfight_Vanguard | V-TD05: Misaki Tokura |  | 28 |
| 16_Cardfight_Vanguard | V-TD06: Naoki Ishida |  | 28 |
| 16_Cardfight_Vanguard | V-TD07: Kouji Ibuki |  | 28 |
| 16_Cardfight_Vanguard | V-TD08: Schokolade Melody |  | 35 |
| 16_Cardfight_Vanguard | V-TD09: Shinemon Nitta |  | 32 |
| 16_Cardfight_Vanguard | V-TD10: Chronojet |  | 32 |
| 16_Cardfight_Vanguard | V-TD11: Altmile |  | 32 |
| 16_Cardfight_Vanguard | V-TD12: Ahsha |  | 34 |

### 17_Force_of_Will（99 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 17_Force_of_Will | 10th Anniversary: Ruler Collection Set |  | 144 |
| 17_Force_of_Will | A New World Emerges |  | 231 |
| 17_Force_of_Will | ABC Duel Decks |  | 833 |
| 17_Force_of_Will | Advent of the Demon King |  | 312 |
| 17_Force_of_Will | Alice Origin |  | 164 |
| 17_Force_of_Will | Alice Origin II |  | 166 |
| 17_Force_of_Will | Alice Origin II Starter Deck |  | 70 |
| 17_Force_of_Will | Alice Origin III |  | 209 |
| 17_Force_of_Will | Alice Origin IV: Prologue of Attoractia |  | 274 |
| 17_Force_of_Will | Alice Origin Memoria Cards |  | 143 |
| 17_Force_of_Will | Alice Origin Starter Deck |  | 70 |
| 17_Force_of_Will | Ancient Nights |  | 328 |
| 17_Force_of_Will | Antechamber of the Ten Dimensions |  | 16 |
| 17_Force_of_Will | Arcana Battle Colosseum |  | 352 |
| 17_Force_of_Will | Assault into the Demonic World |  | 227 |
| 17_Force_of_Will | Attack on Velmardia |  | 221 |
| 17_Force_of_Will | Awakening of the Ancients |  | 203 |
| 17_Force_of_Will | Battle for Attoractia |  | 150 |
| 17_Force_of_Will | Clash of the Star Trees |  | 217 |
| 17_Force_of_Will | Crimson Moon's Battleground |  | 185 |
| 17_Force_of_Will | Crimson Moon's Fairy Tale |  | 115 |
| 17_Force_of_Will | Curse of the Frozen Casket |  | 150 |
| 17_Force_of_Will | Demo Decks: Captain Hook vs. Peter Pan |  | 53 |
| 17_Force_of_Will | Demo Decks: Christie vs. Reiya |  | 24 |
| 17_Force_of_Will | Descent into the Raven's Catacombs |  | 50 |
| 17_Force_of_Will | Dual Deck: Faria & Melgis |  | 34 |
| 17_Force_of_Will | Echoes of the New World |  | 163 |
| 17_Force_of_Will | Evil Cluster Starter Deck 1: Valgott |  | 38 |
| 17_Force_of_Will | Evil Cluster Starter Deck 2: Matelda |  | 38 |
| 17_Force_of_Will | Game of Gods |  | 191 |
| 17_Force_of_Will | Game of Gods: Reloaded |  | 194 |
| 17_Force_of_Will | Game of Gods: Revolution |  | 206 |
| 17_Force_of_Will | Ghost in the Shell SAC_2045 |  | 80 |
| 17_Force_of_Will | Ghost in the Shell SAC_2045 Starter Deck |  | 14 |
| 17_Force_of_Will | Hero Cluster Starter Decks |  | 46 |
| 17_Force_of_Will | Heroes' Contract Pack |  | 12 |
| 17_Force_of_Will | Heroes' Contract Pack 02 |  | 33 |
| 17_Force_of_Will | Journey to Ravidra |  | 219 |
| 17_Force_of_Will | Judgment of the Rogue Planet |  | 246 |
| 17_Force_of_Will | L1 Starter Deck - Fairy Tale Force |  | 12 |
| 17_Force_of_Will | L1 Starter Deck - Malefic Ice |  | 12 |
| 17_Force_of_Will | L1 Starter Deck - Rage of R'lyeh |  | 12 |
| 17_Force_of_Will | L1 Starter Deck - Swarming Elves |  | 12 |
| 17_Force_of_Will | L1 Starter Deck - Vampiric Hunger |  | 12 |
| 17_Force_of_Will | Legacy Lost |  | 158 |
| 17_Force_of_Will | Masterpiece Collection 02 "Fates Reunited!" |  | 150 |
| 17_Force_of_Will | Masterpiece Collection 03 "Dimensional Hope" |  | 300 |
| 17_Force_of_Will | Memoria Collection 01 |  | 15 |
| 17_Force_of_Will | Memoria Collection 02 |  | 10 |
| 17_Force_of_Will | Memoria Collection 03 |  | 7 |
| 17_Force_of_Will | Memoria Collection 04 |  | 9 |
| 17_Force_of_Will | Memoria Collection 05 |  | 12 |
| 17_Force_of_Will | Memoria Collection 06 |  | 12 |
| 17_Force_of_Will | Memoria Collection 07 |  | 25 |
| 17_Force_of_Will | Memoria Collection 08 |  | 12 |
| 17_Force_of_Will | Memoria Collection 09 |  | 10 |
| 17_Force_of_Will | Memoria Collection 10 |  | 54 |
| 17_Force_of_Will | Memoria Collection 11 |  | 10 |
| 17_Force_of_Will | New Dawn Rises |  | 226 |
| 17_Force_of_Will | Promo Cards |  | 619 |
| 17_Force_of_Will | Rebirth of Legend |  | 45 |
| 17_Force_of_Will | Reiya Cluster Starter Deck |  | 65 |
| 17_Force_of_Will | Return of the Dragon Emperor |  | 156 |
| 17_Force_of_Will | Starter Deck: Jet Black Phantom |  | 18 |
| 17_Force_of_Will | Starter Deck: Knights of the Round Table |  | 17 |
| 17_Force_of_Will | Starter Deck: Lehen |  | 31 |
| 17_Force_of_Will | Starter Deck: Magic Circle of the Hurricane |  | 17 |
| 17_Force_of_Will | Starter Deck: Royal Palace of the Roaring Seas |  | 17 |
| 17_Force_of_Will | Starter Deck: Tales |  | 22 |
| 17_Force_of_Will | Starter Deck: The Lost Tomes |  | 18 |
| 17_Force_of_Will | Starter Deck: Villains |  | 22 |
| 17_Force_of_Will | Starter Deck: Wolves of the Raging Flames |  | 17 |
| 17_Force_of_Will | Starter Deck: Yokoshima |  | 29 |
| 17_Force_of_Will | Ten Oaths of Protopaterpolis' War |  | 221 |
| 17_Force_of_Will | The Battle at the Sacred Ruins |  | 217 |
| 17_Force_of_Will | The Castle and The Two Towers |  | 107 |
| 17_Force_of_Will | The Dawn of Valhalla |  | 207 |
| 17_Force_of_Will | The Decisive Battle of Valhalla |  | 202 |
| 17_Force_of_Will | The Epic of the Dragon Lord |  | 202 |
| 17_Force_of_Will | The Magic Stone War - Zero |  | 222 |
| 17_Force_of_Will | The Millennia of Ages |  | 65 |
| 17_Force_of_Will | The Moon Priestess Returns |  | 109 |
| 17_Force_of_Will | The Moonlit Savior |  | 152 |
| 17_Force_of_Will | The Seven Kings of the Lands |  | 150 |
| 17_Force_of_Will | The Seventh |  | 221 |
| 17_Force_of_Will | The Shaft of Light of Valhalla |  | 135 |
| 17_Force_of_Will | The Strangers of New Valhalla |  | 203 |
| 17_Force_of_Will | The Time Spinning Witch |  | 319 |
| 17_Force_of_Will | The Twilight Wanderer |  | 161 |
| 17_Force_of_Will | The Underworld of Secrets |  | 204 |
| 17_Force_of_Will | The War of Valhalla |  | 155 |
| 17_Force_of_Will | The War of the Suns |  | 191 |
| 17_Force_of_Will | Thoth of the Trinity |  | 217 |
| 17_Force_of_Will | Timeless Eclipse of the Underworld |  | 218 |
| 17_Force_of_Will | Valhalla Cluster Starter Deck |  | 115 |
| 17_Force_of_Will | Vingolf -Engage Knights- |  | 143 |
| 17_Force_of_Will | Vingolf 2 - Valkyria Chronicles |  | 95 |
| 17_Force_of_Will | Vingolf 3 - Ruler All Stars |  | 102 |
| 17_Force_of_Will | Winds of the Ominous Moon |  | 254 |

### 18_Dice_Masters（27 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 18_Dice_Masters | Age of Ultron |  | 146 |
| 18_Dice_Masters | Ant-Man: Organized Play |  | 3 |
| 18_Dice_Masters | Avengers vs X-Men |  | 132 |
| 18_Dice_Masters | Avengers vs X-Men: Organized Play |  | 13 |
| 18_Dice_Masters | Batman |  | 211 |
| 18_Dice_Masters | Civil War |  | 133 |
| 18_Dice_Masters | D&D: Battle for Faerun |  | 138 |
| 18_Dice_Masters | D&D: Battle for Faerun: Organized Play |  | 10 |
| 18_Dice_Masters | D&D: Faerun Under Siege |  | 132 |
| 18_Dice_Masters | Deadpool |  | 240 |
| 18_Dice_Masters | Green Arrow & The Flash |  | 240 |
| 18_Dice_Masters | Iron Man and War Machine |  | 34 |
| 18_Dice_Masters | Justice League |  | 138 |
| 18_Dice_Masters | Justice League: Organized Play |  | 11 |
| 18_Dice_Masters | Miscellaneous Promo Cards |  | 1 |
| 18_Dice_Masters | Teenage Mutant Ninja Turtles |  | 57 |
| 18_Dice_Masters | Teenage Mutant Ninja Turtles: Heroes in a Half Shell |  | 58 |
| 18_Dice_Masters | Thanos Imperative: Organized Play |  | 3 |
| 18_Dice_Masters | The Amazing Spider-Man |  | 142 |
| 18_Dice_Masters | The Mighty Thor |  | 136 |
| 18_Dice_Masters | The Uncanny X-Men |  | 126 |
| 18_Dice_Masters | The Uncanny X-Men: Organized Play |  | 9 |
| 18_Dice_Masters | UXM Avengers Disassembled: Organized Play |  | 3 |
| 18_Dice_Masters | War of Light |  | 146 |
| 18_Dice_Masters | World's Finest |  | 132 |
| 18_Dice_Masters | X-Men First Class |  | 124 |
| 18_Dice_Masters | Yu-Gi-Oh! Series One |  | 120 |

### 19_Future_Card_BuddyFight（92 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 19_Future_Card_BuddyFight | Annihilate! Great Demonic Dragon!! |  | 126 |
| 19_Future_Card_BuddyFight | Assault of the Omni Lords |  | 137 |
| 19_Future_Card_BuddyFight | BanG Dream! Girls Band Party! PICO |  | 91 |
| 19_Future_Card_BuddyFight | Blazing Overclash |  | 116 |
| 19_Future_Card_BuddyFight | Break to the Future |  | 147 |
| 19_Future_Card_BuddyFight | Buddy Again Vol.2 ~Super Buddy War EX~ |  | 67 |
| 19_Future_Card_BuddyFight | Buddy Again Vol.3 ~Beyond the Ages~ |  | 66 |
| 19_Future_Card_BuddyFight | Buddy Allstars+ |  | 112 |
| 19_Future_Card_BuddyFight | Buddy Legends |  | 85 |
| 19_Future_Card_BuddyFight | Buddy Lineage |  | 129 |
| 19_Future_Card_BuddyFight | Buddy Ragnarok |  | 173 |
| 19_Future_Card_BuddyFight | Buddy Rave |  | 150 |
| 19_Future_Card_BuddyFight | Bushiroad Event Cards |  | 18 |
| 19_Future_Card_BuddyFight | Chaos Control Crisis |  | 129 |
| 19_Future_Card_BuddyFight | Character Pack Vol.1: Burning Valor |  | 51 |
| 19_Future_Card_BuddyFight | Collector's Glory Vol.1 |  | 10 |
| 19_Future_Card_BuddyFight | Crossing Generations |  | 183 |
| 19_Future_Card_BuddyFight | Cyber Ninja Squad |  | 117 |
| 19_Future_Card_BuddyFight | Darkness Fable |  | 117 |
| 19_Future_Card_BuddyFight | Dimension Destroyer |  | 92 |
| 19_Future_Card_BuddyFight | Drago Knight |  | 87 |
| 19_Future_Card_BuddyFight | Dragon Fighters |  | 132 |
| 19_Future_Card_BuddyFight | Driven to Disorder |  | 170 |
| 19_Future_Card_BuddyFight | Drum's Adventures |  | 117 |
| 19_Future_Card_BuddyFight | Evolution & Mutation |  | 184 |
| 19_Future_Card_BuddyFight | Four Dimensions |  | 124 |
| 19_Future_Card_BuddyFight | Future Card Buddyfight 10th Anniversary Card Set |  | 41 |
| 19_Future_Card_BuddyFight | Galaxy Burst |  | 124 |
| 19_Future_Card_BuddyFight | Gargantua Awakened |  | 98 |
| 19_Future_Card_BuddyFight | Golden Buddy Champion Box |  | 60 |
| 19_Future_Card_BuddyFight | Golden Buddy Pack ver.E |  | 62 |
| 19_Future_Card_BuddyFight | Great Clash!! Dragon VS Danger |  | 54 |
| 19_Future_Card_BuddyFight | Immortal Entities |  | 55 |
| 19_Future_Card_BuddyFight | Introductory Set 1: Dragon World |  | 15 |
| 19_Future_Card_BuddyFight | LVL Up! Heroes & Adventurers! |  | 164 |
| 19_Future_Card_BuddyFight | Lord of Hundred Thunders |  | 69 |
| 19_Future_Card_BuddyFight | Mikado Evolution |  | 126 |
| 19_Future_Card_BuddyFight | Miracle Impack! |  | 69 |
| 19_Future_Card_BuddyFight | Neo Enforcer ver.E |  | 120 |
| 19_Future_Card_BuddyFight | New World Chaos |  | 142 |
| 19_Future_Card_BuddyFight | Overturn! Thunder Empire!! |  | 120 |
| 19_Future_Card_BuddyFight | Perfected Time Ruler |  | 86 |
| 19_Future_Card_BuddyFight | Promo Cards |  | 349 |
| 19_Future_Card_BuddyFight | Rainbow Striker |  | 120 |
| 19_Future_Card_BuddyFight | Re: Collection Vol.1 |  | 55 |
| 19_Future_Card_BuddyFight | Roar! Invincible Dragon!! |  | 128 |
| 19_Future_Card_BuddyFight | S-CBT02: Violence Vanity |  | 85 |
| 19_Future_Card_BuddyFight | S-CBT03: Ultimate Unite |  | 84 |
| 19_Future_Card_BuddyFight | S-Promo Cards |  | 120 |
| 19_Future_Card_BuddyFight | S-SD01: Dradeity |  | 18 |
| 19_Future_Card_BuddyFight | S-SD02: Triangulum Galaxy |  | 18 |
| 19_Future_Card_BuddyFight | S-SD03: Spiral Linkdragon Order |  | 18 |
| 19_Future_Card_BuddyFight | S-SS01: Lost Dimension |  | 34 |
| 19_Future_Card_BuddyFight | S-SS02: 3 Garga Decks! Impact! Triple Punisher |  | 63 |
| 19_Future_Card_BuddyFight | S-SS03: The End Zero |  | 32 |
| 19_Future_Card_BuddyFight | S-TD-C01: Case Closed -Side:White- |  | 24 |
| 19_Future_Card_BuddyFight | S-TD-C02: Case Closed -Side:Black- |  | 24 |
| 19_Future_Card_BuddyFight | S-TD01: Draknight |  | 23 |
| 19_Future_Card_BuddyFight | S-TD02: Legend of Double Horus |  | 23 |
| 19_Future_Card_BuddyFight | S-UB-C01: Case Closed |  | 75 |
| 19_Future_Card_BuddyFight | S-UB01: Superhero Wars Omega -Advent of Cosmoman!- |  | 68 |
| 19_Future_Card_BuddyFight | S-UB02: Miracle Fighters ~Miko & Mel~ |  | 68 |
| 19_Future_Card_BuddyFight | SSSS.GRIDMAN |  | 81 |
| 19_Future_Card_BuddyFight | Shadow VS Hero |  | 73 |
| 19_Future_Card_BuddyFight | Shine! Super Sun Dragon!! |  | 123 |
| 19_Future_Card_BuddyFight | Solar Strife |  | 120 |
| 19_Future_Card_BuddyFight | Starter Deck: Cross Dragoner |  | 20 |
| 19_Future_Card_BuddyFight | Starter Deck: Hollow Black Dragon |  | 20 |
| 19_Future_Card_BuddyFight | Starter Deck: Scorching Sun Dragon |  | 20 |
| 19_Future_Card_BuddyFight | Terror of the Inverse Omni Lords |  | 77 |
| 19_Future_Card_BuddyFight | The Dark Lord's Rebirth! |  | 137 |
| 19_Future_Card_BuddyFight | The iDOLM@STER Cinderella Girls Theater |  | 172 |
| 19_Future_Card_BuddyFight | Trial Deck: Braves Explosion |  | 23 |
| 19_Future_Card_BuddyFight | Trial Deck: Crimson Fist |  | 20 |
| 19_Future_Card_BuddyFight | Trial Deck: Dark Pulse |  | 22 |
| 19_Future_Card_BuddyFight | Trial Deck: Dominant Dragons |  | 19 |
| 19_Future_Card_BuddyFight | Trial Deck: Dragon Emperor of the Colossal Ocean |  | 22 |
| 19_Future_Card_BuddyFight | Trial Deck: Dragonic Force |  | 22 |
| 19_Future_Card_BuddyFight | Trial Deck: Dragonic Star |  | 21 |
| 19_Future_Card_BuddyFight | Trial Deck: Malicious Demons |  | 20 |
| 19_Future_Card_BuddyFight | Trial Deck: Ninja Onslaught |  | 22 |
| 19_Future_Card_BuddyFight | Trial Deck: Radiant Force |  | 20 |
| 19_Future_Card_BuddyFight | Trial Deck: Savage Steel |  | 19 |
| 19_Future_Card_BuddyFight | Trial Deck: Tomorrow! Asmodai |  | 21 |
| 19_Future_Card_BuddyFight | Unleash! Impact Dragon!! |  | 134 |
| 19_Future_Card_BuddyFight | War of Dragods |  | 87 |
| 19_Future_Card_BuddyFight | X Duel Chest |  | 70 |
| 19_Future_Card_BuddyFight | X-SD01: Demon Lord Dragon of Tempest |  | 19 |
| 19_Future_Card_BuddyFight | X-SD02: Dragon Fielder |  | 19 |
| 19_Future_Card_BuddyFight | X-TD01: Decimating Black Dragon |  | 17 |
| 19_Future_Card_BuddyFight | X-TD02: Ruler of Havoc |  | 17 |
| 19_Future_Card_BuddyFight | X-TD03: Thunderous Warlords Alliance |  | 20 |

### 20_Weiss_Schwarz（163 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 20_Weiss_Schwarz | Accel World |  | 142 |
| 20_Weiss_Schwarz | Accel World -Infinite Burst- |  | 123 |
| 20_Weiss_Schwarz | Adventure Time |  | 174 |
| 20_Weiss_Schwarz | Angel Beats! Re:Edit |  | 191 |
| 20_Weiss_Schwarz | Arifureta: From Commonplace to World's Strongest |  | 187 |
| 20_Weiss_Schwarz | Attack On Titan: Final Season |  | 196 |
| 20_Weiss_Schwarz | Attack on Titan |  | 167 |
| 20_Weiss_Schwarz | Attack on Titan Vol. 2 |  | 147 |
| 20_Weiss_Schwarz | Avatar: The Last Airbender |  | 196 |
| 20_Weiss_Schwarz | Ayakashi Triangle |  | 204 |
| 20_Weiss_Schwarz | Azur Lane |  | 217 |
| 20_Weiss_Schwarz | Azur Lane Vol. 2 |  | 265 |
| 20_Weiss_Schwarz | BAKEMONOGATARI |  | 146 |
| 20_Weiss_Schwarz | BOCCHI THE ROCK! |  | 100 |
| 20_Weiss_Schwarz | BOFURI: I Don't Want to Get Hurt, so I'll Max Out My Defense |  | 185 |
| 20_Weiss_Schwarz | BanG Dream! |  | 194 |
| 20_Weiss_Schwarz | BanG Dream! 10th Anniversary! Premium Booster |  | 179 |
| 20_Weiss_Schwarz | BanG Dream! Girls Band Party! |  | 288 |
| 20_Weiss_Schwarz | BanG Dream! Girls Band Party! 5th Anniversary |  | 279 |
| 20_Weiss_Schwarz | BanG Dream! Girls Band Party! Countdown Collection Premium Booster |  | 290 |
| 20_Weiss_Schwarz | BanG Dream! Girls Band Party! MULTI LIVE |  | 251 |
| 20_Weiss_Schwarz | BanG Dream! Girls Band Party! Premium Booster |  | 69 |
| 20_Weiss_Schwarz | BanG Dream! Girls Band Party! Vol.2 |  | 251 |
| 20_Weiss_Schwarz | BanG Dream! Vol.2 |  | 303 |
| 20_Weiss_Schwarz | Batman Ninja |  | 163 |
| 20_Weiss_Schwarz | Blue Archive |  | 196 |
| 20_Weiss_Schwarz | Blue Archive The Animation |  | 210 |
| 20_Weiss_Schwarz | Bushiroad Event Cards |  | 109 |
| 20_Weiss_Schwarz | Cardcaptor Sakura: Clear Card |  | 166 |
| 20_Weiss_Schwarz | Chainsaw Man |  | 201 |
| 20_Weiss_Schwarz | DANDADAN |  | 306 |
| 20_Weiss_Schwarz | Date A Bullet |  | 103 |
| 20_Weiss_Schwarz | Date A Live |  | 164 |
| 20_Weiss_Schwarz | Date A Live Vol.2 |  | 86 |
| 20_Weiss_Schwarz | Dengeki Bunko |  | 436 |
| 20_Weiss_Schwarz | Disgaea |  | 214 |
| 20_Weiss_Schwarz | FAIRY TAIL 100 YEARS QUEST |  | 243 |
| 20_Weiss_Schwarz | Fairy Tail Chronicle Set |  | 178 |
| 20_Weiss_Schwarz | Fairy Tail ver.E |  | 178 |
| 20_Weiss_Schwarz | Fate/Apocrypha |  | 158 |
| 20_Weiss_Schwarz | Fate/Grand Order Absolute Demonic Front: Babylonia |  | 163 |
| 20_Weiss_Schwarz | Fate/Grand Order THE MOVIE Divine Realm of the Round Table: Camelot |  | 149 |
| 20_Weiss_Schwarz | Fate/Zero |  | 150 |
| 20_Weiss_Schwarz | Fate/Zero Chronicle Set |  | 146 |
| 20_Weiss_Schwarz | Fate/kaleid liner PRISMA ILLYA DX |  | 107 |
| 20_Weiss_Schwarz | Fate/stay night [Heaven's Feel] |  | 134 |
| 20_Weiss_Schwarz | Fate/stay night [Heaven's Feel] Vol.2 |  | 133 |
| 20_Weiss_Schwarz | Fate/stay night [Unlimited Blade Works] |  | 145 |
| 20_Weiss_Schwarz | Fate/stay night [Unlimited Blade Works] Vol. II |  | 124 |
| 20_Weiss_Schwarz | Frieren: Beyond Journey's End |  | 283 |
| 20_Weiss_Schwarz | Fujimi Fantasia Bunko |  | 183 |
| 20_Weiss_Schwarz | Fujimi Fantasia Bunko Vol.2 |  | 431 |
| 20_Weiss_Schwarz | GODDESS OF VICTORY: NIKKE |  | 419 |
| 20_Weiss_Schwarz | Girls Band Cry Premium Booster |  | 202 |
| 20_Weiss_Schwarz | Goblin Slayer |  | 162 |
| 20_Weiss_Schwarz | Guilty Gear -Strive- |  | 207 |
| 20_Weiss_Schwarz | Gurren Lagann |  | 155 |
| 20_Weiss_Schwarz | Hatsune Miku -Project DIVA- f |  | 192 |
| 20_Weiss_Schwarz | Hatsune Miku: Project DIVA F 2nd |  | 177 |
| 20_Weiss_Schwarz | Is it Wrong to Try to Pick Up Girls in a Dungeon? |  | 163 |
| 20_Weiss_Schwarz | JoJo's Bizarre Adventure: Golden Wind |  | 237 |
| 20_Weiss_Schwarz | JoJo's Bizarre Adventure: Stardust Crusaders Premium Booster |  | 127 |
| 20_Weiss_Schwarz | KILL la KILL |  | 153 |
| 20_Weiss_Schwarz | KILL la KILL Power Up Set |  | 20 |
| 20_Weiss_Schwarz | KONOSUBA -God’s blessing on this wonderful world! Re:Edit |  | 148 |
| 20_Weiss_Schwarz | Kaguya-Sama: Love is War? |  | 100 |
| 20_Weiss_Schwarz | Kaguya-sama: Love is War |  | 171 |
| 20_Weiss_Schwarz | KanColle |  | 259 |
| 20_Weiss_Schwarz | KanColle, 2nd Fleet |  | 150 |
| 20_Weiss_Schwarz | KanColle: Arrival! Reinforcement Fleets from Europe! |  | 135 |
| 20_Weiss_Schwarz | KanColle: Fleet in the Deep Sea, Sighted! |  | 116 |
| 20_Weiss_Schwarz | KonoSuba |  | 150 |
| 20_Weiss_Schwarz | KonoSuba 2 |  | 131 |
| 20_Weiss_Schwarz | KonoSuba The Movie: Legend of Crimson |  | 144 |
| 20_Weiss_Schwarz | LOG HORIZON |  | 129 |
| 20_Weiss_Schwarz | LOG HORIZON Power Up Set |  | 20 |
| 20_Weiss_Schwarz | Love Live! |  | 188 |
| 20_Weiss_Schwarz | Love Live! DX |  | 140 |
| 20_Weiss_Schwarz | Love Live! DX Vol.2 |  | 240 |
| 20_Weiss_Schwarz | Love Live! School Idol Festival Series 10th Anniversary Premium Booster |  | 182 |
| 20_Weiss_Schwarz | Love Live! School idol festival 2 MIRACLE LIVE! |  | 223 |
| 20_Weiss_Schwarz | Love Live! Sunshine!! |  | 170 |
| 20_Weiss_Schwarz | Love Live! Sunshine!! Extra Booster |  | 164 |
| 20_Weiss_Schwarz | Love Live! Vol. 2 |  | 173 |
| 20_Weiss_Schwarz | Lycoris Recoil |  | 196 |
| 20_Weiss_Schwarz | Lycoris Recoil Premium Booster |  | 118 |
| 20_Weiss_Schwarz | MACROSS Delta Premium Booster |  | 149 |
| 20_Weiss_Schwarz | Magia Record: Puella Magi Madoka Magica [Side Story] (Anime) |  | 165 |
| 20_Weiss_Schwarz | Magia Record: Puella Magi Madoka Magica [Side Story] (Mobile) |  | 154 |
| 20_Weiss_Schwarz | Miss Kobayashi's Dragon Maid |  | 1 |
| 20_Weiss_Schwarz | Mob Psycho 100 |  | 160 |
| 20_Weiss_Schwarz | Morfonica x RAISE A SUILEN |  | 147 |
| 20_Weiss_Schwarz | Mushoku Tensei: Jobless Reincarnation |  | 183 |
| 20_Weiss_Schwarz | MyGO!!!!! x Ave Mujica |  | 301 |
| 20_Weiss_Schwarz | NISEKOI -False Love- |  | 148 |
| 20_Weiss_Schwarz | NISEKOI Extra Booster |  | 76 |
| 20_Weiss_Schwarz | NISEMONOGATARI |  | 98 |
| 20_Weiss_Schwarz | Nazarick: Tomb of the Undead |  | 180 |
| 20_Weiss_Schwarz | Nazarick: Tomb of the Undead Vol.2 |  | 157 |
| 20_Weiss_Schwarz | Nazarick: Tomb of the Undead Vol.3 Extra Booster |  | 141 |
| 20_Weiss_Schwarz | No Game No Life |  | 162 |
| 20_Weiss_Schwarz | Persona 4 ver.E |  | 160 |
| 20_Weiss_Schwarz | Persona 5 |  | 165 |
| 20_Weiss_Schwarz | Poppin’Party x Roselia |  | 125 |
| 20_Weiss_Schwarz | Promo Cards |  | 34 |
| 20_Weiss_Schwarz | Puella Magi Madoka Magica |  | 151 |
| 20_Weiss_Schwarz | Puella Magi Madoka Magica the Movie -Rebellion- |  | 131 |
| 20_Weiss_Schwarz | RWBY |  | 172 |
| 20_Weiss_Schwarz | RWBY Premium Booster |  | 118 |
| 20_Weiss_Schwarz | Rascal Does Not Dream Series |  | 214 |
| 20_Weiss_Schwarz | Rascal Does Not Dream of Bunny Girl Senpai |  | 176 |
| 20_Weiss_Schwarz | Rascal Does Not Dream of a Dreaming Girl |  | 50 |
| 20_Weiss_Schwarz | Re:ZERO |  | 165 |
| 20_Weiss_Schwarz | Re:ZERO -Starting Life in Another World- Vol.3 |  | 236 |
| 20_Weiss_Schwarz | Re:ZERO Memory Snow |  | 134 |
| 20_Weiss_Schwarz | Re:ZERO Vol.2 |  | 135 |
| 20_Weiss_Schwarz | Re:ZERO: The Frozen Bond |  | 109 |
| 20_Weiss_Schwarz | Rent-A-Girlfriend |  | 166 |
| 20_Weiss_Schwarz | Revue Starlight |  | 190 |
| 20_Weiss_Schwarz | Revue Starlight -Re LIVE- |  | 158 |
| 20_Weiss_Schwarz | Revue Starlight The Movie |  | 176 |
| 20_Weiss_Schwarz | Rurouni Kenshin |  | 260 |
| 20_Weiss_Schwarz | SAO Alternative–Gun Gale Online |  | 173 |
| 20_Weiss_Schwarz | SAO Alternative–Gun Gale Online–2 Extra Booster |  | 50 |
| 20_Weiss_Schwarz | SPY x FAMILY |  | 161 |
| 20_Weiss_Schwarz | Saekano the Movie: Finale |  | 145 |
| 20_Weiss_Schwarz | Saekano: How to Raise a Boring Girlfriend |  | 166 |
| 20_Weiss_Schwarz | Shakugan no Shana Premium Booster |  | 50 |
| 20_Weiss_Schwarz | Sword Art Online |  | 158 |
| 20_Weiss_Schwarz | Sword Art Online -Alicization- |  | 164 |
| 20_Weiss_Schwarz | Sword Art Online -Alicization- Vol.2 |  | 146 |
| 20_Weiss_Schwarz | Sword Art Online Animation 10th Anniversary |  | 208 |
| 20_Weiss_Schwarz | Sword Art Online Chronicle Set |  | 154 |
| 20_Weiss_Schwarz | Sword Art Online II |  | 107 |
| 20_Weiss_Schwarz | Sword Art Online II Vol.2 |  | 75 |
| 20_Weiss_Schwarz | Sword Art Online Re: Edit |  | 148 |
| 20_Weiss_Schwarz | Sword Art Online The Movie: -Ordinal Scale- |  | 131 |
| 20_Weiss_Schwarz | Sword Art Online Vol.2 |  | 106 |
| 20_Weiss_Schwarz | That Time I Got Reincarnated as a Slime |  | 168 |
| 20_Weiss_Schwarz | That Time I Got Reincarnated as a Slime Vol.2 |  | 133 |
| 20_Weiss_Schwarz | That Time I Got Reincarnated as a Slime Vol.3 |  | 159 |
| 20_Weiss_Schwarz | The Eminence in Shadow |  | 285 |
| 20_Weiss_Schwarz | The Fruit of Grisaia |  | 184 |
| 20_Weiss_Schwarz | The Melancholy Of Haruhi Suzumiya Power Up Set |  | 19 |
| 20_Weiss_Schwarz | The Melancholy of Haruhi Suzumiya |  | 143 |
| 20_Weiss_Schwarz | The Melancholy of Haruhi Suzumiya Extra Booster |  | 68 |
| 20_Weiss_Schwarz | The Quintessential Quintuplets |  | 318 |
| 20_Weiss_Schwarz | The Quintessential Quintuplets 2 |  | 216 |
| 20_Weiss_Schwarz | The Quintessential Quintuplets Movie |  | 210 |
| 20_Weiss_Schwarz | The Quintessential Quintuplets Specials Premium Booster |  | 52 |
| 20_Weiss_Schwarz | The Seven Deadly Sins |  | 165 |
| 20_Weiss_Schwarz | The Seven Deadly Sins: Revival of The Commandments |  | 175 |
| 20_Weiss_Schwarz | The iDOLM@STER Cinderella Girls |  | 260 |
| 20_Weiss_Schwarz | To Loveru Darkness 2nd |  | 154 |
| 20_Weiss_Schwarz | Tokyo Revengers |  | 197 |
| 20_Weiss_Schwarz | Umamusume: Pretty Derby |  | 335 |
| 20_Weiss_Schwarz | [OSHI NO KO] |  | 184 |
| 20_Weiss_Schwarz | [OSHI NO KO] Vol.2 |  | 232 |
| 20_Weiss_Schwarz | hololive production |  | 618 |
| 20_Weiss_Schwarz | hololive production Premium Booster |  | 40 |
| 20_Weiss_Schwarz | hololive production Summer Collection Premium Booster |  | 100 |
| 20_Weiss_Schwarz | hololive production Vol.2 |  | 200 |
| 20_Weiss_Schwarz | hololive production feat. Weiss Schwarz Ambassadors Premium Set |  | 34 |

### 23_Dragon_Ball_Z_TCG（9 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 23_Dragon_Ball_Z_TCG | Panini Promo Cards |  | 107 |
| 23_Dragon_Ball_Z_TCG | Panini: Awakening |  | 376 |
| 23_Dragon_Ball_Z_TCG | Panini: Evolution |  | 377 |
| 23_Dragon_Ball_Z_TCG | Panini: Heroes & Villains |  | 142 |
| 23_Dragon_Ball_Z_TCG | Panini: Miscellaneous Cards |  | 10 |
| 23_Dragon_Ball_Z_TCG | Panini: Movie Collection |  | 142 |
| 23_Dragon_Ball_Z_TCG | Panini: Perfection |  | 146 |
| 23_Dragon_Ball_Z_TCG | Panini: Set 1 |  | 342 |
| 23_Dragon_Ball_Z_TCG | Panini: Vengeance |  | 112 |

### 28_Dragoborne（11 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 28_Dragoborne | Gears of Apocalypse |  | 125 |
| 28_Dragoborne | Oath of Blood |  | 125 |
| 28_Dragoborne | PR Cards |  | 30 |
| 28_Dragoborne | Rally to War |  | 124 |
| 28_Dragoborne | Reckoning of Vashr |  | 80 |
| 28_Dragoborne | Surge of Titans |  | 85 |
| 28_Dragoborne | TD01: Shadow Legion |  | 21 |
| 28_Dragoborne | TD02: Mystical Hunters |  | 21 |
| 28_Dragoborne | TD03: Alpha Dominance |  | 21 |
| 28_Dragoborne | TD04: Reaper's Gift |  | 20 |
| 28_Dragoborne | TD05: Nature's Wrath |  | 18 |

### 30_MetaX_TCG（5 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 30_MetaX_TCG | Attack on Titan |  | 190 |
| 30_MetaX_TCG | Batman |  | 151 |
| 30_MetaX_TCG | Green Lantern |  | 160 |
| 30_MetaX_TCG | Justice League |  | 216 |
| 30_MetaX_TCG | Promotional Cards |  | 35 |

### 36_Zombie_World_Order_TCG（2 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 36_Zombie_World_Order_TCG | ZWO Promo Cards |  | 1 |
| 36_Zombie_World_Order_TCG | Zombie World Order TCG - Set 1 |  | 68 |

### 37_The_Caster_Chronicles（12 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 37_The_Caster_Chronicles | Caster Wars |  | 89 |
| 37_The_Caster_Chronicles | Polar Night |  | 84 |
| 37_The_Caster_Chronicles | Promos |  | 26 |
| 37_The_Caster_Chronicles | SD01: Wings of Anger |  | 24 |
| 37_The_Caster_Chronicles | SD02: Arrogant Swallowtail |  | 25 |
| 37_The_Caster_Chronicles | SD03: Magical Dream 7 |  | 26 |
| 37_The_Caster_Chronicles | SD04: Angel's Waltz VS Demon's Rondo |  | 50 |
| 37_The_Caster_Chronicles | SD2S2: Polar Night Dual Deck |  | 44 |
| 37_The_Caster_Chronicles | The Earnest Workers VS The Supreme Talents |  | 90 |
| 37_The_Caster_Chronicles | The Magic Battle Begins |  | 193 |
| 37_The_Caster_Chronicles | The New World Order Admissions |  | 84 |
| 37_The_Caster_Chronicles | pith DIMENSION BATTLE ROYALE |  | 100 |

### 47_Exodus_TCG（8 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 47_Exodus_TCG | Birth of Creation |  | 158 |
| 47_Exodus_TCG | Converging Chasms |  | 91 |
| 47_Exodus_TCG | Crystal Forge |  | 83 |
| 47_Exodus_TCG | Exodus Promo Cards |  | 63 |
| 47_Exodus_TCG | Galaxy Tides |  | 62 |
| 47_Exodus_TCG | Limited Edition Sketch Cards |  | 63 |
| 47_Exodus_TCG | The Dimension that Disappeared |  | 77 |
| 47_Exodus_TCG | Threshold of Time |  | 88 |

### 48_Lightseekers_TCG（3 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 48_Lightseekers_TCG | Awakening |  | 739 |
| 48_Lightseekers_TCG | Kindred |  | 744 |
| 48_Lightseekers_TCG | Mythical |  | 373 |

### 53_Munchkin_CCG（4 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 53_Munchkin_CCG | Fashion Furious |  | 135 |
| 53_Munchkin_CCG | Grave Danger |  | 1 |
| 53_Munchkin_CCG | Season 1 |  | 322 |
| 53_Munchkin_CCG | The Desolation of Blarg |  | 130 |

### 54_Warhammer_Age_of_Sigmar_Champions_TCG（5 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 54_Warhammer_Age_of_Sigmar_Champions_TCG | Warband Collectors Pack 1 |  | 16 |
| 54_Warhammer_Age_of_Sigmar_Champions_TCG | Warband Collectors Pack 2 |  | 16 |
| 54_Warhammer_Age_of_Sigmar_Champions_TCG | Wave 1 |  | 553 |
| 54_Warhammer_Age_of_Sigmar_Champions_TCG | Wave 2 - Onslaught |  | 257 |
| 54_Warhammer_Age_of_Sigmar_Champions_TCG | Wave 3 - Savagery |  | 316 |

### 57_Transformers_TCG（8 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 57_Transformers_TCG | Blaster VS Soundwave Box Set |  | 15 |
| 57_Transformers_TCG | Blaster VS Soundwave Box Set 35th Anniversary Edition |  | 15 |
| 57_Transformers_TCG | Rise of the Combiners |  | 142 |
| 57_Transformers_TCG | Titan Masters Attack |  | 143 |
| 57_Transformers_TCG | Transformers Promos |  | 17 |
| 57_Transformers_TCG | War for Cybertron: Siege I |  | 112 |
| 57_Transformers_TCG | War for Cybertron: Siege II |  | 120 |
| 57_Transformers_TCG | Wave 1 |  | 149 |

### 58_Bakugan_TCG（4 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 58_Bakugan_TCG | Age of Aurelus |  | 221 |
| 58_Bakugan_TCG | Armored Elite |  | 271 |
| 58_Bakugan_TCG | Battle Brawlers |  | 374 |
| 58_Bakugan_TCG | Resurgence |  | 246 |

### 60_Chrono_Clash_System（2 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 60_Chrono_Clash_System | GZ Tournament Pack Cards |  | 1 |
| 60_Chrono_Clash_System | NB Tournament Pack Cards |  | 97 |

### 61_Argent_Saga_TCG（10 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 61_Argent_Saga_TCG | Alpha Demo Intro Decks |  | 90 |
| 61_Argent_Saga_TCG | Argent Saga Promos |  | 227 |
| 61_Argent_Saga_TCG | Ascension |  | 130 |
| 61_Argent_Saga_TCG | Betrayal |  | 126 |
| 61_Argent_Saga_TCG | Echoes of Hokken |  | 136 |
| 61_Argent_Saga_TCG | Expansion Pack 1: Generations |  | 25 |
| 61_Argent_Saga_TCG | Expansion Pack 2: Genesis |  | 25 |
| 61_Argent_Saga_TCG | Expansion Pack 3: Conviction |  | 25 |
| 61_Argent_Saga_TCG | Intro Decks - 2019 |  | 86 |
| 61_Argent_Saga_TCG | Revelations |  | 101 |

### 62_Flesh_and_Blood_TCG（99 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 62_Flesh_and_Blood_TCG | 1st Strike |  | 62 |
| 62_Flesh_and_Blood_TCG | Arcane Rising |  | 50 |
| 62_Flesh_and_Blood_TCG | Armory Deck Origins: Hala |  | 27 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Arakni |  | 31 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Aurora |  | 28 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Azalea |  | 32 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Boltyn |  | 28 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Dash |  | 27 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Dr. Mortimer |  | 4 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Gravy Bones |  | 49 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Ira |  | 27 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Jarl Vetreidi |  | 27 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Kayo |  | 28 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Legends Prism |  | 27 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Legends Viserai |  | 30 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Malice |  | 8 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Maxx Nitro |  | 30 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Olympia |  | 29 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Pleiades |  | 32 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Rhinar |  | 30 |
| 62_Flesh_and_Blood_TCG | Armory Deck: Zyggy |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Heavy Hitters - Betsy |  | 31 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Heavy Hitters - Kassai |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Heavy Hitters - Kayo |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Heavy Hitters - Olympia |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Heavy Hitters - Rhinar |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Heavy Hitters - Victor |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Monarch - Boltyn |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Monarch - Chane |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Monarch - Levia |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Monarch - Prism |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Outsiders - Arakni |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Outsiders - Azalea |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Outsiders - Benji |  | 26 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Outsiders - Katsu |  | 26 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Outsiders - Riptide |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Outsiders - Uzuri |  | 31 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Part the Mistveil - Enigma |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Part the Mistveil - Nuu |  | 28 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Part the Mistveil - Zen |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Rosetta - Aurora |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Rosetta - Florian |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Rosetta - Oscilio |  | 29 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Rosetta - Verdance |  | 28 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Tales of Aria - Briar |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Tales of Aria - Lexi |  | 30 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Tales of Aria - Oldhim |  | 32 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: The Hunted - Arakni |  | 26 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: The Hunted - Arakni, Web of Deceit |  | 31 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: The Hunted - Cindra |  | 28 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: The Hunted - Fang |  | 28 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Uprising - Dromai |  | 28 |
| 62_Flesh_and_Blood_TCG | Blitz Deck: Uprising - Fai |  | 26 |
| 62_Flesh_and_Blood_TCG | Bright Lights |  | 200 |
| 62_Flesh_and_Blood_TCG | Classic Battles: Rhinar vs Dorinthea |  | 54 |
| 62_Flesh_and_Blood_TCG | Compendium of Rathe |  | 368 |
| 62_Flesh_and_Blood_TCG | Compendium of Rathe - Antiquity Pack |  | 65 |
| 62_Flesh_and_Blood_TCG | Crucible of War |  | 100 |
| 62_Flesh_and_Blood_TCG | Dusk till Dawn |  | 100 |
| 62_Flesh_and_Blood_TCG | Dynasty |  | 100 |
| 62_Flesh_and_Blood_TCG | Everfest |  | 220 |
| 62_Flesh_and_Blood_TCG | Flesh and Blood: Promo Cards |  | 50 |
| 62_Flesh_and_Blood_TCG | GEM Pack 1 |  | 50 |
| 62_Flesh_and_Blood_TCG | GEM Pack 2 |  | 54 |
| 62_Flesh_and_Blood_TCG | GEM Pack 3 |  | 54 |
| 62_Flesh_and_Blood_TCG | GEM Pack 4 |  | 54 |
| 62_Flesh_and_Blood_TCG | GEM Pack 6 |  | 2 |
| 62_Flesh_and_Blood_TCG | Gem Pack 5 |  | 61 |
| 62_Flesh_and_Blood_TCG | Heavy Hitters |  | 239 |
| 62_Flesh_and_Blood_TCG | Hero Deck: Bravo |  | 29 |
| 62_Flesh_and_Blood_TCG | Hero Deck: Dorinthea |  | 30 |
| 62_Flesh_and_Blood_TCG | Hero Deck: Katsu |  | 30 |
| 62_Flesh_and_Blood_TCG | Hero Deck: Rhinar |  | 31 |
| 62_Flesh_and_Blood_TCG | High Seas |  | 369 |
| 62_Flesh_and_Blood_TCG | Historic Pack 1 Blitz Deck: Bravo |  | 27 |
| 62_Flesh_and_Blood_TCG | Historic Pack 1 Blitz Deck: Dash |  | 28 |
| 62_Flesh_and_Blood_TCG | Historic Pack 1 Blitz Deck: Dorinthea |  | 27 |
| 62_Flesh_and_Blood_TCG | Historic Pack 1 Blitz Deck: Kano |  | 27 |
| 62_Flesh_and_Blood_TCG | Historic Pack 1 Blitz Deck: Rhinar |  | 26 |
| 62_Flesh_and_Blood_TCG | Historic Pack 1 Blitz Deck: Viserai |  | 27 |
| 62_Flesh_and_Blood_TCG | Mastery Pack Assassin |  | 9 |
| 62_Flesh_and_Blood_TCG | Mastery Pack Warrior |  | 165 |
| 62_Flesh_and_Blood_TCG | Monarch |  | 100 |
| 62_Flesh_and_Blood_TCG | Outsiders |  | 96 |
| 62_Flesh_and_Blood_TCG | Rosetta |  | 50 |
| 62_Flesh_and_Blood_TCG | Round the Table: TCCxLSS |  | 110 |
| 62_Flesh_and_Blood_TCG | Silver Age Chapter 1 |  | 173 |
| 62_Flesh_and_Blood_TCG | Silver Age Chapter 3 |  | 173 |
| 62_Flesh_and_Blood_TCG | Silver Age: Usurp the Shadow Throne |  | 34 |
| 62_Flesh_and_Blood_TCG | Smash Palace |  | 32 |
| 62_Flesh_and_Blood_TCG | Smash Palace: Chorus of Steel |  | 12 |
| 62_Flesh_and_Blood_TCG | Tales of Aria |  | 236 |
| 62_Flesh_and_Blood_TCG | The Hunted |  | 297 |
| 62_Flesh_and_Blood_TCG | Uprising |  | 97 |
| 62_Flesh_and_Blood_TCG | Usurp the Shadow Throne |  | 82 |
| 62_Flesh_and_Blood_TCG | Usurp the Shadow Throne Pre-release Cards |  | 4 |
| 62_Flesh_and_Blood_TCG | Welcome Deck Bravo |  | 18 |
| 62_Flesh_and_Blood_TCG | Welcome Deck: Ira |  | 12 |
| 62_Flesh_and_Blood_TCG | Welcome to Rathe |  | 302 |

### 63_Digimon_Card_Game（88 个系列，48 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 63_Digimon_Card_Game | Across Time | https://holodex-prod-bucket.b-cdn.net/sets/digi_23012/logo.webp | 49 |
| 63_Digimon_Card_Game | Across Time Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_23012/logo.webp ※ | 56 |
| 63_Digimon_Card_Game | Advanced Booster Digimon Generation |  | 100 |
| 63_Digimon_Card_Game | Alternative Being Booster | https://holodex-prod-bucket.b-cdn.net/sets/digi_23147/logo.webp | 115 |
| 63_Digimon_Card_Game | Battle of Omni | https://holodex-prod-bucket.b-cdn.net/sets/digi_2838/logo.webp | 164 |
| 63_Digimon_Card_Game | Battle of Omni Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_2838/logo.webp ※ | 34 |
| 63_Digimon_Card_Game | Blast Ace | https://holodex-prod-bucket.b-cdn.net/sets/digi_23178/logo.webp | 94 |
| 63_Digimon_Card_Game | Blast Ace Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_23178/logo.webp ※ | 48 |
| 63_Digimon_Card_Game | Chain of Liberation | https://holodex-prod-bucket.b-cdn.net/sets/digi_23775/logo.webp | 50 |
| 63_Digimon_Card_Game | Classic Collection | https://holodex-prod-bucket.b-cdn.net/sets/digi_2924/logo.webp | 50 |
| 63_Digimon_Card_Game | Cyber Eden | https://holodex-prod-bucket.b-cdn.net/sets/digi_24078/logo.webp | 160 |
| 63_Digimon_Card_Game | Cyber Eden Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_24078/logo.webp ※ | 48 |
| 63_Digimon_Card_Game | Dawn of Liberator | https://holodex-prod-bucket.b-cdn.net/sets/digi_24490/logo.webp | 50 |
| 63_Digimon_Card_Game | Digimon Demo Deck Exclusive Cards |  | 52 |
| 63_Digimon_Card_Game | Digimon LIBERATOR |  | 50 |
| 63_Digimon_Card_Game | Digimon Promotion Cards |  | 298 |
| 63_Digimon_Card_Game | Digital Hazard | https://holodex-prod-bucket.b-cdn.net/sets/digi_3072/logo.webp | 129 |
| 63_Digimon_Card_Game | Digital World Shambala | https://holodex-prod-bucket.b-cdn.net/sets/digi_24630/logo.webp | 156 |
| 63_Digimon_Card_Game | Dimensional Phase | https://holodex-prod-bucket.b-cdn.net/sets/digi_17691/logo.webp | 135 |
| 63_Digimon_Card_Game | Dimensional Phase Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_17691/logo.webp ※ | 56 |
| 63_Digimon_Card_Game | Double Diamond | https://holodex-prod-bucket.b-cdn.net/sets/digi_2880/logo.webp | 182 |
| 63_Digimon_Card_Game | Double Diamond Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_2880/logo.webp ※ | 56 |
| 63_Digimon_Card_Game | Draconic Roar | https://holodex-prod-bucket.b-cdn.net/sets/digi_3163/logo.webp | 50 |
| 63_Digimon_Card_Game | Dual Revolution | https://holodex-prod-bucket.b-cdn.net/sets/digi_24574/logo.webp | 50 |
| 63_Digimon_Card_Game | Exceed Apocalypse | https://holodex-prod-bucket.b-cdn.net/sets/digi_23254/logo.webp | 50 |
| 63_Digimon_Card_Game | Exceed Apocalypse Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_23254/logo.webp ※ | 58 |
| 63_Digimon_Card_Game | Great Legend Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_2763/logo.webp ※ | 56 |
| 63_Digimon_Card_Game | Hackers' Slumber | https://holodex-prod-bucket.b-cdn.net/sets/digi_24430/logo.webp | 139 |
| 63_Digimon_Card_Game | Hackers' Slumber Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_24430/logo.webp ※ | 50 |
| 63_Digimon_Card_Game | Infernal Ascension | https://holodex-prod-bucket.b-cdn.net/sets/digi_23414/logo.webp | 50 |
| 63_Digimon_Card_Game | Limited Card Pack -Another Knight- |  | 33 |
| 63_Digimon_Card_Game | Limited Card Pack -Billion Bullet- |  | 34 |
| 63_Digimon_Card_Game | Limited Card Pack -Final Crest- |  | 34 |
| 63_Digimon_Card_Game | New Awakening | https://holodex-prod-bucket.b-cdn.net/sets/digi_3035/logo.webp | 197 |
| 63_Digimon_Card_Game | New Awakening Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_3035/logo.webp ※ | 58 |
| 63_Digimon_Card_Game | Next Adventure Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_2945/logo.webp ※ | 56 |
| 63_Digimon_Card_Game | Release Special Booster 1.0 | https://holodex-prod-bucket.b-cdn.net/sets/digi_2733/logo.webp | 349 |
| 63_Digimon_Card_Game | Release Special Booster 1.5 | https://holodex-prod-bucket.b-cdn.net/sets/digi_24182/logo.webp | 189 |
| 63_Digimon_Card_Game | Release Special Booster 2.0 | https://holodex-prod-bucket.b-cdn.net/sets/digi_23767/logo.webp | 97 |
| 63_Digimon_Card_Game | Release Special Booster 2.0 Celebration Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_23767/logo.webp ※ | 68 |
| 63_Digimon_Card_Game | Release Special Booster 2.5 | https://holodex-prod-bucket.b-cdn.net/sets/digi_24178/logo.webp | 250 |
| 63_Digimon_Card_Game | Release Special Booster 2.5 Celebration Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_24178/logo.webp ※ | 79 |
| 63_Digimon_Card_Game | Resurgence Booster | https://holodex-prod-bucket.b-cdn.net/sets/digi_23017/logo.webp | 50 |
| 63_Digimon_Card_Game | Revision Pack Cards |  | 54 |
| 63_Digimon_Card_Game | Secret Crisis | https://holodex-prod-bucket.b-cdn.net/sets/digi_23557/logo.webp | 164 |
| 63_Digimon_Card_Game | Secret Crisis Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_23557/logo.webp ※ | 50 |
| 63_Digimon_Card_Game | Special Limited Set | https://holodex-prod-bucket.b-cdn.net/sets/digi_23850/logo.webp | 37 |
| 63_Digimon_Card_Game | Starter Deck 01: Gaia Red |  | 46 |
| 63_Digimon_Card_Game | Starter Deck 02: Cocytus Blue |  | 32 |
| 63_Digimon_Card_Game | Starter Deck 03: Heaven's Yellow |  | 35 |
| 63_Digimon_Card_Game | Starter Deck 04: Giga Green |  | 27 |
| 63_Digimon_Card_Game | Starter Deck 05: Machine Black |  | 20 |
| 63_Digimon_Card_Game | Starter Deck 06: Venomous Violet |  | 22 |
| 63_Digimon_Card_Game | Starter Deck 07: Gallantmon |  | 30 |
| 63_Digimon_Card_Game | Starter Deck 08: Ulforce Veedramon |  | 26 |
| 63_Digimon_Card_Game | Starter Deck 09: Ultimate Ancient Dragon |  | 30 |
| 63_Digimon_Card_Game | Starter Deck 10: Parallel World Tactician |  | 27 |
| 63_Digimon_Card_Game | Starter Deck 12: Jesmon |  | 24 |
| 63_Digimon_Card_Game | Starter Deck 13: Ragnaloardmon |  | 22 |
| 63_Digimon_Card_Game | Starter Deck 14: Beelzemon Advanced Deck Set Pre-Release Cards |  | 17 |
| 63_Digimon_Card_Game | Starter Deck 15: Dragon of Courage |  | 19 |
| 63_Digimon_Card_Game | Starter Deck 15: Dragon of Courage Pre-Release Cards |  | 14 |
| 63_Digimon_Card_Game | Starter Deck 16: Wolf of Friendship |  | 20 |
| 63_Digimon_Card_Game | Starter Deck 16: Wolf of Friendship Pre-Release Cards |  | 14 |
| 63_Digimon_Card_Game | Starter Deck 17: Double Typhoon Advanced Deck Set |  | 38 |
| 63_Digimon_Card_Game | Starter Deck 17: Double Typhoon Advanced Deck Set Pre-Release Cards |  | 13 |
| 63_Digimon_Card_Game | Starter Deck 18: Guardian Vortex |  | 21 |
| 63_Digimon_Card_Game | Starter Deck 19: Fable Waltz |  | 17 |
| 63_Digimon_Card_Game | Starter Deck 20: Protector of Light |  | 24 |
| 63_Digimon_Card_Game | Starter Deck 20: Protector of Light Release Event Cards |  | 11 |
| 63_Digimon_Card_Game | Starter Deck 21: Hero of Hope |  | 25 |
| 63_Digimon_Card_Game | Starter Deck 21: Hero of Hope Release Event Cards |  | 11 |
| 63_Digimon_Card_Game | Starter Deck 22: Amethyst Mandala Advanced Deck Set |  | 29 |
| 63_Digimon_Card_Game | Starter Deck 22: Amethyst Mandala Advanced Deck Set Release Event Cards |  | 5 |
| 63_Digimon_Card_Game | Starter Deck 23: Beatbreak |  | 25 |
| 63_Digimon_Card_Game | Starter Deck 23: Beatbreak Release Event Cards |  | 12 |
| 63_Digimon_Card_Game | Starter Deck 24: Data Squad |  | 16 |
| 63_Digimon_Card_Game | Starter Deck 24: Data Squad Release Event Cards |  | 12 |
| 63_Digimon_Card_Game | Time Stranger | https://holodex-prod-bucket.b-cdn.net/sets/digi_24531/logo.webp | 99 |
| 63_Digimon_Card_Game | Time Stranger Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_24531/logo.webp ※ | 50 |
| 63_Digimon_Card_Game | Timeless Bonds |  | 136 |
| 63_Digimon_Card_Game | Versus Royal Knights | https://holodex-prod-bucket.b-cdn.net/sets/digi_23148/logo.webp | 134 |
| 63_Digimon_Card_Game | Versus Royal Knights Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_23148/logo.webp ※ | 55 |
| 63_Digimon_Card_Game | World Convergence Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_24049/logo.webp ※ | 50 |
| 63_Digimon_Card_Game | X Record | https://holodex-prod-bucket.b-cdn.net/sets/digi_3103/logo.webp | 165 |
| 63_Digimon_Card_Game | X Record Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_3103/logo.webp ※ | 58 |
| 63_Digimon_Card_Game | Xros Encounter | https://holodex-prod-bucket.b-cdn.net/sets/digi_3112/logo.webp | 179 |
| 63_Digimon_Card_Game | Xros Encounter Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/digi_3112/logo.webp ※ | 56 |

### 65_Gate_Ruler（11 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 65_Gate_Ruler | Aces of the Cosmos, Assemble! |  | 198 |
| 65_Gate_Ruler | Become the Hero! |  | 198 |
| 65_Gate_Ruler | Dawn of the Multiverse Alliance |  | 195 |
| 65_Gate_Ruler | Gate Ruler Promo Cards |  | 32 |
| 65_Gate_Ruler | Onslaught of the Eldritch Gods |  | 194 |
| 65_Gate_Ruler | Shout with the Geas |  | 143 |
| 65_Gate_Ruler | Starter Deck: Giant Mechs & Yokai IN SPACE! |  | 19 |
| 65_Gate_Ruler | Starter Deck: March with the Dragon Lords |  | 18 |
| 65_Gate_Ruler | Starter Deck: New York Zombiepocalypse |  | 26 |
| 65_Gate_Ruler | Starter Deck: Summon the Fell Dragons! |  | 20 |
| 65_Gate_Ruler | The Demonic & the Divine |  | 115 |

### 66_MetaZoo（39 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 66_MetaZoo | Brilliant Aura Box |  | 10 |
| 66_MetaZoo | Caster's Cup Promo Cards |  | 139 |
| 66_MetaZoo | Cryptid Nation: First Edition |  | 159 |
| 66_MetaZoo | Cryptid Nation: First Edition Box Toppers |  | 11 |
| 66_MetaZoo | Cryptid Nation: First Edition Release Event Deck |  | 67 |
| 66_MetaZoo | Cryptid Nation: First Edition Tribal Theme Decks |  | 60 |
| 66_MetaZoo | Cryptid Nation: Kickstarter Edition |  | 159 |
| 66_MetaZoo | Cryptid Nation: Kickstarter Edition Tribal Theme Decks |  | 60 |
| 66_MetaZoo | Cryptid Nation: Second Edition |  | 153 |
| 66_MetaZoo | Cryptid Nation: Second Edition Box Toppers |  | 11 |
| 66_MetaZoo | Cryptid Nation: Second Edition Release Event Deck |  | 67 |
| 66_MetaZoo | Cryptid Nation: Second Edition Tribal Theme Decks |  | 60 |
| 66_MetaZoo | Dim Mak Promos |  | 7 |
| 66_MetaZoo | Fan Art Contest 2021 |  | 21 |
| 66_MetaZoo | Fan Art Contest 2022 |  | 30 |
| 66_MetaZoo | Hiroquest 2.0 |  | 153 |
| 66_MetaZoo | Hiroquest Promos |  | 66 |
| 66_MetaZoo | Holiday Promos |  | 70 |
| 66_MetaZoo | Kuromi’s Cryptid Carnival |  | 109 |
| 66_MetaZoo | Magicast April Fool’s Box 2022 |  | 8 |
| 66_MetaZoo | Medals |  | 28 |
| 66_MetaZoo | MetaZoo 30th Anniversary Box: 'Reprint' Edition |  | 16 |
| 66_MetaZoo | Metazoo USPCC Playing Cards: Kickstarter Edition |  | 15 |
| 66_MetaZoo | Miscellaneous Promos |  | 139 |
| 66_MetaZoo | Native: First Edition Release Event Deck |  | 60 |
| 66_MetaZoo | Nightfall: First Edition |  | 96 |
| 66_MetaZoo | Nightfall: First Edition Release Event Deck |  | 28 |
| 66_MetaZoo | Nightfall: First Edition Tribal Theme Decks |  | 66 |
| 66_MetaZoo | ReVive Skateboards Promos |  | 21 |
| 66_MetaZoo | Sample Cards |  | 54 |
| 66_MetaZoo | Seance: First Edition |  | 185 |
| 66_MetaZoo | Seance: First Edition Release Event Deck |  | 61 |
| 66_MetaZoo | UFO: First Edition Release Event Deck |  | 52 |
| 66_MetaZoo | UFO: First Edition Spoiler Pack |  | 161 |
| 66_MetaZoo | UFO: First Edition Tribal Theme Decks |  | 58 |
| 66_MetaZoo | Valentine’s Day Holiday Box 2022 |  | 12 |
| 66_MetaZoo | Wilderness: First Edition |  | 164 |
| 66_MetaZoo | Wilderness: First Edition Release Event Deck |  | 64 |
| 66_MetaZoo | Wilderness: First Edition Tribal Theme Decks |  | 63 |

### 67_WIXOSS（29 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 67_WIXOSS | Blue Archive DIVA |  | 293 |
| 67_WIXOSS | Changing Diva |  | 180 |
| 67_WIXOSS | Collab Booster: Nijisanji Diva |  | 99 |
| 67_WIXOSS | Concord Diva |  | 196 |
| 67_WIXOSS | Conflated Diva |  | 201 |
| 67_WIXOSS | Curiosity Diva |  | 181 |
| 67_WIXOSS | Dissonance Diva |  | 203 |
| 67_WIXOSS | Diva Debut Deck D01: Ancient Surprise |  | 21 |
| 67_WIXOSS | Diva Debut Deck D02: NIJISANJI ver. Sanbaka |  | 21 |
| 67_WIXOSS | Diva Debut Deck D03: Rei Hirana Akino |  | 21 |
| 67_WIXOSS | Diva Debut Deck D04: WOLF LION LOVIT |  | 21 |
| 67_WIXOSS | Diva Debut Deck D05: Bang Tamago Nova |  | 21 |
| 67_WIXOSS | Diva Debut Deck D06: Sanga Muzica Madoka |  | 21 |
| 67_WIXOSS | Diva Debut Deck D08: White Hope |  | 23 |
| 67_WIXOSS | Divisions DIVA |  | 224 |
| 67_WIXOSS | Fesonne Diva |  | 213 |
| 67_WIXOSS | Glowing Diva |  | 199 |
| 67_WIXOSS | Interlude Diva |  | 215 |
| 67_WIXOSS | Legendary DIVA |  | 202 |
| 67_WIXOSS | Prismatic Diva |  | 173 |
| 67_WIXOSS | Promo Cards |  | 475 |
| 67_WIXOSS | Reunion Diva |  | 100 |
| 67_WIXOSS | Spread Diva |  | 177 |
| 67_WIXOSS | Standup Diva |  | 181 |
| 67_WIXOSS | Super Diva Deck: Double Heroines |  | 56 |
| 67_WIXOSS | Super Diva Deck: Urith's MIASMA |  | 28 |
| 67_WIXOSS | Top Diva Deck: DXM |  | 22 |
| 67_WIXOSS | Welcome Back Diva -Lostorage- |  | 214 |
| 67_WIXOSS | Welcome Back Diva -selector- |  | 218 |

### 68_One_Piece_Card_Game（83 个系列，34 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 68_One_Piece_Card_Game | 500 Years in the Future | https://holodex-prod-bucket.b-cdn.net/sets/op_23387/logo.webp | 154 |
| 68_One_Piece_Card_Game | 500 Years in the Future Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23387/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | A Fist of Divine Speed | https://holodex-prod-bucket.b-cdn.net/sets/op_24241/logo.webp | 159 |
| 68_One_Piece_Card_Game | A Fist of Divine Speed Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24241/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | Adventure on Kami's Island | https://holodex-prod-bucket.b-cdn.net/sets/op_24637/logo.webp | 207 |
| 68_One_Piece_Card_Game | Adventure on Kami's Island Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24637/logo.webp ※ | 90 |
| 68_One_Piece_Card_Game | Awakening of the New Era | https://holodex-prod-bucket.b-cdn.net/sets/op_23213/logo.webp | 157 |
| 68_One_Piece_Card_Game | Awakening of the New Era: 1st Anniversary Tournament Cards |  | 75 |
| 68_One_Piece_Card_Game | Carrying On His Will | https://holodex-prod-bucket.b-cdn.net/sets/op_24303/logo.webp | 177 |
| 68_One_Piece_Card_Game | Carrying On His Will: 3rd Anniversary Tournament Cards |  | 79 |
| 68_One_Piece_Card_Game | Emperors in the New World | https://holodex-prod-bucket.b-cdn.net/sets/op_23589/logo.webp | 162 |
| 68_One_Piece_Card_Game | Emperors in the New World: 2nd Anniversary Tournament Cards |  | 75 |
| 68_One_Piece_Card_Game | Extra Booster: Anime 25th Collection | https://holodex-prod-bucket.b-cdn.net/sets/op_23834/logo.webp | 50 |
| 68_One_Piece_Card_Game | Extra Booster: One Piece Heroine's Edition Vol. 2 |  | 6 |
| 68_One_Piece_Card_Game | Extra Booster: One Piece Heroines Edition | https://holodex-prod-bucket.b-cdn.net/sets/op_24545/logo.webp | 102 |
| 68_One_Piece_Card_Game | Kingdoms of Intrigue | https://holodex-prod-bucket.b-cdn.net/sets/op_23024/logo.webp | 50 |
| 68_One_Piece_Card_Game | Kingdoms of Intrigue Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23024/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | Learn Together Deck Set |  | 51 |
| 68_One_Piece_Card_Game | Legacy of the Master | https://holodex-prod-bucket.b-cdn.net/sets/op_24302/logo.webp | 158 |
| 68_One_Piece_Card_Game | Legacy of the Master Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24302/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | One Piece Demo Deck Cards |  | 26 |
| 68_One_Piece_Card_Game | One Piece Promotion Cards |  | 100 |
| 68_One_Piece_Card_Game | Paramount War | https://holodex-prod-bucket.b-cdn.net/sets/op_17698/logo.webp | 156 |
| 68_One_Piece_Card_Game | Paramount War Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_17698/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | Pillars of Strength | https://holodex-prod-bucket.b-cdn.net/sets/op_22890/logo.webp | 155 |
| 68_One_Piece_Card_Game | Pillars of Strength Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_22890/logo.webp ※ | 77 |
| 68_One_Piece_Card_Game | Premium Booster -The Best- | https://holodex-prod-bucket.b-cdn.net/sets/op_23496/logo.webp | 54 |
| 68_One_Piece_Card_Game | Premium Booster -The Best- Vol. 2 | https://holodex-prod-bucket.b-cdn.net/sets/op_24305/logo.webp | 146 |
| 68_One_Piece_Card_Game | Revision Pack Cards |  | 33 |
| 68_One_Piece_Card_Game | Romance Dawn | https://holodex-prod-bucket.b-cdn.net/sets/op_3188/logo.webp | 156 |
| 68_One_Piece_Card_Game | Royal Blood | https://holodex-prod-bucket.b-cdn.net/sets/op_23766/logo.webp | 152 |
| 68_One_Piece_Card_Game | Royal Blood Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23766/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | Starter Deck 11: Uta |  | 5 |
| 68_One_Piece_Card_Game | Starter Deck 12: Zoro and Sanji |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 14: 3D2Y |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 15: RED Edward.Newgate |  | 13 |
| 68_One_Piece_Card_Game | Starter Deck 16: GREEN Uta |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 17: BLUE Donquixote Doflamingo |  | 10 |
| 68_One_Piece_Card_Game | Starter Deck 18: PURPLE Monkey.D.Luffy |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 19: BLACK Smoker |  | 14 |
| 68_One_Piece_Card_Game | Starter Deck 1: Straw Hat Crew |  | 18 |
| 68_One_Piece_Card_Game | Starter Deck 20: YELLOW Charlotte Katakuri |  | 11 |
| 68_One_Piece_Card_Game | Starter Deck 22: Ace & Newgate |  | 31 |
| 68_One_Piece_Card_Game | Starter Deck 23: RED Shanks |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 24: GREEN Jewelry Bonney |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 25: BLUE Buggy |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 26: PURPLE/BLACK Monkey.D.Luffy |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 27: BLACK Marshall.D.Teach |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 28: GREEN/YELLOW Yamato |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 29: Egghead |  | 31 |
| 68_One_Piece_Card_Game | Starter Deck 2: Worst Generation |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 31: RED Monkey.D.Luffy |  | 10 |
| 68_One_Piece_Card_Game | Starter Deck 32: GREEN Roronoa Zoro |  | 9 |
| 68_One_Piece_Card_Game | Starter Deck 33: BLUE Kuzan |  | 9 |
| 68_One_Piece_Card_Game | Starter Deck 34: PURPLE Charlotte Katakuri |  | 10 |
| 68_One_Piece_Card_Game | Starter Deck 35: RED/BLACK Sabo |  | 9 |
| 68_One_Piece_Card_Game | Starter Deck 36: YELLOW Eustass"Captain"Kid |  | 11 |
| 68_One_Piece_Card_Game | Starter Deck 3: The Seven Warlords of The Sea |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 4: Animal Kingdom Pirates |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 5: Film Edition |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 6: Absolute Justice |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 7: Big Mom Pirates |  | 17 |
| 68_One_Piece_Card_Game | Starter Deck 8: Monkey.D.Luffy |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck 9: Yamato |  | 15 |
| 68_One_Piece_Card_Game | Starter Deck EX: Gear 5 |  | 33 |
| 68_One_Piece_Card_Game | Starter Deck EX: Luffy & Ace |  | 34 |
| 68_One_Piece_Card_Game | Super Pre-Release Starter Deck 1: Straw Hat Crew |  | 18 |
| 68_One_Piece_Card_Game | Super Pre-Release Starter Deck 2: Worst Generation |  | 17 |
| 68_One_Piece_Card_Game | Super Pre-Release Starter Deck 3: The Seven Warlords of the Sea |  | 17 |
| 68_One_Piece_Card_Game | Super Pre-Release Starter Deck 4: Animal Kingdom Pirates |  | 17 |
| 68_One_Piece_Card_Game | The Azure Sea's Seven | https://holodex-prod-bucket.b-cdn.net/sets/op_24537/logo.webp | 150 |
| 68_One_Piece_Card_Game | The Azure Sea's Seven Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24537/logo.webp ※ | 89 |
| 68_One_Piece_Card_Game | The Dominance of God |  | 6 |
| 68_One_Piece_Card_Game | The Time of Battle | https://holodex-prod-bucket.b-cdn.net/sets/op_24664/logo.webp | 159 |
| 68_One_Piece_Card_Game | The Time of Battle Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_24664/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | The World's Strongest Warriors | https://holodex-prod-bucket.b-cdn.net/sets/op_1724736/logo.webp | 177 |
| 68_One_Piece_Card_Game | The World's Strongest Warriors Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_1724736/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | Two Legends | https://holodex-prod-bucket.b-cdn.net/sets/op_23462/logo.webp | 50 |
| 68_One_Piece_Card_Game | Two Legends Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23462/logo.webp ※ | 75 |
| 68_One_Piece_Card_Game | Ultra Deck: The Three Brothers |  | 35 |
| 68_One_Piece_Card_Game | Ultra Deck: The Three Captains |  | 18 |
| 68_One_Piece_Card_Game | Wings of the Captain | https://holodex-prod-bucket.b-cdn.net/sets/op_23272/logo.webp | 154 |
| 68_One_Piece_Card_Game | Wings of the Captain Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/op_23272/logo.webp ※ | 75 |

### 71_Disney_Lorcana（18 个系列，14 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 71_Disney_Lorcana | Archazia's Island | https://holodex-prod-bucket.b-cdn.net/sets/dl_24011/logo.webp | 245 |
| 71_Disney_Lorcana | Attack of the Vine! | https://holodex-prod-bucket.b-cdn.net/sets/dl_24666/logo.webp | 261 |
| 71_Disney_Lorcana | Azurite Sea | https://holodex-prod-bucket.b-cdn.net/sets/dl_23746/logo.webp | 149 |
| 71_Disney_Lorcana | D23 Promos | https://holodex-prod-bucket.b-cdn.net/sets/dl_17690/logo.webp | 23 |
| 71_Disney_Lorcana | Disney Lorcana Promo Cards | https://holodex-prod-bucket.b-cdn.net/sets/dl_23234/logo.webp | 172 |
| 71_Disney_Lorcana | Disney100 Promos |  | 6 |
| 71_Disney_Lorcana | Fabled | https://holodex-prod-bucket.b-cdn.net/sets/dl_24348/logo.webp | 253 |
| 71_Disney_Lorcana | Illumineer's Quest: Deep Trouble |  | 39 |
| 71_Disney_Lorcana | Illumineer's Quest: Palace Heist |  | 43 |
| 71_Disney_Lorcana | Illumineer's Quest: The Great Hunny Rescue |  | 5 |
| 71_Disney_Lorcana | Into the Inklands | https://holodex-prod-bucket.b-cdn.net/sets/dl_23367/logo.webp | 150 |
| 71_Disney_Lorcana | Reign of Jafar | https://holodex-prod-bucket.b-cdn.net/sets/dl_24258/logo.webp | 100 |
| 71_Disney_Lorcana | Rise of the Floodborn | https://holodex-prod-bucket.b-cdn.net/sets/dl_23303/logo.webp | 223 |
| 71_Disney_Lorcana | The First Chapter | https://holodex-prod-bucket.b-cdn.net/sets/dl_22937/logo.webp | 222 |
| 71_Disney_Lorcana | Ursula's Return | https://holodex-prod-bucket.b-cdn.net/sets/dl_23474/logo.webp | 232 |
| 71_Disney_Lorcana | Whispers in the Well | https://holodex-prod-bucket.b-cdn.net/sets/dl_24414/logo.webp | 150 |
| 71_Disney_Lorcana | Wilds Unknown | https://holodex-prod-bucket.b-cdn.net/sets/dl_24617/logo.webp | 200 |
| 71_Disney_Lorcana | Winterspell | https://holodex-prod-bucket.b-cdn.net/sets/dl_24500/logo.webp | 266 |

### 72_Battle_Spirits_Saga（18 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 72_Battle_Spirits_Saga | Aquatic Invaders |  | 50 |
| 72_Battle_Spirits_Saga | Battle Spirits Saga Promo Cards |  | 262 |
| 72_Battle_Spirits_Saga | Collaboration Booster 01: Halo of Awakening |  | 104 |
| 72_Battle_Spirits_Saga | Collaboration Booster 01: Halo of Awakening Pre-Release Cards |  | 30 |
| 72_Battle_Spirits_Saga | Expansion Set 01: Elemental Spark |  | 9 |
| 72_Battle_Spirits_Saga | Generational Link |  | 138 |
| 72_Battle_Spirits_Saga | Launch & Event Promos |  | 257 |
| 72_Battle_Spirits_Saga | Lore Set 01: Ancient Heroes |  | 10 |
| 72_Battle_Spirits_Saga | Savior of Chaos |  | 46 |
| 72_Battle_Spirits_Saga | Savior of Chaos Pre-Release Cards |  | 74 |
| 72_Battle_Spirits_Saga | Starter Deck 01: Dragon Onslaught |  | 28 |
| 72_Battle_Spirits_Saga | Starter Deck 02: Call of the Curse |  | 16 |
| 72_Battle_Spirits_Saga | Starter Deck 03: Aegis of the Machine |  | 16 |
| 72_Battle_Spirits_Saga | Starter Deck 04: Forbidden Magic |  | 16 |
| 72_Battle_Spirits_Saga | Starter Deck 05: Verdant Wings |  | 16 |
| 72_Battle_Spirits_Saga | Starter Deck 06: Bodies of Steel |  | 16 |
| 72_Battle_Spirits_Saga | Starter Deck 07: Destined Assault |  | 18 |
| 72_Battle_Spirits_Saga | Strangers in the Sky |  | 99 |

### 73_Shadowverse_Evolve（46 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 73_Shadowverse_Evolve | BP01: Advent of Genesis |  | 269 |
| 73_Shadowverse_Evolve | BP02: Reign of Bahamut |  | 201 |
| 73_Shadowverse_Evolve | BP03: Flame of Laevateinn |  | 198 |
| 73_Shadowverse_Evolve | BP04: Cosmic Mythos |  | 208 |
| 73_Shadowverse_Evolve | BP05: Omens Eternal |  | 209 |
| 73_Shadowverse_Evolve | BP06: Paragons of the Colosseum |  | 189 |
| 73_Shadowverse_Evolve | BP07: Verdant Steel |  | 188 |
| 73_Shadowverse_Evolve | BP08: Alterchaotica |  | 185 |
| 73_Shadowverse_Evolve | BP09: Duet of Dawn and Dusk |  | 240 |
| 73_Shadowverse_Evolve | BP10: Gods of the Arcana |  | 218 |
| 73_Shadowverse_Evolve | BP11: Bullet of Fate |  | 187 |
| 73_Shadowverse_Evolve | BP12: Worldreaver’s Descent |  | 190 |
| 73_Shadowverse_Evolve | BP13: Dominion of Darkness |  | 191 |
| 73_Shadowverse_Evolve | BP14: Banquet of Dreams |  | 192 |
| 73_Shadowverse_Evolve | BP15: Trial of the Omens |  | 233 |
| 73_Shadowverse_Evolve | BP16: New World Genesis |  | 216 |
| 73_Shadowverse_Evolve | BP18: Neometropolis |  | 150 |
| 73_Shadowverse_Evolve | CP01: Umamusume: Pretty Derby |  | 200 |
| 73_Shadowverse_Evolve | CP02: THE IDOLM@STER CINDERELLA GIRLS |  | 272 |
| 73_Shadowverse_Evolve | CP03: Cardfight!! Vanguard |  | 100 |
| 73_Shadowverse_Evolve | CP04: Princess Connect! Re:Dive |  | 248 |
| 73_Shadowverse_Evolve | CSD01: Ready, Set, Umamusume! |  | 34 |
| 73_Shadowverse_Evolve | CSD02: THE IDOLM@STER CINDERELLA GIRLS |  | 96 |
| 73_Shadowverse_Evolve | CSD03: Cardfight!! Vanguard |  | 60 |
| 73_Shadowverse_Evolve | ECP01: Umamusume: Pretty Derby |  | 100 |
| 73_Shadowverse_Evolve | GFB01: Guide to Glory |  | 282 |
| 73_Shadowverse_Evolve | GFD01: Luxheart Legends |  | 75 |
| 73_Shadowverse_Evolve | GFD02: Treacherous Ambitions |  | 75 |
| 73_Shadowverse_Evolve | Gloryfinder Events |  | 22 |
| 73_Shadowverse_Evolve | SD01: Regal Fairy Princess |  | 22 |
| 73_Shadowverse_Evolve | SD02: Blade of Resentment |  | 23 |
| 73_Shadowverse_Evolve | SD03: Mysteries of Conjuration |  | 23 |
| 73_Shadowverse_Evolve | SD04: Wrath of the Greatwyrm |  | 23 |
| 73_Shadowverse_Evolve | SD05: Waltz of the Undying Night |  | 23 |
| 73_Shadowverse_Evolve | SD06: Maculate Ablution |  | 23 |
| 73_Shadowverse_Evolve | SDD01: Showdown Deck: Forestcraft |  | 23 |
| 73_Shadowverse_Evolve | SDD02: Showdown Deck: Swordcraft |  | 26 |
| 73_Shadowverse_Evolve | SDD03: Showdown Deck: Runecraft |  | 30 |
| 73_Shadowverse_Evolve | SDD04: Showdown Deck: Dragoncraft |  | 19 |
| 73_Shadowverse_Evolve | SDD05: Showdown Deck: Abysscraft |  | 23 |
| 73_Shadowverse_Evolve | SDD06: Showdown Deck: Havencraft |  | 19 |
| 73_Shadowverse_Evolve | SP01: Seaside Memories |  | 172 |
| 73_Shadowverse_Evolve | SS01: Worlds Beyond (Swordcraft) |  | 7 |
| 73_Shadowverse_Evolve | SS02: Worlds Beyond (Dragoncraft) |  | 7 |
| 73_Shadowverse_Evolve | Shadowverse: Evolve Bundles |  | 1 |
| 73_Shadowverse_Evolve | Shadowverse: Evolve Promo Cards |  | 248 |

### 74_Grand_Archive_TCG（42 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 74_Grand_Archive_TCG | .asphodel/paradise |  | 385 |
| 74_Grand_Archive_TCG | .asphodel/paradise Starter Decks |  | 63 |
| 74_Grand_Archive_TCG | 2022 Demo Deck |  | 20 |
| 74_Grand_Archive_TCG | 2023 Demo Deck |  | 29 |
| 74_Grand_Archive_TCG | Abyssal Heaven |  | 230 |
| 74_Grand_Archive_TCG | Abyssal Heaven Event Pack |  | 2 |
| 74_Grand_Archive_TCG | Alchemical Revolution |  | 162 |
| 74_Grand_Archive_TCG | Alchemical Revolution Alter Edition |  | 37 |
| 74_Grand_Archive_TCG | Alchemical Revolution Event Pack |  | 3 |
| 74_Grand_Archive_TCG | Alchemical Revolution Starter Decks |  | 111 |
| 74_Grand_Archive_TCG | Dawn of Ashes Event Pack |  | 3 |
| 74_Grand_Archive_TCG | Dawn of Ashes Prelude |  | 118 |
| 74_Grand_Archive_TCG | Dawn of Ashes Starter Decks |  | 109 |
| 74_Grand_Archive_TCG | Diao Chan Re: Collection, Idyll Corsage |  | 41 |
| 74_Grand_Archive_TCG | Distorted Reflections Starter Decks |  | 61 |
| 74_Grand_Archive_TCG | Fractured Crown |  | 123 |
| 74_Grand_Archive_TCG | Guo Jia Re: Collection, Heaven’s Favored |  | 38 |
| 74_Grand_Archive_TCG | Kickstarter Promotional Cards |  | 8 |
| 74_Grand_Archive_TCG | Mercurial Heart |  | 207 |
| 74_Grand_Archive_TCG | Mercurial Heart Alter Edition |  | 35 |
| 74_Grand_Archive_TCG | Merlin Re: Collection, Brilliant Vestige |  | 40 |
| 74_Grand_Archive_TCG | Mordred Re: Collection, Aurelian Regent |  | 35 |
| 74_Grand_Archive_TCG | Mortal Ambition Alter Edition |  | 33 |
| 74_Grand_Archive_TCG | Mortal Ambition Draft Pack |  | 43 |
| 74_Grand_Archive_TCG | Mortal Ambition Event Pack |  | 2 |
| 74_Grand_Archive_TCG | Mortal Ambition Starter Decks |  | 63 |
| 74_Grand_Archive_TCG | Phantom Monarchs Event Pack |  | 26 |
| 74_Grand_Archive_TCG | Promotional Cards |  | 389 |
| 74_Grand_Archive_TCG | Proxia's Vault |  | 13 |
| 74_Grand_Archive_TCG | Radiant Origins |  | 595 |
| 74_Grand_Archive_TCG | Radiant Origins Event Pack |  | 28 |
| 74_Grand_Archive_TCG | Radiant Origins: Pantheon |  | 300 |
| 74_Grand_Archive_TCG | Region Exclusive Promotional Cards |  | 8 |
| 74_Grand_Archive_TCG | Silvie Re:Collection, Slime Sovereign |  | 34 |
| 74_Grand_Archive_TCG | Silvie, Slime Sovereign Re: Collection Lite |  | 33 |
| 74_Grand_Archive_TCG | SquareLive Collaboration |  | 19 |
| 74_Grand_Archive_TCG | Supporter Pack 1 |  | 27 |
| 74_Grand_Archive_TCG | Supporter Pack 2 |  | 43 |
| 74_Grand_Archive_TCG | Supporter Pack 3 |  | 34 |
| 74_Grand_Archive_TCG | Supporter Pack 4 |  | 59 |
| 74_Grand_Archive_TCG | Tristan Re:Collection, Shadowdancer |  | 34 |
| 74_Grand_Archive_TCG | Tristan, Shadowdancer Re:Collection Lite |  | 33 |

### 75_Akora_TCG（8 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 75_Akora_TCG | Afelium Unleashed [1st Edition] |  | 298 |
| 75_Akora_TCG | Eternal Echoes [1st Edition] |  | 370 |
| 75_Akora_TCG | Grordhelm Uprising [1st Edition] |  | 315 |
| 75_Akora_TCG | Spellbound Wings [1st Edition] |  | 235 |
| 75_Akora_TCG | Spellbound Wings [Kickstarter Edition] |  | 150 |
| 75_Akora_TCG | Trials of Ikithia [1st Edition] |  | 341 |
| 75_Akora_TCG | Trials of Ikithia [eBay 1st Edition] |  | 349 |
| 75_Akora_TCG | Warped Crusaders [1st Edition] |  | 161 |

### 76_Kryptik_TCG（5 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 76_Kryptik_TCG | Genesis [Kickstarter] |  | 682 |
| 76_Kryptik_TCG | Genesis [Wave 2] |  | 432 |
| 76_Kryptik_TCG | Kryptik Promos |  | 47 |
| 76_Kryptik_TCG | Wicked Prophecy [Wave 1] |  | 1050 |
| 76_Kryptik_TCG | Wicked Prophecy [Wave 1] (eBay Gen Con Exclusive) |  | 718 |

### 77_Sorcery_Contested_Realm（7 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 77_Sorcery_Contested_Realm | Alpha |  | 911 |
| 77_Sorcery_Contested_Realm | Arthurian Legends |  | 448 |
| 77_Sorcery_Contested_Realm | Arthurian Legends Promo |  | 2 |
| 77_Sorcery_Contested_Realm | Beta |  | 812 |
| 77_Sorcery_Contested_Realm | Dragonlord |  | 26 |
| 77_Sorcery_Contested_Realm | Dust Reward Promos |  | 31 |
| 77_Sorcery_Contested_Realm | Gothic |  | 550 |

### 78_Alpha_Clash（17 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 78_Alpha_Clash | Alpha Clash Promo Cards |  | 11 |
| 78_Alpha_Clash | Ancient Alphas |  | 233 |
| 78_Alpha_Clash | Champion Deck: Brandon Nieves |  | 26 |
| 78_Alpha_Clash | Champion Deck: Michael Hamilton |  | 20 |
| 78_Alpha_Clash | Champion Deck: Zach Bunn |  | 19 |
| 78_Alpha_Clash | Clashgrounds |  | 176 |
| 78_Alpha_Clash | Echoes of Eternity |  | 222 |
| 78_Alpha_Clash | Equilibrium |  | 205 |
| 78_Alpha_Clash | Genesis Returns |  | 204 |
| 78_Alpha_Clash | Spoils of the Forgotten |  | 56 |
| 78_Alpha_Clash | Spoils of the Vault |  | 62 |
| 78_Alpha_Clash | The Awakening |  | 159 |
| 78_Alpha_Clash | The Awakening (Kickstarter) |  | 155 |
| 78_Alpha_Clash | The Awakening Novel Kickstarter |  | 4 |
| 78_Alpha_Clash | The Vault Trials |  | 121 |
| 78_Alpha_Clash | Unrivaled |  | 180 |
| 78_Alpha_Clash | Year of the Dragon |  | 208 |

### 79_Star_Wars_Unlimited（29 个系列，16 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 79_Star_Wars_Unlimited | 2024 Convention Exclusive |  | 6 |
| 79_Star_Wars_Unlimited | 2025 Convention Exclusive |  | 6 |
| 79_Star_Wars_Unlimited | 2025 Gift Box |  | 2 |
| 79_Star_Wars_Unlimited | 2026 Convention Exclusive |  | 6 |
| 79_Star_Wars_Unlimited | A Lawless Time | https://holodex-prod-bucket.b-cdn.net/sets/swu_24572/logo.webp | 92 |
| 79_Star_Wars_Unlimited | A Lawless Time: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_24572/logo.webp ※ | 40 |
| 79_Star_Wars_Unlimited | Ashes of the Empire | https://holodex-prod-bucket.b-cdn.net/sets/swu_ashes24660/logo.webp | 951 |
| 79_Star_Wars_Unlimited | Ashes of the Empire - Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_ashes24660/logo.webp ※ | 40 |
| 79_Star_Wars_Unlimited | Event Exclusive Promos |  | 7 |
| 79_Star_Wars_Unlimited | Galactic Championship 2026 |  | 94 |
| 79_Star_Wars_Unlimited | Gamegenic Promos |  | 6 |
| 79_Star_Wars_Unlimited | Intro Battle: Hoth |  | 104 |
| 79_Star_Wars_Unlimited | Judge Promos |  | 57 |
| 79_Star_Wars_Unlimited | Jump to Lightspeed | https://holodex-prod-bucket.b-cdn.net/sets/swu_23956/logo.webp | 1154 |
| 79_Star_Wars_Unlimited | Jump to Lightspeed: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_23956/logo.webp ※ | 40 |
| 79_Star_Wars_Unlimited | Legends of the Force | https://holodex-prod-bucket.b-cdn.net/sets/swu_24279/logo.webp | 146 |
| 79_Star_Wars_Unlimited | Legends of the Force: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_24279/logo.webp ※ | 40 |
| 79_Star_Wars_Unlimited | Organized Play Promos |  | 142 |
| 79_Star_Wars_Unlimited | Prerelease Promos |  | 6 |
| 79_Star_Wars_Unlimited | Secrets of Power | https://holodex-prod-bucket.b-cdn.net/sets/swu_24387/logo.webp | 1198 |
| 79_Star_Wars_Unlimited | Secrets of Power: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_24387/logo.webp ※ | 40 |
| 79_Star_Wars_Unlimited | Sector and Regional Promos: Season 1 |  | 128 |
| 79_Star_Wars_Unlimited | Shadows of the Galaxy | https://holodex-prod-bucket.b-cdn.net/sets/swu_23488/logo.webp | 536 |
| 79_Star_Wars_Unlimited | Shadows of the Galaxy: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_23488/logo.webp ※ | 20 |
| 79_Star_Wars_Unlimited | Spark of Rebellion | https://holodex-prod-bucket.b-cdn.net/sets/swu_23405/logo.webp | 543 |
| 79_Star_Wars_Unlimited | Spark of Rebellion: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_23405/logo.webp ※ | 20 |
| 79_Star_Wars_Unlimited | Twilight of the Republic | https://holodex-prod-bucket.b-cdn.net/sets/swu_23597/logo.webp | 541 |
| 79_Star_Wars_Unlimited | Twilight of the Republic: Weekly Play Promos | https://holodex-prod-bucket.b-cdn.net/sets/swu_23597/logo.webp ※ | 20 |
| 79_Star_Wars_Unlimited | Twin Suns |  | 84 |

### 80_Dragon_Ball_Super_Fusion_World（48 个系列，31 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 80_Dragon_Ball_Super_Fusion_World | Awakened Pulse | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23401/logo.webp | 164 |
| 80_Dragon_Ball_Super_Fusion_World | Awakened Pulse Alternate Art Reprints | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23505/logo.webp | 6 |
| 80_Dragon_Ball_Super_Fusion_World | Awakened Pulse Pre-Release Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23407/logo.webp | 88 |
| 80_Dragon_Ball_Super_Fusion_World | Blazing Aura | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23470/logo.webp | 160 |
| 80_Dragon_Ball_Super_Fusion_World | Blazing Aura Alternate Art Reprints | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24183/logo.webp | 6 |
| 80_Dragon_Ball_Super_Fusion_World | Blazing Aura Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23471/logo.webp | 89 |
| 80_Dragon_Ball_Super_Fusion_World | Cross Force | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24604/logo.webp | 163 |
| 80_Dragon_Ball_Super_Fusion_World | Cross Force Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24604/logo.webp ※ | 75 |
| 80_Dragon_Ball_Super_Fusion_World | Dual Evolution | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24569/logo.webp | 165 |
| 80_Dragon_Ball_Super_Fusion_World | Dual Evolution Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24569/logo.webp ※ | 75 |
| 80_Dragon_Ball_Super_Fusion_World | Fusion World Energy Markers | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23430/logo.webp | 100 |
| 80_Dragon_Ball_Super_Fusion_World | Fusion World Promotion Cards and Packs | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23428/logo.webp | 114 |
| 80_Dragon_Ball_Super_Fusion_World | Manga Booster 01 | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24335/logo.webp | 135 |
| 80_Dragon_Ball_Super_Fusion_World | Manga Booster 01 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24368/logo.webp | 69 |
| 80_Dragon_Ball_Super_Fusion_World | Manga Booster 02 | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24288/logo.webp | 136 |
| 80_Dragon_Ball_Super_Fusion_World | Manga Booster 02 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24492/logo.webp | 69 |
| 80_Dragon_Ball_Super_Fusion_World | New Adventure | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23928/logo.webp | 142 |
| 80_Dragon_Ball_Super_Fusion_World | New Adventure Alternate Art Reprints | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24311/logo.webp | 1 |
| 80_Dragon_Ball_Super_Fusion_World | New Adventure Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24186/logo.webp | 70 |
| 80_Dragon_Ball_Super_Fusion_World | Raging Roar | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23517/logo.webp | 157 |
| 80_Dragon_Ball_Super_Fusion_World | Raging Roar Alternate Art Reprints | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23823/logo.webp | 8 |
| 80_Dragon_Ball_Super_Fusion_World | Raging Roar Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23518/logo.webp | 91 |
| 80_Dragon_Ball_Super_Fusion_World | Rivals Clash | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24247/logo.webp | 139 |
| 80_Dragon_Ball_Super_Fusion_World | Rivals Clash Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24248/logo.webp | 76 |
| 80_Dragon_Ball_Super_Fusion_World | Saiyan's Pride | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24450/logo.webp | 95 |
| 80_Dragon_Ball_Super_Fusion_World | Saiyan's Pride Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24518/logo.webp | 70 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 10: Giblet |  | 37 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 1: Son Goku |  | 24 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 1: Son Goku Alternate Art Reprints |  | 1 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 2: Vegeta |  | 24 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 3: Broly |  | 25 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 3: Broly Alternate Art Reprints |  | 1 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 4: Frieza |  | 24 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 4: Frieza Alternate Art Reprints |  | 2 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 5: Bardock |  | 24 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 5: Bardock Alternate Art Reprints |  | 2 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 6: Son Goku (Mini) |  | 19 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 7: Vegeta (Mini) |  | 19 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 8: Vegeta (Mini) Super Saiyan 3 |  | 24 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck 9: Shallot |  | 37 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck EX: The Beat of Ki |  | 37 |
| 80_Dragon_Ball_Super_Fusion_World | Starter Deck EX: The Phase of Evolution |  | 37 |
| 80_Dragon_Ball_Super_Fusion_World | Story Booster 01 |  | 148 |
| 80_Dragon_Ball_Super_Fusion_World | Tournament and Championship Promos | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23429/logo.webp | 437 |
| 80_Dragon_Ball_Super_Fusion_World | Ultra Limit | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23658/logo.webp | 155 |
| 80_Dragon_Ball_Super_Fusion_World | Ultra Limit Alternate Art Reprints | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24184/logo.webp | 5 |
| 80_Dragon_Ball_Super_Fusion_World | Ultra Limit Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_23769/logo.webp | 81 |
| 80_Dragon_Ball_Super_Fusion_World | Wish For Shenron Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/dbf_24419/logo.webp | 70 |

### 81_Union_Arena（63 个系列，47 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 81_Union_Arena | UE01BT: BLEACH: Thousand-Year Blood War | https://holodex-prod-bucket.b-cdn.net/sets/union_23522/logo.webp | 98 |
| 81_Union_Arena | UE01BT: BLEACH: Thousand-Year Blood War Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23522/logo.webp ※ | 71 |
| 81_Union_Arena | UE01NC: New Card Selection: BLEACH: Thousand-Year Blood War |  | 12 |
| 81_Union_Arena | UE01ST: BLEACH: Thousand-Year Blood War Starter Deck |  | 22 |
| 81_Union_Arena | UE01ST: BLEACH: Thousand-Year Blood War Super Pre-Release Starter Deck |  | 21 |
| 81_Union_Arena | UE02BT: HUNTER X HUNTER Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23521/logo.webp ※ | 75 |
| 81_Union_Arena | UE02ST: HUNTER X HUNTER Starter Deck |  | 22 |
| 81_Union_Arena | UE02ST: HUNTER X HUNTER Super Pre-Release Starter Deck |  | 21 |
| 81_Union_Arena | UE03BT: Jujutsu Kaisen | https://holodex-prod-bucket.b-cdn.net/sets/union_23526/logo.webp | 133 |
| 81_Union_Arena | UE03BT: Jujutsu Kaisen Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23526/logo.webp ※ | 72 |
| 81_Union_Arena | UE03ST: Jujutsu Kaisen Starter Deck |  | 22 |
| 81_Union_Arena | UE04BT: CODE GEASS: Lelouch of the Rebellion | https://holodex-prod-bucket.b-cdn.net/sets/union_23757/logo.webp | 143 |
| 81_Union_Arena | UE04BT: CODE GEASS: Lelouch of the Rebellion Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23757/logo.webp ※ | 77 |
| 81_Union_Arena | UE05BT: Demon Slayer: Kimetsu no Yaiba Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23790/logo.webp ※ | 78 |
| 81_Union_Arena | UE05ST: Demon Slayer: Kimetsu no Yaiba Starter Deck |  | 22 |
| 81_Union_Arena | UE06BT: One Punch Man | https://holodex-prod-bucket.b-cdn.net/sets/union_23780/logo.webp | 144 |
| 81_Union_Arena | UE06BT: One Punch Man Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23780/logo.webp ※ | 72 |
| 81_Union_Arena | UE06ST: One Punch Man Starter Deck |  | 22 |
| 81_Union_Arena | UE07BT: Sword Art Online | https://holodex-prod-bucket.b-cdn.net/sets/union_23954/logo.webp | 95 |
| 81_Union_Arena | UE07BT: Sword Art Online Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_23954/logo.webp ※ | 72 |
| 81_Union_Arena | UE07ST: Sword Art Online Starter Deck |  | 22 |
| 81_Union_Arena | UE08BT: Black Clover | https://holodex-prod-bucket.b-cdn.net/sets/union_24015/logo.webp | 139 |
| 81_Union_Arena | UE08BT: Black Clover Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24015/logo.webp ※ | 71 |
| 81_Union_Arena | UE08ST: Black Clover Starter Deck |  | 27 |
| 81_Union_Arena | UE09BT: FULLMETAL ALCHEMIST | https://holodex-prod-bucket.b-cdn.net/sets/union_24065/logo.webp | 118 |
| 81_Union_Arena | UE09BT: FULLMETAL ALCHEMIST Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24065/logo.webp ※ | 72 |
| 81_Union_Arena | UE09ST: FULLMETAL ALCHEMIST Starter Deck |  | 27 |
| 81_Union_Arena | UE10BT: Attack on Titan | https://holodex-prod-bucket.b-cdn.net/sets/union_24237/logo.webp | 96 |
| 81_Union_Arena | UE10BT: Attack on Titan Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24237/logo.webp ※ | 4 |
| 81_Union_Arena | UE10ST: Attack on Titan Starter Deck |  | 27 |
| 81_Union_Arena | UE11BT: Rurouni Kenshin Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24255/logo.webp ※ | 72 |
| 81_Union_Arena | UE11ST: Rurouni Kenshin Starter Deck |  | 27 |
| 81_Union_Arena | UE12BT: Kaiju No. 8 | https://holodex-prod-bucket.b-cdn.net/sets/union_24261/logo.webp | 120 |
| 81_Union_Arena | UE12BT: Kaiju No. 8 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24261/logo.webp ※ | 60 |
| 81_Union_Arena | UE13BT: Yu Yu Hakusho: Ghost Files | https://holodex-prod-bucket.b-cdn.net/sets/union_24262/logo.webp | 171 |
| 81_Union_Arena | UE13BT: Yu Yu Hakusho: Ghost Files Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24262/logo.webp ※ | 77 |
| 81_Union_Arena | UE14BT: GODDESS OF VICTORY: NIKKE | https://holodex-prod-bucket.b-cdn.net/sets/union_24328/logo.webp | 178 |
| 81_Union_Arena | UE14BT: GODDESS OF VICTORY: NIKKE Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24328/logo.webp ※ | 77 |
| 81_Union_Arena | UE15BT: Evangelion: New Theatrical Edition | https://holodex-prod-bucket.b-cdn.net/sets/union_24507/logo.webp | 138 |
| 81_Union_Arena | UE15BT: Evangelion: New Theatrical Edition Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24507/logo.webp ※ | 70 |
| 81_Union_Arena | UE15ST: Evangelion: New Theatrical Edition Starter Deck |  | 27 |
| 81_Union_Arena | UE16BT: KAGURABACHI Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24510/logo.webp ※ | 62 |
| 81_Union_Arena | UE17BT: SOLO LEVELING | https://holodex-prod-bucket.b-cdn.net/sets/union_24511/logo.webp | 48 |
| 81_Union_Arena | UE17BT: SOLO LEVELING Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24511/logo.webp ※ | 64 |
| 81_Union_Arena | UE18BT: Tokyo Ghoul | https://holodex-prod-bucket.b-cdn.net/sets/union_24512/logo.webp | 152 |
| 81_Union_Arena | UE18BT: Tokyo Ghoul Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24512/logo.webp ※ | 72 |
| 81_Union_Arena | UE18ST: Tokyo Ghoul Starter Deck |  | 27 |
| 81_Union_Arena | UE19BT: SAKAMOTO DAYS | https://holodex-prod-bucket.b-cdn.net/sets/union_24544/logo.webp | 119 |
| 81_Union_Arena | UE19BT: SAKAMOTO DAYS Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24544/logo.webp ※ | 60 |
| 81_Union_Arena | UE20BT: That Time I Got Reincarnated as a Slime | https://holodex-prod-bucket.b-cdn.net/sets/union_24543/logo.webp | 49 |
| 81_Union_Arena | UE20BT: That Time I Got Reincarnated as a Slime Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24543/logo.webp ※ | 63 |
| 81_Union_Arena | UE22BT: CHAINSAW MAN | https://holodex-prod-bucket.b-cdn.net/sets/union_24642/logo.webp | 49 |
| 81_Union_Arena | UE22BT: CHAINSAW MAN Release Event |  | 60 |
| 81_Union_Arena | UE23BT: Inuyasha | https://holodex-prod-bucket.b-cdn.net/sets/union_ue23bt24687/logo.webp | 49 |
| 81_Union_Arena | UE23BT: Inuyasha Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_ue23bt24687/logo.webp ※ | 58 |
| 81_Union_Arena | UEX01BT: BLEACH: Thousand-Year Blood War Vol.2 | https://holodex-prod-bucket.b-cdn.net/sets/union_24014/logo.webp | 103 |
| 81_Union_Arena | UEX01BT: BLEACH: Thousand-Year Blood War Vol.2 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24014/logo.webp ※ | 55 |
| 81_Union_Arena | UEX02BT: Jujutsu Kaisen Vol.2 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24020/logo.webp ※ | 61 |
| 81_Union_Arena | UEX03BT: CODE GEASS: Lelouch of the Rebellion Vol.2 | https://holodex-prod-bucket.b-cdn.net/sets/union_24393/logo.webp | 47 |
| 81_Union_Arena | UEX03BT: CODE GEASS: Lelouch of the Rebellion Vol.2 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24393/logo.webp ※ | 55 |
| 81_Union_Arena | UEX05BT: Demon Slayer: Kimetsu no Yaiba Vol.2 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24329/logo.webp ※ | 55 |
| 81_Union_Arena | UEX06BT: Sword Art Online Vol.2 | https://holodex-prod-bucket.b-cdn.net/sets/union_24509/logo.webp | 116 |
| 81_Union_Arena | UEX06BT: Sword Art Online Vol.2 Release Event Cards | https://holodex-prod-bucket.b-cdn.net/sets/union_24509/logo.webp ※ | 55 |

### 83_Elestrals（52 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 83_Elestrals | Artist Collection |  | 25 |
| 83_Elestrals | Awakened Promos |  | 71 |
| 83_Elestrals | Base Promos [First Edition] |  | 6 |
| 83_Elestrals | Base Promos [Kickstarter Edition] |  | 32 |
| 83_Elestrals | Base Set [First Edition] |  | 134 |
| 83_Elestrals | Base Set [Kickstarter Edition] |  | 132 |
| 83_Elestrals | Centaurbor Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Centaurbor Starter Deck [Kickstarter Edition] |  | 26 |
| 83_Elestrals | Chronodile Starter Deck [First Edition] |  | 27 |
| 83_Elestrals | Clash! Promos |  | 28 |
| 83_Elestrals | Creator Promos |  | 13 |
| 83_Elestrals | Dallas Open 2025 |  | 11 |
| 83_Elestrals | Daybreak Promos |  | 10 |
| 83_Elestrals | Daybreak [First Edition] |  | 127 |
| 83_Elestrals | Divine Champions: Firestorm |  | 133 |
| 83_Elestrals | Divine Champions: Firestorm Promos |  | 4 |
| 83_Elestrals | Divine Champions: Firestorm Starter Decks |  | 119 |
| 83_Elestrals | Divine Champions: Lifestream |  | 156 |
| 83_Elestrals | Divine Champions: Lifestream Promos |  | 10 |
| 83_Elestrals | Divine Champions: Lifestream Starter Decks |  | 103 |
| 83_Elestrals | Divine Champions: Sunstrike Promos |  | 10 |
| 83_Elestrals | Divine Champions: Sunstrike Starter Decks |  | 104 |
| 83_Elestrals | Elestrals Premier Packs |  | 32 |
| 83_Elestrals | Emperowatt Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Event Pack 2026 |  | 42 |
| 83_Elestrals | Frostfall Promos |  | 6 |
| 83_Elestrals | Frostfall [First Edition] |  | 115 |
| 83_Elestrals | Fulgoryx Starter Deck |  | 29 |
| 83_Elestrals | Kissimmee Open 2025 |  | 13 |
| 83_Elestrals | Kryoscorch Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Majesea Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Majesea Starter Deck [Kickstarter Edition] |  | 26 |
| 83_Elestrals | Moonrise |  | 140 |
| 83_Elestrals | Moonrise Promos |  | 9 |
| 83_Elestrals | OP Promos |  | 7 |
| 83_Elestrals | Ohmperial Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Ohmperial Starter Deck [Kickstarter Edition] |  | 26 |
| 83_Elestrals | Organized Play Series 1 |  | 33 |
| 83_Elestrals | Organized Play Series 2 |  | 30 |
| 83_Elestrals | Organized Play Series 3 |  | 33 |
| 83_Elestrals | Organized Play Series 4 |  | 33 |
| 83_Elestrals | Organized Play Series 5 |  | 20 |
| 83_Elestrals | Penterror Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Penterror Starter Deck [Kickstarter Edition] |  | 26 |
| 83_Elestrals | Pharogeist Starter Deck [First Edition] |  | 27 |
| 83_Elestrals | Posthumoose Starter Deck |  | 26 |
| 83_Elestrals | Shattered Stars Chapter 1 [SS1] |  | 138 |
| 83_Elestrals | Shattered Stars Chapter 2 [SS2] |  | 239 |
| 83_Elestrals | Shattered Stars Chapter 3 [SS3] |  | 18 |
| 83_Elestrals | Trifernal Starter Deck [First Edition] |  | 26 |
| 83_Elestrals | Trifernal Starter Deck [Kickstarter Edition] |  | 26 |
| 83_Elestrals | World Championships 2026 |  | 23 |

### 85_Pokemon_Japan（358 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 85_Pokemon_Japan | 10th Movie Commemoration Set |  | 11 |
| 85_Pokemon_Japan | 11th Movie Commemoration Set |  | 9 |
| 85_Pokemon_Japan | 64 Mario Stadium Best Photo Contest |  | 5 |
| 85_Pokemon_Japan | ADV Expansion Pack |  | 55 |
| 85_Pokemon_Japan | ADV-P Promotional cards |  | 63 |
| 85_Pokemon_Japan | Aqua Deck Kit |  | 33 |
| 85_Pokemon_Japan | Awakening Legends |  | 57 |
| 85_Pokemon_Japan | BK: Cobalion Battle Strength Deck |  | 16 |
| 85_Pokemon_Japan | BK: Terrakion Battle Strength Deck |  | 17 |
| 85_Pokemon_Japan | BK: Virizion Battle Strength Deck |  | 17 |
| 85_Pokemon_Japan | BKB: Black Kyurem-EX Battle Strength Deck |  | 18 |
| 85_Pokemon_Japan | BKR: Reshiram-EX Battle Strength Deck |  | 18 |
| 85_Pokemon_Japan | BKW: White Kyurem-EX Battle Strength Deck |  | 18 |
| 85_Pokemon_Japan | BKZ: Zekrom-EX Battle Strength Deck |  | 18 |
| 85_Pokemon_Japan | BREAK Starter Pack |  | 77 |
| 85_Pokemon_Japan | BW-P Promotional cards |  | 250 |
| 85_Pokemon_Japan | BW1: Black Collection |  | 56 |
| 85_Pokemon_Japan | BW1: White Collection |  | 55 |
| 85_Pokemon_Japan | BW2: Red Collection |  | 71 |
| 85_Pokemon_Japan | BW3: Hail Blizzard |  | 57 |
| 85_Pokemon_Japan | BW3: Psycho Drive |  | 57 |
| 85_Pokemon_Japan | BW4: Dark Rush |  | 76 |
| 85_Pokemon_Japan | BW5: Dragon Blade |  | 55 |
| 85_Pokemon_Japan | BW5: Dragon Blast |  | 55 |
| 85_Pokemon_Japan | BW6: Cold Flare |  | 65 |
| 85_Pokemon_Japan | BW6: Freeze Bolt |  | 65 |
| 85_Pokemon_Japan | BW7: Plasma Gale |  | 79 |
| 85_Pokemon_Japan | BW8: Spiral Force |  | 58 |
| 85_Pokemon_Japan | BW8: Thunder Knuckle |  | 58 |
| 85_Pokemon_Japan | BW9: Megalo Cannon |  | 86 |
| 85_Pokemon_Japan | BW: Extra Regulation Box |  | 48 |
| 85_Pokemon_Japan | Base Expansion Pack |  | 131 |
| 85_Pokemon_Japan | Bastiodon the Defender Half Deck |  | 14 |
| 85_Pokemon_Japan | Battle Academy |  | 74 |
| 85_Pokemon_Japan | Battle Gift Set: Thundurus vs Tornadus |  | 20 |
| 85_Pokemon_Japan | Battle Road |  | 22 |
| 85_Pokemon_Japan | Battle Theme Deck: Victini |  | 21 |
| 85_Pokemon_Japan | Black Deck Kit |  | 20 |
| 85_Pokemon_Japan | CP1: Magma Gang vs Aqua Gang: Double Crisis |  | 34 |
| 85_Pokemon_Japan | CP2: Legendary Shine Collection |  | 27 |
| 85_Pokemon_Japan | CP3: PokeKyun Collection |  | 32 |
| 85_Pokemon_Japan | CP4: Premium Champion Pack |  | 140 |
| 85_Pokemon_Japan | CP6: Expansion Pack 20th Anniversary |  | 103 |
| 85_Pokemon_Japan | CS1: Journey Partners Collection Sheet |  | 9 |
| 85_Pokemon_Japan | Challenge from the Darkness |  | 99 |
| 85_Pokemon_Japan | Champion Road |  | 2 |
| 85_Pokemon_Japan | City Gym Decks |  | 124 |
| 85_Pokemon_Japan | Clash of the Blue Sky |  | 82 |
| 85_Pokemon_Japan | CoroCoro Promotional Cards |  | 51 |
| 85_Pokemon_Japan | DP-P Promotional cards |  | 126 |
| 85_Pokemon_Japan | DP1: Space-Time Creation |  | 121 |
| 85_Pokemon_Japan | DP2: Secret of the Lakes |  | 123 |
| 85_Pokemon_Japan | DP3: Shining Darkness |  | 119 |
| 85_Pokemon_Japan | DP4: Dawn Dash |  | 65 |
| 85_Pokemon_Japan | DP4: Moonlit Pursuit |  | 70 |
| 85_Pokemon_Japan | DP5: Cry from the Mysterious |  | 65 |
| 85_Pokemon_Japan | DP5: Temple of Anger |  | 65 |
| 85_Pokemon_Japan | DPt-P Promotional cards |  | 51 |
| 85_Pokemon_Japan | Deoxys Constructed Starter Deck |  | 16 |
| 85_Pokemon_Japan | Dragon Selection |  | 20 |
| 85_Pokemon_Japan | EX Battle Boost |  | 186 |
| 85_Pokemon_Japan | Elementary School Competition |  | 4 |
| 85_Pokemon_Japan | Entry Pack |  | 12 |
| 85_Pokemon_Japan | Entry Pack '08 |  | 24 |
| 85_Pokemon_Japan | Entry Pack DPt (Dialga) |  | 3 |
| 85_Pokemon_Japan | Entry Pack DPt (Giratina) |  | 5 |
| 85_Pokemon_Japan | Entry Pack DPt (Palkia) |  | 6 |
| 85_Pokemon_Japan | Expansion Pack |  | 93 |
| 85_Pokemon_Japan | Expansion Pack (No Rarity) |  | 1 |
| 85_Pokemon_Japan | Feraligatr Constructed Starter Deck |  | 16 |
| 85_Pokemon_Japan | Fighting Quick Construction Pack |  | 15 |
| 85_Pokemon_Japan | Fire Quick Construction Pack |  | 15 |
| 85_Pokemon_Japan | Flight of Legends |  | 82 |
| 85_Pokemon_Japan | Flygon Constructed Starter Deck |  | 20 |
| 85_Pokemon_Japan | Garchomp Half Deck |  | 15 |
| 85_Pokemon_Japan | Garchomp vs Charizard SP Deck Kit (Charizard) |  | 16 |
| 85_Pokemon_Japan | Garchomp vs Charizard SP Deck Kit (Garchomp) |  | 13 |
| 85_Pokemon_Japan | Giratina vs Dialga Deck Kit (Dialga) |  | 14 |
| 85_Pokemon_Japan | Giratina vs Dialga Deck Kit (Giratina) |  | 14 |
| 85_Pokemon_Japan | Golden Sky, Silvery Ocean |  | 106 |
| 85_Pokemon_Japan | Grass Quick Construction Pack |  | 15 |
| 85_Pokemon_Japan | Gym Challenge |  | 21 |
| 85_Pokemon_Japan | Heatran vs Regigigas Deck Kit |  | 23 |
| 85_Pokemon_Japan | Holon Phantom |  | 52 |
| 85_Pokemon_Japan | Holon Research Tower |  | 74 |
| 85_Pokemon_Japan | Holon Research Tower Fire Quarter Deck |  | 15 |
| 85_Pokemon_Japan | Holon Research Tower Lightning Quarter Deck |  | 14 |
| 85_Pokemon_Japan | Holon Research Tower Water Quarter Deck |  | 15 |
| 85_Pokemon_Japan | How I Became a Pokemon Card |  | 6 |
| 85_Pokemon_Japan | Hydreigon Half Deck |  | 15 |
| 85_Pokemon_Japan | Infernape vs Gallade SP Deck Kit (Gallade) |  | 12 |
| 85_Pokemon_Japan | Infernape vs Gallade SP Deck Kit (Infernape) |  | 18 |
| 85_Pokemon_Japan | Intense Fight in the Destroyed Sky |  | 42 |
| 85_Pokemon_Japan | J Promotional cards |  | 2 |
| 85_Pokemon_Japan | Japanese CD Promo |  | 4 |
| 85_Pokemon_Japan | Keldeo Battle Strength Deck |  | 15 |
| 85_Pokemon_Japan | L-P: Legends Promos |  | 79 |
| 85_Pokemon_Japan | L1: HeartGold Collection |  | 143 |
| 85_Pokemon_Japan | L1: SoulSilver Collection |  | 141 |
| 85_Pokemon_Japan | L2: Revival Legends |  | 160 |
| 85_Pokemon_Japan | L2: Steelix Constructed Standard Deck |  | 19 |
| 85_Pokemon_Japan | L2: Tyranitar Constructed Standard Deck |  | 19 |
| 85_Pokemon_Japan | L3: Clash at the Summit |  | 161 |
| 85_Pokemon_Japan | LL: Lost Link |  | 40 |
| 85_Pokemon_Japan | Leafeon vs Metagross Expert Deck (Leafeon) |  | 15 |
| 85_Pokemon_Japan | Leafeon vs Metagross Expert Deck (Metagross) |  | 14 |
| 85_Pokemon_Japan | Lightning Quick Construction Pack |  | 15 |
| 85_Pokemon_Japan | M Master Deck Build Box Power Style |  | 58 |
| 85_Pokemon_Japan | M Master Deck Build Box Speed Style |  | 57 |
| 85_Pokemon_Japan | M-P Promotional Cards |  | 60 |
| 85_Pokemon_Japan | M2: Inferno X |  | 116 |
| 85_Pokemon_Japan | M2a: High Class Pack: MEGA Dream ex |  | 485 |
| 85_Pokemon_Japan | M3: Nihil Zero |  | 117 |
| 85_Pokemon_Japan | M4: Ninja Spinner |  | 120 |
| 85_Pokemon_Japan | M5: Abyss Eye |  | 118 |
| 85_Pokemon_Japan | M6: Storm Emeralda |  | 116 |
| 85_Pokemon_Japan | MBD: MEGA Starter Set Mega Diancie ex |  | 22 |
| 85_Pokemon_Japan | MBG: MEGA Starter Set Mega Gengar ex |  | 22 |
| 85_Pokemon_Japan | MEE: Starter Set ex Eevee ex |  | 20 |
| 85_Pokemon_Japan | MEM: Starter Set ex Meowscarada ex |  | 18 |
| 85_Pokemon_Japan | MEZ: Starter Set ex Zoroark ex |  | 20 |
| 85_Pokemon_Japan | MP1: Start Deck 100 Battle Collection CoroCiao Version |  | 23 |
| 85_Pokemon_Japan | Magma Deck Kit |  | 33 |
| 85_Pokemon_Japan | Magma VS Aqua: Two Ambitions |  | 80 |
| 85_Pokemon_Japan | Magmortar vs Electivire Deck Kit |  | 26 |
| 85_Pokemon_Japan | Master Deck Build Box EX |  | 46 |
| 85_Pokemon_Japan | Mega Evolution Unnumbered Energies |  | 4 |
| 85_Pokemon_Japan | Meganium Constructed Starter Deck |  | 16 |
| 85_Pokemon_Japan | Metagross Constructed Starter Deck |  | 19 |
| 85_Pokemon_Japan | Mewtwo vs Genesect Deck Kit (Genesect) |  | 16 |
| 85_Pokemon_Japan | Mewtwo vs Genesect Deck Kit (Mewtwo) |  | 16 |
| 85_Pokemon_Japan | Miracle Crystal |  | 75 |
| 85_Pokemon_Japan | Miracle of the Desert |  | 53 |
| 85_Pokemon_Japan | Mirage Forest |  | 86 |
| 85_Pokemon_Japan | Movie Commemoration Random Pack |  | 22 |
| 85_Pokemon_Japan | Movie Commemoration VS Pack |  | 11 |
| 85_Pokemon_Japan | Movie Commemoration VS Pack: Aura's Lucario |  | 16 |
| 85_Pokemon_Japan | Movie Commemoration VS Pack: Sea's Manaphy |  | 12 |
| 85_Pokemon_Japan | Movie Commemoration VS Pack: Sky-Splitting Deoxys |  | 20 |
| 85_Pokemon_Japan | Mudkip Constructed Starter Deck |  | 20 |
| 85_Pokemon_Japan | Mysterious Mountains |  | 91 |
| 85_Pokemon_Japan | Mystery of the Fossils |  | 48 |
| 85_Pokemon_Japan | Neo Premium File 1 |  | 9 |
| 85_Pokemon_Japan | Neo Premium File 2 |  | 9 |
| 85_Pokemon_Japan | Neo Premium File 3 |  | 9 |
| 85_Pokemon_Japan | Offense and Defense of the Furthest Ends |  | 68 |
| 85_Pokemon_Japan | P Promotional cards |  | 1 |
| 85_Pokemon_Japan | PCG-P Promotional cards |  | 155 |
| 85_Pokemon_Japan | PLAY Promotional cards |  | 32 |
| 85_Pokemon_Japan | PPP Promotional cards |  | 7 |
| 85_Pokemon_Japan | Player Placement Trainer Promos |  | 2 |
| 85_Pokemon_Japan | PokePark Blue |  | 9 |
| 85_Pokemon_Japan | PokePark Forest |  | 9 |
| 85_Pokemon_Japan | Pokemon Card Design Contest |  | 6 |
| 85_Pokemon_Japan | Pokemon Card Fan Club |  | 10 |
| 85_Pokemon_Japan | Pokemon Card Information Promotional cards |  | 3 |
| 85_Pokemon_Japan | Pokemon Jungle |  | 48 |
| 85_Pokemon_Japan | Pokemon TCG Classic: Blastoise |  | 34 |
| 85_Pokemon_Japan | Pokemon TCG Classic: Charizard |  | 34 |
| 85_Pokemon_Japan | Pokemon TCG Classic: Venusaur |  | 34 |
| 85_Pokemon_Japan | Pokemon VS |  | 151 |
| 85_Pokemon_Japan | Pokemon Web |  | 47 |
| 85_Pokemon_Japan | Pokemon-e Starter Deck |  | 29 |
| 85_Pokemon_Japan | Psychic Quick Construction Pack |  | 15 |
| 85_Pokemon_Japan | Pt2: Bonds to the End of Time |  | 90 |
| 85_Pokemon_Japan | Pt3: Beat of the Frontier |  | 100 |
| 85_Pokemon_Japan | Pt4: Advent of Arceus |  | 90 |
| 85_Pokemon_Japan | Rampardos the Attacker Constructed Half Deck |  | 15 |
| 85_Pokemon_Japan | Rayquaza Constructed Starter Deck |  | 16 |
| 85_Pokemon_Japan | Rocket Gang |  | 65 |
| 85_Pokemon_Japan | Rocket Gang Strikes Back |  | 85 |
| 85_Pokemon_Japan | Rulers of the Heavens |  | 54 |
| 85_Pokemon_Japan | S10D: Time Gazer |  | 87 |
| 85_Pokemon_Japan | S10P: Space Juggler |  | 87 |
| 85_Pokemon_Japan | S10a: Dark Phantasma |  | 147 |
| 85_Pokemon_Japan | S10b: Pokemon GO |  | 104 |
| 85_Pokemon_Japan | S11: Lost Abyss |  | 127 |
| 85_Pokemon_Japan | S11a: Incandescent Arcana |  | 140 |
| 85_Pokemon_Japan | S12: Paradigm Trigger |  | 125 |
| 85_Pokemon_Japan | S12a: VSTAR Universe |  | 349 |
| 85_Pokemon_Japan | S1H: Shield |  | 75 |
| 85_Pokemon_Japan | S1W: Sword |  | 75 |
| 85_Pokemon_Japan | S1a: VMAX Rising |  | 86 |
| 85_Pokemon_Japan | S2: Rebellion Crash |  | 113 |
| 85_Pokemon_Japan | S2a: Explosive Walker |  | 86 |
| 85_Pokemon_Japan | S3: Infinity Zone |  | 116 |
| 85_Pokemon_Japan | S3a: Legendary Heartbeat |  | 94 |
| 85_Pokemon_Japan | S4: Amazing Volt Tackle |  | 121 |
| 85_Pokemon_Japan | S4a: Shiny Star V |  | 433 |
| 85_Pokemon_Japan | S5I: Single Strike Master |  | 91 |
| 85_Pokemon_Japan | S5R: Rapid Strike Master |  | 91 |
| 85_Pokemon_Japan | S5a: Peerless Fighters |  | 95 |
| 85_Pokemon_Japan | S6H: Silver Lance |  | 95 |
| 85_Pokemon_Japan | S6K: Jet-Black Spirit |  | 93 |
| 85_Pokemon_Japan | S6a: Eevee Heroes |  | 101 |
| 85_Pokemon_Japan | S7D: Skyscraping Perfection |  | 90 |
| 85_Pokemon_Japan | S7R: Blue Sky Stream |  | 50 |
| 85_Pokemon_Japan | S8: Fusion Arts |  | 128 |
| 85_Pokemon_Japan | S8a: 25th Anniversary Collection |  | 55 |
| 85_Pokemon_Japan | S8b: VMAX Climax |  | 396 |
| 85_Pokemon_Japan | S9: Star Birth |  | 126 |
| 85_Pokemon_Japan | S9a: Battle Region |  | 137 |
| 85_Pokemon_Japan | SI: Start Deck 100 |  | 513 |
| 85_Pokemon_Japan | SM10: Double Blaze |  | 116 |
| 85_Pokemon_Japan | SM10a: GG End |  | 69 |
| 85_Pokemon_Japan | SM10b: Sky Legend |  | 69 |
| 85_Pokemon_Japan | SM11: Miracle Twin |  | 115 |
| 85_Pokemon_Japan | SM11a: Remix Bout |  | 80 |
| 85_Pokemon_Japan | SM11b: Dream League |  | 75 |
| 85_Pokemon_Japan | SM12: Alter Genesis |  | 117 |
| 85_Pokemon_Japan | SM12a: TAG TEAM GX: Tag All Stars |  | 342 |
| 85_Pokemon_Japan | SM1M: Collection Moon |  | 73 |
| 85_Pokemon_Japan | SM1S: Collection Sun |  | 73 |
| 85_Pokemon_Japan | SM2K: Islands Await You |  | 62 |
| 85_Pokemon_Japan | SM2L: Alolan Moonlight |  | 62 |
| 85_Pokemon_Japan | SM3H: To Have Seen the Battle Rainbow |  | 64 |
| 85_Pokemon_Japan | SM3N: Darkness that Consumes Light |  | 64 |
| 85_Pokemon_Japan | SM4A: Ultradimensional Beasts |  | 62 |
| 85_Pokemon_Japan | SM4S: Awakened Heroes |  | 62 |
| 85_Pokemon_Japan | SM5M: Ultra Moon |  | 78 |
| 85_Pokemon_Japan | SM5S: Ultra Sun |  | 78 |
| 85_Pokemon_Japan | SM6: Forbidden Light |  | 108 |
| 85_Pokemon_Japan | SM6a: Dragon Storm |  | 66 |
| 85_Pokemon_Japan | SM6b: Champion Road |  | 86 |
| 85_Pokemon_Japan | SM7: Sky-Splitting Charisma |  | 112 |
| 85_Pokemon_Japan | SM7a: Thunderclap Spark |  | 73 |
| 85_Pokemon_Japan | SM7b: Fairy Rise |  | 63 |
| 85_Pokemon_Japan | SM8: Super-Burst Impact |  | 111 |
| 85_Pokemon_Japan | SM8a: Dark Order |  | 65 |
| 85_Pokemon_Japan | SM8b: GX Ultra Shiny |  | 371 |
| 85_Pokemon_Japan | SM9: Tag Bolt |  | 118 |
| 85_Pokemon_Japan | SM9a: Night Unison |  | 70 |
| 85_Pokemon_Japan | SM9b: Full Metal Wall |  | 69 |
| 85_Pokemon_Japan | SM: The Best of XY |  | 315 |
| 85_Pokemon_Japan | SNP: Noivern BREAK Evolution Pack |  | 10 |
| 85_Pokemon_Japan | SNP: Raichu BREAK Evolution Pack |  | 10 |
| 85_Pokemon_Japan | SS: Gengar VMAX High-Class Deck |  | 20 |
| 85_Pokemon_Japan | SS: Inteleon VMAX High-Class Deck |  | 23 |
| 85_Pokemon_Japan | SV-P Promotional Cards |  | 225 |
| 85_Pokemon_Japan | SV10: The Glory of Team Rocket |  | 132 |
| 85_Pokemon_Japan | SV11B: Black Bolt |  | 322 |
| 85_Pokemon_Japan | SV11W: White Flare |  | 319 |
| 85_Pokemon_Japan | SV1S: Scarlet ex |  | 106 |
| 85_Pokemon_Japan | SV1V: Violet ex |  | 108 |
| 85_Pokemon_Japan | SV1a: Triplet Beat |  | 102 |
| 85_Pokemon_Japan | SV2D: Clay Burst |  | 99 |
| 85_Pokemon_Japan | SV2P: Snow Hazard |  | 99 |
| 85_Pokemon_Japan | SV2a: Pokemon Card 151 |  | 513 |
| 85_Pokemon_Japan | SV3: Ruler of the Black Flame |  | 141 |
| 85_Pokemon_Japan | SV3a: Raging Surf |  | 92 |
| 85_Pokemon_Japan | SV4K: Ancient Roar |  | 95 |
| 85_Pokemon_Japan | SV4M: Future Flash |  | 95 |
| 85_Pokemon_Japan | SV4a: Shiny Treasure ex |  | 480 |
| 85_Pokemon_Japan | SV5K: Wild Force |  | 100 |
| 85_Pokemon_Japan | SV5M: Cyber Judge |  | 100 |
| 85_Pokemon_Japan | SV5a: Crimson Haze |  | 96 |
| 85_Pokemon_Japan | SV6: Transformation Mask |  | 133 |
| 85_Pokemon_Japan | SV6a: Night Wanderer |  | 94 |
| 85_Pokemon_Japan | SV7: Stellar Miracle |  | 135 |
| 85_Pokemon_Japan | SV7a: Paradise Dragona |  | 94 |
| 85_Pokemon_Japan | SV8: Super Electric Breaker |  | 138 |
| 85_Pokemon_Japan | SV8a: Terastal Fest ex |  | 480 |
| 85_Pokemon_Japan | SV9: Battle Partners |  | 132 |
| 85_Pokemon_Japan | SV9a: Heat Wave Arena |  | 92 |
| 85_Pokemon_Japan | SV: Ceruledge ex Stellar Tera Type Starter Set |  | 21 |
| 85_Pokemon_Japan | SV: Chien-Pao ex Battle Master Deck |  | 19 |
| 85_Pokemon_Japan | SV: Mewtwo ex Terastal Starter Set |  | 20 |
| 85_Pokemon_Japan | SV: Premium Trainer Box ex |  | 28 |
| 85_Pokemon_Japan | SV: Ruler of the Black Flame Deck Build Box |  | 38 |
| 85_Pokemon_Japan | SV: Skeledirge ex Terastal Starter Set |  | 20 |
| 85_Pokemon_Japan | SV: Stellar Miracle Deck Build Box |  | 45 |
| 85_Pokemon_Japan | SV: Sylveon ex Stellar Tera Type Starter Set |  | 22 |
| 85_Pokemon_Japan | SV: Terastal Charizard ex Battle Master Deck |  | 21 |
| 85_Pokemon_Japan | SV: ex Special Set |  | 7 |
| 85_Pokemon_Japan | SV: ex Start Decks |  | 138 |
| 85_Pokemon_Japan | SVM: Generations Start Decks |  | 175 |
| 85_Pokemon_Japan | SVN: Battle Partners Deck Build Box |  | 45 |
| 85_Pokemon_Japan | Salamence Constructed Starter Deck |  | 20 |
| 85_Pokemon_Japan | Shiny Collection |  | 25 |
| 85_Pokemon_Japan | Silver Deck Kit |  | 20 |
| 85_Pokemon_Japan | Southern Island |  | 18 |
| 85_Pokemon_Japan | Split Earth |  | 91 |
| 85_Pokemon_Japan | Start Deck 100 Battle Collection |  | 850 |
| 85_Pokemon_Japan | T Promotional cards |  | 24 |
| 85_Pokemon_Japan | Team Plasma Battle Gift Set |  | 16 |
| 85_Pokemon_Japan | The Town on No Map |  | 92 |
| 85_Pokemon_Japan | Theater Limited VS Pack |  | 18 |
| 85_Pokemon_Japan | Torchic Constructed Starter Deck |  | 20 |
| 85_Pokemon_Japan | Trainer Prize Cards |  | 3 |
| 85_Pokemon_Japan | Treecko Constructed Starter Deck |  | 20 |
| 85_Pokemon_Japan | Typhlosion Constructed Starter Deck |  | 16 |
| 85_Pokemon_Japan | Undone Seal |  | 83 |
| 85_Pokemon_Japan | Unnumbered Promotional cards |  | 81 |
| 85_Pokemon_Japan | Unnumbered World Championships |  | 6 |
| 85_Pokemon_Japan | WCS23: 2023 World Championships Yokohama Deck: Pikachu |  | 30 |
| 85_Pokemon_Japan | Water Quick Construction Pack |  | 15 |
| 85_Pokemon_Japan | Wind from the Sea |  | 90 |
| 85_Pokemon_Japan | World Champions Pack |  | 102 |
| 85_Pokemon_Japan | World Hobby Fair |  | 8 |
| 85_Pokemon_Japan | XY Beginning Set |  | 41 |
| 85_Pokemon_Japan | XY-Bx: Collection X |  | 63 |
| 85_Pokemon_Japan | XY-By: Collection Y |  | 63 |
| 85_Pokemon_Japan | XY-P: XY Promos |  | 302 |
| 85_Pokemon_Japan | XY10: Awakening Psychic King |  | 88 |
| 85_Pokemon_Japan | XY11-Bb: Fever-Burst Fighter |  | 59 |
| 85_Pokemon_Japan | XY11-Br: Cruel Traitor |  | 59 |
| 85_Pokemon_Japan | XY2: Wild Blaze |  | 90 |
| 85_Pokemon_Japan | XY3: Rising Fist |  | 105 |
| 85_Pokemon_Japan | XY4: Phantom Gate |  | 97 |
| 85_Pokemon_Japan | XY5-Bg: Gaia Volcano |  | 80 |
| 85_Pokemon_Japan | XY5-Bt: Tidal Storm |  | 80 |
| 85_Pokemon_Japan | XY6: Emerald Break |  | 91 |
| 85_Pokemon_Japan | XY7: Bandit Ring |  | 97 |
| 85_Pokemon_Japan | XY8-Bb: Blue Shock |  | 65 |
| 85_Pokemon_Japan | XY8-Br: Red Flash |  | 65 |
| 85_Pokemon_Japan | XY9: Rage of the Broken Heavens |  | 88 |
| 85_Pokemon_Japan | XYA: M Charizard-EX Mega Battle Deck |  | 22 |
| 85_Pokemon_Japan | XYD: M Rayquaza-EX Mega Battle Deck |  | 18 |
| 85_Pokemon_Japan | XYE: Emboar-EX vs Togekiss-EX Deck Kit |  | 22 |
| 85_Pokemon_Japan | XYG: Zygarde-EX Perfect Battle Deck |  | 19 |
| 85_Pokemon_Japan | XYH: M Audino-EX Mega Battle Deck |  | 26 |
| 85_Pokemon_Japan | Xerneas Half Deck |  | 15 |
| 85_Pokemon_Japan | Yveltal Half Deck |  | 15 |
| 85_Pokemon_Japan | m1L: Mega Brave |  | 93 |
| 85_Pokemon_Japan | m1S: Mega Symphonia |  | 92 |
| 85_Pokemon_Japan | s0: Charizard VSTAR vs Rayquaza VMAX Special Deck Set |  | 30 |
| 85_Pokemon_Japan | s8a-G: 25th Anniversary Golden Box |  | 16 |
| 85_Pokemon_Japan | s8a-P: Promo Card Pack 25th Anniversary Edition |  | 25 |
| 85_Pokemon_Japan | sA: Fighting Starter Set V |  | 46 |
| 85_Pokemon_Japan | sA: Fire Starter Set V |  | 45 |
| 85_Pokemon_Japan | sA: Grass Starter Set V |  | 45 |
| 85_Pokemon_Japan | sA: Lightning Starter Set V |  | 46 |
| 85_Pokemon_Japan | sA: Water Starter Set V |  | 45 |
| 85_Pokemon_Japan | sC2: Charizard Starter Set VMAX 2 |  | 21 |
| 85_Pokemon_Japan | sC: Charizard Starter Set VMAX |  | 21 |
| 85_Pokemon_Japan | sC: Grimmsnarl Starter Set VMAX |  | 20 |
| 85_Pokemon_Japan | sD: V Starter Decks |  | 127 |
| 85_Pokemon_Japan | sEF: Venusaur Starter Set VMAX |  | 21 |
| 85_Pokemon_Japan | sEK: Blastoise Starter Set VMAX |  | 20 |
| 85_Pokemon_Japan | sK: VSTAR Premium Trainer Box |  | 30 |
| 85_Pokemon_Japan | sLD: Darkrai Starter Set VSTAR |  | 20 |
| 85_Pokemon_Japan | sLL: Lucario Starter Set VSTAR |  | 21 |
| 85_Pokemon_Japan | sN: Start Deck 100 CoroCoro Comic Version |  | 24 |
| 85_Pokemon_Japan | sm1+: Enhanced Expansion Pack Sun & Moon |  | 1 |
| 85_Pokemon_Japan | smB: Premium Trainer Box |  | 18 |
| 85_Pokemon_Japan | smC: Tapu Bulu-GX Enhanced Starter Set |  | 21 |
| 85_Pokemon_Japan | smD: Ash vs Team Rocket Deck Kit |  | 30 |
| 85_Pokemon_Japan | smH: GX Starter Decks |  | 131 |
| 85_Pokemon_Japan | smJ: Tag Team GX Premium Trainer Box |  | 35 |
| 85_Pokemon_Japan | smK: Trainer Battle Decks |  | 31 |
| 85_Pokemon_Japan | smM: Tag Team GX Starter Sets |  | 31 |
| 85_Pokemon_Japan | smN: Tag Team GX Deck Build Box |  | 29 |
| 85_Pokemon_Japan | smP1: Rockruff Full Power Deck |  | 13 |
| 85_Pokemon_Japan | smP2: Great Detective Pikachu |  | 25 |
| 85_Pokemon_Japan | sp2: VMAX Special Set |  | 8 |
| 85_Pokemon_Japan | sp4: Eevee Heroes VMAX Special Set |  | 4 |
| 85_Pokemon_Japan | sp5: V-UNION Special Card Sets |  | 13 |
| 85_Pokemon_Japan | sp6: VSTAR Special Set |  | 6 |

### 86_Gundam_Card_Game（22 个系列，18 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 86_Gundam_Card_Game | Deck Build Box Freedom Ascension |  | 48 |
| 86_Gundam_Card_Game | Dual Impact | https://holodex-prod-bucket.b-cdn.net/sets/gun_24408/logo.webp | 100 |
| 86_Gundam_Card_Game | Edition Beta | https://holodex-prod-bucket.b-cdn.net/sets/gun_24193/logo.webp | 83 |
| 86_Gundam_Card_Game | Eternal Nexus | https://holodex-prod-bucket.b-cdn.net/sets/gun_24693/logo.webp | 108 |
| 86_Gundam_Card_Game | Freedom Ascension | https://holodex-prod-bucket.b-cdn.net/sets/gun_24699/logo.webp | 49 |
| 86_Gundam_Card_Game | Gundam Promotional Cards | https://holodex-prod-bucket.b-cdn.net/sets/gun_24340/logo.webp | 202 |
| 86_Gundam_Card_Game | Newtype Rising | https://holodex-prod-bucket.b-cdn.net/sets/gun_24221/logo.webp | 192 |
| 86_Gundam_Card_Game | Phantom Aria | https://holodex-prod-bucket.b-cdn.net/sets/gun_24633/logo.webp | 50 |
| 86_Gundam_Card_Game | Promotional EX Base Tokens |  | 27 |
| 86_Gundam_Card_Game | Promotional EX Resource Tokens |  | 14 |
| 86_Gundam_Card_Game | Promotional Resource Tokens |  | 65 |
| 86_Gundam_Card_Game | Starter Deck 01: Heroic Beginnings | https://holodex-prod-bucket.b-cdn.net/sets/gun_24222/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 02: Wings of Advance | https://holodex-prod-bucket.b-cdn.net/sets/gun_24223/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 03: Zeon's Rush | https://holodex-prod-bucket.b-cdn.net/sets/gun_24224/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 04: SEED Strike | https://holodex-prod-bucket.b-cdn.net/sets/gun_24225/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 05: Iron Bloom | https://holodex-prod-bucket.b-cdn.net/sets/gun_24407/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 06: Clan Unity | https://holodex-prod-bucket.b-cdn.net/sets/gun_24409/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 07: Celestial Drive | https://holodex-prod-bucket.b-cdn.net/sets/gun_24410/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 08: Flash of Radiance | https://holodex-prod-bucket.b-cdn.net/sets/gun_24411/logo.webp | 32 |
| 86_Gundam_Card_Game | Starter Deck 09: Destiny Ignition | https://holodex-prod-bucket.b-cdn.net/sets/gun_24625/logo.webp | 39 |
| 86_Gundam_Card_Game | Starter Deck 10: Generation Pulse | https://holodex-prod-bucket.b-cdn.net/sets/gun_24692/logo.webp | 35 |
| 86_Gundam_Card_Game | Steel Requiem | https://holodex-prod-bucket.b-cdn.net/sets/gun_24522/logo.webp | 202 |

### 87_hololive_OFFICIAL_CARD_GAME（17 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 87_hololive_OFFICIAL_CARD_GAME | Ayakashi Vermilion |  | 280 |
| 87_hololive_OFFICIAL_CARD_GAME | Blooming Radiance |  | 248 |
| 87_hololive_OFFICIAL_CARD_GAME | Curious Universe |  | 240 |
| 87_hololive_OFFICIAL_CARD_GAME | Elite Spark |  | 150 |
| 87_hololive_OFFICIAL_CARD_GAME | Enchant Regalia |  | 50 |
| 87_hololive_OFFICIAL_CARD_GAME | Quintet Spectrum |  | 214 |
| 87_hololive_OFFICIAL_CARD_GAME | SD01: Start Deck: Tokino Sora and Azki |  | 19 |
| 87_hololive_OFFICIAL_CARD_GAME | SD02: Start Deck: Red Nakiri Ayame |  | 14 |
| 87_hololive_OFFICIAL_CARD_GAME | SD03: Start Deck: Blue Nekomata Okayu |  | 14 |
| 87_hololive_OFFICIAL_CARD_GAME | SD04: Start Deck: Purple Yuzuki Choco |  | 14 |
| 87_hololive_OFFICIAL_CARD_GAME | SD05: Start Deck: White Todoroki Hajime |  | 15 |
| 87_hololive_OFFICIAL_CARD_GAME | SD06: Start Deck: Green Kazama Iroha |  | 14 |
| 87_hololive_OFFICIAL_CARD_GAME | SD07: Start Deck: Yellow Shiranui Flare |  | 15 |
| 87_hololive_OFFICIAL_CARD_GAME | SD12: Start Deck: Oshi Advent |  | 24 |
| 87_hololive_OFFICIAL_CARD_GAME | SD13: Start Deck: Oshi Justice |  | 23 |
| 87_hololive_OFFICIAL_CARD_GAME | Start Cheer Set |  | 8 |
| 87_hololive_OFFICIAL_CARD_GAME | hololive OFFICIAL CARD GAME Promos |  | 120 |

### 88_Godzilla_Card_Game（6 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 88_Godzilla_Card_Game | Booster Set 1: Godzilla VS. Godzilla |  | 183 |
| 88_Godzilla_Card_Game | Booster Set 2: G: Monsters Raid Again |  | 233 |
| 88_Godzilla_Card_Game | Ink-Brushed Monster Rampage |  | 12 |
| 88_Godzilla_Card_Game | Promo Cards |  | 50 |
| 88_Godzilla_Card_Game | Starter Deck: Godzilla Minus One |  | 23 |
| 88_Godzilla_Card_Game | Starter Deck: Heisei Series |  | 22 |

### 89_Riftbound_League_of_Legends_Trading_Card_Game（9 个系列，5 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Origins | https://holodex-prod-bucket.b-cdn.net/sets/rift_24344/logo.webp | 353 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Origins: Proving Grounds | https://holodex-prod-bucket.b-cdn.net/sets/rift_24344/logo.webp ※ | 28 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Riftbound Judge Promotional Cards |  | 3 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Riftbound Organized Play Promotional Cards |  | 216 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Riftbound Promotional Cards |  | 15 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Secret Garden |  | 3 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Spiritforged | https://holodex-prod-bucket.b-cdn.net/sets/rift_24519/logo.webp | 50 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Unleashed | https://holodex-prod-bucket.b-cdn.net/sets/rift_24560/logo.webp | 308 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | Vendetta | https://holodex-prod-bucket.b-cdn.net/sets/rift_vendetta24698/logo.webp | 150 |

### 90_CookieRun_Braverse_TCG（9 个系列，0 个有关联 logo）

| 品类 | 系列 | 系列logo | 系列包含卡牌数量 |
|------|------|----------|------------------|
| 90_CookieRun_Braverse_TCG | A Game of Truth and Deceit |  | 331 |
| 90_CookieRun_Braverse_TCG | Age of Heroes and Kingdoms |  | 305 |
| 90_CookieRun_Braverse_TCG | Arena of Glory |  | 408 |
| 90_CookieRun_Braverse_TCG | Brave Beginning |  | 202 |
| 90_CookieRun_Braverse_TCG | CookieRun: Braverse TCG Collectible Card Sets |  | 8 |
| 90_CookieRun_Braverse_TCG | Promotion Cards |  | 300 |
| 90_CookieRun_Braverse_TCG | Starter Deck Assortment 1 |  | 108 |
| 90_CookieRun_Braverse_TCG | Starter Deck Assortment 2: Legendary Cookie |  | 99 |
| 90_CookieRun_Braverse_TCG | The Dark Enchantress War |  | 304 |

## 三、数据质量与缺口

### 3.1 logo 来源只覆盖 12 个 game

`crawl/crawl/holodex_sets_organized.json` 只抓了 Holodex 的 gameId 1–12，而本地卡片数据有 47 个品类。对应关系（已逐个人工核对 set 名）：

| gameId | 实测游戏 | 对应品类目录 | holodex set 数 | 有 logo |
|--------|----------|--------------|----------------|---------|
| 1 | Pokémon | 03_Pokemon | 197 | 197 |
| 2 | One Piece Card Game | 68_One_Piece_Card_Game | 22 | 22 |
| 3 | Magic: The Gathering | 01_Magic | 228 | 226 |
| 4 | Yu-Gi-Oh! | 02_YuGiOh | 153 | 150 |
| 5 | Disney Lorcana | 71_Disney_Lorcana | 15 | 15 |
| 6 | Dragon Ball Super: Fusion World | 80_Dragon_Ball_Super_Fusion_World | 30 | 30 |
| 7 | Dragon Ball Super Card Game (Masters) | （本地无卡片数据） | 59 | 59 |
| 8 | Digimon Card Game | 63_Digimon_Card_Game | 36 | 36 |
| 9 | Gundam Card Game | 86_Gundam_Card_Game | 18 | 18 |
| 10 | Union Arena | 81_Union_Arena | 29 | 29 |
| 11 | Riftbound: League of Legends TCG | 89_Riftbound_League_of_Legends_Trading_Card_Game | 4 | 4 |
| 12 | Star Wars: Unlimited | 79_Star_Wars_Unlimited | 8 | 8 |

**其余品类完全没有 logo 来源**，共 36 个品类 / 1712 个系列，其中包括 Pokemon Japan（358 个系列）这类大品类。要补齐必须再爬其它数据源的系列 logo。

### 3.2 Holodex 目录本身不全

即使是有 logo 来源的品类，Holodex 收录的 set 数也明显少于 TCGPlayer：

| 品类 | holodex set | 本地系列 | 有 logo | 未匹配（源里没有） |
|------|-------------|----------|---------|--------------------|
| 01_Magic | 228 | 405 | 195 | 210 |
| 02_YuGiOh | 153 | 605 | 145 | 460 |
| 03_Pokemon | 197 | 197 | 177 | 20 |
| 63_Digimon_Card_Game | 36 | 88 | 48 | 40 |
| 68_One_Piece_Card_Game | 22 | 83 | 34 | 49 |
| 71_Disney_Lorcana | 15 | 18 | 14 | 4 |
| 79_Star_Wars_Unlimited | 8 | 29 | 16 | 13 |
| 80_Dragon_Ball_Super_Fusion_World | 30 | 48 | 31 | 17 |
| 81_Union_Arena | 29 | 63 | 47 | 16 |
| 86_Gundam_Card_Game | 18 | 22 | 18 | 4 |
| 89_Riftbound_League_of_Legends_Trading_Card_Game | 4 | 9 | 5 | 4 |

未匹配掉的绝大多数是 Holodex 不收录的类别：促销卡（Promos）、发售活动/预发售卡（Pre-Release / Release Event Cards）、预组（Starter Deck / Structure Deck）、礼盒与铁盒（Tin / Box Set）、万智牌的 Art Series 与轮抽补充包等。

### 3.3 crawl 目录的元数据不可信

- 除 `pokemon_tcg.json`（gameId 1）外，其余单游戏文件的**文件名与内容对不上**：`magic_gathering.json` 里是 Dragon Ball Super Fusion World（gameId 6）、`one_piece.json` 里是万智牌（gameId 3）、`union_arena.json` 里是游戏王（gameId 4）、`final_fantasy.json` 里是 Disney Lorcana（gameId 5）、`pokemon_tcg_pocket.json` 里是 One Piece（gameId 2）、`pokemon_tcg_china.json` 里是 Riftbound（gameId 11）、`tcg_create.json` 里是 Star Wars Unlimited（gameId 12）、`weiss_schwarz.json` 里是 Union Arena（gameId 10）。**不要按文件名判断游戏，必须按 set 名判断。**
- 每个 series 的 `name` 字段不是真实系列名，而是爬虫脚本按 set 名前缀取众数猜的，出现了 `Extra Booster`（One Piece）、`Commander`（万智牌）、`Starter Deck 10`（Gundam）、`UE23BT`（Union Arena）、`DIGIMON_BASE` 这类结果，无参考价值。**系列归属建议直接用 set 名，不要用该字段。**
- `crawl/__MACOSX/` 是 zip 解压残留，可忽略；`all_sets_temp.json` 是空壳。

### 3.4 本地卡片数据比 TCGPlayer 线上少

抽样比对了 TCGPlayer 搜索接口当前的 setName 聚合（`script_temp/out/agg_*.json`），本地 products.jsonl 明显不完整：

| 品类 | 本地系列 | 本地卡牌 | 线上系列 | 线上卡牌 | 本地/线上 |
|------|----------|----------|----------|----------|-----------|
| 01_Magic | 405 | 97047 | 445 | 115426 | 84% |
| 02_YuGiOh | 605 | 43524 | 613 | 46653 | 93% |
| 03_Pokemon | 197 | 26635 | 216 | 29926 | 89% |
| 62_Flesh_and_Blood_TCG | 99 | 5990 | 105 | 10619 | 56% |
| 68_One_Piece_Card_Game | 83 | 5008 | 85 | 7292 | 69% |
| 71_Disney_Lorcana | 18 | 2739 | 20 | 3769 | 73% |
| 85_Pokemon_Japan | 358 | 26016 | 455 | 30379 | 86% |

本地占比最低的三个品类：Flesh_and_Blood_TCG 56%、One_Piece_Card_Game 69%、Disney_Lorcana 73%。

典型例子：Pokemon 的 `SV: Scarlet & Violet 151`（线上 215 张）本地完全没有；`Modern Horizons 3` 本地 424 / 线上 665；`Theros` 本地 94 / 线上 260。完整逐系列差异见 `csv/series_count_compare.csv`。

### 3.5 系列名书写不规范，需要归一化才能对上

- 代号前缀不统一：`SWSH08: Fusion Strike`、`SWSH: Crown Zenith`、`SM - Cosmic Eclipse`、`XY - Steam Siege`、`ME: Ascended Heroes`、`EX Crystal Guardians`，而 Holodex 侧是纯系列名（`Fusion Strike`、`Cosmic Eclipse`…）。
- 大小写/单复数/连词差异：`POP Series 1` vs `Pop Series 1`、`Diamond and Pearl Promos` vs `Diamond and Pearl Promo`、`Rumble` vs `Pokemon Rumble`。
- 版本变体拆分方式不同：TCGPlayer 把 `Jungle` 合为一项，Holodex 拆成 `Jungle 1st Edition` / `Jungle`；`Base Set` 对应 `Base Set 1st Edition` / `Shadowless` / `Unlimited` 三个 holodex set。本表取非变体名（`Jungle`、`Base Set Unlimited`）作为代表。
- 结论：**不能靠字符串全等关联，必须走归一化 + 分级匹配**，本表用的分级规则见文首图例；`exact` 以外的匹配都在下方可逐条复核。

### 3.6 tcgplayer_sets_rarities_all.json 与本地卡片数据的差异

该 json 是更早一次抓取的快照，品线与系列集合都和本地卡片数据对不齐：

| json 品线 | json 系列 | 本地已统计 | 本地缺 |
|-----------|-----------|------------|--------|
| Pokémon | 213 | 196 | 17 |
| Pokémon Japan | 443 | 352 | 91 |
| Magic: The Gathering | 444 | 399 | 45 |
| Yu-Gi-Oh! | 612 | 603 | 9 |
| One Piece Card Game | 75 | 72 | 3 |
| Disney Lorcana | 18 | 17 | 1 |
| Flesh and Blood TCG | 96 | 90 | 6 |
| Dragon Ball Super: Masters | 102 | 0 | 102 |

另外 `Dragon Ball Super: Masters` 品线（102 个系列）在 `category_cards_final/` 下**没有对应目录**，本地无任何卡片数据；而 crawl gameId 7 恰好就是它，59 个 holodex set 全部能在该品线里找到。

### 3.7 结论与建议

1. **有 logo 的 730 个系列可以放心用**：匹配规则保守（数字/罗马数字必须一致），全部命中项已逐条核对，未发现错配。其中 `inherit` 那 69 条是促销/预发售子线继承母系列 logo，语义上成立但属于推断，使用时可选择性采纳。
2. **要覆盖其余 2549 个系列，必须补 logo 来源**：优先 Pokemon Japan、Weiss Schwarz、Cardfight Vanguard、Flesh and Blood 这几个大品类。
3. **本地卡片数据需要重爬**（见 3.4），这直接影响 setNum 与后续识别召回。
4. 系列数量统计一律以「本地卡片数据」为准（本次 setNum 口径），若要改成 TCGPlayer 线上口径，用 `script_temp/fetch_tcg_agg.py` 抓聚合后按 json 品线回填即可。

