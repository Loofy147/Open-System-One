# Architecture

Opaque State
    +
Independent Typed Questions
    +
Finite Outcome Spaces
    |
    v
Batched Probabilistic Decision Interface
    |
    +-- Representation
    |     +-- label-only
    |     +-- train prototype
    |
    +-- Scorer
    |     +-- pairwise
    |     +-- set-aware
    |     +-- conditional
    |
    +-- Calibration
    |
    v
Deterministic Policy
    |
    v
Capability / Permission / Action

## Separation rules

Contract defines what a decision means.

Representation defines how state and outcomes become machine-readable objects.

Scorer defines how candidate evidence is compared.

Calibration addresses probabilistic reliability.

Policy maps model output to an allowed disposition.

Execution remains outside the model and requires explicit authority.

## Runtime rule

The same contract may run on browser ONNX/WASM, WebGPU, MLX, CoreML/ANE, ONNX Runtime, Android, or another backend.

Runtime optimizations must not silently alter contract semantics.

## Architectural objective

Test a replaceable capability boundary rather than clone one model. A new encoder or scorer should be able to replace the current implementation without changing the decision contract.
