# TCG 单机双策略识别服务：技术方案

日期：2026-09-05；2026-09-08 补充数据、模型与更新约束；2026-09-09 增加 Dify 双 intent、PG/LLM 逐字段合并、LLM 价格曲线与监控契约。状态：可审阅的设计基线；尚未完成本次变更的代码实施或服务器验收。

现有[分步骤实施计划](tcg-match-service-implementation-plan.md)尚未同步本次 Dify 双 intent 变更，将在本设计确认后更新。本方案取代根目录 `tcg-match-service-plan.md` 中与本次要求冲突的规划；原文件保留为历史输入。历史文档中的任务和操作命令不视为本次实施授权。

## 1. 结论与范围

同时提供串行补救与并行融合两个 API，技术上可行。并行版有机会纠正视觉高分误匹配，也会额外消耗 CPU，且可能被错误 OCR 干扰；准确率和延迟改善是需要验证的假设。

生产采用 FastAPI + PostgreSQL/pgvector，单服务器、单 API 实例、默认 CPU-only。DINOv2 编码图片，本地 BGE 编码标准卡文本及客户端 OCR；两种向量分别建库检索，通过全局唯一的 `productId` 融合结果。原始图片和 JSONL 按品类、版本原样保存在部署根目录 `tcg-service/data/` 对应的容器挂载目录，数据库同时保存规范化字段、逐行原文、原始 JSONB、价格数据和两种向量。FAISS 保留为离线精确检索基准。

首版包括：可复用导入命令、本地优先模型加载、两版识别 API、客户端 OCR 辅助重排、前置 Dify 卡牌/品类判断、后置 Dify 消歧与内容增强、卡牌查表及价格查询、离线对比与 CPU 压测。外部接口继续保留可选 category，首版调用方预计不传；服务使用同一个 Dify GPT-5.5 Workflow，通过 `intent=classify` 和 `intent=recognize_enrich` 每请求最多执行两次，这些 intent 对外不可见。服务器 OCR、多实例、Redis、多级缓存、训练新模型和分布式向量库不在首版范围内。

## 2. 已核实事实与实际缺口

代码核对对象是 `tcg-match-service/`，根目录 `app/` 只用来核对 demo 模型。未运行 Docker 构建、全量模型推理或线上 Dify 请求。

| 项目 | 证据/现状 | 本次处理 |
|---|---|---|
| 框架和向量库 | `app/main.py` 为 FastAPI；`services/index_service.py` 从 NPY 加载 FAISS IndexFlatIP | 复用 API 组织方式，改由 PG 保存业务和向量数据 |
| 串行链路 | `routes/recognize.py` 为品类 LLM → DINO → 高分返回/LLM；OCR 入参没有参与匹配 | 补齐图像 → OCR 文本召回重排 → LLM 查表 |
| 品类 | 当前 API 接受可选内部 `category/category_hint`，缺省时可全库检索 | 外部 category 继续可选；匹配前强制执行 Dify `intent=classify`，缺省时采用其 `cardIp`，传入时进行一致性校验，再用内部 category 限定检索 |
| OCR | `main.py` 启动 PP-OCR，`routes/ocr_match.py` 识别上传图片 | 从生产启动与依赖中移除，OCR 由客户端提供 |
| DINO | demo 和服务调用 `dinov2_vitb14`；备用 `facebook/dinov2-base` | ViT-B/14、无 registers、768 维；它是特征提取器，不是 GroundingDINO 检测器 |
| DINO 输出适配 | 当前直接对 `model(x)` 调用 `.dim()`，Transformers 的输出对象不支持此用法 | 显式适配 tensor / `last_hidden_state[:, 0]`，不盲目替换后端 |
| BGE | 本地 README 标识 `bge-small-en-v1.5`；config hidden_size=384，CLS pooling，max_seq_length=512 | 以用户手工放入部署目录 `tcg-service/models/bge_model` 的完整模型包为基线，并记录文件指纹 |
| BGE 一致性 | 查询读本地包，构建脚本重新从网上加载模型 | 离线和在线使用同一加载器、tokenizer 与模型版本 |
| ID | 样例 `productId=100009.0`；在线用 `str(productId)`，文本构建用 `str(int(productId))` | 修复 `100009.0` 与 `100009` 关联失败问题 |
| 导入 | `scripts/build_index.py` 按品类重新加载模型、一次性收集数据；无版本发布和断点协议 | 流式、分批、可恢复、可复用 embedding |
| 启动 | `entrypoint.sh` 启动前自动建索引，忽略传入的构建命令；在线挂载 `/data:ro` | 启动只加载已发布数据；导入使用独立一次性命令 |
| LLM | 当前 Dify client 只读取卡号/系列，orchestrator 调用后丢弃结果；参考 Workflow 尚无 intent 分支 | 同一个已发布 Workflow 增加 `classify/recognize_enrich` 两个 intent；服务严格校验输出和查表，PG 无价格时才采信带明确监控标记的 LLM 生成曲线 |
| 当前数据 | 47 个 products.jsonl，逐行计数 364,136，合计 745,649,639 字节 | 这是物理行数，不代表去重后的有效卡数或图片数 |
| 价格样例 | `prices/03_Pokemon.jsonl` 每行一个产品及 sales 数组 | 按价格数据单独建模，不塞进 embedding 文本 |

前次对话中“每个产品文件只有一行”是统计方法错误，已更正。正式导入以用户另行上传的完整数据包为准，目录名称可以不同。本次未收到可读取的 Image #1 / Image #3，价格设计依据实际 JSONL 样例，不假称核对过截图。

## 3. 两种策略的价值与边界

| 维度 | serial：串行补救 | fusion：并行融合 |
|---|---|---|
| 共同前置 | Dify `intent=classify`，验证卡牌有效性并确定 category | 与 serial 相同；前置分类不计入商品身份 `dataSource` |
| 开始 | 在分类确定的 category 内执行图片编码/召回 | 分类完成后，有可用 OCR 时图片、文本两路一起调度 |
| 图片可信 | 可直接命中，省掉 BGE | 等两路完成后联合判断 |
| 图片低分 | 有 OCR 才执行文本补救 | 已有两路候选可重排 |
| 高分但认错 | 可能提前结束；轻量卡号冲突规则可拦截部分情况 | OCR 有机会纠错，也可能干扰原本正确的结果 |
| 无 OCR | 视觉 → 必要时执行 `intent=recognize_enrich` 消歧/补全 | 同一视觉路径；响应 strategy 仍表示请求的是 fusion |
| 匹配后 | 执行 `intent=recognize_enrich` 生成评级/收藏建议，PG 字段覆盖 LLM 事实字段 | 与 serial 相同 |
| 计算开销 | 文本推理次数较少 | 可用 OCR 请求基本都会进行文本推理 |
| 适用目标 | 成本/吞吐优先的基线 | 召回与纠错效果的实验版本 |

备选融合方法：原始余弦加权虽然简单，但两模型分数分布不同；经过标注校准的分数融合更灵活，但需足够验证数据。首版采用加权 RRF（排名融合）加证据规则，后续只在评测证明收益时引入学习式融合。英语 BGE 的分数不等于概率，模型官方也要求在具体数据上选阈值。[BGE 模型卡](https://huggingface.co/BAAI/bge-small-en-v1.5)

在理想无资源竞争情况下，双路耗时接近 `max(T_visual, T_text)`；CPU 上两模型会争抢核与内存带宽，不能以这个式子承诺实际耗时。串行平均成本还取决于提前命中比例，应报告 CPU 秒/请求而不只看墙钟时间。

## 4. API 与共同响应契约

| 路由 | 语义 |
|---|---|
| `POST /v2/recognize/serial` | 串行补救 |
| `POST /v2/recognize/fusion` | 并行召回融合 |
| `POST /v2/recognize` | 兼容别名，固定指向 serial；返回 strategy 说明实际策略 |
| `GET /v1/health` | 存活信息；不发 LLM 计费请求 |
| `GET /v1/ready` | 模型、数据库、数据版本就绪情况 |
| `GET /v1/categories` | 当前版本有效品类及向量覆盖数 |
| `GET /v1/cards/{category}/{product_id}/prices` | 价格曲线，日期、语言、版本、品相筛选 |
| `GET /v1/images/{category}/{card_id}` | 兼容图片读取；从 DB 取映射路径 |

三个识别入口采用相同 multipart 参数；新业务只使用两个显式策略入口，`/v2/recognize` 仅保留兼容：

- `image`：必填，可为 multipart 二进制文件、HTTPS URL 或服务器白名单根目录内的绝对路径；最终统一解码为单张图片。最大 10 MiB、解码后最大 20MP，拒绝动画/多帧和损坏图。URL 必须限制协议、地址、重定向、超时和下载字节以防 SSRF；路径必须 resolve 后验证仍位于白名单内。
- `text`：可选，空白等于未传；最大 8,192 字符。客户端 OCR 不可信，不能成为系统指令。
- `confidence`：可选，客户端 OCR 可信度，范围 `[0,1]`；内部命名为 `ocr_confidence`，不得与最终决策置信度混用。
- `category`：可选展示枚举。首版调用方不传时由服务自动判断；传入时仍执行前置分类，两者不一致返回 400。category 不能绕过图片有效性检查或覆盖分类结果。
- `category_hint/ocr_lang`：只作为旧接口兼容字段存在，不出现在新业务文档中。

缺必填项返回 422，非法/不可读图片返回 400，过大输入返回 413，服务未就绪/队列已满返回 503。前置 Dify 超时、工作流失败、输出 schema 错误或非法 `cardIp` 也返回 503，禁止静默进入全品类检索。内部召回 K 默认 50，最终最多 5 个候选；K 不向客户端开放，保证实验配置可追溯。

对外响应统一为 `text + priceTrend + monitor`，不得用顶层 `status` 承载匹配结论。当前内部决策的 `status` 映射为 `monitor.status_match`；`decision_path/category/product_id/candidates` 可继续留在内部诊断日志，`warnings/request_id/dataset_version/model_version/workflow_version/decision_version/latency_ms/timings_ms` 迁入 monitor。命中 PG 后按目标字段逐项合并：语义一致且有效的 PG 值优先，PG 缺失时才采用后置 Dify LLM。`priceTrend` 优先使用 PG 的 `purchasePrice/orderDate`，PG 无可用明细时由 LLM 生成，两个来源不得混合且不再调用 JustTCG。

`monitor.confidence` 首版为 null；monitor 分别携带 visual_score、text_score、fusion_score、margin、ocr_used、text_retrieval_used、input_text_confidence 和候选数量。规则门限不是概率；如后续引入概率校准，必须附校准版本及可靠性评估。`ocr_used` 表示实际使用 OCR 规则或文本证据，`text_retrieval_used` 区分是否调用 BGE。

| `monitor.status_match` | 含义 |
|---|---|
| matched | 已确定且有库内记录，product_id 不为空 |
| candidates | 存在多个或证据不足的候选，不自动报成命中 |
| recognized_no_db | LLM 提取了身份，经过限定范围查表无命中；身份与 DB 数据分开展示，productId 为 null |
| unrecognized | 无足够身份或候选；LLM 失败可以返回此状态并附 warning |
| not_a_card | 仅当前置 Dify 明确识别为非支持 TCG 或体育卡时返回；低向量相似度本身不能证明不是卡 |

`text.state` 保留前置 Dify 的“是否为支持的有效 TCG”语义，不表示是否命中 PG；有效 TCG 即使 `status_match=candidates/recognized_no_db/unrecognized` 仍返回 `state=true`。基础设施故障用 HTTP 503。前置分类是必需依赖，失败不可降级；后置增强在商品已可靠匹配时允许降级为空评级/收藏建议并记录 warning，只有商品必须依赖 LLM 消歧时才影响业务结果。匹配 ID 有而业务记录缺失属于数据完整性故障，禁止返回 matched。

## 5. 共同候选与决策逻辑

### 5.1 召回范围与证据

请求进入时先固定数据版本，再调用 Dify `intent=classify`。只有 `state=true`、`isSportsCard=false` 且 `cardIp` 命中八种规范枚举时才继续；外部 category 缺省时采用该 `cardIp`，已传时必须一致，否则返回 400。服务随后映射内部 category，DINO、BGE、身份查表、商品和价格查询全程使用该版本与 category。前置工作流故障或非法品类返回 503，不静默扩大到全库。内部运维/评测仍可保留显式全库能力，但不属于首版外部请求路径。

视觉/文本各取前 K，另提取 OCR 的卡号、系列代码及名称线索。按 `product_id` 合并，最多 `2K + 5` 个候选；category_id 作为检索范围、展示和一致性校验字段，不参与卡片身份主键。OCR 精确身份查表超过 5 个结果时标为歧义，不任取一个。

卡号仅做 Unicode NFKC、大小写和空白归一；保留斜杠、前缀和有意义的分隔符，例如 `12/100` 不等于 `12100`。数字文本可能是 HP、年份或攻击力；孤立数字不能成为排除候选的硬规则。只有卡号+系列等可互相验证的身份组合才标记明确冲突。图像完全相同但不同产品 ID、版本/语言/闪卡差异均保留为歧义候选。

首版 BGE 是英语模型。OCR 为空或仅噪声时跳过文本路；已明确为非英语的文本不使用 BGE 强证据，仍允许卡号/系列规则查表。未给语言时，至少 4 个 ASCII 字母且 ASCII 字母占全部字母不少于 80% 才进入英语密集检索；这是输入筛选启发式，不代表 OCR 质量概率。所有规则都记录原因并在日文/混合文字分组评估，不声称覆盖所有品类语言。

### 5.2 加权排名融合

实验初值 `w_v=0.7, w_t=0.3, c=60`，不是已调优结果。权重必须非负；某一路缺失、超时或不适用时，其权重归零，剩余权重归一化。

```text
R(i) = w_v / (c + rank_v(i)) + w_t / (c + rank_t(i))
候选未进入某路 Top-K → 该项贡献为 0（不是余弦分数为 0）
并列 → visual_cosine 降序 → category_id/product_id 升序
```

RRF 用于排名，不用于把第一名包装成高置信结果。保留原始模态分数和模态缺失标记；必要时对候选集合补算向量点积得到两路完整分数，不能把“未召回”误当“不相似”。明确身份冲突的候选不能自动匹配，但可在诊断中保留。

### 5.3 接受规则与校准

共享决策器使用三类门限：视觉直通（分数+第一二名差距）、融合接受（两路证据下限+RRF 第一二名差距）、身份确认（唯一系列+卡号组合、无图像明显冲突）。融合第一名只在以下任一条件下自动匹配：

1. 它仍为视觉第一名，视觉直通达标，且不存在可信 OCR 冲突；
2. 它具备两路分数支持，达到校准的融合门限，无身份冲突；
3. OCR 或 LLM 身份在同一范围内唯一命中，具备至少两个相互支持的身份字段，并通过校准的最低视觉支持检查。

其余情况进入 LLM 或保留候选。缺第二名不能把 margin 人工设为 1；不得因库只有一张卡就强行接受。完全相同图片的不同 ID 若无身份消歧证据，不自动匹配。

`decision_profile.json` 包含版本、模型指纹、适用数据版本、品类范围模式、视觉/文本/融合门限、RRF 权重和证据规则版本。基线 `0.87/0.02` 仅用于回归对照，不能直接成为 36 万跨品类上线门限。没有已验证 profile 时 `auto_match_enabled=false`，可返回候选和提取身份，不能宣称已校准。样本少的品类使用全局保守 profile；无可靠覆盖的语言禁用相应自动接受路径。

### 5.4 serial 流程

```text
输入校验与固定数据版本
  → Dify(intent=classify) → 业务拒绝直接返回 / 故障返回 503 / 合法 cardIp 固定 category
  → DINO 编码/召回
  → 视觉接受规则通过（可含轻量 OCR 身份冲突拦截）→ matched
  → 否则：有可用 OCR → BGE 编码/召回 + OCR 身份查表 → 合并重排
      → 接受规则通过 → matched
      → 否则 → Dify(intent=recognize_enrich) 消歧 + 严格查表
  → 无可用 OCR：跳过 BGE，必要时执行同一后置 intent 消歧
  → 已有可靠商品时仍执行后置 intent 补充评级/收藏建议
  → PG 优先、LLM 补缺的逐字段合并 → 组装 text / priceTrend / monitor
```

高视觉分支不启动 BGE；轻量 OCR 字段解析不等于调用 OCR 模型或文本 embedding。无校准 profile 时不提前自动命中。后置 intent 失败不能推翻已经可靠确定的视觉/文本匹配，只清空 Dify 专属字段并记录 warning。

### 5.5 fusion 流程

```text
输入校验与固定数据版本
  → Dify(intent=classify) → 业务拒绝直接返回 / 故障返回 503 / 合法 cardIp 固定 category
  → 有可用 OCR：并发调度 DINO 编码/召回 与 BGE 编码/召回
  → OCR 不适合 BGE：视觉召回 + 可用身份规则
  → 合并候选 → 加权 RRF → 共同接受规则
  → 仍不确定：Dify(intent=recognize_enrich) 消歧 + 严格查表
  → 已有可靠商品时执行同一后置 intent 补充评级/收藏建议
  → PG 优先、LLM 补缺的逐字段合并 → 组装 text / priceTrend / monitor
```

有可用文本时不得先看到视觉高分就提前返回，否则实验没有检验融合纠错。文本路失败时退为视觉规则，记录降级，候选不丢失。视觉编码/主检索不可用视为核心故障并返回 503。无 OCR 时复用 serial 的视觉分支，除 strategy 和计时外结果应相同。

## 6. 数据库选择与数据结构

PG+pgvector 可把卡信息、价格及向量置于同一事务体系；PG+FAISS 多一份索引同步协议，PG+Qdrant/Milvus 多一套数据库运维。以单机、36 万、低更新频率约束选择前者。

初版使用 float32 的 `vector(768)` 与 `vector(384)`，采用 HNSW 余弦索引。pgvector 支持这两个维度，近似索引牺牲部分召回率；索引召回率需要对照精确检索测量。[pgvector 官方说明](https://github.com/pgvector/pgvector)

### 6.1 版本组织

`public.dataset_releases` 保存 release UUID、schema_name、manifest_hash、model_fingerprint、状态和统计；`public.active_dataset` 为单行发布指针；`public.import_checkpoints` 保存各文件的哈希、字节偏移和已完成批次。每次更新以一个或多个品类的完整 JSONL 快照为输入，新 release 继承未声明品类，并完整替换已声明品类。

每个待发布数据版本写入独立 `ds_<uuidhex>` schema，验证完成后通过小事务切换指针；正在处理的请求继续使用进入时固定的旧 schema。版本发布后只读；首版保留当前和前一版本，清理使用显式运维命令、备份和无活跃请求检查，不自动删除原始文件。连接池查询必须使用注册表给出的 schema 并进行 SQL identifier 引用，不能把客户端字符串作为 SQL 标识符。

### 6.2 每个版本中的表

| 表 | 主键/主要字段 | 索引与职责 |
|---|---|---|
| categories | category_id、stable_code、display_name、source_mapping | stable_code 唯一，目录名只是路径 |
| source_files | source_file_id、source_version、kind、category_id、relative_path、sha256、bytes | 文件级来源和完整性记录；同一 release 内相对路径唯一 |
| cards | product_id、category_id、name、set_id/name/code、number_norm、raw_line、raw_json、source_file_id/line_no/line_sha256、source_hash、text_hash | `product_id` 全局主键；category_id 索引；(category_id,set_code,number_norm)；名称规范化索引 |
| card_images | product_id、category_id、relative_path、sha256、width/height、orientation_policy、duplicate_group | product_id 主键并 FK cards；首版每卡一个明确的主标准图 |
| visual_embeddings | (category_id, product_id)、embedding vector(768)、model_version、input_hash | FK cards；按 category_id LIST 分区、每分区 HNSW；联合键满足 PostgreSQL 分区约束，不改变 product_id 的全局身份 |
| text_embeddings | (category_id, product_id)、embedding vector(384)、model_version、doc_version、input_hash | 同上，图片缺失不妨碍文本入库 |
| price_source_records | (source_file_id,row_no)、product_id、category_id、raw_line、raw_json、line_sha256 | 完整保留价格 JSONL 每行原文和语义内容，并关联 cards |
| price_snapshots | (product_id,captured_at,currency)、category_id、market/lowest/median 等、source_file_id/row_no | 保存产品 JSON 中的价格快照，不伪装为逐日历史 |
| price_sales | (product_id,source_batch,row_no)、category_id、order_date、purchase_price、shipping_price、condition、variant、language、quantity、currency | 按 product_id/order_date 查询，保存成交明细和来源 |
| price_coverage | (product_id,source_batch)、category_id、min_date、max_date、total_results、loaded_count、complete | 表示抓取覆盖范围和是否完整 |

价格金额用 NUMERIC，时间用 TIMESTAMPTZ，ID 用 BIGINT；解析 JSON 时用 Decimal 校验 ID 必须是正整数，拒绝非整数和越界值，API 中输出 ID 字符串。`productId` 在同一文件、同一品类和跨品类出现重复都必须在数据库写入前失败。raw_json 保留所有原始属性，但 JSONB 不保证键顺序、空白或数字词法形式，因此 cards 和 price_source_records 另存 UTF-8 `raw_line`、行号和行哈希；不可变原始文件及文件哈希是字节级权威来源。变动价格、SKU 品相清单不进入文本向量。

图像文件名通过 manifest 规则映射 product_id；默认可支持 `{product_id}.jpg` / `{product_id}_200w.jpg`，多个文件同时匹配必须明确主图规则。横版真实设计与拍摄旋转不能混为一谈：manifest 指定 `preserve` 或 `portrait_rotate_cw`，保持离线/在线模型输入策略可追溯，不自动把所有横图旋转。

### 6.3 品类过滤与全品类检索

原始 products/price JSONL 继续按品类分文件保存；数据库中的卡片属于同一个 release，视觉和文本向量表按品类物理分区。外部识别请求必须先把 Dify `cardIp` 映射为内部 category，再在对应分区内 ANN 检索，不得先做全局 ANN Top-50 再用 Python 筛品类。分区父表的全库检索只保留给内部运维、离线评测和故障诊断，不是前置分类失败时的线上降级路径。不得为每个品类部署互不关联的数据库或服务；用 EXPLAIN 验证实际计划、分区裁剪和返回数量，不假设数据库一定选择理想计划。

初始 `m=16, ef_construction=64, ef_search=100`，以 Recall@50 和延迟调参。pgvector 的 ANN 附加过滤可能减少结果数，0.8+ 可采用 iterative scan；本方案仍对少结果/小品类提供同一范围精确检索回退。[过滤说明](https://github.com/pgvector/pgvector#filtering)

### 6.4 价格导入与曲线

当前 sales 样例为每个商品一条对象，包含 `productId/totalResults/count/minDate/maxDate/sales[]`；每条 sale 包含 `orderDate/purchasePrice/shippingPrice/condition/variant/language/quantity/listingType/title`，但没有稳定成交 ID。同一交易字段哈希不能证明是同一笔交易，不能简单按价格+时间去重，避免抹掉真实重复成交。首版按“产品+来源批次+数组 row_no”保存，原样保留同日同价重复行；同一文件/版本重复导入幂等。

manifest 记录来源批次、抓取时间窗和币种。`count < totalResults` 时将 coverage 标记为不完整，但仍可保存并返回本批次实际提供的 sale；不得将其宣传为完整历史。不同批次重叠时不能仅凭价格和时间擅自去重，将来拿到稳定成交 ID 后才切到逐笔 upsert。

识别响应的 `priceTrend` 不做按日聚合：每条 sale 输出一个点，`price.extracted` 直接取纯成交价 `purchasePrice`，`price.raw` 按 manifest 币种格式化，`soldDate` 取 `orderDate` 转 UTC 后的 `YYYY-MM-DD`；`shippingPrice` 不计入价格。同一天多笔成交全部保留，按完整 `orderDate` 升序排序后再去除时间部分。`condition/variant/language/quantity/shippingPrice` 保存在 PG，当前业务响应不输出。商品 `raw_json.marketPrice` 有效时直接映射为 `text.marketValuationAvg`；该字段缺失或无效时才允许 Dify LLM 估值兜底。市场趋势按最终采用的价格序列计算，数据不足时可采用 Dify 输出，否则返回 `unknown`。

`priceTrend` 的来源优先级固定为：PG `price_sales` > 后置 `recognize_enrich` 的 LLM 生成曲线 > 空数组。PG 只要存在通过币种、金额和日期校验的可用成交明细，就不得请求或拼接 LLM 曲线；只有 PG 无可用明细且身份已经唯一确认（`status_match=matched/recognized_no_db`）时才允许 LLM 生成，`candidates/unrecognized/not_a_card` 必须返回空数组。LLM 输出必须转换为相同的 `price.raw/price.extracted/soldDate` 结构，校验金额为有限非负美元数、日期合法且不晚于请求日期、最多 100 个点，并按日期升序排序；任一点非法则拒绝整条曲线。LLM 曲线不代表已验证真实成交，必须返回 `monitor.price_source=llm_generated` 和 `PRICE_TREND_LLM_GENERATED` warning。服务不再调用 JustTCG 或其它外部价格 API。

### 6.5 PG 与 LLM 逐字段合并

字段合并器以[后端接口文档第 5.2 节](tcg-recognition-backend-api.md)的映射表为唯一契约，按字段而不是按整个对象选择来源。处理顺序为：读取命中商品 `raw_json` 和规范化列 → 验证字段是否非空、类型正确且语义一致 → 采用 PG 或确定性派生值 → 仅对缺失字段采用 `recognize_enrich` 输出 → 记录 `monitor.field_sources`。有效 PG 值禁止被 LLM 覆盖；LLM 值也必须通过对应枚举、数值、日期和 URL 校验。

当前商品 JSON 可直接或确定性映射的核心字段是：`productId→productId`、`setName→seriesName`、`productName→cardName`（仅移除与 `customAttributes.number` 完全一致的末尾编号）、`customAttributes.number→cardNumber`、`customAttributes.releaseDate→year`、`rarityName/rarityDbName→rarity`、`marketPrice→marketValuationAvg`。`productLineName=Pokemon` 不能区分 Pokémon 与 Pokémon Japan；sales 中的 `language` 不能代替卡牌标准语言；`score` 也不是模型匹配分数。语言、画师、评级字段、收藏建议以及其它缺失字段由 Dify 补齐。`productId` 只能来自 PG 唯一命中，LLM 不得生成。

## 7. 原始包与可复用导入协议

宿主机部署根目录固定为 `tcg-service/`，其中 `tcg-service/data/` 挂载为容器 `/data`，`tcg-service/models/` 挂载为容器 `/models`：

```text
tcg-service/
├── models/
│   ├── dinov2/
│   └── bge_model/
├── data/
│   ├── inbox/
│   ├── raw/
│   ├── imports/
│   ├── vector-cache/
│   └── releases/
└── tcg-match-service/
```

用户把某品类的完整 JSONL、图片和价格压缩包上传到 `/data/inbox/`；导入工具校验后解压/归档到不可变的 `/data/raw/<source_version>/`，禁止覆盖已有 source_version。目录可以不同。自动发现器只提出映射，正式导入读 `manifest.json`：

```json
{
  "schema_version": 1,
  "source_version": "release-20260904",
  "categories": [{
    "code": "magic",
    "source_category_id": 1,
    "products": "cards-pack/renamed-magic/products.jsonl",
    "images": "cards-pack/renamed-magic/images",
    "image_names": ["{product_id}.jpg", "{product_id}_200w.jpg"],
    "orientation_policy": "preserve",
    "prices": [],
    "currency": "USD"
  }]
}
```

示例不是实际生产目录。非标准价格文件通过 manifest 显式指定 `format=sales_snapshot`、路径、window_start/window_end、captured_at、complete；禁止靠模糊文件名推断品类。稳定 category code 不因文件夹改名而变化。

运行时数据目录固定为：`/data/inbox/` 保存待导入压缩包，`/data/raw/` 保存不可变源版本，`/data/imports/` 保存校验/断点/报告，`/data/vector-cache/` 保存可复用向量，`/data/releases/` 保存发布清单。执行过程：discover → validate → stage cards/prices → encode changed inputs → build indexes → verify → publish。独立 CLI 存放 `tcg-match-service/script_temp/import_data.py`，各阶段可恢复，模型只加载一次。

- 校验 UTF-8/JSON、全局 productId 唯一性、类别映射、相对路径和源文件哈希；路径不得越出数据根。保留 products/price JSONL 的原文件、原始行、行号和哈希；只逐批打开图片，不把全图库读进内存。
- 缺图/坏图记录 quarantine，基础信息仍可入库；向量禁止写零值占位。发布要求所有异常都有归因统计，不能默默跳过。
- checkpoint 与批次事务一起提交；中断后从已确认位置续跑。源文件哈希改变不能按旧偏移续跑。
- 向量缓存键至少包含 modality、input_hash、model_fingerprint 和 preprocess/text-template 版本；条件完全一致才可复用。未变化卡从活动版本或缓存复用向量，新增或相关输入变化的卡才重新编码；只修改价格不重新推理。
- 正式更新只接受 `replace-category --scope <category...>` 语义：manifest 声明的每个品类都是完整快照，新版本移除该品类输入中缺失的旧产品；未声明品类从活动版本继承。禁止把残缺文件标成完整快照，导入器不提供默认的逐条 upsert 发布路径。
- 全量替换仍生成新版本；失败不影响 active_dataset。没有发布动作，服务继续查旧版本。
- 图片路径绑定不可变 raw/source_version。原始包应写入新目录后发布，不能在旧请求仍使用时原地覆盖标准图。
- 模型/文本模板/预处理变化需要新版本重建相关向量；CPU↔GPU 变化只有通过数值一致性回归才允许复用。
- 样例图、JSONL、价格、索引、权重、自动生成报告均本地留存并加入忽略；合成测试数据在测试代码中生成，不提交数据集。

## 8. 模型与 CPU/GPU 部署

DINO 基线固定 `dinov2_vitb14`、输入 RGB resize `(168,224)`（W,H）、bicubic、ImageNet mean/std、CLS 768 维、L2 归一化。客户端负责几何预处理；服务做解码、EXIF 处理和模型张量转换，gallery/query 共用转换函数。[DINOv2 官方模型列表](https://github.com/facebookresearch/dinov2)

模型由用户手工放入宿主机部署目录 `tcg-service/models/`，Compose 只读挂载为 `/models`。DINO 包固定读取 `/models/dinov2`，BGE 包固定读取 `/models/bge_model`；两者都必须包含加载所需文件和 commit/hash 清单。生产配置固定 `ALLOW_MODEL_DOWNLOAD=false`，从本地创建架构 `pretrained=False` 后加载本地权重，不得隐式联网。文件缺失、损坏或指纹错误时明确失败，不静默下载或换模型。

若交付包选用 HF 的 `facebook/dinov2-base`，由显式 backend 配置加载，统一适配 CLS 输出，并对照 demo 小样本校验；不把 Torch Hub 权重直接当 HF 目录，也不把相同维度当数值等价。HF 后端启用前完成相同输入的余弦及 top-K 回归，失败则重建并重新校准。

BGE 固定加载 `/models/bge_model`，文档编码不加查询指令，OCR 查询加现有 prefix；正文按名称、卡号、系列、类型、描述/技能的确定顺序生成，去 HTML，列表稳定展开，保留关键身份字段，超出 512 tokens 时截断尾部。模板是跨品类通用字段加少量明确字段映射，不沿用只有宝可梦 HP/攻击的文本布局。

生产为一台主机上的 API 和 PostgreSQL 两个容器，不代表两个 API 实例；Uvicorn workers=1。`DEVICE=cpu` 默认，`cuda` 必须有可用 GPU，否则启动报配置错误；兼容已有 USE_GPU 参数并明确映射。Compose 位于 `tcg-service/tcg-match-service/`，因此宿主机映射固定写为 `../models:/models:ro` 和 `../data:/data`；API 使用只读数据挂载，独立 importer job 使用可写数据挂载。GPU 使用独立镜像/Compose override 切换相同代码；CPU 镜像使用 CPU torch 依赖，不安装 PaddleOCR。

并发由有界请求队列和共享 CPU 工作池控制。起始最多 2 个识别请求、2 个模型作业并发，每模型同时最多 1 次调用；DINO/BGE 可在不同线程执行。torch intra-op 起始 2、interop 1，并协调 BLAS/OMP 线程限制；这是试验初值，不能在请求处理中反复修改全局线程数。同步模型与数据库工作不阻塞 ASGI 事件循环。每条并发 SQL 使用自己的连接，池上限起始 6。

总请求预算起始 60s；排队最多 1s；SQL statement_timeout 起始 2s；LLM 上传+执行总预算不超过剩余时间且最多 45s。模型线程超时不代表底层计算已经停止，作业槽位必须保持到实际结束，避免虚假释放导致超卖；记录排队/推理/SQL/重排/LLM 各阶段。

36 万条双向量的 float32 元素约 1.545 GiB；这不包括表、HNSW、JSON、价格、WAL 和双版本。采购参考起点为 8 vCPU / 32 GiB RAM / SSD，尚未获得目标服务器配置，不能承诺 8 GiB 容器限制足够。磁盘按实测图片体积 + 至少两个 DB 版本 + WAL/备份余量计算。全量导入先跑 1,000 张采样实测再估计，时间公式为图片数/实测吞吐+文本编码+写库/建索引，不承诺几小时完成。

## 9. Dify GPT-5.5 双 intent 工作流

两个策略共用一个已发布 Dify Workflow，同一识别请求最多执行两次。Workflow 开始节点增加必填字符串 `intent`，紧接条件分支，只允许 `classify` 和 `recognize_enrich`；未知 intent 直接输出 schema 错误，不默认进入任一昂贵分支。GPT-5.5 在 Dify 模型节点配置，工作流 API 请求不通过随意增加 model 字段选择模型。

第一次在任何向量检索前调用 `intent=classify`，只传图片，只输出 `{state,stateErrorReason,isSportsCard,cardIp}`。`state=true` 时 error reason 必须为空，且非体育卡必须给出八种规范 `cardIp` 之一。正常的 `state=false` 或 `isSportsCard=true` 是 HTTP 200 业务拒绝；上传失败、超时、429、工作流失败、JSON/schema 错误或非法 cardIp 是必需依赖故障，返回 HTTP 503，禁止静默全库检索。

第二次在候选需要消歧或商品已经匹配后调用 `intent=recognize_enrich`。输入包括图片、可选 OCR/置信度、前置 cardIp、候选摘要、已命中商品 JSON、PG 逐字段缺失清单、`marketPrice` 和 PG `priceTrend` 摘要；输出可以包含候选选择、缺失的卡面/评级字段、`collectionAdviceTag`、`collectionAdviceText`，以及 PG 无可用成交明细时由 LLM 生成的价格曲线。如果向量结果已可靠确定商品，第二次调用只补齐 PG 缺失字段且不得改变 productId；如果商品依赖 LLM 才能确定，服务端必须在前置 category 范围内按候选或卡号+系列查表复核。

两个 intent 都不得访问 JustTCG 或其它外部价格 API；参考 YML 中已有的 JustTCG 节点和连接必须移除或禁用。`recognize_enrich` 只有在输入明确表明 PG 无可用 `priceTrend` 时才让 LLM 生成价格曲线，PG 已提供可用成交明细时必须跳过生成。商品字段按第 6.5 节逐项合并，不再错误地把 PG 整个对象或 LLM 整个对象一次性覆盖另一方。OCR、候选、卡片文字和外部产品描述统一视为不可信资料，不能让它们覆盖工作流规则。

网关使用 `DIFY_BASE_URL`（包含 `/v1`）、`DIFY_API_KEY` 和工作流版本标记。流程为 `/files/upload` 获取 file id，再分别调用 `/workflows/run`；同一次请求的上传和两次运行使用同一 user 和同一已上传图片，避免重复上传。只在 `data.status=succeeded` 时解析 `data.outputs.result`，两个 intent 分别使用严格 Pydantic schema。[上传文件](https://docs.dify.ai/en/api-reference/files/upload-file)、[运行工作流](https://docs.dify.ai/en/api-reference/workflow-runs/run-workflow)

第二次调用失败时按商品身份是否已经可靠确定降级：已确定则返回已有 PG 字段和 PG 价格，缺失字段置空并记录 warning；未确定则保留候选并返回 `monitor.status_match=candidates/unrecognized`。PG 无价格且 LLM 曲线生成失败时只返回空 `priceTrend`，不能推翻已有商品匹配。单次 intent 调用不盲目自动重发，避免重复计费；总 deadline 必须为两次调用、模型和数据库预留明确预算。开发环境可以以 Dify mock 运行测试，但生产 readiness 必须把 Dify classify 能力视为必需项。Dify 密钥只在 secret/environment 中配置；生产分支禁止关闭 TLS 证书校验，参考 YML 中的占位密钥和不安全证书回退不得沿用。

`monitor.dataSource` 只表示最终商品身份来源。前置 classify 必然调用但不计入 `llm`；后置调用仅补字段、生成评级/收藏建议或价格曲线时也不计入。只有第二次调用实际确认商品身份并通过 PG 查表复核时才使用 `llm/visual_llm/text_llm/visual_text_llm`。`monitor.status_match` 独立表达 `matched/candidates/recognized_no_db/unrecognized/not_a_card`；`price_source` 表达 `pg_sales/llm_generated/none`；`field_sources` 逐字段表达 `pg/pg_derived/dify_classify/dify_enrich/llm_generated/system/none`。此外 monitor 统一承载 request/version、warning、总耗时和分阶段耗时，避免混合来源无法追踪。

### 9.1 实现改动位置

对外路由和字段名不新增 `intent`；内部改动集中在下列位置，实施时按现有职责做最小调整：

| 位置 | 需要调整的内容 |
|---|---|
| `app/main.py` | 保留 `/v2/recognize/serial`、`/v2/recognize/fusion` 和兼容别名；完成 `image/text/category/confidence` 输入适配、图片来源校验，以及 classify 故障的 HTTP 503 映射。 |
| `app/models/schemas.py` | 增加严格的 classify/enrich 内部 schema，并把对外响应调整为稳定的 `text + priceTrend + monitor`；匹配枚举放到 `monitor.status_match`，不把内部 intent 或旧匹配 `status` 暴露到顶层业务响应。 |
| `app/services/dify_service.py` | 将现有单一 `recognize()` 拆为一次图片上传和两次按 intent 运行；复用 file id，分别校验输出，并区分必需的 classify 故障与可降级的 enrich 故障。 |
| `app/matching/orchestrator.py` | 调整为“classify → category 限域 → serial/fusion 匹配 → PG 查表/价格 → 计算缺失字段 → enrich → 逐字段合并 → 组装响应”，并生成 `status_match/dataSource/price_source/field_sources`。 |
| `app/repositories/catalog.py`、`app/repositories/pg_catalog.py` | 增加商品详情、`marketPrice`、逐笔 `price_sales` 和价格覆盖信息查询；`priceTrend` 返回纯 `purchasePrice`。 |
| `app/importing/prices.py`、新增数据库 migration | 在不破坏现有价格快照的前提下导入 sales 明细和 coverage；以来源批次和数组行号保证幂等并保留真实重复成交。 |
| `app/config.py`、`app/bootstrap.py` | 增加 Dify 工作流版本、超时和图片白名单等配置；生产环境缺少 classify 所需配置时 readiness 不通过。 |
| 参考 Dify Workflow YML | 开始节点增加内部 `intent` 并分出 `classify`、`recognize_enrich`；移除/禁用 JustTCG 节点，PG 无曲线时由 LLM 生成；清除不安全 TLS 回退和明文/占位密钥。 |
| `tests/` | 覆盖接口字段不变、两种策略、两次 intent 顺序、分类业务拒绝/系统故障、PG/LLM 逐字段优先级、纯 `purchasePrice`、LLM 曲线校验且不混合、`status_match` 与 `dataSource` 全枚举。 |

## 10. 公平对比与验收

先实现 serial 基线，再基于相同服务实现 fusion。相同标注请求逐一跑两版，固定 gallery、OCR、model、预处理、K、规则及 Dify 版本。先冻结相同接受 profile 比较策略调度，再在独立 calibration 集各自调优，报告同等自动接受精度下的覆盖率；不能把不同阈值的结果归因于并行本身。

测试集按卡身份/重复图组切分 calibration 和 held-out，同一卡不同拍照角度不得跨集合泄漏。按品类、语言、OCR 有/无/噪声、全品类/指定品类、相似版本、库外卡/非卡分层；真实照片是主验收依据，标准图自检只证明索引关联，不能证明 95% 识别准确率。

| 指标 | 定义/要求 |
|---|---|
| ANN Recall@50 | 对照相同模态精确 Top-50；建议验收目标 ≥99%，逐品类报告，不等于卡牌识别准确率 |
| Top-1 / Recall@5 / MRR | LLM 前与最终分别统计，唯一身份与重复图等价组分开 |
| 自动接受精度 | 正确自动 matched / 全部自动 matched；建议目标 ≥95%，报告样本数和区间 |
| 自动接受覆盖率 | 自动 matched / 有效库内请求；与精度一起报告，避免全拒绝也过关 |
| 纠错与损伤 | serial 错→fusion 对，以及 serial 对→fusion 错的逐例统计 |
| 幻觉/错误接受 | 库外/非卡误接受率、身份错误、跨品类逃逸；跨品类逃逸必须为 0 |
| 接口状态契约 | 顶层 `status` 不承载匹配枚举；五种 `status_match` 与 `text.state/stateErrorReason/productId` 组合全部按契约测试 |
| 字段与价格溯源 | 有效 PG 字段不被 LLM 覆盖、缺失字段才补齐；`field_sources/price_source` 与真实路径一致；PG 与 LLM 曲线零混合 |
| 资源与耗时 | 无 LLM/含 LLM 的 p50/p95/p99、队列时间、CPU 秒/请求、RSS、QPS、BGE/LLM 调用比例 |
| 导入 | 幂等、断点恢复、价格单独更新不编码、模型不匹配拒绝、发布/回滚可追溯 |

离线精度对比可保存共用 LLM 响应，按 intent、图片/OCR/范围/实际候选输入/工作流版本完整 key 缓存；输入不同不能错误共用。实时端到端延迟试验独立运行，不混入回放缓存。线上每个有效 TCG 请求正常执行前置 classify 和后置 recognize_enrich 两次工作流运行；上传图片应在同一请求内复用，监控必须分别记录两次调用耗时、状态和失败原因。

fusion 能在预先约定的资源预算内，保持同等自动精度并增加覆盖率/纠错收益才考虑成为默认；若未证明收益，仍保留两个 API，旧别名继续 serial。目标机参数和验收标签不足时只能称“可运行”，不能称“已达到 95%”。

## 11. 不确定项及关闭方式

无法用本地源码核实尚未交付的服务器、数据包和外部工作流；以下是验收门槛，不是已解决事实，也不阻塞纯规则和接口开发。

| 编号 | 已确定部分 | 尚需核实的证据 | 关闭时点/负责方 |
|---|---|---|---|
| U1 | 完整数据离线上传，约 36 万 | 正式包路径/品类映射/图片主图规则/有效行统计 | T1/T3，用户提供包，开发产 manifest 校验结果 |
| U2 | CPU-only 单机，GPU 预留 | CPU 型号、核数、RAM、SSD 空间和业务并发/延迟要求 | T9/T10，用户提供主机信息后压测 |
| U3 | 本地 BGE 与 demo DINO | 上线模型包完整文件、哈希、DINO backend 与断网加载结果 | T2，开发核对，用户上传服务器 |
| U4 | GPT-5.5 经同一个 Dify Workflow 两次调用，内部 intent 为 classify/recognize_enrich | 改造后的已发布参数、两个分支结构化输出、LLM 价格曲线 schema、Vision 能力和真实输出 | T6，开发按参考 YML 改造并联调；密钥不写文档 |
| U5 | 已核对 sales 样例含 purchasePrice/shippingPrice/orderDate，响应取纯 purchasePrice | 正式数据币种、批次重叠和时间窗覆盖程度；LLM 曲线仅为估计 | T3，导入报告记录 coverage；不完整批次不得宣称完整历史，LLM 曲线必须带来源 warning |
| U6 | 两 API 公平比较 | 按品类/语言覆盖的真实照片标注、可接受精度/覆盖率和延迟 | T10，用户标注/确认业务目标，开发统计 |
| U7 | 本地规范为英语 BGE | 非英语 OCR 在正式数据上的实际贡献 | T10 分层评估；首版保持保守禁用密集文本强证据 |

开发按配套计划推进；只有相应外部联调、全量导入与验收步骤需要这些材料。设计变更在本文件记录，执行任务状态在配套计划记录，不为尚未测出的参数伪造结论。
