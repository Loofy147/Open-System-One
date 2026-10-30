# Open System One

Machine-native typed decision substrate.

The repository separates:

1. Decision contract — opaque state, typed independent questions, finite outcomes, distributions.
2. Deterministic decision composition — scoring, calibration, abstention/policy layers.
3. Replaceable model/runtime backends — pairwise, set-aware, conditional, browser ONNX, MLX, CoreML/ANE, etc.
4. Research/evidence — experiments, receipts, kill tests, negative findings, and open questions.

## Architecture reference

[MIRA — Machine Intelligence Reference Architecture, Foundation v0.1](docs/MIRA_FOUNDATION_v0.1.md) is a provisional cross-system reference architecture. It connects machine-native research, heterogeneous capabilities, coordination, grounding, memory, agency, authorization, execution and verification.

MIRA does not replace this repository's typed decision contract, turn Open-System-One into a universal runtime kernel, or promote research from other repositories automatically. Specialist repositories retain authority over their implementations and evidence. Adoption remains contract-first and evidence-gated.

## Current status

- Contract specification: **ESTABLISHED as the project design; reference implementation is provisional**
- Browser MiniLM ONNX execution: **EXPERIMENTALLY_SUPPORTED / USER_REPORTED receipt**
- Generic embedding + cosine baseline: **EXPERIMENTALLY_SUPPORTED in the tested small transfer benchmark**
- Set-aware advantage on real decision data: **OPEN**
- Conditional mixture advantage: **OPEN overall; contradicted in the current small transfer receipt**
- Confidence as permission to act: **CONTRADICTED as a contract rule**
- BANKING77 pilot: **implemented in browser lab; reviewed receipt pending**

## Non-goals

This repository is not a Jev reproduction, does not contain proprietary Jev weights, and does not treat one encoder or scorer as canonical.

## Repository map

- `src/open_system_one/` — contract, scorers, policy, metrics
- `tests/` — contract/property/kill tests
- `docs/` — architecture, provenance, research contracts
- `research/` — mechanism catalog, experiment specifications, receipts
- `schema/` — machine-readable contract schemas
- `configs/` — reproducible benchmark configuration
- `runtime/browser/` — browser/ONNX execution boundary

Start with:
- `docs/MIRA_FOUNDATION_v0.1.md`
- `docs/CANONICAL_ARCHITECTURE_CONVERGENCE_v0.1.md`
- `docs/ARCHITECTURE_CONVERGENCE_GAP_REGISTER_v0.1.md`
- `docs/LEGACY_SALVAGE_AUDIT_v0.1.md`

The convergence contract is provisional until its first end-to-end conformance slice executes successfully.
