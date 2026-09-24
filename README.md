# Open System One

Machine-native typed decision substrate.

The repository separates:

1. Decision contract — opaque state, typed independent questions, finite outcome spaces, distributions.
2. Deterministic decision composition — scoring, calibration, abstention/policy layers.
3. Replaceable model/runtime backends — pairwise, set-aware, conditional, browser ONNX, MLX, CoreML/ANE, etc.
4. Research/evidence — experiments, receipts, kill tests, negative findings, and open questions.

## Current status

- Core decision contract: **ESTABLISHED**
- Browser MiniLM ONNX execution: **EXPERIMENTALLY_SUPPORTED**
- Generic embedding + cosine baseline: **EXPERIMENTALLY_SUPPORTED**
- Set-aware advantage on real decision data: **OPEN**
- Conditional mixture advantage: **OPEN; currently not supported by the small transfer benchmark**
- Confidence as permission to act: **REJECTED as a contract rule**
- Real-data BANKING77 pilot: **implemented in the browser lab; receipt pending**

## Non-goals

This repository is not a Jev reproduction, does not contain proprietary Jev weights, and does not treat a particular encoder or scoring head as canonical.

## Repository map

- `src/open_system_one/` — contract and reference logic
- `tests/` — contract/property/kill tests
- `docs/` — architecture and research protocol
- `research/` — experiment specifications and evidence receipts
- `configs/` — reproducible benchmark configuration
- `runtime/browser/` — browser/ONNX execution notes and lab integration contract

See `docs/DECISION_CONTRACT_v0.1.md` and `docs/RESEARCH_PROTOCOL.md` first.