# Full Architecture

## Layer 0 — Contract

Opaque state + typed questions + finite outcome spaces.

This layer defines meaning and invariants, not model internals.

## Layer 1 — Representation

State and outcome materialization are backend concerns.

Possible representations:
- labels/IDs and descriptions
- train-derived prototypes
- contextual embeddings
- learned marker representations
- diffusion read slots

## Layer 2 — Decision computation

Candidate scoring is replaceable:

- pairwise: candidate i sees state and itself
- marker/shared-context: candidates share a conditioned context
- set-aware: candidate scores depend on an aggregate of the candidate set
- relational: candidate-candidate interaction
- conditional mixture: learned or fixed gate between independent and relational evidence

A scorer must preserve candidate identity and define its permutation semantics explicitly.

## Layer 3 — Probability

Raw scores are transformed into a closed distribution over the declared outcome space.

Do not conflate:
- score
- probability
- confidence
- correctness
- permission

## Layer 4 — Calibration and selective prediction

Examples:
- temperature scaling
- proper scoring objectives
- split conformal prediction
- abstention/selective policies

Calibration is an empirical reliability layer, not an authority layer.

## Layer 5 — Policy

A deterministic policy maps model output plus explicit external thresholds/costs/context to a disposition such as accept, review, or abstain.

No threshold is canonical.

## Layer 6 — Capability and execution

Capabilities/permissions determine which actions are authorized.

Tool invocation, retries, side effects, and external state mutation remain outside model inference.

## Layer 7 — Evidence/control plane

The control plane represents:
Question -> Candidate -> Decision -> Run -> Evidence

and separately:
Claim -> Evidence -> Verification -> Gate -> DecisionRevision

This layer remains outside the core decision contract.

## Layer 8 — Discovery

Discovery turns unexplained behavior into explicit candidate mechanisms:

Failure -> failure class -> precomposed recipes -> coordinated mechanism set -> discriminating experiment

The discovery registry is deterministic research infrastructure. A structured FailureObservation is classified by explicit trigger tags; the selector then chooses experiment designs by transparent coverage, evidence-gap coverage, declared cost, and stable key order. It can suggest inference mechanisms, computation/control-plane mechanisms, or an explicit authority handoff, but it cannot grant authority. Generated candidates remain HYPOTHESIS until the evidence ledger is updated by a reviewed receipt. Discovery planning is not itself an experiment result.

## Runtime boundary

The same semantics should be portable across:
- browser ONNX/WASM/WebGPU
- ONNX Runtime
- MLX
- CoreML/ANE
- Android/local runtime
- other compliant backends

Runtime optimization is invalid if it changes declared semantics.

## Training boundary

Teacher-student transfer, cross-entropy, Brier/proper scoring objectives, RLCD-like objectives, calibration fitting, and consistency losses are implementation/training strategies.

None is part of the canonical decision contract.

## Acceptance boundary

A proposed mechanism enters the core only after:
1. structural kill tests
2. isolated causal intervention
3. baseline ablation
4. real-data transfer
5. repeat/controlled measurement
6. provenance-complete receipt
