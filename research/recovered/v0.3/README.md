# Recovered v0.3 Evidence Snapshot

This directory is a **NON-CANONICAL EVIDENCE ARCHIVE** recovered from Library artifacts dated 2026-09-23.

It preserves research evidence and historical experiment sources without promoting them to canonical runtime semantics.

## Provenance

- stage archive SHA-256: 2592f80ca68f3cd181a35c15b2d9cef4a80b2308f6de726fbc6366af26eda6d4
- real-transfer archive SHA-256: f5f389c2a26de28f401e5d1510062059cb367a841fe23d90e4565bb8fd8ac13d
- original v0.3 archive test command: `PYTHONPATH=src pytest -q`
- independent rerun of the extracted original archive: **31 passed**
- rerun environment: Python 3.13.5

## Transfer evidence

The archived transfer result is from the learned 24D bidirectional Transformer surrogate, not pretrained MiniLM or ModernBERT.

The surrogate script was re-executed in the current runtime. Two same-environment reruns were identical, but their metrics differed from the archived receipt (maximum absolute accuracy delta 0.0260417; maximum Brier delta 3.84847e-05). Therefore the archived receipt is retained as an immutable historical measurement rather than silently replaced.

The transfer script also has a fixed final output path under `/mnt/data`; the computation completes, then the script fails on that final write when the directory is absent. This is a harness defect, not a model-result failure.

## Boundary

Do not use this directory to define canonical Decision Contract semantics. Use it to preserve source/result lineage, audit prior claims, and reproduce historical evidence where the environment permits.
