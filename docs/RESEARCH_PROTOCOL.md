# Research Protocol

Operating loop:

Observe -> Identify -> Evidence -> Interpret -> Decide -> Record -> Revalidate

Discovery extension:

Failure -> Mechanism classification -> Precomposed candidate recipes -> Discriminating test -> Evidence -> Frontier update -> Next failure

Adaptive extension:

Structured FailureEvidence -> explicit failure tags -> remaining hypothesis space -> expected information gain -> experiment selection -> experiment receipt -> frontier update

Every durable claim needs provenance, population/split, implementation reference, measured result, limits, and the next discriminating test.

## Status vocabulary

ESTABLISHED
EXPERIMENTALLY_SUPPORTED
USER_REPORTED
INFERENCE
HYPOTHESIS
CONTRADICTED
UNKNOWN
OPEN

Repetition does not upgrade a claim.

Negative results and killed ideas are recorded.

## Discovery rules

1. Generate mechanisms from observed failure structure, not only from named architectures.
2. Prefer precomposed recipes that expose several compatible mechanisms before selecting one implementation.
3. Every generated candidate must carry a hypothesis, predicted effect, kill test, and evidence requirements.
4. Candidate generation is deterministic; ordering is part of the research receipt.
5. Authority mechanisms remain outside inference discovery and require an explicit control-plane boundary.
6. A new candidate does not change contract semantics until it survives the normal acceptance boundary.
7. Failure classification is explicit and typed; free-form language is not treated as evidence or truth.
8. Experiment selection may use expected information gain only when the hypothesis prior and outcome partition are declared explicitly.
9. Expected information gain is a planning quantity, not an empirical probability of correctness.
10. Historical outcomes constrain repeat information only inside their declared experiment scope.
11. Discovery receipts record proposed paths, not experimental results.

## Adaptive Discovery

Structured FailureEvidence is converted into explicit trigger tags before the existing deterministic failure classifier is invoked.

A hypothesis space contains:
- a stable hypothesis key
- a declared research prior
- a status
- an experiment outcome partition

For an experiment E:

H_before = entropy of the active hypothesis priors.

H_after = expected posterior entropy after the declared outcome partition.

Expected information gain = H_before - H_after.

The implementation permits many hypotheses to map to the same outcome. Therefore a non-trivial experiment can have zero expected information gain when it cannot distinguish the remaining hypotheses.

A recorded historical outcome can make a repeat experiment have zero remaining information in the declared scope. This is a constraint on planning, not a claim that future experiments are unnecessary.

## Experiment contract

Each experiment specifies:

1. hypothesis
2. mechanism
3. implementation
4. baseline
5. activation condition
6. kill test
7. metrics
8. composition candidates
9. provenance

Adaptive designs additionally specify:

10. hypothesis keys
11. outcome partition
12. declared prior basis
13. historical outcome scope

## Closed-Loop Experiment Evidence

The closed-loop extension is:

ExecutionResult -> Receipt -> Review -> Evidence -> HypothesisAssessment -> LedgerRevision -> FrontierState -> Replan

Rules:

1. ExecutionResult is machine-produced result data only.
2. A receipt must carry complete provenance and a deterministic execution digest.
3. Only a reviewed receipt with passed kill/discriminator checks becomes ledger evidence.
4. Evidence identity is derived deterministically from the canonical receipt payload.
5. Hypothesis updates are scoped assessment events, not global truth-status mutation.
6. A many-to-one outcome partition must remain UNRESOLVED for compatible hypotheses.
7. A completed experiment is closed in the frontier and cannot be selected again in that state.
8. Replaying the same reviewed receipt is idempotent.
9. Adaptive priors are not rewritten by the closed loop.
10. Bayesian posterior updates require a separate reviewed likelihood/noise model.
11. Evidence-ledger revision is immutable data; persistence is an external storage concern.
12. Inference never acquires execution authority from an assessment or outcome.

## Kill criteria

- NaN or Inf propagation
- invalid probabilities
- question-ID collisions
- candidate identity loss
- permutation-induced semantic change
- test-to-train leakage
- calibration used as execution authority
- improvement that disappears under matched K or hard negatives

## Interpretation rule

A more complex scorer is not retained merely because its average is higher on one small sample. Keep the simplest mechanism that survives controlled intervention and replication.
