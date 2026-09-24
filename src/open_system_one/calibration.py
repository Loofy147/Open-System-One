from __future__ import annotations
from dataclasses import dataclass

def brier(probs: list[float], target: int) -> float:
    return sum((p-(1.0 if i==target else 0.0))**2 for i,p in enumerate(probs))

def expected_calibration_error(probs: list[list[float]], targets: list[int], bins: int=10) -> float:
    if len(probs)!=len(targets) or not probs: raise ValueError("probs and targets must have equal non-zero length")
    buckets=[[] for _ in range(bins)]
    for p,y in zip(probs,targets):
        i=max(range(len(p)),key=p.__getitem__); conf=p[i]; b=min(bins-1,int(conf*bins)); buckets[b].append((conf,1.0 if i==y else 0.0))
    acc=0.0
    for bucket in buckets:
        if bucket:
            mean_conf=sum(x for x,_ in bucket)/len(bucket); mean_acc=sum(x for _,x in bucket)/len(bucket)
            acc += abs(mean_conf-mean_acc)*len(bucket)/len(probs)
    return acc

@dataclass(frozen=True)
class CalibrationReport:
    accuracy: float
    brier: float
    ece: float

def report(probs:list[list[float]],targets:list[int]) -> CalibrationReport:
    correct=sum(max(range(len(p)),key=p.__getitem__)==y for p,y in zip(probs,targets))
    return CalibrationReport(correct/len(targets),sum(brier(p,y) for p,y in zip(probs,targets))/len(targets),expected_calibration_error(probs,targets))
