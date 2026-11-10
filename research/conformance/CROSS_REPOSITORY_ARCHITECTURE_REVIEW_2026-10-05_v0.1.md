# Cross-Repository Architecture Review v0.1

**Date:** 2026-10-05
**Scope:** Review of repositories with direct relevance to the current control-plane convergence.

## Review matrix

| Repository | Observed ref | Primary role | Disposition | Highest-value finding |
|---|---|---|---|---|
| canonical-capability-core | 6396327425e7f5e6c23456579ebc286ca69f771f | Capability/action/execution/reconciliation reference | REFERENCE CANDIDATE | Mature schema + adapter conformance + UNKNOWN/idempotency/fencing model |
| external-staging-authority | 5e313c05245dfa5b646d3b80713b74d443b8c528 | Independent synthetic effect authority | QUALIFICATION TARGET | Durable effect ledger + failure injection + no-redispatch reconciliation |
| My_browser | 402121c0e6cf9294d8e71feecd5752eade859807 | Acquisition/evidence kernel | VERTICAL CANDIDATE | Execution -> Observation -> Evidence -> Verification -> Provenance |
| Conversational | f65be73b9f6b8ac0d91f8e80f0b4e3da44d2a0cd | Continuity/frontier | PROJECTION/CONTINUITY REFERENCE | Immutable frontier events + deterministic rebuild + authorization separation |
| recursive-audit | d89908a99a2eb2330144927483b7538b612dfb1d | Epistemic/truth-maintenance assurance | EPISTEMIC VERTICAL | Claim graph + retraction + bi-temporal state + HARD/SOFT gates |
| Machine | 69d71d60f396492452abf5b19dadd7a104fa88b7 | Substrate research | PARALLEL / OPEN | Main branch currently does not expose enough architectural evidence; research refs remain separate |

## 1. canonical-capability-core

Observed contracts:
- v0.17 core boundary is State + Evidence + Policy + Action + Execution + Reconciliation.
- Durable schemas cover Event, Evidence, Claim, Context, Capability, Authority, ActionRequest, ExecutionRecord, and Reconciliation.
- Adapter conformance explicitly requires authority, scope, effects, idempotency, restart, UNKNOWN_OUTCOME, reconciliation, contradiction, atomicity, and replay.
- RC3 adds multi-process claim ownership, fencing tokens, leases, collision handling, and concurrent reconciliation.
- Target adapter selection requires stable effect identity, post-restart queryability, authoritative disposition, reconciliation without redispatch, duplicate protection, and crash injection.

Architectural disposition:
- Strongest existing semantic reference for G-01/G-03/G-04/G-11.
- Must be cross-mapped, not merged wholesale.
- Its production-readiness posture remains bounded: v0.22.1rc2 is staging-ready, not production-approved.

## 2. external-staging-authority

Observed implementation:
- SQLite WAL ledger with unique idempotency_key and durable effect identity.
- Query by effect_id and idempotency_key.
- Failure modes include TIMEOUT_AFTER_ACCEPT, TIMEOUT_BEFORE_COMMIT, UNAVAILABLE, and DELAYED.
- Reconciliation records disposition and explicitly returns redispatch=false.
- Qualification test records runtime state, effect identity, effect count, dispatch count, restart behavior, and reconciliation.

Architectural disposition:
- Preferred external-effect qualification target for Android B4/B5/B6.
- Stronger than another local mock because the effect ledger is a separate process/service and has its own durable identity.

New concern:
- Reconciliation endpoint state transitions are permissive: the service updates disposition/status without a full terminal-transition matrix. Add adversarial tests before treating it as a final qualification authority.

## 3. My_browser

Observed kernel:
- Execution -> Observation -> Evidence -> Verification -> Provenance/History.
- SHA-256 artifact identity, raw retention, transformation lineage, replay, and SQLite persistence.
- Explicit boundaries: source authenticity is not established; JSON MCP results are not MCP transport; jsdom is not a real browser.

Architectural disposition:
- Best current acquisition/evidence vertical for G-05/G-07.
- Keep source adapter semantics local; only extract the evidence/provenance intersection.

## 4. Conversational

Observed protocol:
- Frontier is a projection/orchestration layer, not domain authority.
- Immutable FrontierEvent, deterministic reduction, source bindings, publication-head separation, and explicit authorization separation.
- Restore does not grant action authorization.

Architectural disposition:
- Use as continuation/frontier projection semantics.
- Do not merge Frontier into execution or authority kernel.

## 5. recursive-audit

Observed assurance model:
- Directed claim graph.
- Evidence represented as typed graph material with support/attack/defeat/refinement relations.
- Bi-temporal storage.
- Retraction propagation, reopen states, branch conflict isolation.
- Execution bindings, deterministic verifier, and HARD/SOFT merge gates.

Architectural disposition:
- Strong epistemic vertical.
- Requires a mapping layer because its current Evidence node model is graph-centric and overlaps with the central distinction between Observation, Evidence, Claim, and Decision.
- Confidence vectors and relation ontology are not promoted to universal kernel semantics.

## 6. Machine

Observed current main ref: 69d71d60f396492452abf5b19dadd7a104fa88b7.

Architectural disposition:
- No promotion from the current main README alone.
- Preserve Machine as independent substrate authority/research track.
- Next review must use exact research refs and the actual interpreter rather than repository metadata.

## Cross-repository convergence findings

### Strong existing convergence
1. UNKNOWN_OUTCOME + reconciliation is independently articulated in canonical-capability-core, external-staging-authority, M0, UWS, and Android.
2. Verification/evidence separation exists independently in M0, UWS, My_browser, and canonical-capability-core.
3. Frontier/continuity explicitly remains a projection in Conversational, matching the control-plane non-authority rule.
4. Artifact provenance/integrity and replay are already strong in My_browser and canonical-capability-core.

### Areas of semantic tension requiring crosswalk
1. Capability/action/effect identity vocabulary differs between canonical-capability-core and Android.
2. Evidence is graph-centric in recursive-audit but record-centric in the emerging kernel.
3. Frontier and DecisionRevision are related but must not be conflated.
4. External-staging authority is a qualification authority, not a universal production authority.
5. Machine substrate semantics remain insufficiently evidenced from current main.

### New immediate review actions
1. Build canonical-capability-core -> Open-System-One field/transition crosswalk for ActionRequest, ExecutionRecord, Reconciliation, Authority, and Effect identity.
2. Bind external-staging-authority to Android B4/B5/B6 qualification.
3. Map My_browser artifact/evidence lineage to the common Artifact/Evidence schemas.
4. Map recursive-audit relations into Claim/Decision/Contradiction without importing its whole ontology.
5. Leave Conversational as Frontier projection and Machine as parallel substrate research.

## Review rule

No repository gains semantic authority because it is more complete, older, reachable, or more sophisticated. Authority remains concern-scoped and evidence-pinned.
