import os


class Settings:
    # Data root directory (per-category subdirectories)
    DATA_DIR = os.environ.get("DATA_DIR", "/data")

    # Model paths
    MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
    BGE_MODEL_PATH = os.environ.get("BGE_MODEL_PATH", "/models/bge_model")
    PPOCR_MODEL_DIR = os.environ.get("PPOCR_MODEL_DIR", "/models/ppocr_models")

    # Matching thresholds
    MATCH_TAU = float(os.environ.get("MATCH_TAU", "0.775"))
    MATCH_MARGIN = float(os.environ.get("MATCH_MARGIN", "0.02"))

    # v2 recognize tiered thresholds
    TAU_HIGH = float(os.environ.get("TAU_HIGH", "0.87"))
    TAU_LOW = float(os.environ.get("TAU_LOW", "0.75"))
    MARGIN_HIGH = float(os.environ.get("MARGIN_HIGH", "0.02"))

    # LLM
    LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://127.0.0.1:15721")
    LLM_CATEGORY_MODEL = os.environ.get("LLM_CATEGORY_MODEL", "qwen3.7-flash")
    LLM_FALLBACK_MODEL = os.environ.get("LLM_FALLBACK_MODEL", "qwen3.7-flash")
    LLM_TIMEOUT_S = float(os.environ.get("LLM_TIMEOUT_S", "30"))

    # Price snapshot date
    PRICE_AS_OF = os.environ.get("PRICE_AS_OF", "")

    # GPU support
    USE_GPU = os.environ.get("USE_GPU", "false").lower() == "true"

    # Server
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "8056"))

    # BGE
    BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

    # DINOv2 input size (W, H) — multiples of 14 for ViT-B/14 patch grid
    DINO_INPUT_SIZE = (168, 224)

    # Index sub-directory names
    VISUAL_INDEX_DIR = "visual-index"
    TEXT_INDEX_DIR = "text-index"

    def get_category_dir(self, category: str) -> str:
        return os.path.join(self.DATA_DIR, category)

    def get_visual_index_dir(self, category: str) -> str:
        return os.path.join(self.DATA_DIR, category, self.VISUAL_INDEX_DIR)

    def get_text_index_dir(self, category: str) -> str:
        return os.path.join(self.DATA_DIR, category, self.TEXT_INDEX_DIR)

    def get_image_dir(self, category: str) -> str:
        return os.path.join(self.DATA_DIR, category, "images")

    def get_products_path(self, category: str) -> str:
        return os.path.join(self.DATA_DIR, category, "products.jsonl")


settings = Settings()