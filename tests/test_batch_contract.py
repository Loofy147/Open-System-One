from open_system_one import DecisionEngine
from open_system_one.backends.mock import FixedBackend
from open_system_one.schema import DecisionRequest
from open_system_one.engine import LegacyAdapter

def req(qs): return DecisionRequest.model_validate({"state":{"x":1},"questions":qs})

def test_backend_is_called_once_for_all_questions():
    backend=FixedBackend()
    out=DecisionEngine(backend).evaluate(req({
        "a":{"type":"choice","instructions":"pick","criteria":{"x":"X","y":"Y"}},
        "b":{"type":"score","instructions":"rank","criteria":["low","high"]},
    }))
    assert backend.calls==1 and set(out.answers)=={"a","b"}

def test_question_order_does_not_affect_other_question_semantics():
    engine=DecisionEngine(FixedBackend())
    a=engine.evaluate(req({"q1":{"type":"choice","instructions":"x","criteria":{"a":None,"b":None}},"q2":{"type":"noul","instructions":"y"}}))
    b=engine.evaluate(req({"q2":{"type":"noul","instructions":"y"},"q1":{"type":"choice","instructions":"x","criteria":{"a":None,"b":None}}}))
    assert a.answers["q1"]==b.answers["q1"] and a.answers["q2"]==b.answers["q2"]

def test_legacy_adapter_is_explicitly_compatible_not_the_core_contract():
    class Old:
        name="old"
        def evaluate_question(self,state_text,question):
            return [0.25,0.75] if question.type=="noul" else [1.0/len(question.criteria)]*len(question.criteria)
    out=DecisionEngine(LegacyAdapter(Old())).evaluate(req({"q":{"type":"noul","instructions":"x"}}))
    assert out.model=="old"
