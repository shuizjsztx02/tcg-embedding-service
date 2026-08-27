"""
ocr_engine.py — OCR engine module supporting both EasyOCR and RapidOCR.

EasyOCR: accurate but slow (~6-7s per image on CPU).
RapidOCR: fast (~2.5s per image on CPU), comparable or better accuracy.

Usage:
    from script_temp.ocr_engine import create_engine
    engine = create_engine("rapidocr")  # or "easyocr"
    results, elapsed = engine.read(image_np)
"""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class OCRResult:
    """A single recognized text block."""
    text: str
    confidence: float
    bbox: List[List[float]]  # 4 corner points: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]


# ---------------------------------------------------------------------------
# RapidOCR engine (default — fast, ONNX-based)
# ---------------------------------------------------------------------------

class RapidOCREngine:
    """Wrapper around RapidOCR (ONNX Runtime, PaddleOCR models).

    Typically ~2.5s per image on CPU, with accuracy comparable to or
    better than EasyOCR for card text.

    Parameters
    ----------
    kwargs
        Passed to ``RapidOCR(**kwargs)``.  See RapidOCR config for details.
    """

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            from rapidocr_onnxruntime import RapidOCR
            self._engine = RapidOCR(**self._kwargs)
        return self._engine

    def read(
        self,
        image: np.ndarray,
        **kwargs,
    ) -> Tuple[List[OCRResult], float]:
        """Run OCR on a (preprocessed) image.

        Parameters
        ----------
        image : np.ndarray
            BGR or RGB uint8 image.

        Returns
        -------
        list of OCRResult, float elapsed
        """
        start = time.perf_counter()
        raw, elapse = self.engine(image, **kwargs)
        elapsed = time.perf_counter() - start

        if raw is None:
            return [], elapsed

        # raw format: [[bbox, text, confidence], ...]
        # bbox: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        # text: str
        # confidence: str (float as string)
        results = []
        for entry in raw:
            if len(entry) < 3:
                continue
            bbox, text, conf_str = entry
            conf = float(conf_str) if isinstance(conf_str, str) else float(conf_str)
            results.append(OCRResult(
                text=str(text),
                confidence=conf,
                bbox=[[float(v) for v in pt] for pt in bbox],
            ))

        return results, elapsed


# ---------------------------------------------------------------------------
# EasyOCR engine (fallback — slower but more language options)
# ---------------------------------------------------------------------------

class EasyOCREngine:
    """Wrapper around EasyOCR.

    Slower on CPU (~6-7s per image) but supports more language combinations.

    Parameters
    ----------
    languages : list of str, optional
        Language codes.  Default: ``["en", "ch_sim"]``.
        Note: ``ch_sim`` is only compatible with ``en``.
    gpu : bool
        Use GPU if available.  Default: False.
    model_storage : str or None
        Custom directory for model files.  Defaults to project/.easyocr_models/.
    user_network : str or None
        Custom directory for user network files.  Defaults to project/.easyocr_models/.
    kwargs
        Extra arguments forwarded to ``easyocr.Reader``.
    """

    def __init__(
        self,
        languages: Optional[List[str]] = None,
        gpu: bool = False,
        model_storage: Optional[str] = None,
        user_network: Optional[str] = None,
        **kwargs,
    ):
        self._languages = languages or ["en", "ch_sim"]
        self._gpu = gpu
        _default_model_dir = str(Path(__file__).resolve().parent.parent / ".easyocr_models")
        self._model_storage = model_storage or _default_model_dir
        self._user_network = user_network or _default_model_dir
        self._reader_kwargs = kwargs
        self._reader = None

    @property
    def reader(self):
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(
                self._languages,
                gpu=self._gpu,
                model_storage_directory=self._model_storage,
                user_network_directory=self._user_network,
                **self._reader_kwargs,
            )
        return self._reader

    def read(
        self,
        image: np.ndarray,
        *,
        paragraph: bool = False,
        min_size: int = 10,
        text_threshold: float = 0.7,
        low_text: float = 0.4,
        **kwargs,
    ) -> Tuple[List[OCRResult], float]:
        """Run OCR on a preprocessed image.

        Returns
        -------
        list of OCRResult, float elapsed
        """
        # easyocr expects RGB
        if image.ndim == 3 and image.shape[2] == 3:
            if image[0, 0, 0] > image[0, 0, 2]:  # B > R → BGR
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb = image
        else:
            rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        start = time.perf_counter()
        raw = self.reader.readtext(
            rgb,
            paragraph=paragraph,
            min_size=min_size,
            text_threshold=text_threshold,
            low_text=low_text,
            **kwargs,
        )
        elapsed = time.perf_counter() - start

        results = []
        for entry in raw:
            if len(entry) == 3:
                bbox, txt, conf = entry
            else:
                bbox, txt = entry
                conf = 0.0
            results.append(OCRResult(text=txt, confidence=conf, bbox=bbox))

        return results, elapsed


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_ENGINES = {
    "rapidocr": RapidOCREngine,
    "easyocr": EasyOCREngine,
}


def create_engine(name: str = "rapidocr", **kwargs) -> object:
    """Create an OCR engine by name.

    Parameters
    ----------
    name : str
        ``"rapidocr"`` (default, fast) or ``"easyocr"`` (fallback).
    kwargs
        Engine-specific arguments.

    Returns
    -------
    An engine instance with a ``.read(image) -> (list[OCRResult], float)`` API.
    """
    cls = _ENGINES.get(name.lower())
    if cls is None:
        raise ValueError(f"Unknown OCR engine: {name!r}.  Options: {list(_ENGINES)}")
    return cls(**kwargs)


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    img = cv2.imread(path)
    assert img is not None, f"cannot read {path}"

    engine = create_engine("rapidocr")
    results, elapsed = engine.read(img)
    print(f"OCR took {elapsed:.2f}s, found {len(results)} text blocks")
    for r in results:
        print(f"  [{r.confidence:.2f}] {r.text}")
