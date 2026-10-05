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
Action: shared fixtures for identity, terminal states, evidence linkage, replay, and contradiction.
Latest evidence: executed 2026-10-05 against pinned M0 and UWS source refs. M0 PASS: run-to-evidence linkage, same-run replay safety, and process-restart replay safety. UWS PASS: checkpoint persistence, resumable-state projection, and retry classification. Verification, provenance-in-record, authority separation, and UNKNOWN-effect semantics are NOT_REPRESENTED or NOT_PROVEN. Full conformance therefore remains OPEN.
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
Latest evidence: the 2026-10-05 conformance record pins repository refs and source blob SHAs and records the local reconstructed execution boundary. This is evidence provenance for the experiment, not a clean-clone CI drift gate.
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

## Priority order

P0: G-01 -> G-02 -> G-03 -> G-04
P1: G-05 -> G-07 -> G-09
Parallel research: G-06
Hygiene: G-08

## Stop rule

A gap closes only after its discriminating action executes and the resulting evidence is recorded with exact provenance.

## 2026-10-05 disposition

The first discriminating cross-runtime pass was intentionally not used to close any P0 gap. It produced partial positive evidence and explicit negative/non-represented findings, which are now recorded in research/conformance/CONFORMANCE_RUN_2026-10-05_v0.1.json.

The next action is repository-native conformance, followed by a deliberately small Verification boundary and an external-effect UNKNOWN/reconciliation fixture.