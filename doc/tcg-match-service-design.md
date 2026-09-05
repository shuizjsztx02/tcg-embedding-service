# TCG 单机双策略识别服务：技术方案

日期：2026-09-05。状态：可审阅的设计基线；本次交付仅为文档，尚未实施或完成服务器验收。

配套执行文档：[分步骤实施计划](tcg-match-service-implementation-plan.md)。本方案取代根目录 `tcg-match-service-plan.md` 中与本次要求冲突的规划；原文件保留为历史输入。历史文档中的任务和操作命令不视为本次实施授权。

## 1. 结论与范围

同时提供串行补救与并行融合两个 API，技术上可行。并行版有机会纠正视觉高分误匹配，也会额外消耗 CPU，且可能被错误 OCR 干扰；准确率和延迟改善是需要验证的假设。

生产采用 FastAPI + PostgreSQL/pgvector，单服务器、单 API 实例、默认 CPU-only。DINOv2 编码图片，本地 BGE 编码标准卡文本及客户端 OCR；两种向量分别建库检索，通过共同产品键融合结果。原始图片和 JSONL 保存在挂载的数据目录，数据库存规范化字段、原始 JSONB、价格数据和两种向量。FAISS 保留为离线精确检索基准。

首版包括：可复用导入命令、本地优先模型加载、全品类/单品类检索、两版识别 API、客户端 OCR 辅助重排、Dify GPT-5.5 兜底、卡牌查表及价格查询、离线对比与 CPU 压测。服务器 OCR、前置 LLM 品类判断、多实例、Redis、多级缓存、训练新模型和分布式向量库不在首版范围内。

## 2. 已核实事实与实际缺口

代码核对对象是 `tcg-match-service/`，根目录 `app/` 只用来核对 demo 模型。未运行 Docker 构建、全量模型推理或线上 Dify 请求。

| 项目 | 证据/现状 | 本次处理 |
|---|---|---|
| 框架和向量库 | `app/main.py` 为 FastAPI；`services/index_service.py` 从 NPY 加载 FAISS IndexFlatIP | 复用 API 组织方式，改由 PG 保存业务和向量数据 |
| 串行链路 | `routes/recognize.py` 为品类 LLM → DINO → 高分返回/LLM；OCR 入参没有参与匹配 | 补齐图像 → OCR 文本召回重排 → LLM 查表 |
| 品类 | 缺少合法 `category_hint` 会调用 LLM | 未指定品类时直接全库；未知品类报错，不猜测或自动扩类 |
| OCR | `main.py` 启动 PP-OCR，`routes/ocr_match.py` 识别上传图片 | 从生产启动与依赖中移除，OCR 由客户端提供 |
| DINO | demo 和服务调用 `dinov2_vitb14`；备用 `facebook/dinov2-base` | ViT-B/14、无 registers、768 维；它是特征提取器，不是 GroundingDINO 检测器 |
| DINO 输出适配 | 当前直接对 `model(x)` 调用 `.dim()`，Transformers 的输出对象不支持此用法 | 显式适配 tensor / `last_hidden_state[:, 0]`，不盲目替换后端 |
| BGE | 本地 README 标识 `bge-small-en-v1.5`；config hidden_size=384，CLS pooling，max_seq_length=512 | 以用户提供的整个 `script_temp/bge_model` 包为基线，并记录文件指纹 |
| BGE 一致性 | 查询读本地包，构建脚本重新从网上加载模型 | 离线和在线使用同一加载器、tokenizer 与模型版本 |
| ID | 样例 `productId=100009.0`；在线用 `str(productId)`，文本构建用 `str(int(productId))` | 修复 `100009.0` 与 `100009` 关联失败问题 |
| 导入 | `scripts/build_index.py` 按品类重新加载模型、一次性收集数据；无版本发布和断点协议 | 流式、分批、可恢复、可复用 embedding |
| 启动 | `entrypoint.sh` 启动前自动建索引，忽略传入的构建命令；在线挂载 `/data:ro` | 启动只加载已发布数据；导入使用独立一次性命令 |
| LLM | 当前调用 Anthropic 风格 `/v1/messages`，默认 qwen 配置 | 换为 Dify 工作流调用，模型在 Dify 中固定 GPT-5.5 |
| 当前数据 | 47 个 products.jsonl，逐行计数 364,136，合计 745,649,639 字节 | 这是物理行数，不代表去重后的有效卡数或图片数 |
| 价格样例 | `prices/03_Pokemon.jsonl` 每行一个产品及 sales 数组 | 按价格数据单独建模，不塞进 embedding 文本 |

前次对话中“每个产品文件只有一行”是统计方法错误，已更正。正式导入以用户另行上传的完整数据包为准，目录名称可以不同。本次未收到可读取的 Image #1 / Image #3，价格设计依据实际 JSONL 样例，不假称核对过截图。

## 3. 两种策略的价值与边界

| 维度 | serial：串行补救 | fusion：并行融合 |
|---|---|---|
| 开始 | 图片编码/召回 | 有可用 OCR 时图片、文本两路一起调度 |
| 图片可信 | 可直接命中，省掉 BGE | 等两路完成后联合判断 |
| 图片低分 | 有 OCR 才执行文本补救 | 已有两路候选可重排 |
| 高分但认错 | 可能提前结束；轻量卡号冲突规则可拦截部分情况 | OCR 有机会纠错，也可能干扰原本正确的结果 |
| 无 OCR | 视觉 → 必要时 LLM | 同一视觉 → 必要时 LLM，结果语义一致 |
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

三个识别入口采用相同 multipart 参数：

- `file`：必填，客户端已裁切、透视矫正、方向校正的单卡图；最大 10 MiB、解码后最大 20MP，拒绝动画/多帧和损坏图。
- `ocr_text`：可选，空白等于未传；最大 8,192 字符。客户端 OCR 不可信，不能成为系统指令。
- `category`：可选，注册的稳定品类代码；空值表示全品类。合法但不匹配时仍只查该品类，不静默搜索其它品类。
- `ocr_lang`：可选语言提示，不作为强制品类过滤条件。
- `category_hint`：兼容旧参数；与 category 同传且不同返回 400；旧别名不再表示“允许 LLM 改写的建议”。

未知 category 返回 400，缺必填项返回 422，过大输入返回 413，服务未就绪/队列已满返回 503。内部召回 K 默认 50，最终最多 5 个候选；K 不向客户端开放，保证实验配置可追溯。

两版统一返回现有 `status/decision_path/category/product_id/product/price/candidates/identity/confidence/scores/warnings/latency_ms`，新增 `request_id/strategy/dataset_version/model_version/decision_version/timings_ms`。候选必须包含 category 和 product_id；不假设 product_id 跨品类唯一。

`confidence` 首版为 null；`scores` 单独携带 visual_cosine、text_cosine、fusion_score、margin、ocr_used 和冲突证据。规则门限不是概率；如后续引入概率校准，必须附校准版本及可靠性评估。`ocr_used` 表示实际使用 OCR 规则或文本证据，另用 `text_retrieval_used` 区分是否调用 BGE。

| status | 含义 |
|---|---|
| matched | 已确定且有库内记录，product_id 不为空 |
| candidates | 存在多个或证据不足的候选，不自动报成命中 |
| recognized_no_db | LLM 提取了身份，经过限定范围查表无命中；身份与 DB 数据分开展示 |
| unrecognized | 无足够身份或候选；LLM 失败可以返回此状态并附 warning |
| not_a_card | 仅有明确的兜底识别依据时返回；低向量相似度本身不能证明不是卡 |

基础设施故障用 HTTP 503；LLM 故障是可降级故障，保留检索候选。匹配 ID 有而业务记录缺失属于数据完整性故障，禁止返回 matched。

## 5. 共同候选与决策逻辑

### 5.1 召回范围与证据

请求进入时固定数据版本和品类范围；两路、LLM 查表、价格查询都使用该版本。未指定 category 时覆盖该版本全部品类，禁止先按预测品类缩小范围。结果中的 category 来自候选记录。

视觉/文本各取前 K，另提取 OCR 的卡号、系列代码及名称线索。按 `(category_id, product_id)` 合并，最多 `2K + 5` 个候选；OCR 精确身份查表超过 5 个结果时标为歧义，不任取一个。

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
输入校验与固定数据范围 → DINO 编码/召回
  → 视觉接受规则通过（可含轻量 OCR 身份冲突拦截）→ matched
  → 否则：有可用 OCR → BGE 编码/召回 + OCR 身份查表 → 合并重排
      → 接受规则通过 → matched
      → 否则 → LLM 识别 + 查表 → matched / candidates / recognized_no_db
  → 无可用 OCR：跳过 BGE，按必要性进入同一 LLM 兜底
```

高视觉分支不启动 BGE；轻量 OCR 字段解析不等于调用 OCR 模型或文本 embedding。无校准 profile 时不提前自动命中。

### 5.5 fusion 流程

```text
输入校验与固定数据范围
  → 有可用 OCR：并发调度 DINO 编码/召回 与 BGE 编码/召回
  → OCR 不适合 BGE：视觉召回 + 可用身份规则
  → 合并候选 → 加权 RRF → 共同接受规则
  → 仍不确定：同一 LLM 识别 + 查表
```

有可用文本时不得先看到视觉高分就提前返回，否则实验没有检验融合纠错。文本路失败时退为视觉规则，记录降级，候选不丢失。视觉编码/主检索不可用视为核心故障并返回 503。无 OCR 时复用 serial 的视觉分支，除 strategy 和计时外结果应相同。

## 6. 数据库选择与数据结构

PG+pgvector 可把卡信息、价格及向量置于同一事务体系；PG+FAISS 多一份索引同步协议，PG+Qdrant/Milvus 多一套数据库运维。以单机、36 万、低更新频率约束选择前者。

初版使用 float32 的 `vector(768)` 与 `vector(384)`，采用 HNSW 余弦索引。pgvector 支持这两个维度，近似索引牺牲部分召回率；索引召回率需要对照精确检索测量。[pgvector 官方说明](https://github.com/pgvector/pgvector)

### 6.1 版本组织

`public.dataset_releases` 保存 release UUID、schema_name、manifest_hash、model_fingerprint、状态和统计；`public.active_dataset` 为单行发布指针；`public.import_checkpoints` 保存各文件的哈希、字节偏移和已完成批次。

每个待发布数据版本写入独立 `ds_<uuidhex>` schema，验证完成后通过小事务切换指针；正在处理的请求继续使用进入时固定的旧 schema。版本发布后只读；首版保留当前和前一版本，清理使用显式运维命令、备份和无活跃请求检查，不自动删除原始文件。连接池查询必须使用注册表给出的 schema 并进行 SQL identifier 引用，不能把客户端字符串作为 SQL 标识符。

### 6.2 每个版本中的表

| 表 | 主键/主要字段 | 索引与职责 |
|---|---|---|
| categories | category_id、stable_code、display_name、source_mapping | stable_code 唯一，目录名只是路径 |
| cards | (category_id, product_id)、name、set_id/name/code、number_norm、raw_json、source_hash、text_hash | 主键；(category_id,set_code,number_norm)；名称规范化索引 |
| card_images | (category_id, product_id)、relative_path、sha256、width/height、orientation_policy、duplicate_group | FK cards；首版每卡一个明确的主标准图 |
| visual_embeddings | (category_id, product_id)、embedding vector(768)、model_version、input_hash | FK cards；按 category_id LIST 分区、每分区 HNSW |
| text_embeddings | (category_id, product_id)、embedding vector(384)、model_version、doc_version、input_hash | 同上，图片缺失不妨碍文本入库 |
| price_snapshots | (category_id,product_id,captured_at,currency)、market/lowest/median 等、source_metadata | 保存产品 JSON 中的价格快照，不伪装为逐日历史 |
| price_sales | (category_id,product_id,source_batch,row_no)、order_date、purchase_price、shipping_price、condition、variant、language、quantity、currency | (category_id,product_id,order_date)，保存成交明细和来源 |
| price_coverage | (category_id,product_id,source_batch)、min_date、max_date、total_results、loaded_count、complete | 表示抓取覆盖范围和是否完整 |

价格金额用 NUMERIC，时间用 TIMESTAMPTZ，ID 用 BIGINT；解析 JSON 时用 Decimal 校验 ID 必须是正整数，拒绝非整数和越界值，API 中输出 ID 字符串。raw_json 保留所有原始属性，但变动价格、SKU 品相清单不进入文本向量。

图像文件名通过 manifest 规则映射 product_id；默认可支持 `{product_id}.jpg` / `{product_id}_200w.jpg`，多个文件同时匹配必须明确主图规则。横版真实设计与拍摄旋转不能混为一谈：manifest 指定 `preserve` 或 `portrait_rotate_cw`，保持离线/在线模型输入策略可追溯，不自动把所有横图旋转。

### 6.3 品类过滤与全品类检索

按品类分区是为了让指定品类在对应分区内 ANN 检索，不采用全局 ANN 先取 50 再用 Python 筛品类。全品类查询在分区父表上按距离排序取全局 K，由 PostgreSQL 合并各分区候选；这不是一个跨分区的物理 HNSW 索引。用 EXPLAIN 验证实际计划、分区裁剪和返回数量，不假设数据库一定选择理想计划。

初始 `m=16, ef_construction=64, ef_search=100`，以 Recall@50 和延迟调参。pgvector 的 ANN 附加过滤可能减少结果数，0.8+ 可采用 iterative scan；本方案仍对少结果/小品类提供同一范围精确检索回退。[过滤说明](https://github.com/pgvector/pgvector#filtering)

### 6.4 价格导入与曲线

当前 sales 样例没有稳定成交 ID。同一交易字段哈希不能证明是同一笔交易，不能简单按价格+时间去重，避免抹掉真实重复成交。首版按“产品+来源时间窗快照”替换对应窗内明细，保留数组中的重复行及 row_no；同一文件/版本重复导入幂等。

替换前要求 manifest 声明数据代表该时间窗的快照，并记录抓取完整性。只有完整窗口允许覆盖旧明细；不完整抓取保留原始批次和 coverage，不更新正式曲线表。当前样例 `totalResults` 与 `count` 不相等，不能声称完整历史。将来拿到成交唯一 ID 后才可切到逐笔 upsert。

曲线端点按 UTC 日聚合 `SUM(purchase_price*quantity)/SUM(quantity)`，必须按 currency、condition、variant、language 分系列；运费单独返回，不默认混入价格。可筛单系列，未筛时返回多系列；无成交日不补零。金额/currency 缺失的记录不得默认填 USD 后参与聚合，币种由来源 manifest 明确给定。真实价格表与截图若不同，在导入适配任务核对，不改识别核心。

## 7. 原始包与可复用导入协议

用户把原始包解压到 `/data/raw/<source_version>/`；目录可以不同。自动发现器只提出映射，正式导入读 `manifest.json`：

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

执行过程：discover → validate → stage cards/prices → encode changed inputs → build indexes → verify → publish。独立 CLI 存放 `tcg-match-service/script_temp/import_data.py`，各阶段可恢复，模型只加载一次。源码与临时脚本遵循仓库位置规则，运行结果放 `/data/imports/`，向量缓存放 `/data/index/`。

- 校验 UTF-8/JSON、ID、重复主键、类别映射、相对路径和源文件哈希；路径不得越出数据根。只逐批打开图片，不把全图库读进内存。
- 缺图/坏图记录 quarantine，基础信息仍可入库；向量禁止写零值占位。发布要求所有异常都有归因统计，不能默默跳过。
- checkpoint 与批次事务一起提交；中断后从已确认位置续跑。源文件哈希改变不能按旧偏移续跑。
- 对未变化的图片哈希/文本 hash 及相同模型指纹复用旧向量；只修改价格不重新推理。
- `upsert` 默认保留输入中未出现的旧产品；`replace --scope <category...>` 才在新版本中移除指定范围缺失产品。范围外数据从旧版本继承，禁止残缺包误删全库。
- 全量替换仍生成新版本；失败不影响 active_dataset。没有发布动作，服务继续查旧版本。
- 图片路径绑定不可变 raw/source_version。原始包应写入新目录后发布，不能在旧请求仍使用时原地覆盖标准图。
- 模型/文本模板/预处理变化需要新版本重建相关向量；CPU↔GPU 变化只有通过数值一致性回归才允许复用。
- 样例图、JSONL、价格、索引、权重、自动生成报告均本地留存并加入忽略；合成测试数据在测试代码中生成，不提交数据集。

## 8. 模型与 CPU/GPU 部署

DINO 基线固定 `dinov2_vitb14`、输入 RGB resize `(168,224)`（W,H）、bicubic、ImageNet mean/std、CLS 768 维、L2 归一化。客户端负责几何预处理；服务做解码、EXIF 处理和模型张量转换，gallery/query 共用转换函数。[DINOv2 官方模型列表](https://github.com/facebookresearch/dinov2)

优先提供与 demo 一致的 Torch Hub 包：本地源码目录、权重和 commit/hash 清单齐全；从本地创建架构 `pretrained=False` 后加载本地权重，不能本地源码仍隐式下载权重。仅在本地缺失且 `ALLOW_MODEL_DOWNLOAD=true` 时下载同一固定版本到可写缓存，完成后加载。文件存在但损坏/指纹错误时明确失败，不静默换模型。

若交付包选用 HF 的 `facebook/dinov2-base`，由显式 backend 配置加载，统一适配 CLS 输出，并对照 demo 小样本校验；不把 Torch Hub 权重直接当 HF 目录，也不把相同维度当数值等价。HF 后端启用前完成相同输入的余弦及 top-K 回归，失败则重建并重新校准。

BGE 挂载 `/models/bge_model`，文档编码不加查询指令，OCR 查询加现有 prefix；正文按名称、卡号、系列、类型、描述/技能的确定顺序生成，去 HTML，列表稳定展开，保留关键身份字段，超出 512 tokens 时截断尾部。模板是跨品类通用字段加少量明确字段映射，不沿用只有宝可梦 HP/攻击的文本布局。

生产为一台主机上的 API 和 PostgreSQL 两个容器，不代表两个 API 实例；Uvicorn workers=1。`DEVICE=cpu` 默认，`cuda` 必须有可用 GPU，否则启动报配置错误；兼容已有 USE_GPU 参数并明确映射。模型文件只读挂载 `/models`，下载缓存单独可写挂载 `/model-cache`。GPU 使用独立镜像/Compose override 切换相同代码；CPU 镜像使用 CPU torch 依赖，不安装 PaddleOCR。

并发由有界请求队列和共享 CPU 工作池控制。起始最多 2 个识别请求、2 个模型作业并发，每模型同时最多 1 次调用；DINO/BGE 可在不同线程执行。torch intra-op 起始 2、interop 1，并协调 BLAS/OMP 线程限制；这是试验初值，不能在请求处理中反复修改全局线程数。同步模型与数据库工作不阻塞 ASGI 事件循环。每条并发 SQL 使用自己的连接，池上限起始 6。

总请求预算起始 60s；排队最多 1s；SQL statement_timeout 起始 2s；LLM 上传+执行总预算不超过剩余时间且最多 45s。模型线程超时不代表底层计算已经停止，作业槽位必须保持到实际结束，避免虚假释放导致超卖；记录排队/推理/SQL/重排/LLM 各阶段。

36 万条双向量的 float32 元素约 1.545 GiB；这不包括表、HNSW、JSON、价格、WAL 和双版本。采购参考起点为 8 vCPU / 32 GiB RAM / SSD，尚未获得目标服务器配置，不能承诺 8 GiB 容器限制足够。磁盘按实测图片体积 + 至少两个 DB 版本 + WAL/备份余量计算。全量导入先跑 1,000 张采样实测再估计，时间公式为图片数/实测吞吐+文本编码+写库/建索引，不承诺几小时完成。

## 9. Dify GPT-5.5 兜底与查表

两个策略共用一个已发布 Dify Workflow。网关传入图片、OCR、限定品类范围、候选摘要；Dify 只输出身份/候选选择依据，价格及库内 ID 的真实性由服务端验证。GPT-5.5 在 Dify 模型节点配置，工作流 API 请求不通过随意增加 model 字段选择模型。

网关使用 `DIFY_BASE_URL`（包含 `/v1`）、`DIFY_API_KEY`、工作流版本标记。流程为 `/files/upload` 获取文件 id，再 `/workflows/run`；上传和运行的 user 必须一致。使用 `inputs.card_images` 数组型图片输入，绑定实际发布工作流参数；候选 JSON 作为普通字符串字段传递。只在 `data.status=succeeded` 时解析 `data.outputs.result`。[上传文件](https://docs.dify.ai/en/api-reference/files/upload-file)、[运行工作流](https://docs.dify.ai/en/api-reference/workflow-runs/run-workflow)

输出 result 的业务契约：`is_card:bool|null, card_name:str|null, set_name:str|null, set_code:str|null, card_number:str|null, category:str|null, language:str|null, selected_product_id:str|null`。拒绝未知类型、非白名单品类和无库中记录的指定 ID；selected_product_id 只是建议，仍需身份核对。OCR、卡片文字和外部产品描述统一当不可信资料，不能让它们覆盖任务规则。

服务端按 category/set/number/name 的规范化索引查表，唯一且身份证据充分才能 matched；仅名称模糊匹配或一个卡号均返回候选。指定品类请求始终限定该范围；全库请求可把 LLM 提供的已注册品类作为兜底查表证据，不影响之前的全库向量召回。

默认每请求只发起一次工作流执行，超时不盲目重发计费调用；连接失败、429、schema 错误均记录原因并降级为原候选。没有 Dify 配置可运行检索开发环境，readiness 标记 llm_degraded；上线全功能验收必须用目标工作流做真实样例联调。密钥只在服务器环境/secret 中配置。

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
| 资源与耗时 | 无 LLM/含 LLM 的 p50/p95/p99、队列时间、CPU 秒/请求、RSS、QPS、BGE/LLM 调用比例 |
| 导入 | 幂等、断点恢复、价格单独更新不编码、模型不匹配拒绝、发布/回滚可追溯 |

离线精度对比可保存共用 LLM 响应，按图片/OCR/范围/实际候选输入/工作流版本完整 key 缓存；输入不同不能错误共用。实时端到端延迟试验独立运行，不混入回放缓存。线上不自动为一个请求调用两次 LLM；评测由调用方明确请求两个接口。

fusion 能在预先约定的资源预算内，保持同等自动精度并增加覆盖率/纠错收益才考虑成为默认；若未证明收益，仍保留两个 API，旧别名继续 serial。目标机参数和验收标签不足时只能称“可运行”，不能称“已达到 95%”。

## 11. 不确定项及关闭方式

无法用本地源码核实尚未交付的服务器、数据包和外部工作流；以下是验收门槛，不是已解决事实，也不阻塞纯规则和接口开发。

| 编号 | 已确定部分 | 尚需核实的证据 | 关闭时点/负责方 |
|---|---|---|---|
| U1 | 完整数据离线上传，约 36 万 | 正式包路径/品类映射/图片主图规则/有效行统计 | T1/T3，用户提供包，开发产 manifest 校验结果 |
| U2 | CPU-only 单机，GPU 预留 | CPU 型号、核数、RAM、SSD 空间和业务并发/延迟要求 | T9/T10，用户提供主机信息后压测 |
| U3 | 本地 BGE 与 demo DINO | 上线模型包完整文件、哈希、DINO backend 与断网加载结果 | T2，开发核对，用户上传服务器 |
| U4 | GPT-5.5 经 Dify Workflow | API 地址/密钥、已发布参数、图片变量、Vision 能力和真实输出 | T6，用户提供部署环境，开发联调；密钥不写文档 |
| U5 | 本地 sales 样例存在 | 正式价格格式、币种、时间窗完整性；截图未收到 | T3，用户提供样例/来源声明；不完整数据只作原始保留 |
| U6 | 两 API 公平比较 | 按品类/语言覆盖的真实照片标注、可接受精度/覆盖率和延迟 | T10，用户标注/确认业务目标，开发统计 |
| U7 | 本地规范为英语 BGE | 非英语 OCR 在正式数据上的实际贡献 | T10 分层评估；首版保持保守禁用密集文本强证据 |

开发按配套计划推进；只有相应外部联调、全量导入与验收步骤需要这些材料。设计变更在本文件记录，执行任务状态在配套计划记录，不为尚未测出的参数伪造结论。
