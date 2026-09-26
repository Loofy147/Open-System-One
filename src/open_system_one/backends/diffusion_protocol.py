from __future__ import annotations
from typing import Any, Protocol

class ReadSlotBackend(Protocol):
    name:str
    def read_batch(self,state:Any,questions:dict[str,Any])->dict[str,list[float]]: ...

class DiffusionDecisionBackend:
    def __init__(self,reader:ReadSlotBackend):
        self.reader=reader; self.name=reader.name
    def evaluate_batch(self,state:Any,questions:dict[str,Any])->dict[str,list[float]]:
        return self.reader.read_batch(state,questions)
