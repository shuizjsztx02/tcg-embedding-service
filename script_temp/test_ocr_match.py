import requests, json, sys

with open("test-images/f52ee7479b6-20260722-22fecf_tcg_img_1784733452824.jpg", "rb") as f:
    img_data = f.read()

resp = requests.post(
    "http://127.0.0.1:8057/v1/ocr-match",
    files={"file": ("test.jpg", img_data, "image/jpeg")},
    timeout=120
)
data = resp.json()
print("Status:", data["status"])
print("Blocks:", data["total_blocks"])
print("Query:", data["query_text"][:200])
print("Results:", len(data["results"]))
for r in data["results"]:
    pid = r["product_id"]
    name = r.get("product_name", "?")
    score = r["score"]
    print(f"  #{r['rank']} id={pid} name={name} score={score}")
