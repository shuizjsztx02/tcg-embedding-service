"""Shared candidate embedding and ranking for both DINO endpoints."""
import time

import numpy as np
import torch

from dino_preprocess import assess_quality, prepare_candidates
from preprocess import to_model_input


@torch.no_grad()
def embed_candidates(model, images):
    mean = np.array([.485, .456, .406], dtype=np.float32)
    std = np.array([.229, .224, .225], dtype=np.float32)
    features = []
    # Small batches bound CPU memory while amortizing model overhead.
    for start in range(0, len(images), 4):
        arrays = [((np.asarray(to_model_input(im), dtype=np.float32) / 255 - mean) / std)
                  .transpose(2, 0, 1) for im in images[start:start + 4]]
        out = model(torch.from_numpy(np.stack(arrays)))
        if hasattr(out, "last_hidden_state"):
            out = out.last_hidden_state[:, 0]
        elif out.ndim == 3:
            out = out[:, 0]
        features.append(out.cpu().numpy().astype(np.float32))
    features = np.concatenate(features)
    norms = np.linalg.norm(features, axis=1, keepdims=True)
    return features / np.maximum(norms, 1e-12)


def rank_candidates(features, index, ids, top_k=5):
    """Merge by card ID across views; margin includes other orientations."""
    if index.ntotal == 0:
        return [], None
    scores, indices = index.search(features, min(top_k, index.ntotal))
    merged = {}
    for candidate, (row_scores, row_indices) in enumerate(zip(scores, indices)):
        for score, idx in zip(row_scores, row_indices):
            if idx < 0:
                continue
            card_id = ids[int(idx)]
            if card_id not in merged or score > merged[card_id]["score"]:
                merged[card_id] = {"card_id": card_id, "score": float(score), "candidate": candidate}
    ranked = sorted(merged.values(), key=lambda row: row["score"], reverse=True)[:top_k]
    return ranked, ranked[0]["candidate"] if ranked else None


def search_image(img, model, index, ids, top_k=5):
    start = time.perf_counter()
    candidates, meta = prepare_candidates(img)
    meta["preprocess_ms"] = round((time.perf_counter() - start) * 1000, 1)
    features = embed_candidates(model, [im for im, _ in candidates])
    ranked, winner = rank_candidates(features, index, ids, top_k)
    selected = None
    if winner is not None:
        selected, provenance = candidates[winner]
        meta["selected"] = provenance
        meta["selected_quality"], _ = assess_quality(selected)
        if meta["quad_found"] and provenance["source"] == "original":
            meta["warnings"].append("裁切候选未胜出，本次使用整图检索；建议检查卡牌边界或重新拍摄")
    meta["total_ms"] = round((time.perf_counter() - start) * 1000, 1)
    return ranked, selected, meta
