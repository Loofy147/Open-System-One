# Architecture Convergence Contract v0.1

**Recorded:** 2026-10-02
**Target/integration repository:** Loofy147/Open-System-One
**Propagation model:** contract-first, evidence-gated, PR-based adoption

## Purpose

This record converts the current cross-repository convergence into an explicit, reviewable contract.

It defines:
1. the common architecture;
2. the owner of each boundary;
3. how changes propagate without hidden coupling;
4. what must be learned or implemented before promotion.

This is an integration contract, not proof that all repositories are already code dependencies.

## 1. Current authority map

| Boundary | Owner | Observed ref on 2026-10-02 | Role |
|---|---|---|---|
| Portfolio identity/lineage/provenance | Portfolio-Repository-Inventory | 4bc9c2f7aea708c3cd8dbc28662c9f2e59fe9d64 | governance/provenance |
| Machine-native substrate research | Machine | 1626bac2f5c478294afa4b9463f694608c322117 (main) | substrate/frontier research |
| Decision semantics | Open-System-One | a7fb4b9c44b41cadf19f9f2c700cb87de8c424e0 | decision kernel |
| Durable execution | m0-durable-run | 2fd9b2d52d194c107c816b0eccf66615eaf3cfed | Run durability/replay |
| Knowledge-work control | unified-knowledge-work-system | fdbf0a3fd1d958e1fadc922603a6c88ca2328d60 | routing/coordination |
| Android effect authority | Llms-mcp-android | 4880767491d29a5f105765683c8224c82244d1a7 | device/runtime execution |
| Product surfaces | Wedgettok / la-rouine-platform | pin exact refs per integration | user-facing applications |

"Owner" means authoritative for that boundary's implementation state and local evidence. It does not authorize other repositories to inherit its claims or code.

## 2. Canonical semantic intersection

The integration target is a small record graph, not a mega-framework:

```
Intent / Goal
    |
    v
Candidate / Plan / Action
    |
    v
Policy / Authorization
    |
    v
Run
    |
    +--> CapabilityInvocation
    +--> Observation -> Verification -> Evidence
    +--> Artifact
    |
    v
Claim / Decision
    |
    +--> DecisionRevision
    +--> Contradiction
    +--> Gap
```

The three useful spines are:

```
operational: Intent -> Plan/Action -> Policy -> Run -> Capability
execution:   Run -> Observation -> Verification -> Evidence
epistemic:   Evidence -> Claim -> Decision -> DecisionRevision
```

They intersect through stable identifiers and provenance rather than collapsing all entities into one object.

## 3. Canonical invariants

### Authority

```
Model/Agent = proposer/reasoner
Policy/Permission Authority = authorization
Capability/Executor = effect boundary
Verifier = evaluation boundary
Evidence = attributable record
```

Model output, tool description, preference, protocol acknowledgement, or successful terminal state does not itself grant authority.

### Evidence

```
Observation != Evidence
Evidence != Claim
Claim != Decision
Result != Conclusion
```

A claim can advance epistemic status only after evaluator validity, scope, causality, contradictions, freshness, and limitations are handled.

### Persistence

Durable state is not chat history.

Ambiguous external effects remain UNKNOWN until reconciled. They are not silently treated as success, failure, or safe-to-repeat.

### Interoperability

```
semantic contract != transport protocol
work archetype != protocol binding
peer completion != verification
artifact availability != truth
```

MCP, HTTP, A2A, Android-native surfaces, browser adapters, and provider APIs remain replaceable adapters.

### Provenance

Every promoted boundary must be traceable through:

```
repository + branch/ref + commit
+ specification revision
+ experiment/run
+ evidence
+ status/disposition
+ next verification
```

### Revision

Contradictions do not silently overwrite history:

```
Claim -> Contradiction -> bounded candidates -> explicit selection -> DecisionRevision
```

Automatic retraction remains disabled by default.

## 4. Repository responsibilities

### Portfolio-Repository-Inventory
Owns repository identity, census observations, relationships/lineage, cross-repository evidence references, review protocol, and portfolio decisions.

It must not become a runtime or semantic implementation dependency.

### Machine
Owns machine-native substrate semantics, frontier/resource experiments, substrate-contract experiments, adaptation/reflection research, and bounded research evidence.

It exports semantic claims, primitive candidates, receipts, and open questions—not canonical implementation merely because code exists.

### Open-System-One
Owns the smallest reusable decision contract, deterministic decision composition, provider/runtime neutrality, and this convergence record.

Its role is the integration nucleus, not a container for every legacy system.

### m0-durable-run
Owns durable Run identity, append-only execution state, replay/idempotency semantics, and the execution evidence boundary.

Provider-specific integration remains experimental until independently demonstrated.

### unified-knowledge-work-system
Owns task framing, relation-aware routing, specialist composition, project/plan continuity, evidence/assumption/validation workflow, coordination, and review policy.

Its framework/database choices remain implementation details above the semantic contract.

### Llms-mcp-android
Owns Android local execution authority, Action/Capability/Tool separation, approval and egress boundaries, lifecycle/recovery semantics, and device CapabilityExecutor adapters.

It exports semantic behavior, not Android-specific assumptions.

## 5. Propagation protocol

A cross-repository architectural change propagates as:

```
Observe
 -> identify owner
 -> extract smallest semantic contract
 -> record evidence/limits
 -> update central convergence record
 -> issue adoption packet
 -> implement local adapter/conformance
 -> run local verification
 -> record refs/evidence
 -> promote status
```

A commit in repository A never silently changes repository B.

Propagation is:

```
source contract
 -> adoption request
 -> local implementation
 -> local verification
 -> provenance update
```

not code copying.

## 6. Propagation classes

| Class | Meaning | Default propagation |
|---|---|---|
| SEMANTIC | shared meaning/contract | contract reference + conformance tests |
| CONFORMANCE | local implementation must satisfy contract | adapter/local test |
| PRIMITIVE | reusable implementation proven across contexts | isolated package/module + provenance |
| EVIDENCE | experiment/verification result | immutable receipt/reference |
| PRODUCT | user-facing behavior | product-local adapter |
| GOVERNANCE | lineage/status/decision | Portfolio record |

Default is SEMANTIC or CONFORMANCE. PRIMITIVE promotion requires stronger evidence.

## 7. Promotion gate

A boundary is promoted only when:

```
contract defined
+ independent implementation exercised
+ result verified
+ scope/limits recorded
+ contradictions checked
+ provenance pinned
+ regression protection added
```

Conversation agreement or repeated statements never promote a claim.

## 8. What we need to learn

### L1 — Canonical record intersection
Find the smallest common schema for Run, Observation, Verification, Evidence, Artifact, Claim, Decision, DecisionRevision, Relationship, Contradiction, and Gap.

Question:
Which fields are invariant across UWS, m0, Android, Machine, and Open-System-One?

### L2 — Cross-repository conformance
Can materially different implementations satisfy the same semantics for identity, terminal states, evidence linkage, replay, and contradiction handling?

### L3 — Capability/Verification contract
Define the smallest stable contract between Capability, CapabilityInvocation, Observation, Verification, and Evidence, including scope, effect identity, failure, and verification obligations.

### L4 — UNKNOWN outcome/reconciliation
Unify:
- failed before effect;
- effect unknown;
- effect confirmed;
- effect contradicted.

Do not assume exactly-once external effects.

### L5 — Provenance-aware egress
Define minimal shared semantics for source, data class, taint, destination, purpose, authorization, minimization, and redaction.

### L6 — Revision/contradiction
Find the smallest shared representation for competing observations/claims and bounded revision without silent deletion.

### L7 — Machine substrate boundary
Freeze the actual canonical Machine state-access contract before classifying indexed relation access as optimization/resource primitive/substrate extension.

### L8 — Evidence integrity
Require exact ref, command, inputs, environment, raw receipt, normalized result, verifier, disposition, and regression protection.

## 9. What we add now

First tranche:
1. this convergence contract;
2. per-repository adoption pointers;
3. machine-readable kernel-schema draft;
4. minimal cross-repository conformance fixtures;
5. gap/evidence register tied to exact refs.

Do not simultaneously add a universal workflow engine, provider swarm, plugin marketplace, distributed exactly-once semantics, or automatic repository synchronization.

## 10. First vertical integration slice

```
UWS Goal
 -> decision/action contract
 -> durable Run
 -> one concrete Capability
 -> Observation
 -> deterministic Verification
 -> Evidence
 -> inspectable result
```

Then reproduce the same semantic contract through a materially different path, preferably Android AgentRuntime, without making Android the canonical ontology.

Success means semantic agreement plus independent evidence, not shared code.

## 11. Immediate decisions

- Converge by semantic intersection and conformance, not repository merger.
- Open-System-One is the current integration target for the new unified implementation.
- Each specialist repository remains authoritative for its local implementation/evidence.
- Portfolio remains provenance/governance rather than runtime authority.
- The frontier remains provisional until exercised by actual implementations.

## 12. Current key gaps

| Gap | Status | Priority | Next action |
|---|---|---|---|
| common kernel intersection | OPEN | P0 | schema extraction |
| cross-repo conformance | OPEN | P0 | minimal shared fixtures |
| Capability/Verification | OPEN | P0 | reconcile Android + UWS/m0 |
| UNKNOWN effect | OPEN cross-system | P0 | common state/replay tests |
| provenance/egress | OPEN | P1 | define shared fields |
| evidence integrity | OPEN | P1 | receipt regression gate |
| product adapter boundary | OPEN | P1 | define product contract |
| Machine substrate contract | OPEN / SPECIFICATION DEBT | P1 | actual interpreter audit |
| UWS roadmap drift | OPEN | P2 | synchronize status after convergence |

This contract itself is PROVISIONAL until the first vertical slice and conformance tests execute successfully.
