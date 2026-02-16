from __future__ import annotations

from collections import defaultdict
from typing import Any


class InMemoryStore:
    def __init__(self) -> None:
        self.models: dict[str, Any] = {}
        self.model_versions: defaultdict[str, dict[str, Any]] = defaultdict(dict)
        self.experiments: dict[str, Any] = {}
        self.runs: dict[str, Any] = {}
        self.deployments: dict[str, Any] = {}
        self.ab_tests: dict[str, Any] = {}


store = InMemoryStore()
