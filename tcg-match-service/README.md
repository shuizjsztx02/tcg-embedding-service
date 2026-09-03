# TCG Match Service

TCG 卡牌多品类视觉 + 文字匹配服务（Docker 部署）

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│  客户端     │     │  TCG Match   │     │   数据目录      │
│  (品类识别) │────▶│  Service     │────▶│  /data/         │
│  预处理     │     │  API:8056    │     │  ├─pokemon/     │
└─────────────┘     │              │     │  │ ├─images/    │
                    │  DINOv2      │     │  │ ├─products.jsonl
                    │  PP-OCRv4    │     │  │ ├─visual-index/
                    │  BGE-small    │     │  │ └─text-index/
                    └──────────────┘     │  ├─magic/       │
                                         │  └─.../         │
                                         └────────────────┘
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 测试前端 |
| GET | `/v1/health` | 健康检查 |
| POST | `/v1/dino-match` | DINOv2 视觉匹配 Top-5 |
| POST | `/v1/ocr-match` | OCR 文字匹配 Top-5 |
| GET | `/v1/images/{category}/{card_id}` | 获取卡牌图片 |

### 请求参数

**`POST /v1/dino-match`**
- `file` (multipart): 已预处理卡牌图片
- `category` (form, default: "pokemon"): 品类标识
- `top_k` (form, default: 5): 返回结果数

**`POST /v1/ocr-match`**
- `file` (multipart): 已预处理卡牌图片
- `category` (form, default: "pokemon"): 品类标识
- `top_k` (form, default: 5): 返回结果数

## 快速开始

### 1. 准备数据

按品类组织数据目录：

```
data/
├── pokemon/
│   ├── images/              # 卡牌图片 (*.jpg, *_200w.jpg)
│   ├── products.jsonl       # 产品元数据
│   ├── visual-index/        # 构建后自动生成
│   └── text-index/          # 构建后自动生成
├── magic/
│   ├── images/
│   ├── products.jsonl
│   ├── visual-index/
│   └── text-index/
└── ...
```

### 2. 准备模型

```
models/
├── bge_model/              # BAAI/bge-small-en-v1.5
│   ├── pytorch_model.bin
│   ├── config.json
│   └── ...
└── ppocr_models/
    ├── ch_PP-OCRv4_det_infer/
    │   ├── inference.pdmodel
    │   └── inference.pdiparams
    ├── ch_PP-OCRv4_rec_infer/
    │   ├── inference.pdmodel
    │   └── inference.pdiparams
    └── ppocr_keys_v1.txt
```

### 3. 构建索引

```bash
# 构建所有品类索引
docker compose --profile build run build-index

# 或手动构建单个品类
docker compose run --rm tcg-match python scripts/build_index.py --category pokemon --type all
```

### 4. 启动服务

```bash
# CPU 模式
docker compose up -d

# GPU 模式（需要 NVIDIA 运行时）
# 编辑 docker-compose.yml 取消 GPU 服务注释后：
docker compose up -d tcg-match-gpu
```

### 5. 测试

```bash
# 健康检查
curl http://localhost:8056/v1/health

# DINO 视觉匹配
curl -X POST http://localhost:8056/v1/dino-match \
  -F "file=@test.jpg" \
  -F "category=pokemon"

# OCR 文字匹配
curl -X POST http://localhost:8056/v1/ocr-match \
  -F "file=@test.jpg" \
  -F "category=pokemon"
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `USE_GPU` | `false` | 启用 GPU 推理 |
| `MATCH_TAU` | `0.775` | 匹配阈值 |
| `MATCH_MARGIN` | `0.02` | 匹配边际 |
| `PORT` | `8056` | 服务端口 |
| `DATA_DIR` | `/data` | 品类数据根目录 |
| `MODEL_DIR` | `/models` | 模型根目录 |
| `BGE_MODEL_PATH` | `/models/bge_model` | BGE 模型路径 |
| `PPOCR_MODEL_DIR` | `/models/ppocr_models` | PP-OCR 模型路径 |

## 品类支持

| 品类标识 | 说明 |
|----------|------|
| `pokemon` | Pokémon TCG |
| `pokemon_japan` | Pokémon Japan |
| `magic` | Magic: The Gathering |
| `yugioh` | Yu-Gi-Oh! |
| `onepiece` | One Piece |
| `disney_lorcana` | Disney Lorcana |
| `flesh_blood` | Flesh and Blood |
| `dragon_ball` | Dragon Ball Super |

## 开发说明

### 新增品类

1. 在 `data/` 下创建品类目录（如 `data/onepiece/`）
2. 放入 `images/`（卡牌图片）和 `products.jsonl`（产品元数据）
3. 运行 `python scripts/build_index.py --category onepiece --type all`
4. 在 `index.html` 的品类选择器中添加选项

### 本地运行（无需 Docker）

```bash
pip install -r requirements.txt
python scripts/build_index.py --category pokemon --type all
python -m app.main
```