# Hamiltonian Verifier Extraction v0.1

## Evidence identity

- Source repository: `Loofy147/Symlib`
- Source ref: `090698ba721bbe8428dc7ccfa003978532d6e446`
- Source path: `symlib/kernel/verify.py`
- Source blob: `58bf9d361c48a2b9398238d47c07d8c33afa54a1`
- Destination: `Loofy147/Open-System-One`
- Extraction branch: `extract/hamiltonian-verifier-v0.1`

## Extracted contract

For positive integers `m,k`, let

`V = Z_m^k`.

The input `sigma` is a map `V -> S_k`, represented as a mapping from
k-tuples to k-tuples. For each vertex `v` and colour `c`, the permutation
entry `sigma[v][c]` selects the coordinate axis incremented modulo `m`.
The induced map for colour `c` must be one directed Hamiltonian cycle over
all `m^k` vertices.

The standalone implementation additionally treats malformed input as
`valid=False` rather than relying on exceptions. It explicitly validates:

1. exact domain cardinality and in-range tuple coordinates;
2. every value is a permutation of `0..k-1`;
3. every colour induces exactly one component and indegree 1 at every vertex.

The core implementation has no Symlib, NumPy, or Numba dependency.

## Delta from legacy implementation

This is an independent reimplementation, not a copy of the legacy module.
The positive semantic target is preserved, while malformed-input handling is
made total and typed. The implementation also emits structured per-colour
diagnostics.

Legacy source documentation described the verifier as deterministic and exact.
That description is treated as the source contract, not as independent proof.

## Verification performed locally

Environment: CPython with pytest; no external runtime dependency for the
verifier.

Result: **8/8 tests passed**.

The suite includes:
- a discovered positive instance at `m=2,k=2`;
- incomplete-domain rejection;
- non-permutation rejection;
- out-of-domain rejection;
- a shape-preserving mutation that breaks the cycle property;
- invalid-parameter rejection;
- exhaustive comparison over all `2^4 = 16` labelled maps for `m=2,k=2`
  against a separately written reference checker;
- positive regression for the extracted API.

## Status

- Primitive: **EXPERIMENTALLY_SUPPORTED**
- Mathematical generality beyond the tested finite instance: **ESTABLISHED by
  the explicit definition of the contract; implementation correctness outside
  the tested instance remains OPEN pending broader property/regression tests.**
- Legacy implementation as a dependency: **REJECTED**
- Direct reuse of legacy NumPy/Numba code: **REJECTED**

## Next discriminating test

Generate or import a canonical verified `m=3,k=3` solution only as a test
fixture, then compare this standalone verifier against an independently
implemented graph checker on that fixture and on controlled single-edge
mutations. Do not import Symlib as a runtime dependency.
