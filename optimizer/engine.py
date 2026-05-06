from .data import Dataset
from .models import PLATFORMS, ContentItem, Recommendation


class RecommendationEngine:
    """Deterministic joint optimizer for platform and posting hour."""

    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset
        self._ranked_cache: dict[tuple[int, str], list[Recommendation]] = {}

    def recommend(self, item: ContentItem) -> Recommendation:
        best = self.rank_candidates(item, limit=1)[0]

        if item.created_timestamp == best.time_slot:
            decision = "POST_NOW"
        else:
            decision = "SCHEDULE"

        if best.decision != decision:
            best = Recommendation(
                content_id=best.content_id,
                platform=best.platform,
                time_slot=best.time_slot,
                decision=decision,
                expected_engagement=best.expected_engagement,
                activity_score=best.activity_score,
                historical_engagement=best.historical_engagement,
                platform_quality=best.platform_quality,
                score=best.score,
                rank=best.rank,
            )
        return best

    def recommend_all(self, items: list[ContentItem] | None = None) -> list[Recommendation]:
        return [self.recommend(item) for item in (items or self.dataset.content)]

    def rank_candidates(self, item: ContentItem, limit: int = 5) -> list[Recommendation]:
        key = (item.creator_id, item.content_type)
        ranked = self._ranked_cache.get(key)
        if ranked is None:
            candidates = [
                self._score_candidate(item, platform, slot)
                for platform in PLATFORMS
                for slot in range(24)
            ]
            candidates.sort(key=_sort_key, reverse=True)
            ranked = [
                Recommendation(
                    content_id=item.content_id,
                    platform=rec.platform,
                    time_slot=rec.time_slot,
                    decision=rec.decision,
                    expected_engagement=rec.expected_engagement,
                    activity_score=rec.activity_score,
                    historical_engagement=rec.historical_engagement,
                    platform_quality=rec.platform_quality,
                    score=rec.score,
                    rank=index + 1,
                )
                for index, rec in enumerate(candidates)
            ]
            self._ranked_cache[key] = ranked

        return [
            Recommendation(
                content_id=item.content_id,
                platform=rec.platform,
                time_slot=rec.time_slot,
                decision="POST_NOW" if item.created_timestamp == rec.time_slot else "SCHEDULE",
                expected_engagement=rec.expected_engagement,
                activity_score=rec.activity_score,
                historical_engagement=rec.historical_engagement,
                platform_quality=rec.platform_quality,
                score=rec.score,
                rank=rec.rank,
            )
            for rec in ranked[:limit]
        ]

    def _score_candidate(self, item: ContentItem, platform: str, slot: int) -> Recommendation:
        base = self.dataset.creators.get(item.creator_id, self.dataset.global_base)
        activity = self.dataset.activity.get((platform, slot), self.dataset.global_activity)
        history = self.dataset.history.get(
            (item.creator_id, platform, item.content_type, slot),
            self.dataset.history_by_platform_type.get(
                (platform, item.content_type, slot),
                self.dataset.global_history,
            ),
        )
        expected = base * activity * history
        platform_quality = platform_quality_score(item.content_type, platform)

        # Mirrors the PDF evaluator: engagement dominates, timing and platform
        # quality provide explicit secondary incentives.
        score = 0.50 * min(expected, 1.5) / 1.5
        score += 0.20 * activity
        score += 0.15 * platform_quality

        return Recommendation(
            content_id=item.content_id,
            platform=platform,
            time_slot=slot,
            decision="SCHEDULE",
            expected_engagement=expected,
            activity_score=activity,
            historical_engagement=history,
            platform_quality=platform_quality,
            score=score,
        )


def platform_quality_score(content_type: str, platform: str) -> float:
    if content_type == "SHORT" and platform == "Instagram":
        return 1.0
    if content_type == "LONG" and platform == "YouTube":
        return 1.0
    if content_type == "SHORT" and platform == "YouTube":
        return 0.85
    return 0.70


def _better(candidate: Recommendation, current: Recommendation | None) -> Recommendation:
    if current is None:
        return candidate

    candidate_key = (
        round(candidate.score, 12),
        round(candidate.expected_engagement, 12),
        round(candidate.activity_score, 12),
        round(candidate.platform_quality, 12),
        -candidate.time_slot,
        1 if candidate.platform == "Instagram" else 0,
    )
    current_key = (
        round(current.score, 12),
        round(current.expected_engagement, 12),
        round(current.activity_score, 12),
        round(current.platform_quality, 12),
        -current.time_slot,
        1 if current.platform == "Instagram" else 0,
    )
    return candidate if candidate_key > current_key else current


def _sort_key(rec: Recommendation) -> tuple[float, float, float, float, int, int]:
    return (
        round(rec.score, 12),
        round(rec.expected_engagement, 12),
        round(rec.activity_score, 12),
        round(rec.platform_quality, 12),
        -rec.time_slot,
        1 if rec.platform == "Instagram" else 0,
    )
