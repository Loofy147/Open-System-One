# Contract Debt

These items are intentionally not frozen as canonical in v0.1.

## D1 — Outcome identity versus description

The current Python reference kernel represents outcomes as strings. The architectural target is stable identity plus semantic description.

Target shape:
- stable outcome ID
- semantic description
- optional structured criteria

Positional index must not become semantic identity.

## D2 — Score result semantics

Score is ordinal, not ordinary classification. A future implementation must expose both:
- distribution over ordered levels
- expected or derived ordinal value

## D3 — Batch independence proof

The backend Protocol accepts one DecisionRequest containing multiple questions, but a real backend experiment must prove that each independent question is invariant under the presence and order of the other questions.

## D4 — Calibration artifact

Calibration stays outside the core score contract. A durable calibration object needs:
- method
- model/scorer identity
- fitting population and split
- fitted parameters
- validity range
- provenance
- revalidation rule

## D5 — Policy thresholds

No confidence threshold is canonical. Previous helper defaults of 0.90 and 0.60 were examples, not evidence-backed policy.

## D6 — Runtime provenance

A production receipt should include:
- model/checkpoint identity and revision
- runtime/backend
- dtype/quantization
- device
- warm/cold state
- latency
- candidate count
- question count

## D7 — Action authority

A probability distribution may inform policy but never grants authority by itself.

Capability issuance, authorization, side effects, retries, and tool execution remain outside inference.

## D8 — Reproducibility

Every benchmark receipt needs code ref, dataset/source ref, configuration, seed policy, population/split, raw metrics, failures, and interpretation.
