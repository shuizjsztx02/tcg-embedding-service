"""Regression tests for recognition batch padding and text/box correspondence."""
import unittest

import numpy as np

from ppocr_v4_engine import PPOCRv4Recognizer


class IdentitySession:
    def __init__(self):
        self.widths = []

    def run(self, feed):
        self.widths.append(feed["x"].shape[-1])
        return [feed["x"]]


class RecognizerTests(unittest.TestCase):
    def recognizer(self):
        # Bypass model loading; encode crop identity as a constant pixel value.
        rec = PPOCRv4Recognizer.__new__(PPOCRv4Recognizer)
        rec._session = IdentitySession()
        rec._rec_img_shape = [3, 48, 320]
        rec._batch_num = 3
        rec._postprocess = lambda batch: [
            (str(round(float(x[0, 0, 0] + 1) * 127.5)), .95) for x in batch
        ]
        return rec

    def test_text_returns_in_original_crop_order_across_batches(self):
        rec = self.recognizer()
        crops = [np.full((10, width, 3), i + 1, np.uint8)
                 for i, width in enumerate([90, 20, 60, 10, 80, 30, 50])]
        results, _ = rec(crops)
        self.assertEqual([text for text, _ in results], list("1234567"))

    def test_short_text_keeps_model_minimum_padding_width(self):
        rec = self.recognizer()
        rec([np.full((20, 40, 3), 255, np.uint8)])
        self.assertEqual(rec._session.widths, [320])

    def test_empty_crops_do_not_invoke_model(self):
        rec = self.recognizer()
        self.assertEqual(rec([]), ([], 0.0))
        self.assertEqual(rec._session.widths, [])


if __name__ == "__main__":
    unittest.main()
