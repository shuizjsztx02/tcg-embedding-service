"""Geometry regressions; no model downloads or production service required."""
import unittest
from unittest.mock import patch

import cv2
import numpy as np
from PIL import Image, ImageDraw

import dino_preprocess
from dino_preprocess import (_quad_score, assess_quality, detect_card, enhance_card,
                             order_points, perspective_correct, prepare_candidates)


class CardGeometryTests(unittest.TestCase):
    def test_detector_prefers_complete_outer_border_over_nearby_inner_separator(self):
        """A strong title separator must not crop away the card's top border."""
        support = np.zeros((400, 300), np.uint8)
        outer = np.array([[21, 17], [283, 18], [248, 394], [8, 360]], np.float32)
        inner = np.array([[21, 31], [282, 30], [249, 391], [8, 363]], np.float32)
        for quad in (outer, inner):
            cv2.polylines(support, [quad.astype(np.int32)], True, 255, 5)
        self.assertGreater(_quad_score(inner, support), _quad_score(outer, support))
        fixture = np.zeros_like(support)
        for quad in (outer, inner):
            cv2.polylines(fixture, [quad.astype(np.int32)], True, 255, 1)
        image = Image.fromarray(np.repeat(fixture[:, :, None], 3, axis=2))
        with patch.object(dino_preprocess.cv2, "findContours", return_value=([], None)), \
                patch.object(dino_preprocess, "_line_quads", return_value=iter((inner, outer))):
            selected = detect_card(image)
        self.assertLess(float(selected[:2, 1].mean()), 20)

    def test_retained_candidates_do_not_multiply_full_resolution_memory(self):
        candidates, _ = prepare_candidates(Image.new("RGB", (4000, 3000), "white"))
        self.assertLess(sum(im.width * im.height for im, _ in candidates), 1000000)

    def test_all_four_original_orientations_survive_failed_detection(self):
        img = Image.new("RGB", (300, 200), "black")
        before = np.asarray(img).copy()
        candidates, meta = prepare_candidates(img)
        originals = [im for im, source in candidates if source["source"] == "original"]
        self.assertEqual(len(originals), 4)
        self.assertFalse(meta["quad_found"])
        self.assertTrue(meta["warnings"])
        self.assertEqual({source["rotation_degrees"] for _, source in candidates
                          if source["source"] == "original"}, {0, 90, 180, 270})
        np.testing.assert_array_equal(np.asarray(img), before)

    def test_exif_applied_before_original_candidate_is_scored(self):
        img = Image.new("RGB", (300, 200), "black")
        ImageDraw.Draw(img).rectangle((0, 0, 99, 199), fill="red")
        img.getexif()[274] = 6
        candidates, _ = prepare_candidates(img)
        original = next(im for im, source in candidates if source == {"source": "original", "rotation_degrees": 0})
        red = np.asarray(original)[:, :, 0] > 200
        self.assertGreater(red[:60].mean(), .95)
        self.assertLess(red[-60:].mean(), .05)
        self.assertEqual(img.getexif()[274], 6)

    def test_detection_coordinates_map_back_to_large_photo(self):
        img = Image.new("RGB", (1500, 1800), (50, 50, 50))
        ImageDraw.Draw(img).rectangle((300, 270, 1140, 1440), fill="white")
        quad = detect_card(img)
        self.assertIsNotNone(quad)
        self.assertLess(np.linalg.norm(quad.mean(axis=0) - [720, 855]), 20)
        self.assertGreater(cv2.contourArea(quad), 900000)

    def test_quality_warns_for_clipped_and_detail_free_image(self):
        quality, warnings = assess_quality(Image.new("RGB", (400, 600), "white"))
        self.assertEqual(quality["highlight_ratio"], 1)
        self.assertEqual(quality["blur_var"], 0)
        self.assertGreaterEqual(len(warnings), 2)

    def test_enhancement_handles_saturated_image_without_numeric_warning(self):
        img = Image.new("RGB", (200, 280), "white")
        quality, _ = assess_quality(img)
        with np.errstate(all="raise"):
            out = enhance_card(img, quality)
        self.assertEqual(out.size, img.size)
        self.assertEqual(out.mode, "RGB")

    def test_low_contrast_card_boundary(self):
        img = Image.new("RGB", (500, 600), (100, 100, 100))
        ImageDraw.Draw(img).polygon([(100, 90), (380, 110), (350, 490), (80, 470)], fill=(112, 112, 112))
        self.assertIsNotNone(detect_card(img))

    def test_broken_borders_can_form_card_without_a_closed_contour(self):
        img = Image.new("RGB", (500, 600), (100, 100, 100))
        draw = ImageDraw.Draw(img)
        for edge in [(120, 100, 360, 100), (380, 120, 380, 460),
                     (360, 480, 120, 480), (100, 460, 100, 120)]:
            draw.line(edge, fill="white", width=3)
        quad = detect_card(img)
        self.assertIsNotNone(quad)
        self.assertGreater(cv2.contourArea(quad), 95000)
        self.assertLess(cv2.contourArea(quad), 120000)

    def test_blank_frame_is_not_a_card(self):
        self.assertIsNone(detect_card(Image.new("RGB", (300, 400), "white")))

    def test_diamond_corners_remain_distinct(self):
        quad = order_points(np.array([[100, 0], [200, 100], [100, 200], [0, 100]], np.float32))
        self.assertEqual(len(np.unique(quad, axis=0)), 4)
        self.assertAlmostEqual(cv2.contourArea(quad), 20000)

    def test_nested_card_not_outer_background(self):
        img = Image.new("RGB", (500, 600), "white")
        draw = ImageDraw.Draw(img)
        draw.rectangle((100, 90, 380, 480), fill=(40, 60, 80), outline="black", width=4)
        quad = detect_card(img)
        self.assertIsNotNone(quad)
        self.assertLess(np.linalg.norm(quad.mean(axis=0) - [240, 285]), 15)
        self.assertGreater(cv2.contourArea(quad), 95000)
        self.assertLess(cv2.contourArea(quad), 125000)

    def test_sideways_card_is_rotated_before_portrait_warp(self):
        img = Image.new("RGB", (280, 200), "blue")
        ImageDraw.Draw(img).rectangle((0, 0, 90, 199), fill="red")
        quad = np.array([[0, 0], [279, 0], [279, 199], [0, 199]], np.float32)
        out = np.asarray(perspective_correct(img, quad, output_size=(200, 280), trim=0))
        red = out[:, :, 0] > 200
        # A left-edge band on a sideways card becomes a top/bottom band,
        # never a left-edge band stretched into a portrait image.
        self.assertGreater(max(red[:95].mean(), red[-95:].mean()), .9)
        self.assertLess(red[:, :65].mean(), .5)


if __name__ == "__main__":
    unittest.main()
