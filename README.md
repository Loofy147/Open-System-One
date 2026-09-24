# Open System One

Machine-native typed decision substrate and research laboratory.

## Architecture

Structured opaque state + typed questions + finite outcome spaces
-> batched probabilistic decisions
-> calibration/selective layer
-> deterministic policy
-> capability/authorized execution.

The contract is independent of encoder, scorer, runtime, provider, and action system.

## Recovered research surface

- Pydantic typed schema: Choice, Score, Noul
- batch-first DecisionEngine
- causal-logit backend skeleton
- diffusion read-slot backend protocol
- compact learned DecisionStudent
- pairwise / marker / set-aware / Set Transformer / relational / conditional scorers
- temperature scaling and split conformal prediction
- shortlist/prefilter
- 12 machine-native primitive probes plus registered pair interactions
- 31-test v0.3 structural suite

## Evidence status

The repository deliberately distinguishes contract correctness from model truth and action authority.

The strongest prior executable artifact is the recovered v0.3 frontier. A local execution of its suite produced 31 passed tests.

Synthetic experiments provide conditional evidence:
- set-aware can exploit candidate interaction, but is not universal
- conditional mixture repeatedly improves Brier in several small interaction batches, with mixed top-1 accuracy
- shortlist can be highly efficient under oracle-vector assumptions
- calibration effects are task-dependent

Real pretrained encoder evidence remains limited:
- browser MiniLM inference has a user-provided successful receipt
- the 12-case browser benchmark is small and hand-authored
- BANKING77 pilot is implemented but the reviewed numerical receipt is still pending

## Non-goals

This repository is not a Jev reproduction and contains no proprietary Jev weights. Public System One/Laya ideas are treated as research inputs, not as hidden ground truth.

## Evidence and recovery

Read:
- docs/DECISION_CONTRACT_v0.1.md
- docs/ARCHITECTURE_FULL.md
- docs/RESEARCH_PROTOCOL.md
- docs/EVIDENCE_LEDGER.md
- docs/RECOVERY_AUDIT_2026-09-24.md
- docs/CONTRACT_DEBT.md

Historical executable archives remain indexed in docs/LEGACY_ARTIFACTS.md.
