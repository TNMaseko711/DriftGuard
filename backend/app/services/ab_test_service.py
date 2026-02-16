from __future__ import annotations

import hashlib
from uuid import UUID

from backend.app.models.schemas import ABTestCreate, ABTestRecord
from backend.app.services.store import store


class ABTestService:
    def create_test(self, payload: ABTestCreate) -> ABTestRecord:
        total = sum(v.traffic_percentage for v in payload.variants)
        if total != 100:
            raise ValueError("variant traffic percentages must sum to 100")
        record = ABTestRecord(**payload.model_dump())
        store.ab_tests[str(record.id)] = record
        return record

    def list_tests(self) -> list[ABTestRecord]:
        return list(store.ab_tests.values())

    def assign_variant(self, test_id: UUID, user_id: str) -> str:
        test = store.ab_tests.get(str(test_id))
        if not test:
            raise KeyError("test not found")
        hash_value = int(hashlib.md5(user_id.encode("utf-8")).hexdigest(), 16)
        percentage = hash_value % 100

        cumulative = 0
        for variant in test.variants:
            cumulative += variant.traffic_percentage
            if percentage < cumulative:
                return variant.variant_id
        return test.variants[0].variant_id


ab_test_service = ABTestService()
