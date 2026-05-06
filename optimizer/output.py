import csv
from pathlib import Path

from .models import Recommendation


def write_submission(recommendations: list[Recommendation], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["content_id", "platform", "time_slot", "decision"],
        )
        writer.writeheader()
        for recommendation in recommendations:
            writer.writerow(recommendation.submission_row())


def write_explanations(recommendations: list[Recommendation], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "content_id",
                "platform",
                "time_slot",
                "decision",
                "expected_engagement",
                "activity_score",
                "historical_engagement",
                "platform_quality",
                "optimizer_score",
                "rank",
            ],
        )
        writer.writeheader()
        for rec in recommendations:
            writer.writerow(
                {
                    "content_id": rec.content_id,
                    "platform": rec.platform,
                    "time_slot": rec.time_slot,
                    "decision": rec.decision,
                    "expected_engagement": f"{rec.expected_engagement:.6f}",
                    "activity_score": f"{rec.activity_score:.3f}",
                    "historical_engagement": f"{rec.historical_engagement:.3f}",
                    "platform_quality": f"{rec.platform_quality:.2f}",
                    "optimizer_score": f"{rec.score:.6f}",
                    "rank": rec.rank,
                }
            )
