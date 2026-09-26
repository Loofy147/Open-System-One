import pytest

from open_system_one.discovery import FailureObservation
from open_system_one.discovery_advanced import AdaptiveExperiment, _EXPERIMENTS, build_adaptive_plan, expected_information_gain, select_adaptive_experiments
from open_system_one.experiment_loop import (
    ExperimentExecutionResult,
    ReceiptProvenance,
    apply_reviewed_receipt,
    derive_hypothesis_assessments,
    genesis_frontier,
    materialize_evidence,
    materialize_receipt,
    parse_execution_result,
    review_receipt,
)


def _reviewed_receipt(
    *,
    experiment_key: str = "interaction_regime_map",
    outcome: str = "regime_aligned",
    tags: tuple[str, ...] = ("candidate_set_changes_output",),
):
    result = ExperimentExecutionResult(
        experiment_key=experiment_key,
        outcome=outcome,
        raw_metrics={"accuracy": 0.82, "brier": 0.03},
        observed_failure_tags=tags,
    )
    provenance = ReceiptProvenance(
        code_ref="git:abc123",
        dataset_ref="dataset:test-v1",
        population="synthetic-k8",
        split="train=test-fixture",
        runtime="python3.11-cpu",
        model="pairwise-test",
        configuration={"seed": 11, "interaction": 1.25},
    )
    return review_receipt(
        materialize_receipt(
            result,
            provenance,
            interpretation="Matched intervention completed.",
            next_discriminating_test="repeat across independent seeds.",
            kill_test_passed=True,
            discriminator_passed=True,
        )
    )


def test_parse_execution_result_is_strict_and_normalizes_tags():
    result = parse_execution_result(
        {
            "experiment_key": "interaction_regime_map",
            "outcome": "regime_aligned",
            "raw_metrics": {"brier": 0.03},
            "observed_failure_tags": ["candidate_set_changes_output", "candidate_set_changes_output"],
        }
    )
    assert result.observed_failure_tags == ("candidate_set_changes_output",)
    assert result.raw_metrics == {"brier": 0.03}
    with pytest.raises(ValueError):
        parse_execution_result(
            {
                "experiment_key": "interaction_regime_map",
                "outcome": "regime_aligned",
                "raw_metrics": {"brier": 0.03},
                "observed_failure_tags": [],
                "extra": True,
            }
        )


def test_review_requires_passed_kill_and_discriminator_tests():
    result = ExperimentExecutionResult(
        "interaction_regime_map",
        "regime_aligned",
        {"brier": 0.03},
        (),
    )
    provenance = ReceiptProvenance(
        "git:abc123",
        "dataset:test-v1",
        "synthetic",
        "fixed",
        "python3.11-cpu",
        "pairwise-test",
        {"seed": 11},
    )
    receipt = materialize_receipt(
        result,
        provenance,
        interpretation="Observed.",
        next_discriminating_test="repeat.",
        kill_test_passed=False,
        discriminator_passed=True,
    )
    with pytest.raises(ValueError):
        review_receipt(receipt)


def test_reviewed_receipt_materializes_deterministic_evidence():
    receipt_a = _reviewed_receipt()
    receipt_b = _reviewed_receipt()
    evidence_a = materialize_evidence(receipt_a)
    evidence_b = materialize_evidence(receipt_b)
    assert evidence_a.evidence_id == evidence_b.evidence_id
    assert evidence_a.receipt_digest == receipt_a.receipt_digest


def test_unique_partition_creates_scoped_hypothesis_assessments():
    receipt = _reviewed_receipt()
    evidence = materialize_evidence(receipt)
    assessments = derive_hypothesis_assessments(receipt, evidence)
    relations = {x.hypothesis_key: x.relation for x in assessments}
    assert relations == {
        "interaction_contextual": "SUPPORTED",
        "interaction_unstable": "CONTRADICTED",
        "interaction_absent": "CONTRADICTED",
    }
    assert all(x.scope == "research" for x in assessments)
    assert all(x.evidence_id == evidence.evidence_id for x in assessments)


def test_many_to_one_partition_does_not_false_promote_compatible_hypotheses():
    experiment = AdaptiveExperiment(
        "many_to_one_loop_test",
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
        (
            ("interaction_contextual", "same"),
            ("interaction_unstable", "same"),
        ),
    )
    _EXPERIMENTS["many_to_one_loop_test"] = experiment
    try:
        receipt = _reviewed_receipt(
            experiment_key="many_to_one_loop_test",
            outcome="same",
        )
        evidence = materialize_evidence(receipt)
        assessments = derive_hypothesis_assessments(receipt, evidence)
        assert {x.relation for x in assessments} == {"UNRESOLVED"}
    finally:
        del _EXPERIMENTS["many_to_one_loop_test"]


def test_apply_reviewed_receipt_is_immutable_and_closes_only_the_executed_experiment():
    frontier = genesis_frontier()
    receipt = _reviewed_receipt()
    revision = apply_reviewed_receipt(frontier, receipt)
    assert revision.status == "APPLIED"
    assert revision.experiment_status_before == "OPEN"
    assert revision.experiment_status_after == "COMPLETED_CURRENT_SCOPE"
    assert revision.evidence is not None
    assert revision.state_after.revision_id == revision.revision_id
    assert revision.state_after.completed_experiments == ("interaction_regime_map",)
    assert frontier.completed_experiments == ()


def test_frontier_state_changes_repeat_information_gain_and_selection():
    frontier = genesis_frontier()
    receipt = _reviewed_receipt()
    revision = apply_reviewed_receipt(frontier, receipt)

    assert expected_information_gain("interaction_regime_map", revision.state_after) == 0.0

    observation = FailureObservation(tags=("candidate_set_changes_output",))
    selections = select_adaptive_experiments(
        observation,
        frontier=revision.state_after,
        limit=10,
    )
    assert selections == ()

    combined_observation = FailureObservation(
        tags=("candidate_set_changes_output", "large_candidate_count")
    )
    mechanisms, replanned = build_adaptive_plan(
        combined_observation,
        frontier=revision.state_after,
        limit=10,
    )
    assert "condition" in mechanisms
    assert replanned
    assert replanned[0].experiment == "interaction_retrieval_guard"
    assert all(item.experiment != "interaction_regime_map" for item in replanned)


def test_replaying_the_same_reviewed_receipt_is_idempotent():
    frontier = genesis_frontier()
    receipt = _reviewed_receipt()
    first = apply_reviewed_receipt(frontier, receipt)
    second = apply_reviewed_receipt(first.state_after, receipt)

    assert second.status == "IDEMPOTENT_REPLAY"
    assert second.revision_id == first.revision_id
    assert second.state_after == first.state_after
    assert second.evidence is None
    assert second.assessments == ()


def test_revision_digest_depends_on_parent_and_evidence():
    first = apply_reviewed_receipt(genesis_frontier(), _reviewed_receipt())
    different = apply_reviewed_receipt(
        genesis_frontier(),
        _reviewed_receipt(
            outcome="regime_mixed",
        ),
    )
    assert first.revision_id != different.revision_id
