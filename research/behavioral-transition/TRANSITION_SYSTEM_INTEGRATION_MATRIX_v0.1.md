# Transition-Centered System Integration Matrix v0.1

Date: 2026-10-02
Status: RESEARCH INTEGRATION / OPEN

This matrix defines how the transition-centered representation relates to the current Open-System-One research surfaces.

| Surface | Primary transition | Role | Evidence boundary |
|---|---|---|---|
| Behavioral Transition Protocol | observed state -> target state | common ontology | methodology only until experiments support it |
| Opportunity Protocol v0.2 | workflow -> candidate intervention | predecessor discovery method | historical method; do not overwrite |
| Gap Engine | observations -> fitted rate -> gap -> mechanism plan | quantitative transition planner | simulation-supported; real-world UNKNOWN |
| Capability Kernel | requested transition -> authorized execution | authority boundary | experimentally supported only within recorded proof limits |
| Direct Impact Guard | mutation -> bounded state delta | impact boundary | experimentally supported only within recorded proof limits |
| Durable Run | attempt -> stable transition identity -> replay/reconciliation | durability boundary | experimentally supported within M0 scope |
| Android UNKNOWN research | external effect? -> UNKNOWN -> reconciled effect | unresolved-effect boundary | research frontier |
| Machine research | research state -> experimental transition -> verified result | scientific/research workflow | research evidence, not product demand |
| Product hypotheses | real workflow -> measurable target transition | external opportunity hypothesis | requires independent external evidence |

## Canonical lifecycle

World@revision
-> RawObservationSet
-> TransitionTarget
-> MechanismSet
-> AuthorizedExecution
-> BoundedImpact
-> ObservedEffect
-> Verification
-> Evidence
-> Claim
-> Decision
-> DecisionRevision

## Non-equivalences

Execution != observed outcome
Observed outcome != verified outcome
Verified outcome != market demand
Mechanism success != opportunity success
Representation change != new evidence
Historical applicability != current authority

## Required provenance

Every transition-bearing artifact should retain:

- source snapshot;
- source record refs;
- representation version;
- mapping version;
- code revision;
- oracle version;
- world revision;
- input/spec digest;
- output/result digest;
- decision revision.

## Regeneration rule

A projection can be regenerated from immutable source records.

The generator must emit:

- COPIED fields;
- DERIVED fields;
- INFERRED fields;
- MISSING fields;
- CONFLICTED fields.

No regeneration step may silently upgrade epistemic state.

## Current methodological status

The transition-centered model is OPEN / EXPERIMENTAL.

The current external opportunity decision remains:

NO_CONFIRMED_PRODUCT_OPPORTUNITY

No mechanism is BUILD_ALLOWED by virtue of this integration matrix.

## Next discriminating tests

1. Reproduce Gap Engine selftest from a pinned commit.
2. Run independent generator family.
3. Complete deterministic v0.2 -> v0.3 representation replay.
4. Re-run the C1 and C2 incumbent-only kill experiments under the transition representation.
5. Replay one real-world transition with a no-build baseline.
