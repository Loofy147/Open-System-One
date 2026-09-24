# Discovery Frontier v0.1

<!-- GENERATED FILE: scripts/build_discovery_docs.py -->

This is research infrastructure, not canonical decision-contract semantics.
Generated classifications are tag-based observations; generated experiments remain HYPOTHESIS until a provenance-complete receipt changes their status.

## Classification rule

A FailureObservation is classified by explicit trigger tags. Matches are ordered by number of matched tags, then class key; no semantic confidence is inferred.

## Selection rule

Experiment selection is deterministic: maximize target failure-class coverage, then requested evidence-gap coverage, then minimize declared cost, then sort by experiment key.

## Failure classes

| Key | Scope | Trigger tags | Description |
|---|---|---|---|
| candidate_interaction | research | candidate_set_changes_output, competitor_effect, context_dependent_score | Candidate quality changes when other candidates are present. |
| retrieval_overload | research | large_candidate_count, retrieval_latency, candidate_budget_exhausted | Too many candidates reach an expensive downstream scorer. |
| repeated_compute | research | same_input_repeated, duplicate_work, cache_miss | Equivalent deterministic work is recomputed across runs or stages. |
| provenance_drift | research | hash_mismatch, lineage_mismatch, same_content_different_id | Equivalent artifacts do not retain stable identity or lineage. |
| ordering_conflict | research | reordered_events, causal_inversion, inconsistent_merge | Events, updates, or evidence arrive in conflicting temporal order. |
| composition_failure | research | stage_boundary, intermediate_loss, hidden_failure | A multi-stage computation loses a required invariant at a stage boundary. |
| authority_boundary | control_plane | confidence_used_for_action, missing_capability, unauthorized_execution | Inference output is being confused with permission or execution authority. |

## Mechanisms

| Key | Operation | Implementation | Boundary |
|---|---|---|---|
| condition | condition(score, context) | conditional mixture / shared context | inference |
| relate | relate(candidate, candidate) | set-aware / relational scorer | inference |
| shortlist | prune(candidates) before expensive scoring | oracle or learned prefilter | inference |
| dynamic_score | score(query, candidate_set) | candidate_scores / adaptive scorer | inference |
| identify | artifact -> canonical identity | content_id | control_plane |
| cache | identity -> reusable result | memoize | control_plane |
| order | event -> logical order | LamportClock | control_plane |
| merge | compatible state -> converged state | GSet | control_plane |
| compose | stage_1 -> stage_2 -> ... | compose | computation |
| reify | continuation -> explicit data | ReifiedContinuation | computation |
| capability_gate | decision -> externally authorized action | CapabilityIssuer | authority |

## Precomposed recipes

| Recipe | Trigger | Mechanisms | Scope |
|---|---|---|---|
| interaction_probe | candidate_interaction | condition -> relate -> dynamic_score | research |
| retrieval_guard | retrieval_overload | identify -> shortlist -> dynamic_score | research |
| deterministic_reuse | repeated_compute, provenance_drift | identify -> cache | research |
| ordered_merge | ordering_conflict, provenance_drift | identify -> order -> merge | research |
| composed_continuation | composition_failure | compose -> reify | research |
| authority_handoff | authority_boundary | identify -> capability_gate | control_plane |

## Experiment designs

| Experiment | Trigger | Recipes | Mechanisms | Cost | Scope |
|---|---|---|---|---:|---|
| interaction_probe | candidate_interaction | interaction_probe | condition -> relate -> dynamic_score | 2 | research |
| interaction_retrieval_guard | candidate_interaction, retrieval_overload | interaction_probe, retrieval_guard | identify -> shortlist -> dynamic_score -> condition -> relate | 3 | research |
| shortlist_safety | retrieval_overload | retrieval_guard | identify -> shortlist -> dynamic_score | 1 | research |
| artifact_reuse | repeated_compute, provenance_drift | deterministic_reuse | identify -> cache | 1 | research |
| evidence_flow_guard | repeated_compute, provenance_drift, ordering_conflict | deterministic_reuse, ordered_merge | identify -> cache -> order -> merge | 3 | research |
| continuation_failure_injection | composition_failure | composed_continuation | compose -> reify | 2 | research |
| authority_handoff_negative | authority_boundary | authority_handoff | identify -> capability_gate | 1 | control_plane |

## Experiment details

### interaction_probe

**Hypothesis:** Candidate interaction carries decision-relevant information in the tested workload.

**Intervention:** Matched interaction=0 and active-interaction runs over the same tasks and candidate budgets.

**Baseline:** Pairwise scorer under the same encoder, parameter-count order, training budget, and K.

**Control:** Matched interaction=0 condition with the same encoder, K, and training budget.

**Discriminator:** Interaction sensitivity: whether any gain appears only when interaction is activated.

**Kill test:** Reject if the effect disappears under matched controls, hard negatives, or permutation/identity tests.

**Evidence required:** implementation_ref, matched_baseline, multiple_seeds, raw_accuracy_and_brier, failure_case

### interaction_retrieval_guard

**Hypothesis:** A safe retrieval gate can preserve the candidate-interaction signal while reducing expensive downstream candidate work.

**Intervention:** Compare full-candidate interaction-aware scoring with K-grid shortlist-then-rerank.

**Baseline:** Full candidate set plus pairwise baseline, with matched encoder and scoring budget.

**Control:** Full-candidate interaction-aware scorer with the same K values and encoder.

**Discriminator:** Joint effect: whether pruning preserves interaction signal while reducing downstream work.

**Kill test:** Reject if shortlist recall misses the declared safety target or interaction gains disappear after pruning.

**Evidence required:** dataset_ref, K_grid, recall_at_K, compute_measure, raw_accuracy_and_brier

### shortlist_safety

**Hypothesis:** Early candidate pruning can reduce downstream work without removing the required candidate.

**Intervention:** Evaluate K-grid recall before the expensive scorer across ordinary and hard-negative candidate sets.

**Baseline:** Full-candidate scoring.

**Control:** Full-candidate scoring with no pruning.

**Discriminator:** Retrieval safety: recall@K versus candidate work across ordinary and hard negatives.

**Kill test:** Reject if the declared recall threshold is missed or candidate identity is not preserved.

**Evidence required:** dataset_ref, K_grid, recall_at_K, compute_measure, failure_case

### artifact_reuse

**Hypothesis:** Stable artifact identity makes deterministic repeated work reusable without conflating distinct content.

**Intervention:** Repeat identical input, then mutate one semantic field and repeat.

**Baseline:** No-cache recomputation plus a changed-content control.

**Control:** Same-input repetition without mutation.

**Discriminator:** Identity/cache discrimination: same content reuses; changed content does not.

**Kill test:** Reject on changed-content cache collision or a value mismatch after reuse.

**Evidence required:** content_fixtures, cache_hit_measure, mutation_kill_test

### evidence_flow_guard

**Hypothesis:** Identity, reuse, logical order, and convergent merge can preserve an evidence flow across repeated and reordered updates.

**Intervention:** Replay the same evidence events with repeated inputs and multiple arrival orders.

**Baseline:** Fresh recomputation in canonical order.

**Control:** Same evidence events replayed once in canonical arrival order.

**Discriminator:** Evidence-flow invariance: final digest, reuse count, and order-independent convergence.

**Kill test:** Reject on cache collision, provenance loss, or order-dependent final state.

**Evidence required:** event_trace, content_fixtures, permutation_test, final_state_digest

### continuation_failure_injection

**Hypothesis:** Explicit stage composition and reification expose the exact failure boundary without altering successful outputs.

**Intervention:** Inject a controlled failing stage and inspect the reified continuation.

**Baseline:** Successful pipeline with the same stages and inputs.

**Control:** Failure localization: boundary identity and continuation payload.

**Discriminator:** Failure localization: boundary identity and continuation payload.

**Kill test:** Reject if the injected failure cannot be localized or if successful output semantics change.

**Evidence required:** stage_fixture, failure_injection, output_equivalence

### authority_handoff_negative

**Hypothesis:** Decision artifacts can be audited by identity while authorization remains external to inference.

**Intervention:** Attempt execution with no capability and with wrong capability scope.

**Baseline:** Valid capability with the required scope.

**Control:** Authority separation: probability/confidence cannot mint permission.

**Discriminator:** Authority separation: probability/confidence cannot mint permission.

**Kill test:** Reject if either unauthorized execution path succeeds inside or through inference.

**Evidence required:** decision_digest, capability_scope_test, negative_authorization

## Authority boundary

Control-plane authority experiments are selected in a separate scope and never merged into research/inference plans.

The classifier and selector are deterministic coordination aids. They do not infer truth from language by themselves, and they do not mint execution authority.

