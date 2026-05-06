# Architecture

Our system is a deterministic, real-time optimizer for creator content posting. It loads the provided content stream, creator base engagement, platform activity, and historical engagement data into indexed dictionaries for fast lookup. For every content item, the engine evaluates all 48 possible platform-time choices: Instagram and YouTube across 24 hours.

Each candidate is scored using the evaluation-aligned formula:

```text
expected_engagement = creator_base * platform_activity * historical_engagement
score = 0.50 * normalized(expected_engagement)
      + 0.20 * platform_activity
      + 0.15 * platform_quality
```

Platform quality is a soft signal: SHORT content is biased toward Instagram and LONG content toward YouTube, but creator-specific history and timing can override that preference when the data supports a better result. This creates the required trade-off between platform fit and peak timing.

The selected recommendation is the highest-scoring platform-time pair. If the chosen time equals the submission hour, the decision is `POST_NOW`; otherwise it is `SCHEDULE`. New submissions are stored in memory so `/submit_content` and `/get_recommendation` stay consistent.

The backend exposes required APIs, batch recommendations, analytics, explanations, and a presentation dashboard. No external APIs or ML inference are used, keeping the system reproducible, explainable, and efficient for burst submissions.
