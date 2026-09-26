from __future__ import annotations
from typing import Any, Dict, List, Literal, Union
from pydantic import BaseModel, Field, ConfigDict, model_validator

class NoulCriteria(BaseModel):
    model_config = ConfigDict(extra="forbid")
    true: Any | None = None
    false: Any | None = None

class NoulQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["noul"]
    instructions: Any
    criteria: NoulCriteria | None = None

class ChoiceQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["choice"]
    instructions: Any
    criteria: Dict[str, Any] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_keys(self):
        if len(self.criteria) > 255:
            raise ValueError("choice supports at most 255 options")
        if any(not isinstance(k, str) or not k for k in self.criteria):
            raise ValueError("choice option names must be non-empty strings")
        return self

class ScoreQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["score"]
    instructions: Any
    criteria: List[Any] = Field(min_length=1, max_length=255)

Question = Union[NoulQuestion, ChoiceQuestion, ScoreQuestion]
State = str | dict[str, Any] | list[Any] | None

class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    state: State
    questions: Dict[str, Question] = Field(min_length=1)
    model: str | None = None

class NoulAnswer(BaseModel):
    type: Literal["noul"]
    noul: float = Field(ge=0.0, le=1.0)

class ChoiceAnswer(BaseModel):
    type: Literal["choice"]
    choice: str
    probabilities: Dict[str, float]
    confidence: float = Field(ge=0.0, le=1.0)

class ScoreAnswer(BaseModel):
    type: Literal["score"]
    score: float
    legend: Dict[str, Any]
    probabilities: Dict[str, float]
    confidence: float = Field(ge=0.0, le=1.0)

Answer = Union[NoulAnswer, ChoiceAnswer, ScoreAnswer]

class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0

class DecisionResponse(BaseModel):
    model: str
    answers: Dict[str, Answer]
    usage: Usage = Usage()
