"""
preprocess_ocr.py — OpenCV-based preprocessing pipeline for card image OCR.

Steps:
  1. Resize to a maximum dimension (speed / accuracy trade-off).
  2. CLAHE contrast enhancement on the L channel of LAB.
  3. Bilateral filter denoising (preserves edges).
  4. Unsharp-mask sharpening.
  5. Optional: grayscale + adaptive threshold binarization.

All functions accept and return uint8 arrays (BGR or grayscale).
"""

import cv2
import numpy as np


class OCRPreprocessor:
    """OpenCV preprocessing tailored for card photos before OCR."""

    def __init__(
        self,
        max_dim: int = 1200,
        clahe_clip: float = 2.0,
        clahe_grid: int = 8,
    ):
        self.max_dim = max_dim
        self._clahe = cv2.createCLAHE(
            clipLimit=clahe_clip,
            tileGridSize=(clahe_grid, clahe_grid),
        )

    def resize_to_max(self, img: np.ndarray) -> np.ndarray:
        h, w = img.shape[:2]
        if max(h, w) <= self.max_dim:
            return img
        scale = self.max_dim / max(h, w)
        return cv2.resize(
            img, (int(w * scale), int(h * scale)),
            interpolation=cv2.INTER_AREA,
        )

    def enhance_contrast(self, img: np.ndarray) -> np.ndarray:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l_eq = self._clahe.apply(l)
        return cv2.cvtColor(cv2.merge([l_eq, a, b]), cv2.COLOR_LAB2BGR)

    def denoise(self, img: np.ndarray) -> np.ndarray:
        return cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    def sharpen(self, img: np.ndarray) -> np.ndarray:
        blurred = cv2.GaussianBlur(img, (0, 0), 3.0)
        return cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

    def to_grayscale(self, img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def binarize(self, gray: np.ndarray) -> np.ndarray:
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2,
        )

    def preprocess(
        self,
        img: np.ndarray,
        *,
        binarize: bool = False,
        grayscale: bool = False,
    ) -> np.ndarray:
        img = self.resize_to_max(img)
        img = self.enhance_contrast(img)
        img = self.denoise(img)
        img = self.sharpen(img)
        if binarize:
            gray = self.to_grayscale(img)
            return self.binarize(gray)
        if grayscale:
            return self.to_grayscale(img)
        return img

    def __call__(self, img: np.ndarray, **kw) -> np.ndarray:
        return self.preprocess(img, **kw)


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    raw = cv2.imread(path)
    assert raw is not None, f"cannot read {path}"
    print(f"Input  shape: {raw.shape}")
    pp = OCRPreprocessor(max_dim=1200)
    out = pp(raw)
    print(f"Output shape: {out.shape}")
    cv2.imwrite("debug_preprocess_ocr.jpg", out)
    print("wrote debug_preprocess_ocr.jpg")
