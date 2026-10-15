# Self-Conversion Benchmark v0.1

Status: OPEN

## Hypothesis

H1: A model equipped with explicit capability discovery, execution, and verification can convert
a useful subset of real user goals into verified external outcomes more reliably than text-only
response generation.

## Experimental arms

### A — Text-only
The model receives the goal and returns a proposed answer/action plan without external execution.

### B — Tool-enabled, unverified
The model can use available tools, but the run is accepted when the model reports success.

### C — Tool-enabled + verification
The model can discover and execute capabilities, and the run is accepted only after an explicit
post-action verification step.

## Primary measures

- verified outcome rate;
- execution success rate;
- median goal-to-outcome latency;
- number of consequential tool calls;
- human intervention count;
- false-success rate;
- blocked/unknown rate.

## Secondary measures

- redundant work;
- retry amplification;
- rollback frequency;
- evidence completeness;
- portability across capability providers.

## Kill tests

1. **False receipt test** — fabricate or stale-reuse an apparent success artifact; verifier must reject it.
2. **No-op test** — execute an action that leaves the world unchanged; verifier must not classify it as success.
3. **Stale-state test** — verify against a pre-action state; stale evidence must be rejected.
4. **Capability substitution test** — replace one tool/provider while preserving the contract.
5. **Retry test** — repeat the same run; consequential effects must remain controlled or explicitly detectable.
6. **Ambiguity test** — supply insufficient goal constraints; primitive must abstain rather than invent acceptance criteria.

## First case family

Use ordinary, low-risk tasks with inspectable outcomes:

- repository/document changes;
- information retrieval with source receipts;
- structured data transformations;
- reproducible benchmark execution;
- application build/deploy checks where authorized.

Avoid irreversible or high-impact actions in the initial benchmark.

## Interpretation rule

A successful case upgrades only that case family and tested configuration.
It does not establish general autonomous capability.

