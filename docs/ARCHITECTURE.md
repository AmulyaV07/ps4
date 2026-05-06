# Creator Content Posting Optimization System

## Goal

The system recommends the best platform, posting hour, and posting decision for each submitted content item. It is tuned to the evaluation formula in the problem statement while keeping the logic deterministic and easy to explain.

## Core Strategy

For every content item, the engine evaluates all 48 possible choices:

```text
2 platforms x 24 time slots
```

Each candidate receives the same weighted score used by the evaluator:

```text
0.50 * normalized_expected_engagement
+ 0.20 * platform_activity
+ 0.15 * platform_quality
```

Expected engagement is:

```text
creator_base_engagement * activity_score * historical_avg_engagement
```

The highest scoring candidate wins. Ties are resolved deterministically by expected engagement, activity score, platform quality, earlier time slot, then Instagram.

## Scheduling

The engine compares the best future slot with the score available at the submission hour. If the immediate option is close enough, it returns `POST_NOW`; otherwise it returns `SCHEDULE`. High sensitivity content uses a wider immediate-post margin, while low sensitivity content is scheduled whenever a better slot exists.

## Robustness

CSV files are validated while loading. Invalid rows are skipped. If a creator or historical row is missing, the engine falls back to global and platform/content/time averages so every valid content item still receives a recommendation.

## Performance

All CSV data is preloaded into dictionaries. Ranked candidates are cached per `(creator_id, content_type)`, so repeated requests for the same creator profile are served from memory. Recommendation generation is constant time per item because only 48 candidates are evaluated before caching. This supports burst submissions and keeps API latency low.

## Demo Surface

The standard-library API serves a dashboard at `/`, score analytics at `/analytics`, single explanations at `/explain`, and batch recommendations at `/batch_recommendations`. These routes are separate from the evaluator-ready `submission.csv`, so presentation features cannot break the required output format.
