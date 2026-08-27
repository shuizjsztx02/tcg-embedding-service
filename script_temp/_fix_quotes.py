import sys
with open("D:\Code2026\tcg-embedding-service\script_temp\_write_html.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(len(lines)):
    line = lines[i]
    # Fix 1: unescaped single quotes in JS string concatenation
    if chr(0x27) + chr(0x29) + chr(0x22) + chr(0x27) + chr(0x20) + chr(0x2B) + chr(0x20) + chr(0x27) + chr(0x22) + chr(0x3E) + chr(0x27) in line:
        lines[i] = line.replace(
            chr(0x27) + chr(0x29) + chr(0x22) + chr(0x27) + chr(0x20) + chr(0x2B) + chr(0x20) + chr(0x27) + chr(0x22) + chr(0x3E) + chr(0x27),
            chr(0x5C) + chr(0x78) + chr(0x32) + chr(0x37) + chr(0x29) + chr(0x22) + chr(0x5C) + chr(0x78) + chr(0x32) + chr(0x37) + chr(0x20) + chr(0x2B) + chr(0x20) + chr(0x5C) + chr(0x78) + chr(0x32) + chr(0x37) + chr(0x22) + chr(0x3E) + chr(0x5C) + chr(0x78) + chr(0x32) + chr(0x37)
        )
    # Fix 2: backslash-single-quote in displaySearchResult
    pattern = chr(0x5C) + chr(0x5C) + chr(0x27) + "none" + chr(0x5C) + chr(0x5C) + chr(0x27)
    if pattern in line:
        lines[i] = line.replace(
            pattern,
            chr(0x5C) + chr(0x5C) + chr(0x78) + chr(0x32) + chr(0x37) + "none" + chr(0x5C) + chr(0x5C) + chr(0x78) + chr(0x32) + chr(0x37)
        )
with open("D:\Code2026\tcg-embedding-service\script_temp\_write_html.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Fixed")
