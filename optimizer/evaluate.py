import csv
import time
from pathlib import Path

from .data import Dataset
from .engine import platform_quality_score


def evaluate_submission(submission_path: str | Path, data_dir: str | Path = "data/raw") -> dict[str, float]:
    started = time.perf_counter()
    dataset = Dataset(data_dir)
    content_by_id = {item.content_id: item for item in dataset.content}

    engagement_total = 0.0
    timing_total = 0.0
    platform_total = 0.0
    count = 0

    with Path(submission_path).open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            item = content_by_id[int(row["content_id"])]
            platform = row["platform"]
            slot = int(row["time_slot"])
            activity = dataset.activity[(platform, slot)]
            history = dataset.history[(item.creator_id, platform, item.content_type, slot)]
            base = dataset.creators[item.creator_id]
            engagement_total += base * activity * history
            timing_total += activity
            platform_total += platform_quality_score(item.content_type, platform)
            count += 1

    latency = time.perf_counter() - started
    engagement_score = min(engagement_total / count, 1.5) / 1.5
    timing_score = timing_total / count
    platform_score = platform_total / count
    efficiency_score = max(0.0, 1.0 - latency)
    final_score = (
        0.50 * engagement_score
        + 0.20 * timing_score
        + 0.15 * platform_score
        + 0.15 * efficiency_score
    )
    return {
        "engagement_score": engagement_score,
        "timing_score": timing_score,
        "platform_score": platform_score,
        "efficiency_score": efficiency_score,
        "final_score": final_score,
        "latency_seconds": latency,
    }
