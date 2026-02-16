# API Reference

## Models
- `POST /api/models`
- `GET /api/models`
- `POST /api/models/{model_id}/versions`
- `GET /api/models/{model_id}/versions`
- `PUT /api/models/{model_id}/versions/{version}/stage`

## Experiments
- `POST /api/experiments`
- `GET /api/experiments`
- `POST /api/experiments/runs`
- `PUT /api/experiments/runs/{run_id}/metrics`
- `PUT /api/experiments/runs/{run_id}/complete`

## Deployments
- `POST /api/deployments`
- `GET /api/deployments`
- `PUT /api/deployments/{deployment_id}/status`

## A/B Tests
- `POST /api/ab-tests`
- `GET /api/ab-tests`
- `GET /api/ab-tests/{test_id}/assign?user_id=...`

## Monitoring
- `POST /api/monitoring/drift`

Request body for drift endpoint:

```json
{
  "feature_name": "income",
  "reference": [10, 20, 30],
  "current": [12, 28, 32],
  "bins": 10
}
```
