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
