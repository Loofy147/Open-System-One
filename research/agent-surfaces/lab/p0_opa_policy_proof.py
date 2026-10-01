#!/usr/bin/env python3
"""P0.03 OPA proof: deterministic allow/deny with reconstructible evidence."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

POLICY = """package agent.authz

decision := {"allow": true, "reason": "allowed"} if {
    input.subject == "agent-1"
    input.capability == "read_repository"
    input.resource == "repo-a"
}

decision := {"allow": false, "reason": "denied"} if not {
    input.subject == "agent-1"
    input.capability == "read_repository"
    input.resource == "repo-a"
}
"""

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run_eval(opa: str, policy: Path, input_path: Path) -> dict:
    proc = subprocess.run(
        [opa, "eval", "--format=json", "--data", str(policy),
         "--input", str(input_path), "data.agent.authz.decision"],
        check=True, capture_output=True, text=True,
    )
    payload = json.loads(proc.stdout)
    return payload["result"][0]["expressions"][0]["value"]

def main() -> int:
    opa = os.environ.get("OPA_BIN", "opa")
    opa_version = subprocess.run(
        [opa, "version"], check=True, capture_output=True, text=True
    ).stdout.strip()

    allow_input = {"subject": "agent-1", "capability": "read_repository", "resource": "repo-a"}
    deny_input = {"subject": "agent-1", "capability": "write_repository", "resource": "repo-a"}

    with tempfile.TemporaryDirectory(prefix="p0-opa-") as td:
        root = Path(td)
        policy = root / "policy.rego"
        allow_path = root / "allow.json"
        deny_path = root / "deny.json"
        policy.write_text(POLICY, encoding="utf-8")
        allow_path.write_text(json.dumps(allow_input, sort_keys=True), encoding="utf-8")
        deny_path.write_text(json.dumps(deny_input, sort_keys=True), encoding="utf-8")

        allow = run_eval(opa, policy, allow_path)
        deny = run_eval(opa, policy, deny_path)

        assert allow == {"allow": True, "reason": "allowed"}, allow
        assert deny == {"allow": False, "reason": "denied"}, deny

        receipt = {
            "schema_version": "oss-p0-opa-proof-v0.1",
            "status": "EXPERIMENTALLY_SUPPORTED",
            "test": "P0.03-OPA",
            "runtime": {
                "opa_version": opa_version,
                "binary_sha256": sha256_bytes(Path(opa).read_bytes()),
            },
            "policy": {
                "source_kind": "inline-test-fixture",
                "sha256": sha256_bytes(POLICY.encode("utf-8")),
            },
            "cases": [
                {"name": "allow", "input_sha256": sha256_bytes(json.dumps(allow_input, sort_keys=True).encode("utf-8")), "decision": allow},
                {"name": "deny", "input_sha256": sha256_bytes(json.dumps(deny_input, sort_keys=True).encode("utf-8")), "decision": deny},
            ],
            "negative_test": {"mutation": "read_repository -> write_repository", "observed": "denied"},
            "scope": [
                "proves deterministic external policy evaluation for the fixed corpus",
                "does not prove Open-System-One integration",
                "does not prove distributed OPA deployment or HA behavior",
            ],
        }
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
