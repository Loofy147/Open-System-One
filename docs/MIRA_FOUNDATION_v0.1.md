# MIRA — Machine Intelligence Reference Architecture
## Foundation v0.1

**Status:** FOUNDATION / PROVISIONAL DESIGN / REVIEW REQUIRED  
**Recorded:** 2026-10-30  
**Integration repository:** `Loofy147/Open-System-One`  
**Branch:** `architecture/mira-foundation-v0.1`  
**Role:** Cross-system reference architecture and contract map. Not a universal runtime, executable framework, or claim of validated general intelligence.

## 1. Purpose

MIRA is a reference architecture for investigating and constructing machine-intelligence systems from differentiated computational capabilities, their coordination, their state and memory, and their interaction with environments.

It addresses two coupled levels:

1. **Within a system:** the native operations, representations, state transitions, adaptation mechanisms and constraints of individual computational components.
2. **Across the whole system:** how components coordinate, share grounding, manage objectives and resources, interact with environments, preserve continuity and produce verifiable outcomes.

Neither level alone is sufficient as an architecture description. A single model's properties do not automatically describe the capabilities of the whole system; whole-system behaviour does not automatically explain the mechanisms of its components.

MIRA must preserve this distinction and allow evidence to move between levels only through explicit contracts and verification.

## 2. Foundational position

### 2.1 Coherence without uniformity

A machine-intelligence system need not reduce every capability to one model, representation, reasoning style or execution process.

Different modules may specialize in:
- statistical and pattern-based computation;
- symbolic, logical and constraint-based operations;
- search, planning and structured deliberation;
- prediction and learned environment models;
- retrieval and evidence inspection;
- perception and interaction with digital, simulated or physical environments;
- distributed or collective computation;
- verification, monitoring and adversarial evaluation.

This is a candidate capability palette, not a mandatory module checklist. A capability belongs in a system only when its contribution, interface, cost and failure modes justify it.

### 2.2 Coordination is not a monolith

The architecture needs coordination functions: task characterization, decomposition, routing, synchronization, arbitration, resource allocation and conflict handling.

These functions do not have to be concentrated in one all-knowing central model. Coordination may be hierarchical, distributed, peer-based or hybrid. The topology is a design variable to evaluate, not a fixed premise.

A coordinator can itself become a bottleneck, a source of correlated error or a single point of failure. MIRA therefore requires explicit observability, fallback and arbitration contracts.

### 2.3 Machine-native foundations remain open research

MIRA does not prescribe human cognition as the underlying implementation.

The Machine research line uses an implementation-independent working model built around:
- State;
- Operation;
- Transition;
- Control / scheduling.

It distinguishes structural execution from optional mechanisms that modify the operation space or operating regime. It also explicitly separates reconfigurability, adaptation, learning, reusable learning and causal reflection.

These are useful research boundaries. They are not a completed universal primitive set. In particular, the Machine project records general-purpose machine intelligence, context discovery and causal reflection as unestablished or open.

MIRA must not promote a mechanism to a universal architectural primitive merely because it has a useful name.

### 2.4 Learning and embodiment are not universal prerequisites

Learning is one possible mechanism for changing future behaviour, not a definition that every intelligent system must satisfy. Likewise, physical embodiment is not assumed to be mandatory: a system may be situated in a digital, simulated, organizational or physical environment.

The architecture distinguishes:
- an internal state change;
- a policy or operating-regime change;
- a representation or executable-structure change;
- a capability that transfers to held-out conditions;
- a persistent effect of interaction with an environment.

These claims require separate tests. MIRA makes no claim about consciousness or subjective experience.

### 2.5 Memory is allocation under uncertainty

Future queries and goals are not generally known when information is written. A memory system should not be designed around the assumption that it can perfectly predict future importance.

MIRA separates:
- **Active state:** compact, currently usable representations.
- **Addressable evidence:** exact or provenance-preserving records that can be retrieved.
- **Working context:** the bounded information currently exposed to a process.
- **Access and retrieval:** the mechanisms and budget for finding, checking and incorporating stored information.

The State–Evidence–Access framework is a useful recent research lens, not a universal physical architecture.

The design requirement is to preserve recoverability while adapting retention, compression and access policies as workloads change. Retention utility, retrieval cost, staleness, distribution shift and irreversible loss must be evaluated together.

### 2.6 Agency, autonomy and execution are different boundaries

MIRA distinguishes:

| Concept | Meaning |
|---|---|
| Intelligence | Produces representations, analyses, hypotheses, predictions and candidate solutions. |
| Agency | Forms or adopts intentions and initiates purposeful activity within a mandate. |
| Autonomy | Defines the permitted degree of independent selection and operation. |
| Authorization | Determines which actions are permitted under policy and authority. |
| Execution | Performs an authorized capability and records its outcome. |
| Verification | Checks whether observed outcomes support the required claims. |

A model or module may propose objectives. Proposal does not itself authorize adoption or execution. Candidate objectives, adopted objectives, policy constraints and permission decisions must remain distinguishable.

### 2.7 Grounding is shared reference, not forced shared representation

Modules may use different internal representations. MIRA requires enough shared grounding to coordinate:
- stable identities and references;
- current observations and their provenance;
- task and environmental context;
- objective and constraint references;
- evidence and uncertainty;
- resource and execution state.

Shared grounding does not mean all modules must use one internal world model. Translation between representations must retain provenance, uncertainty and known information loss.

## 3. Architecture overview

The architecture is expressed as cooperating planes. Their exact deployment topology is intentionally unspecified.

```
                ENVIRONMENTS
       digital / simulated / physical
                    |
           observation and feedback
                    |
                    v
+------------------------------------------------+
|             GROUNDING AND CONTEXT              |
| identity | context | world references | goals  |
| constraints | evidence | provenance | versions |
+----------------------+-------------------------+
                       |
                       v
+------------------------------------------------+
|          COORDINATION / ORCHESTRATION           |
| characterize | decompose | route | arbitrate   |
| synchronize | allocate resources | recover     |
+---------+--------------+-------------+----------+
          |              |             |
          v              v             v
   +-------------+ +-------------+ +-------------+
   | Capability  | | Capability  | | Capability  |
   | module A    | | module B    | | module C    |
   | native form | | native form | | native form |
   +------+------+ +------+------+ +------+------+
          |              |             |
          +--------------+-------------+
                         |
                         v
+------------------------------------------------+
|               MEMORY AND ACCESS                 |
| active state | working context | evidence store|
| retrieval | compression | retention | recovery |
+----------------------+-------------------------+
                       |
                       v
+------------------------------------------------+
|          DECISION / AGENCY / AUTONOMY           |
| objective proposal | adoption | policy | limits|
+----------------------+-------------------------+
                       |
                 authorization
                       |
                       v
+------------------------------------------------+
|           CAPABILITY EXECUTION                  |
| durable run | external effect | lifecycle      |
+----------------------+-------------------------+
                       |
                       v
+------------------------------------------------+
|       OBSERVATION / VERIFICATION / EVIDENCE     |
| outcome | reconciliation | claim | revision    |
+----------------------+-------------------------+
                       |
                       +------ feedback to context,
                              memory and modules

Cross-cutting: resource limits, security, provenance,
governance, observability, versioning and recovery.
```

This is a conceptual map, not a claim that all listed planes are implemented or must be separate processes.

## 4. Plane responsibilities and contracts

### 4.1 Substrate and execution semantics

Defines what can execute and how state changes.

Candidate concerns:
- state representation and access;
- executable operations and composition;
- transition semantics;
- scheduling and concurrency;
- resource accounting;
- interruption, continuation and recovery.

**Primary research owner:** `Loofy147/Machine`.

Machine's abstract-machine and substrate work remains authoritative for its local research claims. The exact state-access and interpreter contract is still recorded as specification debt in the convergence gap register. MIRA must not assume this boundary is fully frozen.

### 4.2 Capability modules

A module exposes a bounded capability through a replaceable interface. Its implementation can be a model, algorithm, tool, interpreter, device interface, retrieval system or another executable component.

A module contract should state:
- identity and version;
- accepted inputs and produced outputs;
- representation assumptions;
- required context and dependencies;
- resource profile;
- uncertainty and failure modes;
- authority required for effects;
- provenance for outputs and derived claims.

A module's internal representation remains local unless a concrete interoperability requirement justifies translation.

### 4.3 Coordination and orchestration

Coordinates capability use without owning every capability's internal reasoning.

Required functions:
1. characterize request, context and constraints;
2. decompose work when useful;
3. select candidate modules;
4. choose sequential, parallel, competitive or iterative execution;
5. allocate compute, time, memory and external-call budgets;
6. collect outputs with provenance;
7. detect disagreement and route it to arbitration or verification;
8. recover from partial, failed or unknown outcomes.

The coordinator must not convert an unverified module output into ground truth. It must not acquire execution authority merely because it can route a task.

### 4.4 Grounding and shared context

Provides stable references and current context while preserving source provenance.

The initial semantic intersection should remain small. Reuse the existing record-envelope and convergence work rather than creating a second universal ontology.

Candidate shared records include:
- intent or goal reference;
- plan or proposal reference;
- policy and authorization reference;
- run and capability-invocation identity;
- observation and evidence reference;
- artifact identity;
- claim and decision reference;
- contradiction, gap and revision reference.

Local repositories may retain richer schemas. Cross-system records should carry only the fields needed for interoperability, identity and verification.

### 4.5 Memory and information access

Uses the decomposition in Section 2.5. It should support more than one retention policy and should expose retrieval cost and evidence provenance.

Memory policies must be evaluated against:
- workload distribution and shifts;
- expected task utility;
- worst-case or lower-tail degradation;
- exact retrieval and state-update quality;
- staleness and contradiction;
- storage and access cost;
- recoverability and irrecoverable-loss rate.

The detailed corrected research record is maintained by Machine:
[`MEMORY-UNDER-UNCERTAINTY-RESEARCH-v0.1.md`](https://github.com/Loofy147/Machine/blob/f96cff40f922797a8055d1d437837c9e3805cbad/docs/MEMORY-UNDER-UNCERTAINTY-RESEARCH-v0.1.md).

Its synthetic measurements are user-reported and not independently reproduced in this foundation. Their status must remain visible.

### 4.6 Decision, agency and autonomy

The decision boundary consumes typed requests, candidate outcomes, evidence and explicit constraints. It returns structured results and dispositions.

Open-System-One's existing decision contract and scoring/policy separation are relevant here. Its foundation PR remains separately reviewable; this MIRA document does not imply that the PR is merged or that all its implementation claims are canonical.

Candidate objective generation should be separated from objective adoption. Adoption requires a mandate, policy or other explicit rule. Autonomy defines how much selection may occur without further human or external approval; it does not remove the need for authorization boundaries.

### 4.7 Capability execution and durable runs

An authorized capability invocation crosses an execution boundary. It should have stable identity, lifecycle state, idempotency semantics where applicable, and recovery/reconciliation behavior.

The existing convergence contract assigns durable Run semantics to `m0-durable-run` and local Android effect authority to `Llms-mcp-android`. Those ownership declarations were recorded in the 2026-10-02 convergence snapshot and must be revalidated against current repository heads before implementation adoption.

Unknown external outcomes must remain UNKNOWN until reconciled. They must not be silently treated as success, failure or safe-to-repeat.

### 4.8 Observation, verification and evidence

The output of an action and the evidence supporting a claim are not the same object.

```
Observation != Evidence
Evidence != Claim
Claim != Decision
Result != Conclusion
```

Evidence should retain source, acquisition path, artifact identity, transformation lineage, verifier, scope, limitations and exact provenance.

Verification must be distinct from the component that produced the result. A green test is evidence only for the test's declared scope.

### 4.9 Governance, trust and resource control

Cross-cutting controls include:
- identity and access;
- mandate and authorization;
- data provenance, sensitivity and egress;
- resource budgets and quotas;
- audit records;
- versioning and controlled revision;
- failure containment;
- rollback or compensating actions where valid;
- explicit UNKNOWN and contradiction states.

Security and governance apply to the interfaces and transitions between planes, not only to individual models.

## 5. Operational and epistemic spines

The existing Open-System-One convergence contract defines a small record graph. MIRA adopts it as the initial operational/evidence spine rather than replacing it.

```
Operational:
Intent / Goal -> Candidate / Plan / Action
 -> Policy / Authorization -> Run -> Capability

Execution:
Run -> CapabilityInvocation -> Observation
 -> Verification -> Evidence -> Artifact

Epistemic:
Evidence -> Claim -> Decision
 -> DecisionRevision / Contradiction / Gap
```

These spines intersect through stable identities and provenance. They must not be collapsed into one universal object.

The current canonical record envelope is still a draft. Its fields and conformance requirements need implementation evidence before they become a production-wide contract.

## 6. Repository ownership and propagation

The current repository map follows the existing convergence contract and system-wide architecture review. These are dated ownership records, not a fresh audit of every repository as of this document's date.

| Repository / system | Existing declared responsibility | MIRA relationship |
|---|---|---|
| `Machine` | Machine-native substrate, primitive and resource research, adaptation/reflection experiments | Research authority for substrate and memory findings; exports bounded claims and evidence |
| `Open-System-One` | Decision semantics and convergence documentation | Hosts this provisional MIRA reference and shared semantic contracts |
| `unified-knowledge-work-system` | Task framing, routing, project/plan continuity and coordination | Orchestration/control-plane authority |
| `m0-durable-run` | Durable Run identity, append-only execution state, replay and recovery | Durable execution contract |
| `Llms-mcp-android` | Android local execution authority, approvals, capability invocation and recovery | Device/runtime execution adapter and independent conformance path |
| `canonical-capability-core` | Capability lifecycle and execution-authority candidate | Candidate capability/authorization implementation; promotion status must be refreshed |
| `My_browser` | Evidence acquisition, artifact identity and transformation lineage | Evidence acquisition candidate |
| `recursive-audit` | Claim/evidence graph, contradiction and truth-maintenance research | Epistemic maintenance research/authority candidate |
| `Portfolio-Repository-Inventory` | Repository identity, lineage and cross-repository provenance | Governance and ownership registry, not runtime authority |

### Propagation rule

Cross-repository propagation is contract-first:

```
observe
 -> identify semantic owner
 -> extract smallest contract
 -> attach evidence and limitations
 -> request adoption
 -> implement local adapter/conformance
 -> verify independently
 -> update provenance and status
```

A commit in one repository does not silently change another repository. Similar terminology does not establish code lineage or semantic equivalence.

Propagate:
- semantic contracts;
- conformance fixtures;
- isolated primitives with demonstrated portability;
- evidence by reference;
- product-specific adapters.

Do not automatically propagate:
- complete repository architectures;
- provider or model assumptions;
- runtime/storage choices;
- unverified benchmark claims;
- execution authority;
- experimental code as a production dependency.

## 7. Research status: what is and is not established

| Proposition | Current status | Reason / boundary |
|---|---|---|
| Machine-native operational model with State, Operation, Transition and Control is a useful research abstraction | RESEARCH FOUNDATION / OPEN | Defined by Machine's abstract model; not a completed universal substrate. |
| Some executable representations can be changed and affect later behaviour | EXPERIMENTALLY_SUPPORTED in specific Machine regimes | Does not establish reusable learning or general intelligence. |
| Context-indexed history can improve policy in tested settings when context labels are supplied | EXPERIMENTALLY_SUPPORTED in a bounded experiment | Does not establish context discovery. |
| Current Machine hot-swap experiment proves causal reflection of the evaluator | NOT ESTABLISHED | The research line explicitly identifies this as an open gap. |
| Heterogeneous modules can be coordinated through stable interfaces | ARCHITECTURAL HYPOTHESIS | Requires independent implementations and conformance evidence. |
| Whole-system intelligence may exceed the isolated capabilities of a single module | RESEARCH HYPOTHESIS | Must be tested with matched-resource ablations and interaction controls. |
| State, Evidence and Access are useful distinctions for hybrid memory | LITERATURE-BACKED FRAMEWORK | Recent survey; not a universal implementation prescription. |
| The supplied synthetic memory results are independently reproduced | NOT ESTABLISHED | Raw source, seed ledger and reproduction receipt are not yet committed. |
| A general MIRA architecture has been experimentally validated | NOT ESTABLISHED | This document establishes a design foundation only. |

## 8. Initial assumptions register

Every open assumption requires an owner and a falsification method. Ownership below identifies the repository or research responsibility, not a person.

| ID | Open assumption / question | Owner | Falsification or closure test |
|---|---|---|---|
| MIRA-A01 | Differentiated modules provide a measurable advantage over a single module under matched resources. | MIRA research / Open-System-One | Compare single-module, heterogeneous and ablated systems on held-out tasks with matched compute, latency and memory budgets. |
| MIRA-A02 | Coordination can improve system performance without becoming a dominant bottleneck or correlated-error source. | UWS / orchestration research | Measure end-to-end utility, overhead, failure propagation and recovery against distributed and non-orchestrated controls. |
| MIRA-A03 | Shared grounding can preserve identity and provenance while allowing module-specific representations. | Open-System-One | Run cross-module and cross-runtime conformance tests with ambiguous, stale and contradictory context. |
| MIRA-A04 | A state-plus-evidence-plus-access memory design improves recoverability under changing demand. | Machine | Run the size-matched and distribution-shift experiments in the Machine memory record; include a no-archive control. |
| MIRA-A05 | Future-use predictors can provide useful write-time admission signals on non-stationary workloads. | Machine | Compare strict insertion-time features with online policies and hindsight oracle on held-out temporal/query distributions. |
| MIRA-A06 | Candidate objectives can be generated without hidden objective injection and remain within an explicit mandate. | Machine / MIRA research | Use hidden-regime and adversarial tests; inspect the source of each objective and enforce separate proposal/adoption gates. |
| MIRA-A07 | The same execution and evidence contracts can be satisfied by materially different runtimes. | Open-System-One + execution owners | Run identical conformance fixtures through at least two independent implementations; preserve all mismatches. |
| MIRA-A08 | Unknown external effects can be recovered without blind duplicate execution. | m0-durable-run / Android execution owner | Crash/restart and ambiguous-response injection with idempotency and reconciliation checks. |
| MIRA-A09 | Digital or simulated interaction can provide sufficient grounding for some capabilities without physical embodiment. | MIRA research | Compare transfer and failure under digital, simulated and physical observation boundaries for a specified task family. |

## 9. Evaluation principles

No single score establishes MIRA capability. Evaluation must state its unit of analysis and include component-level and system-level results.

### Component-level
- task quality and generalization;
- latency, throughput and resource use;
- uncertainty and calibration where relevant;
- representation assumptions;
- failure modes and robustness;
- module-specific ablations.

### System-level
- end-to-end task utility;
- coordination overhead;
- conflict detection and arbitration quality;
- recovery from partial and unknown outcomes;
- performance under module failure and distribution shift;
- memory and retrieval effectiveness;
- authority and policy violations;
- reproducibility and evidence completeness.

### Causal controls
- remove or replace a module;
- remove shared context or provenance;
- change the coordination topology;
- limit or disable retrieval;
- erase or shuffle history;
- introduce conflicting evidence;
- inject stale observations;
- change future workload distribution;
- compare with a resource-matched monolithic or simpler baseline.

Claims should be promoted only within the task, model, environment and budget envelope actually tested.

## 10. Gate-based foundation roadmap

This roadmap is dependency-driven, not date-driven.

### Gate F0 — Ownership and provenance
- confirm the current refs of all declared authority repositories;
- preserve branch/commit-level provenance;
- reconcile existing open foundation and convergence PRs;
- do not merge or delete research branches merely to reduce branch count.

**Exit:** current ownership ledger with exact refs, open conflicts and adoption boundaries.

### Gate F1 — Semantic foundation
- review this MIRA foundation;
- reconcile it with the canonical convergence contract and existing kernel schema;
- identify the smallest common record and capability interfaces;
- keep unresolved fields explicitly OPEN.

**Exit:** approved v0.1 semantic boundary and machine-readable conformance fixtures.

### Gate F2 — Independent conformance
- implement the same minimal contracts in two materially different systems;
- test identity, terminal states, provenance, verification and UNKNOWN outcomes;
- retain mismatches as evidence.

**Exit:** independently passing conformance receipts, not shared-code-only tests.

### Gate F3 — Memory and recoverability
- reproduce the corrected synthetic memory results;
- execute the discriminating memory experiments;
- compare state, evidence, access and hybrid approaches under matched budgets.

**Exit:** source-bound results and explicit promotion/disposition of each claim.

### Gate F4 — Heterogeneous coordination
- compose a small number of materially different capabilities;
- compare centralized, hierarchical and distributed coordination where feasible;
- measure overhead, conflict handling and robustness.

**Exit:** a demonstrated coordination contract with known limits.

### Gate F5 — Environment and adaptation
- add a controlled digital or simulated environment;
- distinguish observation, state update, policy change, representation change and executable-structure change;
- evaluate persistence and transfer under regime shifts.

**Exit:** task-bounded evidence for specific environment interaction and adaptation claims.

### Gate F6 — Architecture revision
- reconcile all confirmed findings and contradictions;
- revise the architecture and interfaces;
- keep consciousness, general intelligence and universal claims outside the evidence boundary unless separately operationalized and tested.

**Exit:** a new versioned architecture with a claim-to-evidence map.

## 11. Explicit non-goals for v0.1

This foundation does not:
- define a universal cognitive ontology;
- mandate a fixed number or type of intelligence modules;
- require every module to be independently intelligent;
- require one central coordinator;
- equate attention, memory, learning, agency or intelligence;
- assume physical embodiment;
- claim consciousness or subjective experience;
- turn model confidence into action authorization;
- promote Machine research branches into production dependencies;
- specify one model, language, runtime, database or deployment topology;
- claim that MIRA is implemented or validated.

## 12. Source documents and provenance

### Primary project sources

- [Machine — machine-native research branch](https://github.com/Loofy147/Machine/tree/research/machine-native-primitives-v0) — observed head at foundation drafting: `f752aac015d9f837bc6a89d44eed50e0325b60a6`.
- [Machine — substrate primitive closure branch](https://github.com/Loofy147/Machine/tree/research/machine-substrate-primitive-closure-v0) — observed head: `5db33b068c0973606e08b596a300e99952764aeb`.
- [Machine — orchestration benchmark branch](https://github.com/Loofy147/Machine/tree/research/orchestration-benchmark-2026-09-27) — observed head: `cdcda922223212ee60edde7b9ab059658c0ab105`.
- [Machine — corrected memory research record](https://github.com/Loofy147/Machine/blob/f96cff40f922797a8055d1d437837c9e3805cbad/docs/MEMORY-UNDER-UNCERTAINTY-RESEARCH-v0.1.md).
- [Machine — research-state canonicalization](https://github.com/Loofy147/Machine/blob/research/evidence-disposition-v0/docs/RESEARCH-STATE-CANONICALIZATION-v0.1.md).
- [Open-System-One — canonical architecture convergence](https://github.com/Loofy147/Open-System-One/blob/main/docs/CANONICAL_ARCHITECTURE_CONVERGENCE_v0.1.md).
- [Open-System-One — system-wide architecture review](https://github.com/Loofy147/Open-System-One/blob/main/docs/SYSTEM_WIDE_ARCHITECTURE_REVIEW_v0.2_2026-10-02.md).
- [Open-System-One — architecture convergence gap register](https://github.com/Loofy147/Open-System-One/blob/main/docs/ARCHITECTURE_CONVERGENCE_GAP_REGISTER_v0.1.md).

### External research relevant to the foundation

- Gu and Dao, Mamba: Linear-Time Sequence Modeling with Selective State Spaces — https://arxiv.org/abs/2312.00752
- Zhang et al., H₂O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models — https://proceedings.neurips.cc/paper_files/paper/2023/file/6ceefa7b15572587b78ecfcebb2827f8-Paper-Conference.pdf
- Xiao et al., Efficient Streaming Language Models with Attention Sinks — https://proceedings.iclr.cc/paper_files/paper/2024/hash/5e5fd18f863cbe6d8ae392a93fd271c9-Abstract-Conference.html
- Liu et al., Lost in the Middle: How Language Models Use Long Contexts — https://aclanthology.org/2024.tacl-1.9/
- Hsieh et al., RULER — https://arxiv.org/abs/2404.06654
- Zhan et al., Overcoming Long-Context Limitations of State Space Models via Context-Dependent Sparse Attention — https://proceedings.neurips.cc/paper_files/paper/2025/hash/3e4ea825a66bf1e1e33eca3e81fe7886-Abstract-Conference.html
- Hu et al., Memory in the Age of AI Agents — https://arxiv.org/abs/2512.13564
- Hu et al., Preserving Memory Function in Hybrid Language Models — https://aclanthology.org/2026.findings-emnlp.1194/
- Afendulev et al., What Attention Recalls and Recurrence Controls in Hybrid Language Models — https://aclanthology.org/2026.findings-emnlp.2061/

## 13. Revision policy

This document is a foundation, not a frozen specification.

Any revision that changes an ownership boundary, semantic contract or claim status must:
1. identify the source branch/ref and exact evidence;
2. state the change and its scope;
3. preserve the prior claim and its disposition;
4. identify affected contracts and consumers;
5. define a falsification or conformance test;
6. update the assumptions and gap registers.

No statement becomes established through repetition or architectural preference alone.
