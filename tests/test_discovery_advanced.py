from open_system_one.discovery import FailureObservation, classify_failure
from open_system_one.discovery_advanced import (
    FailureEvidence,
    build_adaptive_plan,
    expected_information_gain,
    observation_from_evidence,
    select_adaptive_experiments,
)


def test_evidence_derivation_is_structured_not_tag_only():
    observation = observation_from_evidence(
        FailureEvidence(
            candidate_set_changes_output=True,
            candidate_count=20,
            candidate_budget=8,
            retrieval_latency_ms=120.0,
            retrieval_latency_budget_ms=50.0,
            evidence_refs=("receipt:synthetic",),
            evidence_gaps=("recall_at_K",),
        )
    )
    assert "candidate_set_changes_output" in observation.tags
    assert "large_candidate_count" in observation.tags
    assert "candidate_budget_exhausted" in observation.tags
    assert "retrieval_latency" in observation.tags
    assert observation.evidence_refs == ("receipt:synthetic",)
    assert observation.evidence_gaps == ("recall_at_K",)


def test_classifier_remains_multilabel_after_evidence_derivation():
    observation = observation_from_evidence(
        FailureEvidence(
            candidate_set_changes_output=True,
            retrieval_latency_ms=100.0,
            retrieval_latency_budget_ms=50.0,
        )
    )
    assert [row.failure_class for row in classify_failure(observation)] == [
        "candidate_interaction",
        "retrieval_overload",
    ]


def test_previous_mixed_result_eliminates_repeat_information_gain():
    assert expected_information_gain("interaction_probe") == 0.0


def test_regime_map_retains_more_than_one_bit_of_expected_information():
    gain = expected_information_gain("interaction_regime_map")
    assert 1.5 < gain < 1.6
    assert expected_information_gain("interaction_regime_map") == gain


def test_many_to_one_outcomes_can_have_zero_information_gain():
    from open_system_one.discovery_advanced import AdaptiveExperiment, _EXPERIMENTS

    experiment = AdaptiveExperiment(
        "many_to_one_test",
        ("candidate_interaction",),
        ("interaction_probe",),
        ("condition",),
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        ("test",),
        1,
        ("interaction_contextual", "interaction_unstable"),
        (("interaction_contextual", "same"), ("interaction_unstable", "same")),
    )
    _EXPERIMENTS["many_to_one_test"] = experiment
    try:
        assert expected_information_gain("many_to_one_test") == 0.0
    finally:
        del _EXPERIMENTS["many_to_one_test"]


def test_compound_experiment_has_two_bit_discrimination_under_declared_prior():
    gain = expected_information_gain("interaction_retrieval_guard")
    assert 1.99 < gain < 2.01


def test_selector_uses_history_and_information_gain():
    observation = FailureObservation(tags=("candidate_set_changes_output",))
    selections = select_adaptive_experiments(observation, limit=2)
    assert selections[0].experiment == "interaction_regime_map"
    assert selections[0].historical_outcome is None
    assert selections[0].expected_information_gain > 1.5


def test_compound_selector_covers_two_failure_classes():
    observation = FailureObservation(
        tags=("candidate_set_changes_output", "large_candidate_count")
    )
    selections = select_adaptive_experiments(observation, limit=3)
    assert selections[0].experiment == "interaction_retrieval_guard"
    assert selections[0].class_coverage == 2
    assert selections[0].expected_information_gain > 1.9


def test_adaptive_plan_exposes_mechanisms_and_receipt_fields():
    observation = FailureObservation(
        tags=("candidate_set_changes_output", "large_candidate_count"),
        evidence_refs=("receipt:42",),
    )
    mechanisms, selections = build_adaptive_plan(observation, limit=1)
    assert mechanisms == ("identify", "shortlist", "dynamic_score", "condition", "relate")
    assert selections[0].reason.startswith("covers 2 target failure class(es)")
