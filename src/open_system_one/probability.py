from __future__ import annotations
import math
from collections.abc import Sequence

def softmax(logits: Sequence[float]) -> list[float]:
    if not logits or any(not math.isfinite(float(x)) for x in logits):
        raise ValueError("logits must be non-empty and finite")
    m=max(logits); exps=[math.exp(float(x)-m) for x in logits]; z=sum(exps)
    if not math.isfinite(z) or z<=0: raise ValueError("softmax normalization failed")
    return [x/z for x in exps]

def normalize(probs: Sequence[float]) -> list[float]:
    if not probs or any(not math.isfinite(float(x)) or float(x)<0 for x in probs):
        raise ValueError("probabilities must be finite and non-negative")
    z=float(sum(probs))
    if not math.isfinite(z) or z<=0: raise ValueError("probabilities must have finite positive mass")
    out=[float(x)/z for x in probs]
    if any(not math.isfinite(x) for x in out): raise ValueError("normalization produced non-finite output")
    return out

def entropy(probs: Sequence[float]) -> float:
    p=normalize(probs); return -sum(x*math.log(x) for x in p if x>0)

def confidence(probs: Sequence[float]) -> float:
    p=normalize(probs)
    if len(p)==1: return 1.0
    c=1.0-entropy(p)/math.log(len(p))
    return max(0.0,min(1.0,c))

def ordinal_expectation(probs: Sequence[float]) -> float:
    p=normalize(probs); return sum(i*x for i,x in enumerate(p))
