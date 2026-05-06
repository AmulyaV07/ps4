# Creator Content Posting Optimization System

## Team Information
- **Team Name**: D.A.D.
- **Year**: Second
- **All-Female Team**: No

## Architecture Overview

Our system is a deterministic real-time optimizer that jointly chooses the best platform and posting hour. For each content item, it evaluates all 48 possible decisions: Instagram and YouTube across 24 time slots. Every candidate is scored using the evaluation objective: creator base engagement x platform activity x creator-specific historical engagement, with additional weight for timing quality and soft platform-content fit.

SHORT content is biased toward Instagram and LONG content toward YouTube, but this is not a hard rule. If a creator's history or a platform's peak activity shows a better opportunity elsewhere, the optimizer can switch. This handles conflicting platform and timing signals while staying explainable.

All CSV data is loaded once into dictionary indexes, so recommendations are fast enough for burst submissions. Missing history or creator values fall back to global and platform/content/time averages. The decision is simple: if the best slot is the submission hour, return POST_NOW; otherwise return SCHEDULE. Fixed tie-breaking makes outputs reproducible. The backend also supports submit, retrieve, batch, analytics, and explanation APIs.

---

*Keep your description concise and focused on your core decision-making logic.*

**Note:** Please do not change the format or spelling of anything in this README. The fields are extracted using a script, so any changes to the structure or formatting may break the extraction process.
