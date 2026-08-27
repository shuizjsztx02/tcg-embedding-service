# Shared preprocessing: orientation candidates + model input resize.
from PIL import Image
import cv2
import numpy as np



# (W, H) multiples of 14 to match the DINOv2 ViT-B/14 patch grid.
MODEL_INPUT = (168, 224)


def orientation_candidates(img):
    """Yield plausible upright versions of a card image.

    Portrait images yield themselves; landscape images yield both 90-degree
    rotations so downstream scoring can pick the better one without needing
    an orientation classifier.
    """
    w, h = img.size
    if w > h:
        yield img.rotate(-90, expand=True)
        yield img.rotate(90, expand=True)
    else:
        yield img


def to_model_input(img):
    return img.convert("RGB").resize(MODEL_INPUT, Image.BICUBIC)

def detect_card(img):
    """Detect card quadrilateral in a PIL image."""
    img_np = np.array(img.convert("RGB"))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    dilated = cv2.dilate(edged, None, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return order_points(approx.reshape(4, 2).astype(np.float32))
    rect = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rect)
    return order_points(box.astype(np.float32))

def order_points(pts):
    """Order 4 corner points: TL, TR, BR, BL."""
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    d = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    return rect

def perspective_correct(img, quad, output_size=(400, 560)):
    """Warp the card region to a straight-on rectangle."""
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
    return Image.fromarray(warped)

def enhance(img):
    """CLAHE contrast enhancement + unsharp-mask sharpening."""
    img_np = np.array(img.convert("RGB"))
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    enhanced = cv2.cvtColor(cv2.merge([l_eq, a, b]), cv2.COLOR_LAB2RGB)
    blurred = cv2.GaussianBlur(enhanced, (0, 0), 3.0)
    sharpened = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)
    return Image.fromarray(sharpened)

def preprocess_query(img):
    """Full pipeline: detect card, perspective correct, enhance."""
    quad = detect_card(img)
    if quad is not None:
        img = perspective_correct(img, quad)
    else:
        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))
    return enhance(img)
