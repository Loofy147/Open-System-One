# Architecture Convergence Gap Register v0.1

**Recorded:** 2026-10-02
**Latest evidence pass:** 2026-10-05
**Parent:** docs/CANONICAL_ARCHITECTURE_CONVERGENCE_v0.1.md

## G-01 — Canonical kernel intersection
Status: OPEN
Question: Which fields are invariant across Run, Observation, Verification, Evidence, Artifact, Claim, Decision, DecisionRevision, Relationship, Contradiction, Gap?
Action: extract schemas/contracts from Open-System-One, UWS, m0, and Android; classify fields as invariant, adapter-local, unresolved.
Latest evidence: explicit draft Observation, Verification, and Effect references now exist, but the common record graph remains only partially represented across implementations.
Acceptance: minimal machine-readable kernel without forcing implementation-specific fields into it.

## G-02 — Cross-repository conformance
Status: OPEN
Question: Can materially different implementations satisfy the same semantic contract?
Action: shared fixtures for identity, terminal states, evidence linkage, replay, contradiction, verification, cache artifacts, and UNKNOWN_OUTCOME, executed through repository-native tests/adapters.
Latest evidence: M0 and UWS independently pass the same semantic core for Verification/Evidence, Cache reuse, and UNKNOWN_OUTCOME/reconciliation fixtures. UWS still has K-IDENTITY-01 NOT_PROVEN; broader authority/frontier/capability semantics are not common. Full conformance remains OPEN.
Acceptance: two independent implementations pass the same semantic assertions where represented, with no unsupported semantics fabricated by adapters.

## G-03 — Capability/Verification boundary
Status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
Question: What is the smallest contract allowing a Capability to produce an Observation that an independent Verifier can assess?
Action: reconcile the proven runtime boundary with Android CapabilityExecutor and verify effect identity/verification obligations.
Latest evidence: M0 and UWS independently execute a completed Run/step, record an Observation with provenance/integrity, apply an independent verifier that rejects value 55, and record Evidence linking Run -> Observation -> Verification. The execution remains completed after verification failure.
Evidence reference: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.6-verification-cross-runtime.json
Limits: this is still runtime-boundary evidence rather than full Capability/CapabilityInvocation semantics; verifier identity/authority and Android caller-side UNKNOWN remain unresolved; no clean-clone CI.
Acceptance: execute -> observe -> verify -> evidence, including capability/effect identity and verification obligations, reproduced by materially different implementations.

## G-04 — UNKNOWN outcome semantics
Status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
Question: How is an ambiguous external effect represented and reconciled without accidental duplicate execution?
Action: complete Android B4/B5 against external-staging-authority, then B6 concurrent recovery.
Latest evidence: M0 and UWS both pass the same U-01/U-02/U-03/U-04 reconciliation tests. Cross-repository review also identified canonical-capability-core and external-staging-authority as existing implementations of the same semantic family; these are now the preferred reference/qualification path rather than new parallel semantics. The exact repository test files each execute 4/4 PASS. A separate two-process restart check in both runtimes preserved UNKNOWN across process exit, blocked replay, allowed reconciliation to CONFIRMED_NOT_EXECUTED, and then allowed one new reservation. The semantic contract is pinned to Android RuntimeStore.kt at ref 78afd5d3d7716fe31a5f109a5796eb3db7f99970, blob 5fee3cf8d2f9197c2d68f6d2cb18aa5ffa11249e. Android B4/B5 integration has a corrected head 309b47f323ea2be326cbf788341bd8c83cd58c54 with unit tests and APK build PASS; connectedDebugAndroidTest for workflow 37254867999 is still IN_PROGRESS. The previous instrumentation run 37254548378 failed before semantic execution because of test-harness assertion argument order and is recorded separately.
Evidence reference: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.9-unknown-outcome.json; research/conformance/ANDROID_T2_B4_B5_EXPERIMENT_2026-10-05_v0.1.json
Limits: this proves the cross-runtime semantic core, not the full Android caller-side lifecycle. B4 caller dies after provider completion, B5 caller dies before dispatch, and B6 concurrent recovery remain unverified at the Android integration boundary until the current workflow concludes. No real external provider effect was exercised in M0/UWS; no clean-clone CI; general exactly-once is not claimed.
Acceptance: UNKNOWN is durable, blocks replay, requires explicit reconciliation, permits a new reservation only after CONFIRMED_NOT_EXECUTED, and remains separate from Evidence/Authority; the same behavior is reproduced at the Android CapabilityExecutor boundary.

## G-05 — Provenance/egress
Status: OPEN
Question: What minimal provenance must survive a remote-boundary decision?
Action: define data class/source/taint/destination/purpose/authorization/minimization fields.
Acceptance: remote invocation is auditable without exporting arbitrary internal context.

## G-06 — Machine substrate contract
Status: OPEN / SPECIFICATION DEBT
Question: Which state-access operations are actually canonical in Machine?
Action: audit the actual interpreter and compare derived relation traversal with direct indexed access under explicit cost accounting.
Acceptance: evidence-backed classification as optimization, resource primitive, or substrate extension.

## G-07 — Evidence integrity
Status: OPEN
Question: Can evidence drift while an experiment still appears to pass?
Action: pin ref/command/input/verifier/raw receipt and add drift detection.
Latest evidence: the conformance records pin repository refs and source blob SHAs and record reconstructed execution boundaries. This remains experiment provenance, not a clean-clone CI drift gate.
Acceptance: CI detects evidence drift rather than checking only file existence.

## G-08 — UWS documentation drift
Status: OPEN
Observed: roadmap describes evidence/project continuity as upcoming while current main already has project, plan-revision, evidence, assumption, validation, and event persistence.
Action: update roadmap/status after convergence record is reviewed.

## G-09 — Product integration boundary
Status: OPEN
Question: What may a product consume without importing control-plane internals?
Action: define product adapter contract and one read-only vertical.
Acceptance: product uses stable semantics, not repository internals.

## G-10 — Cache validity/reuse
Status: EXPERIMENTALLY_SUPPORTED
Question: What minimum semantics preserve the operational value of caches without allowing stale/derived material to become authority?
Action: extend only where discriminating evidence remains: broader integrity acquisition/verification, clean-clone CI, and integration with real Capability/effect identities.
Evidence:
- Open-System-One cache-reference schema and CACHE_REUSE_GATE_CONTRACT define artifact identity, provenance, integrity, status, reuse policy, source-match requirements, and explicit revalidation.
- M0 and UWS both pass source-drift negative cases: source mismatch blocks reuse; revalidate_before_use remains a gate even when source matches; stale material remains preserved.
- M0 and UWS both pass integrity-mismatch negative cases.
- M0 and UWS both pass cache-backed independent Verification: a reusable cached value of 55 is observed and rejected by an even-sum verifier while the cache remains a distinct Artifact.
Evidence reference: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.8-cache-backed-verification.json
Limits: no clean-clone CI; the reuse gate accepts an externally supplied observed digest rather than owning arbitrary content retrieval/recomputation; capability/effect semantics remain outside this cache contract.
Acceptance: two materially different implementations preserve stale/invalid cache material, refuse reuse after source drift or integrity mismatch, and keep cache distinct from Evidence/Authority while cache-backed material remains independently verifiable.

## G-11 — Stale result / causal ordering
Status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
Priority: P0
Question: Can an older execution result become authoritative after a newer terminal result?
Action: define minimal monotonic attempt/revision semantics, then reproduce the failure through a production-shaped late-callback path before implementing a fix.
Latest evidence: deterministic repository-native kill test StaleResultOrderingTest.lateOlderResultMustNotRegressNewerTerminalRun failed on commit e697e1f6a2a60c8336297fc343d2815157b5cc9d under GitHub Actions workflow 37254953362. 36 tests completed, 1 failed; org.junit.ComparisonFailure at StaleResultOrderingTest.kt:46. The test wrote a newer SUCCEEDED result with output new, then appended an older FAILED result with output old; a fresh JournalRuntimeStore reload returned old/FAILED. A minimal repair on commit d5d80fd4d55ab4f50195ae90fb1bf7be1e4e7db4 makes terminal Run state write-once in both InMemoryRuntimeStore and JournalRuntimeStore; the full unit-test suite and APK build pass, and the stale-ordering regression test passes within that unit suite.
Evidence reference: research/conformance/ANDROID_T2_B7_KILL_RESULT_2026-10-05_v0.1.json
Limits: the repair is a terminal-state immutability boundary, not a general causal revision system; no Binder late-callback path has been exercised. The same branch's instrumentation job failed on unrelated B4/B5 harness StackOverflowError before semantic execution, so that failure does not invalidate the B7 unit result.
Acceptance: a stale result cannot regress a newer causal revision; the durable record retains the newer authoritative state; late results are rejected or explicitly recorded as non-authoritative.

## Priority order

P0: G-01 -> G-02 -> G-03 -> G-04 -> G-11
P1: G-05 -> G-07 -> G-10 -> G-09
Parallel research: G-06
Hygiene: G-08

## Stop rule

A gap closes only after its discriminating action executes and the resulting evidence is recorded with exact provenance.

## 2026-10-05 disposition

The initial conformance pass exposed partial shared Run semantics and explicit absent concepts.

The cache tranche established a reusable Artifact boundary in M0 and UWS with provenance, integrity, status, reuse policy, invalidation conditions, source-drift refusal, integrity-mismatch refusal, preservation, and independent verification of cache-backed material.

The M0 identity mismatch was exposed, repaired, and converted into a regression boundary that rejects same-run-id reuse for a different execution request.

The Verification boundary then moved from a single-runtime result to two materially different runtime implementations: both can keep execution completed while an independent verifier rejects the Observation and Evidence preserves the linkage.

G-10 is now EXPERIMENTALLY_SUPPORTED rather than merely OPEN; the remaining work is verification depth and integration boundaries, not whether caches can be valuable reusable Artifacts.

G-04 is now EXPERIMENTALLY_SUPPORTED_WITH_LIMITS at the semantic-core level. The same UNKNOWN/reconciliation state machine is implemented and exercised in M0 and UWS, and it is directly grounded in the Android RuntimeStore effect semantics. Android caller B4/B5 remains pending at the integration boundary.

A new P0 G-11 was opened by a deterministic kill test. The current Android JournalRuntimeStore has experimentally demonstrated stale-result regression: a late older RunRecord can overwrite a newer terminal state because authority follows journal arrival order rather than a causal/monotonic revision.

P0 gaps remain open because canonical kernel intersection, full cross-repository conformance, complete Capability/effect semantics, Android B4/B5 integration, concurrent recovery, and causal result ordering are not yet closed.

Next actions:
1. complete and record Android B4/B5 against external-staging-authority;
2. define and test the smallest causal revision boundary for G-11;
3. execute B6 with two independent recovery actors/processes and measure dispatch count separately from effect count;
4. complete the canonical-capability-core -> Open-System-One semantic crosswalk;
5. then implement only the minimal proven B6/G-11 repairs;
6. add clean-clone CI where repository infrastructure supports it.

## 2026-10-05 repository-review references

- `docs/CONVERGENCE_STATUS_AND_EXECUTION_PLAN_v0.1.md`
- `research/conformance/CROSS_REPOSITORY_ARCHITECTURE_REVIEW_2026-10-05_v0.1.md`

The cross-repository review does not promote any new universal authority. It identifies canonical-capability-core as the strongest existing capability/reconciliation reference, external-staging-authority as the preferred independent qualification target, My_browser as an acquisition/evidence vertical, Conversational as a Frontier projection reference, recursive-audit as an epistemic/assurance vertical, and Machine as a parallel substrate research track.
