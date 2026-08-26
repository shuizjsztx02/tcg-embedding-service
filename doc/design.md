 # 技术设计文档 — TCG 卡牌视觉匹配服务
 
 版本：v1.0
 日期：2026-08-26
 状态：定稿
 
 ---
 
 ## 1. 系统架构
 
 ```
 ┌─────────────────────────────────────────────────────────────┐
 │                     离线流程（索引构建）                       │
 │                                                             │
 │  images/ ───→ preprocess.py ───→ DINOv2 ───→ L2归一化 ───→ faiss index │
 │   (9434)      (方向修正+resize)     (768维)     (向量归一化)   (IndexFlatIP) │
 │                                                                             │
 │                   ↓                                              ↓          │
 │              csv/metadata.csv                              index/embeddings.npy│
 │                                                              index/ids.json   │
 └─────────────────────────────────────────────────────────────┘
 
                              │
                              │ 加载一次
                              ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                     在线流程（API 推理）                       │
 │                                                             │
 │  用户上传图片 ──→ preprocess.py ──→ DINOv2 ──→ L2归一化 ──→ faiss检索 ──→ 阈值判定 ──→ 返回结果 │
 │                  (同离线路径)      (768维)      (向量归一化)   (top-K)       (τ + m)       │
 └─────────────────────────────────────────────────────────────┘
 ```
 
 **关键原则**：gallery 与 query 走完全相同的预处理与模型代码路径。
 
 ---
 
 ## 2. 组件设计
 
 ### 2.1 预处理管线（preprocess.py）
 
 **输入**：PIL Image（任意大小/方向）
 **输出**：224×224 RGB 图片，归一化到 ImageNet 均值和标准差
 
 ```python
 # 当前实现（v1，基线用）
 def orientation_candidates(img):
     """横版图返回 [90°旋转, 270°旋转]，竖版图返回 [原图]"""
 
 def to_model_input(img):
     """RGB + resize 到 (168, 224)"""
 ```
 
 **未来扩展（v2，需完善）**：
 - EXIF 方向修正
 - 卡片四边形检测（轮廓 + approxPolyDP，回退 minAreaRect，再回退中心裁）
 - 单应性矫正到标准比例
 - 180° 方向修正
 - 轻度质量增强（白平衡、高光抑制、锐化）
 - 等比 resize + padding 到 224×224
 
 ### 2.2 模型服务（DINOv2 ViT-B/14）
 
 | 参数 | 值 |
 |------|-----|
 | 模型 | facebookresearch/dinov2, dinov2_vitb14 |
 | 参数规模 | 87M |
 | 输入尺寸 | 224×224 |
 | Patch 大小 | 14×14 |
 | Embedding 维度 | 768（CLS token） |
 | 推理框架 | torch CPU |
 | 推理延迟 | ~126ms/张（CPU） |
 | 内存占用 | ~670MB（模型权重 + 中间激活） |
 
 **Embedding 方案**：
 - 使用 CLS token 作为图片表示
 - 输出向量做 L2 归一化，使余弦相似度等价于内积
 - 维度 768，每个 float32 占 4 字节，9434 张 × 768 × 4 ≈ 29MB
 
 **微调方案（M2）**：
 - 在 CLS token 后加线性投影头（768 → 512）
 - 对比学习，InfoNCE loss
 - 正对：同一张卡的扫描图 vs 模拟手机拍照图
 - 负例：batch 内其他卡 + memory bank
 - 训练端到端（或 LoRA 低资源适配）
 - 输出维度：512
 
 ### 2.3 索引构建（faiss）
 
 | 参数 | 值 |
 |------|-----|
 | 索引类型 | IndexFlatIP（暴力内积） |
 | 向量维度 | 768（M1）/ 512（M2） |
 | 数据量 | 9434 张 |
 | 检索延迟 | < 5ms（CPU） |
 | 内存占用 | ~29MB（M1）/ ~19MB（M2） |
 
 **索引文件**：
 - `index/embeddings.npy`：N×D float32 数组
 - `index/ids.json`：对应 card_id 列表
 - `index/version.txt`：版本号（格式：`M1-YYYYMMDD` 或 `M2-YYYYMMDD`）
 
 **自检方案**：随机抽 100 张图，检索自身，验证 top-1 命中率 = 100%
 
 ### 2.4 检索与判定
 
 **检索**：faiss IndexFlatIP.search(query, k=3) → top-3 分数和索引
 
 **判定逻辑**：
 ```
 if s1 >= τ and (s1 - s2) >= m:
     return matched(card_id, s1, margin=s1-s2)
 else:
     return rejected(s1)
 ```
 
 其中 τ 和 m 通过校准确定（在验证集上最大化 F1 分数）。
 
 ### 2.5 API 服务（FastAPI）
 
 **接口设计**：
 
 ```
 POST /v1/match
 Content-Type: multipart/form-data
 Body: file=<image>
 Response 200:
   {"status": "matched", "card_id": "100503", "score": 0.87, "margin": 0.12}
   {"status": "rejected", "card_id": null, "score": 0.32, "margin": 0.01}
 Response 400:
   {"status": "error", "message": "无法解码图片"}
 Response 500:
   {"status": "error", "message": "内部错误"}
 
 GET /v1/health
 Response 200:
   {"status": "ok", "model": "dinov2_vitb14", "index_size": 9434, "version": "M1-20260826"}
 ```
 
 **加载策略**：模型和索引在服务启动时一次性加载，后续请求复用。
 
 ### 2.6 延迟预算
 
 | 阶段 | 预估耗时 | 说明 |
 |------|----------|------|
 | 图片解码 + 预处理 | ≤ 50ms | PIL 打开 + resize |
 | Embedding 推理 | ~126ms | DINOv2 CPU 推理 |
 | 向量检索 | ≤ 5ms | faiss IndexFlatIP |
 | 阈值判定 | ≤ 1ms | 简单比较 |
 | 总计 | ≤ 182ms | 不含网络传输 |
 | P95 | ≤ 300ms | 含波动 |
 
 ---
 
 ## 3. 数据流
 
 ### 3.1 离线索引构建流
 
 ```
 1. 读取 images/ 目录和 csv/metadata.csv
 2. 跳过损坏图片（153316_200w.jpg）
 3. 对每张图：
    a.  PIL.Image.open → load()
    b.  orientation_candidates() → 处理横版图
    c.  to_model_input() → resize 到模型输入
    d.  DINOv2 推理 → 768 维向量
    e.  L2 归一化
 4. 拼接所有向量 → embeddings.npy
 5. 保存 ids.json
 6. 自检：随机抽样验证
 ```
 
 ### 3.2 在线匹配流
 
 ```
 1. 接收 multipart 上传的图片
 2. 尝试解码为 PIL Image
 3. 与离线相同的预处理路径
 4. DINOv2 推理 → embedding
 5. faiss 检索 top-3
 6. 阈值判定
 7. 返回结果
 ```
 
 ---
 
 ## 4. 评估协议
 
 ### 协议 A（模拟真拍，迭代用）
 - 留出 10% 的卡作为 query 集
 - 对每张 query 卡，用模拟增强生成 5 个"手机拍照"视图
 - 对剩余 90% 的卡构建索引
 - 指标：top-1 准确率
 - 注意：模拟增强参数分布与训练时不同，防止"自己验自己"
 
 ### 协议 B（未知拒绝）
 - 留出 200 张卡作为 unknown 集
 - 从索引中移除 unknown 集
 - 指标：误接受率（未知卡被错误匹配的比例）
 
 ### 协议 C（真实照片，验收用）
 - 收集 300–500 张带正确 ID 的真实拍摄照片
 - 指标：top-1 准确率 + 拒绝准确率
 - 最终验收口径
 
 ---
 
 ## 5. 部署方案
 
 ### 当前阶段（M1）
 - 本地开发环境（CPU-only）
 - 直接运行 FastAPI 服务
 - 无容器化
 
 ### 后续阶段（M2+）
 - 阿里云 GPU 用于微调
 - 推理阶段保持 CPU
 - 可选 ONNX 优化加速
 - 可选 Docker 容器化部署
 
 ---
 
 ## 6. 版本管理
 
 | 组件 | 版本标识 | 存储位置 |
 |------|----------|----------|
 | 索引 | M1-YYYYMMDD / M2-YYYYMMDD | index/version.txt |
 | 模型权重 | dinov2_vitb14 / finetuned-v1 | model/ 或 torch hub 缓存 |
 | API 接口 | /v1/match | 路径前缀 |
 
 索引重建后，version.txt 递增，API 启动时记录版本号。
 
 ---
 
 ## 7. 安全考虑
 
 1. **输入验证**：限制上传文件大小（≤ 10MB），校验文件类型（仅 JPEG/PNG）
 2. **路径遍历防护**：不信任用户提供的文件名
 3. **资源限制**：单次请求最大内存使用 ≤ 500MB
 4. **超时控制**：单次请求超时 30s
 5. **敏感文件保护**：.gitignore 排除 images/、index/、model/、csv/ 数据文件
 
 ---
 
 ## 8. 依赖清单
 
 ```
 torch>=2.0.0              # DINOv2 推理
 faiss-cpu>=1.7.0          # 向量检索
 fastapi>=0.100.0          # API 框架
 uvicorn>=0.20.0           # ASGI 服务器
 numpy>=1.24.0             # 数值计算
 pillow>=10.0.0            # 图片处理
 opencv-python-headless>=4.8.0  # 预处理（卡片检测等）
 python-multipart>=0.0.6   # FastAPI 文件上传
 ```
 
 完整依赖见 `requirements.txt`。
