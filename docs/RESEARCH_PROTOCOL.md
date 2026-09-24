# Research Protocol

Operating loop:

Observe -> Identify -> Evidence -> Interpret -> Decide -> Record -> Revalidate

Discovery extension:

Failure -> Mechanism classification -> Precomposed candidate recipes -> Discriminating test -> Evidence -> Frontier update -> Next failure

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
