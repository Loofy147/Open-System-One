# Burden Record Templates v0.4

## BurdenRecord

```yaml
burden_id:
source_kind: REPO | CONVERSATION | EXTERNAL | GENERATED
source_refs: []
world_reference:
scope:
statement:
burden_class:
observed_state:
target_transition:
consequence:
  absent:
  wrong:
  frequency:
  stakes:
  recoverability:
  reversibility:
best_existing_mechanism:
counterfactual:
  A_current:
  B_best_no_build:
  C_intervention:
kill_test:
oracle:
disposition: KILL | MERGE | ABSORB | AUTOMATE | BOUND | PROVE | DEFER | REBASE
resolution_condition:
wake_condition:
review_trigger:
owner:
status:
evidence_refs: []
experiment_refs: []
artifact_refs: []
contradiction_refs: []
lineage_refs: []
epistemic:
next_discriminating_action:
```

## SweepRecord

```yaml
sweep_id:
date:
scope:
source_snapshots: []
collector_revision:
burdens_discovered:
burdens_classified:
unclassified_count:
ownerless_actionless_count:
silent_defer_count:
coverage_gaps:
determinism:
decision:
next_sweep_trigger:
```

## ForcedFilterResult

```yaml
burden_id:
stage:
input_state:
observation:
decision:
reason:
evidence_refs: []
next_action:
```

## Invariants

A valid sweep requires:

```text
unclassified_count = 0
ownerless_actionless_count = 0
silent_defer_count = 0
status_upgrade_by_reencoding = 0
```

No burden may reach RESOLVED, ABSORBED, or AUTOMATED solely because a document was rewritten.

No KILLED burden may reopen without:
- new evidence;
- changed scope;
- changed world/revision;
- or a contradiction against the original kill basis.
