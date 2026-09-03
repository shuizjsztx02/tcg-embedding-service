# -*- coding: utf-8 -*-
"""T-1 基准: LLM 品类判断准确率 + 延迟 (在线策略 S1 层假设验证)

从 category_cards_final 各品类 gallery 抽样缩略图, 调用本地 LLM 端点做品类判断,
对比 ground truth 统计准确率与延迟。

用法: python script_temp/bench_category_llm.py [--per-category 6]
"""
import argparse
import base64
import io
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from PIL import Image

API_URL = "http://127.0.0.1:15721/v1/messages"
MODEL = "qwen3.7-flash"
DATA_ROOT = os.path.join(os.path.dirname(__file__), "..", "category_cards_final", "category_cards")

# 目录名 -> 服务端品类标识 (ground truth)
DIR_TO_CATEGORY = {
    "01_Magic": "magic",
    "02_YuGiOh": "yugioh",
    "03_Pokemon": "pokemon",
    "62_Flesh_and_Blood_TCG": "flesh_blood",
    "68_One_Piece_Card_Game": "onepiece",
    "71_Disney_Lorcana": "disney_lorcana",
    "80_Dragon_Ball_Super_Fusion_World": "dragon_ball",
}

PROMPT_TMPL = (
    "你是一个 TCG 卡牌专家。判断图片中的卡牌属于哪个卡牌游戏。\n"
    "候选品类: {candidates}\n"
    "请仅回复 JSON: {{\"category\": \"<候选之一>\", \"confidence\": <0-1>}}"
)


def load_sample(dir_name, k, seed):
    img_dir = os.path.join(DATA_ROOT, dir_name, "images")
    if not os.path.isdir(img_dir):
        return []
    files = [f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.Random(seed).shuffle(files)
    return [(dir_name, os.path.join(img_dir, f)) for f in files[:k]]


def call_llm(b64):
    candidates = ", ".join(sorted(set(DIR_TO_CATEGORY.values())))
    t0 = time.time()
    resp = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": MODEL,
            "max_tokens": 100,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT_TMPL.format(candidates=candidates)},
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
            ]}],
        },
        timeout=30,
    )
    resp.raise_for_status()
    text = "".join(b.get("text", "") for b in resp.json().get("content", []) if b.get("type") == "text")
    return text, (time.time() - t0) * 1000, resp.json().get("model", "?")


def to_b64(path):
    with Image.open(path) as img:
        img = img.convert("RGB")
        w, h = img.size
        scale = 512 / max(w, h)
        if scale < 1:
            img = img.resize((int(w * scale), int(h * scale)))
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode()


def parse_category(text):
    try:
        obj = json.loads(text.strip().removeprefix("```json").removesuffix("```"))
        return obj.get("category", ""), obj.get("confidence")
    except Exception:
        return "", None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-category", type=int, default=6)
    args = ap.parse_args()

    samples = []
    for dir_name in DIR_TO_CATEGORY:
        samples += load_sample(dir_name, args.per_category, seed=42)
    print(f"采样 {len(samples)} 张, 品类 {len(DIR_TO_CATEGORY)} 个")

    results = []

    def work(item):
        dir_name, path = item
        gt = DIR_TO_CATEGORY[dir_name]
        try:
            b64 = to_b64(path)
            text, ms, served_model = call_llm(b64)
            pred, conf = parse_category(text)
            return {"gt": gt, "pred": pred, "conf": conf, "ms": round(ms), "model": served_model,
                    "ok": pred == gt, "file": os.path.basename(path)}
        except Exception as e:
            return {"gt": gt, "pred": "error", "conf": None, "ms": None, "model": "", "ok": False,
                    "file": os.path.basename(path), "err": str(e)[:120]}

    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(work, samples))

    n_ok = sum(1 for r in results if r["ok"])
    lat = [r["ms"] for r in results if r["ms"]]
    print(f"\n准确率: {n_ok}/{len(results)} = {n_ok / len(results):.1%}")
    if lat:
        lat.sort()
        print(f"延迟(ms): avg={sum(lat) / len(lat):.0f} p50={lat[len(lat) // 2]} p90={lat[int(len(lat) * 0.9)]}")
    print(f"服务端模型: {sorted(set(r['model'] for r in results))}")

    print("\n按品类:")
    for gt in sorted(set(DIR_TO_CATEGORY.values())):
        rows = [r for r in results if r["gt"] == gt]
        ok = sum(1 for r in rows if r["ok"])
        preds = {}
        for r in rows:
            preds[r["pred"]] = preds.get(r["pred"], 0) + 1
        print(f"  {gt:15s} {ok}/{len(rows)}  预测分布: {preds}")

    print("\n错误明细:")
    for r in results:
        if not r["ok"]:
            print(f"  gt={r['gt']} pred={r['pred']} file={r['file']} {r.get('err', '')}")


if __name__ == "__main__":
    main()
