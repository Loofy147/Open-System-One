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
Action: shared fixtures for identity, terminal states, evidence linkage, replay, contradiction, and cache artifacts.
Latest evidence: executed 2026-10-05 against pinned M0 and UWS source refs. The original P0 pass remains partial. A subsequent focused cache fixture was executed independently from the modified pinned source representations: M0 and UWS both preserved a cache artifact, exposed explicit reuse policy/status, and retained the artifact after transition from fresh to stale. This is bounded evidence for one Artifact subtype, not full P0 conformance.
Acceptance: two independent implementations pass the same semantic assertions.

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
Latest evidence: the 2026-10-05 conformance record pins repository refs and source blob SHAs and records the local reconstructed execution boundary. The cache experiment also pinned exact modified source blob SHAs. This remains experiment provenance, not a clean-clone CI drift gate.
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
Action: run the common cache fixture through repository-native test paths; add integrity/freshness invalidation checks and an independent verification boundary before allowing cache-backed results to advance epistemic state.
Evidence:
- Open-System-One schema/cache-reference.v0.1.json defines identity, derivation, source, integrity, status, reuse policy, invalidation conditions, evidence role, and authority=none.
- m0-durable-run branch conformance/cache-contract-v0.1 adds cache v1 validation and append-only cache-state tests.
- unified-knowledge-work-system branch conformance/cache-contract-v0.1 adds atomic cache-reference persistence and cache-state tests.
- Focused reconstructed execution from the modified source representations returned M0 CACHE PASS and UWS CACHE PASS.
Limits: these are source-reconstructed focused checks, not a clean-clone repository CI run; they do not establish cache freshness truth or epistemic authority.
Acceptance: two materially different implementations pass the cache fixture and preserve invalidated/stale artifacts without promoting them to Evidence or Authority.

## Priority order

P0: G-01 -> G-02 -> G-03 -> G-04
P1: G-05 -> G-07 -> G-10 -> G-09
Parallel research: G-06
Hygiene: G-08

## Stop rule

A gap closes only after its discriminating action executes and the resulting evidence is recorded with exact provenance.

## 2026-10-05 disposition

The first discriminating cross-runtime pass was intentionally not used to close any P0 gap. It produced partial positive evidence and explicit negative/non-represented findings.

A bounded cache-artifact conformance slice was then added. It confirms that cache material can be represented as a valuable reusable Artifact with explicit provenance, integrity, status, reuse policy, and invalidation conditions in two materially different runtimes. The cache gap therefore moves from UNKNOWN to EXPERIMENTALLY_SUPPORTED_WITH_LIMITS, while all P0 gaps remain OPEN.

Next actions remain:
1. repository-native conformance adapters/results for M0 and UWS;
2. the smallest independent Verification boundary;
3. UNKNOWN_OUTCOME with reconciliation before replay;
4. separate authority/evidence provenance and transport-independence tests.
