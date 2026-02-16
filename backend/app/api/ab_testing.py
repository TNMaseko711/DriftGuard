from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import ABTestCreate
from backend.app.services.ab_test_service import ab_test_service

router = APIRouter(prefix="/api/ab-tests", tags=["ab-tests"])


@router.post("")
def create_test(payload: ABTestCreate):
    try:
        return ab_test_service.create_test(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("")
def list_tests():
    return ab_test_service.list_tests()


@router.get("/{test_id}/assign")
def assign_variant(test_id: UUID, user_id: str = Query(...)):
    try:
        return {"variant": ab_test_service.assign_variant(test_id, user_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
