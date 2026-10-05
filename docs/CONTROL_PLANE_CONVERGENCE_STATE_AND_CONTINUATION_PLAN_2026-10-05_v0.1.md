# Control-Plane Convergence State and Continuation Plan v0.1

Recorded: 2026-10-05
Host repository: Loofy147/Open-System-One
Host branch: control-plane/kernel-contract-v0.1

## Current objective
Establish the smallest cross-repository semantic kernel that can be implemented independently without granting authority through reachability, transport, or model output.

Operational spine: Intent -> Plan/Action -> Policy -> Run -> Capability
Execution spine: Run -> Observation -> Verification -> Evidence
Epistemic spine: Evidence -> Claim -> Decision -> DecisionRevision
Failure spine: Failure -> UNKNOWN/Recovery -> Reconcile -> verified terminal state
Continuation: frontier is a projection, not execution authority.

## Current evidence

1. M0 durable run
Repo: Loofy147/m0-durable-run
Ref: 69b07a54e4b2f8421532b78b8abffca308bbe3da
core.py blob: 7d7b910e5ac4d114af97733d1bf4ddee6fb80a26
test_m0.py blob: 0fb0a3734160cb8167585d950da09f9a89f76999
Result: schema rejection, append-only preservation, same-run replay suppression, new-run execution, and process-restart replay checks pass.
Limit: full Verification, Authority, and external UNKNOWN semantics are not native to the core.

2. UWS runtime
Repo: Loofy147/unified-knowledge-work-system
Ref: 683c38fdc3c921c1d7977786d5b5ed8617969476
Runtime blob: 0b305cacc50339273f5770f5e229524651716d23
Interop test blob: be481b77ac43d958430158a5f25988502b540c5c
Runtime test blob: 5d6fb2fb1c91cdef2792f411ab5742aa16d6a909
Result: durable checkpointing, atomic replacement, retry classification, and separation of peer completion from Verification are directly tested.
Limit: the inspected runtime does not itself implement the full Run -> Observation -> Verification -> Evidence -> UNKNOWN chain.

3. Android B7 stale-result finding
Repo: Loofy147/Llms-mcp-android
Kill-test commit: e697e1f6a2a60c8336297fc343d2815157b5cc9d
Workflow: 37254953362
Result: 36 tests completed, 1 failed. A newer SUCCEEDED RunRecord followed by an older FAILED RunRecord reloaded as FAILED.
Repair commit: d5d80fd4d55ab4f50195ae90fb1bf7be1e4e7db4
Repair: terminal Run state is write-once in both InMemoryRuntimeStore and JournalRuntimeStore.
Verification: full unit suite and APK build pass.
Status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS; terminal immutability is not a general causal revision protocol.

4. Android B4/B5
Branch: conformance/t2-caller-recovery-v0.1
Current head: 9f7b50849018cab5c7bbc32cfa251c1a093ad22c
Latest workflow: 37255335292
Build and unit tests pass.
Instrumentation result: failure because the caller test service was initially in the same process as the instrumentation runner; killProcess therefore crashed the runner.
Correction now applied: T2CallerService uses android:process=:t2caller.
Status: semantic B4/B5 result remains UNKNOWN/PENDING until this corrected process boundary is executed.

5. Verification and cache
M0 and UWS independently pass the cross-runtime Verification/Evidence fixture tranche.
M0 and UWS independently pass cache source-drift, integrity-mismatch, preservation, and cache-backed Verification cases.
Cache status: EXPERIMENTALLY_SUPPORTED.
Verification status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS.

## Current P0 gaps
G-01 Canonical kernel intersection: OPEN
G-02 Cross-repository conformance: OPEN
G-03 Capability/Verification boundary: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
G-04 UNKNOWN outcome semantics: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
G-11 stale result / causal ordering: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS

## Continuation plan
Phase A: finish Android B4/B5 with the caller in a dedicated process. Require process identity change, provider request_count and effect_count, explicit reconciliation decision, and no duplicate dispatch.
Phase B: execute B6 with two independent Android recovery actors sharing the same durable effect identity. Measure dispatch attempts separately from effect applications.
Phase C: test B7 through a production-shaped late Binder callback path. Keep terminal write-once as the smallest current repair; add causal revision only if a real path requires it.
Phase D: qualify canonical-capability-core rc2 against external-staging-authority. Observe runtime state, retry decision, reconciliation, effect identity, idempotency key, evidence reference, timestamps, authority class, persisted record, and external dispatch count.
Phase E: promote only semantics that are independently represented by at least two materially different implementations.
Phase F: use My_browser for acquisition/evidence/provenance integration and distinguish hashing from source authenticity.
Phase G: use Conversational and recursive-audit for lineage, contradiction, continuation, and truth-maintenance assurance without granting them execution authority.
Phase H: use Global-redteam as a source of adversarial failure fixtures, not as an evidence authority.

## Stop rules
No P0 gap closes by documentation alone.
No semantic claim upgrades by repetition.
Every repair needs a before/after kill test.
Keep failed tests and harness defects in history.
Do not generalize single-process results into distributed guarantees.
Do not merge repairs that broaden semantics beyond the targeted gap.

## Current decision frontier
1. Corrected Android B4/B5 execution.
2. B6 multi-process recovery race.
3. RC2 runtime evidence gate against external-staging-authority.
4. Production-shaped B7 late callback test.
5. Only then promote the smallest convergent kernel changes.
