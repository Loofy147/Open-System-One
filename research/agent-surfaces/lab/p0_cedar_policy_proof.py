#!/usr/bin/env python3
"""P0.05 Cedar proof: typed authorization decision on a fixed corpus."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

POLICY = """permit (
    principal == Agent::"agent-1",
    action == Action::"read_repository",
    resource == Repository::"repo-a"
);
"""

ENTITIES = "[]\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def authorize(
    cedar: str, policy: Path, entities: Path, action: str
) -> tuple[str, int]:
    proc = subprocess.run(
        [
            cedar,
            "authorize",
            "--policies",
            str(policy),
            "--entities",
            str(entities),
            "--principal",
            'Agent::"agent-1"',
            "--action",
            f'Action::"{action}"',
            "--resource",
            'Repository::"repo-a"',
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 2):
        raise RuntimeError(
            f"Cedar authorize failed rc={proc.returncode}: "
            f"{proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout.strip(), proc.returncode


def main() -> int:
    cedar = os.environ.get("CEDAR_BIN", "cedar")
    version_proc = subprocess.run(
        [cedar, "--version"], check=True, capture_output=True, text=True
    )
    cedar_version = version_proc.stdout.strip() or version_proc.stderr.strip()

    with tempfile.TemporaryDirectory(prefix="p0-cedar-") as td:
        root = Path(td)
        policy = root / "policy.cedar"
        entities = root / "entities.json"
        policy.write_text(POLICY, encoding="utf-8")
        entities.write_text(ENTITIES, encoding="utf-8")

        allow_raw, allow_rc = authorize(
            cedar, policy, entities, "read_repository"
        )
        deny_raw, deny_rc = authorize(
            cedar, policy, entities, "write_repository"
        )

        allow = allow_raw.splitlines()[0].strip()
        deny = deny_raw.splitlines()[0].strip()
        assert allow == "ALLOW" and allow_rc == 0, (allow_raw, allow_rc)
        assert deny == "DENY" and deny_rc == 2, (deny_raw, deny_rc)

        receipt = {
            "schema_version": "oss-p0-cedar-proof-v0.1",
            "status": "EXPERIMENTALLY_SUPPORTED",
            "test": "P0.05-Cedar",
            "runtime": {
                "cedar_version": cedar_version,
                "binary_sha256": sha256(Path(cedar).read_bytes()),
            },
            "policy": {
                "source_kind": "inline-test-fixture",
                "sha256": sha256(POLICY.encode("utf-8")),
            },
            "entities": {"sha256": sha256(ENTITIES.encode("utf-8"))},
            "cases": [
                {
                    "name": "allow",
                    "input_sha256": sha256(
                        b'Agent::"agent-1"|Action::"read_repository"|Repository::"repo-a"'
                    ),
                    "decision": "ALLOW",
                    "exit_code": allow_rc,
                },
                {
                    "name": "deny",
                    "input_sha256": sha256(
                        b'Agent::"agent-1"|Action::"write_repository"|Repository::"repo-a"'
                    ),
                    "decision": "DENY",
                    "exit_code": deny_rc,
                },
            ],
            "negative_test": {
                "mutation": "read_repository -> write_repository",
                "observed": "denied",
            },
            "scope": [
                "proves bounded typed authorization evaluation for the fixed corpus",
                "proves the harness distinguishes Cedar DENY (exit 2) from execution failure",
                "does not prove Open-System-One integration",
                "does not prove Cedar distributed deployment or HA behavior",
            ],
        }
        print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
