from open_system_one.discovery import (
    FailureObservation,
    build_plan,
    build_plans,
    catalog,
    classify_failure,
    coordinate,
    coordinate_failures,
    propose,
    select_experiments,
)


def test_candidate_interaction_has_multiple_precomposed_mechanisms():
    rows = propose("candidate_interaction")
    assert len(rows) == 1
    assert rows[0].mechanisms == ("condition", "relate", "dynamic_score")


def test_multi_recipe_coordination_deduplicates_shared_mechanisms():
    rows = propose("provenance_drift")
    assert [row.recipe for row in rows] == ["deterministic_reuse", "ordered_merge"]
    plan = coordinate("provenance_drift")
    assert plan.recipes == ("deterministic_reuse", "ordered_merge")
    assert plan.mechanisms == ("identify", "cache", "order", "merge")
    assert len(plan.hypotheses) == 2
    assert "final_state_digest" in plan.evidence_required


def test_authority_recipe_is_outside_research_scope():
    plan = coordinate("authority_boundary")
    assert plan.recipes == ("authority_handoff",)
    assert "capability_gate" in plan.mechanisms
    assert catalog()["authority_rule"].startswith("Control-plane")


def test_unknown_failure_class_is_rejected():
    try:
        propose("not_registered")
    except KeyError:
        return
    raise AssertionError("unknown failure class was accepted")


def test_multi_failure_coordination_merges_recipe_sets():
    plan = coordinate_failures(("repeated_compute", "provenance_drift"))
    assert plan.failure_classes == ("repeated_compute", "provenance_drift")
    assert plan.recipes == ("deterministic_reuse", "ordered_merge")
    assert plan.mechanisms == ("identify", "cache", "order", "merge")


def test_multi_failure_coordination_rejects_authority_mixing():
    try:
        coordinate_failures(("candidate_interaction", "authority_boundary"))
    except ValueError:
        return
    raise AssertionError("authority and discovery recipes were incorrectly merged")


def test_structured_classifier_is_multilabel_and_deterministic():
    observation = FailureObservation(
        tags=("retrieval_latency", "candidate_set_changes_output")
    )
    rows = classify_failure(observation)
    assert [row.failure_class for row in rows] == [
        "candidate_interaction",
        "retrieval_overload",
    ]
    assert [row.score for row in rows] == [1, 1]
    assert classify_failure(observation) == rows


def test_selector_chooses_compound_experiment_for_two_failures():
    observation = FailureObservation(
        tags=("candidate_set_changes_output", "large_candidate_count")
    )
    selections = select_experiments(observation, limit=3)
    assert selections[0].experiment == "interaction_retrieval_guard"
    assert selections[0].class_coverage == 2


def test_selector_uses_requested_evidence_gaps_as_a_secondary_tiebreak():
    observation = FailureObservation(
        tags=("same_input_repeated", "hash_mismatch"),
        evidence_gaps=("mutation_kill_test",),
    )
    selections = select_experiments(observation, limit=2)
    assert selections[0].experiment == "artifact_reuse"
    assert selections[0].evidence_gap_coverage == 1


def test_build_plans_separates_authority_from_research():
    observation = FailureObservation(
        tags=("candidate_set_changes_output", "missing_capability")
    )
    plans = build_plans(observation)
    assert [plan.scope for plan in plans] == ["control_plane", "research"]
    assert all(plan.experiments for plan in plans)


def test_build_plan_contains_complete_discovery_payload():
    observation = FailureObservation(tags=("candidate_set_changes_output",))
    plan = build_plan(observation)
    assert plan.scope == "research"
    assert plan.matches[0].failure_class == "candidate_interaction"
    assert plan.experiments[0].experiment == "interaction_probe"
    assert plan.hypotheses
    assert plan.kill_tests
    assert plan.evidence_required
