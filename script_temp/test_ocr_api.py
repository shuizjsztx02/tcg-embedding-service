"""Both OCR routes must use the same pixels, text and quality decisions."""
import base64
import io
import os
import sys
import unittest
from unittest.mock import patch

import faiss
import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import main as api
from script_temp.ocr_engine import OCRResult


class Engine:
    def read(self, image):
        return [OCRResult("Professor Turo's Scenario", .96, [[2, 2], [90, 2], [90, 15], [2, 15]]),
                OCRResult("ajnl nonsense", .6, [[2, 20], [90, 20], [90, 35], [2, 35]])], .01


class TextEncoder:
    def __init__(self):
        self.queries = []

    def encode(self, text, **kwargs):
        self.queries.append(text)
        return np.array([1, 0], np.float32)


class OcrApiTests(unittest.TestCase):
    def setUp(self):
        index = faiss.IndexFlatIP(2)
        index.add(np.array([[1, 0], [.8, .6], [0, 1], [-.8, .6], [-1, 0]], np.float32))
        self.encoder = TextEncoder()
        state = patch.multiple(api, ocr_engine=Engine(), text_model=self.encoder,
                               text_index=index, text_ids=list("ABCDE"), products={})
        state.start()
        self.addCleanup(state.stop)
        self.client = TestClient(api.app)
        self.addCleanup(self.client.close)
        buffer = io.BytesIO()
        Image.new("RGB", (200, 280), (90, 100, 110)).save(buffer, format="PNG")
        self.photo = buffer.getvalue()

    def request(self, endpoint, data=None):
        return self.client.post(endpoint, files={"file": ("photo.png", self.photo if data is None else data, "image/png")})

    def test_routes_share_actual_ocr_image_and_filtered_query(self):
        read, match = self.request("/v1/ocr"), self.request("/v1/ocr-match")
        self.assertEqual((read.status_code, match.status_code), (200, 200))
        read, match = read.json(), match.json()
        self.assertEqual(match["query_text"], "Professor Turo's Scenario")
        self.assertEqual(read["query_text"], match["query_text"])
        self.assertEqual(read["full_text"], match["full_text"])
        self.assertIn("ajnl nonsense", read["full_text"])
        self.assertEqual(read["preprocessed_image"], match["preprocessed_image"])
        self.assertEqual(read["preprocessing"], match["preprocessing"])
        self.assertEqual(self.encoder.queries, [api.BGE_QUERY_PREFIX + match["query_text"]])
        preview = Image.open(io.BytesIO(base64.b64decode(read["preprocessed_image"])))
        self.assertEqual(preview.size, tuple(read["preprocessing"]["image_size"]))
        self.assertEqual(preview.getpixel((0, 0)), (90, 100, 110))

    def test_uncertain_text_does_not_trigger_embedding_search(self):
        class UncertainEngine:
            def read(self, image):
                return [OCRResult("ajnl nonsense", .6, [[2, 2], [90, 2], [90, 15], [2, 15]])], 0
        with patch.object(api, "ocr_engine", UncertainEngine()):
            response = self.request("/v1/ocr-match").json()
        self.assertEqual(response["results"], [])
        self.assertEqual(self.encoder.queries, [])
        self.assertIn("ajnl nonsense", response["full_text"])
        self.assertTrue(response["warnings"])

    def test_invalid_uploads_are_rejected(self):
        for endpoint in ("/v1/ocr", "/v1/ocr-match"):
            for data in (b"", b"invalid"):
                self.assertEqual(self.request(endpoint, data).status_code, 400)


if __name__ == "__main__":
    unittest.main()
