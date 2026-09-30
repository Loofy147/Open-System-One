# Hamiltonian Verifier Extraction v0.1 — corrected extraction

## Evidence identity

- Source repository: Loofy147/Symlib
- Source ref: 090698ba721bbe8428dc7ccfa003978532d6e446
- Source path: symlib/kernel/verify.py
- Source blob: 58bf9d361c48a2b9398238d47c07d8c33afa54a1
- Destination branch: extract/hamiltonian-verifier-v0.1

## Critical semantic audit

The first extraction attempt was subjected to a canonical m=3,k=3 kill-test.
It exposed an axis/colour inversion in the reimplementation.

The legacy source assigns the edge along axis a to colour sigma[v][a].
Therefore, for a fixed colour c, the extracted implementation must find the
unique axis whose permutation entry equals c. The corrected implementation
now preserves that relation.

The source counts one functional component/cycle for each colour. We retain
that executed predicate in verify_sigma. We also expose a separate strict
Hamiltonian check that adds indegree-one validation, without silently changing
the legacy predicate.

## Canonical fixture

The m=3,k=3 fixture is derived from the source _TABLE_M3 and _table_to_sigma
definitions at the pinned source ref. It contains 27 labelled vertices and is
used only as a test fixture; Symlib is not imported.

All three colours of this canonical fixture satisfy the legacy predicate and
also have indegree one, so the strict Hamiltonian check accepts it.

## Verification

The corrected logic is checked against an independently written legacy
reference checker on the canonical m=3,k=3 fixture and exhaustively on all 16
labelled m=2,k=2 assignments.

Additional tests reject a controlled one-entry mutation and malformed inputs.

The previous extraction commit
00c62a2a5c6033e35b0f2f5cc83601dd39984441 is superseded and must not be merged.

## Status

- Correct legacy predicate extraction: EXPERIMENTALLY_SUPPORTED
- First extraction axis/colour inversion: CONTRADICTED / KILLED
- Strict Hamiltonian check on canonical fixture: EXPERIMENTALLY_SUPPORTED
- Symlib runtime dependency: REJECTED
- Generalized correctness beyond tested fixtures: OPEN

## Next discriminating action

Compare the corrected implementation against source-generated m=5,k=3 and
m=4,k=3 fixtures using an independent reference checker before merge.
