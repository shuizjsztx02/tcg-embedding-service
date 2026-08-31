"""API contract tests using real FAISS and a small deterministic image encoder."""
import io
import os
import sys
import unittest
from unittest.mock import patch

import faiss
import numpy as np
import torch
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import main as api


class TinyEncoder(torch.nn.Module):
    def forward(self, x):
        return torch.tensor([[.8, .6, 0.]], dtype=torch.float32).repeat(len(x), 1)


class DinoApiTests(unittest.TestCase):
    def setUp(self):
        index = faiss.IndexFlatIP(3)
        index.add(np.eye(3, dtype=np.float32))
        self.state = patch.multiple(api, model=TinyEncoder(), faiss_index=index,
                                    index_ids=["A", "B", "C"], products={})
        self.state.start()
        self.addCleanup(self.state.stop)
        # Do not run the unrelated OCR/BGE startup or download any model.
        self.client = TestClient(api.app)
        self.addCleanup(self.client.close)
        buffer = io.BytesIO()
        Image.new("RGB", (160, 240), "white").save(buffer, format="PNG")
        self.photo = buffer.getvalue()

    def request(self, endpoint):
        return self.client.post(endpoint, files={"file": ("photo.png", self.photo, "image/png")})

    def test_endpoints_share_result_and_surface_failed_crop_warning(self):
        search = self.request("/v1/search")
        match = self.request("/v1/match")
        self.assertEqual(search.status_code, 200)
        self.assertEqual(match.status_code, 200)
        search, match = search.json(), match.json()
        self.assertEqual(len(search["results"]), 3)
        self.assertEqual(search["results"][0]["card_id"], match["card_id"])
        self.assertEqual(search["results"][0]["score"], match["score"])
        self.assertTrue(search["warnings"])
        self.assertEqual(search["warnings"], match["warnings"])
        self.assertFalse(search["preprocessing"]["quad_found"])
        self.assertEqual(search["preprocessing"]["selected"]["source"], "original")

    def test_empty_index_returns_service_error(self):
        api.faiss_index = faiss.IndexFlatIP(3)
        api.index_ids = []
        for endpoint in ("/v1/match", "/v1/search"):
            self.assertEqual(self.request(endpoint).status_code, 503)

    def test_invalid_and_empty_uploads_still_rejected(self):
        for endpoint in ("/v1/match", "/v1/search"):
            for data in (b"", b"invalid image"):
                response = self.client.post(endpoint, files={"file": ("x.png", data, "image/png")})
                self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
