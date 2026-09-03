# -*- coding: utf-8 -*-
"""POST /v2/recognize — 端到端识别路由。

S1 品类判断 → S2 DINO 匹配 → 分层决策 → S3 LLM 兜底 → DB 反查 → 价格组装。
"""
import io
import re
import time
import logging
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from PIL import Image

from app.config import settings
from app.models.schemas import RecognizeResponse
from app.services.dino_service import DINOv2Service
from app.services.index_service import IndexService
from app.services.llm_service import LLMService

log = logging.getLogger(__name__)
router = APIRouter()
MAX_CANDIDATES = 5
MAX_FILE_SIZE = 10 * 1024 * 1024


def _init_route(dino_service: DINOv2Service, index_service: IndexService, llm_service: LLMService):
    """Inject dependencies (called from main.py on startup)."""
    router.dino_service = dino_service
    router.index_service = index_service
    router.llm_service = llm_service


# ---- 卡号归一化 ----

def _norm_num(s: Optional[str]) -> str:
    """卡号归一化：去空白/连字符/斜杠，大写。"""
    if not s:
        return ""
    return re.sub(r"[\s\-/]+", "", str(s)).upper()


# ---- 价格组装 ----

def _assemble_price(prod: Optional[dict]) -> Optional[dict]:
    """从 product 字典提取价格字段，容忍缺失。"""
    if not prod:
        return None
    def num(v):
        return v if isinstance(v, (int, float)) else None
    def ival(v):
        return int(v) if isinstance(v, (int, float)) else None
    return {
        "marketPrice": num(prod.get("marketPrice")),
        "lowestPrice": num(prod.get("lowestPrice")),
        "lowestPriceWithShipping": num(prod.get("lowestPriceWithShipping")),
        "medianPrice": num(prod.get("medianPrice")),
        "sellers": ival(prod.get("sellers")),
        "listings": ival(prod.get("listings")),
        "currency": "USD",
        "asOf": settings.PRICE_AS_OF or None,
    }


def _assemble_product(prod: Optional[dict]) -> Optional[dict]:
    """从 product 字典提取基本信息字段。"""
    if not prod:
        return None
    a = prod.get("customAttributes") or {}
    attacks = [a[k] for k in ("attack1", "attack2", "attack3", "attack4") if a.get(k)]
    return {
        "productName": prod.get("productName"),
        "setName": prod.get("setName"),
        "setCode": prod.get("setCode"),
        "rarityName": prod.get("rarityName"),
        "number": a.get("number"),
        "hp": a.get("hp"),
        "attacks": attacks,
        "cardType": a.get("cardType"),
    }


# ---- DINO 合并 ----

def _merge_visual(index: IndexService, feat, categories: list[str]) -> list[dict]:
    """单次 embed 后跨品类搜索合并，返回按分数降序的 top-5。"""
    merged = []
    for cat in categories:
        res = index.search_visual(cat, feat, 5)
        if not res:
            continue
        for r in res:
            r["category"] = cat
            merged.append(r)
    merged.sort(key=lambda r: r["score"], reverse=True)
    return merged[:5]


# ---- DB 反查 ----

def _cands(items: list[tuple]) -> list[dict]:
    """将 (category, pid, prod) 列表转为 candidate dict。"""
    result = []
    for cat, pid, prod in items:
        result.append({
            "product_id": pid,
            "category": cat,
            "product": _assemble_product(prod),
            "price": _assemble_price(prod),
        })
        if len(result) >= MAX_CANDIDATES:
            break
    return result


def _lookup_by_identity(index: IndexService, identity: dict, categories: list[str]) -> tuple:
    """LLM 兜底后，用身份信息反查 products.jsonl。

    Returns:
        (status, decision_path, product_id, product, price, candidates)
        status: matched / candidates / recognized_no_db
    """
    num = _norm_num(identity.get("card_number"))
    sname = (identity.get("set_name") or "").strip().lower()
    cname = (identity.get("card_name") or "").strip().lower()

    exact = []      # 卡号 + 系列都命中
    num_hits = []   # 仅卡号命中
    name_hits = []  # 仅卡名模糊

    for cat in categories:
        for pid, prod in index.products.get(cat, {}).items():
            a = prod.get("customAttributes") or {}
            pnum = _norm_num(a.get("number"))
            pset = (prod.get("setName") or "").lower()
            pcode = (prod.get("setCode") or "").lower()

            if num and pnum and num == pnum:
                if sname and (sname == pset or sname == pcode):
                    exact.append((cat, pid, prod))
                else:
                    num_hits.append((cat, pid, prod))
            elif cname and cname in (prod.get("productName") or "").lower():
                name_hits.append((cat, pid, prod))

    if len(exact) == 1:
        cat, pid, prod = exact[0]
        return ("matched", "llm_fallback_db_hit", pid,
                _assemble_product(prod), _assemble_price(prod), [])
    if exact:
        return ("candidates", "candidates", None, None, None, _cands(exact))
    if num_hits:
        return ("candidates", "candidates", None, None, None, _cands(num_hits))
    if name_hits:
        return ("candidates", "candidates", None, None, None, _cands(name_hits))
    return ("recognized_no_db", "recognized_no_db", None, None, None, [])


# ---- 响应组装 ----

def _resp(status, decision_path, t0, category=None, product_id=None,
          product=None, price=None, candidates=None, identity=None,
          confidence=None, scores=None, warnings=None):
    return RecognizeResponse(
        status=status,
        decision_path=decision_path,
        category=category,
        product_id=product_id,
        product=product,
        price=price,
        candidates=candidates or [],
        identity=identity,
        confidence=confidence,
        scores=scores or {},
        in_database=None if status in ("recognized_no_db", "not_a_card", "error", "unrecognized")
                    else (True if status == "matched" else None),
        warnings=warnings or [],
        latency_ms=round((time.time() - t0) * 1000, 1),
    )


# ---- 主路由 ----

@router.post("/v2/recognize", response_model=RecognizeResponse)
async def recognize(
    file: UploadFile = File(...),
    ocr_text: Optional[str] = Form(None),
    ocr_lang: Optional[str] = Form(None),
    category_hint: Optional[str] = Form(None),
):
    t0 = time.time()

    # 文件解码（仅解码，不做业务校验）
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(400, "Empty file")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
    try:
        img = Image.open(io.BytesIO(contents))
        img.load()
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")

    dino = getattr(router, "dino_service", None)
    index = getattr(router, "index_service", None)
    llm = getattr(router, "llm_service", None)
    if dino is None or index is None or llm is None:
        raise HTTPException(503, "Service not ready")

    whitelist = set(index.visual_indexes.keys())
    warnings = []
    scores = {"ocr_used": None, "card_number_matched": None}

    # ---- S1 品类判断 ----
    candidates = []
    source = None
    if category_hint and category_hint in whitelist:
        candidates = [category_hint]
        source = "hint"
        log.info(f"RECOGNIZE S1: category_hint={category_hint}")
    else:
        if category_hint:
            warnings.append(f"category_hint '{category_hint}' not in whitelist, fallback to LLM")
        cr = llm.classify_category(img, sorted(whitelist))
        if not cr["ok"]:
            log.warning(f"RECOGNIZE S1 LLM failed: {cr.get('error')}")
            if category_hint:
                candidates = [category_hint]
                source = "hint_fallback"
                warnings.append("LLM category failed, fallback to hint")
            else:
                return _resp("error", "category_failed", t0, warnings=warnings + ["LLM category failed"])
        if not cr.get("is_card", True):
            return _resp("not_a_card", "not_a_card", t0)
        if not candidates:
            candidates = [c["name"] for c in cr.get("categories", []) if c["name"] in whitelist][:2]
            source = "llm"
        if not candidates:
            return _resp("error", "category_failed", t0, warnings=warnings + ["LLM returned no valid categories"])
    scores["category_source"] = source
    scores["category_candidates"] = candidates

    # ---- S2 DINO 匹配 ----
    feat = dino.embed(img)
    merged = _merge_visual(index, feat, candidates)
    if not merged:
        return _resp("error", "no_visual_results", t0, warnings=warnings + ["DINO returned no results"])
    best = merged[0]
    margin = best["score"] - merged[1]["score"] if len(merged) > 1 else 1.0
    scores["dino_top1"] = round(best["score"], 4)
    scores["dino_margin"] = round(margin, 4)
    scores["category"] = best.get("category")
    log.info(
        f"RECOGNIZE S2: cat={best.get('category')} "
        f"card_id={best['card_id']} score={best['score']:.4f} margin={margin:.4f}"
    )

    # ---- 高置信路径 ----
    if best["score"] >= settings.TAU_HIGH and margin >= settings.MARGIN_HIGH:
        pid = best["card_id"].removesuffix("_200w")
        cat = best.get("category") or candidates[0]
        prod = index.products.get(cat, {}).get(pid)
        if prod is None:
            warnings.append(f"DINO matched but product {pid} not found in category {cat}")
        log.info(f"RECOGNIZE path=dino_high pid={pid}")
        return _resp(
            "matched", "dino_high", t0,
            category=cat, product_id=pid,
            product=_assemble_product(prod), price=_assemble_price(prod),
            confidence=best["score"], scores=scores, warnings=warnings,
        )

    # ---- 低置信 → LLM 兜底 ----
    fb = llm.recognize_card(img)
    scores["fallback_latency_ms"] = round(fb.get("latency_ms", 0))
    if not fb["ok"] or not fb.get("identity"):
        log.info(f"RECOGNIZE path=unrecognized (fallback failed: {fb.get('error')})")
        return _resp("unrecognized", "unrecognized", t0, scores=scores, warnings=warnings)

    status, decision_path, pid, product, price, cands = _lookup_by_identity(
        index, fb["identity"], candidates
    )
    identity = fb["identity"] if status == "recognized_no_db" else None
    log.info(f"RECOGNIZE path={decision_path} status={status} pid={pid}")
    return _resp(
        status, decision_path, t0,
        category=candidates[0] if candidates else None,
        product_id=pid, product=product, price=price,
        candidates=cands, identity=identity,
        confidence=identity.get("confidence") if identity else None,
        scores=scores, warnings=warnings,
    )