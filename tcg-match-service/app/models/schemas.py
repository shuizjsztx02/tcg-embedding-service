from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    status: str
    categories: list[str] = []
    dino_index_sizes: dict[str, int] = {}
    text_index_sizes: dict[str, int] = {}


class SearchResult(BaseModel):
    rank: int
    card_id: str
    score: float
    product_name: str = ""
    product: Optional[dict] = None


class DinoMatchResponse(BaseModel):
    status: str
    category: str
    query_time_ms: float
    results: list[SearchResult] = []
    warnings: list[str] = []


class OcrMatchResult(BaseModel):
    rank: int
    product_id: str
    product_name: str
    set_name: str = ""
    number: str = ""
    rarity: str = ""
    score: float
    has_image: bool = False
    product: Optional[dict] = None


class OcrMatchResponse(BaseModel):
    status: str
    category: str
    full_text: str = ""
    query_text: str
    query_time_ms: float
    warnings: list[str] = []
    results: list[OcrMatchResult] = []


class RecognizeResponse(BaseModel):
    status: str
    decision_path: str
    category: Optional[str] = None
    product_id: Optional[str] = None
    product: Optional[dict] = None
    price: Optional[dict] = None
    candidates: list[dict] = []
    identity: Optional[dict] = None
    confidence: Optional[float] = None
    scores: dict = {}
    in_database: Optional[bool] = None
    warnings: list[str] = []
    latency_ms: float = 0.0