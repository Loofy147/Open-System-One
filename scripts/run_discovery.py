from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from open_system_one.discovery import FailureObservation, build_plans  # noqa: E402


def render_receipt(payload: dict[str, object]) -> str:
    lines = [
        "# Discovery Run Receipt",
        "",
        "<!-- GENERATED FILE: scripts/run_discovery.py -->",
        "",
        "This receipt records structured observations and deterministic discovery planning. It is not evidence that any hypothesis is true.",
        "",
        "## Observation",
        "",
        "- tags: " + ", ".join(payload["observation"]["tags"]),
        "- evidence refs: " + ", ".join(payload["observation"]["evidence_refs"]),
        "- evidence gaps: " + ", ".join(payload["observation"]["evidence_gaps"]),
        "",
    ]
    for plan in payload["plans"]:
        lines.extend([
            "## Plan — " + plan["scope"],
            "",
            "Matches:",
            "",
        ])
        for match in plan["matches"]:
            lines.append(
                "- " + match["failure_class"] + ": matched "
                + ", ".join(match["matched_tags"]) + " (score="
                + str(match["score"]) + ")"
            )
        lines.extend(["", "Selected experiments:", ""])
        for exp in plan["experiments"]:
            lines.append("- " + exp["experiment"] + " — " + exp["reason"])
        lines.extend([
            "",
            "Mechanisms: " + " -> ".join(plan["mechanisms"]),
            "",
            "Hypotheses:",
            "",
        ])
        for hypothesis in plan["hypotheses"]:
            lines.append("- " + hypothesis)
        lines.extend(["", "Kill tests:", ""])
        for kill_test in plan["kill_tests"]:
            lines.append("- " + kill_test)
        lines.extend(["", "Evidence required: " + ", ".join(plan["evidence_required"]), ""])

    if not payload["plans"]:
        lines.extend([
            "## Result",
            "",
            "No registered failure class matched the supplied tags. Status: OPEN.",
            "",
        ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--evidence-gap", action="append", default=[])
    parser.add_argument("--out", default="research/discovery/runs/latest.json")
    args = parser.parse_args()

    if not args.tag:
        parser.error("at least one --tag is required")

    observation = FailureObservation(
        tags=tuple(args.tag),
        evidence_gaps=tuple(args.evidence_gap),
    )
    plans = build_plans(observation)
    payload = {
        "status": "DISCOVERY_PLAN_NOT_EVIDENCE",
        "observation": asdict(observation),
        "plans": [asdict(plan) for plan in plans],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    out.with_suffix(".md").write_text(render_receipt(payload), encoding="utf-8")
    print("generated: " + str(out))
    print("generated: " + str(out.with_suffix(".md")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
