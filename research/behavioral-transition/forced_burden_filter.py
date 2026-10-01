import json
import sys
from collections import Counter

ALLOWED_DISPOSITIONS = {
    "KILL", "MERGE", "ABSORB", "AUTOMATE", "BOUND", "PROVE", "DEFER", "REBASE"
}
ALLOWED_STATUSES = {
    "KILLED", "MERGED", "ABSORBED", "AUTOMATION_TESTED", "BOUNDED",
    "PROVING", "DEFERRED", "REBASED", "RESOLVED", "UNKNOWN_WITH_ACTION"
}
REQUIRED = {
    "burden_id", "source_kind", "source_refs", "scope", "statement", "burden_class",
    "target_transition", "disposition", "status", "resolution_condition",
    "next_discriminating_action"
}


def check(path: str) -> int:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    burdens = data.get("burdens", [])
    errors = []
    ids = [b.get("burden_id") for b in burdens]
    dup = [k for k, v in Counter(ids).items() if k and v > 1]
    if dup:
        errors.append("duplicate burden_id: " + ", ".join(dup))

    for idx, b in enumerate(burdens):
        missing = sorted(REQUIRED - set(b))
        if missing:
            errors.append(f"[{idx}] missing fields: {', '.join(missing)}")
        if b.get("disposition") not in ALLOWED_DISPOSITIONS:
            errors.append(f"[{idx}] invalid disposition: {b.get('disposition')}")
        if b.get("status") not in ALLOWED_STATUSES:
            errors.append(f"[{idx}] invalid status: {b.get('status')}")
        if b.get("disposition") == "DEFER" and not b.get("wake_condition"):
            errors.append(f"[{idx}] DEFER requires wake_condition")
        if not b.get("next_discriminating_action"):
            errors.append(f"[{idx}] next_discriminating_action is empty")
        if not b.get("target_transition") and b.get("disposition") not in {"KILL", "MERGE"}:
            errors.append(f"[{idx}] non-killed/merged burden requires target_transition")

    summary = data.get("force_summary", {})
    if summary.get("discovered") != len(burdens):
        errors.append("force_summary.discovered does not equal burden count")
    if summary.get("classified") != len(burdens):
        errors.append("force_summary.classified does not equal burden count")
    if summary.get("unclassified") != 0:
        errors.append("force_summary.unclassified must be 0")
    if summary.get("ownerless_actionless") != 0:
        errors.append("ownerless_actionless must be 0")
    if summary.get("silent_defer") != 0:
        errors.append("silent_defer must be 0")

    observed = Counter(b.get("status") for b in burdens)
    declared = {k: v for k, v in summary.get("current_status_counts", {}).items()}
    for status, count in observed.items():
        if declared.get(status) != count:
            errors.append(f"status count mismatch for {status}: declared={declared.get(status)} observed={count}")

    if errors:
        print("FORCED_BURDEN_FILTER=FAIL")
        for e in errors:
            print("-", e)
        return 1

    print("FORCED_BURDEN_FILTER=PASS")
    print(f"burdens={len(burdens)}")
    print("statuses=" + json.dumps(dict(sorted(observed.items())), sort_keys=True))
    print("unclassified=0")
    print("ownerless_actionless=0")
    print("silent_defer=0")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python forced_burden_filter.py CURRENT_BURDEN_LEDGER.json")
        raise SystemExit(2)
    raise SystemExit(check(sys.argv[1]))
