import cv2
import numpy as np
from PIL import Image

from app.config import settings

_DET_MODEL_DIR = settings.PPOCR_MODEL_DIR + "/ch_PP-OCRv4_det_infer"
_REC_MODEL_DIR = settings.PPOCR_MODEL_DIR + "/ch_PP-OCRv4_rec_infer"
_KEYS_PATH = settings.PPOCR_MODEL_DIR + "/ppocr_keys_v1.txt"


class OCRService:
    """PP-OCRv4 detection + recognition.

    No preprocessing, no multi-direction selection — the caller is expected
    to pass a card image that is already cropped and oriented.
    """

    def __init__(self, threads: int = 2):
        from app.services.ppocr_engine import PPOCRv4Engine
        self.engine = PPOCRv4Engine(
            det_model_dir=_DET_MODEL_DIR,
            rec_model_dir=_REC_MODEL_DIR,
            keys_path=_KEYS_PATH,
            threads=threads,
        )

    def read(self, image: Image.Image) -> tuple[list[dict], str, str, list[str]]:
        """Run OCR on a preprocessed card image.

        Returns (blocks, full_text, query_text, warnings).
        - blocks: list of {text, confidence, bbox}
        - full_text: all text joined by newlines
        - query_text: high-confidence unique lines for BGE matching
        - warnings: any issues found
        """
        bgr = cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)
        results, _ = self.engine.read(bgr)
        if not results:
            return [], "", "", ["未识别到文字，请确认卡牌文字清晰可见"]

        # Sort top-to-bottom, left-to-right
        ordered = sorted(results, key=lambda r: (min(p[1] for p in r.bbox), min(p[0] for p in r.bbox)))
        blocks = [{"text": r.text, "confidence": r.confidence, "bbox": r.bbox} for r in ordered]
        full_text = "\n".join(r.text for r in ordered)

        # Build query text from high-confidence lines
        query_lines, seen = [], set()
        warnings = []
        for r in ordered:
            text = " ".join(r.text.split())
            if r.confidence >= 0.75 and text and text.casefold() not in seen:
                query_lines.append(text)
                seen.add(text.casefold())

        if not query_lines:
            warnings.append("没有足够可靠的 OCR 文字，已停止文字向量匹配；请重新拍摄")
        else:
            if any(r.confidence < 0.75 for r in ordered):
                warnings.append("低置信度文字仅供核对，未用于文字向量匹配")

        query_text = "\n".join(query_lines)
        return blocks, full_text, query_text, warnings