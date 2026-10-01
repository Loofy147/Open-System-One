#!/usr/bin/env python3
"""Deterministically regenerate the v0.3 opportunity-transition projection.

This tool intentionally keeps source opportunity records immutable. It reconstructs
only the transition-centric projection and marks reconstructed fields as inferred.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def parse_killed_table(audit: str) -> list[dict[str, str]]:
    start = audit.find("## 2. Re-audit of previous candidate set")
    end = audit.find("## 3. Candidate retained for decisive falsification")
    if start < 0 or end < 0 or end <= start:
        raise ValueError("audit candidate table boundaries not found")

    section = audit[start:end]
    rows: list[dict[str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0] == "Candidate":
            continue
        rows.append({"legacy_id": cells[0], "status": cells[1], "reason": cells[2]})
    return rows


def recipe_map(recipes: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in recipes["target_transition_recipes"]:
        legacy_id, target, representation_status = row
        out[legacy_id] = {
            "target_transition": target,
            "representation_status": representation_status,
        }
    return out


def build_current_transition(
    candidate: dict[str, Any], recipe: dict[str, Any]
) -> dict[str, Any]:
    return {
        "transition_id": f"bt-{candidate['candidate_id']}",
        "legacy_record_id": candidate["candidate_id"],
        "type": "RESEARCH_CANDIDATE",
        "source_basis": "CURRENT_OPPORTUNITY_STATE_2026-10-01.json",
        "representation_status": recipe["representation_status"],
        "observed_context": candidate.get("affected_user_context"),
        "pre_state": None,
        "trigger": None,
        "target_transition": recipe["target_transition"],
        "desired_delta": None,
        "problem_statement": candidate.get("problem_statement"),
        "strongest_incumbent_set": candidate.get("strongest_incumbent_set", []),
        "kill_test": candidate.get("kill_test"),
        "oracle": candidate.get("oracle"),
        "next_discriminating_action": candidate.get("next_discriminating_action"),
        "epistemic": {
            "problem": candidate.get("reality"),
            "residual_pain": candidate.get("residual_pain"),
            "gap": candidate.get("gap"),
            "desired_delta": "HYPOTHESIS",
            "target_transition": "INFERRED",
            "current_transition": "UNKNOWN",
        },
        "status": candidate.get("status"),
        "decision": None,
    }


def build_killed_transition(
    row: dict[str, str], recipe: dict[str, Any]
) -> dict[str, Any]:
    return {
        "transition_id": "bt-" + re.sub(r"[^a-z0-9]+", "-", row["legacy_id"].lower()).strip("-"),
        "legacy_record_id": row["legacy_id"],
        "type": "KILLED_CANDIDATE",
        "source_basis": "OPPORTUNITY_PORTFOLIO_AUDIT_2026-10-01.md",
        "representation_status": recipe["representation_status"],
        "target_transition": recipe["target_transition"],
        "desired_delta": None,
        "kill_reason": row["reason"],
        "status": row["status"],
        "epistemic": "INFERRED",
        "decision": row["status"],
    }


def regenerate(state: dict[str, Any], audit: str, recipes: dict[str, Any]) -> dict[str, Any]:
    recipes_by_id = recipe_map(recipes)

    current = []
    for candidate in state.get("candidates", []):
        legacy_id = candidate["candidate_id"]
        if legacy_id not in recipes_by_id:
            raise ValueError(f"missing recipe for current candidate: {legacy_id}")
        current.append(build_current_transition(candidate, recipes_by_id[legacy_id]))

    killed = []
    audit_rows = parse_killed_table(audit)
    for row in audit_rows:
        legacy_id = row["legacy_id"]
        if legacy_id not in recipes_by_id:
            raise ValueError(f"missing recipe for audited killed candidate: {legacy_id}")
        killed.append(build_killed_transition(row, recipes_by_id[legacy_id]))

    missing_source_current = set(
        c["candidate_id"] for c in state.get("candidates", [])
    ) - set(t["legacy_record_id"] for t in current)
    if missing_source_current:
        raise AssertionError(f"unmapped current candidates: {sorted(missing_source_current)}")

    return {
        "schema_version": "behavioral-transition-opportunity-projection-v0.3",
        "source_schema": state.get("schema_version"),
        "source_snapshot_id": "osone-opportunity-v0.2-2026-10-01",
        "mapping_version": recipes.get("mapping_version"),
        "representation_semantics": {
            "source_immutable": True,
            "reencoding_is_verification": False,
            "reencoding_is_new_evidence": False,
            "epistemic_upgrade_allowed": False,
        },
        "transitions": current + killed,
    }


def validate(output: dict[str, Any], state: dict[str, Any], audit: str) -> dict[str, Any]:
    errors: list[str] = []
    transitions = output["transitions"]

    if len({t["transition_id"] for t in transitions}) != len(transitions):
        errors.append("duplicate transition_id")

    source_current = [c["candidate_id"] for c in state.get("candidates", [])]
    mapped = [t["legacy_record_id"] for t in transitions]
    for cid in source_current:
        if cid not in mapped:
            errors.append(f"current candidate not mapped: {cid}")

    for t in transitions:
        if t.get("representation_status", "").startswith("INFERRED") and isinstance(t.get("epistemic"), dict):
            if t["epistemic"].get("target_transition") == "DIRECT_OBSERVATION":
                errors.append(f"inferred target marked direct: {t['transition_id']}")

    killed_rows = parse_killed_table(audit)
    killed_ids = {r["legacy_id"] for r in killed_rows}
    mapped_killed = {
        t["legacy_record_id"] for t in transitions if t["type"] == "KILLED_CANDIDATE"
    }
    if killed_ids != mapped_killed:
        errors.append("killed candidate accounting mismatch")

    return {
        "ok": not errors,
        "errors": errors,
        "transition_count": len(transitions),
        "current_candidate_count": len(source_current),
        "killed_candidate_count": len(killed_rows),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True, type=Path)
    ap.add_argument("--audit", required=True, type=Path)
    ap.add_argument("--recipes", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    state = load_json(args.state)
    audit = load_text(args.audit)
    recipes = load_json(args.recipes)

    projection = regenerate(state, audit, recipes)
    validation = validate(projection, state, audit)
    projection["validation"] = validation
    projection["canonical_digest_input"] = canonical_json(projection)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(projection, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if not validation["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
