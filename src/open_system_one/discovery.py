from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FailureObservation:
    tags: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()
    evidence_gaps: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "tags", tuple(sorted(set(self.tags))))
        object.__setattr__(self, "evidence_refs", tuple(sorted(set(self.evidence_refs))))
        object.__setattr__(self, "evidence_gaps", tuple(sorted(set(self.evidence_gaps))))


@dataclass(frozen=True)
class FailureClass:
    key: str
    description: str
    trigger_tags: tuple[str, ...]
    scope: str = "research"


@dataclass(frozen=True)
class FailureMatch:
    failure_class: str
    matched_tags: tuple[str, ...]
    score: int


@dataclass(frozen=True)
class MechanismSpec:
    key: str
    operation: str
    implementation: str
    boundary: str


@dataclass(frozen=True)
class CompositeRecipe:
    key: str
    failure_classes: tuple[str, ...]
    mechanisms: tuple[str, ...]
    hypothesis: str
    predicted_effect: str
    kill_test: str
    evidence_required: tuple[str, ...]
    scope: str = "research"


@dataclass(frozen=True)
class DiscoveryCandidate:
    recipe: str
    failure_class: str
    mechanisms: tuple[str, ...]
    hypothesis: str
    predicted_effect: str
    kill_test: str
    evidence_required: tuple[str, ...]
    scope: str


@dataclass(frozen=True)
class CoordinatedPlan:
    failure_class: str
    recipes: tuple[str, ...]
    mechanisms: tuple[str, ...]
    hypotheses: tuple[str, ...]
    kill_tests: tuple[str, ...]
    evidence_required: tuple[str, ...]


@dataclass(frozen=True)
class MultiFailurePlan:
    failure_classes: tuple[str, ...]
    recipes: tuple[str, ...]
    mechanisms: tuple[str, ...]
    hypotheses: tuple[str, ...]
    kill_tests: tuple[str, ...]
    evidence_required: tuple[str, ...]


@dataclass(frozen=True)
class ExperimentDesign:
    key: str
    failure_classes: tuple[str, ...]
    recipe_keys: tuple[str, ...]
    mechanisms: tuple[str, ...]
    hypothesis: str
    intervention: str
    baseline: str
    control: str
    discriminator: str
    kill_test: str
    evidence_required: tuple[str, ...]
    cost: int
    scope: str = "research"


@dataclass(frozen=True)
class ExperimentSelection:
    experiment: str
    class_coverage: int
    evidence_gap_coverage: int
    cost: int
    reason: str


@dataclass(frozen=True)
class DiscoveryPlan:
    scope: str
    observation_tags: tuple[str, ...]
    matches: tuple[FailureMatch, ...]
    experiments: tuple[ExperimentSelection, ...]
    mechanisms: tuple[str, ...]
    hypotheses: tuple[str, ...]
    kill_tests: tuple[str, ...]
    evidence_required: tuple[str, ...]


FAILURE_CLASSES = (
    FailureClass(
        "candidate_interaction",
        "Candidate quality changes when other candidates are present.",
        ("candidate_set_changes_output", "competitor_effect", "context_dependent_score"),
    ),
    FailureClass(
        "retrieval_overload",
        "Too many candidates reach an expensive downstream scorer.",
        ("large_candidate_count", "retrieval_latency", "candidate_budget_exhausted"),
    ),
    FailureClass(
        "repeated_compute",
        "Equivalent deterministic work is recomputed across runs or stages.",
        ("same_input_repeated", "duplicate_work", "cache_miss"),
    ),
    FailureClass(
        "provenance_drift",
        "Equivalent artifacts do not retain stable identity or lineage.",
        ("hash_mismatch", "lineage_mismatch", "same_content_different_id"),
    ),
    FailureClass(
        "ordering_conflict",
        "Events, updates, or evidence arrive in conflicting temporal order.",
        ("reordered_events", "causal_inversion", "inconsistent_merge"),
    ),
    FailureClass(
        "composition_failure",
        "A multi-stage computation loses a required invariant at a stage boundary.",
        ("stage_boundary", "intermediate_loss", "hidden_failure"),
    ),
    FailureClass(
        "authority_boundary",
        "Inference output is being confused with permission or execution authority.",
        ("confidence_used_for_action", "missing_capability", "unauthorized_execution"),
        scope="control_plane",
    ),
)


MECHANISMS = (
    MechanismSpec("condition", "condition(score, context)", "conditional mixture / shared context", "inference"),
    MechanismSpec("relate", "relate(candidate, candidate)", "set-aware / relational scorer", "inference"),
    MechanismSpec("shortlist", "prune(candidates) before expensive scoring", "oracle or learned prefilter", "inference"),
    MechanismSpec("dynamic_score", "score(query, candidate_set)", "candidate_scores / adaptive scorer", "inference"),
    MechanismSpec("identify", "artifact -> canonical identity", "content_id", "control_plane"),
    MechanismSpec("cache", "identity -> reusable result", "memoize", "control_plane"),
    MechanismSpec("order", "event -> logical order", "LamportClock", "control_plane"),
    MechanismSpec("merge", "compatible state -> converged state", "GSet", "control_plane"),
    MechanismSpec("compose", "stage_1 -> stage_2 -> ...", "compose", "computation"),
    MechanismSpec("reify", "continuation -> explicit data", "ReifiedContinuation", "computation"),
    MechanismSpec("capability_gate", "decision -> externally authorized action", "CapabilityIssuer", "authority"),
)


RECIPES = (
    CompositeRecipe(
        "interaction_probe",
        ("candidate_interaction",),
        ("condition", "relate", "dynamic_score"),
        "If candidate interaction carries signal, conditioning or explicit relations should improve decisions when interaction is active.",
        "Interaction-aware scoring should beat or complement pairwise under matched parameter and training budgets while preserving identity/permutation semantics.",
        "Run matched interaction=0 and interaction>0 ablations against pairwise; reject if the gain disappears at interaction=0 or under hard negatives, or if permutation/identity invariants fail.",
        ("implementation_ref", "matched_baseline", "multiple_seeds", "raw_accuracy_and_brier", "failure_case"),
    ),
    CompositeRecipe(
        "retrieval_guard",
        ("retrieval_overload",),
        ("identify", "shortlist", "dynamic_score"),
        "Stable candidate identity plus an early gate can reduce downstream candidate work without silently removing the required candidate.",
        "Candidate computation falls while recall of the downstream-relevant candidate remains above the declared safety threshold.",
        "Measure recall@K before downstream scoring across seeds and hard negatives; reject if the safety recall target is missed or if identity is not preserved.",
        ("dataset_ref", "K_grid", "recall_at_K", "compute_measure", "failure_case"),
    ),
    CompositeRecipe(
        "deterministic_reuse",
        ("repeated_compute", "provenance_drift"),
        ("identify", "cache"),
        "Stable content identity should make deterministic repeated work reusable without conflating distinct artifacts.",
        "Equivalent artifacts share a cache key; changed content produces a different key; reuse does not change the returned value.",
        "Change one semantic input and require a cache miss; repeat the same input and require a single underlying computation.",
        ("content_fixtures", "cache_hit_measure", "mutation_kill_test"),
    ),
    CompositeRecipe(
        "ordered_merge",
        ("ordering_conflict", "provenance_drift"),
        ("identify", "order", "merge"),
        "Stable artifact identity plus logical ordering and convergent merge can preserve evidence across distributed or reordered updates.",
        "Equivalent merge inputs converge regardless of arrival order while provenance remains inspectable.",
        "Permute event arrival order and require identical final state; reject on lost identity or non-convergent state.",
        ("event_trace", "permutation_test", "final_state_digest"),
    ),
    CompositeRecipe(
        "composed_continuation",
        ("composition_failure",),
        ("compose", "reify"),
        "Making a multi-stage computation explicit and reified should expose stage-boundary failures instead of hiding them inside opaque control flow.",
        "The composed pipeline preserves intermediate identity and makes continuation state inspectable at failure boundaries.",
        "Inject a failing stage and require the failing boundary and continuation payload to be identifiable without changing successful outputs.",
        ("stage_fixture", "failure_injection", "output_equivalence"),
    ),
    CompositeRecipe(
        "authority_handoff",
        ("authority_boundary",),
        ("identify", "capability_gate"),
        "Inference artifacts can be bound to an externally issued capability without allowing probability or confidence to mint authority.",
        "The same decision artifact can be audited by identity while authorization remains independently verifiable and revocable by the capability layer.",
        "Attempt execution with a valid-looking decision but no capability, and with the wrong capability scope; both must fail outside inference.",
        ("decision_digest", "capability_scope_test", "negative_authorization"),
        scope="control_plane",
    ),
)


EXPERIMENTS = (
    ExperimentDesign(
        "interaction_probe",
        ("candidate_interaction",),
        ("interaction_probe",),
        ("condition", "relate", "dynamic_score"),
        "Candidate interaction carries decision-relevant information in the tested workload.",
        "Matched interaction=0 and active-interaction runs over the same tasks and candidate budgets.",
        "Pairwise scorer under the same encoder, parameter-count order, training budget, and K.",
        "Matched interaction=0 condition with the same encoder, K, and training budget.",
        "Interaction sensitivity: whether any gain appears only when interaction is activated.",
        "Reject if the effect disappears under matched controls, hard negatives, or permutation/identity tests.",
        ("implementation_ref", "matched_baseline", "multiple_seeds", "raw_accuracy_and_brier", "failure_case"),
        2,
    ),
    ExperimentDesign(
        "interaction_retrieval_guard",
        ("candidate_interaction", "retrieval_overload"),
        ("interaction_probe", "retrieval_guard"),
        ("identify", "shortlist", "dynamic_score", "condition", "relate"),
        "A safe retrieval gate can preserve the candidate-interaction signal while reducing expensive downstream candidate work.",
        "Compare full-candidate interaction-aware scoring with K-grid shortlist-then-rerank.",
        "Full candidate set plus pairwise baseline, with matched encoder and scoring budget.",
        "Full-candidate interaction-aware scorer with the same K values and encoder.",
        "Joint effect: whether pruning preserves interaction signal while reducing downstream work.",
        "Reject if shortlist recall misses the declared safety target or interaction gains disappear after pruning.",
        ("dataset_ref", "K_grid", "recall_at_K", "compute_measure", "raw_accuracy_and_brier"),
        3,
    ),
    ExperimentDesign(
        "shortlist_safety",
        ("retrieval_overload",),
        ("retrieval_guard",),
        ("identify", "shortlist", "dynamic_score"),
        "Early candidate pruning can reduce downstream work without removing the required candidate.",
        "Evaluate K-grid recall before the expensive scorer across ordinary and hard-negative candidate sets.",
        "Full-candidate scoring.",
        "Full-candidate scoring with no pruning.",
        "Retrieval safety: recall@K versus candidate work across ordinary and hard negatives.",
        "Reject if the declared recall threshold is missed or candidate identity is not preserved.",
        ("dataset_ref", "K_grid", "recall_at_K", "compute_measure", "failure_case"),
        1,
    ),
    ExperimentDesign(
        "artifact_reuse",
        ("repeated_compute", "provenance_drift"),
        ("deterministic_reuse",),
        ("identify", "cache"),
        "Stable artifact identity makes deterministic repeated work reusable without conflating distinct content.",
        "Repeat identical input, then mutate one semantic field and repeat.",
        "No-cache recomputation plus a changed-content control.",
        "Same-input repetition without mutation.",
        "Identity/cache discrimination: same content reuses; changed content does not.",
        "Reject on changed-content cache collision or a value mismatch after reuse.",
        ("content_fixtures", "cache_hit_measure", "mutation_kill_test"),
        1,
    ),
    ExperimentDesign(
        "evidence_flow_guard",
        ("repeated_compute", "provenance_drift", "ordering_conflict"),
        ("deterministic_reuse", "ordered_merge"),
        ("identify", "cache", "order", "merge"),
        "Identity, reuse, logical order, and convergent merge can preserve an evidence flow across repeated and reordered updates.",
        "Replay the same evidence events with repeated inputs and multiple arrival orders.",
        "Fresh recomputation in canonical order.",
        "Same evidence events replayed once in canonical arrival order.",
        "Evidence-flow invariance: final digest, reuse count, and order-independent convergence.",
        "Reject on cache collision, provenance loss, or order-dependent final state.",
        ("event_trace", "content_fixtures", "permutation_test", "final_state_digest"),
        3,
    ),
    ExperimentDesign(
        "continuation_failure_injection",
        ("composition_failure",),
        ("composed_continuation",),
        ("compose", "reify"),
        "Explicit stage composition and reification expose the exact failure boundary without altering successful outputs.",
        "Inject a controlled failing stage and inspect the reified continuation.",
        "Successful pipeline with the same stages and inputs.",
        "Failure localization: boundary identity and continuation payload.",
        "Failure localization must remain observable at the injected stage without changing successful semantics.",
        "Reject if the injected failure cannot be localized or if successful output semantics change.",
        ("stage_fixture", "failure_injection", "output_equivalence"),
        2,
    ),
    ExperimentDesign(
        "authority_handoff_negative",
        ("authority_boundary",),
        ("authority_handoff",),
        ("identify", "capability_gate"),
        "Decision artifacts can be audited by identity while authorization remains external to inference.",
        "Attempt execution with no capability and with wrong capability scope.",
        "Valid capability with the required scope.",
        "Authority separation: probability/confidence cannot mint permission.",
        "Authority separation: probability/confidence cannot mint permission.",
        "Reject if either unauthorized execution path succeeds inside or through inference.",
        ("decision_digest", "capability_scope_test", "negative_authorization"),
        1,
        scope="control_plane",
    ),
)


_FAILURES = {x.key: x for x in FAILURE_CLASSES}
_MECHS = {x.key: x for x in MECHANISMS}
_RECIPES = {x.key: x for x in RECIPES}
_EXPERIMENTS = {x.key: x for x in EXPERIMENTS}

if len(_FAILURES) != len(FAILURE_CLASSES):
    raise ValueError("duplicate failure class")
if len(_MECHS) != len(MECHANISMS):
    raise ValueError("duplicate mechanism")
if len(_RECIPES) != len(RECIPES):
    raise ValueError("duplicate recipe")
if len(_EXPERIMENTS) != len(EXPERIMENTS):
    raise ValueError("duplicate experiment")

for recipe in RECIPES:
    if any(key not in _FAILURES for key in recipe.failure_classes):
        raise ValueError(f"unknown failure class in {recipe.key}")
    if any(key not in _MECHS for key in recipe.mechanisms):
        raise ValueError(f"unknown mechanism in {recipe.key}")
    if recipe.scope == "research" and any(_MECHS[key].boundary == "authority" for key in recipe.mechanisms):
        raise ValueError(f"authority mechanism leaked into research recipe {recipe.key}")

for experiment in EXPERIMENTS:
    if any(key not in _FAILURES for key in experiment.failure_classes):
        raise ValueError(f"unknown failure class in {experiment.key}")
    if any(key not in _RECIPES for key in experiment.recipe_keys):
        raise ValueError(f"unknown recipe in {experiment.key}")
    if any(key not in _MECHS for key in experiment.mechanisms):
        raise ValueError(f"unknown mechanism in {experiment.key}")
    recipe_scopes = {_RECIPES[key].scope for key in experiment.recipe_keys}
    if recipe_scopes != {experiment.scope}:
        raise ValueError(f"experiment scope does not match recipes in {experiment.key}")


def propose(failure_class: str) -> tuple[DiscoveryCandidate, ...]:
    if failure_class not in _FAILURES:
        raise KeyError(failure_class)
    matches = [r for r in RECIPES if failure_class in r.failure_classes]
    matches.sort(key=lambda r: r.key)
    return tuple(
        DiscoveryCandidate(
            recipe=r.key,
            failure_class=failure_class,
            mechanisms=r.mechanisms,
            hypothesis=r.hypothesis,
            predicted_effect=r.predicted_effect,
            kill_test=r.kill_test,
            evidence_required=r.evidence_required,
            scope=r.scope,
        )
        for r in matches
    )


def coordinate(failure_class: str, recipe_keys: tuple[str, ...] | None = None) -> CoordinatedPlan:
    candidates = propose(failure_class)
    selected = tuple(recipe_keys) if recipe_keys is not None else tuple(c.recipe for c in candidates)
    if not selected:
        raise ValueError(f"no registered recipes for {failure_class}")
    lookup = {c.recipe: c for c in candidates}
    if any(key not in lookup for key in selected):
        raise ValueError("recipe is not valid for the requested failure class")

    mechanisms: list[str] = []
    hypotheses: list[str] = []
    kill_tests: list[str] = []
    evidence: list[str] = []
    for key in selected:
        c = lookup[key]
        for value in c.mechanisms:
            if value not in mechanisms:
                mechanisms.append(value)
        if c.hypothesis not in hypotheses:
            hypotheses.append(c.hypothesis)
        if c.kill_test not in kill_tests:
            kill_tests.append(c.kill_test)
        for value in c.evidence_required:
            if value not in evidence:
                evidence.append(value)

    return CoordinatedPlan(
        failure_class=failure_class,
        recipes=selected,
        mechanisms=tuple(mechanisms),
        hypotheses=tuple(hypotheses),
        kill_tests=tuple(kill_tests),
        evidence_required=tuple(evidence),
    )


def coordinate_failures(failure_classes: tuple[str, ...]) -> MultiFailurePlan:
    if not failure_classes:
        raise ValueError("at least one failure class is required")
    for failure_class in failure_classes:
        if failure_class not in _FAILURES:
            raise KeyError(failure_class)

    candidates = []
    seen_recipes: set[str] = set()
    for failure_class in failure_classes:
        for candidate in propose(failure_class):
            if candidate.recipe not in seen_recipes:
                candidates.append(candidate)
                seen_recipes.add(candidate.recipe)

    authority = [c for c in candidates if c.scope == "control_plane" and "capability_gate" in c.mechanisms]
    non_authority = [c for c in candidates if c not in authority]
    if authority and non_authority:
        raise ValueError("authority recipe must remain separate from inference/computation discovery")

    mechanisms: list[str] = []
    hypotheses: list[str] = []
    kill_tests: list[str] = []
    evidence: list[str] = []
    for candidate in sorted(candidates, key=lambda c: c.recipe):
        for value in candidate.mechanisms:
            if value not in mechanisms:
                mechanisms.append(value)
        if candidate.hypothesis not in hypotheses:
            hypotheses.append(candidate.hypothesis)
        if candidate.kill_test not in kill_tests:
            kill_tests.append(candidate.kill_test)
        for value in candidate.evidence_required:
            if value not in evidence:
                evidence.append(value)

    return MultiFailurePlan(
        failure_classes=tuple(failure_classes),
        recipes=tuple(sorted(seen_recipes)),
        mechanisms=tuple(mechanisms),
        hypotheses=tuple(hypotheses),
        kill_tests=tuple(kill_tests),
        evidence_required=tuple(evidence),
    )


def classify_failure(observation: FailureObservation) -> tuple[FailureMatch, ...]:
    tag_set = set(observation.tags)
    matches = []
    for failure in FAILURE_CLASSES:
        matched = tuple(sorted(tag_set.intersection(failure.trigger_tags)))
        if matched:
            matches.append(FailureMatch(failure.key, matched, len(matched)))
    return tuple(sorted(matches, key=lambda x: (-x.score, x.failure_class)))


def select_experiments(
    observation: FailureObservation,
    *,
    scope: str = "research",
    excluded: tuple[str, ...] = (),
    limit: int = 3,
) -> tuple[ExperimentSelection, ...]:
    if scope not in {"research", "control_plane"}:
        raise ValueError("scope must be research or control_plane")
    if limit < 1:
        raise ValueError("limit must be positive")

    matches = classify_failure(observation)
    target_classes = {
        match.failure_class
        for match in matches
        if _FAILURES[match.failure_class].scope == scope
    }
    excluded_set = set(excluded)
    gaps = set(observation.evidence_gaps)

    ranked: list[tuple[tuple[int, int, int, str], ExperimentDesign, int, int]] = []
    for experiment in EXPERIMENTS:
        if experiment.scope != scope or experiment.key in excluded_set:
            continue
        class_coverage = len(target_classes.intersection(experiment.failure_classes))
        if class_coverage == 0:
            continue
        gap_coverage = len(gaps.intersection(experiment.evidence_required))
        key = (-class_coverage, -gap_coverage, experiment.cost, experiment.key)
        ranked.append((key, experiment, class_coverage, gap_coverage))

    ranked.sort(key=lambda x: x[0])
    selected = ranked[:limit]
    return tuple(
        ExperimentSelection(
            experiment=experiment.key,
            class_coverage=class_coverage,
            evidence_gap_coverage=gap_coverage,
            cost=experiment.cost,
            reason=(
                f"covers {class_coverage} target failure class(es); "
                f"covers {gap_coverage} requested evidence gap(s); "
                f"declared cost={experiment.cost}"
            ),
        )
        for _, experiment, class_coverage, gap_coverage in selected
    )


def _dedupe(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    out: list[str] = []
    for value in values:
        if value not in out:
            out.append(value)
    return tuple(out)


def build_plan(
    observation: FailureObservation,
    *,
    scope: str = "research",
    excluded: tuple[str, ...] = (),
    limit: int = 3,
) -> DiscoveryPlan:
    matches = classify_failure(observation)
    selections = select_experiments(
        observation, scope=scope, excluded=excluded, limit=limit
    )

    mechanisms: list[str] = []
    hypotheses: list[str] = []
    kill_tests: list[str] = []
    evidence: list[str] = []
    for selection in selections:
        experiment = _EXPERIMENTS[selection.experiment]
        for value in experiment.mechanisms:
            if value not in mechanisms:
                mechanisms.append(value)
        if experiment.hypothesis not in hypotheses:
            hypotheses.append(experiment.hypothesis)
        if experiment.kill_test not in kill_tests:
            kill_tests.append(experiment.kill_test)
        for value in experiment.evidence_required:
            if value not in evidence:
                evidence.append(value)

    scoped_matches = tuple(
        match for match in matches if _FAILURES[match.failure_class].scope == scope
    )

    return DiscoveryPlan(
        scope=scope,
        observation_tags=observation.tags,
        matches=scoped_matches,
        experiments=selections,
        mechanisms=tuple(mechanisms),
        hypotheses=tuple(hypotheses),
        kill_tests=tuple(kill_tests),
        evidence_required=tuple(evidence),
    )


def build_plans(
    observation: FailureObservation,
    *,
    excluded: tuple[str, ...] = (),
    limit: int = 3,
) -> tuple[DiscoveryPlan, ...]:
    scopes = sorted(
        {
            _FAILURES[match.failure_class].scope
            for match in classify_failure(observation)
        }
    )
    return tuple(
        plan
        for scope in scopes
        for plan in (build_plan(observation, scope=scope, excluded=excluded, limit=limit),)
        if plan.experiments
    )


def catalog() -> dict[str, object]:
    return {
        "status": "NON_CANONICAL_RESEARCH_INFRASTRUCTURE",
        "classification_rule": (
            "A FailureObservation is classified by explicit trigger tags. "
            "Matches are ordered by number of matched tags, then class key; no "
            "semantic confidence is inferred."
        ),
        "selection_rule": (
            "Experiment selection is deterministic: maximize target failure-class "
            "coverage, then requested evidence-gap coverage, then minimize declared "
            "cost, then sort by experiment key."
        ),
        "authority_rule": (
            "Control-plane authority experiments are selected in a separate scope "
            "and never merged into research/inference plans."
        ),
        "failure_classes": [
            {
                "key": x.key,
                "description": x.description,
                "trigger_tags": list(x.trigger_tags),
                "scope": x.scope,
            }
            for x in FAILURE_CLASSES
        ],
        "mechanisms": [
            {
                "key": x.key,
                "operation": x.operation,
                "implementation": x.implementation,
                "boundary": x.boundary,
            }
            for x in MECHANISMS
        ],
        "recipes": [
            {
                "key": x.key,
                "failure_classes": list(x.failure_classes),
                "mechanisms": list(x.mechanisms),
                "hypothesis": x.hypothesis,
                "predicted_effect": x.predicted_effect,
                "kill_test": x.kill_test,
                "evidence_required": list(x.evidence_required),
                "scope": x.scope,
            }
            for x in RECIPES
        ],
        "experiments": [
            {
                "key": x.key,
                "failure_classes": list(x.failure_classes),
                "recipe_keys": list(x.recipe_keys),
                "mechanisms": list(x.mechanisms),
                "hypothesis": x.hypothesis,
                "intervention": x.intervention,
                "baseline": x.baseline,
                "control": x.control,
                "discriminator": x.discriminator,
                "kill_test": x.kill_test,
                "evidence_required": list(x.evidence_required),
                "cost": x.cost,
                "scope": x.scope,
            }
            for x in EXPERIMENTS
        ],
    }
