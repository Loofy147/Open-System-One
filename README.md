# Open System One

Machine-native typed decision substrate.

The repository separates:

1. Decision contract — opaque state, typed independent questions, finite outcome spaces, distributions.
2. Deterministic decision composition — scoring, calibration, abstention/policy layers.
3. Replaceable model/runtime backends — pairwise, set-aware, conditional, browser ONNX, MLX, CoreML/ANE, etc.
4. Research/evidence — experiments, receipts, kill tests, negative findings, and open questions.

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

- src/open_system_one/ — contract, scorers, policy, metrics
- tests/ — contract and structural kill tests
- docs/ — architecture, provenance, research protocol, contract debt
- research/ — mechanism catalog, experiment specifications, receipts
- configs/ — reproducible benchmark configuration
- runtime/browser/ — browser/ONNX execution boundary

Start with docs/DECISION_CONTRACT_v0.1.md, docs/RESEARCH_PROTOCOL.md, docs/EVIDENCE_LEDGER.md, and docs/CONTRACT_DEBT.md.
