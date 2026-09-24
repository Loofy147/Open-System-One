from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from open_system_one.discovery_advanced import catalog

MD_PATH = ROOT / "docs" / "ADAPTIVE_DISCOVERY.md"


def render(data: dict[str, object]) -> str:
    lines = [
        "# Adaptive Discovery v0.1",
        "",
        "<!-- GENERATED FILE: scripts/build_adaptive_discovery_docs.py -->",
        "",
        "This is NON-CANONICAL research infrastructure.",
        "",
        "## Purpose",
        "",
        "Convert structured evidence into failure classes, update the unresolved hypothesis space using recorded experiment outcomes, and select the next experiment by explicit expected entropy reduction.",
        "",
        "## Rules",
        "",
        "**Classification:** " + str(data["classification_rule"]),
        "",
        "**Information gain:** " + str(data["information_gain_rule"]),
        "",
        "**History:** " + str(data["history_rule"]),
        "",
        "**Selection:** " + str(data["selection_rule"]),
        "",
        "Priors are research bookkeeping, not empirical probabilities or truth confidence.",
        "",
        "## Hypotheses",
        "",
        "| Key | Prior | Status | Scope | Description |",
        "|---|---:|---|---|---|",
    ]
    for row in data["hypotheses"]:
        lines.append(
            "| " + row["key"] + " | " + str(row["prior"]) + " | "
            + row["status"] + " | " + row["scope"] + " | " + row["description"] + " |"
        )

    lines.extend([
        "",
        "## Historical outcomes",
        "",
        "| Experiment | Outcome | Evidence ref | Scope |",
        "|---|---|---|---|",
    ])
    for row in data["historical_outcomes"]:
        lines.append(
            "| " + row["experiment"] + " | " + row["outcome"] + " | "
            + row["evidence_ref"] + " | " + row["scope"] + " |"
        )

    lines.extend([
        "",
        "## Adaptive experiments",
        "",
        "| Experiment | Failure classes | Mechanisms | Cost | Expected IG (bits) | Historical |",
        "|---|---|---|---:|---:|---|",
    ])
    for row in data["experiments"]:
        lines.append(
            "| " + row["key"] + " | " + ", ".join(row["failure_classes"])
            + " | " + " -> ".join(row["mechanisms"]) + " | " + str(row["cost"])
            + " | " + f"{row['expected_information_gain_bits']:.6f}"
            + " | " + (row["historical_outcome"] or "unobserved") + " |"
        )

    lines.extend([
        "",
        "## Deterministic examples",
        "",
        "- A candidate-interaction observation does not reselect interaction_probe after the recorded mixed_gain result; interaction_regime_map has expected IG 1.512888 bits.",
        "- A combined candidate-interaction + candidate-overload observation can select interaction_retrieval_guard, which covers two failure classes and has expected IG 2.000000 bits under its declared four-state hypothesis partition.",
        "",
        "## Boundary",
        "",
        data["authority_rule"],
        "",
        "Discovery planning is a hypothesis generator and experiment planner. It is not experimental evidence, and it does not execute external side effects.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    generated = render(catalog())
    if args.check:
        actual = MD_PATH.read_text(encoding="utf-8") if MD_PATH.exists() else ""
        if actual != generated:
            print("out of date: " + str(MD_PATH))
            return 1
        return 0

    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text(generated, encoding="utf-8")
    print("generated: " + str(MD_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
