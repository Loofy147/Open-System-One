# Experimental Opportunity Record Templates v0.2

## Problem Candidate

```yaml
candidate_id:
problem_statement:
affected_user_context:
discovery_date:
sources: []
current_solutions: []
workarounds: []
residual_pain:
gap_statement:
action_delta:
kill_tests: []
status:
decision:
evidence_refs: []
contradiction_refs: []
experiment_refs: []
artifact_refs: []
next_discriminating_action:
methods:
  discovery_method:
  search_method:
  competitor_search_method:
  kill_method:
  prototype_method:
  verification_method:
  oracle_method:
  reassessment_method:
```

## Evidence

```yaml
evidence_id:
source:
source_type:
retrieved_or_executed_at:
scope:
claim_supported:
claim_not_supported:
limitations:
artifact_ref:
```

## Experiment

```yaml
experiment_id:
method:
inputs:
environment:
command_or_procedure:
expected_observation:
oracle:
actual_result:
artifacts: []
date:
revision:
status:
```

## Contradiction

```yaml
contradiction_id:
claim:
previous_state:
new_observation:
conflicting_evidence: []
scope:
resolution:
resolution_status:
```

## Decision

```yaml
decision_id:
decision:
date:
based_on: []
rejected_alternatives: []
known_uncertainties: []
next_discriminating_action:
```

## DecisionRevision

```yaml
decision_revision_id:
decision_id:
date:
previous_decision:
new_decision:
trigger_evidence: []
reason:
```

## Negative Result

```yaml
result_id:
candidate_id:
stage:
hypothesis:
test:
result:
kill_reason:
evidence_refs: []
experiment_refs: []
artifact_refs: []
```

## Method Evaluation

```yaml
evaluation_id:
cycle_id:
candidates:
killed_before_build:
mvp_survivors:
action_changing_mvps:
premature_build_rate:
false_survival_rate:
oracle_failure_rate:
competitor_miss_rate:
post_build_kill_rate:
action_delta_rate:
method_lessons: []
method_revision:
```
