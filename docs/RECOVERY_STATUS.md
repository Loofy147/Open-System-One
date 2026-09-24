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

## Verification

Original v0.3-stage:
- PYTHONPATH=src pytest -q
- 31 passed in 2.24s

Local reconstruction check:
- v0.3 source plus two student tests
- 33 passed in 2.01s

The second result is a local reconstruction check, not a remote GitHub CI result.

## Remaining recovery debt

- Raw per-run batch JSON files are summarized by durable receipts but are not all copied as individual files.
- Duplicate contract representations still need consolidation.
- Exact per-K Brier reporting needs to replace mixed-K approximations in the browser pilot.
- BANKING77 numerical receipt remains OPEN.
- Real pretrained encoder comparison remains OPEN.

## Merge gate

Do not merge recovery into main until remote CI passes and the remaining contract/measurement debt is reviewed.
