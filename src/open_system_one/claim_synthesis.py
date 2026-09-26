from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Literal, Mapping
import json

from .experiment_loop import AdaptiveFrontierState, HypothesisAssessment
from .discovery_advanced import HYPOTHESES


ClaimSynthesisDisposition = Literal[
    "NO_EVIDENCE",
    "UNRESOLVED",
    "SUPPORTED",
    "CONTRADICTED",
    "CONFLICTED",
    "SUPPORTED_WITH_UNRESOLVED",
    "CONTRADICTED_WITH_UNRESOLVED",
]

ClaimRevisionStatus = Literal[
    "OPEN",
    "HYPOTHESIS",
    "EXPERIMENTALLY_SUPPORTED",
    "INFERENCE",
    "CONTRADICTED",
    "UNKNOWN",
    "CONFLICTED",
]


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


def _assessment_identity(assessment: HypothesisAssessment) -> str:
    return "assessment:" + _digest(
        {
            "hypothesis_key": assessment.hypothesis_key,
            "experiment_key": assessment.experiment_key,
            "relation": assessment.relation,
            "evidence_id": assessment.evidence_id,
            "scope": assessment.scope,
            "rationale": assessment.rationale,
        }
    )


@dataclass(frozen=True)
class ClaimSpec:
    key: str
    statement: str
    hypothesis_key: str
    scope: str = "research"

    def __post_init__(self) -> None:
        if not self.key or not self.statement or not self.hypothesis_key or not self.scope:
            raise ValueError("claim spec fields must be non-empty")
        if self.hypothesis_key not in {item.key for item in HYPOTHESES}:
            raise ValueError("claim spec references an unknown hypothesis")
        hypothesis_scope = next(item.scope for item in HYPOTHESES if item.key == self.hypothesis_key)
        if self.scope != hypothesis_scope:
            raise ValueError("claim scope does not match hypothesis scope")


@dataclass(frozen=True)
class ClaimEvidenceSynthesis:
    claim_key: str
    hypothesis_key: str
    scope: str
    disposition: ClaimSynthesisDisposition
    assessment_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    supporting_evidence_ids: tuple[str, ...]
    contradicting_evidence_ids: tuple[str, ...]
    unresolved_evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class ClaimRevisionRequest:
    claim_key: str
    parent_revision_id: str
    status: ClaimRevisionStatus
    rationale: str
    limitations: str
    next_discriminating_test: str
    evidence_ids: tuple[str, ...]
    assessment_ids: tuple[str, ...]


@dataclass(frozen=True)
class ClaimRevision:
    claim_key: str
    statement: str
    hypothesis_key: str
    scope: str
    status: ClaimRevisionStatus
    revision_id: str
    parent_revision_id: str
    evidence_ids: tuple[str, ...]
    assessment_ids: tuple[str, ...]
    supporting_evidence_ids: tuple[str, ...]
    contradicting_evidence_ids: tuple[str, ...]
    unresolved_evidence_ids: tuple[str, ...]
    rationale: str
    limitations: str
    next_discriminating_test: str


@dataclass(frozen=True)
class ClaimLedgerState:
    revisions: tuple[ClaimRevision, ...] = ()
    revision_id: str = "claims:genesis"

    def __post_init__(self) -> None:
        if not self.revision_id:
            raise ValueError("revision_id must be non-empty")
        ids = tuple(item.revision_id for item in self.revisions)
        if len(set(ids)) != len(ids):
            raise ValueError("claim revision ids must be unique")
        if self.revisions and ids[-1] != self.revision_id:
            raise ValueError("state revision_id must equal the latest claim revision")
        for index, revision in enumerate(self.revisions):
            expected_parent = "claims:genesis" if index == 0 else ids[index - 1]
            if revision.parent_revision_id != expected_parent:
                raise ValueError("claim revision parent chain is inconsistent")
            if revision.status not in {"OPEN", "HYPOTHESIS", "EXPERIMENTALLY_SUPPORTED", "INFERENCE", "CONTRADICTED", "UNKNOWN", "CONFLICTED"}:
                raise ValueError("invalid claim revision status")
        if not self.revisions and self.revision_id != "claims:genesis":
            raise ValueError("empty claim state must use the genesis revision id")

    def latest(self, claim_key: str) -> ClaimRevision | None:
        matches = [item for item in self.revisions if item.claim_key == claim_key]
        return matches[-1] if matches else None


@dataclass(frozen=True)
class ClaimLedgerRevision:
    status: Literal["APPLIED", "IDEMPOTENT_REPLAY"]
    parent_revision_id: str
    revision_id: str
    claim_revision: ClaimRevision | None
    state_after: ClaimLedgerState


def assessment_id(assessment: HypothesisAssessment) -> str:
    return _assessment_identity(assessment)


def synthesize_claim_evidence(
    frontier: AdaptiveFrontierState,
    claim: ClaimSpec,
) -> ClaimEvidenceSynthesis:
    relevant = tuple(
        item
        for item in frontier.assessments
        if item.hypothesis_key == claim.hypothesis_key and item.scope == claim.scope
    )
    relevant = tuple(
        sorted(
            relevant,
            key=lambda item: (
                item.evidence_id,
                item.experiment_key,
                item.relation,
                item.rationale,
            ),
        )
    )

    assessment_ids = tuple(_assessment_identity(item) for item in relevant)
    evidence_ids = tuple(sorted({item.evidence_id for item in relevant}))
    supporting = tuple(
        sorted({item.evidence_id for item in relevant if item.relation == "SUPPORTED"})
    )
    contradicting = tuple(
        sorted({item.evidence_id for item in relevant if item.relation == "CONTRADICTED"})
    )
    unresolved = tuple(
        sorted({item.evidence_id for item in relevant if item.relation == "UNRESOLVED"})
    )

    if not relevant:
        disposition: ClaimSynthesisDisposition = "NO_EVIDENCE"
    elif supporting and contradicting:
        disposition = "CONFLICTED"
    elif supporting and unresolved:
        disposition = "SUPPORTED_WITH_UNRESOLVED"
    elif contradicting and unresolved:
        disposition = "CONTRADICTED_WITH_UNRESOLVED"
    elif supporting:
        disposition = "SUPPORTED"
    elif contradicting:
        disposition = "CONTRADICTED"
    else:
        disposition = "UNRESOLVED"

    return ClaimEvidenceSynthesis(
        claim_key=claim.key,
        hypothesis_key=claim.hypothesis_key,
        scope=claim.scope,
        disposition=disposition,
        assessment_ids=assessment_ids,
        evidence_ids=evidence_ids,
        supporting_evidence_ids=supporting,
        contradicting_evidence_ids=contradicting,
        unresolved_evidence_ids=unresolved,
    )


def detect_claim_conflict(
    frontier: AdaptiveFrontierState,
    claim: ClaimSpec,
) -> ClaimEvidenceSynthesis:
    synthesis = synthesize_claim_evidence(frontier, claim)
    if synthesis.disposition == "CONFLICTED":
        return synthesis
    if synthesis.disposition in {"SUPPORTED_WITH_UNRESOLVED", "CONTRADICTED_WITH_UNRESOLVED"}:
        return synthesis
    return synthesis


def _validate_request_refs(
    frontier: AdaptiveFrontierState,
    claim: ClaimSpec,
    request: ClaimRevisionRequest,
    synthesis: ClaimEvidenceSynthesis,
) -> None:
    if request.claim_key != claim.key:
        raise ValueError("claim revision request targets a different claim")
    if not request.parent_revision_id:
        raise ValueError("parent_revision_id must be non-empty")
    if request.status not in {"OPEN", "HYPOTHESIS", "EXPERIMENTALLY_SUPPORTED", "INFERENCE", "CONTRADICTED", "UNKNOWN", "CONFLICTED"}:
        raise ValueError("invalid claim revision status")
    if not request.rationale or not request.limitations or not request.next_discriminating_test:
        raise ValueError("claim revision requires rationale, limitations, and next test")

    evidence_ids = tuple(sorted(set(request.evidence_ids)))
    assessment_ids = tuple(sorted(set(request.assessment_ids)))
    if request.evidence_ids != evidence_ids:
        raise ValueError("evidence_ids must be sorted and unique")
    if request.assessment_ids != assessment_ids:
        raise ValueError("assessment_ids must be sorted and unique")

    frontier_evidence = set(frontier.evidence_ids)
    if any(item not in frontier_evidence for item in request.evidence_ids):
        raise ValueError("claim revision references evidence outside the frontier")

    by_id = {_assessment_identity(item): item for item in frontier.assessments}
    if any(item not in by_id for item in request.assessment_ids):
        raise ValueError("claim revision references an assessment outside the frontier")

    selected = tuple(by_id[item] for item in request.assessment_ids)
    if any(
        item.hypothesis_key != claim.hypothesis_key or item.scope != claim.scope
        for item in selected
    ):
        raise ValueError("claim revision assessments do not match the claim")

    selected_evidence = {item.evidence_id for item in selected}
    if selected_evidence != set(request.evidence_ids):
        raise ValueError("claim revision evidence does not match its assessments")

    if (
        request.status in {"EXPERIMENTALLY_SUPPORTED", "CONTRADICTED", "CONFLICTED", "UNKNOWN"}
        and tuple(request.assessment_ids) != synthesis.assessment_ids
    ):
        raise ValueError(
            "decision-status claim revisions must account for the full current claim evidence set"
        )


def _validate_status_against_synthesis(
    status: ClaimRevisionStatus,
    synthesis: ClaimEvidenceSynthesis,
) -> None:
    if status == "EXPERIMENTALLY_SUPPORTED":
        if synthesis.disposition != "SUPPORTED":
            raise ValueError(
                "EXPERIMENTALLY_SUPPORTED requires unconflicted, fully identified support"
            )
    elif status == "INFERENCE":
        if synthesis.disposition not in {
            "SUPPORTED_WITH_UNRESOLVED",
            "CONTRADICTED_WITH_UNRESOLVED",
        }:
            raise ValueError(
                "INFERENCE requires partial or unresolved scoped evidence"
            )
    elif status == "CONTRADICTED":
        if synthesis.disposition != "CONTRADICTED":
            raise ValueError(
                "CONTRADICTED requires unconflicted, fully identified contradiction"
            )
    elif status == "CONFLICTED":
        if synthesis.disposition != "CONFLICTED":
            raise ValueError("CONFLICTED requires both supporting and contradicting evidence")
    elif status == "UNKNOWN":
        if synthesis.disposition not in {"NO_EVIDENCE", "UNRESOLVED"}:
            raise ValueError("UNKNOWN requires no identifying evidence or unresolved evidence")
    if status in {"OPEN", "HYPOTHESIS"}:
        return


def apply_claim_revision(
    state: ClaimLedgerState,
    frontier: AdaptiveFrontierState,
    claim: ClaimSpec,
    request: ClaimRevisionRequest,
) -> ClaimLedgerRevision:
    synthesis = synthesize_claim_evidence(frontier, claim)
    _validate_request_refs(frontier, claim, request, synthesis)

    _validate_status_against_synthesis(request.status, synthesis)

    revision_payload = {
        "claim_key": claim.key,
        "statement": claim.statement,
        "hypothesis_key": claim.hypothesis_key,
        "scope": claim.scope,
        "status": request.status,
        "parent_revision_id": request.parent_revision_id,
        "evidence_ids": list(request.evidence_ids),
        "assessment_ids": list(request.assessment_ids),
        "supporting_evidence_ids": list(synthesis.supporting_evidence_ids),
        "contradicting_evidence_ids": list(synthesis.contradicting_evidence_ids),
        "unresolved_evidence_ids": list(synthesis.unresolved_evidence_ids),
        "rationale": request.rationale,
        "limitations": request.limitations,
        "next_discriminating_test": request.next_discriminating_test,
    }
    revision_id = "claim-revision:" + _digest(revision_payload)

    existing = next(
        (item for item in state.revisions if item.revision_id == revision_id),
        None,
    )
    if existing is not None:
        return ClaimLedgerRevision(
            status="IDEMPOTENT_REPLAY",
            parent_revision_id=existing.parent_revision_id,
            revision_id=revision_id,
            claim_revision=None,
            state_after=state,
        )

    if request.parent_revision_id != state.revision_id:
        raise ValueError("claim revision parent does not match current claim ledger revision")

    latest = state.latest(claim.key)
    if latest is not None and (
        latest.statement != claim.statement
        or latest.hypothesis_key != claim.hypothesis_key
        or latest.scope != claim.scope
    ):
        raise ValueError("claim identity is immutable across revisions")

    revision = ClaimRevision(
        claim_key=claim.key,
        statement=claim.statement,
        hypothesis_key=claim.hypothesis_key,
        scope=claim.scope,
        status=request.status,
        revision_id=revision_id,
        parent_revision_id=request.parent_revision_id,
        evidence_ids=request.evidence_ids,
        assessment_ids=request.assessment_ids,
        supporting_evidence_ids=synthesis.supporting_evidence_ids,
        contradicting_evidence_ids=synthesis.contradicting_evidence_ids,
        unresolved_evidence_ids=synthesis.unresolved_evidence_ids,
        rationale=request.rationale,
        limitations=request.limitations,
        next_discriminating_test=request.next_discriminating_test,
    )

    state_after = ClaimLedgerState(
        revisions=state.revisions + (revision,),
        revision_id=revision_id,
    )
    return ClaimLedgerRevision(
        status="APPLIED",
        parent_revision_id=state.revision_id,
        revision_id=revision_id,
        claim_revision=revision,
        state_after=state_after,
    )


def claim_ledger_catalog_state(state: ClaimLedgerState) -> dict[str, object]:
    return {
        "revision_id": state.revision_id,
        "revisions": [
            {
                "claim_key": item.claim_key,
                "status": item.status,
                "revision_id": item.revision_id,
                "parent_revision_id": item.parent_revision_id,
                "hypothesis_key": item.hypothesis_key,
                "scope": item.scope,
                "evidence_ids": list(item.evidence_ids),
                "assessment_ids": list(item.assessment_ids),
                "supporting_evidence_ids": list(item.supporting_evidence_ids),
                "contradicting_evidence_ids": list(item.contradicting_evidence_ids),
                "unresolved_evidence_ids": list(item.unresolved_evidence_ids),
                "rationale": item.rationale,
                "limitations": item.limitations,
                "next_discriminating_test": item.next_discriminating_test,
            }
            for item in state.revisions
        ],
    }


def genesis_claim_ledger() -> ClaimLedgerState:
    return ClaimLedgerState()


__all__ = [
    "ClaimSynthesisDisposition",
    "ClaimRevisionStatus",
    "ClaimSpec",
    "ClaimEvidenceSynthesis",
    "ClaimRevisionRequest",
    "ClaimRevision",
    "ClaimLedgerState",
    "ClaimLedgerRevision",
    "assessment_id",
    "synthesize_claim_evidence",
    "detect_claim_conflict",
    "apply_claim_revision",
    "claim_ledger_catalog_state",
    "genesis_claim_ledger",
]
