# Adaptive Discovery v0.1

<!-- GENERATED FILE: scripts/build_adaptive_discovery_docs.py -->

This is NON-CANONICAL research infrastructure.

## Purpose

Convert structured evidence into failure classes, condition the unresolved planning space only on explicitly applicable recorded outcomes, and select the next experiment by explicit expected entropy reduction.

## Rules

**Classification:** Structured FailureEvidence is reduced to explicit trigger tags, then classified with the existing deterministic failure registry. No free-form language is treated as truth.

**Information gain:** Expected information gain is Shannon entropy reduction under declared research priors and deterministic outcome partitions. These priors are bookkeeping weights, not empirical probabilities.

**History:** A historical outcome constrains a current experiment only when the record explicitly declares applies_to_current_design=True. Otherwise it remains related evidence and does not alter current priors.

**Selection:** Eligibility requires every failure class declared by an experiment to be present in the observation. Ordering is target failure-class coverage, evidence-gap coverage, expected information gain, declared cost, stable experiment key.

Priors are research bookkeeping, not empirical probabilities or truth confidence.

## Hypotheses

| Key | Prior | Status | Scope | Description |
|---|---:|---|---|---|
| interaction_contextual | 0.35 | OPEN | research | Interaction helps only in regimes where candidate dependency is active. |
| interaction_unstable | 0.45 | OPEN | research | Interaction effects vary across tasks or regimes and do not support a universal rule. |
| interaction_absent | 0.2 | OPEN | research | Candidate interaction adds no decision-relevant information in the tested scope. |
| learned_shortlist_safe | 0.5 | OPEN | research | A learned shortlist preserves required-candidate recall in the target workload. |
| learned_shortlist_unsafe | 0.5 | OPEN | research | A learned shortlist can remove the required candidate in the target workload. |
| reuse_identity_valid | 0.5 | OPEN | research | Stable identity supports deterministic reuse without collisions. |
| reuse_identity_invalid | 0.5 | OPEN | research | Identity reuse can collide or change returned semantics. |
| merge_convergent | 0.5 | OPEN | research | Evidence state converges across reordered compatible updates. |
| merge_nonconvergent | 0.5 | OPEN | research | Evidence state can depend on arrival order. |
| continuation_visible | 0.5 | OPEN | research | Reification exposes stage-boundary failures without changing successful semantics. |
| continuation_opaque | 0.5 | OPEN | research | Reification does not reliably expose stage-boundary failures. |
| authority_external | 0.5 | OPEN | control_plane | Authorization remains external to inference. |
| authority_minted | 0.5 | OPEN | control_plane | Inference can incorrectly mint execution authority. |
| compound_signal_safe | 0.25 | OPEN | research | Interaction signal exists and shortlist pruning preserves it. |
| compound_signal_unsafe | 0.25 | OPEN | research | Interaction signal exists but shortlist pruning removes required signal. |
| compound_no_signal_safe | 0.25 | OPEN | research | Interaction signal is absent and shortlist pruning remains safe. |
| compound_no_signal_unsafe | 0.25 | OPEN | research | Interaction signal is absent but shortlist pruning is unsafe. |

## Historical outcomes

| Experiment | Outcome | Evidence ref | Scope |
|---|---|---|---|
| interaction_probe | mixed_gain | research/receipts/v03-results.md | research |

## Adaptive experiments

| Experiment | Failure classes | Mechanisms | Cost | Expected IG (bits) | Historical |
|---|---|---|---:|---:|---|
| interaction_probe | candidate_interaction | condition -> relate -> dynamic_score | 2 | 0.000000 | mixed_gain |
| interaction_regime_map | candidate_interaction | condition -> relate -> dynamic_score | 2 | 1.512888 | unobserved |
| interaction_retrieval_guard | candidate_interaction, retrieval_overload | identify -> shortlist -> dynamic_score -> condition -> relate | 3 | 2.000000 | unobserved |
| shortlist_safety | retrieval_overload | identify -> shortlist -> dynamic_score | 1 | 1.000000 | unobserved |
| learned_shortlist_transfer | retrieval_overload | identify -> shortlist -> dynamic_score | 2 | 1.000000 | unobserved |
| artifact_reuse | repeated_compute, provenance_drift | identify -> cache | 1 | 1.000000 | unobserved |
| evidence_flow_guard | repeated_compute, provenance_drift, ordering_conflict | identify -> cache -> order -> merge | 3 | 1.000000 | unobserved |
| continuation_failure_injection | composition_failure | compose -> reify | 2 | 1.000000 | unobserved |
| authority_handoff_negative | authority_boundary | identify -> capability_gate | 1 | 1.000000 | unobserved |

## Deterministic examples

- A candidate-interaction observation does not reselect interaction_probe after the recorded mixed_gain result; interaction_regime_map is eligible and has expected IG 1.512888 bits.
- A combined candidate-interaction + candidate-overload observation can select interaction_retrieval_guard, which covers two failure classes and has expected IG 2.000000 bits under its declared four-state hypothesis partition.

## Boundary

Control-plane authority experiments are selected in a separate scope and never merged into research/inference plans.

Discovery planning is a hypothesis generator and experiment planner. It is not experimental evidence, and it does not execute external side effects.
