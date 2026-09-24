import pytest
from open_system_one.policy import DecisionDisposition, PolicyThresholds, apply_policy

def test_policy_thresholds_are_explicit_and_external():
    t = PolicyThresholds(accept_min_confidence=0.9, review_min_confidence=0.6)
    assert apply_policy(0.95, thresholds=t) is DecisionDisposition.ACCEPT
    assert apply_policy(0.75, thresholds=t) is DecisionDisposition.REVIEW
    assert apply_policy(0.20, thresholds=t) is DecisionDisposition.ABSTAIN

def test_invalid_policy_order_is_rejected():
    with pytest.raises(ValueError):
        apply_policy(
            0.7,
            thresholds=PolicyThresholds(
                accept_min_confidence=0.5,
                review_min_confidence=0.8,
            ),
        )
