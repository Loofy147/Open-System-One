#!/usr/bin/env python3
"""P0.04 OpenFGA relation authorization proof."""

from __future__ import annotations

import hashlib
import json
import os
import urllib.request

BASE = os.environ.get("OPENFGA_URL", "http://127.0.0.1:8080")
MODEL = {
    "schema_version": "1.1",
    "type_definitions": [
        {"type": "user"},
        {
            "type": "document",
            "relations": {"reader": {"this": {}}},
            "metadata": {
                "relations": {
                    "reader": {
                        "directly_related_user_types": [{"type": "user"}]
                    }
                }
            },
        },
    ],
}


def sha256_json(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def request(method: str, path: str, payload: object | None = None) -> tuple[int, dict]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read()
        return resp.status, json.loads(body or b"{}")


def main() -> int:
    _, health = request("GET", "/healthz")
    assert health.get("status") == "SERVING", health

    _, store = request("POST", "/stores", {"name": "open-system-one-p0-04"})
    store_id = store["id"]

    _, model = request("POST", f"/stores/{store_id}/authorization-models", MODEL)
    model_id = model["authorization_model_id"]

    tuple_key = {
        "user": "user:agent-1",
        "relation": "reader",
        "object": "document:repo-a",
    }
    _, write_result = request(
        "POST",
        f"/stores/{store_id}/write",
        {"writes": {"tuple_keys": [tuple_key]}},
    )

    def check(user: str) -> bool:
        _, result = request(
            "POST",
            f"/stores/{store_id}/check",
            {"tuple_key": {
                "user": user,
                "relation": "reader",
                "object": "document:repo-a",
            }},
        )
        return result["allowed"] is True

    allowed_before = check("user:agent-1")
    denied_other_user = check("user:other")

    request(
        "POST",
        f"/stores/{store_id}/write",
        {"deletes": {"tuple_keys": [tuple_key]}},
    )
    allowed_after_revoke = check("user:agent-1")

    assert allowed_before is True
    assert denied_other_user is False
    assert allowed_after_revoke is False

    receipt = {
        "schema_version": "oss-p0-openfga-proof-v0.1",
        "status": "EXPERIMENTALLY_SUPPORTED",
        "test": "P0.04-OpenFGA",
        "source_ref": {
            "repository": "openfga/openfga",
            "inspected_commit": "97943bf64d85ac3015272d90ab1145696db9ef5b",
            "runtime_release": "v1.21.0",
        },
        "runtime": {"health": health, "base_url": BASE},
        "store": {
            "id": store_id,
            "model_id": model_id,
            "model_sha256": sha256_json(MODEL),
        },
        "cases": {
            "allow_after_grant": allowed_before,
            "deny_other_user": denied_other_user,
            "deny_after_revoke": allowed_after_revoke,
        },
        "write_response": write_result,
        "negative_test": {
            "mutation": "delete user:agent-1 reader relation",
            "observed": "authorization revoked",
        },
        "scope": [
            "proves OpenFGA relation-based authorization over HTTP for the fixed corpus",
            "proves tuple deletion revokes the authorization",
            "does not prove Open-System-One integration",
            "does not prove distributed storage, HA, or external SDK behavior",
        ],
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
