from open_system_one.sweep import run_pair_sweep,run_single_sweep
def test_all_single_probes_survive():
    rows=run_single_sweep(); assert len(rows)==12 and all(r.status=="EXPERIMENTALLY_SUPPORTED" for r in rows)
def test_pair_sweep_is_exploratory_and_runs():
    rows=run_pair_sweep(["composition","memoization","content_identity","capability"])
    assert len(rows)==6 and all(r.status in {"EXPERIMENTALLY_SUPPORTED","OPEN","CONTRADICTED"} for r in rows)
