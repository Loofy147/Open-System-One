from open_system_one.discovery import catalog, coordinate, propose


def test_candidate_interaction_has_multiple_precomposed_mechanisms():
    rows = propose("candidate_interaction")
    assert len(rows) == 1
    assert rows[0].mechanisms == ("condition", "relate", "dynamic_score")


def test_multi_recipe_coordination_deduplicates_shared_mechanisms():
    rows = propose("provenance_drift")
    assert [row.recipe for row in rows] == ["deterministic_reuse", "ordered_merge"]
    plan = coordinate("provenance_drift")
    assert plan.recipes == ("deterministic_reuse", "ordered_merge")
    assert plan.mechanisms == ("identify", "cache", "order", "merge")
    assert len(plan.hypotheses) == 2
    assert "final_state_digest" in plan.evidence_required


def test_authority_recipe_is_outside_research_scope():
    plan = coordinate("authority_boundary")
    assert plan.recipes == ("authority_handoff",)
    assert "capability_gate" in plan.mechanisms
    assert catalog()["authority_rule"].startswith("No inference recipe")


def test_unknown_failure_class_is_rejected():
    try:
        propose("not_registered")
    except KeyError:
        return
    raise AssertionError("unknown failure class was accepted")
