import os
content = open("D:/Code2026/tcg-embedding-service/app/main.py", "r", encoding="utf-8").read()
content = content.replace('"low_cpu_mem_usage": True', '"use_safetensors": False')
open("D:/Code2026/tcg-embedding-service/app/main.py", "w", encoding="utf-8").write(content)
print("OK")
