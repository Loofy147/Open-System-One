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

Generated candidates remain HYPOTHESIS until the evidence ledger is updated by a reviewed receipt.

## Layer 9 — Adaptive Discovery

Adaptive Discovery consumes structured FailureEvidence, derives failure observations, consults the remaining hypothesis space, and selects the experiment with greatest declared expected entropy reduction after class/evidence-gap constraints.

The layer is non-canonical and non-authoritative.

Its information model is explicit:
- priors are declared research weights
- outcomes are declared partitions
- historical outcomes constrain repeat information
- expected information gain is computed mathematically, not guessed from model confidence
- no free-form semantic confidence is inferred
- no experiment is executed merely because it has high expected information gain

## Layer 10 — Closed-Loop Experiment Evidence

The closed loop begins only after an experiment has executed:

ExperimentExecutionResult
-> ExperimentReceipt
-> reviewed EvidenceRecord
-> scoped HypothesisAssessment
-> immutable EvidenceLedgerRevision
-> AdaptiveFrontierState
-> next adaptive selection

The layer is deliberately non-authoritative:

- execution results contain measured facts, not claims
- receipts bind results to provenance
- only reviewed receipts become evidence
- hypothesis assessments are scoped to the tested experiment
- many-to-one outcome partitions remain unresolved rather than falsely selecting a hypothesis
- frontier revisions close completed experiments and are idempotent on replay
- adaptive priors are not rewritten because no empirical likelihood/noise model exists

Persistence and external execution remain adapters outside this layer.

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
