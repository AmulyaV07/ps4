from dataclasses import dataclass


PLATFORMS = ("Instagram", "YouTube")
CONTENT_TYPES = ("SHORT", "LONG")
DECISIONS = ("POST_NOW", "SCHEDULE")


@dataclass(frozen=True)
class ContentItem:
    content_id: int
    creator_id: int
    content_type: str
    created_timestamp: int
    time_sensitivity: str = "Medium"


@dataclass(frozen=True)
class Recommendation:
    content_id: int
    platform: str
    time_slot: int
    decision: str
    expected_engagement: float
    activity_score: float
    historical_engagement: float
    platform_quality: float
    score: float
    rank: int = 1

    def submission_row(self) -> dict[str, int | str]:
        return {
            "content_id": self.content_id,
            "platform": self.platform,
            "time_slot": self.time_slot,
            "decision": self.decision,
        }
