#!/usr/bin/env python3
"""Quick test of the /v1/search endpoint."""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")


def test_search(card_id, port=8001):
    img_path = os.path.join(IMG_DIR, card_id + ".jpg")
    assert os.path.exists(img_path), "Missing " + img_path

    with open(img_path, "rb") as f:
        img_data = f.read()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = b"--" + boundary.encode() + b"\r\n"
    body += b'Content-Disposition: form-data; name="file"; filename="' + card_id.encode() + b'.jpg"\r\n'
    body += b"Content-Type: image/jpeg\r\n\r\n"
    body += img_data
    body += b"\r\n--" + boundary.encode() + b"--\r\n"

    req = urllib.request.Request(
        f"http://localhost:{port}/v1/search",
        data=body,
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary},
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result


def main():
    card_ids = ["100503_200w", "100507_200w", "117266_200w"]
    passed = 0
    failed = 0
    for cid in card_ids:
        if not os.path.exists(os.path.join(IMG_DIR, cid + ".jpg")):
            print("SKIP", cid, ": image not found")
            continue
        result = test_search(cid)
        top1 = result["results"][0]
        correct = top1["card_id"] == cid
        status = "OK" if correct else "FAIL"
        if correct:
            passed += 1
        else:
            failed += 1
        print(f"{status} {cid}: top1={top1['card_id']} score={top1['score']} ({result['query_time_ms']}ms)")
        for r in result["results"]:
            print(f"    #{r['rank']}: {r['card_id']} {r['score']}")
        print()

    print(f"=== {passed} passed, {failed} failed ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
