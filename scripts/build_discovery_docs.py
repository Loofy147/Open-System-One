from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from open_system_one.discovery import catalog  # noqa: E402

JSON_PATH = ROOT / "research" / "discovery" / "catalog.json"
MD_PATH = ROOT / "docs" / "DISCOVERY_FRONTIER.md"


def render_markdown(data: dict[str, object]) -> str:
    lines = [
        "# Discovery Frontier v0.1",
        "",
        "<!-- GENERATED FILE: scripts/build_discovery_docs.py -->",
        "",
        "This is research infrastructure, not canonical decision-contract semantics.",
        "Every generated candidate remains a HYPOTHESIS until a provenance-complete experiment receipt changes its status.",
        "",
        "## Failure classes",
        "",
        "| Key | Description |",
        "|---|---|",
    ]
    for row in data["failure_classes"]:
        lines.append("| " + row["key"] + " | " + row["description"] + " |")
    lines.extend([
        "",
        "## Mechanisms",
        "",
        "| Key | Operation | Implementation | Boundary |",
        "|---|---|---|---|",
    ])
    for row in data["mechanisms"]:
        lines.append(
            "| " + row["key"] + " | " + row["operation"] + " | "
            + row["implementation"] + " | " + row["boundary"] + " |"
        )
    lines.extend([
        "",
        "## Precomposed recipes",
        "",
        "| Recipe | Trigger | Mechanisms | Predicted effect |",
        "|---|---|---|---|",
    ])
    for row in data["recipes"]:
        lines.append(
            "| " + row["key"] + " | " + ", ".join(row["failure_classes"]) + " | "
            + " -> ".join(row["mechanisms"]) + " | " + row["predicted_effect"] + " |"
        )
    lines.extend(["", "## Kill tests and evidence", ""])
    for row in data["recipes"]:
        lines.extend([
            "### " + row["key"],
            "",
            "**Hypothesis:** " + row["hypothesis"],
            "",
            "**Kill test:** " + row["kill_test"],
            "",
            "**Evidence required:** " + ", ".join(row["evidence_required"]),
            "",
        ])
    lines.extend([
        "## Coordination",
        "",
        data["coordination_rule"],
        "",
        data["authority_rule"],
        "",
        "The generator is deliberately deterministic: the same registered failure class yields the same candidate set and the same coordination order.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = catalog()
    json_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    md_text = render_markdown(data) + "\n"

    if args.check:
        ok = True
        for path, expected in ((JSON_PATH, json_text), (MD_PATH, md_text)):
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            if actual != expected:
                print("out of date: " + str(path))
                ok = False
        return 0 if ok else 1

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json_text, encoding="utf-8")
    MD_PATH.write_text(md_text, encoding="utf-8")
    print("generated: " + str(JSON_PATH))
    print("generated: " + str(MD_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
