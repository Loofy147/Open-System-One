# System-Wide Architecture Review v0.2 — 2026-10-02

Status: REVIEW SNAPSHOT / ARCHITECTURE REFINEMENT
Scope: Portfolio-wide architecture and mechanism review after the convergence tranche

## 1. Purpose

The previous convergence pass established a cross-repository contract and adoption mechanism.

This review widens the boundary.

The portfolio is not accurately represented by the six-repository convergence working set alone. The inspected corpus contains multiple independent implementations of execution, evidence, continuity, decision, research, assurance, domain integration, browser-local inference, mobile execution, security testing, and mathematical research.

The purpose of this record is to:
1. identify the semantic authorities that already exist;
2. distinguish system infrastructure from research, product, and historical/reference assets;
3. identify what may propagate between systems;
4. preserve hard non-merge boundaries;
5. identify the minimum cross-system contracts still requiring evidence;
6. record newly observed portfolio state.

This is not a final architecture decision.

## 2. Current portfolio boundary

A fresh GitHub repository search on 2026-10-02 returned 348 unique repository identities under Loofy147.

The prior persisted exact census was 339 repositories on 2026-09-22. All 339 persisted identities remain present in the current search result set.

Therefore:
- 339 = historical exact census snapshot;
- 348 = current exact GitHub search result used for this review;
- the increase is an observation of repository creation or visibility since the historical snapshot, not evidence that every new repository is architecturally relevant.

A separate 2026-09-28 discovery frontier had recorded 344 observed identities including later-seen MORPHS and other post-census observations. The 348 count supersedes that as the current exact search count for this review.

Evidence boundary:
repository identity was obtained from current GitHub repository search. Capability and architecture claims below require repository/ref/source evidence and are not inferred from names alone.

## 3. Revised architectural interpretation

The portfolio is better modeled as a federated system of semantic authorities than as one universal kernel.

Conceptual map:

Intent / Goal / Project
  -> UWS + product-local control

Decision / Planning
  -> Open-System-One + PIF + domain policy

Authorization / Execution
  -> canonical-capability-core + Android local runtime

External effects / tools / providers
  -> adapters + TOL + staging authority

Observation / Evidence
  -> My_browser + Core + domain assurance

Claims / Context / Continuity / History
  -> recursive-audit + ledger + Conversational

Cross-cutting:
provenance + versioning + verification + recovery + privacy

This is a conceptual map, not a runtime topology.

The key correction is that no single repository should automatically own every noun appearing in the map.

## 4. Semantic authorities already present

### 4.1 Capability lifecycle and executable effect authority

Loofy147/canonical-capability-core
ref/commit: master @ 6396327425e7f5e6c23456579ebc286ca69f771f

Observed assets:
- canonical capability state/lifecycle;
- qualification and contextual authority;
- action/preflight boundaries;
- durable execution;
- reconciliation;
- evidence validity/sufficiency;
- explicit UNKNOWN_OUTCOME semantics;
- adversarial mutation/replay verification;
- versioned immutable and candidate release surfaces.

Important evidence already recorded by the repository includes a v0.16 baseline and later candidate/staging lines, with explicit checksums and test records.

Current interpretation:
canonical execution-authority candidate, with unresolved promotion-blocking gaps.

Do not treat release/extraction directories as a second canonical implementation.

Known open boundaries include post-approval enforcement, reserve-vs-dispatch durability, crash/restart semantics, reconciliation authority, idempotency scope, and the distinction between validity and sufficiency of evidence.

### 4.2 Independent staging authority

Loofy147/external-staging-authority
ref/commit: main @ 5e313c05245dfa5b646d3b80713b74d443b8c528

Observed role:
- synthetic, non-destructive external-effect service;
- durable effect/command identity;
- idempotency and attempt tracking;
- reconciliation surface;
- authority classification;
- failure-injection modes.

The repository explicitly states that it is staging authority and not production/external-world authority.

This is an important architectural component because it provides a separate failure/reconciliation boundary without granting production semantics.

### 4.3 Evidence acquisition and provenance kernel

Loofy147/My_browser
ref/commit: main @ 402121c0e6cf9294d8e71feecd5752eade859807

Observed role:
Execution -> Observation -> Evidence -> Verification -> Provenance / History

Implemented scope includes:
- canonical JSON normalization;
- SHA-256 artifact identity;
- observation/evidence identities;
- raw artifact retention;
- transformation lineage and replay;
- SQLite persistence;
- external MCP-result ingestion bridge.

Important limits:
- jsdom is not a real browser;
- the MCP bridge is not an MCP client;
- hashing proves integrity/identity, not source authenticity;
- cryptographic provenance remains open;
- clean-clone CI/release gate remains open.

Current interpretation:
reusable evidence-acquisition mechanism candidate.

### 4.4 Minimal durable execution

Loofy147/m0-durable-run
ref/commit: main @ 69b07a54e4b2f8421532b78b8abffca308bbe3da

Observed role:
- append-only Run envelope storage;
- schema validation;
- deterministic run identity;
- idempotent replay;
- process-restart recovery;
- Experiment -> Run -> Evidence path;
- HTTP boundary/fingerprinting.

Current interpretation:
minimal durable execution/reference substrate.

It should not be expanded into a universal provider abstraction until a materially different implementation demonstrates a stable shared boundary.

### 4.5 Orchestration and project control

Loofy147/unified-knowledge-work-system
ref/commit: main @ 683c38fdc3c921c1d7977786d5b5ed8617969476

Observed role:
- project/plan/task orchestration;
- evidence and assumptions;
- validations;
- persistence/events;
- routing;
- execution gates;
- explicit distinction between result and conclusion;
- permission authority separate from agent reasoning.

Current interpretation:
control-plane / orchestration authority.

UWS should compose execution primitives rather than reimplement durable effect semantics.

### 4.6 Local mobile execution authority

Loofy147/Llms-mcp-android
ref/commit: main @ 4880767491d29a5f105765683c8224c82244d1a7

Observed role:
- Activation;
- Action;
- Capability;
- Policy;
- Approval;
- Egress;
- Run lifecycle;
- CapabilityInvocation;
- Observation;
- Verification;
- Evidence;
- durable effect reservation and UNKNOWN recovery.

Critical boundary:
Model proposes -> Policy authorizes -> Capability executor acts -> Verifier checks -> Evidence records.

Current interpretation:
independent execution-authority implementation whose semantics are useful for conformance testing.

Android-specific storage/UI/provider details must remain local.

### 4.7 Typed decision substrate

Loofy147/Open-System-One
ref/commit: main @ 0e84832f9478895d30f97cfeb2a20ca2ecdcf95b0

Observed role:
- opaque decision state contract;
- typed independent questions;
- finite outcome spaces/distributions;
- deterministic composition;
- scoring/calibration/abstention/policy layers;
- replaceable model/runtime backends;
- research/evidence structure.

Current interpretation:
decision-semantic anchor and convergence documentation host.

It is not yet justified as the universal execution/evidence kernel.

### 4.8 Decision/context ledger

Loofy147/ledger-system-source-of-truth
ref/commit: main @ e63a92171f6c5b3a4958157be979347857f6a809

Observed role:
- goals;
- constraints;
- findings;
- decisions;
- contradiction detection;
- supersession;
- deterministic history/digest.

Current interpretation:
decision/context state authority.

A decision record does not become evidence merely because it is canonical within the ledger.

### 4.9 Claim/evidence graph and truth-maintenance research

Loofy147/recursive-audit
ref/commit: main @ d89908a99a2eb2330144927483b7538b612dfb1d

Observed role:
- directed claim/evidence graph;
- bi-temporal representation;
- dependency audits;
- contradiction/defeater handling;
- retraction propagation;
- branch isolation;
- trace parsing;
- graph realignment.

Current interpretation:
knowledge/evidence maintenance plane.

It must not become an action authority.

### 4.10 Conversation continuity authority

Loofy147/Conversational
ref/commit: main @ f65be73b9f6b8ac0d91f8e80f0b4e3da44d2a0cd

Observed role:
- event-log to canonical-state reduction;
- revisioned frontier state;
- provenance and lineage verification;
- restore protocol;
- publication boundary;
- explicit separation between restored context and action authorization.

Current interpretation:
continuity and reconstruction authority.

Restore is still explicitly UNVERIFIED for a genuinely fresh conversation.

### 4.11 Research ecology and adaptive verification

Loofy147/MORPHS
ref/commit: main @ 02ea1719a0472beffb9e67218dd508f6daabd249

Observed frontier:
- explicit capability binding;
- real read-only GitHub adapter;
- run-bound receipt;
- independent same-commit verification;
- blob identity checks;
- evidence/epistemic-state discipline;
- preserved negative findings.

Current interpretation:
research environment providing independent evidence about portable capability/verification semantics.

The repository explicitly does not establish unrestricted mutation, provider-independent verification, cryptographic receipt authenticity, or production capability-registry semantics.

## 5. Domain and assurance planes

### Algeria AI Product Fabric

Loofy147/algeria-ai-product-fabric
main @ b3545b83b1592a54a839932adfe9c0f74a8fe2bb

Observed:
- evidence-first document/decision vertical;
- deterministic decision and validation;
- domain contracts;
- adapter boundaries;
- evaluation/mutation cases;
- Algeria-specific integration layer.

Interpretation:
domain composition layer.

It is a strong candidate for the first real vertical proof because it combines extraction, decision, evidence and local adapters without pretending to be the universal kernel.

### Software-res

Loofy147/Software-res
main @ 138a6be19fe4e4bcd008df2e7ba33588b31ca863

Observed:
- explicit evidence contracts;
- fail-closed collection/validation;
- non-compensatory reliability vector;
- deterministic policy;
- controlled fixtures;
- mutation testing;
- local cryptographic proof-of-concept.

Interpretation:
software-assurance vertical.

It should contribute assurance patterns and verification fixtures, not become the universal evidence/authority implementation.

### Global Red Team

Loofy147/Global-redteam
main @ 9cca0b01e1440f749451a682ea9aa9433ba69f37

Observed:
- adversarial security suites;
- orchestration;
- findings history;
- SAST/fuzz/property/race testing;
- vulnerable target environment.

Interpretation:
security/adversarial validation plane.

Its orchestration is not automatically portable as execution authority.

### Digital Twin

Loofy147/digital-twin
main @ 7f1806dd2976a3233207ab6bf7e65d7026d473d3

Observed:
- privacy-first decision support;
- versioned assessment bank;
- interpretable profile inference;
- scenario simulation;
- idempotent training jobs;
- consent and audit;
- provider-neutral connector interfaces;
- export/deletion/retention structures.

Interpretation:
product-domain composition with useful privacy/consent/job-state patterns.

The repository explicitly warns that its model is not a factual replica and that production authentication and privacy hardening remain incomplete.

## 6. Browser/local model layer

Loofy147/All-time-
main @ c9f8662acde83808b64ad75ac8bef4ee67edd5da

Observed:
- browser-local inference;
- WebGPU with fallback;
- pinned model revisions;
- PWA shell;
- CI build/provenance;
- run-level evidence metadata.

Interpretation:
client/runtime layer.

The current branch itself marks product persistence, deterministic acceptance, Android/PWA behavior, structured failure taxonomy, and broader compatibility as open.

This is an implementation surface where a portable evidence kernel can be tested, not evidence that browser runtime semantics belong in the control plane.

## 7. Machine and mathematical research layer

### Machine

Loofy147/Machine
main @ 2d5f6bd0513ecd2d9f29f395d4d95c90849b2648

The machine-native research line remains materially separate from application/control-plane architecture.

Observed frontier includes:
- executable representation change;
- same-process evaluator hot-swap;
- history-conditioned proposal policy;
- context-indexed history;
- error-source localization;
- substrate/frontier research.

Current major OPEN boundary:
the canonical fixed Machine state-access/interpreter contract.

Interpretation:
substrate research plane.

### Delta-bedrani

Loofy147/Delta-bedrani

Observed:
- deterministic exact matching-set enumeration;
- finite-field Tutte certificate path;
- explicit UNKNOWN handling for randomized zero;
- Bouchet/Wenzel exchange experiments;
- exact set-system operations.

Interpretation:
mathematical verification/research asset.

This should not be absorbed into the application kernel merely because it uses strong exactness discipline.

### Global-theorem / FSO / HAG family

The inspected repositories contain substantial mathematical, topological, agentic, and systems material.

Current interpretation:
research/reference family.

Repository claims include stronger production/autonomy language than the currently verified evidence boundary justifies. Those claims must remain scoped to actual experiments and fixtures.

Do not use these repositories as architectural authorities merely because their concepts overlap with Machine, agent, or system language.

## 8. External / upstream / reference assets

The portfolio also contains repositories whose content is evidently an upstream or external software surface, for example the limit-order-protocol repository whose README is the upstream 1inch protocol documentation.

Other names in the corpus similarly indicate imported/reference software or external ecosystems.

Rule:
external software != first-party primitive != evidence of original architecture.

Such repositories may still be valuable as references, dependencies, benchmarks, or comparison targets.

## 9. Killed and historical research

Compute-Qualification-Infrastructure is explicitly KILLED as a product opportunity on 2026-08-31.

Its research remains useful for:
- qualification-state distinctions;
- benchmarking/procurement analysis;
- change-impact questions;
- heterogeneous infrastructure governance.

Correct disposition:
KILLED PRODUCT / RETAIN RESEARCH.

A killed opportunity must not silently return as an implementation requirement under a new name.

## 10. Hard non-merges

Do not collapse:
- optimization into verification;
- evaluation into verification;
- verification into authorization;
- consensus into truth;
- decision history into evidence;
- communication into execution authority;
- restored context into action permission;
- product domain policy into universal policy;
- browser runtime state into canonical control-plane state;
- mathematical research substrate into application semantics;
- simulator evidence into production external-world authority.

The same noun in two repositories is not sufficient reason to merge implementations.

## 11. What can propagate

Propagation should occur by semantic class.

### Semantic contract
A stable invariant or interface can propagate when at least two materially different implementations demonstrate the same behavior.

Example:
UNKNOWN_OUTCOME must prevent blind replay until reconciliation.

### Conformance artifact
A test vector, fixture, schema case, failure injection, or verification rule can propagate when its assumptions remain explicit.

### Primitive candidate
A code primitive can propagate only after isolation and cross-context validation.

### Evidence
Evidence should propagate by reference, not by copying prose. Preserve:

source repository
-> ref/commit
-> execution/observation
-> artifact
-> claim

### Product adapter
Product-specific mapping can propagate implementation knowledge without promoting product assumptions into the universal kernel.

## 12. What should not propagate automatically

Do not copy:
- whole repository architectures;
- provider-specific models;
- storage technologies;
- UI/runtime details;
- unverified confidence scores;
- historical README claims;
- simulator behavior as production guarantees;
- domain-specific ontology;
- execution authority merely because a planner can name an action.

## 13. New architecture gaps exposed by the wider review

### G11 — semantic-authority registry

We need a durable machine-readable map of:

semantic concern
-> authority repository
-> exact ref/commit
-> evidence status
-> known defects
-> consumers
-> superseded authorities

Without this, convergence documentation can itself become another projection that drifts from actual ownership.

### G12 — evidence reference protocol

Cross-system evidence currently exists in several incompatible local forms.

We need a minimal reference protocol for:
- source identity;
- run/observation identity;
- artifact identity;
- verification event;
- claim linkage;
- validity/scope.

This must be smaller than any local evidence schema.

### G13 — authority handoff semantics

A portable action must distinguish:
- proposed;
- qualified;
- authorized;
- dispatched;
- observed;
- verified;
- reconciled.

The current systems demonstrate pieces of this independently, but the cross-runtime ordering and failure semantics are not yet proven.

### G14 — continuity / execution boundary

Conversation restoration, durable Run recovery, and external-effect reconciliation all preserve history differently.

We need to prove where:
context continuity
!=
execution continuity
!=
external-world continuity

remain separate and where they may legitimately compose.

### G15 — current-vs-research authority

The portfolio contains many advanced research branches and large README claims.

We need a machine-readable distinction between:
- default-branch implemented state;
- validated research state;
- historical evidence;
- product target;
- speculative design.

The existing portfolio protocol describes this, but it is not yet a fully enforced cross-repository mechanism.

### G16 — upstream provenance

External or copied repositories can distort portfolio architecture if treated as native assets.

The inventory needs explicit provenance fields for:
- native/original;
- fork;
- copied/imported;
- upstream mirror;
- dependency/reference;
- generated artifact.

## 14. What we need to learn next

The critical learning questions are now narrower.

### Learn whether the same execution invariant survives different implementations
Compare:
- canonical-capability-core;
- m0-durable-run;
- Llms-mcp-android;
- MORPHS.

### Learn whether evidence identity survives acquisition boundaries
Compare:
- My_browser;
- MORPHS;
- canonical-capability-core;
- Software-res.

### Learn whether continuity adds execution semantics or only reconstruction
Compare:
- Conversational;
- m0-durable-run;
- UWS.

### Learn whether typed decision state composes with evidence without becoming a truth oracle
Compare:
- Open-System-One;
- ledger-system-source-of-truth;
- UWS;
- recursive-audit.

### Learn whether domain systems consume the kernel cleanly
Use:
- Algeria AI Product Fabric;
- Digital Twin;
- All-time.

### Learn which research assets actually produce transferable primitives
Prioritize mechanism-level results from:
- Machine;
- Delta-bedrani;
- MORPHS;
- Global Red Team;
- Software-res.

## 15. Required implementation additions

The wider review changes the implementation target.

Do not start by expanding the canonical record schema into a large universal ontology.

Add instead:
1. semantic-authority registry;
2. evidence-reference contract;
3. authority-handoff conformance vectors;
4. current/research/historical provenance classification;
5. upstream/native provenance field;
6. cross-runtime test harness;
7. one real vertical proof.

The first vertical proof should remain:

UWS Goal
-> decision/action contract
-> durable Run
-> concrete Capability
-> Observation
-> deterministic Verification
-> Evidence
-> inspectable result

Then repeat the same semantic contract through a materially different execution path.

## 16. Architectural decision boundary

Current status:
- Portfolio-wide final architecture: OPEN
- Federated semantic-authority model: INFERENCE / STRONGLY SUPPORTED BY CURRENT PORTFOLIO STRUCTURE
- Open-System-One as convergence documentation host: ESTABLISHED
- Open-System-One as universal runtime kernel: NOT ESTABLISHED
- canonical-capability-core as execution-authority candidate: ESTABLISHED AS EXISTING IMPLEMENTATION / PROMOTION OPEN
- UWS as control-plane candidate: ESTABLISHED AS EXISTING IMPLEMENTATION
- My_browser as evidence-acquisition candidate: EXPERIMENTALLY_SUPPORTED WITHIN DECLARED SCOPE
- MORPHS as independent conformance/research source: EXPERIMENTALLY_SUPPORTED WITHIN DECLARED SCOPE
- machine-native research as application architecture: NOT ESTABLISHED
- universal ontology: NOT REQUIRED / DEFERRED

## 17. Governing rule after this review

The portfolio should converge by contracts, authorities, evidence and conformance, not by repository merging.

The architecture is the set of stable semantic boundaries that survive independent implementations.

Everything else remains local until that survival is demonstrated.
