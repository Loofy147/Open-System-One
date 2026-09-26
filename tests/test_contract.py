import math
import pytest

from open_system_one import DecisionEngine
from open_system_one.backends.mock import FixedBackend
from open_system_one.schema import DecisionRequest
from open_system_one.probability import confidence, ordinal_expectation

def test_all_types_and_closed_schema():
    req=DecisionRequest.model_validate({"state":{"msg":"late order"},"questions":{
        "ok":{"type":"noul","instructions":"Is this okay?"},
        "team":{"type":"choice","instructions":"Who?","criteria":{"a":"A","b":"B","c":"C"}},
        "score":{"type":"score","instructions":"How bad?","criteria":["low","mid","high"]},
    }})
    out=DecisionEngine(FixedBackend()).evaluate(req)
    assert set(out.answers)=={"ok","team","score"}
    assert out.answers["ok"].type=="noul"
    assert out.answers["team"].choice in {"a","b","c"}
    s=out.answers["score"]; assert 0<=s.score<=2; assert math.isclose(sum(s.probabilities.values()),1.0)

def test_confidence_extremes():
    assert math.isclose(confidence([1.0]),1.0)
    assert math.isclose(confidence([0.5,0.5]),0.0)
    assert confidence([0.99,0.01])>confidence([0.7,0.3])

def test_ordinal_expectation():
    assert math.isclose(ordinal_expectation([0,0,1]),2.0)

def test_probability_functions_reject_non_finite_values():
    from open_system_one.probability import normalize,softmax
    for values in ([math.nan,1.0],[math.inf,1.0],[-math.inf,1.0],[math.nan,math.nan]):
        with pytest.raises(ValueError): normalize(values)
        with pytest.raises(ValueError): softmax(values)

def test_engine_rejects_backend_non_finite_output():
    class BadBackend:
        name="bad"
        def evaluate_batch(self,state,questions):
            return {qid:[math.nan,1.0] for qid in questions}
    req=DecisionRequest.model_validate({"state":"x","questions":{"q":{"type":"choice","instructions":"pick","criteria":{"a":"a","b":"b"}}}})
    with pytest.raises(ValueError): DecisionEngine(BadBackend()).evaluate(req)

