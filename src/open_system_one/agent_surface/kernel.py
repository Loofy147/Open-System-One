from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Iterable


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


@dataclass(frozen=True)
class CapabilityRequest:
    run_id: str
    subject: str
    capability: str
    target: str
    purpose: str
    idempotency_key: str
    side_effect: bool = False


@dataclass(frozen=True)
class ExecutionObservation:
    run_id: str
    outcome: str
    exit_code: int | None
    stdout: str
    stderr: str
    artifact_sha256: str | None
    artifact_path: str | None
    target: str
    decision: Decision
    decision_reason: str


@dataclass(frozen=True)
class PolicyRule:
    subject: str
    capability: str
    target: str
    allow: bool


@dataclass
class RelationStore:
    """Minimal relation store: grant/revoke is state, not reachability."""

    _relations: set[tuple[str, str, str]] = field(default_factory=set)

    def grant(self, subject: str, capability: str, target: str) -> None:
        self._relations.add((subject, capability, target))

    def revoke(self, subject: str, capability: str, target: str) -> None:
        self._relations.discard((subject, capability, target))

    def permits(self, subject: str, capability: str, target: str) -> bool:
        return (subject, capability, target) in self._relations


class CapabilityKernel:
    """Native request -> policy -> approval -> execution -> observation."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(
            root or tempfile.mkdtemp(prefix="open-system-one-kernel-")
        ).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.relations = RelationStore()
        self._rules: set[PolicyRule] = set()
        self._approved_runs: set[str] = set()
        self._executed_keys: dict[str, ExecutionObservation] = {}

    def add_rule(
        self, *, subject: str, capability: str, target: str, allow: bool = True
    ) -> None:
        self._rules.add(PolicyRule(subject, capability, target, allow))

    def grant(self, *, subject: str, capability: str, target: str) -> None:
        self.relations.grant(subject, capability, target)

    def revoke(self, *, subject: str, capability: str, target: str) -> None:
        self.relations.revoke(subject, capability, target)

    def approve(self, run_id: str) -> None:
        self._approved_runs.add(run_id)

    def decide(self, request: CapabilityRequest) -> tuple[Decision, str]:
        rule = PolicyRule(request.subject, request.capability, request.target, True)
        explicitly_allowed = rule in self._rules
        relation_allowed = self.relations.permits(
            request.subject, request.capability, request.target
        )
        if not (explicitly_allowed and relation_allowed):
            return Decision.DENY, "policy_or_relation_denied"

        if request.side_effect and request.run_id not in self._approved_runs:
            return Decision.APPROVAL_REQUIRED, "explicit_approval_required"

        return Decision.ALLOW, "policy_and_relation_allowed"

    def execute(
        self,
        request: CapabilityRequest,
        command: Iterable[str],
        *,
        artifact_relative_path: str | None = None,
    ) -> ExecutionObservation:
        # Revalidate authority before replay. A cached observation must never
        # resurrect authority that was later revoked.
        decision, reason = self.decide(request)
        if decision is not Decision.ALLOW:
            raise PermissionError(f"{decision.value}: {reason}")

        cached = self._executed_keys.get(request.idempotency_key)
        if cached is not None:
            return cached

        argv = list(command)
        if not argv:
            raise ValueError("command must not be empty")

        # This executor fixes the process working root. It is not an OS sandbox;
        # hardened isolation remains an external capability behind this boundary.
        proc = subprocess.run(
            argv,
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

        artifact_sha256 = None
        artifact_path = None
        if artifact_relative_path is not None:
            candidate = (self.root / artifact_relative_path).resolve()
            candidate.relative_to(self.root)
            data = candidate.read_bytes()
            artifact_sha256 = hashlib.sha256(data).hexdigest()
            artifact_path = str(candidate.relative_to(self.root))

        observation = ExecutionObservation(
            run_id=request.run_id,
            outcome="completed" if proc.returncode == 0 else "failed",
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            artifact_sha256=artifact_sha256,
            artifact_path=artifact_path,
            target=request.target,
            decision=decision,
            decision_reason=reason,
        )
        self._executed_keys[request.idempotency_key] = observation
        return observation

    def receipt(
        self, request: CapabilityRequest, observation: ExecutionObservation
    ) -> dict:
        payload = {
            "schema_version": "agent-surface-receipt-v0.1",
            "run_id": request.run_id,
            "subject": request.subject,
            "capability": request.capability,
            "target": request.target,
            "purpose": request.purpose,
            "idempotency_key": request.idempotency_key,
            "authorization_at_execution": {
                "decision": observation.decision.value,
                "reason": observation.decision_reason,
            },
            "observation": {
                "outcome": observation.outcome,
                "exit_code": observation.exit_code,
                "stdout_sha256": hashlib.sha256(
                    observation.stdout.encode()
                ).hexdigest(),
                "stderr_sha256": hashlib.sha256(
                    observation.stderr.encode()
                ).hexdigest(),
                "artifact_sha256": observation.artifact_sha256,
                "artifact_path": observation.artifact_path,
            },
            "replay": {
                "idempotency_key": request.idempotency_key,
                "same_observation_on_retry": (
                    self._executed_keys.get(request.idempotency_key) == observation
                ),
            },
        }
        payload["receipt_sha256"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return payload
