path = r"D:\Code2026\tcg-embedding-service\script_temp\02_baseline_eval.py"
lines = open(path, "r", encoding="utf-8").readlines()
new_lines = []
in_func = False
for i, line in enumerate(lines):
    if line.strip().startswith("def embed_images"):
        in_func = True
    if in_func and line.strip().startswith("def ") and "embed_images" not in line:
        in_func = False
    if in_func and line.strip().startswith("for i in range(0, len(imgs), batch):"):
        indent = line[:len(line)-len(line.lstrip())]
        new_lines.append(line)
        new_lines.append(indent + "    if i % (batch * 50) == 0:\n")
        new_lines.append(indent + '        print(f"  embedding {i}/{len(imgs)}", flush=True)\n')
    else:
        new_lines.append(line)
open(path, "w", encoding="utf-8").writelines(new_lines)
for i, line in enumerate(open(path, "r", encoding="utf-8"), 1):
    if "embedding" in line or "embed_images" in line or "for i in range" in line:
        print(f"L{i}: {line.rstrip()}")
print("Done")
