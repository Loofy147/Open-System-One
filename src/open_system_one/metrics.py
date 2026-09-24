from __future__ import annotations

from collections.abc import Sequence
from math import isfinite


def multiclass_brier(probabilities: Sequence[float], target_index: int) -> float:
    if not probabilities:
        raise ValueError("probabilities cannot be empty")
    if not 0 <= target_index < len(probabilities):
        raise ValueError("target_index is out of range")
    if any(not isfinite(value) for value in probabilities):
        raise ValueError("probabilities must be finite")
    total = sum(probabilities)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("probabilities must sum to 1")
    return sum(
        (value - (1.0 if index == target_index else 0.0)) ** 2
        for index, value in enumerate(probabilities)
    )


def uniform_brier_baseline(outcome_count: int) -> float:
    if outcome_count < 2:
        raise ValueError("outcome_count must be at least 2")
    return 1.0 - 1.0 / outcome_count


def brier_skill(probabilities: Sequence[float], target_index: int) -> float:
    baseline = uniform_brier_baseline(len(probabilities))
    return 1.0 - multiclass_brier(probabilities, target_index) / baseline
