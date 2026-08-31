"""Direction, quality selection and query-text safety without model downloads."""
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

import ocr_pipeline as pipeline
from script_temp.ocr_engine import OCRResult


def block(text, confidence=.95, y=10):
    return OCRResult(text=text, confidence=confidence,
                     bbox=[[5, y], [95, y], [95, y + 10], [5, y + 10]])


class DirectionEngine:
    def read(self, image):
        h, w = image.shape[:2]
        upright = h > w and image[:h // 4].mean() > image[-h // 4:].mean()
        if upright:
            return [block("Professor Turo's Scenario", .96)], .01
        # More blocks than the correct orientation: block count is unsafe.
        return [block(t, .6, i * 15) for i, t in enumerate(["urn", "ajnl", "xoi"])], .01


class PipelineTests(unittest.TestCase):
    def photo(self):
        arr = np.full((280, 200, 3), 50, np.uint8)
        arr[:70] = 230
        return Image.fromarray(arr)

    def test_all_photo_orientations_choose_readable_text_and_matching_preview(self):
        for angle in (0, 90, 180, 270):
            with self.subTest(angle=angle), patch.object(pipeline, "detect_card", return_value=None):
                result = pipeline.read_card(self.photo().rotate(angle, expand=True), DirectionEngine())
            self.assertEqual(result.query_text, "Professor Turo's Scenario")
            arr = np.array(result.image)
            self.assertGreater(arr[:70].mean(), arr[-70:].mean())
            self.assertEqual(result.blocks[0]["text"], "Professor Turo's Scenario")
            self.assertTrue(result.warnings)  # Detection failure is explicit.

    def test_query_excludes_uncertain_text_and_deduplicates_in_reading_order(self):
        class Engine:
            def read(self, image):
                return [block("257/182", .9, 170), block("ajnl nonsense", .6, 60),
                        block("Professor Turo's Scenario", .96, 10),
                        block("257/182", .85, 190)], 0
        with patch.object(pipeline, "detect_card", return_value=None):
            result = pipeline.read_card(self.photo(), Engine())
        self.assertEqual(result.query_text, "Professor Turo's Scenario\n257/182")
        self.assertIn("ajnl nonsense", result.full_text)
        self.assertEqual(result.blocks[0]["bbox"][0][1], 10)

    def test_only_uncertain_text_does_not_become_a_search_query(self):
        class Engine:
            def read(self, image):
                return [block("ajnl nonsense", .6)], 0
        with patch.object(pipeline, "detect_card", return_value=None):
            result = pipeline.read_card(self.photo(), Engine())
        self.assertEqual(result.query_text, "")
        self.assertIn("ajnl nonsense", result.full_text)
        self.assertTrue(result.warnings)

    def test_enhancement_cannot_replace_a_better_raw_result(self):
        class Engine:
            def read(self, image):
                text = "Professor Turo's Scenario" if image[0, 0, 0] == 50 else "abc"
                return [block(text, .95 if len(text) > 3 else .6)], 0
        with patch.object(pipeline, "detect_card", return_value=None):
            result = pipeline.read_card(Image.new("RGB", (200, 280), (50, 50, 50)), Engine())
        self.assertFalse(result.metadata["selected"]["enhanced"])
        self.assertEqual(result.query_text, "Professor Turo's Scenario")

    def test_exif_rotation_is_applied_before_direction_selection(self):
        photo = self.photo().rotate(90, expand=True)
        photo.getexif()[274] = 6
        with patch.object(pipeline, "detect_card", return_value=None):
            result = pipeline.read_card(photo, DirectionEngine())
        self.assertEqual(result.metadata["selected"]["rotation"], 0)
        self.assertGreater(result.image.height, result.image.width)

    def test_bad_crop_can_fall_back_to_photo(self):
        quad = np.array([[0, 0], [100, 0], [100, 140], [0, 140]], np.float32)
        with patch.object(pipeline, "detect_card", return_value=quad), patch.object(
                pipeline, "perspective_correct", return_value=Image.new("RGB", (200, 280), "gray")):
            result = pipeline.read_card(self.photo(), DirectionEngine())
        self.assertEqual(result.metadata["selected"]["source"], "original")
        self.assertEqual(result.query_text, "Professor Turo's Scenario")

    def test_single_character_noise_cannot_defeat_a_readable_title(self):
        class Engine:
            def read(self, image):
                if image.shape[0] > image.shape[1] and image[:50].mean() > image[-50:].mean():
                    return [block("Pikachu", .80)], 0
                return [block(t, .99, i * 15) for i, t in enumerate("12345678")], 0
        with patch.object(pipeline, "detect_card", return_value=None):
            result = pipeline.read_card(self.photo().rotate(180), Engine())
        self.assertEqual(result.query_text, "Pikachu")

    def test_weak_directions_are_compared_after_enhancement_too(self):
        class Engine:
            def read(self, image):
                upright = image.shape[0] > image.shape[1] and image[:50].mean() > image[-50:].mean()
                improved = image[:50].mean() > 85
                return [block("Pikachu", .96 if upright and improved else .60)], 0
        arr = np.full((280, 200, 3), 35, np.uint8)
        arr[:70] = 80
        with patch.object(pipeline, "detect_card", return_value=None), patch.object(
                pipeline, "_enhance", side_effect=lambda img: Image.fromarray(np.asarray(img) + 10)):
            result = pipeline.read_card(Image.fromarray(arr).rotate(180), Engine())
        self.assertEqual(result.query_text, "Pikachu")
        self.assertEqual(result.metadata["selected"]["rotation"], 180)
        self.assertTrue(result.metadata["selected"]["enhanced"])
        self.assertLessEqual(len(result.metadata["candidates"]), 10)

    def test_card_rectification_preserves_bottom_edge_for_small_card_numbers(self):
        arr = np.array(self.photo())
        arr[-2:] = [0, 0, 200]
        quad = np.array([[0, 0], [199, 0], [199, 279], [0, 279]], np.float32)
        with patch.object(pipeline, "detect_card", return_value=quad):
            result = pipeline.read_card(Image.fromarray(arr), DirectionEngine())
        pixel = result.image.getpixel((result.image.width // 2, result.image.height - 1))
        self.assertGreater(pixel[2], 180)
        self.assertLess(pixel[0], 20)

    def test_extreme_aspect_photo_does_not_expand_detector_input_without_bound(self):
        class Engine:
            def read(self, image):
                h, w = image.shape[:2]
                self.assert_shape(h, w)
                return [], 0
        engine = Engine()
        engine.assert_shape = lambda h, w: (
            self.assertLessEqual(max(h, w), 1200),
            self.assertLessEqual(max(h, w) / min(h, w), 4))
        with patch.object(pipeline, "detect_card", return_value=None):
            result = pipeline.read_card(Image.new("RGB", (4, 1600), "gray"), engine)
        self.assertEqual(result.query_text, "")
        self.assertLessEqual(len(result.metadata["candidates"]), 10)


if __name__ == "__main__":
    unittest.main()
