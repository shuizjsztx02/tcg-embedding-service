 # TCG 卡牌识别方案 V1.0 — Demo 实现文档
 
 > 版本: 1.0 | 最后更新: 2026-08-28
 > 对应代码: `app/main.py` + `script_temp/` 工具脚本
 
 ---
 
 ## 1. 项目概览
 
 宝可梦卡牌视觉 + 文字双模匹配服务。用户上传真实拍摄的卡牌照片，服务通过两条独立链路进行匹配：
 
 - **链路一（视觉匹配）**：DINOv2 提取图像 embedding → faiss 检索 `pokemon-index` → 返回最佳匹配或拒绝
 - **链路二（OCR + 文字匹配）**：PP-OCRv4 识别卡面文字 → BGE-small-en-v1.5 提取文本 embedding → faiss 检索 `text-index` → 返回商品信息
 
 ### 1.1 核心数据
 
 | 数据源 | 数量 | 说明 |
 |--------|------|------|
 | `category_cards_search/03_Pokemon/images/` | 28,378 张 | 英文卡牌 200px 缩略图，格式 `{productId}_200w.jpg` |
 | `category_cards_search/03_Pokemon/products.jsonl` | 28,378 条 | 商品元数据（productId, productName, rarityName, setName, customAttributes 等） |
 | `category_cards_search/85_Pokemon_Japan/images/` | 27,182 张 | 日文卡牌缩略图（暂未使用） |
 | `test-images/` | ~4,187 张 | 真实拍摄的测试照片 |
 | `images/` | 9,434 张 | 旧基线数据（已废弃） |
 
 ### 1.2 三套索引
 
 | 索引 | 路径 | 向量数 | 维度 | 模型 | ID 格式 | 用途 |
 |------|------|--------|------|------|---------|------|
 | **pokemon-index** | `pokemon-index/` | 28,378 | 768 | DINOv2 ViT-B/14 | `{productId}_200w` | 视觉匹配主索引 |
 | **text-index** | `text-index/` | 29,408 | 384 | BGE-small-en-v1.5 | `{productId}` | 文字匹配索引 |
 | ~~旧 index~~ | `index/` | 9,434 | 768 | DINOv2 ViT-B/14 | `{card_id}` | 基线索引（已废弃） |
 
 **索引关联关系：**
 - `pokemon-index` 的 id 格式为 `{productId}_200w`，去掉 `_200w` 后缀即对应 `products.jsonl` 中的 `productId`
 - `text-index` 的 id 直接就是 `productId`
 - 两个索引通过 `productId` 关联：28,378 个 `productId` 完全重叠，`text-index` 多出 1,030 个（有商品信息但无对应图片）
 
 ### 1.3 启动时加载内容
 
 | 加载项 | 耗时 | 说明 |
 |--------|------|------|
 | DINOv2 ViT-B/14 | ~10s | torch.hub.load 或 transformers 兜底 |
 | pokemon-index (28,378 × 768) | ~1s | faiss IndexFlatIP |
 | PP-OCRv4 检测 + 识别模型 | ~3s | PaddleInference, 2 threads |
 | BGE-small-en-v1.5 | ~5s | SentenceTransformer, CPU |
 | text-index (29,408 × 384) | ~0.5s | faiss IndexFlatIP |
 | products.jsonl | ~0.5s | 加载为 dict[productId → product] |
 
 服务端口: **8056**
 
 ---
 
 ## 2. 系统架构总览
 
 ```
 ┌─────────────────────────────────────────────────────────────┐
 │                    FastAPI Server (port 8056)                │
 │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐ │
 │  │  /v1/match     │  │  /v1/search   │  │  /v1/ocr-match   │ │
 │  │  /v1/ocr       │  │  /v1/images   │  │  /v1/health      │ │
 │  └───────┬───────┘  └───────┬───────┘  └────────┬─────────┘ │
 │          │                  │                    │           │
 │  ┌───────▼──────────────────▼────────────────────▼─────────┐ │
 │  │                    预处理管线 (preprocess.py)            │ │
 │  │  EXIF矫正 → 卡牌检测(轮廓/Canny) → 透视校正 → 质量门控 │ │
 │  │  视觉: 504×704 (几何标准)  |  OCR: 882×1232 + 增强     │ │
 │  └──────────────────────────────────────────────────────────┘ │
 │          │                  │                    │           │
 │  ┌───────▼──────┐  ┌───────▼──────┐  ┌─────────▼──────────┐ │
 │  │  DINOv2       │  │  DINOv2      │  │  PP-OCRv4 + BGE   │ │
 │  │  IndexFlatIP  │  │  IndexFlatIP │  │  IndexFlatIP      │ │
 │  │  pokemon-index│  │  pokemon-index│  │  text-index       │ │
 │  └───────────────┘  └───────────────┘  └───────────────────┘ │
 └─────────────────────────────────────────────────────────────┘
 ```
 
 ---
 
 ## 3. 链路一：视觉匹配（DINOv2）
 
 ### 3.1 索引构建
 
 索引构建脚本：`script_temp/build_index.py`（旧基线）/ 手动构建 `pokemon-index`
 
 **pokemon-index 构建参数：**
 - 模型: DINOv2 ViT-B/14（87M 参数，768 维 CLS token embedding）
 - 输入尺寸: 168×224（ViT-B/14 patch 网格的倍数: 12×16 patches）
 - 归一化: ImageNet 标准 (mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
 - 索引类型: faiss.IndexFlatIP（暴力内积搜索，等价于余弦相似度，因为所有向量已 L2 归一化）
 - 构建耗时: 2,273 秒（~38 分钟，CPU）
 - 自检: 100 张随机图，top-1 命中率 100%
 
 ### 3.2 在线匹配流程
 
 ```
 用户上传图片
   │
   ▼
 文件校验 (大小 < 10MB, MIME image/*)
   │
   ▼
 orientation_candidates()  → 横图: ±90° 候选
                             竖图: 原图 + 180° 候选
   │
   ▼
 对每个候选:
   to_model_input() → resize 到 168×224
   embed_single()   → DINOv2 → 768-dim → L2 normalize
   faiss_index.search(k=3)
   │
   ▼
 取所有候选中最高分:
   top1_score, top1_idx, top2_score, top2_idx
   │
   ▼
 阈值判定:
   score >= TAU (0.775)  AND  margin (top1 - top2) >= MARGIN (0.02)
       ├── 通过 → status="matched", card_id, score, margin
       └── 拒绝 → status="rejected", score, margin
 ```
 
 **阈值来源：** 环境变量 `MATCH_TAU`（默认 0.775）和 `MATCH_MARGIN`（默认 0.02），通过 `script_temp/calibrate_quality_gates.py` 在真实照片上校准。
 
 ### 3.3 匹配结果去向
 
 - **`/v1/match`** → 返回 `MatchResponse`（`card_id` 格式为 `{productId}_200w`）
 - **`/v1/search`** → 返回 top-5 `SearchResult`，包含 `product_name` 和完整 `product` 对象
 - 前端可通过 `/v1/images/{card_id}` 获取匹配卡牌的缩略图
 
 ---
 
 ## 4. 链路二：OCR + 文字匹配
 
 ### 4.1 文字索引构建
 
 **text-index 构建参数：**
 - 模型: BAAI/bge-small-en-v1.5（33M 参数，384 维 embedding）
 - 数据源: `category_cards_search/03_Pokemon/products.jsonl`（28,378 条商品）
 - 索引类型: faiss.IndexFlatIP（384 维）
 - 构建耗时: 398 秒（~6.6 分钟, CPU）
 - 查询前缀: `"Represent this sentence for searching relevant passages: "`
 
 索引的文本来源为 `products.jsonl` 中的商品信息，包含 `productName`、`customAttributes.description`、`customAttributes.flavorText` 等字段的拼接。
 
 ### 4.2 OCR 匹配流程
 
 ```
 用户上传图片
   │
   ▼
 文件校验
   │
   ▼
 preprocess_for_ocr():
   EXIF矫正 → detect_card() → perspective_correct(882×1232) → enhance_ocr() → quality_gate
   │
   ▼
 run_ocr():
   numpy 转换 → OCRPreprocessor.preprocess() → PPOCRv4Engine.read()
   │
   ▼
 如果 text_blocks < 2 且启用 retry_180:
   旋转 180° → 重新 OCR → 取结果多的
   │
   ▼
 拼接 full_text
   │
   ▼
 query_text = "Represent this sentence for searching relevant passages: " + full_text
 text_model.encode(query_text, normalize_embeddings=True) → 384-dim
   │
   ▼
 text_index.search(k=5)
   │
   ▼
 查 products.jsonl 获取商品详情:
   product_id, product_name, set_name, number, rarity, has_image, product
   │
   ▼
 返回 OcrMatchResponse(results=[...])
 ```
 
 ### 4.3 纯 OCR 接口
 
 `/v1/ocr` 只做 OCR 不做匹配，返回 OCR 文本块和置信度。预处理使用 `preprocess_query()`（几何标准路径，504×704，无视觉增强）。
 
 ---
 
 ## 5. 预处理管线详解
 
 预处理模块 `preprocess.py` 是两条链路的共享基础，但输出尺寸和增强策略不同：
 
 | 步骤 | 视觉匹配 (504×704) | OCR 匹配 (882×1232) |
 |------|-------------------|-------------------|
 | EXIF 方向矫正 | normalize_orientation() | 同上 |
 | 卡牌检测 | detect_card() | 同上 |
 | 透视校正 | perspective_correct(504×704) | perspective_correct(882×1232) |
 | 边缘裁剪 | trim 1% 边界 | 同上 |
 | 视觉增强 | 无（几何标准） | enhance_ocr() |
 | 质量门控 | assess_quality() | 同上 |
 
 ### 5.1 卡牌检测策略 (detect_card)
 
 四级检测策略，前一策略成功则跳过后续：
 
 1. **Otsu 二值化** → 形态学闭运算 → 最大外轮廓 → 四边形近似
 2. **Canny 边缘检测**（三组阈值: 30/90, 50/150, 70/200）→ 膨胀 → 轮廓查找
 3. **最小外接矩形**（对 Otsu 最大轮廓做 minAreaRect）
 4. 全失败 → 返回 None，走全图 fallback
 
 **四边形有效性校验** `quad_is_plausible()`：
 - 凸四边形（叉积同号）
 - 长宽比 ≤ 1.7（卡牌标准 63:88 ≈ 1.40，允许透视畸变）
 
 ### 5.2 OCR 视觉增强 (enhance_ocr)
 
 保守策略，避免强增强导致笔画丢失：
 
 1. **灰世界白平衡** — 消除色偏，幅度限制在 0.85~1.15
 2. **Gamma 校正** — 向中间调亮度拉近，gamma 范围 0.7~1.4
 3. **CLAHE** — L 通道对比度受限直方图均衡（clipLimit=2.0, grid=8×8）
 4. **双边滤波** — 去噪保边（d=7, sigmaColor=50, sigmaSpace=50）
 5. **轻度 USM 锐化** — 1.2 强度，-0.2 负片
 
 ### 5.3 质量门控 (assess_quality)
 
 | 指标 | 阈值 | 触发条件 | 说明 |
 |------|------|----------|------|
 | 模糊度 (Laplacian var) | < 150 | 警告 | 基于 60 张真实照片 p5=159 校准 |
 | 反光比例 (glare ratio) | > 0.15 | 警告 | 卡面 >15% 像素 ≥240 |
 | 卡牌面积比 (card area) | < 0.20 | 跳过检测 | 卡牌框面积 < 照片 20% 时走全图 fallback |
 
 质量门控为软性警告，不会阻断流程，但 API 返回值中会包含 `warnings` 列表。
 
 ### 5.4 方向候选策略 (orientation_candidates)
 
 - **横图**（宽 > 高）：尝试 -90° 和 +90° 旋转（竖卡被拍横了）
 - **竖图**（高 > 宽）：尝试原图和 180° 旋转（倒置拍摄）
 - 多候选独立评分，取最高分
 
 ---
 
 ## 6. OCR 引擎与预处理
 
 ### 6.1 PP-OCRv4 引擎结构
 
 实际部署使用的是 `script_temp/ppocr_v4_engine.py`，基于 PaddleInference 原生推理：
 
 ```
 PPOCRv4Engine
   ├── PPOCRv4Detector (ch_PP-OCRv4_det_infer)
   │   ├── 预处理: DBResizeForTest (limit_side_len=736) → NormalizeImage → ToCHWImage
   │   ├── 推理: PaddleInference (MKLDNN, 2 threads)
   │   └── 后处理: DBPostProcess (thresh=0.3, box_thresh=0.5, unclip_ratio=1.6)
   │
   └── PPOCRv4Recognizer (ch_PP-OCRv4_rec_infer)
       ├── 预处理: resize_norm_img (48×320, 动态宽高比, batch=6)
       ├── 推理: PaddleInference
       └── 后处理: CTCLabelDecode (ppocr_keys_v1.txt)
 ```
 
 **关键参数：**
 - 检测: 输入短边 736px，检测阈值 0.3，框阈值 0.5，unclip_ratio 1.6
 - 识别: 输入高度 48px，最大宽度 320px（动态），batch size 6
 - 文本置信度阈值: 0.5
 - 推理后端: PaddleInference + MKLDNN, 2 threads
 
 ### 6.2 OCR 独立预处理管线 (preprocess_ocr.py)
 
 `OCRPreprocessor` 类用于 `run_ocr()` 函数中的二次预处理（PP-OCRv4 引擎输入前）：
 
 1. **resize_to_max** — 长边缩放到 1200px（控制推理速度与精度平衡）
 2. **enhance_contrast** — CLAHE（clipLimit=2.0, grid=8×8）
 3. **denoise** — 双边滤波（d=9, sigmaColor=75, sigmaSpace=75）
 4. **sharpen** — USM 锐化（1.5 强度，-0.5 负片）
 5. **可选** — 灰度化 + 自适应阈值二值化
 
 注意：`OCRPreprocessor` 运行在 `preprocess_for_ocr()` 的增强图像之上，相当于对已增强的图像再做一次 OCR 专用优化。
 
 ### 6.3 三种 OCR 引擎对比
 
 | 引擎 | 文件 | 速度 (CPU) | 状态 |
 |------|------|-----------|------|
 | PP-OCRv4 (PaddleInference) | `ppocr_v4_engine.py` | ~2-3s | **当前部署** |
 | RapidOCR (ONNX) | `ocr_engine.py` | ~2.5s | 备选，代码中保留 |
 | EasyOCR (PyTorch) | `ocr_engine.py` | ~6-7s | 备选，代码中保留 |
 
 ---
 
 ## 7. 评估体系
 
 ### 7.1 评估脚本
 
 | 脚本 | 用途 |
 |------|------|
 | `benchmark_ocr.py` | OCR 准确率评估 |
 | `benchmark_ocr_ab.py` | OCR 引擎 A/B 对比测试 |
 | `benchmark_opt.py` | 预处理参数优化 |
 | `calibrate_quality_gates.py` | 质量门控阈值校准（基于 60 张真实照片） |
 | `calibrate_ocr_orientation.py` | OCR 方向校准 |
 
 ### 7.2 评估协议
 
 **协议 A（视觉匹配）：**
 - 随机抽取 100 张 gallery 图，通过 pipeline 匹配，验证 top-1 命中率
 - 当前基线: self-check 100%（100/100）
 - 真实照片评估待补充
 
 **协议 B（OCR + 文字匹配）：**
 - 对真实照片运行 OCR → 文字匹配 → 验证 top-k 中是否包含正确卡牌
 - 指标: OCR 准确率、文字匹配 top-1/top-5 召回率
 
 ---
 
 ## 8. API 接口一览
 
 | 端点 | 方法 | 输入 | 输出 | 用途 |
 |------|------|------|------|------|
 | `/` | GET | — | HTML 页面 | 前端主页 |
 | `/v1/health` | GET | — | 状态 + 索引规模 | 健康检查 |
 | `/v1/match` | POST | 图片 multipart | `matched` / `rejected` + card_id + score | 视觉匹配 |
 | `/v1/search` | POST | 图片 multipart | top-5 + 商品信息 + 预处理图像 | 视觉搜索 |
 | `/v1/ocr` | POST | 图片 multipart | 文本块 + 置信度 | 纯 OCR |
 | `/v1/ocr-match` | POST | 图片 multipart | top-5 商品匹配结果 | OCR + 文字匹配 |
 | `/v1/images/{card_id}` | GET | card_id 路径参数 | JPEG 图片 | 卡牌缩略图服务 |
 
 **服务配置：**
 - 绑定的所有网络接口: `0.0.0.0:8056`
 - 最大文件大小: 10MB
 - CORS: 全开（`allow_origins=["*"]`）
 
 ---
 
 ## 9. 关键设计决策与观察
 
 ### 9.1 设计决策
 
 1. **DINOv2 作视觉基线的理由**：自监督视觉特征，无需标注数据即可做检索基准；768 维 CLS token 足够区分 2.8 万张卡。
 2. **BGE-small-en-v1.5 作文字匹配的理由**：384 维轻量模型，CPU 推理快（~50ms），查询前缀可适配检索场景。
 3. **暴力检索而非 ANN**：2.8 万向量，faiss IndexFlatIP 在 CPU 上 < 5ms，不需要 ANN 索引。
 4. **双阈值拒绝策略**：score >= TAU 确保绝对匹配质量，margin >= MARGIN 确保区分度，避免混淆。
 5. **不先微调**：先跑裸 DINOv2 基线，根据基线数字决定是否微调。
 6. **预处理与索引走同一代码路径**：gallery 和 query 共享 `preprocess.py`，保证数据分布一致。
 7. **双方向推理**：横版图同时尝试 ±90°，竖版图尝试 0° + 180°，取最高分方向。
 8. **OCR 180° 重试**：低文本数时自动旋转 180° 重试，应对倒置拍摄。
 9. **OCR 视觉增强保守策略**：避免强增强导致笔画丢失（系列代码、版权文字等细粒度信息）。
 10. **质量门控为软警告**：不阻断流程，只返回警告，由调用方决定是否重拍。
 
 ### 9.2 当前局限与改进方向
 
 | 局限 | 影响 | 改进方向 |
 |------|------|----------|
 | 200px 缩略图分辨率上限 | 不支持读取卡号/系列标志等细粒度信息 | 使用更高分辨率输入 |
 | 无 GPU | 模型推理慢，微调无法进行 | 阿里云 GPU 实例 |
 | 无真实照片评估数据 | 阈值校准只能用模拟数据 | 收集真实场景标注数据 |
 | 51 组重复 SHA1（旧基线） | 不同卡号共用同一张图，模型无法区分 | 需要标记并可能移除 |
 | 日文卡牌数据未使用 | 缺失日文卡牌匹配能力 | 集成 `85_Pokemon_Japan` 数据 |
 | BGE 模型下载为 safetensors 需特殊配置 | 启动时需设置 `use_safetensors=False` | 切换为可加载 safetensors 的配置 |
 | PP-OCRv4 模型文件大 | 增加部署体积 | 可考虑 ONNX 量化版本 |
 
 ### 9.3 两条链路的关系
 
 当前 Demo 中两条链路**独立运行**，互不依赖：
 
 - **视觉匹配**（`/v1/match` / `/v1/search`）：适合卡面特征明显的场景，对图片质量要求较高
 - **OCR + 文字匹配**（`/v1/ocr-match`）：适合卡面文字清晰的场景，但对图片分辨率要求更高
 
 未来可能的融合策略：
 1. 先视觉匹配，低分时走 OCR 文字匹配兜底
 2. 视觉 + OCR 双通道打分融合
 3. 视觉定位文字区域 → OCR 识别 → 文字匹配
 
 ---
 
 *文档结束*
