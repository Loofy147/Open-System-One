# Self-Conversion Primitive v0.1

Status: RESEARCH / OPEN

## Purpose

Test whether the model-plus-tool environment can convert an externally stated goal into a
verified external outcome, rather than merely generating plausible text.

The primitive under test is:

```
Goal
  -> World/constraint observation
  -> Candidate transition(s)
  -> Capability selection
  -> Execution
  -> External outcome
  -> Verification
  -> Evidence receipt
```

## Core object

A conversion attempt is represented as:

```
K = (G, W, C, X, O, V, E)
```

where:

- `G` = goal and acceptance condition.
- `W` = observed world state relevant to the goal.
- `C` = available capabilities/tools.
- `X` = executed transition sequence.
- `O` = observed external outcome.
- `V` = verification result.
- `E` = evidence/receipt sufficient to audit the attempt.

## Required properties

1. **Externality** — success must change or retrieve something outside the model's text stream.
2. **Verifiability** — the claimed outcome must have an independently inspectable receipt.
3. **Traceability** — each consequential action has a recorded tool/action reference.
4. **Constraint preservation** — user and environment constraints survive decomposition.
5. **Abstention** — the primitive may return OPEN/UNKNOWN when execution or verification is insufficient.
6. **No confidence substitution** — model confidence is never itself an acceptance condition.
7. **Idempotent intent where possible** — retries must not silently duplicate consequential effects.
8. **Capability portability** — the contract must not require a particular vendor, model, repository, or runtime.

## Minimal outcome states

- `UNRESOLVED` — goal not sufficiently specified or executable.
- `CANDIDATE` — a transition was identified but not executed.
- `EXECUTED` — an action ran, but verification is incomplete.
- `VERIFIED` — outcome satisfies the acceptance condition with evidence.
- `CONTRADICTED` — observed outcome conflicts with the expected transition.
- `BLOCKED` — capability, authority, or environment prevents execution.

## Important boundary

This primitive is **not** an autonomous economic agent, marketplace, or generalized AGI claim.
It is a testable substrate contract for converting intent into verified external outcomes.

## First falsification target

Determine whether adding explicit capability discovery + tool execution + post-action verification
produces a materially higher verified-outcome rate than model-only response generation on the same
goal set.

A result is not considered positive merely because the output is more detailed, more confident,
or more persuasive.

## Evidence requirement

Every benchmark case must record:

- exact goal input;
- environment/capability set;
- candidate transition;
- executed actions;
- external artifact or state change;
- verification method;
- final disposition;
- failure/rollback information where applicable.

