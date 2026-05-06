import json
import subprocess
import sys

from optimizer.data import Dataset
from optimizer.engine import RecommendationEngine
from optimizer.evaluate import evaluate_submission
from optimizer.output import write_explanations, write_submission


def main() -> int:
    dataset = Dataset("data/raw")
    engine = RecommendationEngine(dataset)
    recommendations = engine.recommend_all()

    write_submission(recommendations, "submission.csv")
    write_explanations(recommendations, "reports/recommendation_explanations.csv")
    score = evaluate_submission("submission.csv", "data/raw")

    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        check=False,
    )

    print("\n--- PROJECT VALIDATION ---")
    print(f"Content items processed: {len(recommendations)}")
    print("Score breakdown:")
    print(json.dumps(score, indent=2))
    print("Submission: submission.csv")
    print("Explanations: reports/recommendation_explanations.csv")

    if tests.returncode != 0:
        return tests.returncode
    if score["final_score"] < 0.80:
        print("Final score is below the expected competitive threshold.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
