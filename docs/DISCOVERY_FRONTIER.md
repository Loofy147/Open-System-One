# Discovery Frontier v0.1

<!-- GENERATED FILE: scripts/build_discovery_docs.py -->

This is research infrastructure, not canonical decision-contract semantics.
Every generated candidate remains a HYPOTHESIS until a provenance-complete experiment receipt changes its status.

## Failure classes

| Key | Description |
|---|---|
| candidate_interaction | Candidate quality changes when other candidates are present. |
| retrieval_overload | Too many candidates reach an expensive downstream scorer. |
| repeated_compute | Equivalent deterministic work is recomputed across runs or stages. |
| provenance_drift | Equivalent artifacts do not retain stable identity or lineage. |
| ordering_conflict | Events, updates, or evidence arrive in conflicting temporal order. |
| composition_failure | A multi-stage computation loses a required invariant at a stage boundary. |
| authority_boundary | Inference output is being confused with permission or execution authority. |

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

| Recipe | Trigger | Mechanisms | Predicted effect |
|---|---|---|---|
| interaction_probe | candidate_interaction | condition -> relate -> dynamic_score | Interaction-aware scoring should beat or complement pairwise under matched parameter and training budgets while preserving identity/permutation semantics. |
| retrieval_guard | retrieval_overload | identify -> shortlist -> dynamic_score | Candidate computation falls while recall of the downstream-relevant candidate remains above the declared safety threshold. |
| deterministic_reuse | repeated_compute, provenance_drift | identify -> cache | Equivalent artifacts share a cache key; changed content produces a different key; reuse does not change the returned value. |
| ordered_merge | ordering_conflict, provenance_drift | identify -> order -> merge | Equivalent merge inputs converge regardless of arrival order while provenance remains inspectable. |
| composed_continuation | composition_failure | compose -> reify | The composed pipeline preserves intermediate identity and makes continuation state inspectable at failure boundaries. |
| authority_handoff | authority_boundary | identify -> capability_gate | The same decision artifact can be audited by identity while authorization remains independently verifiable and revocable by the capability layer. |

## Kill tests and evidence

### interaction_probe

**Hypothesis:** If candidate interaction carries signal, conditioning or explicit relations should improve decisions when interaction is active.

**Kill test:** Run matched interaction=0 and interaction>0 ablations against pairwise; reject if the gain disappears at interaction=0 or under hard negatives, or if permutation/identity invariants fail.

**Evidence required:** implementation_ref, matched_baseline, multiple_seeds, raw_accuracy_and_brier, failure_case

### retrieval_guard

**Hypothesis:** Stable candidate identity plus an early gate can reduce downstream candidate work without silently removing the required candidate.

**Kill test:** Measure recall@K before downstream scoring across seeds and hard negatives; reject if the safety recall target is missed or if identity is not preserved.

**Evidence required:** dataset_ref, K_grid, recall_at_K, compute_measure, failure_case

### deterministic_reuse

**Hypothesis:** Stable content identity should make deterministic repeated work reusable without conflating distinct artifacts.

**Kill test:** Change one semantic input and require a cache miss; repeat the same input and require a single underlying computation.

**Evidence required:** content_fixtures, cache_hit_measure, mutation_kill_test

### ordered_merge

**Hypothesis:** Stable artifact identity plus logical ordering and convergent merge can preserve evidence across distributed or reordered updates.

**Kill test:** Permute event arrival order and require identical final state; reject on lost identity or non-convergent state.

**Evidence required:** event_trace, permutation_test, final_state_digest

### composed_continuation

**Hypothesis:** Making a multi-stage computation explicit and reified should expose stage-boundary failures instead of hiding them inside opaque control flow.

**Kill test:** Inject a failing stage and require the failing boundary and continuation payload to be identifiable without changing successful outputs.

**Evidence required:** stage_fixture, failure_injection, output_equivalence

### authority_handoff

**Hypothesis:** Inference artifacts can be bound to an externally issued capability without allowing probability or confidence to mint authority.

**Kill test:** Attempt execution with a valid-looking decision but no capability, and with the wrong capability scope; both must fail outside inference.

**Evidence required:** decision_digest, capability_scope_test, negative_authorization

## Coordination

Select compatible recipes across one or more failure classes, deduplicate mechanism stages, and keep every hypothesis/kill-test/evidence requirement explicit.

No inference recipe may contain the capability authority mechanism; authority_handoff remains a separate control-plane recipe.

The generator is deliberately deterministic: the same registered failure class yields the same candidate set and the same coordination order.

