#!/usr/bin/env python3
"""Direct proof for the native Capability Kernel."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from open_system_one.agent_surface import CapabilityKernel, CapabilityRequest, Decision


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="open-system-one-native-proof-") as td:
        root = Path(td)
        kernel = CapabilityKernel(root)
        kernel.add_rule(subject="agent-1", capability="read_repository", target="repo-a")
        kernel.grant(subject="agent-1", capability="read_repository", target="repo-a")

        request = CapabilityRequest(
            run_id="native-p0-run-001",
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
            purpose="native kernel proof",
            idempotency_key="native-proof-key",
        )

        allow, allow_reason = kernel.decide(request)
        assert allow is Decision.ALLOW
        assert allow_reason == "policy_and_relation_allowed"

        artifact = root / "artifact.txt"
        artifact.write_text("native-kernel-proof\n", encoding="utf-8")

        first = kernel.execute(
            request,
            ["python", "-c", "print(open('artifact.txt').read(), end='')"],
            artifact_relative_path="artifact.txt",
        )
        replay = kernel.execute(
            request,
            ["python", "-c", "print('SHOULD-NOT-EXECUTE')"],
            artifact_relative_path="artifact.txt",
        )
        assert replay == first

        side_effect_request = CapabilityRequest(
            run_id="native-p0-side-effect",
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
            purpose="approval boundary proof",
            idempotency_key="native-side-effect-key",
            side_effect=True,
        )
        pending, pending_reason = kernel.decide(side_effect_request)
        assert pending is Decision.APPROVAL_REQUIRED
        assert pending_reason == "explicit_approval_required"
        kernel.approve(side_effect_request.run_id)
        approved, _ = kernel.decide(side_effect_request)
        assert approved is Decision.ALLOW

        kernel.revoke(subject="agent-1", capability="read_repository", target="repo-a")
        revoked, revoked_reason = kernel.decide(request)
        assert revoked is Decision.DENY
        assert revoked_reason == "policy_or_relation_denied"

        try:
            kernel.execute(
                request,
                ["python", "-c", "print('SHOULD-NOT-RUN')"],
                artifact_relative_path="artifact.txt",
            )
        except PermissionError as exc:
            replay_after_revoke = str(exc)
        else:
            raise AssertionError("revoked request was replayed")

        receipt = kernel.receipt(request, first)
        assert receipt["authorization_at_execution"]["decision"] == "ALLOW"
        assert receipt["replay"]["same_observation_on_retry"] is True
        assert len(receipt["receipt_sha256"]) == 64

        print(json.dumps({
            "schema_version": "native-capability-kernel-proof-v0.1",
            "status": "EXPERIMENTALLY_SUPPORTED",
            "checks": {
                "policy_and_relation_intersection": allow.value,
                "same_authority_idempotency": replay == first,
                "approval_boundary": pending.value,
                "revocation": revoked.value,
                "revoked_replay": replay_after_revoke,
                "historical_receipt_authorization": receipt["authorization_at_execution"],
                "artifact_sha256": receipt["observation"]["artifact_sha256"],
                "receipt_sha256": receipt["receipt_sha256"],
            },
            "scope": [
                "native control-plane contract only",
                "local subprocess executor is not an OS sandbox",
                "external hardened runtimes remain replaceable adapters",
            ],
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
