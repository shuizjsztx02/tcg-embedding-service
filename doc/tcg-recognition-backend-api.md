# TCG 识别服务：后端集成接口说明

文档版本：v1.0
更新日期：2026-09-09

## 1. 目的和范围

本文档定义业务后端调用 TCG 卡牌识别服务的对外契约。服务根据图片、已知 OCR 文字和品类范围识别卡牌，返回结构化卡牌信息和近期成交价趋势。

对外只暴露两种策略：

| 策略 | 请求方法与路径 | 适用场景 |
| --- | --- | --- |
| serial | `POST /v2/recognize/serial` | 默认推荐。先做视觉召回，仅在视觉证据不足时再使用文本证据，吞吐和成本更低。 |
| fusion | `POST /v2/recognize/fusion` | 优先用图像 + OCR 文字联合纠错时使用。它会合并两路召回，延迟和 CPU 消耗通常更高。 |

`POST /v2/recognize` 可作为历史兼容别名，固定等同于 `serial`；新的业务代码不应依赖它。

> 注：以上是对外目标契约。截至本文档日期，现有 FastAPI 核心路由仍使用 `file`、`ocr_text` 和内部品类代码，并且不支持 URL/服务器本地路径。在 API 网关或路由适配层完成第 3 节的转换后，才可按本文档对外承诺。

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
| `category` | string enum | 否 | 仅在指定品类的数据集内检索。不传时检索当前发布的全部品类。 |
| `confidence` | number | 否 | `text` 的上游 OCR 可信度，必须满足 `0 <= confidence <= 1`。不传时不对 OCR 做额外置信。它不是卡牌匹配的输出置信度。 |

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
| `category` | `category` | 品类代码（见下表） |
| `confidence` | `confidence` | 随 OCR 证据传递；现有核心路由需增加该字段才能真正生效 |

### 3.3 `category` 枚举

对外仅接受下表的展示值，大小写、标点和空格必须完全一致。网关转为内部代码后再调用核心服务。

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

不传 `category` 表示全品类检索；传入不在枚举中的值时返回 HTTP 400。

## 4. 调用示例

### 4.1 上传本地文件（推荐）

```bash
curl -sS -X POST 'http://127.0.0.1:8003/v2/recognize/serial' \\
  -F 'image=@/opt/tcg-service/data/inbox/catalog-2026-09-09/category_cards/03_Pokemon/images/201276_200w.jpg;type=image/jpeg' \\
  -F 'text=Zeraora GX\n033/060\nSM7a' \\
  -F 'category=Pokémon Japan' \\
  -F 'confidence=0.96' | python3 -m json.tool
```

### 4.2 使用图片 URL

```bash
curl -sS -X POST 'http://127.0.0.1:8003/v2/recognize/fusion' \\
  -F 'image=https://d38riav3v3q1e4.cloudfront.net/example/card.jpg?Expires=...&Signature=...&Key-Pair-Id=...' \\
  -F 'text=Zeraora GX\n033/060' \\
  -F 'category=Pokémon Japan' \\
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
    "dataSource": "visual",
    "confidence": null,
    "strategy": "serial"
  }
}
```

### 5.1 `text` 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `state` | boolean | `true` 代表已找到可返回的卡牌结果；`false` 代表未确认卡牌身份。 |
| `stateErrorReason` | string | `state=false` 时的稳定错误原因代码，例如 `NO_MATCH`、`AMBIGUOUS`、`NOT_A_CARD`、`NOT_IN_DATABASE`。成功时为空字符串。 |
| `isSportsCard` | boolean | TCG 服务固定返回 `false`。 |
| `cardIp` | string | 品类展示名称，与第 3.3 节枚举值一致。 |
| `seriesName`、`cardName`、`cardNumber`、`language`、`year`、`artist`、`rarity` | string | 卡牌元数据。无法从数据源确认时返回 `""`，不使用猜测值。 |
| `gradingAgency`、`gradingStatus` | string | 卡牌评级信息。未知时返回 `""`。 |
| `gradingValue` | number or null | 评级分数。未知时返回 `null`。 |
| `collectionAdviceTag`、`collectionAdviceText` | string | 收藏建议。未配置建议数据时返回 `""`。 |
| `marketValuationTrend` | string | 市场估值趋势：`up`、`down`、`flat` 或 `unknown`。 |
| `marketValuationAvg` | number or null | 市场估值平均值。未知时返回 `null`。 |
| `productId` | number or string or null | 商品主键。数据源 ID 为非整数时可保留为字符串，不丢失精度。 |
| `link`、`thumbnail` | string | 商品页和缩略图 URL。无值时为空字符串。 |

### 5.2 `priceTrend` 字段

`priceTrend` 是按 `soldDate` 升序排列的历史成交记录数组，无成交数据时返回空数组 `[]`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `priceTrend[].price.raw` | string | 数据源中的原始价格字符串，例如 `$2.29`。 |
| `priceTrend[].price.extracted` | number or null | 解析后的数字价格。无法解析时为 `null`。 |
| `priceTrend[].soldDate` | string | 成交日期，格式 `YYYY-MM-DD`。 |

多币种数据不应直接混合成单一数值趋势；如果数据源未保留币种，后端应对该结果保守返回 `[]`。

### 5.3 `monitor` 字段

`monitor` 用于观测最终结果采用了哪些证据以及实际执行策略，不作为商品业务信息展示。无论是否匹配成功，HTTP 200 响应都必须返回该对象；没有对应证据的排名、分数和置信度返回 `null`，不得用 `0` 代替缺失值。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `visual_rank` | integer or null | 最终 `productId` 在 DINOv2 视觉召回结果中的名次，从 1 开始。没有最终商品或该商品未进入视觉候选时为 `null`。 |
| `visual_score` | number or null | 最终商品的 DINOv2 原始视觉相似度。它是模型相似度而不是概率；不得复制到 `confidence`。 |
| `text_rank` | integer or null | 最终商品在 OCR/BGE 文本召回结果中的名次，从 1 开始。未执行文本召回或未进入文本候选时为 `null`。 |
| `text_score` | number or null | 最终商品的 OCR/BGE 原始文本相似度。仅解析卡号等规则但未执行 BGE 召回时为 `null`。 |
| `dataSource` | string enum | 最终业务结论实际使用的证据来源，枚举规则见下表。它描述“用了什么证据”，不描述 serial/fusion 调度方式。 |
| `confidence` | number or null | 最终决策经过校准后的置信度，范围为 `[0,1]`。未上线概率校准或本次路径无法生成可比较置信度时必须为 `null`。 |
| `strategy` | string enum | 实际执行策略：`serial` 或 `fusion`。兼容路由 `/v2/recognize` 返回 `serial`。 |

#### `dataSource` 完整枚举

组合值按 `visual_text_llm` 的固定顺序命名，不得生成 `text_visual`、`llm_visual` 等同义值。

| 枚举值 | 适用情况 | 典型路径 |
| --- | --- | --- |
| `visual` | 最终结果只依据视觉检索接受。 | DINOv2 top-1 分数和 margin 达到直出门限；serial 高置信直出。 |
| `text` | 最终结果只依据客户端 OCR 文本、卡号/系列规则或文本召回接受。 | OCR 身份唯一命中，或文本 top-1 达到接受规则；保留给允许文本独立决策的实现。 |
| `visual_text` | 视觉和文本证据共同支持同一结果，未使用 LLM 决策。 | serial 的低视觉置信文本补救命中；fusion 合并 DINOv2 与 BGE 后接受。 |
| `llm` | 最终身份或未入库结论只由 LLM 产生，没有可用于最终决策的视觉/文本候选。 | LLM 识别后唯一查表命中，或返回 `NOT_IN_DATABASE`。 |
| `visual_llm` | LLM 基于视觉候选完成确认或消歧，未使用有效文本证据。 | 无 OCR 时视觉候选不确定，LLM 选择/确认候选。 |
| `text_llm` | LLM 基于 OCR/文本候选完成确认或消歧，视觉证据未参与最终结论。 | 文本候选有效但视觉候选不可用或未支持最终商品。 |
| `visual_text_llm` | 视觉、文本和 LLM 三类证据均参与最终结论。 | fusion 两路仍有歧义，再由 LLM 在候选中确认；serial 文本补救后仍需 LLM。 |
| `none` | 没有形成可采用的识别证据。 | `NO_MATCH`、`AMBIGUOUS`、`NOT_A_CARD`，或识别流程未得到候选。 |

`dataSource` 以“最终决策实际依赖”为准，而不是以“模块是否运行过”为准。例如 fusion 请求虽然同时执行了视觉和文本召回，但文本结果未支持最终商品且最终按视觉规则接受时，应返回 `visual`，不能因为策略名是 fusion 就返回 `visual_text`。LLM 仅执行了格式整理、没有影响商品选择时，也不得在来源中增加 `llm`。

## 6. 未命中与错误处理

业务不命中不等于 HTTP 请求失败：服务返回 HTTP 200，并将 `text.state` 设为 `false`。调用方应以 `state` 判断是否展示卡牌结果。

| 情形 | HTTP | `text.stateErrorReason` | 调用方处理 |
| --- | --- | --- | --- |
| 已确认匹配 | 200 | `""` | 使用 `text` 和 `priceTrend`。 |
| 证据不足或候选歧义 | 200 | `AMBIGUOUS` 或 `NO_MATCH` | 提示用户补拍清晰图片或补充文字；`monitor.dataSource=none`。 |
| 图片不是卡牌 | 200 | `NOT_A_CARD` | 提示重新上传单张 TCG 卡牌图片；`monitor.dataSource=none`。 |
| 识别出身份但库中无该商品 | 200 | `NOT_IN_DATABASE` | 可展示身份字段，但不应展示为已命中库内商品。 |
| 缺失图片字段 | 422 | 不适用 | 修正请求后重试。 |
| 非法图片、图片过大、URL/路径不可读 | 400 或 413 | 不适用 | 修正输入后重试。 |
| 品类不在枚举内、`confidence` 超出范围 | 400 | 不适用 | 修正参数后重试。 |
| 模型、数据库未就绪、队列满 | 503 | 不适用 | 按退避重试策略重试。 |

## 7. 与当前核心服务的适配清单

要让第 1–6 节成为可用的对外 API，适配层或核心服务还需完成以下最小更改：

1. 暴露同名 `image` 的文件上传和 URL/白名单路径两种输入，在取得图片后复用现有解码、大小和帧数校验。
2. 将 `text` 转发为 `ocr_text`，校验 `confidence` 并将其与 OCR 证据一起传递。
3. 将第 3.3 节的展示枚举转为内部品类代码，不向内部检索层传入展示文案。
4. 将现有 `RecognizeResponse`中的品牌、商品、价格数据映射为第 5 节的 `text` 和 `priceTrend`。数据不存在时保持空值约定，不伪造字段。
5. 根据候选的视觉/文本排名和分数、LLM 是否真正参与决策以及实际策略，组装 `monitor`；`confidence` 未校准前保持 `null`。
6. 所有 HTTP 200 响应保证存在 `text`、`priceTrend` 和 `monitor`；不命中则使用 `state=false` 而不使用 HTTP 500。
