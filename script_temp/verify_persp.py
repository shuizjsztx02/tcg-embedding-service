"""Verify persp_coeffs produces correct PIL perspective transforms."""
import sys, os, importlib.util, numpy as np
from PIL import Image

spec = importlib.util.spec_from_file_location(
    "baseline_eval",
    r"D:\Code2026\tcg-embedding-service\script_temp\02_baseline_eval.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
persp_coeffs = mod.persp_coeffs

# Test 1: Identity quad
W, H = 200, 300
ident_quad = [(0, 0), (W, 0), (W, H), (0, H)]
c = persp_coeffs(ident_quad, (W, H))
assert abs(c[0] - 1.0) < 1e-6
assert abs(c[4] - 1.0) < 1e-6
assert abs(c[2]) < 1e-6 and abs(c[5]) < 1e-6
for i, v in enumerate(c):
    if i not in (0, 4):
        assert abs(v) < 1e-6, f"coeff[{i}] should be 0, got {v}"
print("Test 1 PASS: identity quad")

# Test 2: Non-identity quad
W, H = 200, 300
grad = np.zeros((H, W, 3), dtype=np.uint8)
grad[:,:,0] = (np.arange(W, dtype=np.float32) / (W-1) * 255).astype(np.uint8)
grad[:,:,1] = (np.arange(H, dtype=np.float32).reshape(-1, 1) / (H-1) * 255).astype(np.uint8)
grad[:,:,2] = 128
src = Image.fromarray(grad, "RGB")

quad = [(5, 10), (185, 8), (190, 285), (3, 278)]
dst = src.transform((W, H), Image.PERSPECTIVE, persp_coeffs(quad, (W, H)),
                    Image.BICUBIC, fillcolor=(0, 0, 0))

corners = [(0, 0), (W-1, 0), (W-1, H-1), (0, H-1)]
cnames = ["top-left", "top-right", "bottom-right", "bottom-left"]
ok = True
for (cx, cy), name, (sx, sy) in zip(corners, cnames, quad):
    out_px = dst.getpixel((cx, cy))
    src_expected = (int(sx / (W-1) * 255), int(sy / (H-1) * 255), 128)
    dr = abs(out_px[0] - src_expected[0])
    dg = abs(out_px[1] - src_expected[1])
    if dr > 4 or dg > 4:
        print(f"  {name}: got {out_px}, expected ~{src_expected}, diff=({dr},{dg})")
        ok = False
    else:
        print(f"  {name}: got {out_px}, expected ~{src_expected} OK")

if ok:
    print("Test 2 PASS: non-identity quad")
else:
    print("Test 2 FAIL"); exit(1)

print("All tests PASS.")
