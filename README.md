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
## OpenAI Dots readiness

The branch research/dots-readiness-v0.1 contains a product-boundary-independent readiness and characterization layer for OpenAI Dots:

- docs/dots/ — readiness contract, onboarding brief, validation matrix, first-task pack, and characterization report
- src/open_system_one/dots/ — receipt and local task-contract policy primitives
- tests/test_dots_receipt.py — receipt contract and negative tests
- research/dots/dots_first_run_manifest_v0.1.json — first-access test manifest

Dots are treated as a replaceable execution surface. Open-System-One remains the durable authority for claims, evidence, decisions, verification, and provenance.
## Agent surfaces

The branch research/dots-readiness-v0.1 also contains a vendor-neutral registry and common characterization protocol for external agent surfaces. See docs/agent-surfaces/AGENT_SURFACE_REGISTRY_v0.1.md, docs/agent-surfaces/AGENT_SURFACE_COMMON_TEST_PROTOCOL_v0.1.md, and docs/agent-surfaces/AGENT_SURFACE_EXPERIMENT_PLAN_v0.1.md.
The same branch also contains docs/agent-surfaces/AGENT_GAP_MAP_v0.1.md for direct/infrastructure/indirect coverage and docs/agent-surfaces/MICRO_ACTIVATION_PROOF_CARD_v0.1.md for evidence-backed narrow integrations.
