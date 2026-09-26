from __future__ import annotations
import json
from typing import Any, Protocol
from .probability import confidence, ordinal_expectation, normalize
from .schema import Answer, ChoiceAnswer, ChoiceQuestion, DecisionRequest, DecisionResponse, NoulAnswer, NoulQuestion, ScoreAnswer, ScoreQuestion, Usage

def state_to_text(state: Any) -> str:
    if state is None: return "null"
    if isinstance(state, str): return state
    return json.dumps(state, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

def question_labels(question: Any) -> list[str]:
    if isinstance(question, NoulQuestion): return ["true", "false"]
    if isinstance(question, ChoiceQuestion): return list(question.criteria.keys())
    if isinstance(question, ScoreQuestion): return [str(i) for i in range(len(question.criteria))]
    raise TypeError(type(question).__name__)

class BatchBackend(Protocol):
    name: str
    def evaluate_batch(self, state: Any, questions: dict[str, Any]) -> dict[str, list[float]]: ...

class LegacyQuestionBackend(Protocol):
    name: str
    def evaluate_question(self, state_text: str, question: Any) -> list[float]: ...

class LegacyAdapter:
    def __init__(self, backend: LegacyQuestionBackend):
        self.backend = backend
        self.name = backend.name
    def evaluate_batch(self, state: Any, questions: dict[str, Any]) -> dict[str, list[float]]:
        text = state_to_text(state)
        return {qid: self.backend.evaluate_question(text, q) for qid, q in questions.items()}

class DecisionEngine:
    def __init__(self, backend: BatchBackend):
        self.backend = backend

    def evaluate(self, request: DecisionRequest) -> DecisionResponse:
        raw = self.backend.evaluate_batch(request.state, request.questions)
        if not isinstance(raw, dict) or set(raw) != set(request.questions):
            raise ValueError("backend answers must exactly match question ids")
        answers: dict[str, Answer] = {}
        for qid, question in request.questions.items():
            probs = normalize(raw[qid])
            expected = question_labels(question)
            if len(probs) != len(expected):
                raise ValueError(f"probability count mismatch for {qid}")
            if isinstance(question, NoulQuestion):
                answers[qid] = NoulAnswer(type="noul", noul=probs[0])
            elif isinstance(question, ChoiceQuestion):
                idx = max(range(len(probs)), key=probs.__getitem__)
                answers[qid] = ChoiceAnswer(
                    type="choice", choice=expected[idx],
                    probabilities=dict(zip(expected, probs)), confidence=confidence(probs),
                )
            else:
                answers[qid] = ScoreAnswer(
                    type="score", score=ordinal_expectation(probs),
                    legend={str(i): text for i, text in enumerate(question.criteria)},
                    probabilities=dict(zip(expected, probs)), confidence=confidence(probs),
                )
        return DecisionResponse(model=request.model or self.backend.name, answers=answers, usage=Usage())
