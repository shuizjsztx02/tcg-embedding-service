# TCG 卡牌识别服务：后端集成接口说明

文档版本：v2.0
更新日期：2026-09-10

## 1. 服务地址与能力范围

后端通过 Nginx 访问服务：

```text
http://172.31.12.82:8003
```

当前服务仅支持宝可梦卡牌图库的视觉检索和 OCR 文本检索。它不会自动判断卡牌 IP、不会调用 Dify、不会返回价格趋势、收藏建议或标准化的卡牌业务详情。调用方应根据实际需要使用下列接口：

| 用途 | 方法与路径 | 推荐程度 |
| --- | --- | --- |
| 判断图片是否能可靠命中图库 | `POST /v1/match` | 推荐用于自动确认 |
| 获取视觉相似的前 5 个候选及商品原始数据 | `POST /v1/search` | 推荐用于人工确认或业务二次决策 |
| 识别卡面文字 | `POST /v1/ocr` | 按需使用 |
| 基于 OCR 文字检索前 5 个候选 | `POST /v1/ocr-match` | 图片视觉效果不佳时按需使用 |
| 查询服务与视觉索引状态 | `GET /v1/health` | 建议用于健康检查 |
| 获取图库缩略图 | `GET /v1/images/{card_id}` | 可选 |

`/` 返回内置的调试页面，不是后端集成接口。

## 2. 通用约定

- 所有上传接口使用 `multipart/form-data`，图片字段固定为 `file`。
- 只接收单张图片文件；图片大小不得超过 **10 MiB**。
- 已声明 MIME 类型时，必须以 `image/` 开头；服务还会解码校验图片内容。
- 不支持传图片 URL、服务器本地路径、`image` 字段、`text`/`ocr_text` 字段或 `category` 字段。
- 服务会自动进行 EXIF 方向归正、卡牌边界检测/透视矫正和方向候选检索。图片模糊、反光或卡牌过小时会返回 `warnings`，但不必然拒绝请求。
- 视觉相似度 `score` 是余弦相似度，不是百分比，也不是概率。
- HTTP 调用超时建议设为至少 30 秒；模型和索引均在服务启动时加载。

除文件上传外，接口无需鉴权参数。生产环境的访问控制由 Nginx 或调用方所在内网负责。

## 3. 健康检查

### `GET /v1/health`

```bash
curl -sS 'http://172.31.12.82:8003/v1/health'
```

成功响应示例：

```json
{
  "status": "ok",
  "index_size": 9434,
  "embedding_dim": 768,
  "version": "2026-09-10"
}
```

| 字段 | 说明 |
| --- | --- |
| `status` | 正常时为 `ok`。 |
| `index_size` | 已加载的视觉索引向量数。 |
| `embedding_dim` | 视觉向量维度。 |
| `version` | 视觉索引版本；未配置时为 `unknown`。 |

## 4. 自动视觉匹配

### `POST /v1/match`

该接口将图片检索结果与当前服务阈值比较：top-1 相似度须不低于 `MATCH_TAU`（默认 `0.775`），且与 top-2 的分差须不低于 `MATCH_MARGIN`（默认 `0.02`）。满足两项时返回 `matched`，否则返回 `rejected`；两种业务结果均为 HTTP 200。

```bash
curl -sS -X POST 'http://172.31.12.82:8003/v1/match' \
  -F 'file=@/path/to/card.jpg;type=image/jpeg'
```

匹配成功示例：

```json
{
  "status": "matched",
  "card_id": "100503_200w",
  "score": 0.9123,
  "margin": 0.0841,
  "top2_id": "100507_200w",
  "top2_score": 0.8282,
  "warnings": [],
  "preprocessing": {
    "quad_found": true,
    "warnings": [],
    "preprocess_ms": 18.2,
    "total_ms": 862.5
  }
}
```

拒绝示例：

```json
{
  "status": "rejected",
  "card_id": null,
  "score": 0.7412,
  "margin": 0.0168,
  "top2_id": null,
  "top2_score": null,
  "warnings": ["图像较模糊，建议在光线充足处重新拍摄"],
  "preprocessing": {"quad_found": false}
}
```

| 字段 | 说明 |
| --- | --- |
| `status` | `matched` 或 `rejected`。调用方应以此字段判断是否自动确认。 |
| `card_id` | `matched` 时返回图库卡图 ID；`rejected` 时为 `null`。ID 通常带 `_200w` 后缀。 |
| `score` | top-1 视觉相似度。 |
| `margin` | top-1 与 top-2 的相似度差。 |
| `top2_id`、`top2_score` | top-2 候选。若 top-1 分数未达到阈值，拒绝结果中两者为 `null`。 |
| `warnings` | 图片质量或预处理提示；为空不代表识别绝对正确。 |
| `preprocessing` | 预处理诊断信息，仅供排查与观测，不应作为稳定业务契约依赖。 |

## 5. 视觉候选检索

### `POST /v1/search`

返回视觉检索的前 5 个候选，不执行阈值拒绝。适用于业务侧需要展示候选、人工复核，或自行制定确认策略的场景。

```bash
curl -sS -X POST 'http://172.31.12.82:8003/v1/search' \
  -F 'file=@/path/to/card.jpg;type=image/jpeg'
```

响应示例：

```json
{
  "status": "ok",
  "query_time_ms": 862.5,
  "results": [
    {
      "rank": 1,
      "card_id": "100503_200w",
      "score": 0.9123,
      "product_name": "Pikachu ex",
      "product": {"productId": 100503, "productName": "Pikachu ex"}
    }
  ],
  "preprocessed_image": "/9j/4AAQSkZJRgABAQ...",
  "warnings": [],
  "preprocessing": {"quad_found": true}
}
```

| 字段 | 说明 |
| --- | --- |
| `status` | 正常时为 `ok`。 |
| `query_time_ms` | 从接收图片到检索完成的服务端耗时，单位毫秒。 |
| `results` | 最多 5 条，按 `score` 降序排列。 |
| `results[].rank` | 候选名次，从 1 开始。 |
| `results[].card_id` | 图库卡图 ID，可用于 `/v1/images/{card_id}`。 |
| `results[].score` | 视觉相似度。 |
| `results[].product_name` | 商品名称；商品元数据缺失时回退为 `card_id`。 |
| `results[].product` | 当前索引关联的原始商品 JSON；字段随数据源变化，调用方只应读取已与服务约定的字段。 |
| `preprocessed_image` | 实际用于视觉检索的 JPEG 图像 Base64 原文，**不含** `data:image/jpeg;base64,` 前缀。 |
| `warnings`、`preprocessing` | 含义同 `/v1/match`。 |

## 6. OCR 文字识别

### `POST /v1/ocr`

对图片执行 OCR，返回完整识别文字、适合参与文本检索的高置信文字和坐标块。

```bash
curl -sS -X POST 'http://172.31.12.82:8003/v1/ocr' \
  -F 'file=@/path/to/card.jpg;type=image/jpeg'
```

响应示例：

```json
{
  "status": "ok",
  "ocr_time_ms": 381.6,
  "total_blocks": 2,
  "blocks": [
    {
      "text": "Pikachu ex",
      "confidence": 0.98,
      "bbox": [[10.0, 20.0], [120.0, 20.0], [120.0, 45.0], [10.0, 45.0]]
    }
  ],
  "full_text": "Pikachu ex\n025/165",
  "query_text": "Pikachu ex\n025/165",
  "preprocessed_image": "/9j/4AAQSkZJRgABAQ...",
  "warnings": [],
  "preprocessing": {"bbox_space": "preprocessed_image"}
}
```

| 字段 | 说明 |
| --- | --- |
| `ocr_time_ms` | OCR 服务端耗时，单位毫秒。 |
| `total_blocks` | OCR 文字块数量。 |
| `blocks[].text`、`blocks[].confidence` | 文字内容及 OCR 置信度。 |
| `blocks[].bbox` | 四点坐标；坐标系对应 `preprocessed_image`，不是上传原图。 |
| `full_text` | 所有 OCR 文字，按版面顺序以换行分隔。 |
| `query_text` | 通过置信度筛选后实际可用于 `/v1/ocr-match` 的文字；可能为空。 |
| `preprocessed_image` | OCR 实际使用的 JPEG 图像 Base64 原文，不含 data URL 前缀。 |

## 7. OCR 文本候选检索

### `POST /v1/ocr-match`

该接口先 OCR，再将高置信文字进行 BGE 文本检索，返回前 5 个商品候选。它不使用视觉检索结果，也不根据分数自动确认单一卡牌。

```bash
curl -sS -X POST 'http://172.31.12.82:8003/v1/ocr-match' \
  -F 'file=@/path/to/card.jpg;type=image/jpeg'
```

响应示例：

```json
{
  "status": "ok",
  "full_text": "Pikachu ex\n025/165",
  "query_text": "Pikachu ex\n025/165",
  "query_time_ms": 612.4,
  "preprocessed_image": "/9j/4AAQSkZJRgABAQ...",
  "warnings": [],
  "results": [
    {
      "rank": 1,
      "product_id": "100503",
      "product_name": "Pikachu ex",
      "set_name": "Scarlet & Violet—151",
      "number": "025/165",
      "rarity": "Double Rare",
      "score": 0.8912,
      "has_image": true,
      "product": {"productId": 100503, "productName": "Pikachu ex"}
    }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `query_time_ms` | 包含 OCR 与文本检索的服务端总耗时，单位毫秒。 |
| `full_text`、`query_text` | 含义同 `/v1/ocr`。`query_text` 为空时，`results` 为空数组。 |
| `results` | 最多 5 条，按文本相似度降序排列。 |
| `results[].product_id` | 商品 ID；与视觉接口的 `card_id` 不同，不带 `_200w` 后缀。 |
| `results[].set_name`、`number`、`rarity` | 商品元数据字段；元数据缺失时返回空字符串。 |
| `results[].has_image` | 该商品是否存在本地图库缩略图。 |
| `results[].product` | 当前索引关联的原始商品 JSON。 |

## 8. 图库缩略图

### `GET /v1/images/{card_id}`

可按视觉检索返回的 `card_id` 获取 JPEG 缩略图：

```bash
curl -o card.jpg 'http://172.31.12.82:8003/v1/images/100503_200w'
```

`card_id` 可以带或不带 `.jpg` 后缀。为避免路径穿越，值不得包含 `..`、`/` 或 `\\`。图片不存在时返回 HTTP 404。

## 9. 错误处理与调用建议

错误响应为 FastAPI 标准 JSON，例如：

```json
{"detail": "Only image files are supported"}
```

| 情形 | HTTP 状态码 | 调用方处理 |
| --- | --- | --- |
| 缺少必填 `file` 字段或字段格式不正确 | 422 | 修正 `multipart/form-data` 请求。 |
| 空文件、超过 10 MiB、非图片 MIME 类型、图片无法解码 | 400 | 提示调用方或用户更换有效图片。 |
| 视觉模型或索引未就绪 | 503 | 按退避策略重试，并检查 `/v1/health`。 |
| 图库图片 ID 非法 | 400 | 不要拼接或透传未经校验的 ID。 |
| 图库图片不存在 | 404 | 不展示该缩略图或改用其他候选。 |
| `POST /v1/match` 返回 `status: "rejected"` | 200 | 这是正常业务结果；可提示重拍，或继续调用 `/v1/search`、`/v1/ocr-match` 获取候选。 |

推荐调用顺序：需要自动确认时先调用 `/v1/match`；若返回 `rejected`，再按业务需要调用 `/v1/search` 获取视觉候选，或调用 `/v1/ocr-match` 获取文字候选。不要把 `score` 当作绝对置信度，也不要仅凭低分候选自动写入业务数据。
