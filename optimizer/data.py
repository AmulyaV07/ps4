import csv
from pathlib import Path

from .models import CONTENT_TYPES, PLATFORMS, ContentItem


class Dataset:
    def __init__(self, data_dir: str | Path = "data/raw") -> None:
        self.data_dir = Path(data_dir)
        self.content = self._load_content()
        self.creators = self._load_creators()
        self.activity = self._load_activity()
        self.history = self._load_history()

        self.global_base = _mean(self.creators.values(), 1.0)
        self.global_activity = _mean(self.activity.values(), 0.6)
        self.global_history = _mean(self.history.values(), 0.6)
        self.history_by_platform_type = self._build_history_fallbacks()

    def _open(self, name: str):
        return (self.data_dir / name).open("r", newline="", encoding="utf-8-sig")

    def _load_content(self) -> list[ContentItem]:
        items: list[ContentItem] = []
        with self._open("content.csv") as handle:
            for row in csv.DictReader(handle):
                try:
                    content_type = row["content_type"].strip().upper()
                    created = int(row["created_timestamp"])
                    if content_type not in CONTENT_TYPES or not 0 <= created <= 23:
                        continue
                    items.append(
                        ContentItem(
                            content_id=int(row["content_id"]),
                            creator_id=int(row["creator_id"]),
                            content_type=content_type,
                            created_timestamp=created,
                            time_sensitivity=row.get("time_sensitivity", "Medium") or "Medium",
                        )
                    )
                except (KeyError, TypeError, ValueError):
                    continue
        return items

    def _load_creators(self) -> dict[int, float]:
        creators: dict[int, float] = {}
        with self._open("creators.csv") as handle:
            for row in csv.DictReader(handle):
                try:
                    creators[int(row["creator_id"])] = max(0.0, float(row["base_engagement"]))
                except (KeyError, TypeError, ValueError):
                    continue
        return creators

    def _load_activity(self) -> dict[tuple[str, int], float]:
        activity: dict[tuple[str, int], float] = {}
        with self._open("platform_activity.csv") as handle:
            for row in csv.DictReader(handle):
                try:
                    platform = row["platform"].strip()
                    slot = int(row["time_slot"])
                    if platform in PLATFORMS and 0 <= slot <= 23:
                        activity[(platform, slot)] = max(0.0, float(row["activity_score"]))
                except (KeyError, TypeError, ValueError):
                    continue
        return activity

    def _load_history(self) -> dict[tuple[int, str, str, int], float]:
        history: dict[tuple[int, str, str, int], float] = {}
        with self._open("historical_engagement.csv") as handle:
            for row in csv.DictReader(handle):
                try:
                    creator_id = int(row["creator_id"])
                    platform = row["platform"].strip()
                    content_type = row["content_type"].strip().upper()
                    slot = int(row["time_slot"])
                    if platform in PLATFORMS and content_type in CONTENT_TYPES and 0 <= slot <= 23:
                        history[(creator_id, platform, content_type, slot)] = max(
                            0.0, float(row["avg_engagement"])
                        )
                except (KeyError, TypeError, ValueError):
                    continue
        return history

    def _build_history_fallbacks(self) -> dict[tuple[str, str, int], float]:
        buckets: dict[tuple[str, str, int], list[float]] = {}
        for (_creator, platform, content_type, slot), value in self.history.items():
            buckets.setdefault((platform, content_type, slot), []).append(value)
        return {key: _mean(values, self.global_history) for key, values in buckets.items()}


def _mean(values, default: float) -> float:
    values = list(values)
    if not values:
        return default
    return sum(values) / len(values)
