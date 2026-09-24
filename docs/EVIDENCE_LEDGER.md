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
| Browser MiniLM ONNX execution works in the deployed lab | USER_REPORTED / EXPERIMENTALLY_SUPPORTED | User supplied a successful 384-d browser receipt; deployment readiness is separately tool-verified. |
| Generic embedding plus cosine yields useful signal on the tiny hand-authored benchmark | USER_REPORTED / EXPERIMENTALLY_SUPPORTED in that receipt | 12-case transfer benchmark; small and hand-authored. |
| Set-aware scorer is better than pairwise on real NLP decision data | OPEN | No reviewed real-data receipt yet. |
| Set-aware can exploit candidate interaction | EXPERIMENTALLY_SUPPORTED in synthetic scope | Representative interaction run showed large gains, but other grid conditions reversed the relation. Not universal. |
| Conditional mixture improves probability quality in some interaction regimes | EXPERIMENTALLY_SUPPORTED in synthetic scope | Two-seed batch results repeatedly reduced Brier at interaction 1.0 and 2.0, with mixed accuracy effects. |
| Conditional mixture is universally superior to pairwise | CONTRADICTED | It loses on some tasks/metrics and is not universally better. |
| Candidate-order permutation is semantically neutral | EXPERIMENTALLY_SUPPORTED structurally | Neural scorer permutation errors were around numerical precision in the recovered tests; real pretrained encoder receipt is still pending. |
| Confidence alone can authorize actions | CONTRADICTED as a contract rule | Policy authority remains external. |
| Shortlist-then-rerank can reduce candidate work safely | EXPERIMENTALLY_SUPPORTED only in an oracle-vector test | N=128; K=8 kept 6.25 percent with recall@1 from 0.9961 to 1.0 across three seeds; K=16 was 1.0. |
| Temperature calibration is useful as a separate layer | EXPERIMENTALLY_SUPPORTED structurally; efficacy OPEN | Implemented and tested, but metric changes are task-dependent. |
| Split conformal prediction is useful as a separate uncertainty layer | EXPERIMENTALLY_SUPPORTED structurally | Coverage, set size, abstention, and NaN rejection are tested; shift validity remains open. |
| Candidate interaction is universally required | CONTRADICTED by synthetic comparison | Pairwise performs strongly when interaction is absent. |

## Rules

1. A higher number is not automatically a better model.
2. A structural property is not a performance result.
3. A synthetic result is not a real-data result.
4. A user-provided receipt is not independently re-executed evidence.
5. Repetition does not upgrade status.
6. Any claim used to justify execution authority needs a separate policy and authority proof.
