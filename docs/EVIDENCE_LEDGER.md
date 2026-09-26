# Evidence Ledger

This ledger is the durable boundary between facts, experiments, reports, and hypotheses.

## Status vocabulary

ESTABLISHED: supported by stable specification or independently established external fact.
EXPERIMENTALLY_SUPPORTED: verified by an executed experiment whose implementation and result are recorded.
USER_REPORTED: supplied as a receipt by the user; not independently re-executed here.
INFERENCE: derived from observed evidence but not directly measured.
HYPOTHESIS: proposed mechanism awaiting a discriminating test.
CONTRADICTED: current evidence argues against the claim in the tested scope.
UNKNOWN: insufficient evidence.
OPEN: explicitly awaiting a test or decision.

## Core claims

| Claim | Status | Evidence / limit |
|---|---|---|
| Typed decision contract can be represented independently of a model/runtime | EXPERIMENTALLY_SUPPORTED | Rich v0.3 schema and DecisionEngine are covered by the recovered contract suite. |
| Probabilities form a closed finite distribution | EXPERIMENTALLY_SUPPORTED | v0.3 normalization plus finite/non-finite tests. |
| Model output does not own execution authority | ESTABLISHED | Policy/capability layers are separate from inference. |
| Set-aware scorer is better than pairwise on real NLP decision data | OPEN | No reviewed real-data receipt yet. |
| Set-aware can exploit candidate interaction | EXPERIMENTALLY_SUPPORTED in synthetic scope | Representative interaction runs showed gains, but other grid conditions reversed the relation. Not universal. |
| Conditional mixture improves probability quality in some interaction regimes | EXPERIMENTALLY_SUPPORTED in synthetic scope | Two-seed batch results repeatedly reduced Brier in tested interaction regimes, with mixed accuracy effects. |
| Conditional mixture is universally superior to pairwise | CONTRADICTED | It loses on some tasks/metrics and is not universally better. |
| Shortlist-then-rerank can reduce candidate work safely | EXPERIMENTALLY_SUPPORTED only in an oracle-vector test | N=128; K=8 kept 6.25 percent with recall@1 from 0.9961 to 1.0 across three seeds; K=16 was 1.0. |
| Discovery can deterministically map an observed failure class to precomposed mechanism candidates | EXPERIMENTALLY_SUPPORTED | Base discovery registry and tests provide deterministic proposal/coordination behavior. |
| Structured FailureEvidence can reproducibly derive failure tags | EXPERIMENTALLY_SUPPORTED structurally | Numeric candidate/latency budgets and explicit boolean observations produce deterministic tags. |
| Expected information gain can be computed reproducibly from declared priors and outcome partitions | EXPERIMENTALLY_SUPPORTED structurally | Shannon entropy reduction is deterministic; priors are bookkeeping weights. |
| A recorded historical outcome can make a repeat experiment have zero expected information gain | EXPERIMENTALLY_SUPPORTED structurally | interaction_probe is recorded as mixed_gain, leaving one compatible hypothesis under its declared partition. |
| A compound experiment can explicitly distinguish more joint hypotheses than a single mechanism probe | EXPERIMENTALLY_SUPPORTED structurally | interaction_retrieval_guard declares four joint states and a 2-bit maximum under a uniform prior. This is a planning property, not empirical evidence. |
| Adaptive Discovery itself proves any research hypothesis | CONTRADICTED | Planner output remains ADAPTIVE_PLAN_NOT_EVIDENCE until a real experiment produces a reviewed receipt. |
| A reviewed experiment result can deterministically produce scoped evidence, hypothesis assessments, and an immutable frontier revision | EXPERIMENTALLY_SUPPORTED structurally | Closed-loop contracts and tests validate strict execution parsing, provenance binding, deterministic evidence identity, many-to-one handling, idempotent replay, and frontier-aware reselection. |
| The closed loop performs Bayesian posterior updating | CONTRADICTED | Priors remain declared research weights; no likelihood/noise model is implemented. |
| Cross-experiment evidence can be synthesized deterministically without rewriting the underlying assessments | OPEN | Layer 11 implementation and structural tests exist at the current frontier, but no post-change CI execution has been independently revalidated yet. |
| Contradictory evidence is represented as a conflict rather than silently resolved by experiment priority | OPEN | The Layer 11 contract and tests specify CONFLICTED synthesis, but post-change execution evidence is still required. |
| An EXPERIMENTALLY_SUPPORTED claim revision requires the full current scoped evidence set to be unconflicted | OPEN | Structural test coverage exists for rejecting support-only cherry-picking; post-change CI verification is still required. |
| Claim status changes are explicit immutable revisions rather than automatic hypothesis mutations | OPEN | The implementation and tests encode parent-linked immutable revisions, but the current post-change execution result is not yet recorded. |

## Rules

1. A higher number is not automatically a better model.
2. A structural property is not a performance result.
3. A synthetic result is not a real-data result.
4. A user-provided receipt is not independently re-executed evidence.
5. Repetition does not upgrade a claim.
6. Discovery output is a hypothesis generator, not evidence by itself.
7. Adaptive information gain is a planning quantity, not a model-performance result.
8. Any claim used to justify execution authority needs a separate policy and authority proof.
9. A reviewed experiment receipt is required before execution output becomes ledger evidence.
10. Hypothesis assessments are scoped evidence-derived interpretations; they do not rewrite priors.
11. A many-to-one outcome partition cannot uniquely support a hypothesis.
12. Replaying the same reviewed receipt must not duplicate evidence or frontier state.
13. Cross-experiment synthesis must preserve the original assessment and evidence identities.
14. Conflict is an observable state; synthesis does not select a winning source by recency, experiment key, or declared cost.
15. An experimental claim revision must account for the full current scoped evidence set and may not cherry-pick around contradictory evidence.
16. Claim revisions are control-plane records and do not grant execution authority.
