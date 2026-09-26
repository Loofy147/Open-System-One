import pytest

from open_system_one.discovery_advanced import AdaptiveExperiment, _EXPERIMENTS
from open_system_one.experiment_loop import (
    ExperimentExecutionResult,
    ReceiptProvenance,
    apply_reviewed_receipt,
    genesis_frontier,
    materialize_receipt,
    review_receipt,
)
from open_system_one.claim_synthesis import (
    ClaimRevisionRequest,
    ClaimSpec,
    apply_claim_revision,
    assessment_id,
    genesis_claim_ledger,
    synthesize_claim_evidence,
)


def _receipt(
    experiment_key: str,
    outcome: str,
):
    result = ExperimentExecutionResult(
        experiment_key=experiment_key,
        outcome=outcome,
        raw_metrics={"accuracy": 0.8},
        observed_failure_tags=(),
    )
    provenance = ReceiptProvenance(
        code_ref="git:claim-test",
        dataset_ref="dataset:claim-test",
        population="synthetic",
        split="fixed",
        runtime="python3.11-cpu",
        model="claim-test-model",
        configuration={"seed": 1},
    )
    return review_receipt(
        materialize_receipt(
            result,
            provenance,
            interpretation="Reviewed fixture outcome.",
            next_discriminating_test="repeat fixture.",
            kill_test_passed=True,
            discriminator_passed=True,
        )
    )


def _install_experiment(key: str, partition: tuple[tuple[str, str], ...]):
    experiment = AdaptiveExperiment(
        key,
        ("candidate_interaction",),
        ("interaction_probe",),
        ("condition",),
        "claim test",
        "claim test",
        "claim test",
        "claim test",
        "claim test",
        "claim test",
        ("fixture",),
        1,
        ("interaction_contextual", "interaction_unstable"),
        partition,
    )
    _EXPERIMENTS[key] = experiment
    return experiment


def test_synthesis_distinguishes_no_evidence_and_unique_support():
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    empty = synthesize_claim_evidence(genesis_frontier(), claim)
    assert empty.disposition == "NO_EVIDENCE"

    experiment = _install_experiment(
        "claim_support_fixture",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    try:
        frontier = apply_reviewed_receipt(
            genesis_frontier(),
            _receipt(experiment.key, "support"),
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)
        assert synthesis.disposition == "SUPPORTED"
        assert len(synthesis.supporting_evidence_ids) == 1
        assert len(synthesis.contradicting_evidence_ids) == 0
    finally:
        del _EXPERIMENTS[experiment.key]


def test_many_to_one_assessment_produces_unresolved_claim_synthesis():
    experiment = _install_experiment(
        "claim_unresolved_fixture",
        (
            ("interaction_contextual", "same"),
            ("interaction_unstable", "same"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = apply_reviewed_receipt(
            genesis_frontier(),
            _receipt(experiment.key, "same"),
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)
        assert synthesis.disposition == "UNRESOLVED"
    finally:
        del _EXPERIMENTS[experiment.key]


def test_cross_experiment_support_and_contradiction_are_conflicted_not_resolved():
    support = _install_experiment(
        "claim_support_fixture_2",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    contradict = _install_experiment(
        "claim_contradict_fixture",
        (
            ("interaction_contextual", "contradict"),
            ("interaction_unstable", "other"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = genesis_frontier()
        frontier = apply_reviewed_receipt(
            frontier, _receipt(support.key, "support")
        ).state_after
        frontier = apply_reviewed_receipt(
            frontier, _receipt(contradict.key, "contradict")
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)
        assert synthesis.disposition == "CONFLICTED"
        assert len(synthesis.supporting_evidence_ids) == 1
        assert len(synthesis.contradicting_evidence_ids) == 1
    finally:
        del _EXPERIMENTS[support.key]
        del _EXPERIMENTS[contradict.key]


def test_experimental_support_requires_full_unconflicted_evidence_set():
    support = _install_experiment(
        "claim_support_fixture_3",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    contradict = _install_experiment(
        "claim_contradict_fixture_2",
        (
            ("interaction_contextual", "contradict"),
            ("interaction_unstable", "other"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = genesis_frontier()
        frontier = apply_reviewed_receipt(
            frontier, _receipt(support.key, "support")
        ).state_after
        frontier = apply_reviewed_receipt(
            frontier, _receipt(contradict.key, "contradict")
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)

        request = ClaimRevisionRequest(
            claim_key=claim.key,
            parent_revision_id="claims:genesis",
            status="EXPERIMENTALLY_SUPPORTED",
            rationale="Support-only evidence appears favorable.",
            limitations="Conflict evidence exists and is intentionally not selected.",
            next_discriminating_test="Resolve the contradiction with a controlled repeat.",
            evidence_ids=synthesis.supporting_evidence_ids,
            assessment_ids=tuple(
                item_id
                for item_id in synthesis.assessment_ids
                if item_id == synthesis.assessment_ids[0]
            ),
        )
        with pytest.raises(ValueError, match="full current claim evidence set"):
            apply_claim_revision(
                genesis_claim_ledger(), frontier, claim, request
            )
    finally:
        del _EXPERIMENTS[support.key]
        del _EXPERIMENTS[contradict.key]


def test_explicit_claim_revision_is_immutable_and_does_not_change_frontier():
    experiment = _install_experiment(
        "claim_revision_fixture",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = apply_reviewed_receipt(
            genesis_frontier(),
            _receipt(experiment.key, "support"),
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)
        state = genesis_claim_ledger()
        request = ClaimRevisionRequest(
            claim_key=claim.key,
            parent_revision_id=state.revision_id,
            status="EXPERIMENTALLY_SUPPORTED",
            rationale="The reviewed outcome uniquely supports the mapped hypothesis.",
            limitations="The claim is limited to the experiment population and split.",
            next_discriminating_test="Repeat under an independent dataset and multiple seeds.",
            evidence_ids=synthesis.evidence_ids,
            assessment_ids=synthesis.assessment_ids,
        )

        result = apply_claim_revision(state, frontier, claim, request)
        assert result.status == "APPLIED"
        assert result.claim_revision is not None
        assert result.claim_revision.status == "EXPERIMENTALLY_SUPPORTED"
        assert state.revision_id == "claims:genesis"
        assert result.state_after.revision_id == result.revision_id
        assert len(result.state_after.revisions) == 1
        assert frontier.completed_experiments == (experiment.key,)
    finally:
        del _EXPERIMENTS[experiment.key]


def test_replaying_identical_claim_revision_is_idempotent():
    experiment = _install_experiment(
        "claim_revision_replay_fixture",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = apply_reviewed_receipt(
            genesis_frontier(),
            _receipt(experiment.key, "support"),
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)
        state = genesis_claim_ledger()
        request = ClaimRevisionRequest(
            claim.key,
            state.revision_id,
            "EXPERIMENTALLY_SUPPORTED",
            "Unique reviewed support.",
            "Scope limited to the fixture.",
            "Repeat independently.",
            synthesis.evidence_ids,
            synthesis.assessment_ids,
        )
        first = apply_claim_revision(state, frontier, claim, request)
        second = apply_claim_revision(state, frontier, claim, request)

        assert second.status == "IDEMPOTENT_REPLAY"
        assert second.revision_id == first.revision_id
        assert second.state_after == state
    finally:
        del _EXPERIMENTS[experiment.key]


def test_stale_parent_cannot_overwrite_claim_ledger():
    experiment = _install_experiment(
        "claim_revision_parent_fixture",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = apply_reviewed_receipt(
            genesis_frontier(),
            _receipt(experiment.key, "support"),
        ).state_after
        synthesis = synthesize_claim_evidence(frontier, claim)
        state = genesis_claim_ledger()
        request = ClaimRevisionRequest(
            claim.key,
            state.revision_id,
            "EXPERIMENTALLY_SUPPORTED",
            "Unique reviewed support.",
            "Fixture scope only.",
            "Repeat independently.",
            synthesis.evidence_ids,
            synthesis.assessment_ids,
        )
        first = apply_claim_revision(state, frontier, claim, request)

        stale = ClaimRevisionRequest(
            claim.key,
            "claims:genesis",
            "HYPOTHESIS",
            "Retain hypothesis framing.",
            "The support is still narrow.",
            "Run an independent real-data experiment.",
            synthesis.evidence_ids,
            synthesis.assessment_ids,
        )
        with pytest.raises(ValueError, match="parent"):
            apply_claim_revision(first.state_after, frontier, claim, stale)
    finally:
        del _EXPERIMENTS[experiment.key]


def test_assessment_identity_is_stable():
    experiment = _install_experiment(
        "claim_identity_fixture",
        (
            ("interaction_contextual", "support"),
            ("interaction_unstable", "other"),
        ),
    )
    claim = ClaimSpec(
        key="claim:interaction-contextual",
        statement="Interaction benefit is contextual in the tested research scope.",
        hypothesis_key="interaction_contextual",
    )
    try:
        frontier = apply_reviewed_receipt(
            genesis_frontier(),
            _receipt(experiment.key, "support"),
        ).state_after
        assessment = next(
            item
            for item in frontier.assessments
            if item.hypothesis_key == claim.hypothesis_key
        )
        assert assessment_id(assessment) == assessment_id(assessment)
    finally:
        del _EXPERIMENTS[experiment.key]
