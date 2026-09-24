from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DecisionDisposition(str, Enum):
    ACCEPT = "accept"
    REVIEW = "review"
    ABSTAIN = "abstain"


@dataclass(frozen=True)
class PolicyThresholds:
    """Caller-supplied policy parameters; no threshold is canonical here."""

    accept_min_confidence: float
    review_min_confidence: float


def apply_policy(
    confidence: float,
    *,
    thresholds: PolicyThresholds,
) -> DecisionDisposition:
    if not (
        0.0 <= thresholds.review_min_confidence
        <= thresholds.accept_min_confidence
        <= 1.0
    ):
        raise ValueError("Policy thresholds are invalid")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence must be in [0, 1]")

    if confidence >= thresholds.accept_min_confidence:
        return DecisionDisposition.ACCEPT
    if confidence >= thresholds.review_min_confidence:
        return DecisionDisposition.REVIEW
    return DecisionDisposition.ABSTAIN
