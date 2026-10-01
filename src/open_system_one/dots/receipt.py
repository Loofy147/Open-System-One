from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any


STATUS_VALUES = {
    "ESTABLISHED",
    "EXPERIMENTALLY_SUPPORTED",
    "USER_REPORTED",
    "INFERENCE",
    "HYPOTHESIS",
    "CONTRADICTED",
    "UNKNOWN",
    "OPEN",
}


@dataclass(frozen=True)
class ActionRecord:
    action_id: str
    category: str
    target: str | None
    requested: bool
    executed: bool
    approved: bool
    outcome: str
    reversible: bool
    details: str | None = None


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    kind: str
    location: str
    sha256: str | None
    created: bool
    notes: str | None = None


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str
    action_id: str
    required: bool
    granted: bool
    actor: str
    timestamp: str
    scope: str


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    source: str
    source_ref: str | None
    observed_at: str
    disposition: str
    claim: str | None = None
    details: str | None = None


@dataclass(frozen=True)
class DotReceipt:
    schema_version: str
    task_id: str
    run_id: str
    recorded_at: str
    dot_id: str
    objective: str
    environment: dict[str, Any]
    permissions: dict[str, Any]
    actions: tuple[ActionRecord, ...] = field(default_factory=tuple)
    approvals: tuple[ApprovalRecord, ...] = field(default_factory=tuple)
    artifacts: tuple[ArtifactRecord, ...] = field(default_factory=tuple)
    evidence: tuple[EvidenceRecord, ...] = field(default_factory=tuple)
    verification_status: str = "OPEN"
    failures: tuple[str, ...] = field(default_factory=tuple)
    rollback: dict[str, Any] = field(default_factory=dict)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in ("actions", "approvals", "artifacts", "evidence", "failures", "notes"):
            if isinstance(data[key], tuple):
                data[key] = list(data[key])
        return data

    def canonical_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_receipt(
    *,
    task_id: str,
    run_id: str,
    dot_id: str,
    objective: str,
    environment: dict[str, Any] | None = None,
    permissions: dict[str, Any] | None = None,
    actions: list[ActionRecord] | None = None,
    approvals: list[ApprovalRecord] | None = None,
    artifacts: list[ArtifactRecord] | None = None,
    evidence: list[EvidenceRecord] | None = None,
    verification_status: str = "OPEN",
    failures: list[str] | None = None,
    rollback: dict[str, Any] | None = None,
    notes: list[str] | None = None,
) -> DotReceipt:
    receipt = DotReceipt(
        schema_version="dots-receipt-v0.1",
        task_id=task_id,
        run_id=run_id,
        recorded_at=now_utc(),
        dot_id=dot_id,
        objective=objective,
        environment=environment or {},
        permissions=permissions or {},
        actions=tuple(actions or []),
        approvals=tuple(approvals or []),
        artifacts=tuple(artifacts or []),
        evidence=tuple(evidence or []),
        verification_status=verification_status,
        failures=tuple(failures or []),
        rollback=rollback or {},
        notes=tuple(notes or []),
    )
    validate_receipt(receipt)
    return receipt


def validate_receipt(receipt: DotReceipt) -> None:
    required_strings = {
        "schema_version": receipt.schema_version,
        "task_id": receipt.task_id,
        "run_id": receipt.run_id,
        "recorded_at": receipt.recorded_at,
        "dot_id": receipt.dot_id,
        "objective": receipt.objective,
    }
    missing = [name for name, value in required_strings.items() if not value]
    if missing:
        raise ValueError(f"missing required receipt fields: {', '.join(missing)}")

    if receipt.verification_status not in STATUS_VALUES:
        raise ValueError(
            f"invalid verification_status={receipt.verification_status!r}"
        )

    action_ids = {a.action_id for a in receipt.actions}
    for approval in receipt.approvals:
        if approval.action_id not in action_ids:
            raise ValueError(
                f"approval {approval.approval_id!r} references unknown "
                f"action {approval.action_id!r}"
            )
        if not approval.timestamp:
            raise ValueError(f"approval {approval.approval_id!r} has no timestamp")

    evidence_ids = {e.evidence_id for e in receipt.evidence}
    if len(evidence_ids) != len(receipt.evidence):
        raise ValueError("duplicate evidence_id detected")

    artifact_ids = {a.artifact_id for a in receipt.artifacts}
    if len(artifact_ids) != len(receipt.artifacts):
        raise ValueError("duplicate artifact_id detected")
