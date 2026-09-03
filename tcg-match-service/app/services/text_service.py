import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings


class TextService:
    """BGE text embedding service for OCR-based text matching."""

    def __init__(self, model_path: str = None, device: str = "cpu"):
        model_path = model_path or settings.BGE_MODEL_PATH
        self.model = SentenceTransformer(
            model_path, device=device,
            model_kwargs={"use_safetensors": False},
        )
        self.query_prefix = settings.BGE_QUERY_PREFIX

    def encode(self, text: str) -> np.ndarray:
        """Encode query text into a 384-d L2-normalized embedding."""
        query = self.query_prefix + text
        return self.model.encode(query, normalize_embeddings=True).astype(np.float32)