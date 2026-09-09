# TCG Recognize 内部 Dify 编排实施计划

> **执行说明：** 本计划按 `superpowers:executing-plans` 的任务粒度编写；每项均先补测试、再实现、再执行指定验证。

**目标：** 在不新增对外端点、不暴露 `intent` 的前提下，使 `POST /v2/recognize/serial` 与 `POST /v2/recognize/fusion` 支持图片文件、HTTPS URL、白名单本地路径，以及内部 Dify 分类和补全；返回新的 `text`、`priceTrend`、`monitor` 契约。

**架构：** 请求适配层将 `image` 统一为受校验的图片字节；编排器先调用同一 Dify 工作流的 `intent=classify`，再运行 serial 或 fusion 检索。检索命中商品后以 PG 字段逐字段填充，缺失字段才由 `intent=recognize_enrich` 的 Dify 输出补齐。成交曲线完全来自 PG 的 `purchasePrice/orderDate`；没有合格成交记录时整段使用 LLM 生成曲线，禁止拼接两种来源。

**技术栈：** FastAPI、Pydantic、psycopg、PostgreSQL、requests/httpx、pytest、PyYAML（仅工作流格式验证）。

**相关设计：** [后端接口契约](tcg-recognition-backend-api.md)、[服务技术设计](tcg-match-service-design.md)。

## 全局约束

- 外部 API 不接受或返回 `intent`；它仅是内部 Dify 工作流变量。
- 旧顶层业务 `status` 删除；截图中的五种状态只放 `monitor.status_match`。
- `text.state` 是卡牌/IP 判定，不是数据库命中状态；分类工作流不可用必须返回 HTTP 503，业务拒绝返回 HTTP 200。
- 外部类别显示值支持八种卡牌 IP；兼容现有内部代码（如 `pokemon`）但响应统一显示值。
- `marketValuationAvg` 只取命中商品有效的 `raw_json.marketPrice`，没有才允许 Dify 生成估值。
- PG 成交曲线仅取有限非负的 `purchasePrice` 和可解析的 `orderDate`；不使用运费、`lowestPrice`、`lowestPriceWithShipping` 或 JustTCG。
- `prices` 文件存在时 manifest 必须声明 `price_currency`；未声明币种的成交数据不导入为可用趋势。
- URL 下载只允许 HTTPS，拒绝内网/回环/链路本地解析结果、重定向到禁用地址、超限内容和非图片 MIME；本地路径必须位于配置白名单根目录。
- 修改外部 Dify YAML 时严格最小改动，完成后必须验证 YAML 语法和 Dify DSL 根对象、nodes、edges 引用完整性。外部 YAML 不加入本仓库 Git。

## 任务 1：定义新的响应模型、类别映射与合并规则

**文件：**

- 修改：`tcg-service/tcg-match-service/app/models/schemas.py`
- 新增：`tcg-service/tcg-match-service/app/matching/response_builder.py`
- 新增：`tcg-service/tcg-match-service/app/matching/categories.py`
- 新增：`tcg-service/tcg-match-service/tests/test_recognize_response_builder.py`
- 修改：`tcg-service/tcg-match-service/tests/test_api_contract.py`

**第 1 步：先写失败测试。** 覆盖：

```python
def test_pg_fields_win_and_only_missing_fields_use_llm() -> None:
    result = build_response(
        matched_product=product(marketPrice=5.6, setName="ME: Ascended Heroes", number="248/217"),
        enrichment={"seriesName": "wrong", "language": "English", "marketValuationAvg": 9.9},
    )
    assert result.text.series_name == "ME: Ascended Heroes"
    assert result.text.card_number == "248/217"
    assert result.text.language == "English"
    assert result.text.market_valuation_avg == 5.6
    assert result.monitor.field_sources["seriesName"] == "pg"
    assert result.monitor.field_sources["language"] == "llm"


def test_recognized_without_db_is_not_top_level_status() -> None:
    result = build_response(matched_product=None, classification=valid_pokemon())
    body = result.model_dump(by_alias=True)
    assert "status" not in body
    assert body["text"]["state"] is True
    assert body["monitor"]["status_match"] == "recognized_no_db"
```

**第 2 步：实现最小模型和 builder。**

- 创建显示类别与内部代码的双向映射，唯一接受：Pokémon、Pokémon Japan、Magic、Yu-Gi-Oh!、One Piece、Disney Lorcana、Flesh and Blood、Dragon Ball Super: Masters；同时接受历史小写代码作为兼容输入。
- 使用 Pydantic 别名输出规定的 camelCase 字段，包括 `text`、`priceTrend`、`monitor`。
- `monitor` 固定包含：`visual_rank`、`visual_score`、`text_rank`、`text_score`、`fusion_score`、`margin`、`dataSource`、`confidence`、`strategy`、`ocr_used`、`text_retrieval_used`、`input_text_confidence`、`candidate_count`、`status_match`、`price_source`、`field_sources`、`llm_enrich_status`、`warnings`、`request_id`、`dataset_version`、`model_version`、`workflow_version`、`decision_version`、`latency_ms`、`timings_ms`。
- `dataSource` 只描述身份命中证据：`visual`、`visual_ocr`、`visual_text`、`visual_ocr_text`、`text`、`ocr_text`、`llm_confirmed`、`none`；仅因分类或补字段调用 LLM 时不得标为 `llm_confirmed`。
- PG 覆盖 LLM 的字段严格为：`setName`→`seriesName`、`productName`（移除精确结尾 ` - {number}`）→`cardName`、`customAttributes.number`→`cardNumber`、`customAttributes.releaseDate`→`year`、`rarityName`/`customAttributes.rarityDbName`→`rarity`、`marketPrice`→`marketValuationAvg`、唯一命中 `productId`→`productId`。其余缺失值才可使用 LLM。

**第 3 步：运行验证。**

```powershell
python -m pytest tcg-service/tcg-match-service/tests/test_recognize_response_builder.py tcg-service/tcg-match-service/tests/test_api_contract.py -q
```

## 任务 2：扩展 Dify 客户端为同工作流双 intent 调用

**文件：**

- 修改：`tcg-service/tcg-match-service/app/config.py`
- 修改：`tcg-service/tcg-match-service/app/services/dify_service.py`
- 修改：`tcg-service/tcg-match-service/app/bootstrap.py`
- 修改：`tcg-service/tcg-match-service/tests/test_dify_service.py`

**第 1 步：先写失败测试。**

```python
def test_classify_sends_internal_intent_and_parses_business_rejection(requests_mock) -> None:
    service = configured_service(requests_mock)
    output = service.classify(image_bytes=b"image", mime_type="image/jpeg")
    assert output.state is False
    assert output.is_sports_card is True
    assert workflow_payload(requests_mock)["inputs"]["intent"] == "classify"


def test_enrich_accepts_json_string_output_and_sends_context(requests_mock) -> None:
    output = configured_service(requests_mock).recognize_enrich(
        image_bytes=b"image", mime_type="image/jpeg", candidates=[{"productId": 676060}]
    )
    assert output.price_trend[0].price.extracted == 2.29
    assert workflow_payload(requests_mock)["inputs"]["intent"] == "recognize_enrich"


def test_transport_failure_raises_classification_unavailable(requests_mock) -> None:
    with pytest.raises(ClassificationUnavailable):
        configured_service(requests_mock).classify(b"image", "image/jpeg")
```

**第 2 步：实现最小客户端。**

- 增加 `DIFY_TIMEOUT_SECONDS`、`DIFY_WORKFLOW_VERSION` 配置；无 base URL/key 时保留 unavailable 实现。
- 明确定义 `ClassificationOutput`、`EnrichmentOutput`、`GeneratedPricePoint`、`ClassificationUnavailable`。分类仅接收四个判定字段；补全接收候选、OCR 文本、类别、`field_sources` 和价格缺口。
- 每次调用上传图片后请求同一 `workflows/run`，分别传 `inputs.intent="classify"` 和 `inputs.intent="recognize_enrich"`。工作流输出既支持 JSON 字符串，也支持对象；格式不合法或网络超时按 unavailable 处理。
- `UnavailableDifyService.classify` 与 `.recognize_enrich` 均可预测地抛出各自可处理的 unavailable 异常；绝不让旧 `card_number/set_code` 解析继续决定新流程。

**第 3 步：运行验证。**

```powershell
python -m pytest tcg-service/tcg-match-service/tests/test_dify_service.py -q
```

## 任务 3：导入并查询 PG 纯成交价

**文件：**

- 修改：`tcg-service/tcg-match-service/db/migrations/002_release_schema.sql`
- 新增：`tcg-service/tcg-match-service/db/migrations/003_price_sales.sql`
- 修改：`tcg-service/tcg-match-service/app/importing/manifest.py`
- 修改：`tcg-service/tcg-match-service/app/importing/prices.py`
- 修改：`tcg-service/tcg-match-service/app/importing/pg_release.py`
- 修改：`tcg-service/tcg-match-service/app/repositories/catalog.py`
- 修改：`tcg-service/tcg-match-service/app/repositories/pg_catalog.py`
- 修改：`tcg-service/tcg-match-service/tests/test_price_import.py`
- 修改：`tcg-service/tcg-match-service/tests/test_repository_contract.py`
- 修改：`tcg-service/tcg-match-service/tests/integration/test_pg_schema.py`

**第 1 步：先写失败测试。**

```python
def test_import_sales_retains_duplicate_dates_and_excludes_shipping() -> None:
    rows = parse_sales(source_payload, currency="USD")
    assert [(row.purchase_price, row.order_date) for row in rows] == [
        (2.29, date(2026, 8, 10)), (2.29, date(2026, 8, 11)), (2.29, date(2026, 8, 12))
    ]
    assert not hasattr(rows[0], "shipping_price")


def test_price_file_requires_manifest_currency() -> None:
    with pytest.raises(ManifestError, match="price_currency"):
        validate_manifest({"prices": "sales.json"})


def test_repository_returns_purchase_price_and_order_date_only(pg_catalog) -> None:
    assert pg_catalog.get_sales(676060) == [
        {"purchasePrice": 2.29, "orderDate": "2026-08-10", "currency": "USD"}
    ]
```

**第 2 步：实现最小存储链路。**

- manifest 的可选 `prices` 条目和必填伴随 `price_currency` 指向含 `sales[]` 的 JSON/JSONL 数据；对用户提供格式读取 `purchasePrice` 和 `orderDate`，保留同日重复记录。
- 新表 `price_sales` 以 release/category/product/日期/导入行序号为唯一键，保存 `purchase_price`、`order_date`、`currency`、原始 JSON。`002` 为新 schema 创建表，`003` 对已有 release schema 使用幂等 SQL 补表和索引。
- 在发布导入事务中写入成交记录；仓储协议新增 `get_sales(product_id)`，按 `order_date ASC, import_sequence ASC` 返回纯成交字段。
- `price_snapshots` 仍保留给已有功能，但新 recognize 不再读取它。

**第 3 步：运行验证。**

```powershell
python -m pytest tcg-service/tcg-match-service/tests/test_price_import.py tcg-service/tcg-match-service/tests/test_repository_contract.py tcg-service/tcg-match-service/tests/integration/test_pg_schema.py -q
```

## 任务 4：改造 serial/fusion 编排顺序与来源决策

**文件：**

- 修改：`tcg-service/tcg-match-service/app/matching/orchestrator.py`
- 修改：`tcg-service/tcg-match-service/tests/test_serial_strategy.py`
- 修改：`tcg-service/tcg-match-service/tests/test_fusion_strategy.py`
- 新增：`tcg-service/tcg-match-service/tests/test_recognize_orchestration.py`

**第 1 步：先写失败测试。**

```python
def test_serial_classifies_before_visual_search(orchestrator, dify, visual) -> None:
    orchestrator.run_serial(request(image=b"image"))
    assert dify.events == ["classify"]
    assert visual.events == ["search"]


def test_not_a_card_short_circuits_retrieval(orchestrator, dify, visual) -> None:
    dify.classification = ClassificationOutput(state=False, is_sports_card=True)
    result = orchestrator.run_fusion(request(image=b"image"))
    assert result.status_match == "not_a_card"
    assert visual.events == []


def test_no_pg_sales_uses_whole_llm_curve_and_marks_warning(orchestrator, catalog, dify) -> None:
    catalog.sales = []
    result = orchestrator.run_serial(request(image=b"image"))
    assert result.price_trend_source == "llm_generated"
    assert result.warnings == ["PRICE_TREND_LLM_GENERATED"]
    assert len(result.price_trend) == len(dify.enrichment.price_trend)
```

**第 2 步：实现最小编排。**

- 扩展内部 `RecognitionRequest` 支持外部文本、类别、置信度及经适配器提供的图片 bytes/mime；保留 DINO/BGE 的现有策略细节。
- 入口先 `classify`：服务不可用映射给上层 503；`state=false` 或 sports 卡立即返回 `not_a_card`，不检索；分类正常的 `cardIp` 映射成检索类别，调用方显式类别冲突时按分类结果处理并加入 `CATEGORY_OVERRIDDEN_BY_CLASSIFY` 警告。
- 命中后读取商品和 `get_sales`。有合格销售记录则 `price_source="pg_sales"`；没有时调用 `recognize_enrich` 获取完整 LLM 曲线，设 `price_source="llm_generated"` 并加唯一警告。命中库商品也调用补全，但 builder 保证 PG 不被覆盖。
- 有身份但无库记录时以 `recognized_no_db` 返回；候选不确定为 `candidates`；无身份为 `unrecognized`；高置信直出、视觉+OCR、视觉+文本、文本、LLM 确认正确归类 `dataSource`。
- serial 与 fusion 均复用该前后置流程，保留自身检索差异和 `strategy` 字段；记录各阶段计时和 workflow 版本。

**第 3 步：运行验证。**

```powershell
python -m pytest tcg-service/tcg-match-service/tests/test_serial_strategy.py tcg-service/tcg-match-service/tests/test_fusion_strategy.py tcg-service/tcg-match-service/tests/test_recognize_orchestration.py -q
```

## 任务 5：实现对外 image 适配和新 HTTP 响应

**文件：**

- 修改：`tcg-service/tcg-match-service/app/main.py`
- 新增：`tcg-service/tcg-match-service/app/services/image_input.py`
- 修改：`tcg-service/tcg-match-service/app/config.py`
- 修改：`tcg-service/tcg-match-service/tests/test_api_contract.py`
- 新增：`tcg-service/tcg-match-service/tests/test_image_input.py`

**第 1 步：先写失败测试。**

```python
def test_serial_accepts_multipart_image_and_returns_new_shape(client) -> None:
    response = client.post("/v2/recognize/serial", files={"image": ("card.jpg", b"jpg", "image/jpeg")})
    assert response.status_code == 200
    assert set(response.json()) == {"text", "priceTrend", "monitor"}


def test_remote_private_address_is_rejected_before_download(httpx_mock) -> None:
    with pytest.raises(ImageInputError, match="private"):
        resolve_image_url("https://127.0.0.1/card.jpg", settings())


def test_classification_unavailable_becomes_503(client) -> None:
    response = client.post("/v2/recognize/serial", files={"image": ("card.jpg", b"jpg", "image/jpeg")})
    assert response.status_code == 503
```

**第 2 步：实现最小适配。**

- 两个端点保持原路径；请求 form 支持 `image` 作为上传文件、HTTPS URL 字符串或本地文件绝对路径。兼容历史上传字段 `file`，但当 `image` 与 `file` 同时给出时返回 422。
- 支持可选 `text`、`category`、`confidence`；`confidence` 必须为有限 0 到 1 浮点数。旧 `ocr_text` 仅作为 `text` 兼容别名。
- 设置新增 `IMAGE_LOCAL_ROOTS`、`IMAGE_URL_TIMEOUT_SECONDS`、`IMAGE_MAX_BYTES`；URL 使用显式 DNS/IP 检查和逐跳重定向校验，本地解析路径必须落在配置根内；验证图片 content type、字节上限与空内容。
- Dify 分类不可用由专用异常转换成 RFC 7807 风格 HTTP 503；任何正常业务结论均 HTTP 200，实体固定为 `{text, priceTrend, monitor}`。

**第 3 步：运行验证。**

```powershell
python -m pytest tcg-service/tcg-match-service/tests/test_api_contract.py tcg-service/tcg-match-service/tests/test_image_input.py -q
```

## 任务 6：最小修改 Dify YAML，并进行全量回归和工作流校验

**文件：**

- 修改：`D:\Code2026\Dify\BallStarCard\TCG-project\TCG-V3-20260818\【生产】IGBG-TCG卡-TCG卡识别-【V3-20260824】.yml`
- 修改：`tcg-service/tcg-match-service/requirements.txt`
- 新增：`tcg-service/tcg-match-service/tests/test_dify_workflow_contract.py`

**第 1 步：先写失败测试。**

```python
def test_workflow_has_intent_input_and_no_justtcg_fallback() -> None:
    workflow = yaml.safe_load(Path(os.environ["DIFY_WORKFLOW_PATH"]).read_text(encoding="utf-8"))
    start_node = next(node for node in workflow["workflow"]["graph"]["nodes"] if node["data"]["type"] == "start")
    names = {field["variable"] for field in start_node["data"]["variables"]}
    assert "intent" in names
    assert "justtcg" not in json.dumps(workflow).lower()
```

**第 2 步：修改工作流。**

- 在 start 节点增加内部字符串变量 `intent`，保持已有图片变量不变。
- 在现有工作流增加以 `intent` 为条件的两个分支：`classify` 只输出 `state`、`stateErrorReason`、`isSportsCard`、`cardIp`；`recognize_enrich` 接受后端上下文，输出可缺省的卡牌补全字段、LLM 估值和完整 LLM 价格曲线。
- 删除/断开 JustTCG 价格查询、TLS 回退与默认密钥路径；所有 PG 数据由后端读取，工作流只负责 LLM 兜底。
- 更新输出节点，使两个分支均返回可解析 JSON，且不改变与该需求无关的节点配置。

**第 3 步：验证 YAML 和 DSL。**

```powershell
python -c "import yaml; from pathlib import Path; p=Path(r'D:\Code2026\Dify\BallStarCard\TCG-project\TCG-V3-20260818\【生产】IGBG-TCG卡-TCG卡识别-【V3-20260824】.yml'); d=yaml.safe_load(p.read_text(encoding='utf-8')); g=d['workflow']['graph']; ids={n['id'] for n in g['nodes']}; assert ids; assert all(e['source'] in ids and e['target'] in ids for e in g['edges']); print('YAML and Dify DSL graph passed')"
$env:DIFY_WORKFLOW_PATH = 'D:\Code2026\Dify\BallStarCard\TCG-project\TCG-V3-20260818\【生产】IGBG-TCG卡-TCG卡识别-【V3-20260824】.yml'; python -m pytest tcg-service/tcg-match-service/tests/test_dify_workflow_contract.py -q
```

**第 4 步：全量验证与提交。**

```powershell
python -m pytest tcg-service/tcg-match-service/tests -q
git diff --check
git status --short
git add tcg-service/tcg-match-service/app tcg-service/tcg-match-service/db tcg-service/tcg-match-service/tests tcg-service/tcg-match-service/requirements.txt doc/tcg-recognition-dify-implementation-plan.md
git diff --cached --check
git commit -m "feat: integrate recognize with internal dify workflow"
```

外部 Dify YAML 位于仓库之外，交付前记录其 SHA-256 和验证结果，但不通过本仓库 `git add` 暂存。推送前仅在用户或运行环境明确允许时执行 `git push origin main`。

## 覆盖性复核

| 需求 | 对应任务 | 验收点 |
|---|---|---|
| 端点不变、intent 内部化 | 2、5 | 请求 payload 与 HTTP 契约测试 |
| 先分类、失败 503、拒绝 200 | 2、4、5 | 编排与 HTTP 测试 |
| PG 字段优先、LLM 仅补缺 | 1、4 | 字段来源断言 |
| purchasePrice/orderDate 优先 | 3、4 | 导入、查询、回退曲线测试 |
| 禁止 JustTCG 回退 | 4、6 | 运行时分支与 YAML 扫描 |
| 新 monitor/status_match | 1、4、5 | 响应 shape 与状态测试 |
| 图片文件、URL、本地白名单 | 5 | 输入与 SSRF 测试 |
| YAML/DSL 合法 | 6 | `safe_load`、图引用和工作流测试 |
