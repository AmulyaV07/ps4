import argparse
import json

from optimizer.data import Dataset
from optimizer.engine import RecommendationEngine
from optimizer.evaluate import evaluate_submission
from optimizer.output import write_explanations, write_submission


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Creator content posting optimizer")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--submission", default="submission.csv")
    parser.add_argument("--explain", default="reports/recommendation_explanations.csv")
    parser.add_argument("--score", action="store_true", help="Evaluate the generated submission")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    dataset = Dataset(args.data_dir)
    engine = RecommendationEngine(dataset)
    recommendations = engine.recommend_all()
    write_submission(recommendations, args.submission)
    write_explanations(recommendations, args.explain)

    print(f"Wrote {len(recommendations)} recommendations to {args.submission}")
    print(f"Wrote explanation report to {args.explain}")

    if args.score:
        print(json.dumps(evaluate_submission(args.submission, args.data_dir), indent=2))


if __name__ == "__main__":
    main()
