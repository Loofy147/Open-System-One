# Behavioral Transition Record Templates v0.3

Status: METHODOLOGY — OPEN / EXPERIMENTAL

## 1. TransitionTarget

```yaml
transition_id:
representation_version: bt-v0.3
world_reference:
  world_revision:
  observed_at:
  environment:
source_record_refs: []
observed_context:
pre_state:
trigger:
target_state:
desired_delta:
constraints: []
human_machine_boundary:
  machine_responsibility:
  human_responsibility:
  approval_required:
  recovery_boundary:
oracle:
consequence:
  absent:
  wrong:
  frequency:
  stakes:
  recoverability:
  reversibility:
current_transition:
automation_gap:
mechanism_candidates: []
counterfactual_baseline:
  A_current:
  B_best_no_build:
  C_intervention:
  observed_delta:
adoption_cost:
status:
decision:
evidence_refs: []
contradiction_refs: []
experiment_refs: []
artifact_refs: []
lineage_refs: []
next_discriminating_action:
epistemic:
  observed_context: DIRECT_OBSERVATION
  target_transition: HYPOTHESIS
  current_transition: UNKNOWN
  gap: UNKNOWN
  consequence: UNKNOWN
  mechanism: UNKNOWN
  actual_delta: UNKNOWN
  verification: UNKNOWN
```

## 2. MechanismCandidate

```yaml
mechanism_id:
transition_id:
type:
description:
expected_delta:
scope:
dependencies: []
setup_cost:
permission_cost:
migration_cost:
maintenance_cost:
failure_modes: []
reversibility:
prior_art_freshness:
source_refs: []
status:
```

## 3. Execution

```yaml
execution_id:
transition_id:
mechanism_id:
run_id:
world_revision:
pre_state_digest:
authorization:
approval:
impact_budget:
actual_post_state_digest:
actual_delta:
effect_status:
receipt_ref:
artifact_refs: []
```

## 4. TransitionVerification

```yaml
verification_id:
transition_id:
execution_id:
oracle_id:
oracle_version:
expected:
observed:
result:
coverage:
limitations: []
evidence_refs: []
artifact_refs: []
date:
```

## 5. RepresentationEvent

This records re-encoding, not a new experiment.

```yaml
representation_event_id:
source_snapshot_id:
source_record_refs: []
mapping_version:
mapping_digest:
target_representation: bt-v0.3
generated_at:
generator_revision:
field_provenance:
  field_name:
    class: COPIED | DERIVED | INFERRED | MISSING | CONFLICTED
    source_refs: []
    note:
excluded_fields: []
status_before:
status_after:
status_preserved: true
representation_digest:
determinism_check:
```

## 6. LineageEdge

```yaml
lineage_id:
from_id:
to_id:
relation:
scope:
created_at:
evidence_refs: []
```

Allowed relations include:

- DERIVED_FROM
- REPRESENTS
- SPLIT_FROM
- SAME_TARGET
- MECHANISM_FOR
- EXECUTED_AS
- VERIFIED_BY
- SUPPORTED_BY
- CONTRADICTS
- REVISED_BY

## 7. DecisionRevision

```yaml
decision_revision_id:
decision_id:
transition_id:
date:
previous_decision:
new_decision:
trigger_evidence: []
reason:
scope_change:
representation_change: false
```

A representation change alone must not generate a decision revision.

## 8. NegativeResult

```yaml
result_id:
transition_id:
stage:
hypothesis:
test:
oracle:
result:
kill_reason:
scope:
evidence_refs: []
experiment_refs: []
artifact_refs: []
```

## 9. Re-encoding Rules

1. Never overwrite the source record.
2. Never promote epistemic status by rewording.
3. Every inferred field must be marked INFERRED.
4. Missing source evidence stays MISSING or UNKNOWN.
5. Conflicting sources stay CONFLICTED until separately resolved.
6. A deterministic regeneration must reproduce the same canonical digest from the same source snapshot and mapping version.
7. A new source snapshot creates a new representation event.
8. Re-encoding is not verification.
9. Re-encoding is not evidence.
10. A kill decision is preserved with its original scope and incumbent set.

## 10. Method Evaluation

```yaml
evaluation_id:
cycle_id:
source_snapshot_id:
transition_count:
fully_represented:
partially_represented:
unmapped:
inferred_fields:
conflicts_detected:
status_upgrades: 0
determinism_checks:
provenance_complete:
transition_distinctions_exposed:
method_lessons: []
method_revision:
```
