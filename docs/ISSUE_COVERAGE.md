# Issue Coverage

This project covers the 20 issue requirements from `ISSUES.md`.

| Issue | Coverage |
| --- | --- |
| 1 | `optimizer/data.py` loads and validates content submissions. |
| 2 | `optimizer/data.py` indexes platform activity by `(platform, time_slot)`. |
| 3 | `optimizer/data.py` indexes historical engagement by `(creator, platform, content_type, time_slot)`. |
| 4 | `optimizer/data.py` loads creator base engagement and global fallbacks. |
| 5 | `optimizer/engine.py` implements the weighted evaluator-aligned scoring function. |
| 6 | `optimizer/engine.py` selects between Instagram and YouTube using joint score. |
| 7 | `optimizer/engine.py` evaluates all 24 posting hours. |
| 8 | `optimizer/engine.py` jointly searches all 48 platform-time candidates. |
| 9 | `optimizer/engine.py` returns `POST_NOW` only when the best slot is the submission hour. |
| 10 | Creator-specific history and base engagement are first-class scoring inputs. |
| 11 | Tie-breaking is deterministic and tests verify repeated runs match. |
| 12 | `optimizer/output.py` writes `content_id,platform,time_slot,decision`. |
| 13 | Preloaded dictionaries make burst processing constant time per content item. |
| 14 | Only 48 candidates are scored per item; no external APIs or slow model calls. |
| 15 | Missing values fall back to global and platform/content/time averages. |
| 16 | CSV loaders validate enum values and time-slot ranges. |
| 17 | Scores clamp negative/missing values and avoid invalid math. |
| 18 | `optimizer/evaluate.py` reproduces the PDF scoring script. |
| 19 | `docs/ARCHITECTURE.md` documents design and tradeoffs. |
| 20 | `tests/test_optimizer.py` and `validate_project.py` provide validation. |
