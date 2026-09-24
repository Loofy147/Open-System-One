# Research Protocol

Operating loop:

Observe -> Identify -> Evidence -> Interpret -> Decide -> Record -> Revalidate

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
