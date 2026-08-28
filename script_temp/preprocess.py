# Shared preprocessing: EXIF normalization, card detection, perspective
# correction, quality gates, orientation candidates and light OCR enhancement.
#
# Design follows the v4 preprocessing guideline:
#   - retrieval gets a geometric standard image (no color edits);
#   - OCR gets a high-res visually enhanced image (conservative settings);
#   - bad photos (blur / glare / tiny card) produce warnings, not crashes.
from PIL import Image, ImageOps
import cv2
import numpy as np


# (W, H) multiples of 14 to match the DINOv2 ViT-B/14 patch grid.
MODEL_INPUT = (168, 224)

# Corrected-card output sizes, 63:88 card aspect ratio.
SEARCH_OUTPUT = (504, 704)   # retrieval: geometry only, downsized for DINOv2
OCR_OUTPUT = (882, 1232)     # OCR: keep >=800px long edge for small text

# Quality gates calibrated on 60 real phone photos
# (script_temp/calibrate_quality_gates.py):
#   laplacian_var p5=159, glare_ratio p95=0.024, card area_ratio p5=0.48.
BLUR_VAR_MIN = 150.0      # Laplacian variance below this -> too blurry
GLARE_RATIO_MAX = 0.15    # >15% near-saturated card face -> ask to retake
CARD_AREA_MIN = 0.20      # card should cover >=20% of the photo
EDGE_TRIM = 0.01          # trim 1% of each side after warp (sleeve/background)


def normalize_orientation(img):
    """Apply EXIF orientation so pixel data matches what the user sees."""
    out = ImageOps.exif_transpose(img)
    return out if out is not None else img


def orientation_candidates(img):
    """Yield candidate orientations; caller scores each and keeps the best.

    Landscape photos are treated as rotated portrait cards (+/-90).
    Portrait photos also try 180 to cover upside-down shots.
    The first candidate preserves gallery/index-building behavior.
    """
    w, h = img.size
    if w > h:
        yield img.rotate(-90, expand=True)
        yield img.rotate(90, expand=True)
    else:
        yield img
        yield img.rotate(180, expand=True)


def to_model_input(img):
    return img.convert("RGB").resize(MODEL_INPUT, Image.BICUBIC)


# Card aspect ratio is 63:88 = 1.40 (long/short); allow perspective distortion.
QUAD_MAX_SIDE_RATIO = 1.7


def quad_is_plausible(quad):
    """A card quad must be convex and its side-length ratio near 63:88.

    Rejects fabric folds, desk regions and background blobs that contour
    detection happily fits a 4-gon onto; warping those would destroy the
    embedding far worse than falling back to the full frame.
    """
    edges = quad[[1, 2, 3, 0]] - quad
    cross = np.cross(edges, np.roll(edges, -1, axis=0))
    if (cross > 1e-6).any() and (cross < -1e-6).any():
        return False  # non-convex
    w = (np.linalg.norm(quad[1] - quad[0]) + np.linalg.norm(quad[2] - quad[3])) / 2
    h = (np.linalg.norm(quad[3] - quad[0]) + np.linalg.norm(quad[2] - quad[1])) / 2
    if w <= 0 or h <= 0:
        return False
    return max(w, h) / min(w, h) <= QUAD_MAX_SIDE_RATIO


def detect_card(img):
    img_np = np.array(img.convert("RGB"))
    h, w = img_np.shape[:2]
    img_area = h * w
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    candidates = []

    def consider(quad):
        if quad is not None and quad_is_plausible(quad):
            candidates.append(quad)

    def quad_from_contour(c):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return order_points(approx.reshape(4, 2).astype(np.float32))
        return None

    # Strategy 1: Otsu thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    otsu_contours = []
    if contours:
        otsu_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in otsu_contours[:10]:
            area = cv2.contourArea(c)
            if area < img_area * 0.05 or area > img_area * 0.95:
                continue
            consider(quad_from_contour(c))

    # Strategy 2: Canny with multiple threshold ranges
    for low, high in [(30, 90), (50, 150), (70, 200)]:
        edged = cv2.Canny(blurred, low, high)
        dilated = cv2.dilate(edged, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours[:5]:
            area = cv2.contourArea(c)
            if area < img_area * 0.05 or area > img_area * 0.95:
                continue
            consider(quad_from_contour(c))

    # Last resort: min-area rect of the largest Otsu contour (validated too)
    if not candidates:
        for c in otsu_contours[:5]:
            if cv2.contourArea(c) < img_area * 0.05:
                continue
            box = cv2.boxPoints(cv2.minAreaRect(c))
            consider(order_points(box.astype(np.float32)))
            if candidates:
                break

    if candidates:
        return max(candidates, key=cv2.contourArea)
    return None


def order_points(pts):
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    d = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    return rect


def perspective_correct(img, quad, output_size=SEARCH_OUTPUT, trim=EDGE_TRIM):
    dst = np.array([
        [0, 0],
        [output_size[0] - 1, 0],
        [output_size[0] - 1, output_size[1] - 1],
        [0, output_size[1] - 1],
    ], dtype=np.float32)
    img_np = np.array(img.convert("RGB"))
    M = cv2.getPerspectiveTransform(quad, dst)
    warped = cv2.warpPerspective(
        img_np, M, output_size,
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    if trim > 0:
        # Trim a thin border: background bleed, sleeve edges, warp artifacts.
        tw = int(round(output_size[0] * trim))
        th = int(round(output_size[1] * trim))
        warped = warped[th:output_size[1] - th, tw:output_size[0] - tw]
    return Image.fromarray(warped)


def assess_quality(img, quad_area_ratio=None):
    """Quality re-check on the corrected card image.

    Returns (warnings, metrics). Warnings are soft: the pipeline continues,
    the API surfaces them so the user can retake the photo.
    """
    arr = np.array(img.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    blur_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    glare_ratio = float(np.all(arr >= 240, axis=2).mean())
    warnings = []
    if blur_var < BLUR_VAR_MIN:
        warnings.append("图像较模糊，建议在光线充足处重新拍摄")
    if glare_ratio > GLARE_RATIO_MAX:
        warnings.append("卡面大面积反光，建议稍微倾斜手机重新拍摄")
    if quad_area_ratio is not None and quad_area_ratio < CARD_AREA_MIN:
        warnings.append("卡牌占比过小，建议靠近卡牌重新拍摄")
    metrics = {
        "blur_var": round(blur_var, 1),
        "glare_ratio": round(glare_ratio, 4),
        "quad_area_ratio": round(quad_area_ratio, 4) if quad_area_ratio is not None else None,
    }
    return warnings, metrics


def preprocess_card(img, output_size=SEARCH_OUTPUT, enhance_fn=None):
    """Core pipeline: EXIF -> detect card -> perspective correct -> trim -> quality gate.

    Returns (result_img, meta). Without enhance_fn the result is the geometric
    standard image (no color edits), which is what retrieval should embed.
    """
    img = normalize_orientation(img)
    quad = detect_card(img)
    quad_area_ratio = None
    if quad is not None:
        w, h = img.size
        quad_area_ratio = cv2.contourArea(quad) / (w * h)
        if quad_area_ratio < CARD_AREA_MIN:
            # Too small to be the card: warping would magnify background.
            quad = None
    if quad is not None:
        card = perspective_correct(img, quad, output_size)
    else:
        # Fallback: keep the whole frame. A center square crop would cut off
        # card content; matching/rejection thresholds handle poor inputs.
        card = img
    warnings, metrics = assess_quality(card, quad_area_ratio)
    meta = {"quad_found": quad is not None, "warnings": warnings}
    meta.update(metrics)
    result = enhance_fn(card) if enhance_fn is not None else card
    return result.convert("RGB"), meta


def preprocess_for_search(img):
    """Geometric standard image + meta for embedding retrieval."""
    return preprocess_card(img, SEARCH_OUTPUT)


def preprocess_query(img):
    """Backward-compatible wrapper used by the API."""
    return preprocess_for_search(img)[0]


def enhance_ocr(img):
    """Light visual enhancement for OCR (the "visual enhanced" output).

    Deliberately conservative: strong sharpening, strong CLAHE or binarization
    can fabricate or erase thin strokes (set codes, copyright text).
    """
    arr = np.array(img.convert("RGB")).astype(np.float32)
    # 1. Gray-world white balance, clamped (card art can dominate the frame)
    avg = arr.reshape(-1, 3).mean(axis=0)
    scale = np.clip(avg.mean() / np.maximum(avg, 1.0), 0.85, 1.15)
    arr = np.clip(arr * scale, 0, 255).astype(np.uint8)
    # 2. Gamma toward mid-tone brightness
    mean_lum = max(arr.mean() / 255.0, 1e-3)
    gamma = float(np.clip(np.log(0.5) / np.log(mean_lum), 0.7, 1.4))
    table = ((np.arange(256, dtype=np.float32) / 255.0) ** gamma * 255).astype(np.uint8)
    arr = cv2.LUT(arr, table)
    # 3. Light CLAHE on the L channel
    l, a, b = cv2.split(cv2.cvtColor(arr, cv2.COLOR_RGB2LAB))
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    arr = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2RGB)
    # 4. Light edge-preserving denoise
    arr = cv2.bilateralFilter(arr, d=7, sigmaColor=50, sigmaSpace=50)
    # 5. Very light unsharp mask
    blurred = cv2.GaussianBlur(arr, (0, 0), 1.5)
    arr = cv2.addWeighted(arr, 1.2, blurred, -0.2, 0)
    return Image.fromarray(arr)


def preprocess_for_ocr(img):
    """High-res geometric correction + light enhancement for OCR."""
    return preprocess_card(img, OCR_OUTPUT, enhance_fn=enhance_ocr)


def preprocess_query_ocr(img):
    """Backward-compatible wrapper used by OCR tooling."""
    return preprocess_for_ocr(img)[0]
