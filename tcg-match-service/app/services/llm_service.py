# -*- coding: utf-8 -*-
"""LLM 调用封装（Anthropic-style /v1/messages）。

品类判断 + 兜底识图两个入口。纯 HTTP 客户端，零模型加载。
不产出价格，只产出身份/品类信息。
"""
import base64
import io
import json
import logging
import time
from typing import Optional

import requests
from PIL import Image

from app.config import settings

log = logging.getLogger(__name__)

CATEGORY_PROMPT = (
    "你是TCG卡牌识别专家。判断图片：(1)是否一张集换式卡牌；(2)若是，最可能的品类（从候选中选，"
    "最多2个，按可能性降序；不确定英/日文版时两个都返回）。\n"
    "候选品类: {categories}\n"
    "只回复JSON：{{\"is_card\": true|false, \"categories\": [{{\"name\":\"<候选之一>\",\"confidence\":0~1}}]}}"
)

FALLBACK_PROMPT = (
    "你是TCG卡牌识别专家。仔细识别这张卡并抽取信息，不确定就填null，禁止编造。\n"
    "只回复JSON：{{\"card_name\":\"...\",\"set_name\":\"...\","
    "\"card_number\":\"如151/172或XY55\",\"language\":\"en|ja|...\",\"card_type\":\"...\",\"confidence\":0~1}}"
)


class LLMService:
    """Anthropic-style /v1/messages 客户端。"""

    def __init__(self):
        self.url = settings.LLM_BASE_URL.rstrip("/") + "/v1/messages"
        self.category_model = settings.LLM_CATEGORY_MODEL
        self.fallback_model = settings.LLM_FALLBACK_MODEL
        self.timeout = settings.LLM_TIMEOUT_S

    # ---- 对外入口 ----

    def classify_category(self, image: Image.Image, whitelist: list[str]) -> dict:
        """S1 品类判断。

        Args:
            image: 预处理后卡图（PIL RGB）
            whitelist: 有效品类白名单，来自 index.visual_indexes.keys()

        Returns:
            {ok: bool, is_card: bool, categories: [{name, confidence}], latency_ms: float, error: str}
        """
        t0 = time.time()
        b64 = self._to_b64(image, 512)
        prompt = CATEGORY_PROMPT.format(categories=", ".join(sorted(whitelist)))
        text, err = self._post(self.category_model, [
            {"type": "text", "text": prompt},
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
        ], max_tokens=200)
        lat = (time.time() - t0) * 1000

        if err:
            return {"ok": False, "is_card": True, "categories": [], "latency_ms": round(lat), "error": err}

        obj = self._extract_json(text)
        if obj is None:
            return {"ok": False, "is_card": True, "categories": [], "latency_ms": round(lat), "error": "json_parse_failed"}

        is_card = obj.get("is_card", True)
        cats = obj.get("categories", [])
        if not isinstance(cats, list):
            cats = []
        cats = [c for c in cats if isinstance(c, dict) and c.get("name") in whitelist][:2]
        return {"ok": True, "is_card": bool(is_card), "categories": cats, "latency_ms": round(lat), "error": ""}

    def recognize_card(self, image: Image.Image) -> dict:
        """S3 兜底识图。

        Returns:
            {ok: bool, identity: dict|None, latency_ms: float, error: str}
            identity = {card_name, set_name, card_number, language, card_type, confidence}
        """
        t0 = time.time()
        b64 = self._to_b64(image, 1024)
        text, err = self._post(self.fallback_model, [
            {"type": "text", "text": FALLBACK_PROMPT},
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
        ], max_tokens=400)
        lat = (time.time() - t0) * 1000

        if err:
            return {"ok": False, "identity": None, "latency_ms": round(lat), "error": err}

        obj = self._extract_json(text)
        if obj is None:
            return {"ok": False, "identity": None, "latency_ms": round(lat), "error": "json_parse_failed"}

        identity = {
            "card_name": obj.get("card_name") or None,
            "set_name": obj.get("set_name") or None,
            "card_number": obj.get("card_number") or None,
            "language": obj.get("language") or None,
            "card_type": obj.get("card_type") or None,
            "confidence": obj.get("confidence"),
        }
        return {"ok": True, "identity": identity, "latency_ms": round(lat), "error": ""}

    # ---- 内部 ----

    def _to_b64(self, image: Image.Image, long_edge: int) -> str:
        """等比缩放至 long_edge，JPEG q85，返回 base64 字符串。"""
        w, h = image.size
        scale = long_edge / max(w, h)
        if scale < 1:
            image = image.resize((int(w * scale), int(h * scale)), Image.BICUBIC)
        buf = io.BytesIO()
        image.save(buf, "JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode()

    def _post(self, model: str, blocks: list, max_tokens: int) -> tuple[Optional[str], Optional[str]]:
        """POST /v1/messages，超时 + 重试 1 次；返回 (text, err)。"""
        for attempt in range(2):
            try:
                resp = requests.post(
                    self.url,
                    json={
                        "model": model,
                        "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": blocks}],
                    },
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                resp_data = resp.json()
                text = "".join(
                    b.get("text", "") for b in resp_data.get("content", []) if b.get("type") == "text"
                )
                return text, None
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                log.warning(f"LLM _post attempt {attempt + 1} failed: {err}")
        return None, err

    def _extract_json(self, text: str) -> Optional[dict]:
        """容忍式 JSON 解析：直接 parse → 剥 ```json fence → 取首个 {…} 三级兜底。"""
        if not text:
            return None
        # 1. 直接 parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        # 2. 剥 ```json ... ``` fence
        text = text.strip()
        if text.startswith("```"):
            text = text.removeprefix("```json").removeprefix("```").rstrip("`").strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        # 3. 取首个 { 到末尾（或最后一个 }）
        start = text.find("{")
        if start >= 0:
            end = text.rfind("}")
            if end > start:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    pass
        return None