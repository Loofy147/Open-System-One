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
        "Structured evidence is converted into failure classes; previous experiment outcomes constrain repeat information gain; selection uses explicit entropy reduction under declared research priors.",
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
        "| Experiment | Failure classes | Mechanisms | Cost | Expected IG (bits) | Historical outcome |",
        "|---|---|---|---:|---:|---|",
    ])
    for row in data["experiments"]:
        historical = row["historical_outcome"] or "unobserved"
        lines.append(
            "| " + row["key"] + " | " + ", ".join(row["failure_classes"])
            + " | " + " -> ".join(row["mechanisms"]) + " | " + str(row["cost"])
            + " | " + f"{row['expected_information_gain_bits']:.6f}"
            + " | " + historical + " |"
        )

    lines.extend(["", "## Experiment details", ""])
    for row in data["experiments"]:
        lines.extend([
            "### " + row["key"],
            "",
            "**Hypothesis:** " + row["hypothesis"],
            "",
            "**Intervention:** " + row["intervention"],
            "",
            "**Baseline:** " + row["baseline"],
            "",
            "**Control:** " + row["control"],
            "",
            "**Discriminator:** " + row["discriminator"],
            "",
            "**Kill test:** " + row["kill_test"],
            "",
            "**Evidence required:** " + ", ".join(row["evidence_required"]),
            "",
            "**Outcome partition:** " + "; ".join(
                key + " -> " + value for key, value in row["outcome_partition"].items()
            ),
            "",
        ])

    lines.extend([
        "## Boundary",
        "",
        data["authority_rule"],
        "",
        "Priors are research bookkeeping, not truth probabilities. Discovery planning is not experimental evidence.",
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
