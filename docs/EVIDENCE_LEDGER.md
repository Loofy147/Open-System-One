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
| Typed decision contract can be represented independently of a model/runtime | ESTABLISHED | Project specification and reference tests. |
| Probabilities form a closed finite distribution | ESTABLISHED | Contract invariant plus tests. |
| Model output does not own execution authority | ESTABLISHED | Contract/policy separation. |
| Browser MiniLM ONNX execution works in the deployed lab | USER_REPORTED / EXPERIMENTALLY_SUPPORTED | User supplied a successful 384-d browser receipt; deployment readiness is separately tool-verified. |
| Generic embedding plus cosine yields useful signal on the tiny hand-authored benchmark | USER_REPORTED / EXPERIMENTALLY_SUPPORTED in that receipt | 12-case transfer benchmark; small and hand-authored. |
| Set-aware scorer is better than pairwise on real NLP decision data | OPEN | No reviewed BANKING77 receipt yet. |
| Conditional mixture is superior to pairwise | CONTRADICTED in the 12-case receipt; OPEN overall | Small sample; not a universal claim. |
| Candidate-order permutation is semantically neutral | OPEN at real-encoder level | Structural neural scorer tests passed; corrected browser receipt is still pending. |
| Confidence alone can authorize actions | CONTRADICTED as a contract rule | Policy authority remains external. |
| Shortlist-then-rerank can reduce candidate work safely | EXPERIMENTALLY_SUPPORTED only in an oracle-vector test | N=128; K=8 kept 6.25 percent of candidates with 0.9961 to 1.0 recall@1 across three seeds; K=16 was 1.0. |
| Temperature calibration is useful as a separate layer | EXPERIMENTALLY_SUPPORTED in prior synthetic tests | Held-out post-hoc implementation; domain-shift validation remains open. |
| Split conformal prediction is useful as a separate uncertainty layer | EXPERIMENTALLY_SUPPORTED structurally | Coverage and set-size implementation tested; broad shift validation remains open. |
| Candidate interaction is universally required | CONTRADICTED by synthetic comparison | Pairwise remains strong when interaction is absent; usefulness is task-dependent. |

## Rules

1. A higher number is not automatically a better model.
2. A structural property is not a performance result.
3. A synthetic result is not a real-data result.
4. A user-provided receipt is not independently re-executed evidence.
5. Repetition does not upgrade status.
6. Any claim used to justify execution authority needs a separate policy and authority proof.
