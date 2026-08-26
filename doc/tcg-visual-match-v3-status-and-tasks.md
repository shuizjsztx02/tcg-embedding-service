 # TCG 卡牌视觉匹配 — 现状分析与任务拆解 v3
 
 日期：2026-08-26
 作者：Codex
 目标：用户上传真实拍摄的宝可梦卡牌照片 → 预处理 → 模型 → 返回库中匹配卡或拒绝。准确率目标 95%。
 
 ---
 
 ## 一、当前项目状态（实测确认）
 
 ### 数据层
 | 指标 | 数值 | 说明 |
 |------|------|------|
 | 图片总数 | 9435 | 全部为 JPG |
 | 有效图片 | 9434 | 1 张损坏：`153316_200w.jpg`（0 字节） |
 | 竖版图 | 8888 | 200×279 为主流 |
 | 横版图 | 546 | 200×14x，疑似旋转 90° 的竖卡 |
 | 重复 SHA1 组 | 51 组（118 张） | 不同 ID 但图片内容完全一致（同画不同卡号） |
 | 解码失败 | 0 | 所有有效图均可完整解码 |
 | 图片质量 | 200px 宽缩略图，6.6–41KB | 不支持读取卡号/系列标志等细粒度信息 |
 
 ### 环境层
 | 组件 | 版本 | 备注 |
 |------|------|------|
 | Python | 3.13.12 | — |
 | torch | 2.13.0+cpu | CPU-only，无 CUDA |
 | faiss-cpu | 1.15.0 | 已装 |
 | fastapi / uvicorn | 0.141.1 / 0.52.4 | 已装 |
 | opencv-python-headless | 5.0.0.93 | 已装 |
 | pillow / numpy | 12.2.0 / 2.4.4 | 已装 |
 | DINOv2 ViT-B/14 | 已缓存（~330MB） | 推理 126ms/张（CPU 单图） |
 
 ### 产物层
 | 文件 | 状态 | 说明 |
 |------|------|------|
 | csv/metadata.csv | 已完成 | 含 name, width, height, orientation, sha1 等 |
 | csv/data_audit_summary.csv | 已完成 | 汇总统计 |
 | script_temp/00_download_model.py | 已完成 | 模型已下载 |
 | script_temp/01_data_audit.py | 已完成 | 审计脚本，已产出完整结果 |
 | script_temp/02_baseline_eval.py | 已写，未运行 | **有 bug：persp_coeffs 矩阵行列错误** |
 | script_temp/preprocess.py | 已完成 | orientation_candidates + to_model_input |
 | script_temp/__pycache__/ | 存在 | 缓存目录 |
 | doc/tcg-visual-match-plan-v1.md | 已完成 | 技术方案 |
 | doc/tcg-visual-match-plan-v2-task-breakdown.md | 已完成 | 任务拆解 v2 |
 | index/ | 不存在 | 尚未构建 |
 | 无 .gitignore | 不存在 | 需要创建 |
 
 ---
 
 ## 二、方案评审：v2 任务拆解的问题与修正
 
 v2 文档整体质量很高，但实测发现以下问题需要修正：
 
 ### 问题 1：02_baseline_eval.py 的 persp_coeffs 有 bug
 `persp_coeffs` 函数中 row 3 和 row 7 的 `-x3*H` / `-y3*H` 被错误地放到了 g 系数列（index 6），而非 h 系数列（index 7）。非恒等变换下，生成的透视变换矩阵是错误的。**运行基线评估前必须修复**。
 
 ### 问题 2：Task 顺序和依赖关系可优化
 v2 建议 Task 0 → Task 1 → Task 5 的顺序。但 Task 0 的"完整预处理管线"（涉及 OpenCV 卡片检测等）可以先不阻塞基线评估和索引构建。修正后的顺序应为：
 1. 先修 bug + 跑基线（Task 1 修正版，用现有 preprocess.py）
 2. 再建索引（Task 3）
 3. 阈值校准 + API（Task 4 + Task 5）
 4. 预处理管线完善作为并行改进（Task 2）
 
 ### 问题 3：缺少灰度发布/回滚策略
 目前没有考虑索引版本管理、模型版本管理、API 接口版本兼容性。
 
 ### 问题 4：缺少安全基线
 没有 .gitignore，敏感文件（图片、模型权重、索引）可能被误提交。
 
 ### 问题 5：缺少"库外卡"的明确定义
 拒绝策略需要"库外卡"测试集。目前没有这类数据，需要从真实照片中收集或从现有数据中按系列留出。
 
 ---
 
 ## 三、修正后的任务拆解
 
 ---
 
 ### Task 1：修复基线评估脚本 + 跑通基线（P0）
 
 **做什么**：
 1. 修复 02_baseline_eval.py 中 persp_coeffs 的 bug（row 3 和 row 7 的 h 列）
 2. 验证修复后的透视变换在 PIL 中正确工作
 3. 以 n_query=100, n_unknown=50 小规模跑通基线
 4. 输出 csv/baseline_eval.csv + 基线报告 doc/baseline-report.md
 
 **验收标准**：
 - 修复后的 persp_coeffs 在非恒等透视变换下能正确 warp 图片
 - 基线评估脚本可完整运行（无报错）
 - 产出 top-1 准确率、genuine/impostor 分数分布
 - 产出 baseline_eval.csv
 
 **测试方法**：
 ```
 python script_temp/02_baseline_eval.py --n-query 100 --n-unknown 50
 # 检查：无报错，输出 csv 和终端指标
 ```
 
 **堵点**：
 - CPU 推理：100 张 query × 9.4k 索引 ≈ 100 次推理 ≈ 12.6s，加上 augment 时间 ≈ 20s。可接受。
 - 如果基线 top-1 准确率低于 60%（裸 DINOv2 对模拟拍照图的 domain gap 可能很大），需要决定是否继续推进或直接跳到 Task 6 微调。
 
 **预估耗时**：1–2 小时
 
 ---
 
 ### Task 2：数据治理加固（P0）
 
 **做什么**：
 1. 处理 1 张损坏图片（删除或标记）
 2. 调查 51 组重复 SHA1（确认是否确实为不同卡号用同一张图，还是误标）
 3. 横版图方向确认：抽样 20 张 landscape 图目视，确认是否全部为旋转 90° 的竖卡
 4. 产出 csv/corrupt_ids.txt（损坏图片清单）
 5. 产出 csv/duplicate_groups.csv（重复组清单）
 6. 创建 .gitignore（忽略 images/、index/、csv/ 下的数据文件、__pycache__、*.pth）
 
 **验收标准**：
 - 损坏图片已确认不影响后续流程
 - 重复图片的合理性质疑已记录
 - 横版图方向确认结果已记录
 - .gitignore 已创建
 
 **测试方法**：
 ```
 # 目视抽样 20 张 landscape 图
 python -c "from PIL import Image; import os; import random; imgs=[f for f in os.listdir('images') if Image.open(os.path.join('images',f)).size[0] > Image.open(os.path.join('images',f)).size[1]][:20]; print('\n'.join(imgs))"
 ```
 
 **堵点**：
 - 如果重复 SHA1 的图片确实是不同卡号但同一张图，则模型无法区分——这是系统性上限。
 - 如果横版图中有部分不是旋转的竖卡（如 Trainer 卡是横向设计），需要特殊处理。
 
 **预估耗时**：1 小时
 
 ---
 
 ### Task 3：完整 Embedding 索引构建 + 自检（P0）
 
 **做什么**：
 1. 编写 script_temp/build_index.py
 2. 用 preprocess.py 处理所有 9434 张有效 gallery 图
 3. 用 DINOv2 CLS token 提取 768 维 embedding，L2 归一化
 4. 用 faiss IndexFlatIP 构建索引，保存到 index/
 5. 自检：随机抽 100 张图检索自身，验证 top-1 命中率 = 100%
 6. 记录索引构建时间和 embedding 统计信息
 
 **验收标准**：
 - index/ 目录下产出 embeddings.npy（9434×768 float32）和 ids.json
 - 自检 100 张图 top-1 命中率 100%
 - 索引构建时间记录
 
 **测试方法**：
 ```
 python script_temp/build_index.py
 # 检查 index/ 目录
 python -c "import numpy as np; import json; emb=np.load('index/embeddings.npy'); ids=json.load(open('index/ids.json')); print(f'embeddings: {emb.shape}, ids: {len(ids)}')"
 ```
 
 **堵点**：
 - CPU 构建 9.4k 张图 embedding 约 126ms × 9434 ≈ 20 分钟（含 I/O）。建议一次性跑完。
 - 需要确保 preprocess.py 对横版图的处理与 API 端完全一致，否则索引侧和查询侧 embedding 不匹配。
 
 **预估耗时**：2–3 小时（含构建等待时间）
 
 ---
 
 ### Task 4：基线评估正式版（P0）
 
 **做什么**：
 1. 修复后的 02_baseline_eval.py → 改为使用已构建的索引（而非重新计算），以节省时间
 2. 用 n_query=500, n_unknown=200 跑正式基线
 3. 分析结果：
    - top-1 准确率
    - genuine / impostor 分数分布（P5, P50, P95）
    - 混淆分析：哪些卡容易被误判
    - 重复 SHA1 组的误判率
 4. 输出 doc/baseline-report.md
 
 **验收标准**：
 - 基线数字已产出
 - 混淆分析报告已产出
 - 已知卡准确率 + 未知卡拒绝率已记录
 
 **测试方法**：
 ```
 python script_temp/02_baseline_eval.py --n-query 500 --n-unknown 200
 ```
 
 **堵点**：
 - 如果基线准确率远低于 80%，需要沟通是否跳过后续步骤，直接进入微调阶段。
 - 混淆分析需要人工判断，无法完全自动化。
 
 **预估耗时**：2–3 小时
 
 ---
 
 ### Task 5：阈值校准（P0）
 
 **做什么**：
 1. 编写 script_temp/calibrate_threshold.py
 2. 用基线评估中的 genuine score 和 impostor score 分布
 3. 搜索最优 τ（top-1 分数阈值）和 m（top-1 与 top-2 分差阈值）
 4. 优化目标：已知卡接受率 ≥ 95% 且 未知卡拒绝率 ≥ 95%
 5. 输出校准报告 doc/threshold-calibration.md
 6. 输出最优 τ, m 值，固化到配置
 
 **验收标准**：
 - τ 和 m 已确定并记录
 - 校准曲线（PR 曲线、F1 曲线）已产出
 - 在验证集上达到目标接受率/拒绝率
 
 **测试方法**：
 ```
 python script_temp/calibrate_threshold.py
 ```
 
 **堵点**：
 - 模拟增强数据与真实照片的 domain gap 导致阈值校准偏差
 - 如果 genuine 和 impostor 分数分布重叠严重，可能无法同时满足 95%/95% 的目标
 - 缺乏真实照片数据，阈值只能基于模拟数据校准，到真实场景可能需要调整
 
 **预估耗时**：1–2 小时
 
 ---
 
 ### Task 6：预处理管线完善（P1，与 Task 3–5 并行）
 
 **做什么**：
 1. 扩展 preprocess.py 为完整管线：
    - EXIF 方向修正
    - 卡片四边形检测（轮廓 + approxPolyDP，回退 minAreaRect，再回退中心裁）
    - 单应性矫正到标准比例
    - 180° 方向修正（小分类器或双方向推理取最高分）
    - 轻度质量增强（白平衡、高光抑制、锐化）
    - 等比 resize + padding 到模型输入
 2. 确保离线（构建索引）和在线（API 查询）走同一路径
 3. 编写单元测试覆盖：
    - 横版图 → 自动旋转竖卡
    - 竖版图 → 保持原样
    - 小尺寸图 → 等比缩放
    - 有白边图 → 裁剪
 
 **验收标准**：
 - 预处理管线可处理所有方向/尺寸的图片
 - 对 546 张横版图自动旋转竖卡
 - 输出标准化图片可目视验收
 - 单元测试覆盖 4 个场景
 
 **测试方法**：
 ```
 # 目视验收
 python -c "from preprocess import preprocess_pipeline; import os; from PIL import Image; imgs=[f for f in os.listdir('images') if os.path.splitext(f)[1].lower() in ('.jpg','.jpeg','.png')][:10]; [preprocess_pipeline(Image.open(os.path.join('images',f))).save(os.path.join('script_temp','test_'+f)) for f in imgs]"
 ```
 
 **堵点**：
 - OpenCV 的卡片四边形检测对 200px 低分辨率图效果有限，可能需要回退到简单策略
 - 如果卡片本身是横向设计（如 Trainer 卡），方向分类器需要特殊处理
 - 完整的预处理管线可能引入新的 image artifacts，需要做回归测试
 
 **预估耗时**：3–5 小时
 
 ---
 
 ### Task 7：API 服务构建（P1）
 
 **做什么**：
 1. 用 FastAPI 构建推理服务 app/main.py
 2. 加载索引和模型（启动时一次加载）
 3. 接口：
    - POST /v1/match：接收 multipart 上传的图片 → 预处理 → embedding → 检索 → 阈值判定 → 返回结果
    - GET /v1/health：健康检查
 4. 返回格式：
    ```json
    {"status": "matched", "card_id": "100503", "score": 0.87, "margin": 0.12}
    {"status": "rejected", "card_id": null, "score": 0.32, "margin": 0.01}
    ```
 5. 错误处理：图片损坏、无法解码、预处理失败等
 6. 编写启动脚本 run_api.py
 
 **验收标准**：
 - API 可正常启动和响应
 - 上传一张库内卡图片，返回 matched
 - 上传一张非卡图片，返回 rejected
 - 端到端延迟 P95 ≤ 500ms（CPU）
 
 **测试方法**：
 ```
 # 启动服务
 python script_temp/run_api.py &
 # 测试
 curl -X POST -F "file=@images/100503_200w.jpg" http://localhost:8000/v1/match
 curl http://localhost:8000/v1/health
 # 测试非卡图片
 curl -X POST -F "file=@test_not_card.jpg" http://localhost:8000/v1/match
 ```
 
 **堵点**：
 - CPU 推理 126ms + 预处理 ~50ms + 检索 ~5ms ≈ 180ms，P95 可控制在 500ms 内
 - 预处理管线需要移植到服务端，保持与离线版一致
 - 内存占用：模型 ~670MB（87M params × 4 bytes × 2 for inference）+ 索引 ~29MB ≈ 700MB，可接受
 
 **预估耗时**：3–4 小时
 
 ---
 
 ### Task 8：对比学习微调（P2，需 GPU）
 
 **做什么**：
 1. 编写 script_temp/finetune_dinov2.py
 2. 数据准备：对每张 gallery 卡，用模拟增强生成"手机拍照"视图（正对）
 3. 用对比学习微调 DINOv2（InfoNCE loss）：
    - 正对：同一张卡的扫描图 vs 模拟拍照图
    - 负例：batch 内其他卡
 4. 训练结束后导出模型权重
 5. 重新构建索引（用微调后的模型）
 6. 重新跑基线评估 + 阈值校准
 
 **验收标准**：
 - 微调后模型准确率 ≥ 95%（模拟协议 A）
 - 未知卡拒绝率 ≥ 95%（协议 B）
 - 模型权重已保存
 
 **测试方法**：
 ```
 # 在 GPU 机器上运行
 python script_temp/finetune_dinov2.py --epochs 60 --batch-size 128
 # 重新构建索引
 python script_temp/build_index.py --model-path models/finetuned_dinov2.pth
 # 重新评估
 python script_temp/02_baseline_eval.py --n-query 500 --n-unknown 200 --model-path models/finetuned_dinov2.pth
 ```
 
 **堵点**：
 - 需要 GPU（云单卡 24GB，几小时）
 - 模拟增强的参数分布需要精心设计，防止过拟合模拟器
 - 如果元数据（系列、卡号）不可得，无法做"同系列硬负例"策略
 - 微调后的模型需要重新构建索引，整个流程耗时长
 
 **预估耗时**：3–5 天（含训练等待、调参、验证）
 
 ---
 
 ### Task 9：真实照片验收（P2，持续进行）
 
 **做什么**：
 1. 收集 300–500 张真实拍摄的宝可梦卡牌照片（不同设备/光照/角度）
 2. 每张照片标注正确的 card_id（或标记为"库外卡"）
 3. 用最终的模型 + API 跑验收测试
 4. 输出验收报告 doc/acceptance-report.md
 
 **验收标准**：
 - 真实照片测试集上 top-1 准确率 ≥ 95%
 - 拒绝准确率 ≥ 95%
 - P95 延迟达标
 
 **测试方法**：
 ```
 python script_temp/acceptance_test.py --test-dir real_photos --labels csv/real_photo_labels.csv
 ```
 
 **堵点**：
 - 真实照片的收集和标注是最大瓶颈——需要用户配合
 - 真实照片可能包含更多极端情况：严重眩光、卡片弯曲、手指遮挡、其他卡片背景
 - 如果真实照片质量比模拟增强的"最坏情况"还要差，准确率可能骤降
 
 **预估耗时**：1–2 周（含收集、标注、验收）
 
 ---
 
 ## 四、执行路线图
 
 ```
 Week 1:
   ┌─────────────────────────────────────────────────────┐
   │ Task 1: 修 bug + 跑通基线 (1h)                      │  ← 立即开始
   ├─────────────────────────────────────────────────────┤
   │ Task 2: 数据治理 (1h)                               │  ← 并行
   ├─────────────────────────────────────────────────────┤
   │ Task 3: 构建索引 (2h 含等待)                         │  ← Task 2 完成后
   ├─────────────────────────────────────────────────────┤
   │ Task 4: 正式基线评估 + 混淆分析 (2h)                 │  ← Task 3 完成后
   ├─────────────────────────────────────────────────────┤
   │ Task 5: 阈值校准 (1h)                               │  ← Task 4 完成后
   ├─────────────────────────────────────────────────────┤
   │ Task 7: API 服务 (3-4h)                             │  ← Task 3+5 完成后
   └─────────────────────────────────────────────────────┘
 
 Week 2:
   ┌─────────────────────────────────────────────────────┐
   │ Task 6: 预处理管线完善 (3-5h，与周 1 并行)           │  ← 周 1 可并行
   ├─────────────────────────────────────────────────────┤
   │ Task 9: 真实照片收集 (持续)                          │  ← 现在开始
   └─────────────────────────────────────────────────────┘
 
 Week 3+:
   ┌─────────────────────────────────────────────────────┐
   │ Task 8: 对比学习微调 (需 GPU，3-5天)                 │  ← 基线评估后决策
   └─────────────────────────────────────────────────────┘
 ```
 
 **关键决策点**：
 1. 基线评估后：如果 top-1 < 60% → 直接跳 Task 8 微调；如果 ≥ 60% → 先出 API 再微调
 2. 阈值校准后：如果 95%/95% 无法同时满足 → 需要调整目标（如 90%/95%）或等待微调
 3. 真实照片收集后：如果 domain gap 太大 → 优先微调
 
 ---
 
 ## 五、关键风险清单
 
 | 风险 | 影响 | 缓解措施 |
 |------|------|----------|
 | 200px 分辨率上限 | 模型天花板，卡号/系列标志不可读 | 寻找高分辨率原图；微调时用 448px 输入 |
 | 重复 SHA1（51 组） | 模型无法区分"同画不同卡"的卡 | 确认后标记为"无法区分组"，API 返回时提示 |
 | 无真实照片数据 | 阈值校准不准确，上线后准确率低 | 从现在开始收集；先用模拟数据占位 |
 | CPU 推理延迟 | 无法支持高并发 | 目前并发要求低，以跑通为准；ONNX 优化延后 |
 | 横版图方向误判 | 索引和查询方向不一致，准确率下降 | 双方向推理取最高分（目前 preprocess.py 已实现） |
 | 损坏图片影响 | 索引构建失败 | 已识别并跳过（1 张） |
 | 模型微调后的回归 | 索引需要重建，API 需要重新部署 | 版本管理（索引 + 模型版本号） |
 
 ---
 
 ## 六、与 v2 的差异说明
 
 1. **Task 顺序调整**：v2 建议 Task 0 → Task 1 → Task 5。但数据治理不阻塞基线评估，且基线评估中有 orientation_candidates 逻辑处理横版图，因此 Task 2 可以和 Task 1 并行。
 2. **新增 Task 1 修复**：发现 02_baseline_eval.py 有 bug，必须修复后才能运行。
 3. **新增 Task 9 真实照片验收**：从 v2 的最后阶段拆分为独立任务，强调需要从现在开始收集。
 4. **Task 2 范围缩小**：数据治理不包含"预处理管线完善"，该部分拆到 Task 6。
 5. **Task 5 阈值校准**：从 v2 的 Task 4 移动到 Task 5，因为需要先有基线评估数据。
 6. **新增关键决策点**：在基线评估后增加决策点，根据基线数字决定后续路径。
 7. **新增风险清单**：系统性整理了 7 个风险点及缓解措施。
