import csv
import tempfile
import unittest
from pathlib import Path

from optimizer.data import Dataset
from optimizer.engine import RecommendationEngine
from optimizer.evaluate import evaluate_submission
from optimizer.output import write_submission


class OptimizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset = Dataset("data/raw")
        cls.engine = RecommendationEngine(cls.dataset)

    def test_recommendations_are_deterministic(self) -> None:
        first = [rec.submission_row() for rec in self.engine.recommend_all()]
        second = [rec.submission_row() for rec in self.engine.recommend_all()]
        self.assertEqual(first, second)

    def test_output_has_required_fields_and_valid_values(self) -> None:
        recommendations = self.engine.recommend_all()
        self.assertEqual(len(recommendations), len(self.dataset.content))
        for rec in recommendations:
            self.assertIn(rec.platform, {"Instagram", "YouTube"})
            self.assertIn(rec.decision, {"POST_NOW", "SCHEDULE"})
            self.assertGreaterEqual(rec.time_slot, 0)
            self.assertLessEqual(rec.time_slot, 23)

    def test_score_is_competitive_on_visible_dataset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "submission.csv"
            write_submission(self.engine.recommend_all(), path)
            score = evaluate_submission(path, "data/raw")
        self.assertGreater(score["final_score"], 0.80)
        self.assertGreater(score["timing_score"], 0.95)
        self.assertGreater(score["platform_score"], 0.98)

    def test_submission_csv_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "submission.csv"
            write_submission(self.engine.recommend_all(), path)
            with path.open("r", newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(
                    reader.fieldnames,
                    ["content_id", "platform", "time_slot", "decision"],
                )
                self.assertEqual(len(list(reader)), len(self.dataset.content))

    def test_ranked_candidates_are_explainable_and_sorted(self) -> None:
        item = self.dataset.content[0]
        ranked = self.engine.rank_candidates(item, limit=5)
        self.assertEqual([rec.rank for rec in ranked], [1, 2, 3, 4, 5])
        self.assertEqual(ranked[0].submission_row(), self.engine.recommend(item).submission_row())
        scores = [rec.score for rec in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
