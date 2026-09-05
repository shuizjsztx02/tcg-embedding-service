# TCG 单机双策略识别服务实施计划

> **供执行人员使用：** 实施时必须使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`，逐项执行本计划；步骤使用复选框（`- [ ]`）跟踪状态。

**目标：** 将现有 FastAPI + FAISS demo 改造成 PostgreSQL/pgvector 单机服务，完整实现串行 OCR 文字向量补救 API 和并行融合 API，并用同一数据、规则与评测证明其准确率、延迟和资源差异。

**架构：** 一个 FastAPI 实例共享 DINOv2 ViT-B/14、BGE-small-en-v1.5、版本化 PostgreSQL/pgvector repository 和 Dify client。serial 执行视觉直通，否则 OCR 文本召回重排，再必要时 LLM；fusion 在 OCR 可用时并发执行两路召回并进行加权 RRF。原始数据按 manifest 导入不可变 dataset release，通过 active pointer 发布。

**技术栈：** Python 3.11、FastAPI、Pydantic、PyTorch CPU/CUDA、sentence-transformers、PostgreSQL、pgvector、psycopg 3、HTTPX、pytest、Docker Compose。

**技术方案：** `doc/tcg-match-service-design.md`

## 全局约束

- 生产默认 CPU-only、单服务器、单 API 实例和一个 Uvicorn worker；GPU 由显式配置切换相同业务代码。
- 正式数据约 36 万行，目录名不是接口；导入只依赖已校验的 `manifest.json` 相对路径。
- 图片必填；`ocr_text`、`ocr_lang`、`category` 可选；服务端不运行 OCR，也不先调用 LLM 判品类。
- DINO 固定 `dinov2_vitb14`、768 维；BGE 固定用户本地包、384 维。模型、预处理、文本模板均带指纹。
- serial 的低视觉置信请求在 OCR 可用时必须先做 BGE 召回和重排，再决定是否调用 Dify。
- fusion 在 OCR 可用时必须等待两路召回再决策，不因视觉高分提前结束。
- 指定品类只检索该品类；未指定品类做全库向量召回。
- RRF 用于排序，不当作概率；未校准 profile 时禁用自动 matched。
- 原始图片、JSONL、价格、向量、模型、缓存和生成报告不得提交 Git；提交前只暂存本任务源码、配置、测试和文档。
- 每项 Task 完成后运行所列验证、检查暂存区、独立 commit 并 push；若外部环境门槛未满足，停止在该 Task 的发布/联调步骤并保留已验证的本地成果。

---

## 文件职责

| 文件/目录 | 单一职责 |
|---|---|
| `tcg-match-service/app/config.py` | 解析并验证环境配置，不加载服务 |
| `tcg-match-service/app/domain/models.py` | 请求上下文、候选、证据、决策、数据版本类型 |
| `tcg-match-service/app/models/schemas.py` | HTTP 输入输出 schema |
| `tcg-match-service/app/services/model_gateway.py` | 本地优先的 DINO/BGE 加载和模型指纹 |
| `tcg-match-service/app/services/dino_service.py` | 共用图片变换、单/批视觉编码 |
| `tcg-match-service/app/services/text_service.py` | 共用文档模板、OCR 查询编码及适用性判断 |
| `tcg-match-service/app/repositories/catalog.py` | repository Protocol |
| `tcg-match-service/app/repositories/pg_catalog.py` | 固定 release 的 PG 查询、向量召回、身份/价格查表 |
| `tcg-match-service/app/matching/identity.py` | OCR/LLM 身份抽取、规范化、冲突判断 |
| `tcg-match-service/app/matching/fusion.py` | 候选合并、加权 RRF、稳定排序 |
| `tcg-match-service/app/matching/decision.py` | 版本化接受门限和结果判定 |
| `tcg-match-service/app/matching/orchestrator.py` | serial/fusion 两种调度，不实现模型细节 |
| `tcg-match-service/app/services/dify_service.py` | Dify 文件上传、workflow 执行和输出校验 |
| `tcg-match-service/app/routes/recognize.py` | 三个识别路由、校验、HTTP 状态映射 |
| `tcg-match-service/app/routes/catalog.py` | categories、price、ready 路由 |
| `tcg-match-service/db/migrations/*.sql` | public 控制表和 release schema 模板 |
| `tcg-match-service/script_temp/import_data.py` | discover/validate/stage/encode/index/verify/publish CLI |
| `tcg-match-service/script_temp/evaluate_strategies.py` | paired 离线对比和门限校准 |
| `tcg-match-service/script_temp/benchmark_cpu.py` | CPU 并发、延迟、CPU/RSS 压测 |
| `tcg-match-service/tests/` | 不依赖真实模型/数据的单元和集成测试；真实依赖测试显式标记 |

依赖方向：routes → orchestrator → model services/repository/decision/Dify；importer 可复用 model services 和 DB schema，但不能反向依赖 routes。测试以 fake repository/model/Dify 替换外部依赖。

---

### 任务 1： 冻结契约、配置和可测试服务生命周期

**文件：**
- 修改： `tcg-match-service/app/config.py`
- 修改： `tcg-match-service/app/models/schemas.py`
- 新建： `tcg-match-service/app/domain/__init__.py`
- 新建： `tcg-match-service/app/domain/models.py`
- 修改： `tcg-match-service/app/main.py`
- 新建： `tcg-match-service/tests/test_config.py`
- 新建： `tcg-match-service/tests/test_api_contract.py`
- 修改： `tcg-match-service/.env.example`

**接口：**
- 输出： immutable `Settings`, `DatasetRef`, `SearchScope`, `Candidate`, `Evidence`, `Decision`; app lifespan factory accepting fake dependencies in tests.
- 输出： shared multipart fields and response metadata for all recognize endpoints.

- [ ] **步骤 1： Add failing configuration tests**

```python
def test_cpu_is_default_and_model_download_is_opt_in(monkeypatch):
    monkeypatch.delenv("DEVICE", raising=False)
    monkeypatch.delenv("ALLOW_MODEL_DOWNLOAD", raising=False)
    s = Settings.from_env()
    assert s.device == "cpu"
    assert s.allow_model_download is False

def test_cuda_configuration_fails_when_runtime_has_no_cuda(monkeypatch):
    monkeypatch.setenv("DEVICE", "cuda")
    with pytest.raises(ConfigError, match="CUDA requested"):
        Settings.from_env(cuda_available=lambda: False)
```

- [ ] **步骤 2： Add failing API contract tests**

```python
@pytest.mark.parametrize("path", [
    "/v2/recognize", "/v2/recognize/serial", "/v2/recognize/fusion"
])
def test_recognize_contract_accepts_optional_client_ocr(client, jpeg_bytes, path):
    r = client.post(path, files={"file": ("card.jpg", jpeg_bytes, "image/jpeg")},
                    data={"ocr_text": "Pikachu 025/165", "category": "pokemon"})
    assert r.status_code == 200
    body = r.json()
    assert {"strategy", "dataset_version", "model_version", "decision_version"} <= body.keys()
```

还需测试：10 MiB+1 返回 413、非法图片返回 400、未知品类返回 400、category/category_hint 冲突返回 400、缺少图片返回 422、全空白 OCR 不执行文本检索。

- [ ] **步骤 3： Run focused tests and observe failure**

运行： `cd tcg-match-service && pytest tests/test_config.py tests/test_api_contract.py -q`

预期结果：由于新的领域类型或路由不存在，测试收集或导入失败。

- [ ] **步骤 4： Implement typed configuration and contracts**

```python
@dataclass(frozen=True)
class SearchScope:
    dataset: DatasetRef
    category: str | None

@dataclass(frozen=True)
class Candidate:
    category: str
    product_id: str
    visual_rank: int | None = None
    visual_score: float | None = None
    text_rank: int | None = None
    text_score: float | None = None
    fusion_score: float | None = None
```

解析 `DATABASE_URL`、`DEVICE`、模型路径与后端、Dify 配置、连接池/队列上限、K、超时和决策配置路径。对象显示和日志必须隐去密钥。将 Pydantic 可变默认值替换为 `Field(default_factory=...)`。使用 FastAPI lifespan 和显式依赖容器；`/v1/health` 只表示进程存活。

- [ ] **步骤 5： Run the focused test set**

运行： `cd tcg-match-service && pytest tests/test_config.py tests/test_api_contract.py -q`

预期结果：使用替身依赖、不访问网络、模型或数据库时全部通过。

- [ ] **步骤 6： Commit and push 任务 1**

```powershell
git add tcg-match-service/app/config.py tcg-match-service/app/models/schemas.py tcg-match-service/app/domain tcg-match-service/app/main.py tcg-match-service/tests/test_config.py tcg-match-service/tests/test_api_contract.py tcg-match-service/.env.example
git diff --cached --check
git diff --cached --stat
git commit -m "feat: freeze TCG matching API and runtime contracts"
git push origin main
```

---

### 任务 2： 建立 PostgreSQL/pgvector release schema

**文件：**
- 新建： `tcg-match-service/db/migrations/001_control_schema.sql`
- 新建： `tcg-match-service/db/migrations/002_release_schema.sql`
- 新建： `tcg-match-service/app/repositories/__init__.py`
- 新建： `tcg-match-service/app/repositories/catalog.py`
- 新建： `tcg-match-service/app/repositories/pg_catalog.py`
- 新建： `tcg-match-service/tests/integration/test_pg_schema.py`
- 新建： `tcg-match-service/tests/test_repository_contract.py`

**接口：**
- 输入： `DatasetRef`, `SearchScope`, `Candidate` from 任务 1.
- 输出： `CatalogRepository.pin_active_release()`, `search_visual()`, `search_text()`, `lookup_identity()`, `get_card()`, `get_prices()`.

- [ ] **步骤 1： Write repository contract tests against a fake**

```python
class CatalogRepository(Protocol):
    def pin_active_release(self) -> DatasetRef: ...
    def list_categories(self, dataset: DatasetRef) -> list[CategoryInfo]: ...
    def search_visual(self, scope: SearchScope, vector: NDArray, k: int) -> list[Candidate]: ...
    def search_text(self, scope: SearchScope, vector: NDArray, k: int) -> list[Candidate]: ...
    def lookup_identity(self, scope: SearchScope, identity: Identity, limit: int) -> list[Candidate]: ...
```

断言每个候选都包含 category 和规范化 product_id；品类范围不会泄漏；没有活动版本时抛出 RepositoryNotReady；同一请求内不重新计算已固定的 schema。

- [ ] **步骤 2： Write PG integration tests**

在临时 release schema 中创建两个品类和一组已知的三维测试向量。断言品类检索只返回该品类；全局检索返回真正的跨品类最近邻；品类检索的 `EXPLAIN` 包含分区裁剪/索引扫描；切换版本不影响已经固定的 `DatasetRef`。

- [ ] **步骤 3： Run tests and observe failure**

运行： `cd tcg-match-service && pytest tests/test_repository_contract.py -q`

预期结果：由于 repository 模块尚不存在而失败。只有设置 `TEST_DATABASE_URL` 时才执行数据库集成测试。

- [ ] **步骤 4： Add control and release DDL**

DDL 必须启用 vector 扩展、创建控制表，并按技术方案生成每个版本的业务表。迁移接口接收服务端生成的 UUID，并安全引用 schema 名称。核心向量 DDL：

```sql
CREATE TABLE visual_embeddings (
  category_id bigint NOT NULL,
  product_id bigint NOT NULL,
  embedding vector(768) NOT NULL,
  model_version text NOT NULL,
  input_hash text NOT NULL,
  PRIMARY KEY (category_id, product_id)
) PARTITION BY LIST (category_id);
```

各品类的数据加载完成后，才为其创建分区和 HNSW 余弦索引。文本使用 vector(384)。为 cards 增加身份索引和外键校验。版本状态为 PREPARING、VERIFIED、ACTIVE、RETIRED、FAILED；只有 VERIFIED 状态可以发布。

- [ ] **步骤 5： Implement PG repository with safe release pinning**

内部 schema 标识符使用 psycopg SQL 组合，所有值均使用绑定参数。每个事务内设置 `SET LOCAL hnsw.ef_search` 和 statement timeout。全局检索查询分区父表，品类检索增加 category 条件。ANN 返回少于 K 条时，在同一范围执行精确检索，并返回发生回退的诊断信息。

- [ ] **步骤 6： Run unit and database integration tests**

运行： `cd tcg-match-service && pytest tests/test_repository_contract.py -q`

使用测试 PG 运行：`cd tcg-match-service && pytest tests/integration/test_pg_schema.py -q`

预期结果：两组测试都通过；仅在缺少本地测试数据库变量时允许跳过集成测试，并必须报告跳过事实。

- [ ] **步骤 7： Commit and push 任务 2**

只暂存任务 2 的文件，检查 `git diff --cached`，提交信息使用 `feat: add versioned pgvector catalog`，然后推送 main。

---

### 任务 3： 统一本地优先模型加载、预处理与文本模板

**文件：**
- 新建： `tcg-match-service/app/services/model_gateway.py`
- 修改： `tcg-match-service/app/services/dino_service.py`
- 修改： `tcg-match-service/app/services/text_service.py`
- 新建： `tcg-match-service/tests/test_model_gateway.py`
- 新建： `tcg-match-service/tests/test_dino_service.py`
- 新建： `tcg-match-service/tests/test_text_service.py`
- 修改： `tcg-match-service/scripts/build_index.py` (mark legacy; delegate transforms to shared code during transition)

**接口：**
- 输入： 任务 1 Settings.
- 输出： `ModelBundle`, `DINOv2Service.embed()/embed_batch()`, `TextService.build_document()/is_query_eligible()/encode_query()/encode_documents()` and deterministic fingerprints.

- [ ] **步骤 1： Write local loading and backend adapter tests**

```python
def test_present_but_invalid_local_model_does_not_fall_back_to_network(tmp_path, fake_hub):
    (tmp_path / "weights.pth").write_bytes(b"broken")
    with pytest.raises(ModelIntegrityError):
        load_dino(local_dir=tmp_path, allow_download=True, hub=fake_hub)
    assert fake_hub.calls == []

@pytest.mark.parametrize("output", [torch.ones(1, 768), FakeHFOutput(torch.ones(1, 5, 768))])
def test_backend_outputs_become_normalized_cls(output):
    v = extract_cls(output)
    assert v.shape == (1, 768)
    np.testing.assert_allclose(np.linalg.norm(v, axis=1), 1.0)
```

还需测试：本地模型缺失且禁用下载时失败；本地模型缺失且允许下载时只调用一次固定版本加载器；模型文件哈希影响指纹；维度错误时失败；查询不会误用文档编码路径。

- [ ] **步骤 2： Write deterministic preprocessing/text tests**

使用生成的 RGB 图片验证：相同像素的 gallery/query tensor 完全一致；`(W,H)=(168,224)`；横图策略显式可见；截断或动画图片被拒绝；批处理中一张图片失败时，其他项目 ID 仍保持对齐。测试 `100009.0 → "100009"`、字段顺序稳定、移除 HTML、英语查询前缀、8,192 字符输入上限、非英语适用性，以及关键身份字段排在可能被截断的描述之前。

- [ ] **步骤 3： Run tests and observe failures**

运行： `cd tcg-match-service && pytest tests/test_model_gateway.py tests/test_dino_service.py tests/test_text_service.py -q`

预期结果：由于网关和共用转换函数不存在而失败。

- [ ] **步骤 4： Implement explicit DINO backends and BGE bundle**

支持 `DINO_BACKEND=torch_hub|huggingface`；本地源码+权重或 HF 目录必须完整。优先加载本地模型。只有本地路径不存在且 `ALLOW_MODEL_DOWNLOAD=true` 时才访问网络，并把固定 revision 写入指纹。Torch tensor 直接映射，HF 输出取 `last_hidden_state[:,0]`。强制校验 eval/no_grad、设备、维度、float32 和 L2 归一化。

从 `BGE_MODEL_PATH` 加载一次 BGE，校验 manifest、pooling、最大序列长度和维度；导入器和 API 复用同一对象。索引脚本中不得在线调用 `SentenceTransformer("BAAI/...")`。

- [ ] **步骤 5： Implement shared transforms and model package smoke command**

对外提供：

```python
def preprocess_dino(image: Image.Image, policy: OrientationPolicy) -> torch.Tensor: ...
def build_document(card: Mapping[str, Any], category_code: str) -> str: ...
def is_query_eligible(text: str | None, lang: str | None) -> Eligibility: ...
```

`python -m app.services.model_gateway verify` loads both local models, encodes one generated image/text, prints fingerprints/dimensions and performs no request after loading.

- [ ] **步骤 6： Run tests and local model smoke test**

运行： `cd tcg-match-service && pytest tests/test_model_gateway.py tests/test_dino_service.py tests/test_text_service.py -q`

挂载模型后运行：`cd tcg-match-service && python -m app.services.model_gateway verify`

预期结果：分别得到 768 维和 384 维归一化向量；本地模型包完整时，在禁止网络的环境中成功运行。

- [ ] **步骤 7： Commit and push 任务 3**

只暂存列出的源码、测试和最小旧脚本委托改动。使用 `feat: unify local-first embedding models` 提交，然后推送。

---

### 任务 4： 实现 manifest 驱动、可恢复的数据与价格导入

**文件：**
- 新建： `tcg-match-service/app/importing/__init__.py`
- 新建： `tcg-match-service/app/importing/manifest.py`
- 新建： `tcg-match-service/app/importing/pipeline.py`
- 新建： `tcg-match-service/app/importing/prices.py`
- 新建： `tcg-match-service/script_temp/import_data.py`
- 新建： `tcg-match-service/tests/test_manifest.py`
- 新建： `tcg-match-service/tests/test_import_pipeline.py`
- 新建： `tcg-match-service/tests/test_price_import.py`

**接口：**
- 输入： Tasks 2 repository schema and 任务 3 model services.
- 输出： `discover`, `validate`, `prepare`, `encode`, `build-index`, `verify`, `publish`, `status`, `rollback` commands and `ImportReport` JSON.

- [ ] **步骤 1： Write manifest and path-security tests**

生成改过名称的临时品类目录。断言发现阶段只提出产品/图片路径，不擅自确定稳定品类身份；通过校验的 manifest 只能解析到数据根目录的子路径；`../`、符号链接越界、重复 category code/source ID、非整数 product ID 和主图歧义均在写数据库前失败。

- [ ] **步骤 2： Write idempotence, resume and reuse tests**

```python
def test_low_price_only_release_reuses_embeddings(importer, old_release, price_manifest):
    new = importer.prepare(price_manifest, base_release=old_release)
    importer.run_to_verified(new)
    assert importer.dino.calls == 0
    assert importer.bge.calls == 0
    assert new.visual_count == old_release.visual_count

def test_source_hash_change_invalidates_checkpoint(importer, changed_source):
    with pytest.raises(SourceChangedError):
        importer.resume(changed_source)
```

还需断言：记录和 checkpoint 在同一事务提交；损坏图片进入隔离清单且不写零向量；replace 范围只删除明确声明的品类；失败版本不修改活动指针；发布已验证版本时原子更新指针。

- [ ] **步骤 3： Write price snapshot tests**

使用很小的内联 JSONL，断言数组中的重复行按 row_no 保持独立；同一来源批次重复导入具有幂等性；`count < totalResults` 的不完整数据不能替换正式曲线窗口；完整替换只修改声明的窗口；价格按 UTC 日期/currency/condition/variant/language 聚合，缺失币种时不填默认值。

- [ ] **步骤 4： Run tests and observe failure**

运行： `cd tcg-match-service && pytest tests/test_manifest.py tests/test_import_pipeline.py tests/test_price_import.py -q`

预期结果：由于 importing 包和 CLI 不存在而失败。

- [ ] **步骤 5： Implement streaming import pipeline**

每次读取一行 JSONL 和一个有界图片批次；使用 Decimal 校验 ID，并用 COPY/批量写入。保存 sha256 和模板哈希。只有输入哈希、模型指纹、转换/模板版本全部一致时才复用向量。每条命令中每个模型只加载一次。持久化隔离详情和精确计数，但不保存原始密钥。

- [ ] **步骤 6： Implement CLI and dry-run report**

```powershell
python script_temp/import_data.py discover --data-root D:\incoming\release --output D:\incoming\manifest.draft.json
python script_temp/import_data.py validate --manifest D:\incoming\manifest.json --report D:\incoming\validation.json
python script_temp/import_data.py prepare --manifest D:\incoming\manifest.json --mode replace --scope magic,pokemon
python script_temp/import_data.py status --release-id <printed-release-id>
```

命令打印生成的 release ID；运维人员将该精确值传给后续 `encode/build-index/verify/publish` 命令。`publish` 拒绝发布非 VERIFIED 状态的版本。`rollback --to-release <id>` 只能指向仍被保留的 VERIFIED/RETIRED 版本。

- [ ] **步骤 7： Run tests and a 1,000-card sample rehearsal**

先运行上述单元测试，再对生成或批准的 1,000 张卡样例执行所有阶段。验证数据库计数、哈希复用、自匹配、隔离报告、HNSW 对比精确检索的 Recall@50、发布、重启和回滚。生成报告保存到已忽略的 `/data/imports/<release-id>/`。

- [ ] **步骤 8： Commit and push 任务 4**

只提交源码和测试，提交信息使用 `feat: add resumable versioned data importer`；确认没有暂存 JSONL、图片、向量、模型或报告，然后推送。

---

### 任务 5： 实现身份证据、候选合并、RRF 和版本化决策器

**文件：**
- 新建： `tcg-match-service/app/matching/__init__.py`
- 新建： `tcg-match-service/app/matching/identity.py`
- 新建： `tcg-match-service/app/matching/fusion.py`
- 新建： `tcg-match-service/app/matching/decision.py`
- 新建： `tcg-match-service/tests/test_identity.py`
- 新建： `tcg-match-service/tests/test_fusion.py`
- 新建： `tcg-match-service/tests/test_decision.py`
- 新建： `tcg-match-service/config/decision_profile.example.json`

**接口：**
- 输入： 任务 1 domain models.
- 输出： `extract_identity()`, `merge_rankings()`, `rank_rrf()`, `DecisionEngine.decide()`.

- [ ] **步骤 1： Write identity tests before implementation**

断言 NFKC/大小写/空白规范化会保留斜杠和有效前缀；`12/100 != 12100`；HP/年份不是确定卡号；系列+卡号可以构成强身份；只有名称时不能自动匹配；没有版本证据时，同图多 ID 组仍为候选；畸形 OCR 不得导致异常。

- [ ] **步骤 2： Write RRF tests**

```python
def test_rrf_merges_by_category_and_product_id():
    got = rank_rrf(visual=[c("pokemon","42",1,.91)],
                   text=[c("magic","42",1,.88), c("pokemon","42",2,.80)],
                   visual_weight=.7, text_weight=.3, c=60)
    assert [(x.category, x.product_id) for x in got] == [("pokemon","42"),("magic","42")]
```

断言缺失模态贡献为零且剩余权重重新归一化；原始分数保留；允许只有文本证据的候选；同分顺序稳定；RRF 分数绝不复制到 confidence。

- [ ] **步骤 3： Write decision tests**

测试以下情况：无 profile 时不能 matched；视觉高分+足够差值+无冲突时 matched；OCR 冲突阻止直接接受；只有通过校准门槛时，联合证据才能纠正视觉 top1；单候选结果的差值未知；重复组保持 candidates；两个身份字段唯一且满足最低视觉支持时可以匹配；模型/数据/profile 指纹不一致时禁用接受。

- [ ] **步骤 4： Run tests and observe failures**

运行： `cd tcg-match-service && pytest tests/test_identity.py tests/test_fusion.py tests/test_decision.py -q`

- [ ] **步骤 5： Implement pure matching functions**

这些模块不执行 I/O。RRF 公式严格为 `sum(normalized_weight/(c+rank))`，rank 从 1 开始。`DecisionProfile.load()` 校验 schema、指纹和适用范围。`Decision` 枚举 MATCHED、CANDIDATES、NEED_LLM、UNRECOGNIZED，并包含规则 ID 和审计证据。

- [ ] **步骤 6： Run focused property/table tests**

运行上述测试文件。增加参数化测试，覆盖缺失模态、相同分数、拒绝 NaN、拒绝负权重，并通过 100 种随机输入排列证明输出顺序稳定。

- [ ] **步骤 7： Commit and push 任务 5**

使用 `feat: add calibrated multimodal ranking rules` 提交并推送。

---

### 任务 6： 接入 Dify GPT-5.5 工作流并严格查表

**文件：**
- 替换： `tcg-match-service/app/services/llm_service.py` with compatibility import or removal
- 新建： `tcg-match-service/app/services/dify_service.py`
- 新建： `tcg-match-service/tests/test_dify_service.py`
- 新建： `tcg-match-service/tests/test_llm_lookup.py`

**接口：**
- 输入： image bytes, OCR text, scope, candidate summaries and repository identity lookup.
- 输出： `DifyService.recognize(context) -> FallbackIdentity | FallbackFailure`.

- [ ] **步骤 1： Write HTTP contract tests with a mock transport**

断言 `/files/upload` 先于 `/workflows/run`；两次调用使用同一个请求级匿名 user；上传 ID 作为本地文件输入传递；Bearer 密钥不出现在日志或错误中；只解析 succeeded 输出；401、429、5xx、超时、非法 JSON 和 schema 不匹配分别返回有类型的失败；blocking 调用不自动重试。

- [ ] **步骤 2： Write anti-hallucination lookup tests**

断言 Dify 选择的 ID 不在候选或范围内时被拒绝；未知品类被拒绝；唯一系列+卡号并满足最低视觉支持时可匹配；只有名称时返回候选；识别到但库中不存在时返回 recognized_no_db；Dify 失败时返回已有向量候选并附 warning。

- [ ] **步骤 3： Run tests and observe failure**

运行： `cd tcg-match-service && pytest tests/test_dify_service.py tests/test_llm_lookup.py -q`

- [ ] **步骤 4： Implement Dify client and output validator**

使用共享 HTTPX 客户端。把 multipart 图片和 user POST 到 `{DIFY_BASE_URL}/files/upload`；再把 inputs、blocking 模式和同一个 user POST 到 `{DIFY_BASE_URL}/workflows/run`。仅在显式就绪检查或诊断时从 `/parameters` 映射实际工作流变量名，不得每次请求都查询。校验文档定义的结果 schema，并限制候选 JSON 和输入大小。

- [ ] **步骤 5： Add a real-workflow opt-in smoke test**

只在设置 `DIFY_LIVE_TEST=1`、测试 API key 和获准的非敏感图片时运行。验证已发布工作流暴露所需的图片/OCR/候选输入；运维检查中配置的 Dify 节点显示 GPT-5.5；输出通过校验；一次有界请求完成。不得提交响应、图片或密钥。

- [ ] **步骤 6： Run focused tests and commit**

运行测试，只暂存源码和测试，使用 `feat: integrate Dify card fallback` 提交并推送。

---

### 任务 7： 完成 serial 的 OCR 文字向量补救链路

**文件：**
- 新建： `tcg-match-service/app/matching/orchestrator.py`
- 修改： `tcg-match-service/app/routes/recognize.py`
- 新建： `tcg-match-service/tests/test_serial_strategy.py`
- 修改： `tcg-match-service/tests/test_api_contract.py`

**接口：**
- 输入： DINO/BGE, CatalogRepository, DecisionEngine, identity functions and DifyService.
- 输出： `RecognitionOrchestrator.run_serial(context) -> RecognizeResult`.

- [ ] **步骤 1： Write the regression test for the currently missing behavior**

```python
def test_serial_low_visual_runs_text_before_llm(harness):
    harness.dino.result = [candidate("pokemon", "1", visual=.70)]
    harness.text.result = [candidate("pokemon", "2", text=.93)]
    harness.decision.results = [Decision.need_text(), Decision.matched("pokemon", "2")]

    result = harness.orchestrator.run_serial(request(ocr_text="Pikachu 025/165"))

    assert result.product_id == "2"
    assert harness.calls == ["dino.embed", "repo.visual", "bge.query", "repo.text"]
    assert harness.dify.calls == 0
```

该测试专门证明：视觉置信度低时，不会再绕过文字向量匹配而直接调用 LLM。

- [ ] **步骤 2： Cover every serial branch**

增加以下测试：视觉高置信时跳过 BGE/Dify；视觉高置信但存在强 OCR 冲突时继续文本检索；视觉低置信+OCR 可用时先做文本检索并可完成匹配；文本重排后仍不确定时才调用 Dify；视觉低置信+OCR 为空或不适用时跳过 BGE 并按需调用 Dify；文本失败时保留视觉候选后调用 Dify；限定范围不越界；全局请求检索全部品类；无 profile 时不自动匹配；向量数据库/DINO 失败时返回服务错误。

- [ ] **步骤 3： Run tests and observe the regression fail**

运行： `cd tcg-match-service && pytest tests/test_serial_strategy.py tests/test_api_contract.py -q`

预期结果：当前代码在核心回归测试中记录为视觉召回后立即调用 Dify，因此测试失败。

- [ ] **步骤 4： Implement serial orchestration**

```python
visual = visual_retriever.search(ctx)
first = decision.decide(ctx, visual=visual)
if first.is_final:
    return hydrate(first)
if text_service.is_query_eligible(ctx.ocr_text, ctx.ocr_lang):
    text = text_retriever.search(ctx)
    ranked = merge_and_rank(visual, text, ctx)
    second = decision.decide(ctx, visual=visual, text=text, ranked=ranked)
    if second.is_final:
        return hydrate(second)
return fallback_then_lookup(ctx, visual, text if executed else [])
```

请求开始时只固定一次数据版本。保证所有调用使用同一范围。只有做出决策后才补全产品和价格。记录真实的 `ocr_used`、`text_retrieval_used`、调用顺序和阶段耗时。

- [ ] **步骤 5： Bind serial and compatibility routes**

`/v2/recognize/serial` and `/v2/recognize` both call `run_serial`; the latter does not select strategy from headers/query strings. Retire category-classification calls. Keep old endpoint fields where compatible and return new metadata.

- [ ] **步骤 6： Run serial unit/API tests**

运行： `cd tcg-match-service && pytest tests/test_serial_strategy.py tests/test_api_contract.py -q`

预期结果：在不使用真实模型、数据库和 Dify 的情况下，调用顺序回归测试及全部分支通过。

- [ ] **步骤 7： Commit and push 任务 7**

使用 `feat: add OCR text recovery before LLM fallback` 提交并推送。该提交是本次“LLM 前增加 OCR 文字向量补救”要求的独立可审查交付。

---

### 任务 8： 完成 fusion 并行融合 API 和有界 CPU 调度

**文件：**
- 修改： `tcg-match-service/app/matching/orchestrator.py`
- 新建： `tcg-match-service/app/services/work_scheduler.py`
- 修改： `tcg-match-service/app/routes/recognize.py`
- 新建： `tcg-match-service/tests/test_fusion_strategy.py`
- 新建： `tcg-match-service/tests/test_work_scheduler.py`

**接口：**
- 输出： `RecognitionOrchestrator.run_fusion()` and `WorkScheduler` with queue/model semaphores and stage timing.

- [ ] **步骤 1： Write paired strategy behavior tests**

断言可用 OCR 会在消费任一结果前启动视觉和文本任务；fusion 等待两路完成；视觉高分但文本指向正确结果的分歧进入共同决策，不提前返回视觉结果；无 OCR 时与 serial 的候选和决策相同；文本失败时降级为视觉；DINO 失败仍返回 503；两路都不确定时只调用一次 Dify；两条路由返回不同 strategy 但 schema 一致。

- [ ] **步骤 2： Write scheduler resource tests**

使用事件/屏障而不是 sleep 计时，证明最大请求和模型并发限制；队列超时在未启动任务时拒绝请求；任务超时后保持信号量，直到 worker 实际停止；取消请求不会释放仍在运行的模型作业；每次 PG 操作获得自己的连接；模型替身阻塞时 ASGI 仍能响应 health。

- [ ] **步骤 3： Run tests and observe failure**

运行： `cd tcg-match-service && pytest tests/test_fusion_strategy.py tests/test_work_scheduler.py -q`

- [ ] **步骤 4： Implement fusion scheduling**

在异步边界将 DINO 和满足适用条件的 BGE 并发提交给有界执行器。每个任务包含编码和相应 repository 查询，使连接归属于执行它的 worker。等待两路完成后执行合并和 RRF，再使用与 serial 相同的决策/Dify/结果补全路径。路由函数中不得复制匹配规则。

- [ ] **步骤 5： Implement overload/error semantics**

队列已满映射为 HTTP 503 和 Retry-After。文本失败时标记降级并继续；视觉失败时终止请求。Dify 使用剩余的 deadline。lifespan 关闭时关闭 worker、client 和连接池，并在有限时间内等待，不以不安全方式终止线程。

- [ ] **步骤 6： Run focused and combined strategy tests**

运行： `cd tcg-match-service && pytest tests/test_serial_strategy.py tests/test_fusion_strategy.py tests/test_work_scheduler.py tests/test_api_contract.py -q`

- [ ] **步骤 7： Commit and push 任务 8**

使用 `feat: add bounded parallel fusion matching` 提交并推送。

---

### 任务 9： 完成 Docker、就绪检查、价格和运维接口

**文件：**
- 修改： `tcg-match-service/Dockerfile`
- 修改： `tcg-match-service/Dockerfile.gpu`
- 修改： `tcg-match-service/docker-compose.yml`
- 新建： `tcg-match-service/docker-compose.gpu.yml`
- 修改： `tcg-match-service/entrypoint.sh`
- 修改： `tcg-match-service/requirements.txt`
- 新建： `tcg-match-service/app/routes/catalog.py`
- 修改： `tcg-match-service/app/main.py`
- 新建： `tcg-match-service/tests/test_readiness.py`
- 新建： `tcg-match-service/tests/test_prices_api.py`
- 修改： `tcg-match-service/README.md`
- 修改： `tcg-match-service/OPERATION_GUIDE.md`

**接口：**
- 输出： deployable CPU image, optional GPU override, PostgreSQL service, readiness/categories/prices APIs and runbook.

- [ ] **步骤 1： Write readiness and price endpoint tests**

断言 health 不执行数据库、模型或 Dify 操作；模型、数据库、活动版本和有效 profile 齐备前 ready 失败，并单独报告可选 Dify 的降级状态；categories 返回向量数量；价格曲线保留系列维度、日期顺序和币种；非法范围被拒绝；缺失卡返回 404；无价格数据时返回 200、空序列及覆盖信息。

- [ ] **步骤 2： Update dependencies and container startup**

固定兼容的主/次版本范围，CPU 镜像使用 CPU PyTorch 安装源。增加 psycopg/pgvector/httpx，移除 Paddle/OCR 依赖。入口脚本先执行迁移再启动服务，绝不自动构建 36 万条索引。增加显式导入 profile/命令。在可写挂载允许的情况下使用非 root 用户运行服务。

- [ ] **步骤 3： Add Postgres/pgvector and durable volumes**

使用固定的 `pgvector/pgvector:pg16` 镜像标签，并在实施时解析到测试过的 patch/digest。PGDATA 存在命名卷；原始数据以 `/data:ro` 挂载，模型以 `/models:ro` 挂载，模型缓存和导入报告使用独立可写挂载。API 等待数据库健康和活动版本就绪，不使用固定 sleep。不得内置默认生产密码；`.env.example` 只包含变量名和安全的本地示例。

- [ ] **步骤 4： Implement routes and wire lifespan**

注册 recognize 和 catalog 路由。启动时对照活动数据和决策 profile 校验模型指纹。为支持导入操作，API 可以在未就绪状态启动；就绪前 recognize 返回 503。配置 Dify 后，就绪诊断只在运维命令或启动时调用 `/parameters`，且不生成内容。

- [ ] **步骤 5： Run automated and container checks**

```powershell
cd tcg-match-service
pytest -q
docker compose config -q
docker compose build tcg-match
docker compose up -d postgres tcg-match
docker compose ps
```

验证 `/v1/health` 返回 200；`/v1/ready` 报告正确状态；迁移具有幂等性；重启保留活动版本；进程只有一个 worker；镜像不包含 Paddle 包；本地模型完整时，阻断模型网络访问仍能启动服务。

- [ ] **步骤 6： Update runbooks with exact operator workflows**

记录首次安装、模型上传校验、manifest/导入阶段、版本发布/回滚、CPU/GPU 选择、数据库备份/恢复、数据/版本保留、两个 API 的 curl 示例、Dify 降级行为、日志/指标字段和故障排查。命令必须与已实现 CLI 的 `--help` 输出一致。

- [ ] **步骤 7： Commit and push 任务 9**

只暂存配置、源码、测试和文档；运行 `git diff --cached --check`；确认 `git ls-files` 不包含数据或模型产物；使用 `feat: package pgvector matching service` 提交并推送。

---

### 任务 10： 校准、serial/fusion 公平评测与 CPU 验收

**文件：**
- 新建： `tcg-match-service/script_temp/evaluate_strategies.py`
- 新建： `tcg-match-service/script_temp/benchmark_cpu.py`
- 新建： `tcg-match-service/tests/test_evaluator.py`
- 新建： `tcg-match-service/tests/test_benchmark_report.py`
- 新建： `doc/tcg-match-service-evaluation-template.md`

**接口：**
- 输入： immutable labeled evaluation manifest, both APIs or in-process orchestrators, active release/model/Dify versions.
- 输出： ignored JSON/CSV raw results, versioned decision profile candidate, Markdown comparison report.

- [ ] **步骤 1： Define and test evaluation manifest validation**

要求 sample_id 唯一，并提供图片相对路径/哈希、预期 category/product/等价组、in_db/is_card、ocr_text/lang 和 split/group_id。拒绝 calibration/held-out 组重叠、缺失标签、路径越界和文件哈希变化。

- [ ] **步骤 2： Test metric calculations on a hand-computed fixture**

对手工可计算样例验证 Top-1、Recall@5、MRR、自动接受精度/覆盖率、错误接受、纠错、损伤、配对 McNemar 计数和延迟分位数。全部请求都拒绝的样例覆盖率必须为零，不能通过验收。报告分子、分母和 bootstrap 置信区间，不能只给百分比。

- [ ] **步骤 3： Implement exact-vs-HNSW retrieval audit**

按比例从每个品类取样，并设置每品类最低样本数。在相同向量下，将 ANN Top-50 与 pgvector/FAISS 精确结果比较；报告全局、宏平均、最差品类 Recall@50、少于 K 条的发生率和查询计划。之后在报告中固定 HNSW 参数。

- [ ] **步骤 4： Implement two-phase strategy experiment**

A 阶段固定同一个决策 profile，测量调度和可用证据。B 阶段只在 calibration 集上网格搜索 serial/fusion profile：RRF 视觉权重 `{0.5,0.6,0.7,0.8,0.9}`、召回 K `{20,50,100}` 以及根据观测分数确定的分数/差值门限，并满足自动接受精度 ≥95% 和错误接受约束。选择覆盖率最高的配置，再在 held-out 集上评估一次；不得用 held-out 集调参。

- [ ] **步骤 5： Implement LLM control and paired outputs**

支持 `--llm-mode live|record|replay|off`。缓存键包含图片/OCR/范围/候选 payload/工作流版本哈希。配对结果列出 serial 正确而 fusion 错误，以及相反情况，并附分数和耗时。真实延迟报告使用 live 且不回放，并把包含 LLM 和不包含 LLM 的结果分开。

- [ ] **步骤 6： Implement CPU benchmark**

预热模型和 PG，然后分别在并发 1、2 下测量 serial/fusion、OCR/无 OCR、指定品类/全局、排除 LLM/包含 LLM。报告 p50/p95/p99、吞吐、排队时间、进程和 PG RSS、每请求 CPU 秒、失败/降级数量以及 BGE/Dify 调用率。数据、模型或 profile 版本漂移时终止测试。

- [ ] **步骤 7： Run script unit tests**

运行： `cd tcg-match-service && pytest tests/test_evaluator.py tests/test_benchmark_report.py -q`

预期结果：全部手工可计算指标和报告 schema 校验通过。

- [ ] **步骤 8： Execute staged evaluation gates**

1. Generated/approved 1,000-card import rehearsal.
2. Labeled demo set regression.
3. Formal real-photo calibration/held-out set after user supplies labels.
4. Target CPU server full benchmark after user supplies machine access/spec.

每个门槛的原始输出保存到已忽略的 `/data/evaluations/<run-id>/`；只有不包含数据产物或密钥时，才在 `doc/` 保存 Markdown 报告。`decision_profile.json` 写入运行时配置存储；只有数据集/模型标识不敏感且稳定时，才提交已净化的 profile。

- [ ] **步骤 9： Commit and push 任务 10**

使用 `test: add paired serial fusion evaluation` 提交脚本、测试、模板和获准的净化报告/配置；确认未暂存原始数据、Dify 响应和凭据，然后推送。

---

### 任务 11： 全量导入、发布和回滚演练

**文件：**
- Modify after evidence: `doc/tcg-match-service-evaluation-template.md` into a dated deployment report
- No source change is accepted silently during this task; discovered bugs return to the owning Task with tests.

**接口：**
- 输入： official raw package + manifest, model packages, target Postgres, Dify configuration, accepted decision profile.
- 输出： active verified release and signed-off operational evidence.

- [ ] **步骤 1： Record immutable input inventory**

记录原始 source_version/文件哈希、品类、产品/图片/价格数量、模型/后端/文件指纹、代码 commit、迁移版本、profile 版本、Dify 已发布工作流/版本标记和目标 CPU/RAM/磁盘；不保存 API key。

- [ ] **步骤 2： Validate the formal raw package**

运行 discover，在 manifest 中人工绑定稳定 category code，然后运行 validate。检查重复项、缺失/损坏图片、非法 ID、未知币种和不完整价格窗口。遇到无法解释的失败时停止发布；保留报告并显式修复数据源或 manifest。

- [ ] **步骤 3： Import to a new release with checkpoints**

使用打印出的准确 release ID 运行 prepare → encode → build-index → verify。在安全测试点中断一次并恢复，以证明断点能力。观察模型只加载一次、内存受限、模型加载没有线上 API 流量，并在满足条件时复用未变化向量。

- [ ] **步骤 4： Verify database and retrieval integrity**

比较有效产品数与数据源、卡牌图片/向量覆盖与隔离记录，并校验外键、维度/范数、身份查表、价格覆盖、HNSW 对比精确召回和抽样自匹配。运行 `ANALYZE`，记录索引/表大小和 EXPLAIN 计划。

- [ ] **步骤 5： Publish, smoke test and rollback**

发布 VERIFIED 版本，使用指定品类/全局以及 OCR/无 OCR 样例调用两个 API 并检查价格；然后回滚到上一版本并验证请求元数据变化。只有回滚成功后才重新发布新版本。已在处理中的请求必须保持其固定版本。

- [ ] **步骤 6： Run target-host paired and resource acceptance**

执行任务 10 的评测和压测。确认 serial 在视觉低置信时先使用 OCR 文本再调用 LLM；fusion 等待全部可用模态；范围泄漏为零；明确报告自动接受精度/覆盖率和延迟；Dify 不可用时返回向量候选。

- [ ] **步骤 7： Final documentation commit and push**

用实际证据和剩余限制完成带日期的报告。只暂存报告、运维手册和配置改动，检查已跟踪文件中是否包含数据，使用 `docs: record TCG matching deployment acceptance` 提交并推送。只有验收报告包含实际执行结果而非计划值时，才能标记实施完成。

---

## Execution order and review gates

```text
任务 1：接口契约
  → 任务 2 DB schema/repository ─┐
  → 任务 3 model consistency ───┼→ 任务 4 importer
  → 任务 5 matching rules ──────┼→ 任务 7 serial OCR recovery
  → 任务 6 Dify fallback ───────┘        ↓
                                  任务 8 fusion/concurrency
                                           ↓
                                  任务 9 Docker/operations
                                           ↓
                                  任务 10 evaluation
                                           ↓
                                  任务 11 formal release
```

任务 2 的 PG 集成测试、任务 3 的真实本地模型 smoke、任务 4 的采样导入可以在对应依赖齐备时并行准备，但同一 git 工作区按 Task 顺序提交，避免交叉暂存。任务 7 是 serial 可验收里程碑，任务 8 不得通过复制一套规则绕过共用决策器。

## 完成标准

- 两个独立策略 API 和兼容 serial 别名使用同一版本、repository、模型、决策及 Dify 查表逻辑。
- 自动测试实际证明低视觉+可用 OCR 的 serial 调用顺序为 DINO → BGE/文字召回 → 决策 → 必要时 Dify。
- fusion 有 OCR 时双路并发，无 OCR 与 serial 语义一致，并发受界、降级可观测。
- 正式数据包可校验、断点导入、版本发布、回滚；36 万物理行的有效/重复/缺图统计来自报告。
- CPU 镜像完全离线加载已上传模型，DINO/BGE 的在线与离线处理一致；GPU override 通过 smoke test 后可用。
- pgvector 的品类/全局检索经过 exact 对照；价格查询保留来源、币种、窗口和系列维度。
- 真实照片 held-out 报告同时给出精度、覆盖率、纠错/损伤、错误接受和资源/延迟；95% 目标有明确分母，未达标时如实保留 serial/fusion 实验结果。
- Git 历史只包含源码、配置、测试和文档；数据、图片、模型、向量、缓存、密钥和原始评测输出均未被跟踪。
