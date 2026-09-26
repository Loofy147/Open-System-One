# Closed-Loop Experiment Layer v0.1

This is NON-CANONICAL research infrastructure.

## Purpose

Close the executable research loop after an experiment has run:

ExecutionResult -> validated ExperimentReceipt -> reviewed EvidenceRecord -> scoped HypothesisAssessment events -> immutable EvidenceLedgerRevision -> updated AdaptiveFrontierState -> next adaptive planning against the updated frontier

The layer does not execute external experiments and does not persist state by itself. Persistence remains a control-plane/storage concern.

## Contract boundaries

### Execution result

An execution result contains only machine-produced result facts:

- experiment key
- observed outcome
- raw numeric metrics
- observed failure tags

It has no authority and no claim status.

### Experiment receipt

A receipt binds the execution result to provenance:

- experiment id
- code/source ref
- dataset/source ref
- population and split
- runtime and model
- configuration
- raw metrics
- observed failures
- interpretation
- receipt status
- next discriminating test
- kill-test result
- discriminator result
- scope
- execution digest

A receipt becomes ledger evidence only after review.

### Evidence

Evidence is a deterministic materialization of a reviewed receipt. Its identity is:

evidence:<sha256(receipt_canonical_payload)>

The evidence record preserves the execution and provenance facts. It does not itself become a claim.

### Hypothesis assessment

The experiment outcome is interpreted only through the experiment's declared deterministic outcome partition.

If exactly one hypothesis is compatible with the reviewed outcome:

- that hypothesis receives SUPPORTED for the tested scope
- incompatible hypotheses receive CONTRADICTED

If multiple hypotheses share the same outcome:

- all compatible hypotheses remain UNRESOLVED
- incompatible hypotheses receive CONTRADICTED

These are scoped assessment events. They do not mutate the global hypothesis prior or silently promote/demote a hypothesis across unrelated experiments.

### Frontier revision

A reviewed receipt closes the executed experiment in the immutable frontier state:

OPEN/HYPOTHESIS -> COMPLETED_CURRENT_SCOPE

The revision records:

- parent revision id
- evidence id
- experiment transition
- hypothesis assessments
- resulting frontier revision id

Applying the same reviewed receipt again is an IDEMPOTENT_REPLAY and does not duplicate evidence or assessments.

## Epistemic boundary

This layer deliberately does NOT perform Bayesian posterior updates.

The adaptive priors remain declared research weights until a reviewed likelihood/noise model exists.

Therefore:

- an assessment is not a posterior probability
- expected information gain remains a planning quantity
- evidence is not a claim
- a hypothesis assessment does not grant execution authority

## Replanning

select_adaptive_experiments(..., frontier=state) observes experiment closure from the frontier. A completed current-scope experiment is no longer eligible for reselection, while unrelated experiments remain selectable.

## Acceptance criteria

A closed-loop implementation is structurally valid only when:

1. execution parsing is strict
2. receipt provenance is complete
3. outcome belongs to the declared partition
4. kill and discriminator checks pass before review
5. evidence identity is deterministic
6. assessments are scoped to the exact receipt
7. many-to-one partitions never falsely identify a hypothesis
8. frontier updates are immutable
9. replay is idempotent
10. future planning reads the revised frontier
11. priors are not silently rewritten
12. authority remains outside inference

## Remaining debt

Automatic experiment execution, persistence adapters, empirical likelihood/noise models, and cross-experiment evidence synthesis remain OPEN.
