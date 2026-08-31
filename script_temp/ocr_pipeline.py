"""OCR-only card preparation and recognition-guided orientation selection.

Geometry is shared with DINO; photometric processing and selection are not.
Keep every result tied to its actual input image and never synthesize text.
"""
from dataclasses import dataclass
import time

import cv2
import numpy as np
from PIL import Image, ImageOps

from dino_preprocess import detect_card, perspective_correct


QUERY_CONFIDENCE = .75
MAX_SIDE = 1200


@dataclass
class CardReading:
    image: Image.Image
    blocks: list
    full_text: str
    query_text: str
    elapsed: float
    metadata: dict
    warnings: list


def _readable_length(text):
    return sum(c.isalnum() for c in text)


def _query_eligible(result):
    return result.confidence >= QUERY_CONFIDENCE and _readable_length(result.text) >= 2


def _quality_score(results):
    """Heuristic evidence, not a calibrated probability or OCR accuracy.

    Count unique confident characters; cap long paragraphs so several weak
    hallucinations cannot beat a well-recognized title just by block count.
    """
    scores = {}
    for result in results:
        key = " ".join(result.text.casefold().split())
        if _query_eligible(result):
            score = min(_readable_length(key), 40) * (2 * result.confidence - 1) ** 2
            scores[key] = max(scores.get(key, 0), score)
    return sum(sorted(scores.values(), reverse=True)[:8])


def _bounded(image):
    image = image.copy()
    image.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
    # The detector scales its short side to 736: bound extreme panorama cost.
    w, h = image.size
    size = (max(w, (h + 3) // 4), max(h, (w + 3) // 4))
    return ImageOps.pad(image, size, color="white") if size != image.size else image


def _measure(image):
    small = image.copy()
    small.thumbnail((600, 600))
    rgb = np.asarray(small)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return {"luminance": round(float(gray.mean()), 2),
            "contrast": round(float(np.percentile(gray, 95) - np.percentile(gray, 5)), 2),
            "highlight_ratio": round(float(np.all(rgb >= 248, axis=2).mean()), 4),
            "detail_variance": round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2)}


def _enhance(image):
    """One mild luminance-only pass. No smoothing, heavy sharpening or fill."""
    lab = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2LAB)
    light = lab[:, :, 0]
    local = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8)).apply(light)
    lab[:, :, 0] = cv2.addWeighted(light, .5, local, .5, 0)
    return Image.fromarray(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB))


def read_card(image, engine):
    start = time.perf_counter()
    photo = ImageOps.exif_transpose(image).convert("RGB")
    quad = detect_card(photo)
    # Preserve the bottom card number; DINO's border trim is inappropriate here.
    card = perspective_correct(photo, quad, output_size=(882, 1232), trim=0) if quad is not None else photo
    card = _bounded(card)
    candidates = []
    warnings = []

    def evaluate(img, source, angle, enhanced=False):
        img = img.rotate(angle, expand=True) if angle else img
        bgr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        results, _ = engine.read(bgr)
        candidate = {"image": img, "results": results, "score": _quality_score(results),
                     "source": source, "rotation": angle, "enhanced": enhanced}
        candidates.append(candidate)
        return candidate

    source = "card" if quad is not None else "original"
    # Portrait geometry determines the long axis, never which end is upright.
    for angle in ((0, 180) if quad is not None else (0, 180, 90, 270)):
        evaluate(card, source, angle)
    best = max(candidates, key=lambda c: c["score"])
    if quad is None:
        warnings.append("未可靠检测到卡片边界，已保留原图比较四个方向")
    elif best["score"] < 6:
        warnings.append("裁剪后的可靠文字不足，已比较原图四个方向")
        original = _bounded(photo)
        for angle in (0, 180, 90, 270):
            evaluate(original, "original", angle)
        best = max(candidates, key=lambda c: c["score"])

    # Always retain the unenhanced result. Enhance only when there is evidence
    # of difficult exposure/contrast or weak recognition, then require a gain.
    quality = _measure(best["image"])
    needs_enhancement = (quality["luminance"] < 80 or quality["luminance"] > 200
                         or quality["contrast"] < 100 or best["score"] < 15)
    if needs_enhancement:
        pool_source = "original" if best["score"] < 6 else best["source"]
        pool = [c for c in candidates if c["source"] == pool_source]
        ambiguous = any(c is not best and c["score"] >= best["score"] * .9 for c in pool)
        # If raw OCR has no direction evidence, enhancing just angle 0 would
        # recreate the inversion bug. Bounded to ten total candidates.
        enhance_candidates = pool if best["score"] < 6 or ambiguous else [best]
        raw_score = best["score"]
        for candidate in enhance_candidates:
            enhanced = evaluate(_enhance(candidate["image"]), candidate["source"], 0, enhanced=True)
            enhanced["rotation"] = candidate["rotation"]
            if enhanced["score"] > max(best["score"], raw_score * 1.05):
                best = enhanced

    alternatives = [c["score"] for c in candidates
                    if c["source"] == best["source"] and c["rotation"] != best["rotation"]]
    if alternatives and max(alternatives) >= best["score"] * .9:
        warnings.append("文字方向证据不足或接近，请核对预览；当前方向评分不是准确率")
    if min(photo.size) < 400:
        warnings.append("原图分辨率较低，放大不能恢复卡号等细小文字，请优先上传原始照片")
    if quality["detail_variance"] < 50:
        warnings.append("图像细节不足或模糊，请对焦后重拍；增强不能恢复丢失文字")
    if quality["highlight_ratio"] > .08:
        warnings.append("存在高亮饱和区域（也可能是白色卡面），反光或过曝遮住的文字需换角度重拍")

    ordered = sorted(best["results"], key=lambda r: (min(p[1] for p in r.bbox), min(p[0] for p in r.bbox)))
    blocks = [{"text": r.text, "confidence": r.confidence, "bbox": r.bbox} for r in ordered]
    query_lines, seen = [], set()
    for r in ordered:
        text = " ".join(r.text.split())
        if _query_eligible(r) and text.casefold() not in seen:
            query_lines.append(text)
            seen.add(text.casefold())
    if any(r.confidence < QUERY_CONFIDENCE for r in ordered):
        warnings.append("低置信度文字仅供核对，未用于文字向量匹配")
    if not query_lines:
        warnings.append("没有足够可靠的 OCR 文字，已停止文字向量匹配；请重新拍摄")

    def summary(candidate):
        return {key: candidate[key] for key in ("source", "rotation", "enhanced")} | {
            "score": round(candidate["score"], 3), "blocks": len(candidate["results"])}

    metadata = {"pipeline": "ocr-card-v2", "quad_found": quad is not None,
                "quad": quad.round(2).tolist() if quad is not None else None,
                "selected": summary(best), "candidates": [summary(c) for c in candidates],
                "quality": quality, "image_size": list(best["image"].size),
                "bbox_space": "preprocessed_image", "query_min_confidence": QUERY_CONFIDENCE}
    return CardReading(best["image"], blocks, "\n".join(r.text for r in ordered),
                       "\n".join(query_lines), time.perf_counter() - start, metadata, warnings)
