 # AGENTS.md — TCG 卡牌视觉匹配服务
 
 本文档为 Codex 在此项目中的工作指南。合并通用 AGENTS.md 规则使用。
 
 ---
 
 ## 项目概览
 
 宝可梦卡牌视觉匹配服务。用户上传真实拍摄的宝可梦卡牌照片 → 预处理 → DINOv2 提取 embedding → 检索库中匹配 → 返回匹配结果或拒绝。目标准确率 95%。
 
 | 维度 | 值 |
 |------|-----|
 | 库规模 | 9434 张有效卡（1 张损坏），200px 缩略图 |
 | 模型 | DINOv2 ViT-B/14（87M 参数，768 维 embedding） |
 | 索引 | faiss IndexFlatIP（暴力余弦） |
 | 框架 | FastAPI + Python 3.13 + torch CPU |
 | 当前阶段 | 基线尚未运行，索引尚未构建，API 尚未搭建 |
 
 ---
 
 ## 目录结构
 
 ```
 tcg-embedding-service/
 ├── images/          # 卡牌图片（9434 张有效，1 张损坏）
 ├── csv/             # 元数据、审计结果、评估数据
 ├── doc/             # 文档（PRD、设计、实施计划、报告）
 ├── index/           # embedding 索引（待构建）
 ├── model/           # 微调后模型权重（待创建）
 ├── script_temp/     # 一次性脚本和工具脚本
 ├── app/             # API 服务（待创建）
 ├── AGENTS.md        # 本文件
 ├── .gitignore       # 忽略数据文件、缓存、模型权重
 └── requirements.txt # 依赖列表
 ```
 
 **自定义规则**（优先级高于通用规则）：
 1. `*.py` 脚本放在 `script_temp/` 下
 2. `*.md` 文档放在 `doc/` 下
 3. `*.csv` 数据文件放在 `csv/` 下
 4. 索引文件放在 `index/` 下
 5. 修改 `.yml` 时（Dify agent 配置），必须做 YAML 语法 + Dify DSL 结构校验
 
 ---
 
 ## 数据约定
 
 ### 图片
 - 来源：`images/` 目录，全部为 `_200w.jpg` 格式的缩略图
 - 损坏图片：`153316_200w.jpg`（0 字节），已在 csv/metadata.csv 中排除
 - 方向：8888 张竖版、546 张横版（疑似旋转 90° 的竖卡）
 - 重复 SHA1：51 组（118 张），不同卡号但图像内容完全一致
 - 预处理时用 `preprocess.orientation_candidates()` 处理横版图（双方向候选）
 
 ### 元数据
 - `csv/metadata.csv`：name, width, height, orientation, rotation_advice, bytes, mode, sha1
 - `csv/data_audit_summary.csv`：汇总统计（total, corrupt, portrait, landscape, duplicate_sha1）
 
 ### 索引
 - `index/embeddings.npy`：9434×768 float32，L2 归一化
 - `index/ids.json`：对应 card_id 列表
 - 索引版本号记录在 `index/version.txt`
 
 ---
 
 ## 关键设计决策
 
 1. **DINOv2 路线的选择理由**：自监督视觉特征，无需标注数据即可做检索基准；CLS token 768 维 embedding 足够区分 9.4k 张卡。
 2. **不先微调**：先跑裸 DINOv2 基线，根据基线数字决定是否微调。基线 top-1 < 60% 则直接微调。
 3. **暴力检索而非 ANN**：9.4k 向量，faiss IndexFlatIP 在 CPU 上 < 5ms，目前不需要 ANN。
 4. **预处理与索引走同一代码路径**：gallery 和 query 共享 `preprocess.py`，保证数据分布一致。
 5. **拒绝策略**：top-1 分数 ≥ τ 且 top-1 与 top-2 分差 ≥ m，τ 和 m 通过校准确定。
 6. **双方向推理**：横版图同时尝试 90° 和 270° 旋转，取最高分方向。
 7. **API 接口**：POST /v1/match（multipart），返回 {status, card_id, score, margin}。
 
 ---
 
 ## 当前任务状态
 
 完整任务跟踪见 [doc/implementation-plan.md](doc/implementation-plan.md)。
 
 | 任务 | 状态 | 负责人 | 优先级 |
 |------|------|--------|--------|
 | Task 1: 修 bug + 跑基线 | 待开始 | Codex | P0 |
 | Task 2: 数据治理 | 待开始 | Codex | P0 |
 | Task 3: 构建索引 | 待开始 | Codex | P0 |
 | Task 4: 正式基线评估 | 待开始 | Codex | P0 |
 | Task 5: 阈值校准 | 待开始 | Codex | P0 |
 | Task 6: 预处理管线完善 | 待开始 | Codex | P1 |
 | Task 7: API 服务 | 待开始 | Codex | P1 |
 | Task 8: 微调 | 待开始 | Codex | P2 |
 | Task 9: 真实照片验收 | 待开始 | 用户 | P2 |
 
 ---
 
 ## 已知问题
 
 1. **02_baseline_eval.py bug**：persp_coeffs 函数 row 3 和 row 7 的 -x3*H / -y3*H 被错误放在 g 列（index 6），应放在 h 列（index 7）。非恒等变换下透视变换错误。
 2. **51 组重复 SHA1**：不同卡号共用同一张图，模型无法区分，需要标记。
 3. **200px 分辨率上限**：不支持读取卡号/系列标志等细粒度信息，可能成为准确率天花板。
 4. **无 GPU**：当前环境 CPU-only，微调需要阿里云 GPU。
 5. **无真实照片数据**：阈值校准只能用模拟数据，上线后可能需要调整。
 
 ---
 
 ## 代码风格
 
 1. 遵循已有命名风格（snake_case 函数/变量，PascalCase 类）
 2. 所有脚本可独立运行（`if __name__ == "__main__"`）
 3. 脚本参数使用 argparse
 4. 路径使用 os.path 构建，避免硬编码
 5. 临时文件放在 `script_temp/` 下
 6. 文档用 UTF-8 编码
 
 ---
 
 ## 参考文档
 
 | 文档 | 内容 |
 |------|------|
 | [doc/PRD.md](doc/PRD.md) | 产品需求文档 |
 | [doc/design.md](doc/design.md) | 技术设计文档 |
 | [doc/implementation-plan.md](doc/implementation-plan.md) | 实施计划与任务跟踪 |
 | [doc/tcg-visual-match-plan-v1.md](doc/tcg-visual-match-plan-v1.md) | 技术方案 v1 |
 | [doc/tcg-visual-match-v3-status-and-tasks.md](doc/tcg-visual-match-v3-status-and-tasks.md) | 现状分析与任务拆解 v3 |
 | [csv/metadata.csv](csv/metadata.csv) | 图片元数据 |
 | [csv/data_audit_summary.csv](csv/data_audit_summary.csv) | 数据审计摘要 |
