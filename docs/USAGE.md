# Usage

## Generate Submission

```bash
python main.py --score
```

Outputs:

- `submission.csv`: evaluator-ready file with `content_id,platform,time_slot,decision`
- `reports/recommendation_explanations.csv`: explanation report for presentation and debugging

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Run API

```bash
python api.py
```

Open:

```text
http://127.0.0.1:8000
```

Endpoints:

- `GET /health`
- `GET /analytics`
- `GET /get_recommendation?content_id=1`
- `GET /explain?content_id=1`
- `POST /submit_content`
- `POST /batch_recommendations`

Example POST body:

```json
{
  "content_id": 1001,
  "creator_id": 24,
  "content_type": "SHORT",
  "created_timestamp": 18,
  "time_sensitivity": "High"
}
```

Batch POST body:

```json
{
  "items": [
    {
      "content_id": 1001,
      "creator_id": 24,
      "content_type": "SHORT",
      "created_timestamp": 18,
      "time_sensitivity": "High"
    },
    {
      "content_id": 1002,
      "creator_id": 43,
      "content_type": "LONG",
      "created_timestamp": 22,
      "time_sensitivity": "Medium"
    }
  ]
}
```

## Why This Should Score Well

The optimizer directly targets the scoring formula from the problem statement:

```text
engagement = creator_base_engagement * activity_score * historical_avg_engagement
```

It then adds the evaluator's timing and platform-quality incentives before choosing a recommendation. This avoids one-size-fits-all rules and lets creator-specific history override simple assumptions when the data supports it.
