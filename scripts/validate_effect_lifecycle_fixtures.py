#!/usr/bin/env python3
"""Validate the draft effect identity, attempt, and reconciliation contract fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
FIXTURE_PATH = ROOT / "research" / "conformance" / "effect-lifecycle-fixtures.v0.1.json"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def pointer_parent(document: dict[str, Any], pointer: str) -> tuple[dict[str, Any], str]:
    if not pointer.startswith("/"):
        raise AssertionError(f"Only absolute JSON pointers are supported: {pointer}")
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    parent: Any = document
    for part in parts[:-1]:
        if not isinstance(parent, dict) or part not in parent:
            raise AssertionError(f"JSON pointer does not exist: {pointer}")
        parent = parent[part]
    if not isinstance(parent, dict):
        raise AssertionError(f"Mutation parent must be an object: {pointer}")
    return parent, parts[-1]


def apply_mutations(document: dict[str, Any], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    result = json.loads(json.dumps(document))
    for mutation in mutations:
        parent, key = pointer_parent(result, mutation["path"])
        operation = mutation["op"]
        if operation == "remove":
            if key not in parent:
                raise AssertionError(f"Cannot remove missing property: {mutation['path']}")
            del parent[key]
        elif operation == "replace":
            if key not in parent:
                raise AssertionError(f"Cannot replace missing property: {mutation['path']}")
            parent[key] = mutation["value"]
        elif operation == "add":
            if key in parent:
                raise AssertionError(f"Cannot add existing property: {mutation['path']}")
            parent[key] = mutation["value"]
        else:
            raise AssertionError(f"Unsupported mutation operation: {operation}")
    return result


def assert_valid(validator: Draft202012Validator, value: dict[str, Any], label: str) -> None:
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.absolute_path))
    if errors:
        rendered = "; ".join(
            f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise AssertionError(f"{label} expected VALID, got: {rendered}")


def assert_invalid(validator: Draft202012Validator, value: dict[str, Any], label: str) -> None:
    if validator.is_valid(value):
        raise AssertionError(f"{label} expected INVALID but schema accepted it")


def canonical_parameter_digest(parameters: dict[str, str]) -> str:
    import hashlib

    payload = bytearray()
    for key in sorted(parameters, key=lambda item: item.encode("utf-8")):
        key_bytes = key.encode("utf-8")
        value_bytes = parameters[key].encode("utf-8")
        payload.extend(str(len(key_bytes)).encode("ascii"))
        payload.extend(b":")
        payload.extend(key_bytes)
        payload.extend(str(len(value_bytes)).encode("ascii"))
        payload.extend(b":")
        payload.extend(value_bytes)
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def validate_kernel_unknown_v03(identity_validator: Draft202012Validator) -> None:
    path = ROOT / "research" / "conformance" / "kernel-conformance-fixtures.v0.3.json"
    document = read_json(path)
    if document.get("schema") != "open_system_one.kernel_conformance_fixtures.v0.3":
        raise AssertionError("kernel fixture schema must be v0.3")

    case = next(item for item in document["cases"] if item["id"] == "K-UNKNOWN-01")
    vector = case["test_vectors"][0]
    if vector.get("schema") != "open_system_one.unknown_effect_test_vector.v0.2":
        raise AssertionError("K-UNKNOWN vector schema mismatch")
    if len(vector["steps"]) != 9:
        raise AssertionError("K-UNKNOWN vector must contain exactly nine steps")

    for effect_ref, effect in vector["effects"].items():
        identity = {
            "schema": "open_system_one.effect_identity.v0.1",
            "effect_id": effect["effect_id"],
            "run_id": effect["run_id"],
            "capability_id": effect["capability_id"],
            "action_id": effect["action_id"],
            "action_version": effect["action_version"],
            "scope": effect["scope"],
            "attributed_to": effect["attributed_to"],
            "parameters_digest": effect["parameters_digest"],
        }
        assert_valid(identity_validator, identity, f"K-UNKNOWN:{effect_ref}:identity")
        if effect["parameters_digest"] != canonical_parameter_digest(effect["parameters"]):
            raise AssertionError(f"K-UNKNOWN:{effect_ref}: parameters_digest mismatch")
        if effect.get("attempt_number") != 1 or not effect.get("attempt_id"):
            raise AssertionError(f"K-UNKNOWN:{effect_ref}: initial attempt identity missing")

    latest_status: dict[str, str] = {}
    record_counts: dict[str, int] = {}
    attempt_numbers: dict[str, int] = {}
    seen_attempt_ids: set[str] = set()

    for index, step in enumerate(vector["steps"], start=1):
        effect = vector["effects"][step["effect_ref"]]
        effect_id = effect["effect_id"]
        status = latest_status.get(effect_id)
        count = record_counts.get(effect_id, 0)
        operation = step["op"]

        if operation == "reserve":
            attempt_id = step.get("attempt_id") or effect.get("attempt_id")
            attempt_number = step.get("attempt_number") or effect.get("attempt_number")
            if not attempt_id or not attempt_number:
                raise AssertionError(f"K-UNKNOWN step {index}: reservation attempt metadata missing")
            previous_attempt = attempt_numbers.get(effect_id, 0)
            if attempt_id in seen_attempt_ids or attempt_number != previous_attempt + 1:
                raise AssertionError(f"K-UNKNOWN step {index}: reused or non-monotonic attempt identity")
            if status is None or status == "CONFIRMED_NOT_EXECUTED":
                seen_attempt_ids.add(attempt_id)
                attempt_numbers[effect_id] = attempt_number
                latest_status[effect_id] = "RESERVED"
                record_counts[effect_id] = count + 1
                actual_result = "RESERVED"
            else:
                actual_result = "REPLAY_BLOCKED"
        elif operation == "mark_unknown":
            if status != "RESERVED":
                raise AssertionError(f"K-UNKNOWN step {index}: mark_unknown without RESERVED")
            latest_status[effect_id] = "UNKNOWN"
            record_counts[effect_id] = count + 1
            actual_result = "UNKNOWN"
        elif operation == "reconcile":
            if status != "UNKNOWN":
                raise AssertionError(f"K-UNKNOWN step {index}: reconciliation without UNKNOWN")
            decision = step["decision"]
            if decision not in ("CONFIRMED_COMPLETED", "CONFIRMED_NOT_EXECUTED"):
                raise AssertionError(f"K-UNKNOWN step {index}: invalid reconciliation decision")
            latest_status[effect_id] = (
                "COMPLETED" if decision == "CONFIRMED_COMPLETED" else "CONFIRMED_NOT_EXECUTED"
            )
            record_counts[effect_id] = count + 1
            actual_result = "RECONCILED"
        else:
            raise AssertionError(f"K-UNKNOWN step {index}: unsupported operation {operation}")

        actual_status = latest_status.get(effect_id)
        delta = record_counts.get(effect_id, 0) - count
        expected = step["expected"]
        if (actual_result, actual_status, delta) != (
            expected["result"], expected["status"], expected["record_count_delta"]
        ):
            raise AssertionError(
                f"K-UNKNOWN step {index} mismatch: "
                f"{(actual_result, actual_status, delta)!r} != "
                f"{(expected['result'], expected['status'], expected['record_count_delta'])!r}"
            )

    print("PASS kernel-conformance:K-UNKNOWN-01-V2")
    

def main() -> None:
    identity_schema = read_json(SCHEMA_DIR / "effect-identity.v0.1.json")
    attempt_schema = read_json(SCHEMA_DIR / "effect-attempt.v0.1.json")
    attestation_schema = read_json(SCHEMA_DIR / "effect-reconciliation-attestation.v0.1.json")
    fixtures = read_json(FIXTURE_PATH)

    for label, schema in (
        ("identity", identity_schema),
        ("attempt", attempt_schema),
        ("reconciliation attestation", attestation_schema),
    ):
        Draft202012Validator.check_schema(schema)
        print(f"PASS schema:{label}")

    registry = Registry().with_resource(
        identity_schema["$id"],
        Resource.from_contents(identity_schema),
    )
    format_checker = FormatChecker()
    identity_validator = Draft202012Validator(identity_schema, format_checker=format_checker)
    attempt_validator = Draft202012Validator(
        attempt_schema, registry=registry, format_checker=format_checker
    )
    attestation_validator = Draft202012Validator(
        attestation_schema, registry=registry, format_checker=format_checker
    )

    valid_identity = fixtures["valid_identity"]
    assert_valid(identity_validator, valid_identity, "valid_identity")

    for case in fixtures["identity_cases"]:
        candidate = (
            valid_identity
            if case.get("identity_ref") == "valid_identity"
            else apply_mutations(valid_identity, case.get("mutations", []))
        )
        expected = case["expected"]
        if expected == "VALID":
            assert_valid(identity_validator, candidate, case["id"])
        elif expected == "INVALID":
            assert_invalid(identity_validator, candidate, case["id"])
        elif expected == "IDENTITY_CONFLICT":
            assert_valid(identity_validator, candidate, case["id"] + ":shape")
            if candidate["effect_id"] != valid_identity["effect_id"]:
                raise AssertionError(f"{case['id']} must preserve effect_id")
            immutable_fields = (
                "run_id", "capability_id", "action_id", "action_version",
                "scope", "attributed_to", "parameters_digest",
            )
            if not any(candidate[field] != valid_identity[field] for field in immutable_fields):
                raise AssertionError(f"{case['id']} did not mutate immutable identity")
        else:
            raise AssertionError(f"Unknown identity expectation: {expected}")
        print(f"PASS identity:{case['id']}")

    valid_attempt = fixtures["valid_attempt"]
    assert_valid(attempt_validator, valid_attempt, "valid_attempt")
    attempts = fixtures["attempt_cases"]
    for case in attempts:
        if case["id"] == "EA-NEW-ATTEMPT":
            first, second = case["attempt_1"], case["attempt_2"]
            if first["attempt_id"] == second["attempt_id"]:
                raise AssertionError("new attempt must use a fresh attempt_id")
            if second["attempt_number"] != first["attempt_number"] + 1:
                raise AssertionError("new attempt number must increase by exactly one")
        elif case["id"] == "EA-REUSED-ATTEMPT-ID":
            first, second = case["attempt_1"], case["attempt_2"]
            if first["attempt_id"] != second["attempt_id"]:
                raise AssertionError("fixture must actually reuse attempt_id")
            if case["expected"] != "INVALID":
                raise AssertionError("reused attempt_id must be invalid")
        else:
            raise AssertionError(f"Unknown attempt fixture: {case['id']}")
        print(f"PASS attempt:{case['id']}")

    valid_attestation = fixtures["valid_attestation"]
    assert_valid(attestation_validator, valid_attestation, "valid_attestation")
    for case in fixtures["reconciliation_cases"]:
        candidate = (
            valid_attestation
            if case.get("attestation_ref") == "valid_attestation"
            else apply_mutations(valid_attestation, case.get("mutations", []))
        )
        expected = case["expected"]
        if expected in ("RESOLVE_COMPLETED", "RESOLVE_CONFIRMED_NOT_EXECUTED", "REMAIN_UNKNOWN"):
            assert_valid(attestation_validator, candidate, case["id"])
            if expected == "REMAIN_UNKNOWN" and candidate["decision"] != "UNRESOLVED":
                raise AssertionError(f"{case['id']} must preserve UNKNOWN")
        elif expected == "INVALID":
            assert_invalid(attestation_validator, candidate, case["id"])
        elif expected == "REJECT_STALE_ATTESTATION":
            assert_valid(attestation_validator, candidate, case["id"] + ":shape")
            if case["attestation_attempt_id"] == case["current_attempt_id"]:
                raise AssertionError("stale-attestation fixture must use different attempt IDs")
            if candidate["attempt_id"] != case["attestation_attempt_id"]:
                raise AssertionError("stale-attestation fixture does not match attestation")
        else:
            raise AssertionError(f"Unknown reconciliation expectation: {expected}")
        print(f"PASS reconciliation:{case['id']}")

    machine = fixtures["state_machine"]
    legal = {(item["from"], item["to"]) for item in machine["legal_transitions"]}
    required = {
        ("RESERVED", "COMPLETED"),
        ("RESERVED", "UNKNOWN"),
        ("UNKNOWN", "COMPLETED"),
        ("UNKNOWN", "CONFIRMED_NOT_EXECUTED"),
    }
    if legal != required:
        raise AssertionError(f"Legal transition set mismatch: {legal!r}")
    forbidden = {
        ("UNKNOWN", "RESERVED"),
        ("COMPLETED", "UNKNOWN"),
        ("COMPLETED", "RESERVED"),
        ("CONFIRMED_NOT_EXECUTED", "COMPLETED"),
    }
    if legal.intersection(forbidden):
        raise AssertionError("Forbidden transition is marked legal")
    print("PASS state-machine:legal-and-forbidden-transitions")

    validate_kernel_unknown_v03(identity_validator)
    print("PASS effect lifecycle contract fixtures")


if __name__ == "__main__":
    main()
