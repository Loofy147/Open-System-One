# Architecture Convergence Gap Register v0.1

**Recorded:** 2026-10-02
**Latest evidence pass:** 2026-10-05
**Parent:** docs/CANONICAL_ARCHITECTURE_CONVERGENCE_v0.1.md

## G-01 — Canonical kernel intersection
Status: OPEN
Question: Which fields are invariant across Run, Observation, Verification, Evidence, Artifact, Claim, Decision, DecisionRevision, Relationship, Contradiction, Gap?
Action: extract schemas/contracts from Open-System-One, UWS, m0, and Android; classify fields as invariant, adapter-local, unresolved.
Latest evidence: explicit draft Observation and Verification references now exist, but the common record graph remains only partially represented across implementations.
Acceptance: minimal machine-readable kernel without forcing implementation-specific fields into it.

## G-02 — Cross-repository conformance
Status: OPEN
Question: Can materially different implementations satisfy the same semantic contract?
Action: shared fixtures for identity, terminal states, evidence linkage, replay, contradiction, verification, and cache artifacts, executed through repository-native adapters.
Latest evidence: M0 passes K-IDENTITY-01, K-VERIFY-01, K-EVIDENCE-01, and K-CACHE-01. UWS passes K-VERIFY-01, K-EVIDENCE-01, and K-CACHE-01, but K-IDENTITY-01 remains NOT_PROVEN. UNKNOWN, authority, and frontier semantics remain absent in both inspected runtimes. Full conformance remains OPEN.
Acceptance: two independent implementations pass the same semantic assertions where represented, with no unsupported semantics fabricated by adapters.

## G-03 — Capability/Verification boundary
Status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
Question: What is the smallest contract allowing a Capability to produce an Observation that an independent Verifier can assess?
Action: reconcile the proven runtime boundary with Android CapabilityExecutor and verify effect identity/verification obligations.
Latest evidence: M0 and UWS independently execute a completed Run/step, record an Observation with provenance/integrity, apply an independent verifier that rejects value 55, and record Evidence linking Run -> Observation -> Verification. The execution remains completed after verification failure.
Evidence reference: research/conformance/CONFORMANCE_RUN_2026-10-05_v0.6-verification-cross-runtime.json
Limits: this is still runtime-boundary evidence rather than full Capability/CapabilityInvocation semantics; verifier identity/authority and UNKNOWN effects remain unresolved; no clean-clone CI.
Acceptance: execute -> observe -> verify -> evidence, including capability/effect identity and verification obligations, reproduced by materially different implementations.

## G-04 — UNKNOWN outcome semantics
Status: OPEN across systems; local evidence exists in Android/m0 regimes.
Question: How is an ambiguous external effect represented and reconciled without accidental duplicate execution?
Action: common states + idempotency/reconciliation fixtures.
Latest evidence: neither M0 nor UWS represents UNKNOWN external-effect reconciliation. M0 replay safety is proven for a completed Run identity, not for an ambiguous effect. UWS retry policy does not establish effect reconciliation.
Acceptance: UNKNOWN is not silently treated as safe-to-repeat.

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
Status: EXPERIMENTALLY_SUPPORTED_WITH_LIMITS
Question: What minimum semantics preserve the operational value of caches without allowing stale/derived material to become authority?
Action: add source-drift invalidation and independent Verification before allowing cache-backed results to advance epistemic state.
Evidence:
- Open-System-One cache-reference schema defines identity, derivation, source, integrity, status, reuse policy, invalidation conditions, evidence role, and authority=none.
- M0 and UWS both pass K-CACHE-01 and preserve fresh/stale cache material.
- The independent Verification boundary now exists in both runtimes, but it has not yet been applied specifically to a cache-backed result.
Limits: freshness truth after source drift is not established; cache material is preserved but not yet proven safe to promote epistemically after drift.
Acceptance: two materially different implementations preserve stale/invalid cache material, refuse authoritative reuse after source drift, and keep cache distinct from Evidence/Authority.

## Priority order

P0: G-01 -> G-02 -> G-03 -> G-04
P1: G-05 -> G-07 -> G-10 -> G-09
Parallel research: G-06
Hygiene: G-08

## Stop rule

A gap closes only after its discriminating action executes and the resulting evidence is recorded with exact provenance.

## 2026-10-05 disposition

The initial conformance pass exposed partial shared Run semantics and explicit absent concepts.

The cache tranche established a reusable Artifact boundary in M0 and UWS with provenance, integrity, status, reuse policy, and invalidation conditions.

The M0 identity mismatch was exposed, repaired, and converted into a regression boundary that rejects same-run-id reuse for a different execution request.

The Verification boundary then moved from a single-runtime result to two materially different runtime implementations: both can keep execution completed while an independent verifier rejects the Observation and Evidence preserves the linkage.

P0 gaps remain open because canonical kernel intersection, full cross-repository conformance, capability/effect semantics, and UNKNOWN external-effect reconciliation are not yet established.

Next actions:
1. apply source-drift invalidation to cache-backed reuse and preserve the stale artifact;
2. implement UNKNOWN_OUTCOME plus reconciliation before replay;
3. reconcile the verification boundary with Android CapabilityExecutor semantics;
4. decide whether UWS should adopt an explicit run-id/request binding invariant or an equivalent identity contract.