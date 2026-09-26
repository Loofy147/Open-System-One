# Contract Debt

Items intentionally not frozen as final v0.1 semantics.

## D1 — Duplicate contract representations

The recovery tree now contains both:
- the richer Pydantic contract in schema.py + engine.py
- the earlier minimal dataclass contract in contract.py

The richer Pydantic path is the recovered v0.3 reference and is currently more complete. The minimal contract must either become an explicitly named mathematical/minimal layer or be removed after compatibility review.

## D2 — Outcome model generalization

The richer schema already has stable Choice keys and descriptions, but Score/Noul have different representations. A future canonical contract should formalize a uniform Outcome object while preserving Score order and Noul binary semantics.

## D3 — Batch independence proof

The engine and tests prove one batched backend call and question-order stability with a deterministic backend. A real learned backend still needs an intervention proving independent questions do not alter one another's distributions.

## D4 — Calibration artifact

Calibration stays outside the score contract. A durable calibration object needs:
- method
- model/scorer identity
- fitting population and split
- fitted parameters
- validity range
- provenance
- revalidation rule

## D5 — Runtime provenance

A production receipt should include model/checkpoint identity and revision, runtime/backend, dtype/quantization, device, warm/cold state, latency, candidate count, and question count.

## D6 — Action authority

A probability distribution may inform policy but never grants authority by itself.

Capability issuance, authorization, side effects, retries, and tool execution remain outside inference.

## D7 — Reproducibility

Every benchmark receipt needs code ref, dataset/source ref, configuration, seed policy, population/split, raw metrics, failures, and interpretation.

## D8 — BANKING77 pilot statistics

The current browser pilot still has two measurement debts:
- exact per-K uniform Brier baseline rather than a mixed-K approximation
- deterministic, distribution-aware prototype sampling rather than first-five selection

Do not promote mixed-K skill or final prototype comparisons until these are fixed.

## D9 — Pretrained real-data comparison

The learned 24D transfer surrogate is useful evidence but cannot substitute for pretrained MiniLM/ModernBERT experiments.

Required next comparison:
representation x candidate regime x K x scorer, with fixed train/test provenance.

## D10 — Discovery evidence boundary

The precomposed discovery registry is deterministic and structurally tested, but registry membership is not empirical evidence. A future promotion path must link each candidate recipe to an observed failure receipt, a discriminating experiment, and its resulting evidence-ledger revision.

The current layer does not yet perform open-ended semantic failure classification from free-form observations, adaptive experiment selection from measured information gain, or autonomous experiment execution. Those remain discovery-frontier work, not established capability.

The current selector uses explicit deterministic ordering only: target-class coverage, requested evidence-gap coverage, declared cost, then key. No learned utility score is used.

## D11 — Adaptive Discovery epistemic model

The adaptive layer computes expected information gain from declared priors and outcome partitions. This is a formal planning calculation, not calibrated belief about the world.

Remaining debt:
- priors are manually declared research weights
- outcome partitions are manually declared
- historical outcomes are coarse receipts, not a posterior likelihood model
- experiment cost is a declared ordinal proxy, not measured resource cost
- no empirical noise/likelihood model is used
- free-form evidence-to-tag semantic classification remains open
- automatic experiment execution remains open

## D12 — Closed-loop persistence and epistemic update

The closed-loop layer validates an executed result, binds it to provenance, materializes reviewed evidence, creates scoped hypothesis-assessment events, and produces an immutable frontier revision.

Remaining debt:
- frontier persistence is represented as an immutable state artifact but has no canonical storage adapter
- automatic external experiment execution remains outside
- assessment events are deterministic interpretations of declared outcome partitions, not posterior probabilities
- no empirical likelihood/noise model updates the declared priors
- receipt review is explicit; the system does not auto-promote unreviewed execution output to evidence

## D13 — Claim verification and authority boundary

Layer 11 now provides deterministic cross-experiment synthesis, conflict detection, and explicit parent-linked ClaimRevision records.

Remaining debt:
- claim verification is not yet a separate verification event with an independently defined verifier contract
- Gate semantics are not yet frozen
- DecisionRevision is not yet connected to a verified claim
- conflict resolution remains an explicit future research/control-plane action rather than automatic adjudication
- no canonical persistence adapter exists for the claim ledger
- claim synthesis remains scoped to an explicit hypothesis-to-claim binding; open-ended semantic claim extraction is not established
