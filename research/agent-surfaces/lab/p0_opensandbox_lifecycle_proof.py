#!/usr/bin/env python3
"""P0.02 OpenSandbox lifecycle proof using the Docker runtime."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import timedelta

from opensandbox import SandboxSync
from opensandbox.config import ConnectionConfigSync


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run() -> dict:
    domain = os.environ.get("OPEN_SANDBOX_DOMAIN", "localhost:8080")
    config = ConnectionConfigSync(
        domain=domain,
        request_timeout=timedelta(seconds=30),
    )

    sandbox = SandboxSync.create(
        "alpine:3.20",
        connection_config=config,
        timeout=timedelta(minutes=5),
        ready_timeout=timedelta(seconds=60),
    )

    sandbox_id = sandbox.id
    lifecycle = []
    artifact_bytes = b""

    try:
        info = sandbox.get_info()
        lifecycle.append({"operation": "create", "state": info.status.state})
        assert info.status.state == "Running", info

        execution = sandbox.commands.run(
            ["sh", "-c", "printf 'open-system-one-p0.02\\n' > /tmp/p0-artifact.txt && cat /tmp/p0-artifact.txt"]
        )
        output = "".join(message.text for message in execution.logs.stdout)
        assert output == "open-system-one-p0.02\n", output
        lifecycle.append(
            {
                "operation": "execute",
                "exit_code": getattr(execution, "exit_code", None),
                "output": output,
            }
        )

        artifact_bytes = sandbox.files.read_bytes("/tmp/p0-artifact.txt")
        assert artifact_bytes == b"open-system-one-p0.02\n"
        lifecycle.append(
            {
                "operation": "collect_artifact",
                "path": "/tmp/p0-artifact.txt",
                "sha256": sha256_bytes(artifact_bytes),
                "size": len(artifact_bytes),
            }
        )

        post_exec = sandbox.get_info()
        lifecycle.append(
            {"operation": "inspect_after_execute", "state": post_exec.status.state}
        )
        assert post_exec.status.state == "Running", post_exec
    finally:
        sandbox.destroy()

    negative = "not-run"
    try:
        sandbox.commands.run(["true"])
    except Exception as exc:
        negative = type(exc).__name__
    assert negative != "not-run", "destroyed sandbox accepted a new command"

    return {
        "schema_version": "oss-p0-opensandbox-proof-v0.1",
        "status": "EXPERIMENTALLY_SUPPORTED",
        "test": "P0.02-OpenSandbox",
        "source_ref": {
            "repository": "opensandbox-group/OpenSandbox",
            "release": "release-1.1.0",
            "release_tag_object": "836b182e208e66c046026fa0f633e089321f1efb",
            "release_commit": "b1a29cf93a823a95913f7943010febb3f29de05c",
            "inspected_current_commit": "c7dc78a4090e5de2b9119e9bd93952cae24f87bd",
        },
        "runtime": {
            "server_config": {
                "runtime": "docker",
                "execd_image": "opensandbox/execd:v1.1.0",
                "store": "sqlite",
            },
            "sandbox_image": "alpine:3.20",
            "domain": domain,
        },
        "sandbox": {
            "id": sandbox_id,
            "lifecycle": lifecycle,
            "terminal_verification": {
                "post_destroy_command_attempt": negative,
                "observed": "destroyed_handle_rejected_command",
            },
        },
        "artifact": {
            "path": "/tmp/p0-artifact.txt",
            "sha256": sha256_bytes(artifact_bytes),
            "size": len(artifact_bytes),
            "content": artifact_bytes.decode("utf-8"),
        },
        "negative_test": {
            "mutation": "destroy -> attempt command on destroyed handle",
            "observed": negative,
        },
        "scope": [
            "proves create/inspect/execute/read-artifact/destroy through the Docker-backed OpenSandbox SDK",
            "proves a destroyed handle rejects a subsequent command",
            "does not prove Kubernetes runtime behavior",
            "does not prove credential vault or network egress policy behavior",
            "does not prove Open-System-One integration",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
