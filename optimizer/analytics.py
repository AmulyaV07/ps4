from collections import Counter

from .data import Dataset
from .engine import RecommendationEngine
from .evaluate import evaluate_submission
from .models import Recommendation
from .output import write_submission


def build_analytics(
    dataset: Dataset,
    engine: RecommendationEngine,
    submission_path: str = "submission.csv",
) -> dict:
    recommendations = engine.recommend_all()
    write_submission(recommendations, submission_path)
    score = evaluate_submission(submission_path, dataset.data_dir)

    return {
        "count": len(recommendations),
        "score": {key: round(value, 6) for key, value in score.items()},
        "platform_distribution": _counter_map(rec.platform for rec in recommendations),
        "decision_distribution": _counter_map(rec.decision for rec in recommendations),
        "time_slot_distribution": _counter_map(str(rec.time_slot) for rec in recommendations),
        "content_type_distribution": _counter_map(item.content_type for item in dataset.content),
        "average_expected_engagement": round(
            sum(rec.expected_engagement for rec in recommendations) / len(recommendations),
            6,
        ),
        "top_recommendations": [_recommendation_detail(rec) for rec in _top(recommendations, 10)],
    }


def _counter_map(values) -> dict[str, int]:
    return dict(sorted(Counter(values).items(), key=lambda item: item[0]))


def _top(recommendations: list[Recommendation], limit: int) -> list[Recommendation]:
    return sorted(
        recommendations,
        key=lambda rec: (rec.score, rec.expected_engagement, rec.activity_score),
        reverse=True,
    )[:limit]


def _recommendation_detail(rec: Recommendation) -> dict:
    return {
        "content_id": rec.content_id,
        "platform": rec.platform,
        "time_slot": rec.time_slot,
        "decision": rec.decision,
        "expected_engagement": round(rec.expected_engagement, 6),
        "activity_score": rec.activity_score,
        "historical_engagement": rec.historical_engagement,
        "platform_quality": rec.platform_quality,
        "score": round(rec.score, 6),
    }
