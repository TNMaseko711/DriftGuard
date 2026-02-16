# User Guide

## Typical workflow

1. Register a model with metadata.
2. Create version records with metrics and artifacts URI.
3. Track experiments and runs while logging metrics over steps.
4. Create deployments with rollout strategy metadata.
5. Configure A/B test variants with weighted traffic split.
6. Submit reference/current feature windows to drift endpoint.

## Example curl snippets

```bash
curl -X POST http://localhost:8000/api/models \
  -H 'Content-Type: application/json' \
  -d '{"name":"customer_churn","framework":"xgboost","task_type":"classification","created_by":"alice"}'
```

```bash
curl -X POST http://localhost:8000/api/monitoring/drift \
  -H 'Content-Type: application/json' \
  -d '{"feature_name":"income","reference":[1,2,3],"current":[2,3,4]}'
```
