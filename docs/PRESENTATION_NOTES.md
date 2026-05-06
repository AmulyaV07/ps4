# Presentation Notes

## One-Line Pitch

Our system is a deterministic, real-time recommendation engine that jointly optimizes platform and posting hour using creator history, platform activity, and content-platform fit.

## What Makes It Strong

- It directly optimizes the hackathon scoring formula instead of using generic rules.
- It checks every Instagram and YouTube hour, so it never misses a better platform-time combination.
- It adapts per creator using historical engagement and base engagement.
- It is fast because all data is pre-indexed and each recommendation checks only 48 candidates.
- It is explainable because every output includes activity, history, platform quality, and final optimizer score in `reports/recommendation_explanations.csv`.

## Demo Flow

1. Run `python validate_project.py`.
2. Show the score breakdown.
3. Open `submission.csv` to show evaluator-ready output.
4. Open `reports/recommendation_explanations.csv` to explain why a recommendation was chosen.
5. Run `python api.py` and open `http://127.0.0.1:8000`.
6. Use the lookup panel or call `/explain?content_id=1` to show the top alternatives.

## Key Technical Point

For each content item:

```text
score = 0.50 * normalized(base * activity * historical)
      + 0.20 * activity
      + 0.15 * platform_quality
```

This balances engagement, peak timing, and platform fit exactly like the evaluation criteria.
