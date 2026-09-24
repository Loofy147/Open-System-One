from __future__ import annotations

from typing import Protocol

from .contract import DecisionRequest, DecisionResult


class DecisionBackend(Protocol):
    """Replaceable backend contract for batched typed decisions."""

    def evaluate(self, request: DecisionRequest) -> DecisionResult:
        ...
