from open_system_one.discovery import catalog, coordinate, propose


def test_candidate_interaction_has_multiple_precomposed_mechanisms():
    rows = propose("candidate_interaction")
    assert len(rows) == 1
    assert rows[0].mechanisms == ("condition", "relate", "dynamic_score")


def test_coordination_deduplicates_mechanisms_and_keeps_evidence():
    plan = coordinate("candidate_interaction")
    assert plan.recipes == ("interaction_probe",)
    assert plan.mechanisms == ("condition", "relate", "dynamic_score")
    assert "matched_baseline" in plan.evidence_required


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
