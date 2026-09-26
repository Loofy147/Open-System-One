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
        "Generated classifications are tag-based observations; generated experiments remain HYPOTHESIS until a provenance-complete receipt changes their status.",
        "",
        "## Classification rule",
        "",
        data["classification_rule"],
        "",
        "## Selection rule",
        "",
        data["selection_rule"],
        "",
        "## Failure classes",
        "",
        "| Key | Scope | Trigger tags | Description |",
        "|---|---|---|---|",
    ]
    for row in data["failure_classes"]:
        lines.append(
            "| " + row["key"] + " | " + row["scope"] + " | "
            + ", ".join(row["trigger_tags"]) + " | " + row["description"] + " |"
        )

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
        "| Recipe | Trigger | Mechanisms | Scope |",
        "|---|---|---|---|",
    ])
    for row in data["recipes"]:
        lines.append(
            "| " + row["key"] + " | " + ", ".join(row["failure_classes"]) + " | "
            + " -> ".join(row["mechanisms"]) + " | " + row["scope"] + " |"
        )

    lines.extend([
        "",
        "## Experiment designs",
        "",
        "| Experiment | Trigger | Recipes | Mechanisms | Cost | Scope |",
        "|---|---|---|---|---:|---|",
    ])
    for row in data["experiments"]:
        lines.append(
            "| " + row["key"] + " | " + ", ".join(row["failure_classes"]) + " | "
            + ", ".join(row["recipe_keys"]) + " | "
            + " -> ".join(row["mechanisms"]) + " | " + str(row["cost"]) + " | "
            + row["scope"] + " |"
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
        ])

    lines.extend([
        "## Authority boundary",
        "",
        data["authority_rule"],
        "",
        "The classifier and selector are deterministic coordination aids. They do not infer truth from language by themselves, and they do not mint execution authority.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = catalog()
    json_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    md_text = render_markdown(data)

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
