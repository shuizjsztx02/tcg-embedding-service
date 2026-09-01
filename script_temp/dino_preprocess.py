"""Query-only DINO preprocessing. Gallery normalization stays in preprocess.py.

Keep OCR's existing pipeline unchanged. Geometry and mild enhancement are
candidates, not irreversible decisions; retrieval can fall back to the photo.
"""
import cv2
import numpy as np
from itertools import combinations
from PIL import Image

from preprocess import normalize_orientation, perspective_correct as _warp, to_model_input


DETECTION_MAX_SIDE = 960
CARD_RATIO = 88 / 63


def order_points(pts):
    """Clockwise vertices starting near top-left, without sum/difference ties."""
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    center = pts.mean(axis=0)
    angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
    pts = pts[np.argsort(angles)]
    return np.roll(pts, -int(np.argmin(pts.sum(axis=1))), axis=0).copy()


def _quad_score(quad, support):
    h, w = support.shape
    if (quad < 0).any() or (quad[:, 0] >= w).any() or (quad[:, 1] >= h).any():
        return -1
    area = cv2.contourArea(quad) / (w * h)
    if not .06 <= area <= .97 or not cv2.isContourConvex(quad):
        return -1
    lengths = np.linalg.norm(np.roll(quad, -1, axis=0) - quad, axis=1)
    if lengths.min() < 20:
        return -1
    a, b = (lengths[0] + lengths[2]) / 2, (lengths[1] + lengths[3]) / 2
    ratio = max(a, b) / min(a, b)
    if not 1.12 <= ratio <= 1.95:
        return -1
    if max(lengths[0] / lengths[2], lengths[2] / lengths[0],
           lengths[1] / lengths[3], lengths[3] / lengths[1]) > 1.8:
        return -1
    side_support = []
    for start, end in zip(quad, np.roll(quad, -1, axis=0)):
        points = start + np.linspace(.08, .92, 60)[:, None] * (end - start)
        x, y = points[:, 0].astype(int), points[:, 1].astype(int)
        side_support.append(float((support[y, x] > 0).mean()))
    if min(side_support) < .45 or np.mean(side_support) < .7:
        return -1
    return area ** .5 * np.exp(-2 * abs(np.log(ratio / CARD_RATIO))) * np.mean(side_support)


def _select_best_quad(scored, shape):
    """Prefer a nearby enclosing border when its evidence is almost tied.

    Internal title separators can share three card edges and score slightly
    higher because their apparent ratio is closer to CARD_RATIO. Keep the
    global score strict; only override it for a 2-15% larger enclosing quad
    whose corners and score are both very close to the raw winner.
    """
    if not scored:
        return None
    best, best_score = max(scored, key=lambda item: item[1])
    best_area = cv2.contourArea(best)
    corner_limit = min(shape) * .06
    outside_tolerance = min(shape) * .02
    alternatives = [best]
    for quad, score in scored:
        area = cv2.contourArea(quad)
        if not best_area * 1.02 <= area <= best_area * 1.15:
            continue
        if score < best_score * .99:
            continue
        if np.linalg.norm(quad - best, axis=1).max() > corner_limit:
            continue
        if all(cv2.pointPolygonTest(quad, tuple(map(float, point)), True) >= -outside_tolerance
               for point in best):
            alternatives.append(quad)
    return max(alternatives, key=cv2.contourArea)


def _line_quads(gray):
    """Join long, nearly parallel border segments when fingers break contours.

    Bound combinatorics to 24 segments. Every inferred quad is still checked
    against observed edge support, aspect ratio and original image bounds.
    """
    detected = cv2.createLineSegmentDetector().detect(gray)[0]
    if detected is None:
        return
    segments = detected.reshape(-1, 2, 2)
    vectors = segments[:, 1] - segments[:, 0]
    lengths = np.linalg.norm(vectors, axis=1)
    selected = np.argsort(-lengths)[:24]
    selected = selected[lengths[selected] > min(gray.shape) * .15]
    segments, vectors, lengths = segments[selected], vectors[selected], lengths[selected]
    directions = vectors / lengths[:, None]
    lines = np.cross(np.concatenate((segments[:, 0], np.ones((len(segments), 1))), axis=1),
                     np.concatenate((segments[:, 1], np.ones((len(segments), 1))), axis=1))
    lines /= np.linalg.norm(lines[:, :2], axis=1, keepdims=True)
    pairs = []
    for i, j in combinations(range(len(segments)), 2):
        if abs(np.dot(directions[i], directions[j])) < .94:
            continue
        separation = abs(np.dot(lines[i, :2], segments[j].mean(axis=0)) + lines[i, 2])
        if separation > min(gray.shape) * .15:
            pairs.append((i, j))
    for (a, b), (c, d) in combinations(pairs, 2):
        if len({a, b, c, d}) < 4 or abs(np.dot(directions[a], directions[c])) > .4:
            continue
        corners = np.cross(lines[[a, a, b, b]], lines[[c, d, d, c]])
        if (np.abs(corners[:, 2]) < 1e-6).any():
            continue
        yield order_points(corners[:, :2] / corners[:, 2:])


def detect_card(img):
    """Find a supported card quadrilateral, including nested contours.

    Detect on a bounded thumbnail, map coordinates back to the original.
    Never fit an arbitrary foreground blob with a minimum-area rectangle.
    """
    small = img.convert("RGB")
    small.thumbnail((DETECTION_MAX_SIDE, DETECTION_MAX_SIDE), Image.Resampling.LANCZOS)
    arr = np.asarray(small)
    h, w = arr.shape[:2]
    if min(w, h) < 20:
        return None
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 10, 30)
    support = cv2.dilate(edges, np.ones((5, 5), np.uint8))
    _, otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    masks = [cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
             for mask in (otsu, 255 - otsu)]
    for low, high in ((10, 30), (50, 150), (90, 220)):
        edge = cv2.Canny(blurred, low, high)
        masks.append(cv2.morphologyEx(edge, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)))
        masks.append(cv2.dilate(edge, None, iterations=2))
    scored = []
    for mask in masks:
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:80]:
            area = cv2.contourArea(contour)
            if not .06 * w * h <= area <= .97 * w * h:
                continue
            perimeter = cv2.arcLength(contour, True)
            for epsilon in (.015, .025, .04):
                approx = cv2.approxPolyDP(contour, epsilon * perimeter, True)
                if len(approx) != 4 or not cv2.isContourConvex(approx):
                    continue
                quad = order_points(approx)
                score = _quad_score(quad, support)
                if score >= 0:
                    scored.append((quad, score))
    for quad in _line_quads(gray):
        score = _quad_score(quad, support)
        if score >= 0:
            scored.append((quad, score))
    best = _select_best_quad(scored, (h, w))
    if best is None:
        return None
    return best * np.array([img.width / w, img.height / h], dtype=np.float32)


def perspective_correct(img, quad, output_size=(504, 704), trim=.01):
    quad = order_points(quad)
    lengths = np.linalg.norm(np.roll(quad, -1, axis=0) - quad, axis=1)
    if lengths[0] + lengths[2] > lengths[1] + lengths[3]:
        quad = np.roll(quad, -1, axis=0).copy()
    # Preserve the existing 1% sleeve/warp-edge trim, without brightness rotation.
    return _warp(img, quad, output_size=output_size, trim=trim)


def assess_quality(img):
    """Comparable measurements at model resolution, before any enhancement.

    Clipped highlights can be glare OR white printing; report the ambiguity.
    Metrics are diagnostics, not calibrated acceptance/rejection thresholds.
    """
    arr = np.asarray(to_model_input(img))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    blur = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    clipped = float(np.all(arr >= 248, axis=2).mean())
    dark = float((gray < 35).mean())
    mean = float(gray.mean())
    contrast = float(np.percentile(gray, 95) - np.percentile(gray, 5))
    warnings = []
    if blur < 100:
        warnings.append("图像细节不足或模糊，请对焦后重新拍摄；锐化无法恢复丢失细节")
    if clipped > .08:
        warnings.append("检测到高亮饱和区域（也可能是白色卡面），如有反光或过曝请换角度重拍")
    if mean > 205:
        warnings.append("卡面整体偏亮，建议降低曝光；纯白区域无法恢复")
    if mean < 65 or dark > .5:
        warnings.append("图像偏暗，建议补充均匀光照")
    return {"blur_var": round(blur, 2), "highlight_ratio": round(clipped, 4),
            "dark_ratio": round(dark, 4), "mean_luminance": round(mean, 2),
            "contrast": round(contrast, 2)}, warnings


def enhance_card(img, quality):
    """Mild luminance correction; no inpainting, generative fill or recoloring."""
    arr = np.asarray(img.convert("RGB"))
    lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
    light = lab[:, :, 0]
    mean = quality["mean_luminance"]
    if mean < 85 or mean > 190:
        gamma = float(np.clip(np.log(.5) / np.log(np.clip(mean / 255, .01, .99)), .8, 1.2))
        lut = np.clip((np.arange(256) / 255) ** gamma * 255, 0, 255).astype(np.uint8)
        light = cv2.LUT(light, lut)
    if quality["contrast"] < 100:
        local = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8)).apply(light)
        light = cv2.addWeighted(light, .7, local, .3, 0)
    if quality["blur_var"] < 100:
        smooth = cv2.GaussianBlur(light, (0, 0), .8)
        light = cv2.addWeighted(light, 1.15, smooth, -.15, 0)
    lab[:, :, 0] = light
    return Image.fromarray(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB))


def prepare_candidates(img):
    """Return up to eight (image, provenance) candidates plus diagnostics."""
    photo = normalize_orientation(img).convert("RGB")
    quad = detect_card(photo)
    card = perspective_correct(photo, quad) if quad is not None else photo
    quality, warnings = assess_quality(card)
    area = float(cv2.contourArea(quad) / (photo.width * photo.height)) if quad is not None else None
    if quad is None:
        warnings.append("未可靠检测到卡牌边界，保留整图多方向检索；建议靠近卡牌并使用简洁背景")
    elif area < .2:
        warnings.append("卡牌占比过小，建议靠近卡牌重新拍摄")
    candidates = []

    def add_orientations(image, source, angles):
        for angle in angles:
            # Resize before retaining: four 12MP RGB views otherwise cost
            # ~192 MB per request, despite tiny model inputs. The transient
            # rotation is released each iteration; gallery resize is unchanged.
            oriented = image if angle == 0 else image.rotate(angle, expand=True)
            candidates.append((to_model_input(oriented), {"source": source, "rotation_degrees": angle}))

    if quad is not None:
        add_orientations(card, "card", (0, 180))
    # Photo orientation says nothing about the card orientation; retain all four.
    add_orientations(photo, "original", (0, 180, 90, 270))
    needs_enhancement = (quality["blur_var"] < 100 or quality["contrast"] < 100
                         or quality["mean_luminance"] < 85 or quality["mean_luminance"] > 190)
    if quad is not None and needs_enhancement:
        add_orientations(enhance_card(card, quality), "enhanced_card", (0, 180))
    meta = {"pipeline": "dino-query-v2", "quad_found": quad is not None,
            "quad": quad.round(2).tolist() if quad is not None else None,
            "quad_area_ratio": round(area, 4) if area is not None else None,
            "quality": quality, "warnings": warnings, "candidate_count": len(candidates)}
    return candidates, meta
