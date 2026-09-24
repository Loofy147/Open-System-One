from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from open_system_one.discovery import classify_failure
from open_system_one.discovery_advanced import FailureEvidence, build_adaptive_plan, observation_from_evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-count", type=int)
    parser.add_argument("--candidate-budget", type=int)
    parser.add_argument("--retrieval-latency-ms", type=float)
    parser.add_argument("--retrieval-latency-budget-ms", type=float)
    parser.add_argument("--candidate-set-changes-output", action="store_true")
    parser.add_argument("--competitor-effect", action="store_true")
    parser.add_argument("--context-dependent-score", action="store_true")
    parser.add_argument("--same-input-repeated", action="store_true")
    parser.add_argument("--duplicate-work", action="store_true")
    parser.add_argument("--cache-miss", action="store_true")
    parser.add_argument("--hash-mismatch", action="store_true")
    parser.add_argument("--lineage-mismatch", action="store_true")
    parser.add_argument("--same-content-different-id", action="store_true")
    parser.add_argument("--reordered-events", action="store_true")
    parser.add_argument("--causal-inversion", action="store_true")
    parser.add_argument("--inconsistent-merge", action="store_true")
    parser.add_argument("--stage-boundary", action="store_true")
    parser.add_argument("--intermediate-loss", action="store_true")
    parser.add_argument("--hidden-failure", action="store_true")
    parser.add_argument("--confidence-used-for-action", action="store_true")
    parser.add_argument("--missing-capability", action="store_true")
    parser.add_argument("--unauthorized-execution", action="store_true")
    parser.add_argument("--evidence-ref", action="append", default=[])
    parser.add_argument("--evidence-gap", action="append", default=[])
    parser.add_argument("--out", default="research/discovery/runs/adaptive-latest.json")
    args = parser.parse_args()

    evidence = FailureEvidence(
        candidate_set_changes_output=args.candidate_set_changes_output,
        competitor_effect=args.competitor_effect,
        context_dependent_score=args.context_dependent_score,
        candidate_count=args.candidate_count,
        candidate_budget=args.candidate_budget,
        retrieval_latency_ms=args.retrieval_latency_ms,
        retrieval_latency_budget_ms=args.retrieval_latency_budget_ms,
        same_input_repeated=args.same_input_repeated,
        duplicate_work=args.duplicate_work,
        cache_miss=args.cache_miss,
        hash_mismatch=args.hash_mismatch,
        lineage_mismatch=args.lineage_mismatch,
        same_content_different_id=args.same_content_different_id,
        reordered_events=args.reordered_events,
        causal_inversion=args.causal_inversion,
        inconsistent_merge=args.inconsistent_merge,
        stage_boundary=args.stage_boundary,
        intermediate_loss=args.intermediate_loss,
        hidden_failure=args.hidden_failure,
        confidence_used_for_action=args.confidence_used_for_action,
        missing_capability=args.missing_capability,
        unauthorized_execution=args.unauthorized_execution,
        evidence_refs=tuple(args.evidence_ref),
        evidence_gaps=tuple(args.evidence_gap),
    )
    observation = observation_from_evidence(evidence)
    matches = classify_failure(observation)
    plans = []
    for scope in ("research", "control_plane"):
        mechanisms, selections = build_adaptive_plan(observation, scope=scope)
        if selections:
            plans.append({
                "scope": scope,
                "observation_tags": list(observation.tags),
                "failure_matches": [asdict(match) for match in matches if (
                    match.failure_class in {item.failure_class for item in matches}
                )],
                "mechanisms": list(mechanisms),
                "selections": [asdict(selection) for selection in selections],
            })

    payload = {
        "status": "ADAPTIVE_PLAN_NOT_EVIDENCE",
        "observation": asdict(observation),
        "plans": plans,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("generated: " + str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
