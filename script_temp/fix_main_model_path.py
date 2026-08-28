import os
content = open("D:/Code2026/tcg-embedding-service/app/main.py", "r", encoding="utf-8").read()
content = content.replace(
    'BGE_MODEL_NAME = "C:/Users/admin/.cache/huggingface/hub/models--BAAI--bge-small-en-v1.5/snapshots/5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"',
    'BGE_MODEL_NAME = "D:/Code2026/tcg-embedding-service/script_temp/bge_model"'
)
open("D:/Code2026/tcg-embedding-service/app/main.py", "w", encoding="utf-8").write(content)
print("OK")
