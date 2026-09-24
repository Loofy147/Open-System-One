import math

import pytest

from open_system_one.contract import (
    ChoiceQuestion,
    DecisionRequest,
    NoulQuestion,
    ScoreQuestion,
    distribution_from_scores,
    validate_distribution,
    validate_request,
)
from open_system_one.policy import (
    DecisionDisposition,
    PolicyThresholds,
    apply_policy,
)


def test_typed_questions_have_finite_outcome_spaces():
    request = DecisionRequest(
        state={"opaque": True},
        questions=(
            ChoiceQuestion("route", "Choose a route", ("a", "b")),
            ScoreQuestion("risk", "Rate risk", ("low", "medium", "high")),
            NoulQuestion("valid", "Is it valid?"),
        ),
    )
    validate_request(request)


def test_duplicate_question_ids_are_rejected():
    request = DecisionRequest(
        state=None,
        questions=(
            ChoiceQuestion("q", "x", ("a", "b")),
            NoulQuestion("q", "y"),
        ),
    )
    with pytest.raises(ValueError):
        validate_request(request)


def test_non_finite_scores_are_rejected():
    question = ChoiceQuestion("q", "x", ("a", "b"))
    with pytest.raises(ValueError):
        distribution_from_scores(question, [0.0, math.nan])


def test_distribution_must_close_to_one():
    question = ChoiceQuestion("q", "x", ("a", "b"))
    with pytest.raises(ValueError):
        validate_distribution(question, {"a": 0.4, "b": 0.4}, "a")


def test_score_order_is_semantic():
    question = ScoreQuestion("risk", "Rate risk", ("low", "medium", "high"))
    result = distribution_from_scores(question, [0.1, 0.2, 0.7])
    assert result.selected == "high"


def test_policy_uses_explicit_caller_thresholds():
    thresholds = PolicyThresholds(
        accept_min_confidence=0.9,
        review_min_confidence=0.6,
    )
    assert apply_policy(0.95, thresholds=thresholds) is DecisionDisposition.ACCEPT
    assert apply_policy(0.75, thresholds=thresholds) is DecisionDisposition.REVIEW
    assert apply_policy(0.20, thresholds=thresholds) is DecisionDisposition.ABSTAIN


def test_invalid_policy_thresholds_fail():
    with pytest.raises(ValueError):
        apply_policy(
            0.7,
            thresholds=PolicyThresholds(
                accept_min_confidence=0.5,
                review_min_confidence=0.8,
            ),
        )
