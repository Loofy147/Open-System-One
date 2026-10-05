# Control-Plane Convergence Status & Execution Plan v0.1

**Date:** 2026-10-05
**Parent:** Open-System-One convergence contract
**Purpose:** durable record of what is experimentally established, what remains open, and the next discriminating work.

## 1. Current established state

### EXPERIMENTALLY_SUPPORTED

1. Cache as valuable reusable Artifact. M0 and UWS preserve cache material with provenance, integrity, freshness/status, reuse policy, and invalidation conditions. Source-drift and integrity-mismatch reuse are rejected without deleting the artifact. Cache-backed material can then be independently verified.
Primary record: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.8-cache-backed-verification.json

2. Independent Verification boundary. M0 and UWS both execute Run -> Observation -> Verification -> Evidence. A Run may remain completed while an independent verifier marks the Observation failed.
Primary record: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.6-verification-cross-runtime.json

3. UNKNOWN_OUTCOME semantic core. M0 and UWS pass the same U-01/U-02/U-03/U-04 semantics. UNKNOWN survives restart, blocks replay, requires reconciliation, and CONFIRMED_NOT_EXECUTED permits a later reservation.
Primary record: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.9-unknown-outcome.json

4. M0 run identity correction. Reuse of the same run_id with a different execution request is explicitly rejected.

5. Android stale terminal-result regression and minimal repair. A deterministic kill test proved that a late older RunRecord could overwrite a newer terminal result. A terminal-state write-once repair passes the full unit suite and APK build.
Primary records: research/conformance/ANDROID_T2_B7_KILL_RESULT_2026-10-05_v0.1.json and research/conformance/ANDROID_T2_B7_FIX_RESULT_2026-10-05_v0.1.json

## 2. Explicitly open

| Gap | Status | Immediate action |
|---|---|---|
| G-01 Kernel intersection | OPEN | Cross-map canonical-capability-core + M0 + UWS + Android |
| G-02 Cross-repo conformance | OPEN | Shared fixtures through repository-native adapters |
| G-03 Capability/Verification | EXPERIMENTALLY_SUPPORTED_WITH_LIMITS | Bind to real CapabilityExecutor/effect identity |
| G-04 UNKNOWN/reconciliation | EXPERIMENTALLY_SUPPORTED_WITH_LIMITS | Finish Android B4/B5, then B6 |
| G-11 stale ordering | EXPERIMENTALLY_SUPPORTED_WITH_LIMITS | Production-shaped late callback test |
| G-05 provenance/egress | OPEN | Map My_browser provenance/source boundaries |
| G-07 evidence integrity | OPEN | Clean-clone CI drift gate |
| G-09 product adapter | OPEN | Stable read-only adapter |
| G-06 Machine substrate | OPEN / SPECIFICATION DEBT | Audit exact research refs and interpreter |

## 3. Current Android experiment

Repository: Loofy147/Llms-mcp-android
Branch: conformance/t2-caller-recovery-v0.1
Head: ff0c2b9b8fc5a520f97a0b8a47a9f843190ceec6
Workflow: 37255335292
Current status at record time: IN_PROGRESS

The B4/B5 experiment measures request_count separately from effect_count so provider-side idempotency cannot hide an unauthorized caller replay. The branch has passed compilation, unit tests, and APK assembly. No B4/B5 PASS is recorded until connectedDebugAndroidTest concludes.

Negative harness history is retained: missing runtime imports; JUnit assertion argument order; recursive Kotlin process-identity getter. None of these are semantic evidence.

## 4. Cross-repository review completed

### canonical-capability-core
Observed ref: 6396327425e7f5e6c23456579ebc286ca69f771f.
Finding: high-value existing semantic reference. v0.17 defines State + Evidence + Policy + Action + Execution + Reconciliation; versions Event, Evidence, Claim, Context, Capability, Authority, ActionRequest, ExecutionRecord, and Reconciliation schemas; and specifies UNKNOWN_OUTCOME, idempotency, restart, reconciliation, replay, atomicity, contradiction, and adapter conformance. RC3 adds multi-process claims, fencing tokens, leases, collision detection, and concurrent reconciliation. Its target adapter contract requires stable effect identity, query after restart, authoritative dispositions, reconciliation without redispatch, duplicate protection, and crash injection.
Interpretation: use as a reference for G-01, G-03, G-04, and G-11. Do not merge its ontology into Open-System-One without a semantic crosswalk.

### external-staging-authority
Observed ref: 5e313c05245dfa5b646d3b80713b74d443b8c528.
Finding: strong independent qualification target. Durable SQLite effect ledger, unique idempotency key, stable effect identity, query by effect_id and idempotency key, explicit UNKNOWN, synthetic failure modes, and reconciliation with redispatch=false. Qualification harness measures effect/dispatch behavior across restart.
Interpretation: preferred real target for Android B4-B6 qualification instead of another mock.
Open concern: reconciliation state-transition validation is currently permissive and needs an adversarial transition matrix before production-like qualification authority.

### My_browser
Observed ref: 402121c0e6cf9294d8e71feecd5752eade859807.
Finding: acquisition kernel already models Execution -> Observation -> Evidence -> Verification -> Provenance/History, with SHA-256 artifact identity, raw retention, transformation lineage, replay, and SQLite persistence. CI passes the tested kernel scope.
Interpretation: best existing acquisition/evidence vertical for G-05 and G-07. Its own non-claims remain binding: hashing is not source authenticity, JSON MCP result is not an MCP connection, jsdom is not a real browser.

### Conversational
Observed ref: f65be73b9f6b8ac0d91f8e80f0b4e3da44d2a0cd.
Finding: strong Frontier/continuity model with immutable events, deterministic reduction, source bindings, publication-head separation, and explicit authorization separation. Restore never grants external authorization.
Interpretation: use as Frontier/Continuation adapter semantics, not execution authority.

### recursive-audit
Observed ref: d89908a99a2eb2330144927483b7538b612dfb1d.
Finding: strong epistemic/assurance vertical with directed claim graphs, evidence nodes, bi-temporal state, retraction propagation, branch conflicts, execution bindings, and deterministic HARD/SOFT audit gates.
Interpretation: map it into the central Claim/Evidence/Decision layer carefully. Its Evidence is currently a graph node under ClaimType, so it must not be promoted as the universal Evidence ontology without a semantic mapping.

### Machine
Observed current main README ref: 69d71d60f396492452abf5b19dadd7a104fa88b7.
Finding: current main README provides no usable architectural evidence by itself. Known research refs remain the relevant substrate evidence surface.
Interpretation: no promotion. Keep Machine parallel to the control plane until the exact interpreter/substrate audit is executed.

## 5. Revised execution plan

Phase 0 — Finish Android qualification
1. Finish B4/B5 on ff0c2b9b8fc5a520f97a0b8a47a9f843190ceec6.
2. Record PASS/FAIL with workflow/job/log provenance.
3. Do not merge on build-only or unit-only success.

Phase 1 — Real effect boundary
1. Put external-staging-authority behind the qualification path.
2. Run B4 and B5 against its durable ledger.
3. Run B6 with two independent recovery actors/processes.
4. Measure dispatch_count, effect_count, reconciliation_count, and final disposition separately.
5. Require zero unsafe duplicate effects.

Phase 2 — Causal ordering
1. Keep terminal write-once as the minimal candidate repair.
2. Build one production-shaped late-callback path.
3. Test stale results after success, failure, reconciliation, and cancellation.
4. Introduce explicit causal revisions only if terminal immutability is insufficient.

Phase 3 — Kernel intersection
Cross-map canonical-capability-core, Open-System-One, M0, UWS, Android, My_browser, and external-staging-authority. Classify fields as INVARIANT, ADAPTER_LOCAL, DERIVED, UNRESOLVED, or CONFLICTING. Do not create a mega-schema.

Phase 4 — Epistemic and continuity integration
1. Map recursive-audit relations into Claim/Evidence/Decision.
2. Map Conversational Frontier as a projection/continuation layer.
3. Map My_browser as an acquisition/evidence provider.
4. Preserve Evidence != Claim, Frontier != Authority, Acquisition != Truth, Verification != Authorization.

Phase 5 — Evidence integrity
1. Add clean-clone conformance.
2. Pin repo/ref/commit/blob/command/input/output/verifier.
3. Re-run fixtures from fresh checkouts.
4. Detect source drift and stale reports.
5. Promote only after reproducibility.

## 6. Merge and stop gates

Do not promote based only on unit tests, schema existence, MCP health, repository claims, repeated statements, or artifact presence.
Promotion requires: implementation exercised + discriminating test + independent verification + exact provenance + regression protection.
A gap closes only when its acceptance condition is satisfied; otherwise it remains OPEN or EXPERIMENTALLY_SUPPORTED_WITH_LIMITS.

## 7. Immediate next actions

1. Resolve the live B4/B5 Workflow.
2. Bind Android qualification to external-staging-authority.
3. Execute B6 concurrent recovery.
4. Turn G-11 stale ordering into a production-shaped callback test.
5. Complete the canonical-capability-core to Open-System-One semantic crosswalk.
