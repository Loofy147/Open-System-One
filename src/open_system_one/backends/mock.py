from __future__ import annotations
from typing import Any
from ..schema import ChoiceQuestion, NoulQuestion, ScoreQuestion

class FixedBackend:
    name="fixed-test"
    def __init__(self,value:float=0.5):
        self.value=value; self.calls=0
    def evaluate_batch(self,state:Any,questions:dict[str,Any])->dict[str,list[float]]:
        self.calls+=1; out={}
        for qid,q in questions.items():
            if isinstance(q,NoulQuestion): out[qid]=[self.value,1.0-self.value]
            elif isinstance(q,ChoiceQuestion): out[qid]=[1.0/len(q.criteria)]*len(q.criteria)
            elif isinstance(q,ScoreQuestion): out[qid]=[1.0/len(q.criteria)]*len(q.criteria)
            else: raise TypeError(type(q).__name__)
        return out
