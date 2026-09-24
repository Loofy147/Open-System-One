# Recovery Audit — 2026-09-24

## Purpose
Prevent loss of capabilities and evidence achieved before the GitHub repository was initialized.

## Critical finding
The current GitHub foundation is a simplified contract layer. The strongest prior verified research state is the local open-system-one-v0.3-stage artifact, which passes 31/31 tests and contains substantially more executable surface.

Therefore: v0.3-stage is the recovery baseline for research capability. It is not automatically the canonical architecture; its claims remain classified by evidence.

## Verified local receipt
Command: PYTHONPATH=src pytest -q
Result: 31 passed in 2.24s
Artifact: open-system-one-foundation-v0.3-realtransfer.zip
SHA-256: f5f389c2a26de28f401e5d1510062059cb367a841fe23d90e4565bb8fd8ac13d
Related staged archive SHA-256: 2592f80ca68f3cd181a35c15b2d9cef4a80b2308f6de726fbc6366af26eda6d4

## Capability inventory recovered
### Contract / orchestration
- Pydantic schema with Choice, Score, Noul.
- Runtime-supplied finite outcome spaces.
- Stable question IDs and structured candidate descriptions.
- Batch-first backend protocol.
- DecisionEngine and explicit LegacyAdapter.
- Entropy-derived confidence and ordinal expectation.
- Closed probability normalization and non-finite rejection.

### Backends
- causal-logit backend skeleton with single-token outcome verification.
- diffusion read-slot backend protocol.
- mock backend for contract testing.

### Learned student
- DecisionStudent with a bidirectional encoder and scalar candidate head.
- Candidate-row packing and group softmax per question.
- Soft-target KL/NLL plus Brier distillation loss.
- ModernBERT-base is the default candidate encoder.

### Scorer research
- pairwise
- marker/shared-context
- DeepSets/set-aware
- Set Transformer
- explicit relational attention
- conditional mixture

### Uncertainty
- Brier and ECE.
- temperature fitting.
- split conformal calibration and prediction sets.
- coverage, set size, and abstention rate.

### Scalability
- cosine shortlist.
- recall@K.
- deterministic and lossless K=N behavior.

### Primitive layer
12 independently probed mechanisms: reification, composition, unification, explicit control, memoization, approximate prefilter, associative accumulation, causal order, content identity, capability, convergent merge, dynamic candidate scoring.
Single sweep: 12/12 probes passed.
Registered pair interaction probes: 5.
Unregistered pairs remain OPEN instead of being misclassified as synergy.

## High-value findings
### Candidate interaction is not universal
In the synthetic rerun at interaction=0, K=8, pairwise accuracy was 0.96094 while set-aware was 0.76953. Set awareness therefore cannot be assumed beneficial.

### Set-aware can recover interaction signal
A representative earlier sweep at interaction=1.25, K=8 gave pairwise accuracy 0.73242 and Brier 0.02513 versus set-aware accuracy 0.84375 and Brier 0.01220. A later grid rerun did not reproduce the same magnitude consistently. Keep this as a high-value hypothesis, not a general winner.

### Conditional mixture has a probability-quality signal
At interaction=1.0, K=8, two-seed means were:
- contrastive: pairwise accuracy 0.82031, Brier 0.027217; conditional accuracy 0.83984, Brier 0.024735.
- competitive: pairwise accuracy 0.60156, Brier 0.050487; conditional accuracy 0.59766, Brier 0.047649.
- global: pairwise accuracy 0.75781, Brier 0.015980; conditional accuracy 0.75391, Brier 0.014120.
At interaction=2.0, global Brier was 0.053281 pairwise versus 0.045413 conditional.
Interpretation: conditional mixture repeatedly improves Brier in these small synthetic batches while sometimes slightly reducing top-1 accuracy. This suggests a probability-quality mechanism, not a universal accuracy improvement.

### Calibration is not automatically positive
Temperature fitting changed metrics only slightly in the recorded sweep and did not monotonically improve ECE. Calibration remains an empirical layer.

### Shortlisting is a scalability lead
Oracle-vector N=128 experiments retained 6.25 percent of candidates at K=8 with recall@1 of 1.0, 0.99609, and 0.99609 across three seeds; K=16 was 1.0 across all three. This does not prove real-encoder retrieval safety.

## Real-encoder boundary
The local environment could not directly load a pretrained checkpoint. The learned 24D bidirectional encoder experiment is therefore a transfer surrogate. The later browser MiniLM experiment established real browser inference execution, but its 12-case benchmark was user-reported and hand-authored.
BANKING77 remains the real-data discriminator.

## Recovery decision
Do not reduce the system to embedding -> cosine -> probability.
The recovered frontier spans typed contract, batch engine, replaceable scorer, learned student, probability/calibration, selective prediction, shortlist, policy, and capability boundary.

## Immediate recovery tasks
1. Port the v0.3 executable modules and all 31 tests into the GitHub tree.
2. Preserve the evidence ledger, failure ledger, and contract-debt documents.
3. Reconcile duplicate contract definitions so one schema is canonical.
4. Port experiment scripts and raw result receipts.
5. Correct mixed-K Brier reporting before new BANKING77 conclusions.
6. Make prototype sampling deterministic and distribution-aware before final BANKING77 claims.
7. Keep set-aware and conditional mixture as research candidates until real-data intervention confirms value.