from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Mapping

from .discovery import FailureObservation, FAILURE_CLASSES, classify_failure


@dataclass(frozen=True)
class FailureEvidence:
    candidate_set_changes_output: bool = False
    competitor_effect: bool = False
    context_dependent_score: bool = False
    candidate_count: int | None = None
    candidate_budget: int | None = None
    retrieval_latency_ms: float | None = None
    retrieval_latency_budget_ms: float | None = None
    same_input_repeated: bool = False
    duplicate_work: bool = False
    cache_miss: bool = False
    hash_mismatch: bool = False
    lineage_mismatch: bool = False
    same_content_different_id: bool = False
    reordered_events: bool = False
    causal_inversion: bool = False
    inconsistent_merge: bool = False
    stage_boundary: bool = False
    intermediate_loss: bool = False
    hidden_failure: bool = False
    confidence_used_for_action: bool = False
    missing_capability: bool = False
    unauthorized_execution: bool = False
    evidence_refs: tuple[str, ...] = ()
    evidence_gaps: tuple[str, ...] = ()


def observation_from_evidence(evidence: FailureEvidence) -> FailureObservation:
    tags: list[str] = []
    direct = (
        ("candidate_set_changes_output", evidence.candidate_set_changes_output),
        ("competitor_effect", evidence.competitor_effect),
        ("context_dependent_score", evidence.context_dependent_score),
        ("same_input_repeated", evidence.same_input_repeated),
        ("duplicate_work", evidence.duplicate_work),
        ("cache_miss", evidence.cache_miss),
        ("hash_mismatch", evidence.hash_mismatch),
        ("lineage_mismatch", evidence.lineage_mismatch),
        ("same_content_different_id", evidence.same_content_different_id),
        ("reordered_events", evidence.reordered_events),
        ("causal_inversion", evidence.causal_inversion),
        ("inconsistent_merge", evidence.inconsistent_merge),
        ("stage_boundary", evidence.stage_boundary),
        ("intermediate_loss", evidence.intermediate_loss),
        ("hidden_failure", evidence.hidden_failure),
        ("confidence_used_for_action", evidence.confidence_used_for_action),
        ("missing_capability", evidence.missing_capability),
        ("unauthorized_execution", evidence.unauthorized_execution),
    )
    tags.extend(key for key, active in direct if active)
    if (
        evidence.candidate_count is not None
        and evidence.candidate_budget is not None
        and evidence.candidate_count > evidence.candidate_budget
    ):
        tags.extend(("large_candidate_count", "candidate_budget_exhausted"))
    if (
        evidence.retrieval_latency_ms is not None
        and evidence.retrieval_latency_budget_ms is not None
        and evidence.retrieval_latency_ms > evidence.retrieval_latency_budget_ms
    ):
        tags.append("retrieval_latency")
    return FailureObservation(
        tags=tuple(tags),
        evidence_refs=evidence.evidence_refs,
        evidence_gaps=evidence.evidence_gaps,
    )


@dataclass(frozen=True)
class HypothesisState:
    key: str
    description: str
    prior: float
    status: str
    scope: str = "research"


@dataclass(frozen=True)
class HistoricalOutcome:
    experiment: str
    outcome: str
    evidence_ref: str
    applies_to_current_design: bool = False
    scope: str = "research"


@dataclass(frozen=True)
class AdaptiveExperiment:
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
    hypothesis_keys: tuple[str, ...]
    outcome_partition: tuple[tuple[str, str], ...]
    status: str = "OPEN"
    scope: str = "research"


@dataclass(frozen=True)
class AdaptiveSelection:
    experiment: str
    class_coverage: int
    evidence_gap_coverage: int
    expected_information_gain_bits: float
    historical_outcome: str | None
    cost: int
    reason: str


HYPOTHESES = (
    HypothesisState(
        "interaction_contextual",
        "Interaction helps only in regimes where candidate dependency is active.",
        0.35,
        "OPEN",
    ),
    HypothesisState(
        "interaction_unstable",
        "Interaction effects vary across tasks or regimes and do not support a universal rule.",
        0.45,
        "OPEN",
    ),
    HypothesisState(
        "interaction_absent",
        "Candidate interaction adds no decision-relevant information in the tested scope.",
        0.20,
        "OPEN",
    ),
    HypothesisState(
        "learned_shortlist_safe",
        "A learned shortlist preserves required-candidate recall in the target workload.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "learned_shortlist_unsafe",
        "A learned shortlist can remove the required candidate in the target workload.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "reuse_identity_valid",
        "Stable identity supports deterministic reuse without collisions.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "reuse_identity_invalid",
        "Identity reuse can collide or change returned semantics.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "merge_convergent",
        "Evidence state converges across reordered compatible updates.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "merge_nonconvergent",
        "Evidence state can depend on arrival order.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "continuation_visible",
        "Reification exposes stage-boundary failures without changing successful semantics.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "continuation_opaque",
        "Reification does not reliably expose stage-boundary failures.",
        0.50,
        "OPEN",
    ),
    HypothesisState(
        "authority_external",
        "Authorization remains external to inference.",
        0.50,
        "OPEN",
        "control_plane",
    ),
    HypothesisState(
        "authority_minted",
        "Inference can incorrectly mint execution authority.",
        0.50,
        "OPEN",
        "control_plane",
    ),
    HypothesisState(
        "compound_signal_safe",
        "Interaction signal exists and shortlist pruning preserves it.",
        0.25,
        "OPEN",
    ),
    HypothesisState(
        "compound_signal_unsafe",
        "Interaction signal exists but shortlist pruning removes required signal.",
        0.25,
        "OPEN",
    ),
    HypothesisState(
        "compound_no_signal_safe",
        "Interaction signal is absent and shortlist pruning remains safe.",
        0.25,
        "OPEN",
    ),
    HypothesisState(
        "compound_no_signal_unsafe",
        "Interaction signal is absent but shortlist pruning is unsafe.",
        0.25,
        "OPEN",
    ),
)


HISTORICAL_OUTCOMES = (
    HistoricalOutcome(
        "interaction_probe",
        "mixed_gain",
        "research/receipts/v03-results.md",
        applies_to_current_design=False,
    ),
)


ADAPTIVE_EXPERIMENTS = (
    AdaptiveExperiment(
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
        ("interaction_contextual", "interaction_unstable", "interaction_absent"),
        (
            ("interaction_contextual", "active_gain_only"),
            ("interaction_unstable", "mixed_gain"),
            ("interaction_absent", "no_gain"),
        ),
        status="COMPLETED_HISTORICAL_SCOPE",
    ),
    AdaptiveExperiment(
        "interaction_regime_map",
        ("candidate_interaction",),
        ("interaction_probe",),
        ("condition", "relate", "dynamic_score"),
        "The observed interaction effect can be separated into contextual benefit versus regime instability.",
        "Sweep interaction strength and candidate-set perturbations over matched K and multiple seeds.",
        "Pairwise scorer under the same encoder and training budget.",
        "Previous mixed v0.3 evidence is held fixed; the new sweep tests whether the remaining uncertainty is contextual or unstable.",
        "Whether outcome changes follow the declared interaction regime rather than one synthetic point.",
        "Reject if the regime map is not reproducible across seeds or explanations remain observationally indistinguishable.",
        ("matched_baseline", "multiple_seeds", "interaction_grid", "raw_metrics", "failure_case"),
        2,
        ("interaction_contextual", "interaction_unstable", "interaction_absent"),
        (
            ("interaction_contextual", "regime_aligned"),
            ("interaction_unstable", "regime_mixed"),
            ("interaction_absent", "regime_null"),
        ),
    ),
    AdaptiveExperiment(
        "interaction_retrieval_guard",
        ("candidate_interaction", "retrieval_overload"),
        ("interaction_probe", "retrieval_guard"),
        ("identify", "shortlist", "dynamic_score", "condition", "relate"),
        "A safe retrieval gate can preserve the candidate-interaction signal while reducing expensive downstream candidate work.",
        "Compare full-candidate interaction-aware scoring with K-grid shortlist-then-rerank.",
        "Full candidate set plus pairwise baseline, with matched encoder and scoring budget.",
        "Full-candidate interaction-aware scorer with the same K values and encoder.",
        "Whether pruning preserves the required interaction signal while reducing downstream work.",
        "Reject if shortlist recall misses the safety target or interaction gains disappear after pruning.",
        ("dataset_ref", "K_grid", "recall_at_K", "compute_measure", "raw_accuracy_and_brier"),
        3,
        ("compound_signal_safe", "compound_signal_unsafe", "compound_no_signal_safe", "compound_no_signal_unsafe"),
        (
            ("compound_signal_safe", "signal_and_safe"),
            ("compound_signal_unsafe", "signal_and_unsafe"),
            ("compound_no_signal_safe", "no_signal_and_safe"),
            ("compound_no_signal_unsafe", "no_signal_and_unsafe"),
        ),
    ),
    AdaptiveExperiment(
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
        ("learned_shortlist_safe", "learned_shortlist_unsafe"),
        (
            ("learned_shortlist_safe", "safe"),
            ("learned_shortlist_unsafe", "unsafe"),
        ),
    ),
    AdaptiveExperiment(
        "learned_shortlist_transfer",
        ("retrieval_overload",),
        ("retrieval_guard",),
        ("identify", "shortlist", "dynamic_score"),
        "The oracle shortlist proof can transfer to a learned prefilter without losing required-candidate recall.",
        "Train or fine-tune the learned prefilter, then measure recall@K and downstream work over real or realistic embeddings.",
        "Full-candidate scorer; the earlier oracle-vector result is evidence, not a learned-data baseline.",
        "Full-candidate scoring on the same learned embeddings, seeds, and downstream scoring budget.",
        "Whether learned pruning remains safe after distributional transfer.",
        "Reject if learned recall falls below the declared safety threshold or varies materially across seeds/domains.",
        ("real_embedding_ref", "K_grid", "multiple_seeds", "recall_at_K", "compute_measure"),
        2,
        ("learned_shortlist_safe", "learned_shortlist_unsafe"),
        (
            ("learned_shortlist_safe", "safe"),
            ("learned_shortlist_unsafe", "unsafe"),
        ),
        status="OPEN",
    ),
    AdaptiveExperiment(
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
        ("reuse_identity_valid", "reuse_identity_invalid"),
        (
            ("reuse_identity_valid", "reuse_ok"),
            ("reuse_identity_invalid", "collision"),
        ),
    ),
    AdaptiveExperiment(
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
        ("merge_convergent", "merge_nonconvergent"),
        (
            ("merge_convergent", "convergent"),
            ("merge_nonconvergent", "order_dependent"),
        ),
    ),
    AdaptiveExperiment(
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
        ("continuation_visible", "continuation_opaque"),
        (
            ("continuation_visible", "visible"),
            ("continuation_opaque", "opaque"),
        ),
    ),
    AdaptiveExperiment(
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
        ("authority_external", "authority_minted"),
        (
            ("authority_external", "external"),
            ("authority_minted", "minted"),
        ),
        scope="control_plane",
    ),
)


_HYPOTHESES = {item.key: item for item in HYPOTHESES}
_EXPERIMENTS = {item.key: item for item in ADAPTIVE_EXPERIMENTS}
_HISTORICAL = {item.experiment: item for item in HISTORICAL_OUTCOMES}

_VALID_STATUSES = {"ESTABLISHED", "EXPERIMENTALLY_SUPPORTED", "HYPOTHESIS", "OPEN", "CONTRADICTED"}

if set(_EXPERIMENTS) != {item.key for item in ADAPTIVE_EXPERIMENTS}:
    raise ValueError("duplicate adaptive experiment")
if set(_HYPOTHESES) != {item.key for item in HYPOTHESES}:
    raise ValueError("duplicate hypothesis")
if set(_HISTORICAL) != {item.experiment for item in HISTORICAL_OUTCOMES}:
    raise ValueError("duplicate historical outcome")

for hypothesis in HYPOTHESES:
    if hypothesis.prior < 0:
        raise ValueError("hypothesis prior must be non-negative")
    if hypothesis.status not in _VALID_STATUSES:
        raise ValueError(f"invalid hypothesis status: {hypothesis.status}")

for experiment in ADAPTIVE_EXPERIMENTS:
    if any(item not in _HYPOTHESES for item in experiment.hypothesis_keys):
        raise ValueError(f"unknown hypothesis in {experiment.key}")
    if experiment.status not in {"OPEN", "HYPOTHESIS", "COMPLETED_HISTORICAL_SCOPE", "CONTRADICTED"}:
        raise ValueError(f"invalid experiment status in {experiment.key}")
    partition = dict(experiment.outcome_partition)
    if set(partition) != set(experiment.hypothesis_keys):
        raise ValueError(f"partition does not cover hypotheses in {experiment.key}")
    recipe_scopes = {
        "control_plane" if key == "authority_handoff" else "research"
        for key in experiment.recipe_keys
    }
    if recipe_scopes != {experiment.scope}:
        raise ValueError(f"scope mismatch in {experiment.key}")


def expected_information_gain(experiment_key: str) -> float:
    if experiment_key not in _EXPERIMENTS:
        raise KeyError(experiment_key)
    experiment = _EXPERIMENTS[experiment_key]
    partition = dict(experiment.outcome_partition)
    priors = {
        key: _HYPOTHESES[key].prior
        for key in experiment.hypothesis_keys
        if _HYPOTHESES[key].status in {"OPEN", "HYPOTHESIS"}
    }

    if experiment.status not in {"OPEN", "HYPOTHESIS"}:
        return 0.0
    historical = _HISTORICAL.get(experiment_key)
    if historical and historical.applies_to_current_design:
        priors = {
            key: prior for key, prior in priors.items()
            if partition[key] == historical.outcome
        }

    total = sum(priors.values())
    if total <= 0 or len(priors) <= 1:
        return 0.0
    priors = {key: value / total for key, value in priors.items()}

    before = -sum(value * log2(value) for value in priors.values() if value > 0)
    outcome_probability: dict[str, float] = {}
    for key, prior in priors.items():
        outcome = partition[key]
        outcome_probability[outcome] = outcome_probability.get(outcome, 0.0) + prior

    after = 0.0
    for outcome, probability in outcome_probability.items():
        posterior = {
            key: prior / probability
            for key, prior in priors.items()
            if partition[key] == outcome
        }
        entropy = -sum(value * log2(value) for value in posterior.values() if value > 0)
        after += probability * entropy

    return max(0.0, before - after)


def select_adaptive_experiments(
    observation: FailureObservation,
    *,
    scope: str = "research",
    excluded: tuple[str, ...] = (),
    limit: int = 3,
) -> tuple[AdaptiveSelection, ...]:
    if scope not in {"research", "control_plane"}:
        raise ValueError("invalid scope")
    if limit < 1:
        raise ValueError("limit must be positive")

    matches = classify_failure(observation)
    target_classes = {
        match.failure_class
        for match in matches
        if next(
            item.scope for item in FAILURE_CLASSES if item.key == match.failure_class
        ) == scope
    }
    gaps = set(observation.evidence_gaps)
    excluded_set = set(excluded)

    rows = []
    for experiment in ADAPTIVE_EXPERIMENTS:
        if experiment.scope != scope or experiment.key in excluded_set:
            continue
        required_classes = set(experiment.failure_classes)
        if not required_classes.issubset(target_classes):
            continue
        class_coverage = len(target_classes.intersection(experiment.failure_classes))
        if class_coverage == 0:
            continue
        gap_coverage = len(gaps.intersection(experiment.evidence_required))
        information_gain = expected_information_gain(experiment.key)
        historical = _HISTORICAL.get(experiment.key)
        sort_key = (
            -class_coverage,
            -gap_coverage,
            -information_gain,
            experiment.cost,
            experiment.key,
        )
        rows.append((
            sort_key,
            AdaptiveSelection(
                experiment.key,
                class_coverage,
                gap_coverage,
                information_gain,
                historical.outcome if historical else None,
                experiment.cost,
                (
                    f"covers {class_coverage} target failure class(es); "
                    f"covers {gap_coverage} requested evidence gap(s); "
                    f"expected IG={information_gain:.6f} bits; "
                    f"historical outcome={historical.outcome if historical else 'unobserved'}; "
                    f"declared cost={experiment.cost}"
                ),
            ),
        ))

    rows.sort(key=lambda item: item[0])
    return tuple(item[1] for item in rows[:limit])


def build_adaptive_plan(
    observation: FailureObservation,
    *,
    scope: str = "research",
    excluded: tuple[str, ...] = (),
    limit: int = 3,
) -> tuple[tuple[str, ...], tuple[AdaptiveSelection, ...]]:
    selections = select_adaptive_experiments(
        observation,
        scope=scope,
        excluded=excluded,
        limit=limit,
    )
    mechanisms: list[str] = []
    for selection in selections:
        for mechanism in _EXPERIMENTS[selection.experiment].mechanisms:
            if mechanism not in mechanisms:
                mechanisms.append(mechanism)
    return tuple(mechanisms), selections


def catalog() -> dict[str, object]:
    return {
        "status": "NON_CANONICAL_ADAPTIVE_DISCOVERY",
        "classification_rule": (
            "Structured FailureEvidence is reduced to explicit trigger tags, then "
            "classified with the existing deterministic failure registry. No free-form "
            "language is treated as truth."
        ),
        "information_gain_rule": (
            "Expected information gain is Shannon entropy reduction under declared "
            "research priors and deterministic outcome partitions. These priors are "
            "bookkeeping weights, not empirical probabilities."
        ),
        "history_rule": (
            "A historical outcome constrains a current experiment only when the record "
            "explicitly declares applies_to_current_design=True. Otherwise it remains related evidence and does not alter current priors."
        ),
        "selection_rule": (
            "Eligibility requires every failure class declared by an experiment to be present "
            "in the observation. Ordering is target failure-class coverage, evidence-gap coverage, "
            "expected information gain, declared cost, stable experiment key."
        ),
        "authority_rule": (
            "Control-plane authority experiments are selected in a separate scope and never "
            "merged into research/inference plans."
        ),
        "hypotheses": [
            {
                "key": item.key,
                "description": item.description,
                "prior": item.prior,
                "status": item.status,
                "scope": item.scope,
            }
            for item in HYPOTHESES
        ],
        "historical_outcomes": [
            {
                "experiment": item.experiment,
                "outcome": item.outcome,
                "evidence_ref": item.evidence_ref,
                "applies_to_current_design": item.applies_to_current_design,
                "scope": item.scope,
            }
            for item in HISTORICAL_OUTCOMES
        ],
        "experiments": [
            {
                "key": item.key,
                "failure_classes": list(item.failure_classes),
                "recipe_keys": list(item.recipe_keys),
                "mechanisms": list(item.mechanisms),
                "hypothesis": item.hypothesis,
                "intervention": item.intervention,
                "baseline": item.baseline,
                "control": item.control,
                "discriminator": item.discriminator,
                "kill_test": item.kill_test,
                "evidence_required": list(item.evidence_required),
                "cost": item.cost,
                "hypothesis_keys": list(item.hypothesis_keys),
                "outcome_partition": dict(item.outcome_partition),
                "status": item.status,
                "scope": item.scope,
                "expected_information_gain_bits": expected_information_gain(item.key),
                "historical_outcome": (
                    _HISTORICAL[item.key].outcome if item.key in _HISTORICAL else None
                ),
            }
            for item in ADAPTIVE_EXPERIMENTS
        ],
    }


__all__ = [
    "FailureEvidence",
    "HypothesisState",
    "HistoricalOutcome",
    "AdaptiveExperiment",
    "AdaptiveSelection",
    "HYPOTHESES",
    "HISTORICAL_OUTCOMES",
    "ADAPTIVE_EXPERIMENTS",
    "observation_from_evidence",
    "expected_information_gain",
    "select_adaptive_experiments",
    "build_adaptive_plan",
    "catalog",
]
