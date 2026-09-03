# TCG Match Service — CPU 镜像
# 可选 GPU（安装 torch 时自动检测 CUDA）
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    USE_GPU=false \
    DATA_DIR=/data \
    MODEL_DIR=/models \
    BGE_MODEL_PATH=/models/bge_model \
    PPOCR_MODEL_DIR=/models/ppocr_models \
    PORT=8056

# 系统依赖（OpenCV + PaddleOCR 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ app/
COPY scripts/ scripts/

# 创建数据/模型目录
RUN mkdir -p /data /models

# 启动脚本
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8056

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["serve"]