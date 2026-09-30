# Hamiltonian Verifier Extraction v0.1 — corrected contract

## Evidence identity

- Source repository: `Loofy147/Symlib`
- Source ref: `090698ba721bbe8428dc7ccfa003978532d6e446`
- Source path: `symlib/kernel/verify.py`
- Source blob: `58bf9d361c48a2b9398238d47c07d8c33afa54a1`
- Extraction branch: `extract/hamiltonian-verifier-v0.1`

## Critical finding

The legacy module is documented as checking Hamiltonian cycles, and its
function is named `verify_sigma`, but the executed predicate is weaker.

For each colour, the legacy code:
1. builds a total function on the `m^k` vertices;
2. counts functional components by walking from every not-yet-visited vertex;
3. accepts exactly when there is one such component.

For a finite functional graph, this counts directed cycles, not indegree
constraints. Therefore one component does **not** imply that every vertex lies
on the cycle.

The canonical Symlib `m=3,k=3` table is direct evidence: the legacy verifier
accepts it, while some colour maps have vertices with indegree 0 or 2. Thus the
legacy predicate is not equivalent to a genuine Hamiltonian-cycle verifier.

This distinction is now preserved explicitly.

## Implementation

`verify_sigma` and `verify_and_diagnose` preserve the executed legacy
single-cycle predicate for well-formed `sigma : Z_m^k -> S_k` inputs.

`verify_strict_hamiltonian` is provided separately for the stronger criterion:
one cycle + indegree one in every colour.

The implementation remains standalone and has no Symlib/NumPy/Numba dependency.

## Verification

Local checks for the corrected implementation:
- canonical Symlib `m=3,k=3` fixture: accepted by legacy-compatible verifier;
- same fixture: rejected by strict Hamiltonian verifier;
- exhaustive `m=2,k=2` comparison across all 16 labelled assignments
  against an independently written legacy reference checker;
- one-entry mutation of the `m=3,k=3` fixture is rejected;
- malformed-domain and malformed-permutation cases are rejected deterministically.

## Status

- Legacy-compatible predicate extraction: **EXPERIMENTALLY_SUPPORTED**
- Genuine Hamiltonian semantics in the legacy code: **CONTRADICTED**
- Strict Hamiltonian verifier implementation: **EXPERIMENTALLY_SUPPORTED**
  on the tested fixtures; broader property testing remains OPEN.
- Symlib runtime dependency: **REJECTED**
- Prior indegree-strengthened extraction as a semantic-preserving claim:
  **REJECTED**

## Next discriminating action

Do not merge the original extraction. Extend the corrected verifier with
property tests over additional small `(m,k)`, and only then consider whether
the strict Hamiltonian variant belongs in the reusable core.
