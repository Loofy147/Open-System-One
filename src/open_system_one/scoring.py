from __future__ import annotations

from math import isfinite, sqrt
from typing import Sequence


Vector = Sequence[float]


def cosine(a: Vector, b: Vector) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have equal dimensions")

    dot = sum(x * y for x, y in zip(a, b))
    aa = sum(x * x for x in a)
    bb = sum(y * y for y in b)
    denominator = sqrt(aa * bb)
    if denominator == 0.0:
        return 0.0
    value = dot / denominator
    if not isfinite(value):
        raise ValueError("Cosine score is not finite")
    return value


def pairwise_scores(query: Vector, candidates: Sequence[Vector]) -> list[float]:
    if not candidates:
        raise ValueError("At least one candidate is required")
    return [cosine(query, candidate) for candidate in candidates]


def set_aware_scores(
    query: Vector,
    candidates: Sequence[Vector],
    *,
    interaction_weight: float = 0.35,
) -> list[float]:
    if not candidates:
        raise ValueError("At least one candidate is required")

    dimension = len(candidates[0])
    if any(len(candidate) != dimension for candidate in candidates):
        raise ValueError("Candidate dimensions must match")

    mean = [
        sum(candidate[d] for candidate in candidates) / len(candidates)
        for d in range(dimension)
    ]
    return [
        cosine(query, candidate) + interaction_weight * cosine(candidate, mean)
        for candidate in candidates
    ]


def conditional_mixture_scores(
    query: Vector,
    candidates: Sequence[Vector],
    *,
    pairwise_weight: float = 0.75,
) -> list[float]:
    if not 0.0 <= pairwise_weight <= 1.0:
        raise ValueError("pairwise_weight must be in [0, 1]")
    if not candidates:
        raise ValueError("At least one candidate is required")

    set_weight = 1.0 - pairwise_weight
    dimension = len(candidates[0])
    mean = [
        sum(candidate[d] for candidate in candidates) / len(candidates)
        for d in range(dimension)
    ]
    return [
        pairwise_weight * cosine(query, candidate)
        + set_weight * cosine(candidate, mean)
        for candidate in candidates
    ]
