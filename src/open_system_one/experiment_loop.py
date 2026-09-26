from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
from math import isfinite
import json
from typing import Any, Literal, Mapping

from .discovery_advanced import (
    ADAPTIVE_EXPERIMENTS,
    HYPOTHESES,
    _EXPERIMENTS,
)


ReceiptStatus = Literal["EXECUTED", "REVIEWED", "REJECTED"]
AssessmentRelation = Literal["SUPPORTED", "CONTRADICTED", "UNRESOLVED"]


def _canonical_json(value: object) -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("value is not canonical-JSON serializable") from exc


def _digest(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExperimentExecutionResult:
    experiment_key: str
    outcome: str
    raw_metrics: Mapping[str, float]
    observed_failure_tags: tuple[str, ...] = ()

    @property
    def result_digest(self) -> str:
        return _digest(
            {
                "experiment_key": self.experiment_key,
                "outcome": self.outcome,
                "raw_metrics": dict(self.raw_metrics),
                "observed_failure_tags": list(self.observed_failure_tags),
            }
        )


@dataclass(frozen=True)
class ReceiptProvenance:
    code_ref: str
    dataset_ref: str
    population: str
    split: str
    runtime: str
    model: str
    configuration: Mapping[str, Any]


@dataclass(frozen=True)
class ExperimentReceipt:
    experiment_key: str
    outcome: str
    code_ref: str
    dataset_ref: str
    population: str
    split: str
    runtime: str
    model: str
    configuration: Mapping[str, Any]
    raw_metrics: Mapping[str, float]
    observed_failure_tags: tuple[str, ...]
    interpretation: str
    status: ReceiptStatus
    next_discriminating_test: str
    kill_test_passed: bool
    discriminator_passed: bool
    scope: str = "research"
    evidence_refs: tuple[str, ...] = ()
    execution_digest: str = ""

    @property
    def receipt_digest(self) -> str:
        return _digest(self._payload(include_status=True))

    def _payload(self, *, include_status: bool) -> dict[str, object]:
        payload: dict[str, object] = {
            "experiment_key": self.experiment_key,
            "outcome": self.outcome,
            "code_ref": self.code_ref,
            "dataset_ref": self.dataset_ref,
            "population": self.population,
            "split": self.split,
            "runtime": self.runtime,
            "model": self.model,
            "configuration": dict(self.configuration),
            "raw_metrics": dict(self.raw_metrics),
            "observed_failure_tags": list(self.observed_failure_tags),
            "interpretation": self.interpretation,
            "next_discriminating_test": self.next_discriminating_test,
            "kill_test_passed": self.kill_test_passed,
            "discriminator_passed": self.discriminator_passed,
            "scope": self.scope,
            "evidence_refs": list(self.evidence_refs),
            "execution_digest": self.execution_digest,
        }
        if include_status:
            payload["status"] = self.status
        return payload


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    receipt_digest: str
    experiment_key: str
    outcome: str
    scope: str
    code_ref: str
    dataset_ref: str
    population: str
    split: str
    runtime: str
    model: str
    configuration: Mapping[str, Any]
    raw_metrics: Mapping[str, float]
    observed_failure_tags: tuple[str, ...]
    interpretation: str
    kill_test_passed: bool
    discriminator_passed: bool
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class HypothesisAssessment:
    hypothesis_key: str
    experiment_key: str
    relation: AssessmentRelation
    evidence_id: str
    scope: str
    rationale: str


@dataclass(frozen=True)
class AdaptiveFrontierState:
    completed_experiments: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    assessments: tuple[HypothesisAssessment, ...] = ()
    revision_id: str = "frontier:genesis"

    def experiment_status(self, experiment_key: str) -> str:
        if experiment_key not in _EXPERIMENTS:
            raise KeyError(experiment_key)
        if experiment_key in self.completed_experiments:
            return "COMPLETED_CURRENT_SCOPE"
        return _EXPERIMENTS[experiment_key].status

    def has_evidence(self, evidence_id: str) -> bool:
        return evidence_id in self.evidence_ids


@dataclass(frozen=True)
class EvidenceLedgerRevision:
    status: Literal["APPLIED", "IDEMPOTENT_REPLAY"]
    parent_revision_id: str
    revision_id: str
    evidence: EvidenceRecord | None
    assessments: tuple[HypothesisAssessment, ...]
    experiment_key: str
    experiment_status_before: str
    experiment_status_after: str
    state_after: AdaptiveFrontierState


def parse_execution_result(payload: Mapping[str, object]) -> ExperimentExecutionResult:
    required = {"experiment_key", "outcome", "raw_metrics", "observed_failure_tags"}
    if set(payload) != required:
        raise ValueError("execution result keys must exactly match the execution contract")

    experiment_key = payload["experiment_key"]
    outcome = payload["outcome"]
    raw_metrics = payload["raw_metrics"]
    observed_failure_tags = payload["observed_failure_tags"]

    if not isinstance(experiment_key, str) or not experiment_key:
        raise ValueError("experiment_key must be a non-empty string")
    if not isinstance(outcome, str) or not outcome:
        raise ValueError("outcome must be a non-empty string")
    if not isinstance(raw_metrics, Mapping):
        raise ValueError("raw_metrics must be a mapping")
    if any(
        not isinstance(key, str)
        or not key
        or not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not isfinite(float(value))
        for key, value in raw_metrics.items()
    ):
        raise ValueError("raw_metrics must contain finite numeric values")
    if not isinstance(observed_failure_tags, (tuple, list)):
        raise ValueError("observed_failure_tags must be a sequence")

    tags = tuple(sorted(set(observed_failure_tags)))
    if any(not isinstance(tag, str) or not tag for tag in tags):
        raise ValueError("observed_failure_tags must contain non-empty strings")

    return ExperimentExecutionResult(
        experiment_key=experiment_key,
        outcome=outcome,
        raw_metrics={str(key): float(value) for key, value in raw_metrics.items()},
        observed_failure_tags=tags,
    )


def materialize_receipt(
    result: ExperimentExecutionResult,
    provenance: ReceiptProvenance,
    *,
    interpretation: str,
    next_discriminating_test: str,
    kill_test_passed: bool,
    discriminator_passed: bool,
    status: ReceiptStatus = "EXECUTED",
    scope: str = "research",
    evidence_refs: tuple[str, ...] = (),
) -> ExperimentReceipt:
    receipt = ExperimentReceipt(
        experiment_key=result.experiment_key,
        outcome=result.outcome,
        code_ref=provenance.code_ref,
        dataset_ref=provenance.dataset_ref,
        population=provenance.population,
        split=provenance.split,
        runtime=provenance.runtime,
        model=provenance.model,
        configuration=dict(provenance.configuration),
        raw_metrics=dict(result.raw_metrics),
        observed_failure_tags=result.observed_failure_tags,
        interpretation=interpretation,
        status=status,
        next_discriminating_test=next_discriminating_test,
        kill_test_passed=kill_test_passed,
        discriminator_passed=discriminator_passed,
        scope=scope,
        evidence_refs=tuple(sorted(set(evidence_refs))),
        execution_digest=result.result_digest,
    )
    validate_experiment_receipt(receipt)
    return receipt


def review_receipt(receipt: ExperimentReceipt) -> ExperimentReceipt:
    validate_experiment_receipt(receipt)
    if receipt.status != "EXECUTED":
        raise ValueError("only an executed receipt can be reviewed")
    if not receipt.kill_test_passed or not receipt.discriminator_passed:
        raise ValueError("receipt cannot be reviewed until kill and discriminator tests pass")
    return replace(receipt, status="REVIEWED")


def validate_experiment_receipt(receipt: ExperimentReceipt) -> None:
    if receipt.experiment_key not in _EXPERIMENTS:
        raise KeyError(receipt.experiment_key)
    experiment = _EXPERIMENTS[receipt.experiment_key]

    if receipt.scope != experiment.scope:
        raise ValueError("receipt scope does not match experiment scope")
    if receipt.status not in {"EXECUTED", "REVIEWED", "REJECTED"}:
        raise ValueError("invalid receipt status")
    if not receipt.code_ref or not receipt.dataset_ref or not receipt.population:
        raise ValueError("receipt provenance is incomplete")
    if not receipt.split or not receipt.runtime or not receipt.model:
        raise ValueError("receipt runtime/model provenance is incomplete")
    if not receipt.interpretation or not receipt.next_discriminating_test:
        raise ValueError("receipt interpretation and next test are required")
    if not receipt.outcome or receipt.outcome not in dict(experiment.outcome_partition).values():
        raise ValueError("receipt outcome is not in the experiment partition")
    if receipt.observed_failure_tags != tuple(sorted(set(receipt.observed_failure_tags))):
        raise ValueError("observed_failure_tags must be sorted and unique")
    if receipt.evidence_refs != tuple(sorted(set(receipt.evidence_refs))):
        raise ValueError("evidence_refs must be sorted and unique")
    if any(
        not isinstance(key, str)
        or not key
        or not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not isfinite(float(value))
        for key, value in receipt.raw_metrics.items()
    ):
        raise ValueError("receipt raw_metrics must be finite numeric values")
    _canonical_json(receipt.configuration)

    expected_result_digest = ExperimentExecutionResult(
        receipt.experiment_key,
        receipt.outcome,
        receipt.raw_metrics,
        receipt.observed_failure_tags,
    ).result_digest
    if receipt.execution_digest != expected_result_digest:
        raise ValueError("execution_digest does not match recorded execution result")

    if receipt.status == "REVIEWED":
        if not receipt.kill_test_passed or not receipt.discriminator_passed:
            raise ValueError("reviewed receipt requires passed kill and discriminator tests")


def materialize_evidence(receipt: ExperimentReceipt) -> EvidenceRecord:
    validate_experiment_receipt(receipt)
    if receipt.status != "REVIEWED":
        raise ValueError("only a reviewed receipt can become ledger evidence")

    evidence_id = "evidence:" + receipt.receipt_digest
    return EvidenceRecord(
        evidence_id=evidence_id,
        receipt_digest=receipt.receipt_digest,
        experiment_key=receipt.experiment_key,
        outcome=receipt.outcome,
        scope=receipt.scope,
        code_ref=receipt.code_ref,
        dataset_ref=receipt.dataset_ref,
        population=receipt.population,
        split=receipt.split,
        runtime=receipt.runtime,
        model=receipt.model,
        configuration=dict(receipt.configuration),
        raw_metrics=dict(receipt.raw_metrics),
        observed_failure_tags=receipt.observed_failure_tags,
        interpretation=receipt.interpretation,
        kill_test_passed=receipt.kill_test_passed,
        discriminator_passed=receipt.discriminator_passed,
        evidence_refs=receipt.evidence_refs,
    )


def derive_hypothesis_assessments(
    receipt: ExperimentReceipt,
    evidence: EvidenceRecord,
) -> tuple[HypothesisAssessment, ...]:
    if evidence.receipt_digest != receipt.receipt_digest:
        raise ValueError("evidence does not belong to receipt")
    if evidence.experiment_key != receipt.experiment_key or evidence.outcome != receipt.outcome:
        raise ValueError("evidence does not match receipt execution")
    experiment = _EXPERIMENTS[receipt.experiment_key]
    partition = dict(experiment.outcome_partition)
    compatible = tuple(
        key for key in experiment.hypothesis_keys if partition[key] == receipt.outcome
    )
    if not compatible:
        raise ValueError("receipt outcome has no compatible hypothesis in partition")

    assessments: list[HypothesisAssessment] = []
    for key in experiment.hypothesis_keys:
        if key in compatible:
            if len(compatible) == 1:
                relation: AssessmentRelation = "SUPPORTED"
                rationale = (
                    "Reviewed outcome uniquely selects this hypothesis under the "
                    "experiment's declared deterministic outcome partition."
                )
            else:
                relation = "UNRESOLVED"
                rationale = (
                    "Reviewed outcome is compatible with multiple hypotheses under the "
                    "declared many-to-one partition; this experiment does not identify which one."
                )
        else:
            relation = "CONTRADICTED"
            rationale = (
                "Reviewed outcome is incompatible with this hypothesis under the experiment's "
                "declared deterministic outcome partition."
            )
        assessments.append(
            HypothesisAssessment(
                hypothesis_key=key,
                experiment_key=receipt.experiment_key,
                relation=relation,
                evidence_id=evidence.evidence_id,
                scope=receipt.scope,
                rationale=rationale,
            )
        )
    return tuple(assessments)


def apply_reviewed_receipt(
    frontier: AdaptiveFrontierState,
    receipt: ExperimentReceipt,
) -> EvidenceLedgerRevision:
    validate_experiment_receipt(receipt)
    if receipt.status != "REVIEWED":
        raise ValueError("closed-loop application requires a reviewed receipt")

    evidence = materialize_evidence(receipt)
    if frontier.has_evidence(evidence.evidence_id):
        status = frontier.experiment_status(receipt.experiment_key)
        return EvidenceLedgerRevision(
            status="IDEMPOTENT_REPLAY",
            parent_revision_id=frontier.revision_id,
            revision_id=frontier.revision_id,
            evidence=None,
            assessments=(),
            experiment_key=receipt.experiment_key,
            experiment_status_before=status,
            experiment_status_after=status,
            state_after=frontier,
        )

    before_status = frontier.experiment_status(receipt.experiment_key)
    if before_status not in {"OPEN", "HYPOTHESIS"}:
        raise ValueError(
            f"experiment {receipt.experiment_key} is not open in the current frontier"
        )

    assessments = derive_hypothesis_assessments(receipt, evidence)
    completed = tuple(sorted(set(frontier.completed_experiments) | {receipt.experiment_key}))
    evidence_ids = tuple(sorted(set(frontier.evidence_ids) | {evidence.evidence_id}))
    all_assessments = frontier.assessments + assessments

    revision_payload = {
        "parent_revision_id": frontier.revision_id,
        "evidence_id": evidence.evidence_id,
        "experiment_key": receipt.experiment_key,
        "assessments": [
            {
                "hypothesis_key": item.hypothesis_key,
                "relation": item.relation,
                "scope": item.scope,
            }
            for item in assessments
        ],
    }
    revision_id = "revision:" + _digest(revision_payload)

    state_after = AdaptiveFrontierState(
        completed_experiments=completed,
        evidence_ids=evidence_ids,
        assessments=all_assessments,
        revision_id=revision_id,
    )

    return EvidenceLedgerRevision(
        status="APPLIED",
        parent_revision_id=frontier.revision_id,
        revision_id=revision_id,
        evidence=evidence,
        assessments=assessments,
        experiment_key=receipt.experiment_key,
        experiment_status_before=before_status,
        experiment_status_after="COMPLETED_CURRENT_SCOPE",
        state_after=state_after,
    )


def frontier_catalog_state(frontier: AdaptiveFrontierState) -> dict[str, object]:
    return {
        "revision_id": frontier.revision_id,
        "completed_experiments": list(frontier.completed_experiments),
        "evidence_ids": list(frontier.evidence_ids),
        "assessments": [
            {
                "hypothesis_key": item.hypothesis_key,
                "experiment_key": item.experiment_key,
                "relation": item.relation,
                "evidence_id": item.evidence_id,
                "scope": item.scope,
            }
            for item in frontier.assessments
        ],
    }


def genesis_frontier() -> AdaptiveFrontierState:
    return AdaptiveFrontierState()


__all__ = [
    "ExperimentExecutionResult",
    "ReceiptProvenance",
    "ExperimentReceipt",
    "EvidenceRecord",
    "HypothesisAssessment",
    "AdaptiveFrontierState",
    "EvidenceLedgerRevision",
    "parse_execution_result",
    "materialize_receipt",
    "validate_experiment_receipt",
    "review_receipt",
    "materialize_evidence",
    "derive_hypothesis_assessments",
    "apply_reviewed_receipt",
    "frontier_catalog_state",
    "genesis_frontier",
]
