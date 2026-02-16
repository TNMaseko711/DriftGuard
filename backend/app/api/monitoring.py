from __future__ import annotations

import numpy as np
from fastapi import APIRouter

from backend.app.models.schemas import DriftRequest
from backend.app.services.monitoring_service import monitoring_service

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.post("/drift")
def calculate_drift(payload: DriftRequest):
    reference = np.array(payload.reference, dtype=float)
    current = np.array(payload.current, dtype=float)

    psi = monitoring_service.calculate_psi(reference, current, bins=payload.bins)
    ks_drift, ks_stat, p_value = monitoring_service.ks_test(reference, current)

    return {
        "feature_name": payload.feature_name,
        "psi": psi,
        "psi_status": "high" if psi >= 0.2 else "warning" if psi >= 0.1 else "ok",
        "ks": {
            "drift_detected": ks_drift,
            "statistic": ks_stat,
            "p_value": p_value,
        },
    }
