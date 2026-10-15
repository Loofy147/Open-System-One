# Self-Conversion Case 0001

Status: EXPERIMENTALLY_SUPPORTED (single case)

## Goal

Convert the current architectural discussion into a repository-backed, auditable research starting point
without requiring a separate product specification or waiting for a later implementation phase.

## Initial observed world

- Repository: `Loofy147/Open-System-One`
- Default branch: `main`
- Main initially exposed `README.md` at the repository root.
- README described a decision substrate and research/evidence structure, while the referenced
  `docs/DECISION_CONTRACT_v0.1.md` and `docs/RESEARCH_PROTOCOL.md` were not present at the observed root state.
- Repository permissions available to this run included push/admin.

## Executed transition

1. Inspected repository metadata and root contents.
2. Created branch `research/self-conversion-primitive-v0` from `main`.
3. Added `docs/SELF_CONVERSION_PRIMITIVE_v0.1.md`.
4. Added `research/SELF_CONVERSION_BENCHMARK_v0.1.md`.
5. Re-read both files from the created branch to verify their existence and content.

## Receipts

Initial branch base:
`main` at repository state preceding the experiment.

Commits produced:
- `3316ed6479772c96e3502c36da596c758ce172f5`
- `c8e2da8d82872967fadff918ef82a5893c6bc5ef`

Verified file blob SHAs:
- `docs/SELF_CONVERSION_PRIMITIVE_v0.1.md` → `003b3ecdb793b1db439fb01b796fbf711835b183`
- `research/SELF_CONVERSION_BENCHMARK_v0.1.md` → `2c7b671ff8318474dffb3aef613183f7b10747aa`

## Outcome

A repository-external-to-chat transformation occurred:

```
conversation intent
  -> repository inspection
  -> branch creation
  -> durable specification
  -> falsification benchmark
  -> re-read verification
```

Disposition: **VERIFIED for this case**.

## Limits

This case does not establish generalized autonomous conversion capability.
It establishes only that the connected model-plus-tool environment successfully executed and verified
this particular low-risk repository transformation.

## Next discriminating experiment

Run a fixed mixed goal set across:
A. text-only,
B. tool-enabled without verification,
C. tool-enabled with explicit post-action verification,

and compare verified-outcome rate, false-success rate, latency, intervention count, and evidence completeness.
