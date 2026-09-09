# TCG 识别服务：后端集成接口说明

文档版本：v1.2
更新日期：2026-09-09

## 1. 目的和范围

本文档定义业务后端调用 TCG 卡牌识别服务的对外契约。服务自动判断图片是否为支持的 TCG 卡牌及所属品类，再根据图片和可选 OCR 文字识别卡牌，返回结构化卡牌信息、成交价格趋势和监控信息。内部模型及工作流调用对后端调用方透明。

对外只暴露两种策略：

| 策略 | 请求方法与路径 | 适用场景 |
| --- | --- | --- |
| serial | `POST /v2/recognize/serial` | 默认推荐。先做视觉召回，仅在视觉证据不足时再使用文本证据，吞吐和成本更低。 |
| fusion | `POST /v2/recognize/fusion` | 优先用图像 + OCR 文字联合纠错时使用。它会合并两路召回，延迟和 CPU 消耗通常更高。 |

`POST /v2/recognize` 可作为历史兼容别名，固定等同于 `serial`；新的业务代码不应依赖它。

> 注：以上是对外目标契约。截至本文档日期，现有 FastAPI 核心路由仍使用 `file`、`ocr_text` 和内部品类代码，不支持 URL/服务器本地路径，也尚未完成自动品类判断与目标响应组装。完成第 3、5、7 节的适配后，才可按本文档对外承诺。

## 2. 通用约定

- **Content-Type**：`multipart/form-data`。
- **字符集**：文本按 UTF-8 处理。
- **超时**：调用方应将 HTTP 超时设置为不小于 30 秒。
- **图片限制**：单张、静态图片，上传大小不超过 10 MiB，解码后不超过 20MP。
- **幂等性**：本接口不持久化请求数据，重试同一请求是安全的。

## 3. 请求参数

### 3.1 字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `image` | file 或 string | 是 | 卡牌图片。可传二进制文件、HTTPS URL，或服务器白名单目录下的绝对路径，三者必须且只能选一种。 |
| `text` | string | 否 | 上游 OCR 结果或人工输入的卡面文字。多个文字块以换行符（`\n`）分隔；空串视为未提供。上限为 8,192 个字符。 |
| `category` | string enum | 否 | 可选品类范围，枚举见第 3.3 节。首版调用方不传时由服务自动判断；传入时必须与服务识别的品类一致。 |
| `confidence` | number | 否 | `text` 的上游 OCR 可信度，必须满足 `0 <= confidence <= 1`。不传时不对 OCR 做额外置信。它不是卡牌匹配的输出置信度。 |

首版调用方预计不传 `category`，但字段保留，接口结构不变。未传时服务自动判断品类；传入时它是调用方声明的范围，不会关闭服务自身的图片有效性与品类校验。两者不一致时返回 HTTP 400，禁止在错误品类中继续匹配。

### 3.2 `image` 的三种传入方式

| 方式 | 传值 | 调用人员注意事项 |
| --- | --- | --- |
| 本地文件上传 | `image=@/path/to/card.jpg` | “本地”指调用方所在主机；HTTP 客户端需将文件内容上传。这是最通用、最安全的方式。 |
| HTTPS URL | 文本字段 `image=https://...` | 服务端下载后按同一图片校验。仅允许 `https`，必须防止访问内网地址、跟随跳转到非 HTTPS 地址。带签名参数的 CloudFront URL 可直接传入，不要二次 URL 编码。 |
| 服务器本地路径 | 文本字段 `image=/opt/tcg-service/data/.../card.jpg` | 路径必须位于配置的读取白名单根目录中。不得根据客户端传入的任意路径读取文件。该方式只适用于与服务部署在同一主机或共享挂载中的调用方。 |

同名 `image` part 上传文件时带 `filename`，传 URL/路径时不带 `filename`；API 适配层据此区分两种输入。转换规则如下：

| 对外逻辑字段 | 网关实际接收字段 | 转发至现有核心识别路由 |
| --- | --- | --- |
| 本地上传 `image` | `image` （binary） | `file` （binary） |
| URL 或白名单路径 `image` | `image` （string） | 适配层取得图片后以 `file` 转发 |
| `text` | `text` | `ocr_text` |
| `category` | `category` | 校验展示枚举，并转换为内部品类代码 |
| `confidence` | `confidence` | 随 OCR 证据传递；现有核心路由需增加该字段才能真正生效 |

### 3.3 `category` 与返回 `cardIp` 枚举

可选入参 `category` 与返回字段 `cardIp` 使用同一组展示值。服务只接受下表的规范值，大小写、标点和空格必须完全一致，并在进入匹配前转换成内部代码。

| 对外 `category` | 内部代码 |
| --- | --- |
| `Pokémon` | `pokemon` |
| `Pokémon Japan` | `pokemon_japan` |
| `Magic` | `magic` |
| `Yu-Gi-Oh!` | `yugioh` |
| `One Piece` | `onepiece` |
| `Disney Lorcana` | `disney_lorcana` |
| `Flesh and Blood` | `flesh_blood` |
| `Dragon Ball Super: Masters` | `dragon_ball` |

调用方不传 `category` 时无需关心内部代码；服务会自动得到规范 `cardIp`。自动判断失败或产生非法品类时返回 HTTP 503，不静默执行全品类检索。

### 3.4 自动预检与内容补全

调用方只需调用 recognize API，不传任何工作流名称、节点或 `intent`。服务内部会自动完成：

1. 匹配前检查图片是否为有效 TCG、是否为体育卡并确定 `cardIp`。
2. 在确定的品类范围内执行 serial 或 fusion 匹配。
3. 在需要时完成候选消歧，并补充评级和收藏建议。

内部预检不可用时返回 HTTP 503。商品已经可靠确定但内容补全失败时不推翻匹配，只将对应扩展字段置空并在 monitor 记录 warning；商品身份必须依赖内容识别才能确定时，失败返回 `monitor.status_match=candidates` 或 `unrecognized`。

## 4. 调用示例

### 4.1 上传本地文件（推荐）

```bash
curl -sS -X POST 'http://127.0.0.1:8003/v2/recognize/serial' \
  -F 'image=@/opt/tcg-service/data/inbox/catalog-2026-09-09/category_cards/03_Pokemon/images/201276_200w.jpg;type=image/jpeg' \
  -F 'text=Zeraora GX\n033/060\nSM7a' \
  -F 'confidence=0.96' | python3 -m json.tool
```

### 4.2 使用图片 URL

```bash
curl -sS -X POST 'http://127.0.0.1:8003/v2/recognize/fusion' \
  -F 'image=https://d38riav3v3q1e4.cloudfront.net/example/card.jpg?Expires=...&Signature=...&Key-Pair-Id=...' \
  -F 'text=Zeraora GX\n033/060' \
  -F 'confidence=0.96' | python3 -m json.tool
```

URL 必须放在单引号中，否则 shell 会将 `&` 解释为后台命令分隔符。

### 4.3 策略选择

- 没有 `text`：使用 `serial`；`fusion` 没有可融合的文本证据。
- 有质量较高的 OCR 文本、希望优先避免视觉相似卡误匹配：使用 `fusion`。
- 延迟或 CPU 成本优先：使用 `serial`。

## 5. 成功响应契约

成功返回 HTTP 200。业务识别结果统一返回以下 JSON：

```json
{
  "text": {
    "state": true,
    "stateErrorReason": "",
    "isSportsCard": false,
    "cardIp": "Pokémon Japan",
    "seriesName": "SM7a: Thunderclap Spark",
    "cardName": "Zeraora GX",
    "cardNumber": "033/060",
    "language": "Japanese",
    "year": "2018",
    "artist": "PLANETA Otani",
    "gradingAgency": "CGC",
    "gradingStatus": "GRADED",
    "gradingValue": 10,
    "rarity": "Double Rare",
    "collectionAdviceTag": "Long Hold",
    "collectionAdviceText": "CGC 10 Japanese GX from 2018; solid hold for Zeraora collectors.",
    "marketValuationTrend": "up",
    "marketValuationAvg": 40.22,
    "productId": 123334,
    "link": "",
    "thumbnail": ""
  },
  "priceTrend": [
    {"price": {"raw": "$2.29", "extracted": 2.29}, "soldDate": "2026-08-10"},
    {"price": {"raw": "$2.29", "extracted": 2.29}, "soldDate": "2026-08-11"},
    {"price": {"raw": "$2.29", "extracted": 2.29}, "soldDate": "2026-08-12"}
  ],
  "monitor": {
    "visual_rank": 1,
    "visual_score": 1.0,
    "text_rank": null,
    "text_score": null,
    "fusion_score": null,
    "margin": 0.18,
    "ocr_used": false,
    "text_retrieval_used": false,
    "input_text_confidence": 0.96,
    "candidate_count": 5,
    "dataSource": "visual",
    "confidence": null,
    "strategy": "serial",
    "status_match": "matched",
    "price_source": "pg_sales",
    "field_sources": {
      "state": "dify_classify",
      "stateErrorReason": "dify_classify",
      "isSportsCard": "dify_classify",
      "cardIp": "dify_classify",
      "seriesName": "pg",
      "cardName": "pg",
      "cardNumber": "pg",
      "language": "dify_enrich",
      "year": "pg_derived",
      "artist": "dify_enrich",
      "gradingAgency": "dify_enrich",
      "gradingStatus": "dify_enrich",
      "gradingValue": "dify_enrich",
      "rarity": "pg",
      "collectionAdviceTag": "dify_enrich",
      "collectionAdviceText": "dify_enrich",
      "marketValuationTrend": "pg_derived",
      "marketValuationAvg": "pg",
      "productId": "pg",
      "link": "none",
      "thumbnail": "none"
    },
    "llm_enrich_status": "succeeded",
    "warnings": [],
    "request_id": "d14171a7-c3d8-4835-a8d8-3be585590e35",
    "dataset_version": "c685f480-ca25-4121-8145-d70a3aa02ffd",
    "model_version": "13e8cd27a36b8d6f373809f4bf2ab7e59c2e1a48d0645c30717b15335bc65460",
    "workflow_version": "tcg-v3-20260824",
    "decision_version": "c583c8ffbfac2777621bf7192feb2c2478afdc20fb48f58ff284aac9c4c2b508",
    "latency_ms": 1420.5,
    "timings_ms": {
      "classify": 420.1,
      "visual": 155.3,
      "text": 0.0,
      "database": 18.7,
      "enrich": 801.2
    }
  }
}
```

### 5.1 `text` 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `state` | boolean | 前置 Dify 对图片内容有效性的判断。`true` 表示是八种支持 IP 中的有效 TCG；它不表示已经命中 PG，库内匹配结果见 `monitor.status_match`。 |
| `stateErrorReason` | string | 只说明 `state=false` 的内容拒绝原因，例如 `NOT_A_TCG_CARD`、`SPORTS_CARD`、`UNSUPPORTED_CARD_IP`。不得承载 `matched/candidates/recognized_no_db/unrecognized` 等数据库匹配状态。成功时为空字符串。 |
| `isSportsCard` | boolean | 服务自动预检结果。为 `true` 时停止 TCG 匹配，并令 `state=false`。 |
| `cardIp` | string | 服务自动判断的规范品类名称，与第 3.3 节枚举值一致；非 TCG/体育卡拒绝结果可为空字符串。 |
| `seriesName`、`cardName`、`cardNumber`、`language`、`year`、`artist`、`rarity` | string | 按第 5.2 节逐字段合并：语义一致且有效的 PG 字段优先，缺失时使用后置 Dify LLM 结果。仍无法确认时返回 `""`。 |
| `gradingAgency`、`gradingStatus` | string | 从图片内容识别的卡牌评级信息。未知时返回 `""`。 |
| `gradingValue` | number or null | 从图片内容识别的评级分数。未知时返回 `null`。 |
| `collectionAdviceTag`、`collectionAdviceText` | string | 服务内容补全阶段生成的收藏建议；补全失败时返回 `""`，不影响已经可靠确定的商品匹配。 |
| `marketValuationTrend` | string | 根据最终采用的 `priceTrend` 计算：`up`、`down`、`flat` 或 `unknown`；数据不足时可采用 Dify LLM 值，否则为 `unknown`。 |
| `marketValuationAvg` | number or null | 命中商品且 PG `raw_json.marketPrice` 有效时直接使用；例如 `marketPrice: 5.6` 返回 `5.6`。该字段缺失或无效时才使用 Dify LLM 估值。 |
| `productId` | number or string or null | 仅返回已在 PG 复核命中的商品主键；`recognized_no_db` 不得由 LLM 编造 productId。 |
| `link`、`thumbnail` | string | 优先使用 PG 中可构造、可访问的数据；缺失时允许使用 Dify 返回值，但必须通过 HTTPS、域名白名单和格式校验，否则返回空字符串。 |

### 5.2 PG 字段与目标 `text` 字段映射

字段合并按单个字段执行，而不是“命中 PG 后整个对象都只用 PG”。PG 值只有在非空、类型正确且与目标字段语义一致时才具有优先级；PG 缺失、空值或语义不一致时，使用 `intent=recognize_enrich` 的 LLM 结果兜底。LLM 不得覆盖已有的有效 PG 值，每个最终字段来源写入 `monitor.field_sources`。

以下映射基于当前商品 JSON 示例：

| 目标字段 | PG 可用字段 | 采用规则 | PG 不可用时 |
| --- | --- | --- | --- |
| `state` | 无 | 使用前置 Dify `classify.state`，它表示是否为支持的有效 TCG，不表示是否命中数据库。 | 不再进行第二套判断。 |
| `stateErrorReason` | 无 | 使用前置 Dify 原因并归一为稳定代码；匹配状态禁止写入此字段。 | 系统调用失败使用 HTTP 503，不伪造业务原因。 |
| `isSportsCard` | 无 | 使用前置 Dify `classify.isSportsCard`。 | 无兜底；前置输出非法视为 503。 |
| `cardIp` | `categories.display_name/code`；`raw_json.productLineName` 仅用于核对 | 数据集品类能精确映射八种枚举时可确认 Dify 结果。`productLineName=Pokemon` 不能区分 `Pokémon` 与 `Pokémon Japan`，不得单独覆盖。 | 使用前置 Dify `cardIp`。 |
| `seriesName` | `raw_json.setName` | 含义一致，直接采用；`setCode` 只用于校验/消歧，不替代完整系列名。 | Dify 根据图片、OCR、`setCode` 和候选上下文补齐。 |
| `cardName` | `raw_json.productName` | 优先采用。仅当末尾严格等于 ` - {customAttributes.number}` 时移除该编号后缀，例如 `Drakloak - 248/217` → `Drakloak`。 | Dify 补齐。`productUrlName` 只能作辅助，不直接作为展示名。 |
| `cardNumber` | `raw_json.customAttributes.number` | 含义一致，保留斜杠和前缀后直接采用。规范化列 `number_norm` 只用于检索，不替代展示值。 | Dify 补齐。 |
| `language` | 当前商品 JSON 无可靠商品级字段 | `price_sales.language` 是成交记录属性，不代表卡牌标准语言，禁止回填。若内部品类明确为 `pokemon_japan`，可派生 `Japanese`。 | Dify 从卡面文字/评级标签识别。 |
| `year` | `raw_json.customAttributes.releaseDate` | 日期合法时取 UTC 年份，例如 `2026-01-30T00:00:00Z` → `2026`，来源记为 `pg_derived`。 | Dify 补齐。 |
| `artist` | 当前示例无对应字段 | `description/flavorText` 不等于画师，不能代替。 | Dify 仅从图片中可见 artist/illustrator 字样提取；不确定时为空。 |
| `gradingAgency`、`gradingStatus`、`gradingValue` | 无 | 这些是本次上传图片的封装/评级状态，不是商品目录固有属性。 | 始终由 Dify 从图片识别；无法确认时返回空值/null。 |
| `rarity` | `raw_json.rarityName`；次选 `raw_json.customAttributes.rarityDbName` | 优先采用 `rarityName`；为空时采用 `rarityDbName`。两者冲突时记录 warning 并以 `rarityName` 为准。 | Dify 补齐。 |
| `collectionAdviceTag`、`collectionAdviceText` | 无 | 商品目录没有同义字段。 | 始终由 Dify 生成。 |
| `marketValuationTrend` | PG `price_sales` 序列 | PG 有足够同币种成交数据时由服务端确定性计算，不直接读取 `lowestPrice` 等快照字段。 | 先根据 LLM 生成的 `priceTrend` 计算；仍不足时使用 Dify 给出的趋势或 `unknown`。 |
| `marketValuationAvg` | `raw_json.marketPrice` | 有效非负数时直接采用。`lowestPrice`、`lowestPriceWithShipping` 和 `score` 含义不同，禁止替代。 | Dify LLM 估值兜底，并在字段来源中标记。 |
| `productId` | `raw_json.productId` / `cards.product_id` | 只有视觉、文本或 LLM 身份经过 PG 查表唯一命中时返回。 | 返回 `null`，不得由 LLM 猜测。 |
| `link` | `productLineUrlName/setUrlName/productUrlName` 仅为 URL slug | 只有配置了官方基础域名和固定 URL 模板时才可确定性拼接。 | Dify 可返回候选 URL，但必须校验 HTTPS 与域名白名单；失败返回 `""`。 |
| `thumbnail` | `card_images.relative_path` 或商品 JSON 中未来增加的缩略图字段 | 通过已配置的静态资源基础地址生成，不能把服务器文件路径直接暴露给调用方。 | Dify 返回值必须通过 HTTPS 与域名白名单；失败返回 `""`。 |

以下 PG 字段虽然可保留或传给 Dify 作上下文，但不能直接映射到当前 `text`：`shippingCategoryId`、`productTypeId`、`sealed`、`lowestPriceWithShipping`、`lowestPrice`、`totalListings`、`sellerListable`、`maxFulfillableQuantity`、攻击/HP/弱点/抗性等 `customAttributes`。特别是商品 JSON 的 `score` 不是 DINO/BGE 匹配分数，禁止写入 `monitor.visual_score`、`text_score` 或 `confidence`。

### 5.3 `priceTrend` 字段

`priceTrend` 有两个内部来源，调用方无需指定：优先使用后续导入 PG 的 prices 成交数据；PG 没有该商品的可用成交明细时，由后置 Dify 工作流中的 LLM 生成价格曲线。不得调用 JustTCG 或其它外部价格 API，两个来源不得混合；两者均无有效结果时返回空数组 `[]`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `priceTrend[].price.raw` | string | PG 来源由 `purchasePrice` 按币种格式化，例如 `$2.29`；LLM 来源由生成的美元数值统一格式化。 |
| `priceTrend[].price.extracted` | number or null | PG 来源直接取纯成交价 `purchasePrice`，不包含 `shippingPrice`；LLM 来源取其生成并通过校验的非负有限数值。 |
| `priceTrend[].soldDate` | string | PG 来源将 `orderDate` 转为 UTC 日期；LLM 来源使用其生成并通过校验的日期。统一格式为 `YYYY-MM-DD`。 |

PG 来源按完整 `orderDate` 升序排序，同一天的多笔成交全部保留，不按日期去重；其中 `price.extracted=purchasePrice`，不包含 `shippingPrice`。`shippingPrice`、`condition`、`variant`、`language` 和 `quantity` 原样保存在 PG 成交明细中，当前响应暂不输出。多币种数据不直接混合成单一趋势；PG 数据缺少可确认币种时视为不可用并进入 LLM 兜底。

LLM 价格曲线只允许在商品身份已经唯一确认时生成，即 `status_match=matched` 或 `recognized_no_db`；候选歧义和无法识别时必须返回 `[]`。生成结果必须转换成相同 schema，并校验美元金额为有限非负数、日期合法且不晚于请求日期、数组不超过 100 个点，随后按日期升序排序。它是模型估计，不是已验证的真实成交记录，因此必须同时返回 `monitor.price_source=llm_generated` 和 warning `PRICE_TREND_LLM_GENERATED`；任何一个点不合法时拒绝整条 LLM 曲线并返回 `[]`，不能与 PG 数据拼接或用 JustTCG 补救。

### 5.4 `monitor` 字段

`monitor` 用于观测最终结果采用了哪些证据以及调用方请求的策略，不作为商品业务信息展示。无论是否匹配成功，HTTP 200 响应都必须返回该对象及下表中的稳定字段；没有对应证据的排名、分数和置信度返回 `null`，不得用 `0` 代替缺失值。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `visual_rank` | integer or null | 最终 `productId` 在 DINOv2 视觉召回结果中的名次，从 1 开始。没有最终商品或该商品未进入视觉候选时为 `null`。 |
| `visual_score` | number or null | 最终商品的 DINOv2 原始视觉相似度。它是模型相似度而不是概率；不得复制到 `confidence`。 |
| `text_rank` | integer or null | 最终商品在 OCR/BGE 文本召回结果中的名次，从 1 开始。未执行文本召回或未进入文本候选时为 `null`。 |
| `text_score` | number or null | 最终商品的 OCR/BGE 原始文本相似度。仅解析卡号等规则但未执行 BGE 召回时为 `null`。 |
| `fusion_score` | number or null | fusion/RRF 重排后的内部分数；未执行融合或最终商品未进入融合候选时为 `null`。它不是概率。 |
| `margin` | number or null | 最终决策使用的 top-1 与 top-2 分差；没有可比较的第二候选时为 `null`。 |
| `ocr_used` | boolean | 客户端 `text` 是否实际参与规则判断或身份提取。 |
| `text_retrieval_used` | boolean | 是否实际执行 BGE 文本向量召回；与仅解析卡号等轻量规则区分。 |
| `input_text_confidence` | number or null | 原样记录并校验后的入参 `confidence`，不等于输出决策 `confidence`。 |
| `candidate_count` | integer | 最终决策阶段保留的候选数量。 |
| `dataSource` | string enum | 最终业务结论实际使用的证据来源，枚举规则见下表。它描述“用了什么证据”，不描述 serial/fusion 调度方式。 |
| `confidence` | number or null | 最终决策经过校准后的置信度，范围为 `[0,1]`。未上线概率校准或本次路径无法生成可比较置信度时必须为 `null`。 |
| `strategy` | string enum | 调用方请求的策略：`serial` 或 `fusion`。fusion 在无可用文字时可复用视觉路径，但仍返回 `fusion`；兼容路由 `/v2/recognize` 返回 `serial`。 |
| `status_match` | string enum | 数据库匹配状态，取代截图中原先占用顶层 `status` 的语义；完整枚举见下表。 |
| `price_source` | string enum | `pg_sales`、`llm_generated` 或 `none`。它独立于商品身份 `dataSource`。 |
| `field_sources` | object | `text` 中每个业务字段的最终来源。值只能为 `pg`、`pg_derived`、`dify_classify`、`dify_enrich`、`llm_generated`、`system` 或 `none`。 |
| `llm_enrich_status` | string enum | 后置工作流状态：`succeeded`、`failed` 或 `skipped`。失败原因写入 `warnings`。 |
| `warnings` | string[] | 可降级问题和数据冲突代码，例如 `PRICE_TREND_LLM_GENERATED`、`PG_RARITY_CONFLICT`、`DIFY_ENRICH_FAILED`。 |
| `request_id` | string | 本次请求的唯一追踪 ID。 |
| `dataset_version`、`model_version`、`workflow_version`、`decision_version` | string or null | 数据、向量模型、Dify 工作流和决策规则版本，用于复现结果。 |
| `latency_ms` | number | 服务端总耗时。 |
| `timings_ms` | object | `classify/visual/text/database/enrich` 等阶段耗时；未执行阶段返回 `0.0`。 |

#### 来源监控枚举

| 字段 | 枚举值 | 含义 |
| --- | --- | --- |
| `price_source` | `pg_sales` | `priceTrend` 来自 PG 逐笔成交数据，`price.extracted` 为 `purchasePrice`。 |
| `price_source` | `llm_generated` | PG 无可用成交数据，曲线由 Dify LLM 估计生成；必须同时带 `PRICE_TREND_LLM_GENERATED` warning。 |
| `price_source` | `none` | 没有返回有效价格曲线。 |
| `field_sources.*` | `pg` | 直接采用 PG 原始或规范化字段。 |
| `field_sources.*` | `pg_derived` | 由 PG 字段按确定性规则派生，例如由 `releaseDate` 取年份。 |
| `field_sources.*` | `dify_classify` | 来自前置图片有效性/IP 分类分支。 |
| `field_sources.*` | `dify_enrich` | 来自后置 Dify 的字段识别或内容补全。 |
| `field_sources.*` | `llm_generated` | 来自后置 LLM 的市场估值/趋势生成，不是 PG 事实。 |
| `field_sources.*` | `system` | 由服务固定规则或请求上下文生成。 |
| `field_sources.*` | `none` | 最终字段为空且没有可采用来源。 |

#### `status_match` 完整枚举

顶层不得再使用 `status` 表达下列匹配结论；目标业务响应不输出顶层 `status`。如果网关统一包装必须保留顶层 `status`，它只能表示 HTTP/网关处理状态，不能取下列值。

| 枚举值 | 含义 |
| --- | --- |
| `matched` | 已确定且命中 PG 记录，`text.productId` 不为空。 |
| `candidates` | 存在多个候选或证据不足，不自动报成命中，`text.productId` 为 `null`。 |
| `recognized_no_db` | LLM 提取了足够身份，但在限定品类内查询 PG 无命中；允许展示 LLM 身份字段，`text.productId` 为 `null`。 |
| `unrecognized` | 无足够身份或候选；保留可降级 warning，`text.productId` 为 `null`。 |
| `not_a_card` | 前置 Dify 明确判断为非支持 TCG 或体育卡；低向量相似度本身不能产生此状态。 |

#### `dataSource` 完整枚举

组合值按 `visual_text_llm` 的固定顺序命名，不得生成 `text_visual`、`llm_visual` 等同义值。

| 枚举值 | 适用情况 | 典型路径 |
| --- | --- | --- |
| `visual` | 最终结果只依据视觉检索接受。 | DINOv2 top-1 分数和 margin 达到直出门限；serial 高置信直出。 |
| `text` | 最终结果只依据客户端 OCR 文本、卡号/系列规则或文本召回接受。 | OCR 身份唯一命中，或文本 top-1 达到接受规则；保留给允许文本独立决策的实现。 |
| `visual_text` | 视觉和文本证据共同支持同一结果，未使用 LLM 决策。 | serial 的低视觉置信文本补救命中；fusion 合并 DINOv2 与 BGE 后接受。 |
| `llm` | 最终身份或未入库结论只由 LLM 产生，没有可用于最终决策的视觉/文本候选。 | LLM 识别后唯一查表命中，或形成 `recognized_no_db` 结论。 |
| `visual_llm` | LLM 基于视觉候选完成确认或消歧，未使用有效文本证据。 | 无 OCR 时视觉候选不确定，LLM 选择/确认候选。 |
| `text_llm` | LLM 基于 OCR/文本候选完成确认或消歧，视觉证据未参与最终结论。 | 文本候选有效但视觉候选不可用或未支持最终商品。 |
| `visual_text_llm` | 视觉、文本和 LLM 三类证据均参与最终结论。 | fusion 两路仍有歧义，再由 LLM 在候选中确认；serial 文本补救后仍需 LLM。 |
| `none` | 没有形成可采用的商品身份。 | `status_match` 为 `unrecognized` 或 `not_a_card`，或识别流程未得到候选。 |

`dataSource` 以“最终商品身份实际依赖”为准，而不是以“模块是否运行过”为准。内部前置分类只确定图片有效性和检索范围，不计入商品身份来源；后置内容补全只生成评级/收藏建议且没有改变商品选择时也不计入 `llm`。例如自动分类后由 DINOv2 高分直出并补充收藏建议，仍返回 `visual`。只有 LLM 实际确认或改变 `productId` 时才使用带 `_llm` 的枚举。

## 6. 未命中与错误处理

业务不命中不等于 HTTP 请求失败。`text.state` 只表达图片是否为支持的有效 TCG；调用方以 `monitor.status_match` 判断是否命中 PG、是否展示候选或是否仅展示 LLM 识别身份。例如有效 TCG 没有库内命中时，仍可返回 `text.state=true` 和 `monitor.status_match=recognized_no_db`。

| 情形 | HTTP | `text.state` | `text.stateErrorReason` | `monitor.status_match` | 调用方处理 |
| --- | --- | --- | --- | --- | --- |
| 已确认命中 PG | 200 | `true` | `""` | `matched` | 使用 `text` 和 `priceTrend`。 |
| 有效 TCG，但候选歧义 | 200 | `true` | `""` | `candidates` | 提示用户补拍清晰图片或补充文字。 |
| 有效 TCG，LLM 已识别但 PG 无记录 | 200 | `true` | `""` | `recognized_no_db` | 可展示 LLM 身份字段，但不得展示为库内商品。 |
| 有效 TCG，但没有足够身份或候选 | 200 | `true` | `""` | `unrecognized` | 提示重新拍摄；查看 `monitor.warnings`。 |
| 图片不是支持的 TCG | 200 | `false` | `NOT_A_TCG_CARD` 或 `UNSUPPORTED_CARD_IP` | `not_a_card` | 提示重新上传支持的 TCG 卡牌。 |
| 图片是体育卡 | 200 | `false` | `SPORTS_CARD` | `not_a_card` | 当前服务不进入 TCG 匹配。 |
| 缺失图片字段 | 422 | 不适用 | 不适用 | 不适用 | 修正请求后重试。 |
| 非法图片、图片过大、URL/路径不可读 | 400 或 413 | 不适用 | 不适用 | 不适用 | 修正输入后重试。 |
| `category` 非法、与自动识别品类冲突，或 `confidence` 超出范围 | 400 | 不适用 | 不适用 | 不适用 | 修正参数后重试。 |
| 自动预检超时/失败、输出非法或无法得到合法 `cardIp` | 503 | 不适用 | 不适用 | 不适用 | 按退避策略重试；禁止静默进入全品类匹配。 |
| 模型、数据库未就绪、队列满 | 503 | 不适用 | 不适用 | 不适用 | 按退避重试策略重试。 |

## 7. 内部实现适配清单

本节供 TCG 服务开发使用，不增加后端调用方参数。要让第 1–6 节成为可用的对外 API，适配层或核心服务还需完成以下更改：

1. 暴露同名 `image` 的文件上传和 URL/白名单路径两种输入，在取得图片后复用现有解码、大小和帧数校验。
2. 将 `text` 转发为内部 `ocr_text`，校验 `confidence` 并将其与 OCR 证据一起传递；外部首版不再依赖 category 入参。
3. 改造同一个 Dify Workflow：新增必填 `intent`，提供 `classify` 与 `recognize_enrich` 两个条件分支和各自的结构化输出；移除/禁用 JustTCG 分支，PG 无价格曲线时由后置 LLM 直接生成。
4. 在任何 DINO/BGE 检索前调用 `intent=classify`，严格验证四字段，并将合法 `cardIp` 映射为内部 category；系统故障与业务拒绝使用不同 HTTP 语义。
5. 修复 serial/fusion 决策与 Dify 查表：只有 LLM 真正参与商品身份确认时才将 `llm` 写入 `dataSource`。
6. 命中后从 PG 取得商品原始 JSON、`marketPrice` 和成交明细，按第 5.2 节逐字段合并；有效 PG 字段优先，缺失字段才使用 LLM。
7. 调用 `intent=recognize_enrich` 生成缺失身份字段、评级、收藏建议和必要的 LLM 价格曲线；PG `priceTrend` 存在时不得生成或混入 LLM 曲线。
8. 根据候选排名/分数、身份决策证据、请求策略、匹配状态、价格来源和逐字段来源组装 `monitor`；`confidence` 未校准前保持 `null`。
9. 将现有识别 `status` 迁移到 `monitor.status_match`；目标业务响应不再用顶层 `status` 表达匹配结果。
10. 所有 HTTP 200 响应保证存在 `text`、`priceTrend` 和 `monitor`；有效 TCG 未命中时通过 `status_match` 表达，不把 `text.state` 错误改成 `false`。
