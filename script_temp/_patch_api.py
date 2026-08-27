import os, sys, json

path = r'D:\Code2026\tcg-embedding-service\app\main.py'
lines = open(path, 'r', encoding='utf-8').readlines()

# Insert SearchResponse model after line 60 (0-indexed)
search_model = 'class SearchResult(BaseModel):\n    rank: int\n    card_id: str\n    score: float\n\n\nclass SearchResponse(BaseModel):\n    status: str\n    query_time_ms: float\n    results: list[SearchResult]\n\n\n'

lines.insert(61, search_model)

search_endpoint = '''

@app.post("/v1/search", response_model=SearchResponse)
async def search(file: UploadFile = File(...)):
    """Upload card image -> return top-5 matches without threshold filtering."""
    t0 = time.time()

    # Read & validate
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files are supported")
        img = Image.open(io.BytesIO(contents))
        img.load()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Invalid image: {e}")

    # Preprocess: try all orientation candidates, pick the best score
    cands = list(orientation_candidates(img))
    best_score = -1.0
    best_feat = None

    for cand in cands:
        inp = to_model_input(cand)
        feat = embed_single(model, inp)
        scores, indices = faiss_index.search(feat.reshape(1, -1), 5)
        s0 = float(scores[0, 0])
        if s0 > best_score:
            best_score = s0
            best_feat = feat

    # Search with the best orientation
    scores, indices = faiss_index.search(best_feat.reshape(1, -1), 5)
    elapsed = (time.time() - t0) * 1000

    results = []
    for k in range(5):
        results.append(SearchResult(
            rank=k + 1,
            card_id=index_ids[int(indices[0, k])],
            score=round(float(scores[0, k]), 4),
        ))

    log.info(f"SEARCH top1={results[0].card_id} score={results[0].score:.4f} ({elapsed:.0f}ms)")
    return SearchResponse(
        status="ok",
        query_time_ms=round(elapsed, 1),
        results=results,
    )
'''

lines.append(search_endpoint)

open(path, 'w', encoding='utf-8').write(''.join(lines))
import ast
ast.parse(open(path, 'r', encoding='utf-8').read())
print('Added search endpoint. Python syntax OK')
