"""Regression tests for cross-candidate ranking and confidence margins."""
import unittest

import faiss
import numpy as np

from dino_search import rank_candidates


class CandidateRankingTests(unittest.TestCase):
    def setUp(self):
        self.index = faiss.IndexFlatIP(3)
        self.index.add(np.eye(3, dtype=np.float32))

    def test_competing_orientation_is_in_top_two(self):
        features = np.array([[.8, .1, .59], [.1, .79, .604]], dtype=np.float32)
        rows, winner = rank_candidates(features, self.index, ["A", "B", "C"], 3)
        self.assertEqual([r["card_id"] for r in rows], ["A", "B", "C"])
        self.assertAlmostEqual(rows[0]["score"] - rows[1]["score"], .01, places=5)
        self.assertEqual(winner, 0)

    def test_repeated_card_across_candidates_appears_once(self):
        features = np.array([[.8, .1, .59], [.9, .2, .38]], dtype=np.float32)
        rows, winner = rank_candidates(features, self.index, ["A", "B", "C"], 5)
        self.assertEqual(len(rows), 3)
        self.assertEqual(winner, 1)
        self.assertAlmostEqual(rows[0]["score"], .9, places=5)

    def test_empty_index_has_no_fake_last_id(self):
        rows, winner = rank_candidates(np.ones((1, 3), np.float32), faiss.IndexFlatIP(3), [], 5)
        self.assertEqual(rows, [])
        self.assertIsNone(winner)


if __name__ == "__main__":
    unittest.main()
