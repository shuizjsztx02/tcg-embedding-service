import json
import os
import logging

import numpy as np
import faiss

from app.config import settings

log = logging.getLogger(__name__)


class IndexService:
    """Per-category FAISS index manager.

    Each category maintains its own visual (DINOv2) and text (BGE) index.
    Indexes are loaded on startup and queried by category.
    """

    def __init__(self):
        self.visual_indexes: dict[str, faiss.Index] = {}
        self.visual_ids: dict[str, list[str]] = {}
        self.text_indexes: dict[str, faiss.Index] = {}
        self.text_ids: dict[str, list[str]] = {}
        self.products: dict[str, dict[str, dict]] = {}

    def load_category(self, category: str) -> bool:
        """Load visual + text index + products for a single category.

        Returns True if at least one index was loaded.
        """
        visual_dir = settings.get_visual_index_dir(category)
        text_dir = settings.get_text_index_dir(category)
        products_path = settings.get_products_path(category)
        image_dir = settings.get_image_dir(category)
        loaded = False

        # --- Visual index ---
        if os.path.exists(visual_dir):
            try:
                emb = np.load(os.path.join(visual_dir, "embeddings.npy"))
                with open(os.path.join(visual_dir, "ids.json"), "r") as f:
                    ids = json.load(f)
                idx = faiss.IndexFlatIP(emb.shape[1])
                idx.add(emb)
                self.visual_indexes[category] = idx
                self.visual_ids[category] = ids
                log.info(f"  [{category}] visual index: {idx.ntotal} vectors, dim={emb.shape[1]}")
                loaded = True
            except Exception as e:
                log.warning(f"  [{category}] visual index load failed: {e}")

        # --- Text index ---
        if os.path.exists(text_dir):
            try:
                emb = np.load(os.path.join(text_dir, "embeddings.npy"))
                with open(os.path.join(text_dir, "ids.json"), "r") as f:
                    ids = json.load(f)
                idx = faiss.IndexFlatIP(emb.shape[1])
                idx.add(emb)
                self.text_indexes[category] = idx
                self.text_ids[category] = ids
                log.info(f"  [{category}] text index: {idx.ntotal} vectors, dim={emb.shape[1]}")
                loaded = True
            except Exception as e:
                log.warning(f"  [{category}] text index load failed: {e}")

        # --- Products ---
        if os.path.exists(products_path):
            try:
                prods = {}
                with open(products_path, "r", encoding="utf-8") as f:
                    for line in f:
                        d = json.loads(line)
                        if d.get("productId"):
                            prods[str(d["productId"])] = d
                self.products[category] = prods
                log.info(f"  [{category}] products: {len(prods)} records")
            except Exception as e:
                log.warning(f"  [{category}] products load failed: {e}")

        return loaded

    def load_all_categories(self) -> list[str]:
        """Scan DATA_DIR for all available categories."""
        loaded = []
        if not os.path.isdir(settings.DATA_DIR):
            log.warning(f"Index base dir not found: {settings.DATA_DIR}")
            return loaded
        for name in sorted(os.listdir(settings.DATA_DIR)):
            cat_dir = os.path.join(settings.DATA_DIR, name)
            if not os.path.isdir(cat_dir):
                continue
            if self.load_category(name):
                loaded.append(name)
        log.info(f"Categories loaded: {loaded}")
        return loaded

    def search_visual(self, category: str, query: np.ndarray, top_k: int = 5):
        """Search visual index for a category."""
        index = self.visual_indexes.get(category)
        ids = self.visual_ids.get(category)
        if index is None or ids is None:
            return None
        scores, indices = index.search(query.reshape(1, -1), min(top_k, index.ntotal))
        results = []
        for k in range(len(indices[0])):
            idx = int(indices[0, k])
            if idx < 0:
                continue
            card_id = ids[idx]
            pid = card_id.removesuffix("_200w")
            product = self.products.get(category, {}).get(pid)
            results.append({
                "rank": k + 1,
                "card_id": card_id,
                "score": float(scores[0, k]),
                "product_name": product.get("productName", card_id) if product else card_id,
                "product": product,
            })
        return results

    def search_text(self, category: str, query: np.ndarray, top_k: int = 5):
        """Search text index for a category."""
        index = self.text_indexes.get(category)
        ids = self.text_ids.get(category)
        products = self.products.get(category, {})
        if index is None or ids is None:
            return None
        scores, indices = index.search(query.reshape(1, -1), min(top_k, index.ntotal))
        results = []
        for k in range(len(indices[0])):
            idx = int(indices[0, k])
            if idx < 0:
                continue
            pid = ids[idx]
            prod = products.get(pid, {})
            attrs = prod.get("customAttributes") or {}
            image_dir = settings.get_image_dir(category)
            has_image = os.path.exists(os.path.join(image_dir, f"{pid}_200w.jpg"))
            results.append({
                "rank": k + 1,
                "product_id": pid,
                "product_name": prod.get("productName") or pid,
                "set_name": prod.get("setName") or "",
                "number": attrs.get("number") or "",
                "rarity": prod.get("rarityName") or "",
                "score": float(scores[0, k]),
                "has_image": has_image,
                "product": prod if prod else None,
            })
        return results

    @property
    def categories(self) -> list[str]:
        return list(self.visual_indexes.keys() | self.text_indexes.keys())

    @property
    def dino_index_sizes(self) -> dict[str, int]:
        return {k: v.ntotal for k, v in self.visual_indexes.items()}

    @property
    def text_index_sizes(self) -> dict[str, int]:
        return {k: v.ntotal for k, v in self.text_indexes.items()}