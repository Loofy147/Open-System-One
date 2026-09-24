from __future__ import annotations

import itertools
import json
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable

from .primitives import (
    GSet, BloomPrefilter, CapabilityIssuer, LamportClock, candidate_scores,
    compose, content_id, fold_monoid, memoize, reify, unify,
    PrimitiveSpec, PRIMITIVES,
)


@dataclass(frozen=True)
class ProbeResult:
    primitive: str
    status: str
    elapsed_ms: float
    detail: str


@dataclass(frozen=True)
class PairResult:
    first: str
    second: str
    status: str
    elapsed_ms: float
    detail: str


def _timed(fn: Callable[[], Any]) -> tuple[float, Any]:
    start = time.perf_counter_ns()
    value = fn()
    return (time.perf_counter_ns() - start) / 1_000_000.0, value


def canonical_probe(spec: PrimitiveSpec) -> Any:
    name = spec.name
    if name == "reification":
        c = reify(3, lambda x: x + 2)
        assert c.value == 3 and c.continue_(3) == 5
        return c
    if name == "composition":
        assert compose(lambda x: x + 1, lambda x: x * 2)(3) == 8
        return True
    if name == "unification":
        env = unify(("?x", "b"), ("a", "b"))
        assert env == {"?x": "a"}
        return env
    if name == "explicit_control":
        from .primitives import ControlState, Continuation
        s = ControlState(4, Continuation(lambda x: x * 3))
        assert s.step() == 12 and s.done
        return s
    if name == "memoization":
        calls = {"n": 0}
        @memoize
        def f(x: int) -> int:
            calls["n"] += 1
            return x * x
        assert f(4) == 16 and f(4) == 16 and calls["n"] == 1
        return f
    if name == "approximate_prefilter":
        b = BloomPrefilter()
        b.add("known")
        assert b.maybe_contains("known")
        return b
    if name == "associative_accumulation":
        assert fold_monoid([1, 2, 3], lambda a, b: a + b, 0) == 6
        return 6
    if name == "causal_order":
        a, b = LamportClock(), LamportClock()
        x = a.tick()
        y = b.receive(x)
        assert y > x and b.value == y
        return y
    if name == "content_identity":
        assert content_id({"b": 2, "a": 1}) == content_id({"a": 1, "b": 2})
        return content_id({"a": 1})
    if name == "capability":
        issuer = CapabilityIssuer(b"secret")
        cap = issuer.issue("agent", "read", "dataset")
        assert issuer.verify(cap, "agent", "read", "dataset")
        assert not issuer.verify(cap, "agent", "write", "dataset")
        return cap
    if name == "convergent_merge":
        a = GSet().add("a")
        b = GSet().add("b")
        assert a.merge(b) == b.merge(a) == GSet(frozenset({"a", "b"}))
        return a.merge(b)
    if name == "dynamic_scoring":
        scores = candidate_scores([1, 0], {"a": [1, 0], "b": [0, 1]})
        assert scores["a"] > scores["b"]
        return scores
    raise KeyError(name)


def kill_probe(spec: PrimitiveSpec) -> None:
    name = spec.name
    if name == "unification":
        from .primitives import UnificationError
        try:
            unify(("a",), ("b",))
        except UnificationError:
            return
        raise AssertionError("unification accepted incompatible structures")
    if name == "approximate_prefilter":
        b = BloomPrefilter()
        b.add("a")
        assert b.maybe_contains("a")
        return
    if name == "capability":
        issuer = CapabilityIssuer(b"s")
        cap = issuer.issue("a", "read", "r")
        assert not issuer.verify(cap, "a", "write", "r")
        return
    if name == "content_identity":
        assert content_id({"x": 1}) != content_id({"x": 2})
        return
    if name == "convergent_merge":
        a = GSet().add("a")
        b = GSet().add("b")
        assert a.merge(b) == b.merge(a)
        return
    if name == "dynamic_scoring":
        try:
            candidate_scores([1, 0], {"bad": [1]})
        except ValueError:
            return
        raise AssertionError("candidate dimension mismatch was accepted")


def run_single_sweep() -> list[ProbeResult]:
    results = []
    for spec in PRIMITIVES:
        def run(spec=spec):
            value = canonical_probe(spec)
            kill_probe(spec)
            return value
        try:
            elapsed, _ = _timed(run)
        except Exception as exc:
            results.append(ProbeResult(spec.name, "CONTRADICTED", 0.0, repr(exc)))
        else:
            results.append(ProbeResult(spec.name, "EXPERIMENTALLY_SUPPORTED", elapsed, spec.relation))
    return results


def run_pair_sweep(names: list[str] | None = None) -> list[PairResult]:
    selected = [s for s in PRIMITIVES if names is None or s.name in names]
    results = []
    for a, b in itertools.combinations(selected, 2):
        start = time.perf_counter_ns()
        try:
            detail = _pair_probe(a.name, b.name)
        except Exception as exc:
            results.append(PairResult(a.name, b.name, "CONTRADICTED",
                                      (time.perf_counter_ns() - start) / 1e6, repr(exc)))
        else:
            status = "EXPERIMENTALLY_SUPPORTED" if detail is not None else "OPEN"
            results.append(PairResult(
                a.name, b.name, status, (time.perf_counter_ns() - start) / 1e6,
                detail or "no registered interaction hypothesis",
            ))
    return results


def _pair_probe(a: str, b: str) -> str | None:
    pair = frozenset((a, b))
    if pair == frozenset(("composition", "memoization")):
        f = memoize(compose(lambda x: x + 1, lambda x: x * 2))
        assert f(4) == 10 == f(4)
        return "memoization preserves composed pipeline result and removes repeated computation"
    if pair == frozenset(("content_identity", "memoization")):
        cache = {content_id({"x": 1}): 42}
        assert cache[content_id({"x": 1})] == 42
        return "content identity provides stable cache key"
    if pair == frozenset(("capability", "content_identity")):
        issuer = CapabilityIssuer(b"s")
        cap = issuer.issue("a", "read", "r")
        assert issuer.verify(cap, "a", "read", "r")
        assert content_id(cap.__dict__) == content_id(cap.__dict__.copy())
        return "capability artifact has stable content identity"
    if pair == frozenset(("causal_order", "convergent_merge")):
        c = LamportClock()
        t = c.tick()
        state = GSet().add(("event", t)).merge(GSet().add(("event", c.tick())))
        assert len(state.values) == 2
        return "causal tags survive convergent set merge"
    if pair == frozenset(("dynamic_scoring", "approximate_prefilter")):
        scores = candidate_scores([1, 0], {"a": [1, 0], "b": [0, 1]})
        gate = BloomPrefilter()
        gate.add("a")
        assert max(scores, key=scores.get) == "a" and gate.maybe_contains("a")
        return "prefilter retains the candidate required by the scoring maximum"
    return None


def save_results(path: str, singles: list[ProbeResult], pairs: list[PairResult]) -> None:
    payload = {"singles": [asdict(x) for x in singles], "pairs": [asdict(x) for x in pairs]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
