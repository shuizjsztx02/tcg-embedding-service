 # 实施计划 — TCG 卡牌视觉匹配服务
 
 版本：v1.0
 最后更新：2026-08-26
 更新者：Codex
 
 ---
 
 ## 总体状态
 
 | 阶段 | 状态 | 完成度 |
 |------|------|--------|
 | M0：数据治理 | 基本完成，待加固 | 80% |
 | M1：裸 DINOv2 基线 | 脚本已写，未运行 | 20% |
 | M2：API 服务 | 未开始 | 0% |
 | M3：微调（需 GPU） | 未开始 | 0% |
 | M4：真实照片验收 | 未开始 | 0% |
 
 **当前焦点**：修复 02_baseline_eval.py 的 bug → 跑通基线 → 构建索引 → 搭 API
 
 ---
 
 ## 任务列表
 
 每个任务包含：状态、验收标准、测试方法、依赖、预估耗时。完成时更新状态和完成日期。
 
 ---
 
 ### Task 1：修复基线评估脚本 + 跑通基线
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P0 |
 | 依赖 | 无 |
 | 预估耗时 | 1–2 小时 |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 修复 02_baseline_eval.py 中 persp_coeffs 的 bug（row 3 和 row 7 的 h 列）
 2. 验证修复后的透视变换在 PIL 中正确工作
 3. 以 n_query=100, n_unknown=50 小规模跑通基线
 4. 输出 csv/baseline_eval.csv + 基线报告 doc/baseline-report.md
 
 **验收标准**：
 - [ ] 修复后的 persp_coeffs 在非恒等透视变换下能正确 warp 图片
 - [ ] 基线评估脚本可完整运行（无报错）
 - [ ] 产出 top-1 准确率、genuine/impostor 分数分布
 - [ ] 产出 baseline_eval.csv
 
 **测试方法**：
 ```bash
 python script_temp/02_baseline_eval.py --n-query 100 --n-unknown 50
 ```
 
 **堵点**：
 - 如果基线 top-1 准确率低于 60%，需要决策是否跳过后续步骤，直接进入微调
 
 **备注**：
 - 验证脚本：`persp_coeffs` 需要将 row 3 的 `-x3*H` 从 index 6 移到 index 7，row 7 的 `-y3*H` 从 index 6 移到 index 7
 
 ---
 
 ### Task 2：数据治理加固
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P0 |
 | 依赖 | 无 |
 | 预估耗时 | 1 小时 |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 处理 1 张损坏图片（153316_200w.jpg，0 字节）
 2. 调查 51 组重复 SHA1（118 张），确认是否不同卡号共用同一张图
 3. 抽样 20 张 landscape 图目视确认方向
 4. 产出 csv/corrupt_ids.txt
 5. 产出 csv/duplicate_groups.csv
 6. 创建 .gitignore
 
 **验收标准**：
 - [ ] 损坏图片已确认不影响后续流程
 - [ ] 重复图片清单已产出
 - [ ] 横版图方向确认结果已记录
 - [ ] .gitignore 已创建（忽略 images/、index/、csv/*.csv、__pycache__、*.pth）
 
 **测试方法**：
 ```bash
 python -c "from PIL import Image; import os; imgs=[f for f in os.listdir('images') if Image.open(os.path.join('images',f)).size[0] > Image.open(os.path.join('images',f)).size[1]][:20]; print('\n'.join(imgs))"
 ```
 
 **堵点**：
 - 如果重复 SHA1 的图片确实是不同卡号但同一张图，模型无法区分——这是系统性上限
 - 如果横版图中有部分不是旋转的竖卡（如 Trainer 卡），需要特殊处理
 
 ---
 
 ### Task 3：完整 Embedding 索引构建
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P0 |
 | 依赖 | Task 2 |
 | 预估耗时 | 2–3 小时（含构建等待 20 分钟） |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 编写 script_temp/build_index.py
 2. 用 preprocess.py 处理所有 9434 张有效图
 3. 用 DINOv2 提取 768 维 embedding，L2 归一化
 4. 用 faiss IndexFlatIP 构建索引
 5. 保存到 index/embeddings.npy + index/ids.json
 6. 自检：随机抽 100 张图检索自身，验证 top-1 命中率 = 100%
 
 **验收标准**：
 - [ ] index/ 目录下产出 embeddings.npy（9434×768 float32）和 ids.json
 - [ ] 自检 100 张图 top-1 命中率 100%
 - [ ] 索引构建时间已记录
 
 **测试方法**：
 ```bash
 python script_temp/build_index.py
 python -c "import numpy as np; import json; emb=np.load('index/embeddings.npy'); ids=json.load(open('index/ids.json')); print(f'embeddings: {emb.shape}, ids: {len(ids)}')"
 ```
 
 **堵点**：
 - CPU 构建 9.4k 张图 embedding 约 20 分钟，建议一次性跑完
 - 需要确保 preprocess.py 对横版图的处理与 API 端完全一致
 
 ---
 
 ### Task 4：正式基线评估与混淆分析
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P0 |
 | 依赖 | Task 3（索引已构建） |
 | 预估耗时 | 2–3 小时 |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 修改 02_baseline_eval.py 使用已构建的索引（而非重新计算）
 2. 用 n_query=500, n_unknown=200 跑正式基线
 3. 分析：top-1 准确率、分数分布、混淆矩阵
 4. 输出 doc/baseline-report.md
 
 **验收标准**：
 - [ ] 基线数字已产出（top-1 准确率、genuine/impostor 分数分布）
 - [ ] 混淆分析报告已产出
 - [ ] 已知卡准确率 + 未知卡拒绝率已记录
 
 **测试方法**：
 ```bash
 python script_temp/02_baseline_eval.py --n-query 500 --n-unknown 200
 ```
 
 **堵点**：
 - 如果基线准确率远低于 80%，需要决策是否跳过后续步骤，直接进入微调
 - 混淆分析需要人工判断
 
 **关键决策点**：基线评估结果将决定下一步路径——
 - top-1 ≥ 60%：继续推进 API 服务
 - top-1 < 60%：直接跳 Task 8（微调）
 
 ---
 
 ### Task 5：阈值校准
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P0 |
 | 依赖 | Task 4 |
 | 预估耗时 | 1–2 小时 |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 编写 script_temp/calibrate_threshold.py
 2. 用基线评估中的 genuine score 和 impostor score 分布
 3. 搜索最优 τ 和 m
 4. 优化目标：已知卡接受率 ≥ 95%，未知卡拒绝率 ≥ 95%
 5. 输出 doc/threshold-calibration.md
 
 **验收标准**：
 - [ ] τ 和 m 已确定并记录
 - [ ] 校准曲线已产出
 - [ ] 在验证集上达到目标接受率/拒绝率
 
 **测试方法**：
 ```bash
 python script_temp/calibrate_threshold.py
 ```
 
 **堵点**：
 - 模拟增强数据与真实照片的 domain gap 可能导致校准偏差
 - 如果 genuine 和 impostor 分数分布重叠严重，可能无法同时满足 95%/95%
 
 ---
 
 ### Task 6：预处理管线完善
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P1 |
 | 依赖 | 无（与 Task 3–5 并行） |
 | 预估耗时 | 3–5 小时 |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 扩展 preprocess.py 为完整管线
 2. 添加：EXIF 方向修正、卡片四边形检测、单应性矫正、质量增强
 3. 确保离线/在线走同一路径
 4. 编写单元测试
 
 **验收标准**：
 - [ ] 预处理管线可处理所有方向/尺寸的图片
 - [ ] 对 546 张横版图自动旋转竖卡
 - [ ] 输出标准化图片可目视验收
 - [ ] 单元测试覆盖 4 个场景
 
 **测试方法**：
 目视验收 + 单元测试
 
 **堵点**：
 - OpenCV 卡片检测对 200px 低分辨率图效果有限
 - 横向设计的卡（如 Trainer 卡）需要特殊处理
 
 ---
 
 ### Task 7：API 服务构建
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P1 |
 | 依赖 | Task 3（索引）+ Task 5（阈值） |
 | 预估耗时 | 3–4 小时 |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 创建 app/main.py（FastAPI 服务）
 2. 实现 POST /v1/match 和 GET /v1/health
 3. 加载模型和索引（启动时一次加载）
 4. 实现预处理 → 推理 → 检索 → 判定流程
 5. 错误处理
 6. 编写启动脚本 script_temp/run_api.py
 7. 接口测试
 
 **验收标准**：
 - [ ] API 可正常启动和响应（/v1/health → 200）
 - [ ] 上传库内卡图片 → 返回 matched 含 card_id
 - [ ] 上传非卡图片 → 返回 rejected
 - [ ] 端到端延迟 P95 ≤ 500ms（CPU）
 - [ ] 错误处理正常（损坏图片 → 400，内部错误 → 500）
 
 **测试方法**：
 ```bash
 python script_temp/run_api.py &
 curl -X POST -F "file=@images/100503_200w.jpg" http://localhost:8000/v1/match
 curl http://localhost:8000/v1/health
 ```
 
 ---
 
 ### Task 8：对比学习微调
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P2 |
 | 依赖 | Task 1（基线基线）+ Task 6（预处理管线） |
 | 预估耗时 | 3–5 天（含训练等待、调参、验证） |
 | 实际耗时 | — |
 | 完成日期 | — |
 | 所需资源 | 阿里云 GPU（单卡 24GB） |
 
 **做什么**：
 1. 编写 script_temp/finetune_dinov2.py
 2. 数据准备：模拟增强生成"手机拍照"视图
 3. 对比学习训练（InfoNCE loss）
 4. 导出模型权重
 5. 重新构建索引
 6. 重新跑基线评估 + 阈值校准
 
 **验收标准**：
 - [ ] 微调后模型准确率 ≥ 95%（模拟协议 A）
 - [ ] 未知卡拒绝率 ≥ 95%（协议 B）
 - [ ] 模型权重已保存
 - [ ] 微调前后对比报告已产出
 
 **测试方法**：
 ```bash
 python script_temp/finetune_dinov2.py --epochs 60 --batch-size 128
 python script_temp/build_index.py --model-path model/finetuned-v1.pth
 python script_temp/02_baseline_eval.py --n-query 500 --n-unknown 200 --model-path model/finetuned-v1.pth
 ```
 
 **堵点**：
 - 需要 GPU（云单卡 24GB，几小时量级）
 - 模拟增强参数分布需精心设计，防止过拟合
 - 无元数据（系列、卡号）无法做"同系列硬负例"
 - 微调后需要重新构建索引，流程耗时长
 
 ---
 
 ### Task 9：真实照片验收
 
 | 元数据 | 值 |
 |--------|-----|
 | 状态 | **待开始** |
 | 优先级 | P2 |
 | 依赖 | Task 7（API 服务）+ Task 8（微调，可选） |
 | 预估耗时 | 1–2 周（含收集、标注、验收） |
 | 实际耗时 | — |
 | 完成日期 | — |
 
 **做什么**：
 1. 收集 300–500 张真实拍摄的宝可梦卡牌照片
 2. 标注正确的 card_id（或标记为"库外卡"）
 3. 编写 script_temp/acceptance_test.py
 4. 跑验收测试
 5. 输出 doc/acceptance-report.md
 
 **验收标准**：
 - [ ] 真实照片测试集上 top-1 准确率 ≥ 95%
 - [ ] 拒绝准确率 ≥ 95%
 - [ ] P95 延迟达标
 - [ ] 错误案例分析报告已产出
 
 **测试方法**：
 ```bash
 python script_temp/acceptance_test.py --test-dir real_photos --labels csv/real_photo_labels.csv
 ```
 
 **堵点**：
 - 真实照片的收集和标注是最大瓶颈——需要用户配合
 - 真实照片可能包含更多极端情况：严重眩光、卡片弯曲、手指遮挡
 - 如果真实照片质量比模拟增强的"最坏情况"还要差，准确率可能骤降
 
 **建议**：从现在开始收集，不阻塞任何技术工作
 
 ---
 
 ## 执行路线图
 
 ```
 第 1 天（当前会话）：
   Task 1 ──→ 修 bug，跑基线
   Task 2 ──→ 数据治理（并行）
 
 第 2 天：
   Task 3 ──→ 构建索引
   Task 4 ──→ 正式基线评估
   Task 5 ──→ 阈值校准
   Task 6 ──→ 预处理管线完善（并行）
 
 第 3–4 天：
   Task 7 ──→ API 服务（依赖 Task 3+5 完成）
 
 第 1–2 周（持续）：
   Task 9 ──→ 真实照片收集
 
 基线评估后决策：
   ┌─ top-1 ≥ 60% → 继续 Task 7
   └─ top-1 < 60% → 跳 Task 8 微调
 
 第 3–5 天（微调，需 GPU）：
   Task 8 ──→ 对比学习微调
 ```
 
 ---
 
 ## 决策日志
 
 | 日期 | 决策 | 理由 | 决策者 |
 |------|------|------|--------|
 | 2026-08-26 | 使用 DINOv2 ViT-B/14 作为基线模型 | 自监督视觉特征，无需标注数据 | 用户 |
 | 2026-08-26 | 先跑基线，不微调 | 验证裸 DINOv2 在 TCG 领域的表现 | 用户 |
 | 2026-08-26 | 使用缩略图而非原图 | 先跑通流程，效果不好再换 | 用户 |
 | 2026-08-26 | 不区分卡牌版本 | 当前版本不涉及 | 用户 |
 | 2026-08-26 | 使用阿里云 GPU 资源 | 微调需要 GPU | 用户 |
 
 ---
 
 ## 变更记录
 
 | 日期 | 版本 | 变更内容 | 作者 |
 |------|------|----------|------|
 | 2026-08-26 | v1.0 | 初始版本 | Codex |
 
 ---
 
 ## 使用说明
 
 新对话开始时，请依次阅读：
 1. [AGENTS.md](/AGENTS.md) — 项目概览和开发指南
 2. [doc/implementation-plan.md](/doc/implementation-plan.md) — 当前任务状态（本文档）
 3. 根据需要阅读 [doc/PRD.md](/doc/PRD.md) 或 [doc/design.md](/doc/design.md)
 
 任务完成后，更新本文档中的状态（将"待开始"改为"已完成"，并填写实际耗时和完成日期）。
