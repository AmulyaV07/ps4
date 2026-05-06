# Creator Content Posting Optimization System

## Team Information
- **Team Name**: [Team Name]
- **Year**: [Year]
- **All-Female Team**: [Yes/No]

## Architecture Overview

The system uses a deterministic joint optimizer. For every content item, it evaluates all Instagram and YouTube posting hours and selects the platform-time pair with the highest weighted score. The score mirrors the evaluation objective: creator base engagement multiplied by platform activity and creator-specific historical engagement, with secondary weights for timing quality and soft platform-content fit. SHORT content receives a light Instagram preference and LONG content receives a light YouTube preference, but the final choice can still switch platforms when historical creator performance and activity signals are stronger.

All datasets are loaded once into dictionary indexes, so each recommendation checks only 48 candidates and remains fast during burst submissions. Missing creator or history values fall back to global and platform/content/time averages, ensuring every valid content item receives an output. The scheduling decision is explainable: if the best-scoring slot is the submission hour, the system returns POST_NOW; otherwise it schedules the content for the optimal future slot. Ties are resolved by fixed rules, making repeated runs identical.

---

*Keep your description concise and focused on your core decision-making logic.*

**Note:** Please do not change the format or spelling of anything in this README. The fields are extracted using a script, so any changes to the structure or formatting may break the extraction process.
