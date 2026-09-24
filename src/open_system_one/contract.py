from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Literal, Mapping, Sequence


QuestionType = Literal["choice", "score", "noul"]


@dataclass(frozen=True)
class ChoiceQuestion:
    id: str
    instructions: str
    options: tuple[str, ...]
    criteria: tuple[str, ...] = ()

    @property
    def type(self) -> QuestionType:
        return "choice"


@dataclass(frozen=True)
class ScoreQuestion:
    id: str
    instructions: str
    levels: tuple[str, ...]
    criteria: tuple[str, ...] = ()

    @property
    def type(self) -> QuestionType:
        return "score"


@dataclass(frozen=True)
class NoulQuestion:
    id: str
    instructions: str
    true_label: str = "true"
    false_label: str = "false"
    criteria: tuple[str, ...] = ()

    @property
    def type(self) -> QuestionType:
        return "noul"

    @property
    def options(self) -> tuple[str, str]:
        return (self.true_label, self.false_label)


Question = ChoiceQuestion | ScoreQuestion | NoulQuestion


@dataclass(frozen=True)
class DecisionRequest:
    state: Any
    questions: tuple[Question, ...]


@dataclass(frozen=True)
class QuestionDistribution:
    question_id: str
    probabilities: Mapping[str, float]
    selected: str


@dataclass(frozen=True)
class DecisionResult:
    answers: Mapping[str, QuestionDistribution]


def question_options(question: Question) -> tuple[str, ...]:
    if isinstance(question, ChoiceQuestion):
        return question.options
    if isinstance(question, ScoreQuestion):
        return question.levels
    return question.options


def validate_request(request: DecisionRequest) -> None:
    if not request.questions:
        raise ValueError("DecisionRequest requires at least one question")

    seen: set[str] = set()
    for question in request.questions:
        if not question.id:
            raise ValueError("Question id must be non-empty")
        if question.id in seen:
            raise ValueError(f"Duplicate question id: {question.id}")
        seen.add(question.id)

        options = question_options(question)
        if len(options) < 2:
            raise ValueError(f"Question {question.id} needs at least two outcomes")
        if any(not option for option in options):
            raise ValueError(f"Question {question.id} contains an empty outcome")
        if len(set(options)) != len(options):
            raise ValueError(f"Question {question.id} contains duplicate outcomes")


def validate_distribution(
    question: Question,
    probabilities: Mapping[str, float],
    selected: str,
    *,
    tolerance: float = 1e-9,
) -> None:
    options = question_options(question)
    if set(probabilities) != set(options):
        raise ValueError(f"Distribution keys do not match outcomes for {question.id}")
    if selected not in options:
        raise ValueError(f"Selected outcome is not valid for {question.id}")

    values = list(probabilities.values())
    if any(not isfinite(value) or value < 0.0 for value in values):
        raise ValueError(f"Distribution contains non-finite or negative values for {question.id}")

    total = sum(values)
    if abs(total - 1.0) > tolerance:
        raise ValueError(f"Distribution must sum to 1 for {question.id}; got {total}")


def distribution_from_scores(
    question: Question,
    scores: Sequence[float],
) -> QuestionDistribution:
    options = question_options(question)
    if len(scores) != len(options):
        raise ValueError("Score vector length does not match outcome space")
    if any(not isfinite(value) for value in scores):
        raise ValueError("Scores must be finite")

    maximum = max(scores)
    import math

    exponentials = [math.exp(value - maximum) for value in scores]
    total = sum(exponentials)
    probabilities = {
        option: value / total for option, value in zip(options, exponentials)
    }
    selected = options[max(range(len(scores)), key=scores.__getitem__)]
    result = QuestionDistribution(
        question_id=question.id,
        probabilities=probabilities,
        selected=selected,
    )
    validate_distribution(question, result.probabilities, result.selected)
    return result
