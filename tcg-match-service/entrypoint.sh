#!/bin/bash
set -e

# 检查索引是否需要构建（任意品类有 visual-index 即可）
if ! find "${DATA_DIR}" -name "embeddings.npy" -path "*/visual-index/*" 2>/dev/null | head -1 | grep -q .; then
    echo "=============================================="
    echo "Visual index not found, building indexes..."
    echo "=============================================="
    python scripts/build_index.py --category all --type all
fi

echo "=============================================="
echo "Starting TCG Match Service on port ${PORT}..."
echo "  GPU: ${USE_GPU}"
echo "  Data: ${DATA_DIR}"
echo "  Models: ${MODEL_DIR}"
echo "=============================================="

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --workers 1