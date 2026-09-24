# Recovery Status — 2026-09-24

## Recovered

The recovery branch contains the richer v0.3 implementation surface:

- schema.py
- engine.py
- probability.py
- calibration.py
- student.py
- causal backend skeleton
- diffusion read-slot protocol
- primitive layer
- adaptive primitive sweep
- scorer architectures and extended architectures
- shortlist
- selective prediction
- experiment scripts
- evidence and research documentation

A non-canonical evidence snapshot is now preserved under `research/recovered/v0.3/`, including the historical research frontier, the learned-encoder transfer source/result, the historical research catalog, archive hashes, and raw batch SHA-256 inventory.

## Verification

Original v0.3-stage archive:
- command: `PYTHONPATH=src pytest -q`
- independent rerun of the extracted archive: **31 passed in 2.90s** under Python 3.13.5 / torch 2.10.0+cpu / numpy 2.3.5.
- the previously recorded **31 passed in 2.24s** remains a historical receipt; runtime duration is environment-dependent.

Local reconstruction check recorded by the recovery work:
- v0.3 source plus two added student tests
- 33 passed in 2.01s
- this is a local reconstruction check, not remote CI evidence.

## Transfer re-execution finding

The historical 24D learned bidirectional encoder surrogate was re-executed.

- two runs in the same current environment were identical;
- the recomputed metrics differ from the archived receipt by up to 0.02604 absolute accuracy and 3.84847e-05 Brier;
- the script computes the result matrix but then fails on its fixed final write path when `/mnt/data/open-system-one-realtransfer/` is absent.

Therefore the historical transfer result is retained as an immutable receipt, not silently replaced by the current rerun.

## Remaining recovery debt

- The 19 historical batch JSON files are not yet copied individually into the repository; their SHA-256 inventory is preserved in `RAW_BATCH_HASHES.txt` and the source archive hashes are recorded in `ARCHIVE_MANIFEST.json`.
- Duplicate contract representations still need consolidation.
- Exact per-K Brier reporting needs to replace mixed-K approximations in the browser pilot.
- BANKING77 numerical receipt remains OPEN.
- Real pretrained encoder comparison remains OPEN.
- Remote CI status for the new recovery commit still requires a completed run.

## Merge gate

Do not merge recovery into `main` until remote CI passes and the remaining contract/measurement debt is reviewed.
