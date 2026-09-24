from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FailureClass:
    key: str
    description: str


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


FAILURE_CLASSES = (
    FailureClass("candidate_interaction", "Candidate quality changes when other candidates are present."),
    FailureClass("retrieval_overload", "Too many candidates reach an expensive downstream scorer."),
    FailureClass("repeated_compute", "Equivalent deterministic work is recomputed across runs or stages."),
    FailureClass("provenance_drift", "Equivalent artifacts do not retain stable identity or lineage."),
    FailureClass("ordering_conflict", "Events, updates, or evidence arrive in conflicting temporal order."),
    FailureClass("composition_failure", "A multi-stage computation loses a required invariant at a stage boundary."),
    FailureClass("authority_boundary", "Inference output is being confused with permission or execution authority."),
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

_FAILURES = {x.key: x for x in FAILURE_CLASSES}
_MECHS = {x.key: x for x in MECHANISMS}
_RECIPES = {x.key: x for x in RECIPES}

if len(_FAILURES) != len(FAILURE_CLASSES):
    raise ValueError("duplicate failure class")
if len(_MECHS) != len(MECHANISMS):
    raise ValueError("duplicate mechanism")
if len(_RECIPES) != len(RECIPES):
    raise ValueError("duplicate recipe")
for recipe in RECIPES:
    if any(key not in _FAILURES for key in recipe.failure_classes):
        raise ValueError(f"unknown failure class in {recipe.key}")
    if any(key not in _MECHS for key in recipe.mechanisms):
        raise ValueError(f"unknown mechanism in {recipe.key}")
    if recipe.scope == "research" and any(_MECHS[key].boundary == "authority" for key in recipe.mechanisms):
        raise ValueError(f"authority mechanism leaked into research recipe {recipe.key}")


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
        raise ValueError(f"no discovery recipes registered for {failure_class}")
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

def catalog() -> dict[str, object]:
    return {
        "status": "NON_CANONICAL_RESEARCH_INFRASTRUCTURE",
        "failure_classes": [
            {"key": x.key, "description": x.description} for x in FAILURE_CLASSES
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
        "coordination_rule": "Select compatible recipes across one or more failure classes, deduplicate mechanism stages, and keep every hypothesis/kill-test/evidence requirement explicit.",
        "authority_rule": "No inference recipe may contain the capability authority mechanism; authority_handoff remains a separate control-plane recipe.",
    }
