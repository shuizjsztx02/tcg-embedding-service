# TCG 单机双策略识别服务 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 FastAPI + FAISS demo 改造成 PostgreSQL/pgvector 单机服务，完整实现串行 OCR 文字向量补救 API 和并行融合 API，并用同一数据、规则与评测证明其准确率、延迟和资源差异。

**Architecture:** 一个 FastAPI 实例共享 DINOv2 ViT-B/14、BGE-small-en-v1.5、版本化 PostgreSQL/pgvector repository 和 Dify client。serial 执行视觉直通，否则 OCR 文本召回重排，再必要时 LLM；fusion 在 OCR 可用时并发执行两路召回并进行加权 RRF。原始数据按 manifest 导入不可变 dataset release，通过 active pointer 发布。

**Tech Stack:** Python 3.11、FastAPI、Pydantic、PyTorch CPU/CUDA、sentence-transformers、PostgreSQL、pgvector、psycopg 3、HTTPX、pytest、Docker Compose。

**Spec:** `doc/tcg-match-service-design.md`

## Global Constraints

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

## File map

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

### Task 1: 冻结契约、配置和可测试服务生命周期

**Files:**
- Modify: `tcg-match-service/app/config.py`
- Modify: `tcg-match-service/app/models/schemas.py`
- Create: `tcg-match-service/app/domain/__init__.py`
- Create: `tcg-match-service/app/domain/models.py`
- Modify: `tcg-match-service/app/main.py`
- Create: `tcg-match-service/tests/test_config.py`
- Create: `tcg-match-service/tests/test_api_contract.py`
- Modify: `tcg-match-service/.env.example`

**Interfaces:**
- Produces: immutable `Settings`, `DatasetRef`, `SearchScope`, `Candidate`, `Evidence`, `Decision`; app lifespan factory accepting fake dependencies in tests.
- Produces: shared multipart fields and response metadata for all recognize endpoints.

- [ ] **Step 1: Add failing configuration tests**

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

- [ ] **Step 2: Add failing API contract tests**

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

Also test 10 MiB+1 → 413, invalid image → 400, unknown category → 400, conflicting category/category_hint → 400, missing file → 422, and whitespace OCR → no text route.

- [ ] **Step 3: Run focused tests and observe failure**

Run: `cd tcg-match-service && pytest tests/test_config.py tests/test_api_contract.py -q`

Expected: collection/import failure for the new domain types or missing routes.

- [ ] **Step 4: Implement typed configuration and contracts**

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

Parse `DATABASE_URL`, `DEVICE`, model paths/backends, Dify values, pool/queue limits, K, timeouts and decision profile path. Redact secrets from repr/logs. Replace deprecated mutable Pydantic defaults with `Field(default_factory=...)`. Use FastAPI lifespan and explicit dependency container; `/v1/health` remains process-liveness only.

- [ ] **Step 5: Run the focused test set**

Run: `cd tcg-match-service && pytest tests/test_config.py tests/test_api_contract.py -q`

Expected: all tests pass with fake dependencies and no network/model/database access.

- [ ] **Step 6: Commit and push Task 1**

```powershell
git add tcg-match-service/app/config.py tcg-match-service/app/models/schemas.py tcg-match-service/app/domain tcg-match-service/app/main.py tcg-match-service/tests/test_config.py tcg-match-service/tests/test_api_contract.py tcg-match-service/.env.example
git diff --cached --check
git diff --cached --stat
git commit -m "feat: freeze TCG matching API and runtime contracts"
git push origin main
```

---

### Task 2: 建立 PostgreSQL/pgvector release schema

**Files:**
- Create: `tcg-match-service/db/migrations/001_control_schema.sql`
- Create: `tcg-match-service/db/migrations/002_release_schema.sql`
- Create: `tcg-match-service/app/repositories/__init__.py`
- Create: `tcg-match-service/app/repositories/catalog.py`
- Create: `tcg-match-service/app/repositories/pg_catalog.py`
- Create: `tcg-match-service/tests/integration/test_pg_schema.py`
- Create: `tcg-match-service/tests/test_repository_contract.py`

**Interfaces:**
- Consumes: `DatasetRef`, `SearchScope`, `Candidate` from Task 1.
- Produces: `CatalogRepository.pin_active_release()`, `search_visual()`, `search_text()`, `lookup_identity()`, `get_card()`, `get_prices()`.

- [ ] **Step 1: Write repository contract tests against a fake**

```python
class CatalogRepository(Protocol):
    def pin_active_release(self) -> DatasetRef: ...
    def list_categories(self, dataset: DatasetRef) -> list[CategoryInfo]: ...
    def search_visual(self, scope: SearchScope, vector: NDArray, k: int) -> list[Candidate]: ...
    def search_text(self, scope: SearchScope, vector: NDArray, k: int) -> list[Candidate]: ...
    def lookup_identity(self, scope: SearchScope, identity: Identity, limit: int) -> list[Candidate]: ...
```

Assert every candidate has category+normalized product_id, category scope never leaks, no active release raises RepositoryNotReady, and the pinned schema is not recomputed within one request.

- [ ] **Step 2: Write PG integration tests**

Create two categories with a known set of 3-D test vectors in a temporary release schema. Assert category search stays in one category, global search returns the true cross-category nearest row, `EXPLAIN` for category search contains partition pruning/index scan, and release switching does not affect an already pinned `DatasetRef`.

- [ ] **Step 3: Run tests and observe failure**

Run: `cd tcg-match-service && pytest tests/test_repository_contract.py -q`

Expected: missing repository module. Integration tests are run only when `TEST_DATABASE_URL` is present.

- [ ] **Step 4: Add control and release DDL**

The DDL must enable vector, create control tables, and generate per-release tables from the design. The migration API receives a server-generated UUID and quotes schema names. Core vector DDL:

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

Create a partition and HNSW cosine index for each imported category only after its rows load. Text uses vector(384). Add cards identity indexes and FK validation. Control release states are PREPARING, VERIFIED, ACTIVE, RETIRED, FAILED; only VERIFIED can publish.

- [ ] **Step 5: Implement PG repository with safe release pinning**

Use psycopg SQL composition for internal schema identifiers; bind all values. Apply `SET LOCAL hnsw.ef_search` and statement timeout inside each transaction. Query the partitioned parent for global search and a category predicate for scoped search. Fewer than K ANN rows triggers exact search in the same scope; return diagnostics indicating fallback.

- [ ] **Step 6: Run unit and database integration tests**

Run: `cd tcg-match-service && pytest tests/test_repository_contract.py -q`

Run with test PG: `cd tcg-match-service && pytest tests/integration/test_pg_schema.py -q`

Expected: both pass; skip is acceptable only when the local database variable is absent and must be reported.

- [ ] **Step 7: Commit and push Task 2**

Stage only Task 2 files, inspect `git diff --cached`, commit `feat: add versioned pgvector catalog`, and push main.

---

### Task 3: 统一本地优先模型加载、预处理与文本模板

**Files:**
- Create: `tcg-match-service/app/services/model_gateway.py`
- Modify: `tcg-match-service/app/services/dino_service.py`
- Modify: `tcg-match-service/app/services/text_service.py`
- Create: `tcg-match-service/tests/test_model_gateway.py`
- Create: `tcg-match-service/tests/test_dino_service.py`
- Create: `tcg-match-service/tests/test_text_service.py`
- Modify: `tcg-match-service/scripts/build_index.py` (mark legacy; delegate transforms to shared code during transition)

**Interfaces:**
- Consumes: Task 1 Settings.
- Produces: `ModelBundle`, `DINOv2Service.embed()/embed_batch()`, `TextService.build_document()/is_query_eligible()/encode_query()/encode_documents()` and deterministic fingerprints.

- [ ] **Step 1: Write local loading and backend adapter tests**

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

Also test missing local+download disabled fails, missing local+download enabled invokes pinned loader once, model file hashes affect fingerprint, wrong dimensions fail, and a query never uses the document encoder path accidentally.

- [ ] **Step 2: Write deterministic preprocessing/text tests**

Use generated RGB images to verify gallery/query tensors are identical for identical pixels, `(W,H)=(168,224)`, landscape policy is explicit, truncated/animated images reject, and batch item IDs stay aligned when one image fails. Test `100009.0 → "100009"`, stable field order, HTML removal, English query prefix, 8,192-character input bound, non-English eligibility, and key identity fields precede truncated description.

- [ ] **Step 3: Run tests and observe failures**

Run: `cd tcg-match-service && pytest tests/test_model_gateway.py tests/test_dino_service.py tests/test_text_service.py -q`

Expected: missing gateway and shared transformation functions.

- [ ] **Step 4: Implement explicit DINO backends and BGE bundle**

Support `DINO_BACKEND=torch_hub|huggingface`; local source+weights or HF directory must be complete. Load local first. Network occurs only when local path is absent and `ALLOW_MODEL_DOWNLOAD=true`; pin revision into fingerprint. Map Torch tensor directly and HF output from `last_hidden_state[:,0]`. Enforce eval/no_grad, device, dimensions, float32 and L2 normalization.

Load BGE once from `BGE_MODEL_PATH`, validate manifest/pooling/max sequence/dimension, and use the same object for importer and API. Do not use online `SentenceTransformer("BAAI/...")` inside index scripts.

- [ ] **Step 5: Implement shared transforms and model package smoke command**

Expose:

```python
def preprocess_dino(image: Image.Image, policy: OrientationPolicy) -> torch.Tensor: ...
def build_document(card: Mapping[str, Any], category_code: str) -> str: ...
def is_query_eligible(text: str | None, lang: str | None) -> Eligibility: ...
```

`python -m app.services.model_gateway verify` loads both local models, encodes one generated image/text, prints fingerprints/dimensions and performs no request after loading.

- [ ] **Step 6: Run tests and local model smoke test**

Run: `cd tcg-match-service && pytest tests/test_model_gateway.py tests/test_dino_service.py tests/test_text_service.py -q`

Run with model mounts: `cd tcg-match-service && python -m app.services.model_gateway verify`

Expected: 768- and 384-dimensional normalized vectors; network denied mode succeeds with complete local packages.

- [ ] **Step 7: Commit and push Task 3**

Stage only listed source/tests and the minimal legacy delegation change. Commit `feat: unify local-first embedding models`, then push.

---

### Task 4: 实现 manifest 驱动、可恢复的数据与价格导入

**Files:**
- Create: `tcg-match-service/app/importing/__init__.py`
- Create: `tcg-match-service/app/importing/manifest.py`
- Create: `tcg-match-service/app/importing/pipeline.py`
- Create: `tcg-match-service/app/importing/prices.py`
- Create: `tcg-match-service/script_temp/import_data.py`
- Create: `tcg-match-service/tests/test_manifest.py`
- Create: `tcg-match-service/tests/test_import_pipeline.py`
- Create: `tcg-match-service/tests/test_price_import.py`

**Interfaces:**
- Consumes: Tasks 2 repository schema and Task 3 model services.
- Produces: `discover`, `validate`, `prepare`, `encode`, `build-index`, `verify`, `publish`, `status`, `rollback` commands and `ImportReport` JSON.

- [ ] **Step 1: Write manifest and path-security tests**

Generate temporary renamed category folders. Assert discovery proposes products/images without defining stable category identity; validated manifest resolves only children of data root; `../`, symlink escape, duplicate category code/source ID, non-integer product ID and ambiguous main images fail before DB writes.

- [ ] **Step 2: Write idempotence, resume and reuse tests**

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

Also assert a transaction commits records and checkpoint together, corrupt images are quarantined without zero vectors, replace scope deletes only declared categories, failed release never changes active pointer, and publishing a verified release is an atomic pointer update.

- [ ] **Step 3: Write price snapshot tests**

Using tiny inline JSONL, assert duplicate array rows remain distinct by row_no; reimport of same source batch is idempotent; incomplete `count < totalResults` cannot replace the formal curve window; complete replacement changes only declared window; prices aggregate by UTC date/currency/condition/variant/language and never default missing currency.

- [ ] **Step 4: Run tests and observe failure**

Run: `cd tcg-match-service && pytest tests/test_manifest.py tests/test_import_pipeline.py tests/test_price_import.py -q`

Expected: missing importing package/CLI.

- [ ] **Step 5: Implement streaming import pipeline**

Read one JSONL line and bounded image batch at a time; use Decimal ID validation and COPY/batched inserts. Store sha256 and template hash. Reuse vectors only when input hash, model fingerprint and transform/template version all match. Load each model once per command. Persist quarantine details and exact counts without raw secrets.

- [ ] **Step 6: Implement CLI and dry-run report**

```powershell
python script_temp/import_data.py discover --data-root D:\incoming\release --output D:\incoming\manifest.draft.json
python script_temp/import_data.py validate --manifest D:\incoming\manifest.json --report D:\incoming\validation.json
python script_temp/import_data.py prepare --manifest D:\incoming\manifest.json --mode replace --scope magic,pokemon
python script_temp/import_data.py status --release-id <printed-release-id>
```

The command prints the generated release ID; operators copy that exact value into subsequent `encode/build-index/verify/publish` commands. `publish` refuses any release not VERIFIED. `rollback --to-release <id>` only points to an existing retained VERIFIED/RETIRED version.

- [ ] **Step 7: Run tests and a 1,000-card sample rehearsal**

Run unit tests above, then execute all stages on a generated or approved 1,000-card sample. Verify DB counts, hash reuse, self-match, quarantine report, HNSW vs exact Recall@50, publish, restart and rollback. Save generated reports under ignored `/data/imports/<release-id>/`.

- [ ] **Step 8: Commit and push Task 4**

Commit source/tests only as `feat: add resumable versioned data importer`; verify no JSONL/image/vector/model/report is staged, then push.

---

### Task 5: 实现身份证据、候选合并、RRF 和版本化决策器

**Files:**
- Create: `tcg-match-service/app/matching/__init__.py`
- Create: `tcg-match-service/app/matching/identity.py`
- Create: `tcg-match-service/app/matching/fusion.py`
- Create: `tcg-match-service/app/matching/decision.py`
- Create: `tcg-match-service/tests/test_identity.py`
- Create: `tcg-match-service/tests/test_fusion.py`
- Create: `tcg-match-service/tests/test_decision.py`
- Create: `tcg-match-service/config/decision_profile.example.json`

**Interfaces:**
- Consumes: Task 1 domain models.
- Produces: `extract_identity()`, `merge_rankings()`, `rank_rrf()`, `DecisionEngine.decide()`.

- [ ] **Step 1: Write identity tests before implementation**

Assert NFKC/case/whitespace normalization preserves slash and meaningful prefix; `12/100 != 12100`; HP/year is not a hard card number; set+number can form strong identity; name-only cannot auto-match; identical-image multi-ID group stays candidates without version evidence; malformed OCR never raises.

- [ ] **Step 2: Write RRF tests**

```python
def test_rrf_merges_by_category_and_product_id():
    got = rank_rrf(visual=[c("pokemon","42",1,.91)],
                   text=[c("magic","42",1,.88), c("pokemon","42",2,.80)],
                   visual_weight=.7, text_weight=.3, c=60)
    assert [(x.category, x.product_id) for x in got] == [("pokemon","42"),("magic","42")]
```

Assert absent modality contributes zero then remaining weights renormalize, raw scores are retained, text-only candidate is possible, tie order is deterministic, and RRF is never copied into confidence.

- [ ] **Step 3: Write decision tests**

Test no profile → no matched; visual high+margin+no conflict → matched; OCR conflict blocks direct acceptance; joint evidence can correct visual top1 only when calibrated gates pass; one-card result has unknown margin; duplicate group remains candidates; identity unique by two fields and minimum visual support may match; model/data/profile fingerprint mismatch disables acceptance.

- [ ] **Step 4: Run tests and observe failures**

Run: `cd tcg-match-service && pytest tests/test_identity.py tests/test_fusion.py tests/test_decision.py -q`

- [ ] **Step 5: Implement pure matching functions**

Keep no I/O in these modules. RRF formula is exactly `sum(normalized_weight/(c+rank))`; use rank starting at 1. `DecisionProfile.load()` verifies schema, fingerprints and scope. `Decision` enumerates MATCHED, CANDIDATES, NEED_LLM, UNRECOGNIZED and includes rule IDs/evidence for audit.

- [ ] **Step 6: Run focused property/table tests**

Run the test file set above. Add parametrized tests across missing modalities, equal scores, NaN rejection, negative weight rejection and 100 random input permutations proving stable output.

- [ ] **Step 7: Commit and push Task 5**

Commit `feat: add calibrated multimodal ranking rules` and push.

---

### Task 6: 接入 Dify GPT-5.5 工作流并严格查表

**Files:**
- Replace: `tcg-match-service/app/services/llm_service.py` with compatibility import or removal
- Create: `tcg-match-service/app/services/dify_service.py`
- Create: `tcg-match-service/tests/test_dify_service.py`
- Create: `tcg-match-service/tests/test_llm_lookup.py`

**Interfaces:**
- Consumes: image bytes, OCR text, scope, candidate summaries and repository identity lookup.
- Produces: `DifyService.recognize(context) -> FallbackIdentity | FallbackFailure`.

- [ ] **Step 1: Write HTTP contract tests with a mock transport**

Assert `/files/upload` occurs before `/workflows/run`; both use the same per-request pseudonymous user; upload id is passed as a local file input; bearer key never appears in logs/errors; only succeeded output is parsed; 401/429/5xx/timeout/invalid JSON/schema mismatch each return typed failure; blocking calls are not automatically retried.

- [ ] **Step 2: Write anti-hallucination lookup tests**

Assert Dify-selected ID outside candidate/scope rejects; unknown category rejects; unique set+number+minimum visual support matches; name-only returns candidates; identified but absent card returns recognized_no_db; Dify failure returns existing vector candidates with warning.

- [ ] **Step 3: Run tests and observe failure**

Run: `cd tcg-match-service && pytest tests/test_dify_service.py tests/test_llm_lookup.py -q`

- [ ] **Step 4: Implement Dify client and output validator**

Use a shared HTTPX client. POST multipart image and user to `{DIFY_BASE_URL}/files/upload`; POST inputs, blocking mode and the same user to `{DIFY_BASE_URL}/workflows/run`. Map actual workflow variable names from `/parameters` during explicit readiness/diagnostic, never on every request. Validate the documented result schema and cap candidate JSON/input sizes.

- [ ] **Step 5: Add a real-workflow opt-in smoke test**

Run only with `DIFY_LIVE_TEST=1`, a test API key and an approved non-sensitive image. Verify the published workflow exposes required image/OCR/candidate inputs, the configured Dify node reports GPT-5.5 in operator inspection, output validates, and one bounded request completes. Do not commit the response image/key.

- [ ] **Step 6: Run focused tests and commit**

Run tests, stage only source/tests, commit `feat: integrate Dify card fallback`, and push.

---

### Task 7: 完成 serial 的 OCR 文字向量补救链路

**Files:**
- Create: `tcg-match-service/app/matching/orchestrator.py`
- Modify: `tcg-match-service/app/routes/recognize.py`
- Create: `tcg-match-service/tests/test_serial_strategy.py`
- Modify: `tcg-match-service/tests/test_api_contract.py`

**Interfaces:**
- Consumes: DINO/BGE, CatalogRepository, DecisionEngine, identity functions and DifyService.
- Produces: `RecognitionOrchestrator.run_serial(context) -> RecognizeResult`.

- [ ] **Step 1: Write the regression test for the currently missing behavior**

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

This test specifically proves low visual confidence no longer jumps directly to LLM.

- [ ] **Step 2: Cover every serial branch**

Add tests for: high visual skips BGE/Dify; high visual plus strong OCR conflict continues to text; low visual+eligible OCR runs text then can match; low visual+eligible OCR remains uncertain then calls Dify; low visual+empty/noneligible OCR skips BGE and may call Dify; text failure preserves visual candidates then uses Dify; scoped requests never escape; global requests search all; no profile never auto-matches; vector DB/DINO failure returns service error.

- [ ] **Step 3: Run tests and observe the regression fail**

Run: `cd tcg-match-service && pytest tests/test_serial_strategy.py tests/test_api_contract.py -q`

Expected: current code records Dify immediately after visual on the main regression test.

- [ ] **Step 4: Implement serial orchestration**

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

Pin the release once at request start. Ensure all calls use the same scope. Hydrate product/price only after a decision. Record actual `ocr_used`, `text_retrieval_used`, call order and stage timings.

- [ ] **Step 5: Bind serial and compatibility routes**

`/v2/recognize/serial` and `/v2/recognize` both call `run_serial`; the latter does not select strategy from headers/query strings. Retire category-classification calls. Keep old endpoint fields where compatible and return new metadata.

- [ ] **Step 6: Run serial unit/API tests**

Run: `cd tcg-match-service && pytest tests/test_serial_strategy.py tests/test_api_contract.py -q`

Expected: call-order regression and all branches pass without real models/DB/Dify.

- [ ] **Step 7: Commit and push Task 7**

Commit `feat: add OCR text recovery before LLM fallback` and push. This commit is the independently reviewable delivery of the user’s latest correction.

---

### Task 8: 完成 fusion 并行融合 API 和有界 CPU 调度

**Files:**
- Modify: `tcg-match-service/app/matching/orchestrator.py`
- Create: `tcg-match-service/app/services/work_scheduler.py`
- Modify: `tcg-match-service/app/routes/recognize.py`
- Create: `tcg-match-service/tests/test_fusion_strategy.py`
- Create: `tcg-match-service/tests/test_work_scheduler.py`

**Interfaces:**
- Produces: `RecognitionOrchestrator.run_fusion()` and `WorkScheduler` with queue/model semaphores and stage timing.

- [ ] **Step 1: Write paired strategy behavior tests**

Assert eligible OCR starts visual and text tasks before either result is consumed; fusion waits for both; visual-high/text-correct disagreement reaches common decision instead of early visual return; no OCR gives the same candidate/decision as serial; one text failure degrades to visual; DINO failure remains 503; both uncertain invoke Dify once; two routes return distinct strategy but identical schema.

- [ ] **Step 2: Write scheduler resource tests**

Use events/barriers, not sleep timing, to prove max request/model concurrency; queue timeout rejects without starting work; task timeout keeps semaphore until worker actually stops; cancellation does not release a live model job; each PG operation obtains its own connection; ASGI can serve health while model fake is blocked.

- [ ] **Step 3: Run tests and observe failure**

Run: `cd tcg-match-service && pytest tests/test_fusion_strategy.py tests/test_work_scheduler.py -q`

- [ ] **Step 4: Implement fusion scheduling**

In an async boundary submit DINO and, only when eligible, BGE to the bounded executor concurrently. Each task includes encoding plus corresponding repository query so the connection belongs to its worker. Await both, merge, RRF, then use the same decision/Dify/hydration path as serial. Do not duplicate match rules inside route functions.

- [ ] **Step 5: Implement overload/error semantics**

Map queue full → HTTP 503 + Retry-After. Text failure marks degradation and continues; visual failure fails request. Use remaining deadline for Dify. Close workers/clients/pool during lifespan shutdown and wait bounded time without killing a thread unsafely.

- [ ] **Step 6: Run focused and combined strategy tests**

Run: `cd tcg-match-service && pytest tests/test_serial_strategy.py tests/test_fusion_strategy.py tests/test_work_scheduler.py tests/test_api_contract.py -q`

- [ ] **Step 7: Commit and push Task 8**

Commit `feat: add bounded parallel fusion matching` and push.

---

### Task 9: 完成 Docker、就绪检查、价格和运维接口

**Files:**
- Modify: `tcg-match-service/Dockerfile`
- Modify: `tcg-match-service/Dockerfile.gpu`
- Modify: `tcg-match-service/docker-compose.yml`
- Create: `tcg-match-service/docker-compose.gpu.yml`
- Modify: `tcg-match-service/entrypoint.sh`
- Modify: `tcg-match-service/requirements.txt`
- Create: `tcg-match-service/app/routes/catalog.py`
- Modify: `tcg-match-service/app/main.py`
- Create: `tcg-match-service/tests/test_readiness.py`
- Create: `tcg-match-service/tests/test_prices_api.py`
- Modify: `tcg-match-service/README.md`
- Modify: `tcg-match-service/OPERATION_GUIDE.md`

**Interfaces:**
- Produces: deployable CPU image, optional GPU override, PostgreSQL service, readiness/categories/prices APIs and runbook.

- [ ] **Step 1: Write readiness and price endpoint tests**

Assert health does no DB/model/Dify work; ready fails until model+DB+active release+valid profile available and reports optional Dify degraded separately; categories expose vector counts; price curve preserves series dimensions/date ordering/currency; invalid ranges reject; missing card 404; no price data is 200 with empty series and coverage metadata.

- [ ] **Step 2: Update dependencies and container startup**

Pin compatible major/minor ranges and use CPU PyTorch installation source in CPU image. Add psycopg/pgvector/httpx and remove Paddle/OCR dependencies. Entrypoint runs migrations then serves; it never auto-builds 36 万索引. Add explicit import profile/command. Ensure service runs non-root where writable mounts permit.

- [ ] **Step 3: Add Postgres/pgvector and durable volumes**

Use a pinned `pgvector/pgvector:pg16` image tag resolved to a tested patch/digest during implementation. Store PGDATA on a named volume; mount raw `/data:ro`, models `/models:ro`, model cache/import reports writable separately. API waits on database health and active release readiness, not a fixed sleep. Avoid embedding default production passwords; `.env.example` contains names and safe local-only examples.

- [ ] **Step 4: Implement routes and wire lifespan**

Register recognize and catalog routers. Startup validates model fingerprints against active data/decision profile. API can start in not-ready state for import operations; recognize returns 503 until ready. Dify readiness diagnostic calls `/parameters` only on operator command/startup when configured and does not generate content.

- [ ] **Step 5: Run automated and container checks**

```powershell
cd tcg-match-service
pytest -q
docker compose config -q
docker compose build tcg-match
docker compose up -d postgres tcg-match
docker compose ps
```

Verify `/v1/health` 200, `/v1/ready` reports correct state, migrations are idempotent, restart preserves active release, process has one worker, image lacks Paddle packages, and service starts with outbound model access blocked when local models are complete.

- [ ] **Step 6: Update runbooks with exact operator workflows**

Document first install, model upload verification, manifest/import stages, release publish/rollback, CPU/GPU selection, DB backup/restore, data/version retention, both API curl examples, Dify degraded behavior, log/metric fields and troubleshooting. Commands must match implemented CLI `--help` output.

- [ ] **Step 7: Commit and push Task 9**

Stage configs/source/tests/docs only, run `git diff --cached --check`, verify `git ls-files` has no data/model outputs, commit `feat: package pgvector matching service`, and push.

---

### Task 10: 校准、serial/fusion 公平评测与 CPU 验收

**Files:**
- Create: `tcg-match-service/script_temp/evaluate_strategies.py`
- Create: `tcg-match-service/script_temp/benchmark_cpu.py`
- Create: `tcg-match-service/tests/test_evaluator.py`
- Create: `tcg-match-service/tests/test_benchmark_report.py`
- Create: `doc/tcg-match-service-evaluation-template.md`

**Interfaces:**
- Consumes: immutable labeled evaluation manifest, both APIs or in-process orchestrators, active release/model/Dify versions.
- Produces: ignored JSON/CSV raw results, versioned decision profile candidate, Markdown comparison report.

- [ ] **Step 1: Define and test evaluation manifest validation**

Require unique sample_id, image relative path/hash, expected category/product/equivalence group, in_db/is_card, ocr_text/lang and split/group_id. Reject calibration/held-out group overlap, missing labels, path escape and mutable file hash mismatch.

- [ ] **Step 2: Test metric calculations on a hand-computed fixture**

Assert Top-1, Recall@5, MRR, auto precision/coverage, false accept, correction, damage, paired McNemar counts and latency percentiles. A fixture where all requests are rejected must have zero coverage and cannot pass. Report numerator/denominator and bootstrap confidence interval, not only percentages.

- [ ] **Step 3: Implement exact-vs-HNSW retrieval audit**

Sample every category proportionally with a minimum per category. Compare ANN Top-50 against exact pgvector/FAISS results under the same vectors, report global/macro/worst category Recall@50, fewer-than-K incidence and query plan. HNSW parameters are then fixed in the report.

- [ ] **Step 4: Implement two-phase strategy experiment**

Phase A freezes the same decision profile and measures scheduling/available evidence. Phase B grid-searches serial/fusion profiles on calibration only: RRF visual weight `{0.5,0.6,0.7,0.8,0.9}`, retrieval K `{20,50,100}`, admissible observed-score/margin thresholds, subject to auto precision ≥95% and false-accept constraints. Select maximum coverage, then evaluate once on held-out. Do not tune on held-out.

- [ ] **Step 5: Implement LLM control and paired outputs**

Allow `--llm-mode live|record|replay|off`. Cache key includes image/OCR/scope/candidate payload/workflow version hash. Paired result lists serial-correct/fusion-wrong and reverse with scores/timings. Real latency report uses live/no replay and separates with-LLM from without-LLM.

- [ ] **Step 6: Implement CPU benchmark**

Warm models and PG, then measure concurrency 1 and 2 for serial/fusion, OCR/no-OCR, category/global, LLM excluded/included. Report p50/p95/p99, throughput, queue time, process and PG RSS, CPU seconds/request, failure/degrade counts and BGE/Dify call rates. Abort on data/model/profile version drift.

- [ ] **Step 7: Run script unit tests**

Run: `cd tcg-match-service && pytest tests/test_evaluator.py tests/test_benchmark_report.py -q`

Expected: all hand-computed metrics and report schema pass.

- [ ] **Step 8: Execute staged evaluation gates**

1. Generated/approved 1,000-card import rehearsal.
2. Labeled demo set regression.
3. Formal real-photo calibration/held-out set after user supplies labels.
4. Target CPU server full benchmark after user supplies machine access/spec.

At each gate save raw output under ignored `/data/evaluations/<run-id>/` and a Markdown report under `doc/` only when it contains no data artifacts or secrets. Write `decision_profile.json` to runtime config storage; commit only a sanitized profile when dataset/model identifiers are non-sensitive and stable.

- [ ] **Step 9: Commit and push Task 10**

Commit scripts, tests, template and approved sanitized report/config as `test: add paired serial fusion evaluation`; verify raw data, Dify responses and credentials are not staged, then push.

---

### Task 11: 全量导入、发布和回滚演练

**Files:**
- Modify after evidence: `doc/tcg-match-service-evaluation-template.md` into a dated deployment report
- No source change is accepted silently during this task; discovered bugs return to the owning Task with tests.

**Interfaces:**
- Consumes: official raw package + manifest, model packages, target Postgres, Dify configuration, accepted decision profile.
- Produces: active verified release and signed-off operational evidence.

- [ ] **Step 1: Record immutable input inventory**

Record raw source_version/file hashes, categories, product/image/price counts, model/backend/file fingerprints, code commit, migration version, profile version, Dify published workflow/version marker and target CPU/RAM/disk. Store no API key.

- [ ] **Step 2: Validate the formal raw package**

Run discover and manually bind stable category codes in manifest; run validate. Review duplicates, missing/corrupt images, invalid IDs, unknown currency and incomplete price windows. Stop publish on unexplained failures; keep the report and fix source/manifest explicitly.

- [ ] **Step 3: Import to a new release with checkpoints**

Run prepare → encode → build-index → verify using the exact printed release ID. Interrupt once at a safe test point and resume to prove recovery. Observe model loaded once, memory bounded, no online API traffic for model load, and unchanged vectors reused when applicable.

- [ ] **Step 4: Verify database and retrieval integrity**

Compare valid product counts to source, card-image/vector coverage to quarantine, foreign keys, dimensions/norms, identity lookups, price coverage, HNSW vs exact recall, and sampled self-match. Run `ANALYZE`; capture index/table sizes and EXPLAIN plans.

- [ ] **Step 5: Publish, smoke test and rollback**

Publish the VERIFIED release, call both APIs for category/global and OCR/no-OCR samples, check prices, then roll back to prior release and verify request metadata changes. Re-publish new release only after rollback succeeds. Existing in-flight requests must retain their pinned version.

- [ ] **Step 6: Run target-host paired and resource acceptance**

Execute Task 10 evaluation/benchmark. Confirm serial call order includes OCR text before LLM for low visual confidence, fusion waits for both available modalities, scoped leakage is zero, auto precision/coverage and latency are explicitly reported, and Dify outage returns vector candidates.

- [ ] **Step 7: Final documentation commit and push**

Complete the dated report with evidence and remaining limitations. Stage only report/runbook/config changes, inspect tracked files for data, commit `docs: record TCG matching deployment acceptance`, and push. Mark the implementation complete only when the acceptance report contains executed results rather than planned values.

---

## Execution order and review gates

```text
Task 1 contracts
  → Task 2 DB schema/repository ─┐
  → Task 3 model consistency ───┼→ Task 4 importer
  → Task 5 matching rules ──────┼→ Task 7 serial OCR recovery
  → Task 6 Dify fallback ───────┘        ↓
                                  Task 8 fusion/concurrency
                                           ↓
                                  Task 9 Docker/operations
                                           ↓
                                  Task 10 evaluation
                                           ↓
                                  Task 11 formal release
```

Task 2 的 PG 集成测试、Task 3 的真实本地模型 smoke、Task 4 的采样导入可以在对应依赖齐备时并行准备，但同一 git 工作区按 Task 顺序提交，避免交叉暂存。Task 7 是 serial 可验收里程碑，Task 8 不得通过复制一套规则绕过共用决策器。

## Definition of done

- 两个独立策略 API 和兼容 serial 别名使用同一版本、repository、模型、决策及 Dify 查表逻辑。
- 自动测试实际证明低视觉+可用 OCR 的 serial 调用顺序为 DINO → BGE/文字召回 → 决策 → 必要时 Dify。
- fusion 有 OCR 时双路并发，无 OCR 与 serial 语义一致，并发受界、降级可观测。
- 正式数据包可校验、断点导入、版本发布、回滚；36 万物理行的有效/重复/缺图统计来自报告。
- CPU 镜像完全离线加载已上传模型，DINO/BGE 的在线与离线处理一致；GPU override 通过 smoke test 后可用。
- pgvector 的品类/全局检索经过 exact 对照；价格查询保留来源、币种、窗口和系列维度。
- 真实照片 held-out 报告同时给出精度、覆盖率、纠错/损伤、错误接受和资源/延迟；95% 目标有明确分母，未达标时如实保留 serial/fusion 实验结果。
- Git 历史只包含源码、配置、测试和文档；数据、图片、模型、向量、缓存、密钥和原始评测输出均未被跟踪。
