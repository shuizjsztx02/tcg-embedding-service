# TCG Match Service — 运维指南

## 目录

- [一、扩展品类数据](#一扩展品类数据)
- [二、部署到服务器](#二部署到服务器)
- [三、测试与调用](#三测试与调用)
- [四、常见问题](#四常见问题)

---

## 一、扩展品类数据

### 1.1 数据目录结构

每个品类在 `DATA_DIR`（默认 `/data`）下独立一个子目录，按以下结构组织：

```
/data/
├── <品类标识>/                    # 如 pokemon、magic、yugioh
│   ├── images/                    # 卡牌图片目录
│   │   ├── 100503_200w.jpg
│   │   ├── 100504_200w.jpg
│   │   └── ...
│   ├── products.jsonl             # 产品元数据
│   ├── visual-index/              # DINOv2 视觉索引（构建后生成）
│   │   ├── embeddings.npy
│   │   ├── ids.json
│   │   └── version.txt
│   └── text-index/                # BGE 文本索引（构建后生成）
│       ├── embeddings.npy
│       ├── ids.json
│       └── version.txt
```

### 1.2 品类标识命名规范

品类标识使用小写英文字母 + 下划线，禁止空格和特殊字符：

| 品类标识 | 对应品类 |
|----------|----------|
| `pokemon` | Pokémon TCG |
| `pokemon_japan` | Pokémon Japan |
| `magic` | Magic: The Gathering |
| `yugioh` | Yu-Gi-Oh! |
| `onepiece` | One Piece Card Game |
| `disney_lorcana` | Disney Lorcana |
| `flesh_blood` | Flesh and Blood |
| `dragon_ball` | Dragon Ball Super |

### 1.3 图片文件要求

图片命名规则：
- 文件名 = 产品 ID + `_200w.jpg`（兼容原项目约定）
- 示例：`676008_200w.jpg`
- 图片应已做预处理（裁切、透视矫正、方向修正），服务器不再做任何预处理

图片格式规范：
- 格式：JPEG（推荐）或 PNG
- 分辨率：建议 504×704 像素以上
- 色彩：RGB，非 CMYK

### 1.4 products.jsonl 格式说明

每行一个 JSON 对象，UTF-8 编码。核心字段：

```json
{
  "productId": 676008,
  "productName": "Night Stretcher",
  "setName": "ME: Ascended Heroes",
  "setCode": "ASC",
  "rarityName": "Common",
  "customAttributes": {
    "description": "Put 2 Basic Energy cards from your discard pile into your hand.",
    "stage": null,
    "cardTypeB": "Trainer - Item",
    "hp": null,
    "attack1": "Draw 2 cards",
    "attack2": null,
    "number": "196/217",
    "flavorText": ""
  }
}
```

**构建文档时会被使用的字段：** `productName`、`stage`、`cardTypeB`/`energyType`、`hp`、`attack1~4`、`description`、`flavorText`、`number`、`setName`、`rarityName`。其中 `productId` 作为唯一标识。

### 1.5 完整扩展流程（以新增 One Piece 品类为例）

**步骤 1：准备数据**

在服务器上创建品类数据目录：
```bash
# 假设 DATA_DIR 挂载在 /data
mkdir -p /data/onepiece/images
```

将 One Piece 的卡牌图片放入 `/data/onepiece/images/`，products.jsonl 放入 `/data/onepiece/`。

**步骤 2：构建索引**

```bash
# 方式一：使用 Docker 构建
docker compose run --rm tcg-match python scripts/build_index.py \
  --category onepiece --type all

# 方式二：只构建视觉索引（如果还没有 products.jsonl）
docker compose run --rm tcg-match python scripts/build_index.py \
  --category onepiece --type visual

# 方式三：只构建文本索引（如果图片已有索引）
docker compose run --rm tcg-match python scripts/build_index.py \
  --category onepiece --type text
```

**步骤 3：验证索引**

构建完成后，检查目录结构：
```bash
ls -la /data/onepiece/visual-index/
# 应包含：embeddings.npy  ids.json  version.txt

ls -la /data/onepiece/text-index/
# 应包含：embeddings.npy  ids.json  version.txt
```

**步骤 4：重启服务加载新品类**

```bash
docker compose restart tcg-match
```

**步骤 5：验证服务端已加载**

```bash
curl http://localhost:8056/v1/health
# 响应中应包含 onepiece 的索引信息：
# {"status":"ok","categories":["pokemon","onepiece",...],
#  "dino_index_sizes":{"pokemon":9434,"onepiece":3000,...},
#  "text_index_sizes":{"pokemon":5000,"onepiece":1500,...}}
```

**步骤 6：前端添加品类选项（可选）**

编辑 `app/static/index.html`，在品类下拉选择器中添加：
```html
<option value="onepiece">One Piece</option>
```

需要重新构建镜像：
```bash
docker compose build
docker compose up -d
```

### 1.6 批量构建所有品类

```bash
# 自动扫描 DATA_DIR 下所有品类并构建
docker compose --profile build run build-index
```

此命令会遍历 `/data/` 下的每个子目录，对每个目录尝试构建视觉和文本索引。如果某个品类缺少图片目录或 products.jsonl，会自动跳过。

---

## 二、部署到服务器

### 2.1 服务器要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|---------|---------|
| CPU | 4 核 | 8 核 |
| 内存 | 8 GB | 16 GB |
| 磁盘 | 50 GB | 100 GB |
| GPU（可选） | NVIDIA GPU 6GB+ | NVIDIA A10/RTX 3090+ |
| 软件 | Docker 24+、Docker Compose v2 | 同左 |
| 操作系统 | Linux (Ubuntu 22.04+) | 同左 |

### 2.2 首次部署流程

**步骤 1：服务器安装 Docker**

```bash
# Ubuntu 22.04
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker
```

**步骤 2：获取项目**

```bash
# 将项目文件复制到服务器
# 方式一：git clone
git clone <仓库地址> /opt/tcg-match-service
cd /opt/tcg-match-service

# 方式二：直接 scp 上传
# scp -r tcg-match-service/ user@server:/opt/tcg-match-service
```

**步骤 3：准备数据和模型**

```bash
# 创建数据目录
mkdir -p /opt/tcg-match-service/data/pokemon/images
mkdir -p /opt/tcg-match-service/models

# 上传数据到 /opt/tcg-match-service/data/
# 上传模型到 /opt/tcg-match-service/models/

# 最终目录结构：
# /opt/tcg-match-service/
# ├── data/
# │   ├── pokemon/
# │   │   ├── images/
# │   │   └── products.jsonl
# │   ├── magic/
# │   │   └── ...
# │   └── ...
# ├── models/
# │   ├── bge_model/
# │   └── ppocr_models/
# ├── docker-compose.yml
# ├── Dockerfile
# └── ...
```

**步骤 4：构建镜像**

```bash
cd /opt/tcg-match-service
docker compose build
```

**步骤 5：构建索引并启动**

```bash
# 先构建索引
docker compose --profile build run build-index

# 启动服务
docker compose up -d
```

**步骤 6：验证服务**

```bash
# 健康检查
curl http://localhost:8056/v1/health
# 期望响应：{"status":"ok","categories":["pokemon"],"dino_index_sizes":{"pokemon":9434},...}

# 查看日志
docker compose logs -f
```

### 2.3 生产部署建议

**配置 systemd 服务（可选）**

创建 `/etc/systemd/system/tcg-match.service`：

```ini
[Unit]
Description=TCG Match Service
Requires=docker.service
After=docker.service

[Service]
WorkingDirectory=/opt/tcg-match-service
ExecStart=/usr/bin/docker compose up
ExecStop=/usr/bin/docker compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now tcg-match
```

**资源限制**

在 `docker-compose.yml` 中已配置 8GB 内存限制。如需调整：

```yaml
deploy:
  resources:
    limits:
      memory: 16G   # 改为 16GB
      cpus: '8'      # 限制 8 核
```

**GPU 部署**

确保服务器已安装 NVIDIA 驱动和 nvidia-container-toolkit：

```bash
# 安装 NVIDIA 容器运行时
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker

# 启动 GPU 服务
docker compose up -d tcg-match-gpu
```

**日志管理**

```bash
# 查看实时日志
docker compose logs -f --tail 100

# 日志轮转（docker-compose.yml 中配置）
# 在 volumes 段添加：
#   - /var/log/tcg-match:/app/logs
```

### 2.4 更新服务

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker compose build

# 重新启动
docker compose up -d
```

### 2.5 备份与恢复

**需要备份的数据：**
- `data/` 目录下的所有品类数据（images + products.jsonl + 构建后的索引）
- `models/` 目录下的模型文件

**备份命令：**
```bash
tar -czf tcg-match-backup-$(date +%Y%m%d).tar.gz \
  data/ models/ docker-compose.yml
```

---

## 三、测试与调用

### 3.1 健康检查

```bash
curl http://localhost:8056/v1/health
```

**成功响应：**
```json
{
  "status": "ok",
  "categories": ["pokemon"],
  "dino_index_sizes": {"pokemon": 9434},
  "text_index_sizes": {"pokemon": 5000}
}
```

### 3.2 DINO 视觉匹配

**请求：**
```bash
curl -X POST http://localhost:8056/v1/dino-match \
  -F "file=@/path/to/test_card.jpg" \
  -F "category=pokemon" \
  -F "top_k=5"
```

**成功响应：**
```json
{
  "status": "ok",
  "category": "pokemon",
  "query_time_ms": 185.3,
  "results": [
    {
      "rank": 1,
      "card_id": "100503_200w",
      "score": 0.9123,
      "product_name": "Pikachu ex",
      "product": {
        "productId": 100503,
        "productName": "Pikachu ex",
        "setName": "Paldea Evolved",
        "rarityName": "Ultra Rare",
        "customAttributes": {
          "number": "219/193",
          "cardTypeB": "Pokémon - ex",
          "hp": "200"
        }
      }
    },
    {
      "rank": 2,
      "card_id": "100504_200w",
      "score": 0.8456,
      "product_name": "Raichu",
      "product": { ... }
    }
  ]
}
```

**参数说明：**
- `file`：已预处理的卡牌图片（JPEG/PNG）
- `category`：品类标识，默认 `pokemon`
- `top_k`：返回结果数，默认 5，最大 20

**图片获取：**
```bash
# 获取匹配结果的卡牌图片
curl -o result.jpg http://localhost:8056/v1/images/pokemon/100503_200w.jpg
```

### 3.3 OCR 文字匹配

**请求：**
```bash
curl -X POST http://localhost:8056/v1/ocr-match \
  -F "file=@/path/to/test_card.jpg" \
  -F "category=pokemon" \
  -F "top_k=5"
```

**成功响应：**
```json
{
  "status": "ok",
  "category": "pokemon",
  "full_text": "Pikachu ex\nElectric Pokémon\nHP 200\nThunderbolt 180\nWeakness: Fighting\nRetreat: 1",
  "query_text": "Pikachu ex\nElectric Pokémon\nHP 200\nThunderbolt 180",
  "query_time_ms": 1250.4,
  "warnings": [],
  "results": [
    {
      "rank": 1,
      "product_id": "100503",
      "product_name": "Pikachu ex",
      "set_name": "Paldea Evolved",
      "number": "219/193",
      "rarity": "Ultra Rare",
      "score": 0.8945,
      "has_image": true,
      "product": { ... }
    }
  ]
}
```

**字段说明：**
- `full_text`：OCR 识别的全部文字（含低置信度）
- `query_text`：清洗后用于向量匹配的可靠文字（置信度 >= 0.75）
- `warnings`：警告信息（如低置信度文字、未识别到文字等）
- `results`：Top-5 匹配结果

### 3.4 Python 客户端调用示例

```python
import requests

API_BASE = "http://localhost:8056"

# ---- DINO 视觉匹配 ----
def dino_match(image_path: str, category: str = "pokemon") -> dict:
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/v1/dino-match",
            files={"file": f},
            data={"category": category, "top_k": 5},
        )
    return resp.json()

# ---- OCR 文字匹配 ----
def ocr_match(image_path: str, category: str = "pokemon") -> dict:
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/v1/ocr-match",
            files={"file": f},
            data={"category": category, "top_k": 5},
        )
    return resp.json()

# ---- 使用示例 ----
result = dino_match("test_card.jpg", "pokemon")
print(f"Top-1: {result['results'][0]['product_name']} (score: {result['results'][0]['score']:.4f})")

# 获取结果图片
card_id = result['results'][0]['card_id']
img_resp = requests.get(f"{API_BASE}/v1/images/pokemon/{card_id}")
with open(f"result_{card_id}.jpg", "wb") as f:
    f.write(img_resp.content)
```

### 3.5 批量测试脚本

保存为 `batch_test.py`：

```python
"""批量测试 TCG Match Service 的视觉和 OCR 匹配效果。"""
import argparse
import json
import os
import time
import requests


def test_category(api_base: str, test_dir: str, category: str):
    """对品类下所有测试图片运行 DINO 和 OCR 匹配。"""
    results = {"category": category, "dino": [], "ocr": []}

    for fname in sorted(os.listdir(test_dir)):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(test_dir, fname)
        print(f"  [{category}] {fname}...", end=" ", flush=True)

        # DINO 匹配
        try:
            with open(path, "rb") as f:
                t0 = time.time()
                resp = requests.post(
                    f"{api_base}/v1/dino-match",
                    files={"file": f},
                    data={"category": category},
                )
                dt = time.time() - t0
                data = resp.json()
                top1 = data["results"][0] if data.get("results") else None
                results["dino"].append({
                    "file": fname, "time_ms": round(dt * 1000, 1),
                    "top1_id": top1["card_id"] if top1 else None,
                    "top1_score": top1["score"] if top1 else None,
                })
                print(f"dino: {top1['product_name'] if top1 else 'N/A'}", end=" | ", flush=True)
        except Exception as e:
            print(f"dino ERR: {e}", end=" | ", flush=True)

        # OCR 匹配
        try:
            with open(path, "rb") as f:
                t0 = time.time()
                resp = requests.post(
                    f"{api_base}/v1/ocr-match",
                    files={"file": f},
                    data={"category": category},
                )
                dt = time.time() - t0
                data = resp.json()
                top1 = data["results"][0] if data.get("results") else None
                results["ocr"].append({
                    "file": fname, "time_ms": round(dt * 1000, 1),
                    "query_text": data.get("query_text", ""),
                    "top1_id": top1["product_id"] if top1 else None,
                    "top1_score": top1["score"] if top1 else None,
                })
                print(f"ocr: {top1['product_name'] if top1 else 'N/A'}")
        except Exception as e:
            print(f"ocr ERR: {e}")

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://localhost:8056")
    ap.add_argument("--test-dir", required=True, help="测试图片目录")
    ap.add_argument("--category", default="pokemon")
    ap.add_argument("--output", default="test_results.json")
    args = ap.parse_args()

    print(f"Testing {args.category} against {args.api}...")
    results = test_category(args.api, args.test_dir, args.category)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
```

```bash
# 使用示例
python batch_test.py --test-dir ./test_images --category pokemon --output results.json
```

### 3.6 前端测试

启动服务后，在浏览器中访问 `http://<服务器IP>:8056/` 即可使用图形界面：

1. 选择品类（下拉框）
2. 拖放或点击选择卡牌图片
3. 点击"DINO 匹配 Top-5"或"OCR 文字匹配 Top-5"
4. 查看结果列表和详情

---

## 四、常见问题

### Q1: 启动后 `/v1/health` 返回的空结果

**原因：** 数据目录未挂载或品类索引未构建。

**检查：**
```bash
# 检查容器内数据目录
docker compose exec tcg-match ls /data/

# 检查索引文件是否存在
docker compose exec tcg-match ls /data/pokemon/visual-index/embeddings.npy
```

**解决：** 运行索引构建命令：
```bash
docker compose --profile build run build-index
```

### Q2: "Category 'xxx' not found" 错误

**原因：** 请求的品类未加载到服务中。

**检查：**
```bash
curl http://localhost:8056/v1/health | python -m json.tool
# 查看 categories 字段是否包含该品类
```

**解决：** 确保品类索引已构建，然后重启服务：
```bash
docker compose restart tcg-match
```

### Q3: 内存不足

**原因：** 多个模型同时加载（DINOv2 ~1.5GB、BGE ~0.5GB、PP-OCRv4 ~0.3GB）需要至少 4GB 内存。

**解决：**
- 缩小 `docker-compose.yml` 中其他服务的资源限制
- 增加服务器内存
- 使用 `memory: 8G` 限制并增加 swap

### Q4: OCR 识别不到文字

**原因：** 图片未做预处理，PP-OCRv4 对原图直接识别率受图片质量影响。

**检查：** 查看响应的 `warnings` 字段。

**解决：** 确保客户端传图前已做预处理（裁切、透视矫正、方向修正）。

### Q5: DINO 匹配分数偏低

**原因：** 上传图片与索引图片的预处理标准不一致（如未做同样的方向修正和缩放）。

**解决：** 确保客户端预处理与离线索引构建时的预处理保持一致（方向修正规则、分辨率等）。

### Q6: 如何定位问题

```bash
# 查看容器日志
docker compose logs -f

# 进入容器调试
docker compose exec tcg-match bash

# 重启服务
docker compose restart tcg-match

# 完全重建
docker compose down -v
docker compose build --no-cache
docker compose up -d
```