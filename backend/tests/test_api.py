from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_model_registry_version_and_promote_flow() -> None:
    model_resp = client.post(
        "/api/models",
        json={
            "name": "customer_churn",
            "description": "binary churn classifier",
            "framework": "xgboost",
            "task_type": "classification",
            "created_by": "alice",
            "tags": ["production"],
        },
    )
    assert model_resp.status_code == 200
    model_id = model_resp.json()["id"]

    version_resp = client.post(
        f"/api/models/{model_id}/versions",
        json={
            "version": "1.0.0",
            "artifact_uri": "s3://models/customer_churn/1.0.0/model.joblib",
            "metrics": {"accuracy": 0.91},
            "parameters": {"max_depth": 5},
            "training_data_hash": "abc123",
            "training_duration_seconds": 120,
            "model_size": 100000,
            "inference_latency_ms": 9.5,
            "notes": "baseline",
        },
    )
    assert version_resp.status_code == 200

    promote_resp = client.put(
        f"/api/models/{model_id}/versions/1.0.0/stage",
        json={"stage": "production", "promoted_by": "ml-engineer"},
    )
    assert promote_resp.status_code == 200
    assert promote_resp.json()["stage"] == "production"


def test_ab_assignment_is_deterministic() -> None:
    model_resp = client.post(
        "/api/models",
        json={
            "name": "ab_model",
            "description": "",
            "framework": "sklearn",
            "task_type": "classification",
            "created_by": "alice",
            "tags": [],
        },
    )
    model_id = model_resp.json()["id"]

    test_resp = client.post(
        "/api/ab-tests",
        json={
            "name": "v1-v2",
            "model_id": model_id,
            "primary_metric": "accuracy",
            "variants": [
                {"variant_id": "control", "model_version": "1.0.0", "traffic_percentage": 50},
                {"variant_id": "treatment", "model_version": "2.0.0", "traffic_percentage": 50},
            ],
        },
    )
    assert test_resp.status_code == 200
    test_id = test_resp.json()["id"]

    r1 = client.get(f"/api/ab-tests/{test_id}/assign", params={"user_id": "user-42"})
    r2 = client.get(f"/api/ab-tests/{test_id}/assign", params={"user_id": "user-42"})
    assert r1.status_code == 200
    assert r1.json()["variant"] == r2.json()["variant"]


def test_monitoring_drift_endpoint() -> None:
    resp = client.post(
        "/api/monitoring/drift",
        json={
            "feature_name": "income",
            "reference": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "current": [25, 24, 23, 22, 21, 20, 19, 18, 17, 16],
            "bins": 5,
        },
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert "psi" in payload
    assert payload["ks"]["statistic"] >= 0
