# Architecture Convergence Gap Register v0.1

**Recorded:** 2026-10-02
**Latest evidence pass:** 2026-10-05
**Parent:** docs/CANONICAL_ARCHITECTURE_CONVERGENCE_v0.1.md

## G-01 — Canonical kernel intersection
Status: OPEN
Question: Which fields are invariant across Run, Observation, Verification, Evidence, Artifact, Claim, Decision, DecisionRevision, Relationship, Contradiction, Gap?
Action: extract schemas/contracts from Open-System-One, UWS, m0, and Android; classify fields as invariant, adapter-local, unresolved.
Latest evidence: first reconstructed conformance pass shows that M0 and UWS share some Run durability semantics but do not expose the full common record graph. The current machine-readable schemas therefore remain a draft intersection, not an established canonical kernel.
Acceptance: minimal machine-readable kernel without forcing implementation-specific fields into it.

## G-02 — Cross-repository conformance
Status: OPEN
Question: Can materially different implementations satisfy the same semantic contract?
Action: shared fixtures for identity, terminal states, evidence linkage, replay, contradiction, and cache artifacts, executed through repository-native adapters.
Latest evidence: repository-native adapters now exist on M0 and UWS branches. M0 adapter execution produced K-IDENTITY-01=FAIL and K-CACHE-01=PASS; UWS produced K-IDENTITY-01=NOT_PROVEN and K-CACHE-01=PASS. The M0 failure is a concrete semantic mismatch: current lookup reuses an existing run_id for a different goal. The adapters did not fabricate support for absent concepts. Full conformance therefore remains OPEN.
Acceptance: two independent implementations pass the same semantic assertions where both represent them, and mismatches are explicit.

## G-03 — Capability/Verification boundary
Status: OPEN
Question: What is the smallest contract allowing a Capability to produce an Observation that an independent Verifier can assess?
Action: reconcile Android CapabilityExecutor with UWS/m0 execution/evidence.
Latest evidence: M0 has executable Run -> Evidence, but no independent Verification record. UWS has execution/checkpoint/retry state, but no independent verification representation in the inspected runtime.
Acceptance: execute -> observe -> verify -> evidence without model prose as authority.

## G-04 — UNKNOWN outcome semantics
Status: OPEN across systems; local evidence exists in Android/m0 regimes.
Question: How is an ambiguous external effect represented and reconciled without accidental duplicate execution?
Action: common states + idempotency/reconciliation fixtures.
Latest evidence: neither M0 nor the inspected UWS runtime represents UNKNOWN external-effect reconciliation. M0 replay safety is proven for a completed Run identity, not for an ambiguous external effect. UWS retry policy does not establish effect reconciliation.
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
Latest evidence: the 2026-10-05 conformance records pin repository refs and source blob SHAs and record the local reconstructed execution boundaries. This remains experiment provenance, not a clean-clone CI drift gate.
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
Action: complete repository-native K-CACHE-01 execution, then add source-drift invalidation and independent Verification before allowing cache-backed results to advance epistemic state.
Evidence:
- Open-System-One schema/cache-reference.v0.1.json defines identity, derivation, source, integrity, status, reuse policy, invalidation conditions, evidence role, and authority=none.
- m0-durable-run branch conformance/cache-contract-v0.1 adds cache v1 validation, append-only cache-state tests, and a repository-native conformance adapter.
- unified-knowledge-work-system branch conformance/cache-contract.v0.1 adds atomic cache-reference persistence, cache-state tests, and a repository-native conformance adapter.
- Focused adapter execution returned K-CACHE-01=PASS in both implementations.
Limits: no clean-clone CI result; freshness truth after source drift is not established; cache content has not crossed an independent Verification boundary.
Acceptance: two materially different implementations pass the cache fixture and preserve stale/invalid artifacts without promoting them to Evidence or Authority.

## Priority order

P0: G-01 -> G-02 -> G-03 -> G-04
P1: G-05 -> G-07 -> G-10 -> G-09
Parallel research: G-06
Hygiene: G-08

## Stop rule

A gap closes only after its discriminating action executes and the resulting evidence is recorded with exact provenance.

## 2026-10-05 disposition

The first discriminating cross-runtime pass was intentionally not used to close any P0 gap. It produced partial positive evidence and explicit negative/non-represented findings.

A bounded cache-artifact conformance slice was then added. It confirms that cache material can be represented as a valuable reusable Artifact with explicit provenance, integrity, status, reuse policy, and invalidation conditions in two materially different runtimes.

Repository-native adapters were then added. They expose an important negative result rather than smoothing it away: M0 currently fails the stronger run-identity assertion for reuse of the same run_id with a different goal. UWS does not currently represent that contract. This keeps G-02 OPEN with a precise discriminating mismatch.

Next actions:
1. fix or explicitly version the M0 same-run-id/different-goal behavior and add it as a regression boundary;
2. implement the smallest independent Verification record;
3. implement UNKNOWN_OUTCOME plus reconciliation before replay;
4. run source-drift invalidation for K-CACHE-01;
5. wire adapter execution into repository-native CI where available.
