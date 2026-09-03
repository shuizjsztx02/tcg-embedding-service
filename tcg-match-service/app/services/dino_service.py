import torch
import numpy as np
from PIL import Image

from app.config import settings

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


class DINOv2Service:
    """DINOv2 ViT-B/14 embedding service.

    The caller is responsible for preprocessing (card detection, perspective
    correction, orientation). This service only resizes + normalizes + embeds.
    """

    def __init__(self, device: str = "cpu"):
        self.device = device
        self.model = self._load_model()

    def _load_model(self):
        try:
            m = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
        except Exception:
            from transformers import AutoModel
            m = AutoModel.from_pretrained("facebook/dinov2-base")
        m.eval().to(self.device)
        return m

    @torch.no_grad()
    def embed(self, image: Image.Image) -> np.ndarray:
        """Embed a single preprocessed image into a 768-d L2-normalized CLS token."""
        w, h = settings.DINO_INPUT_SIZE
        img = image.convert("RGB").resize((w, h), Image.BICUBIC)
        arr = np.asarray(img, dtype=np.float32) / 255.0
        arr = (arr - MEAN) / STD
        x = torch.from_numpy(arr.transpose(2, 0, 1)[None]).float().to(self.device)
        out = self.model(x)
        if out.dim() == 3:
            out = out[:, 0]
        feat = out.cpu().numpy().astype(np.float32)
        norms = np.linalg.norm(feat)
        return feat / max(norms, 1e-12)