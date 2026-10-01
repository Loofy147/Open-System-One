# Behavioral Transition Protocol v0.3

Status: METHODOLOGY — OPEN / EXPERIMENTAL
Date: 2026-10-02
Supersedes as active opportunity methodology: Experimental Opportunity Protocol v0.2
Historical v0.2 records remain immutable; v0.3 is a new representation/projection layer.

## 0. Purpose

The unit searched for is no longer a Problem Candidate or a Tool Candidate.

The primary unit is an observed or hypothesized **Target Transition**:

\[
S_0 \xrightarrow{\text{transition}} S_1
\]

The method asks:

1. What state/context exists now?
2. What target state transition would matter operationally?
3. Is that transition actually consequential?
4. What happens today?
5. Why does the target transition not already occur reliably?
6. Which existing mechanisms can realize it?
7. Does a minimal intervention create a measurable counterfactual delta?
8. Did the intended transition actually occur?
9. Can the result be independently verified and preserved?

The method does not assume that the mechanism is a new program.
A script, hook, CI rule, library, OS facility, existing product feature, manual procedure, or no-build result are all valid mechanisms.

The preferred outcome remains:

\[
\text{NO\_BUILD}
\]

when the target transition is already adequately realized or does not justify intervention.

---

## 1. Core ontology

### 1.1 World

\[
W=(world\_revision, environment, observed\_at)
\]

The world reference prevents a historical transition description from being silently reused as current authority.

### 1.2 Observed State

\[
S_0
\]

The state that exists before the candidate transition.

### 1.3 Context

\[
C
\]

Preconditions, actor/context, object scope, and other applicability conditions.

### 1.4 Trigger

\[
\tau
\]

The event or condition at which the transition becomes applicable.

### 1.5 Target Transition

\[
T=(W,C,\tau,\Delta S^*,K,O,H)
\]

where:

- \(W\): world/revision reference;
- \(C\): context/preconditions;
- \(\tau\): trigger;
- \(\Delta S^*\): desired state delta;
- \(K\): invariants/constraints;
- \(O\): independent oracle;
- \(H\): human/machine boundary.

The target transition is the primary research object.

### 1.6 Mechanism

A mechanism is a candidate realization of \(T\):

\[
M_j: S_0\rightarrow \widehat{S}_1
\]

Examples:

- existing product;
- embedded feature;
- command/script;
- library;
- CI/hook;
- OS integration;
- workflow/procedure;
- new small tool.

### 1.7 Actual Transition

\[
\Delta S_{obs}=S_1-S_0
\]

The observed change, computed independently where possible.

### 1.8 Verification

\[
V=O(S_0,S_1,context)
\]

Verification establishes whether the target transition occurred, not merely whether a mechanism executed.

### 1.9 Evidence

Evidence supports a claim about the transition, mechanism, execution, or outcome. Execution telemetry alone is not automatically evidence of successful outcome.

### 1.10 Decision

A decision is a versioned consequence of verified evidence. It does not rewrite prior decisions.

---

## 2. Problem is a projection, not the primary object

A human-readable problem statement remains valid, but it is derived from a state/transition relation:

\[
Problem \approx description(S_0,\Delta S^*)
\]

Therefore:

\[
Transition > Problem\ description > Mechanism > Artifact
\]

The protocol must not silently convert:

- a complaint into a target transition;
- a target transition into demand;
- an executable mechanism into an opportunity;
- a successful run into a verified outcome.

Each conversion requires its own evidence.

---

## 3. Automaticity is a mechanism property, not an assumption

The target transition may eventually be realized:

\[
\text{manual}
\rightarrow
\text{assisted}
\rightarrow
\text{approval-gated}
\rightarrow
\text{automatic}
\]

Therefore the protocol does not require zero human involvement.

Record explicitly:

- machine responsibility;
- human responsibility;
- approval boundary;
- failure/recovery boundary.

The desired property is **reliable realization of the target transition**, not automation for its own sake.

---

## 4. Transition record

Every transition candidate must record:

\`
transition_id
representation_version
world_reference
observed_context
pre_state
trigger
target_state
desired_delta
constraints
human_machine_boundary
oracle
consequence
current_transition
automation_gap
mechanism_candidates
counterfactual_baseline
adoption_cost
status
decision
evidence_refs
contradiction_refs
experiment_refs
artifact_refs
source_record_refs
lineage_refs
next_discriminating_action
\`

### Required epistemic labels

Every material field must be classifiable as one of:

- DIRECT_OBSERVATION
- USER_REPORTED
- EXPERIMENTALLY_SUPPORTED
- ESTABLISHED
- DERIVED
- INFERRED
- HYPOTHESIS
- CONTRADICTED
- UNKNOWN
- OPEN

**Re-representation never upgrades epistemic status.**

---

## 5. Target Transition admissibility

A target transition may enter the research frontier only when it has:

1. a bounded pre-state;
2. a bounded target delta;
3. an identifiable context/trigger or explicit absence thereof;
4. a consequence that can be observed or measured;
5. an independent oracle or a declared UNKNOWN oracle state.

The protocol must reject vague targets such as:

> make workflow better

Prefer:

\[
S_0\rightarrow S_1
\]

with explicit observables.

---

## 6. Consequence gate

A transition is not automatically valuable because it is measurable.

Record:

- consequence if the transition is absent;
- consequence if it is wrong;
- frequency;
- stakes;
- recoverability;
- reversibility.

Cosmetic or low-consequence deltas do not become opportunities merely because they are easy to automate.

---

## 7. Current-transition measurement

Describe the transition that occurs without a new intervention:

\[
T_{current}
\]

Record where possible:

- elapsed time;
- manual steps;
- error exposure;
- hidden failure;
- coordination cost;
- irreversible effects;
- operator burden.

If the current workflow already realizes the target transition adequately, kill the candidate.

---

## 8. Automation/realization gap

The gap must be falsifiable:

> Under context C and trigger \(\tau\), the current mechanism set realizes X. It does not reliably realize target delta Y under condition Z. The missing part is operationally consequential. A minimal intervention could change the realized transition.

The gap must identify the missing transition, not merely an uncomfortable interface.

---

## 9. Strongest incumbent set

For every candidate, evaluate the union of:

1. direct product/tool;
2. adjacent product/tool;
3. embedded feature;
4. script / shell / CLI / library;
5. documented procedure;
6. manual workflow;
7. no-build workaround.

The kill baseline is the strongest practical realization of the target transition.

---

## 10. Counterfactual action delta

Use the same:

- case;
- actor/user role;
- starting state;
- constraints.

Compare:

\[
A=\text{current workflow}
\]

\[
B=\text{strongest no-build workaround}
\]

\[
C=\text{proposed intervention}
\]

The intervention survives this gate only when:

\[
C \neq B
\]

in an operationally meaningful, observable way.

A prettier report, shorter explanation, or different UI is insufficient unless it changes a consequential transition.

---

## 11. Mechanism search

Only after the target transition is explicit may mechanism search begin.

For each mechanism record:

- mechanism_id;
- type;
- scope;
- expected delta;
- dependencies;
- setup;
- permissions;
- migration;
- maintenance;
- failure modes;
- reversibility;
- prior-art freshness.

A new tool is merely one row in this set.

---

## 12. Pre-build kill test

The kill test must be written against the target transition:

- kill hypothesis;
- fixed test corpus or operational cases;
- incumbent-only procedure where possible;
- pre-registered oracle;
- failure condition;
- survival condition.

Example:

\[
\text{Kill if incumbent realizes }\Delta S^*
\]

in the required proportion without material additional burden.

Do not build before this gate permits it.

---

## 13. Minimal intervention

If the candidate survives:

\[
M^*=\arg\min_M complexity(M)
\]

subject to:

\[
Verified(M) = TargetTransition
\]

The MVP/minimal intervention contains only what is required to test the transition hypothesis.

Dashboard/auth/cloud/AI/plugins are not justified by default.

---

## 14. Execution is not transition

A run can succeed while the target transition does not occur.

Therefore retain separate records:

\[
ExecutionResult \neq TransitionResult
\]

For every intervention, capture where possible:

- run identity;
- pre-state digest;
- post-state digest;
- actual delta;
- effect status;
- authorization;
- impact bounds;
- receipt.

---

## 15. Authority, impact, durability

The transition model integrates three orthogonal controls:

\[
Authority(T)
\]

May this transition occur?

\[
Impact(T)
\]

What magnitude/scope of state change may occur?

\[
Durability(T)
\]

Can the identity/effect of the transition be reconstructed across retry, restart, or process failure?

These dimensions must not be collapsed into one success bit.

---

## 16. UNKNOWN effect

If the system cannot establish whether the target transition occurred:

\[
UNKNOWN =
\text{transition occurrence unresolved}
\]

UNKNOWN is not equivalent to execution failure and must not be silently retried when a duplicate external effect is unsafe.

Resolution must converge, where possible, to:

\[
UNKNOWN\rightarrow
\{COMPLETED,CONFIRMED\_NOT\_EXECUTED\}
\]

or remain explicitly unresolved.

---

## 17. Verification and oracle integrity

The oracle must be independent from the candidate mechanism whenever feasible.

Minimum matrix:

| Class | Purpose |
|---|---|
| Normal | target transition |
| Boundary | transition limits |
| False Positive | reject non-transition |
| False Negative | catch missed transition |
| Malformed | invalid input |
| Hostile | adversarial input |
| Unsupported | declared limits |
| Oracle Check | verify expected truth independently |

An oracle that derives expected truth from the candidate's own output is not independent evidence.

---

## 18. Re-representation and regeneration contract

v0.3 does not rewrite v0.2 records.

It creates a deterministic representation:

\[
R_{v0.2}
\xrightarrow{Mapping\ Version\ m}
R_{v0.3}
\]

with:

- source snapshot identifier;
- source record identifier;
- mapping version;
- mapping digest;
- representation timestamp;
- field-level provenance;
- excluded fields with reasons;
- target transition identifier;
- representation digest.

### Field derivation classes

Every regenerated field is one of:

- COPIED — directly carried from a source record;
- DERIVED — mechanically derived from source fields;
- INFERRED — interpretive reconstruction;
- MISSING — not supported by source evidence;
- CONFLICTED — multiple source records disagree.

A regenerated **INFERRED** transition must never be presented as an observed transition.

### Determinism rule

Given the same:

\[
(source\_snapshot, mapping\_version)
\]

the representation generator must produce the same canonical representation and digest.

Changes in source data require a new source snapshot and a new representation event.

---

## 19. Splitting and merging during re-representation

### One legacy record → multiple transitions

Allowed.

Create separate transition IDs and link each with:

\[
DERIVED\_FROM
\]

Do not silently merge them.

### Multiple legacy records → one apparent transition

Allowed as a **relationship**, not an automatic merge.

Use:

\[
SAME\_TARGET
\]

or another explicit relationship and preserve all source records.

### Contradictory source records

Do not resolve by recency alone.

Create a contradiction record with:

- source snapshots;
- scope;
- conflict;
- resolution state.

---

## 20. Re-representation is not re-verification

Changing representation does not constitute a new experiment.

Therefore:

\[
Reencoding \neq Verification
\]

and:

\[
Reencoding \neq New\ Evidence
\]

A regenerated representation can expose a missing field or a contradiction. It may then trigger a new experiment, but that experiment is separately recorded.

---

## 21. Transition lineage

Every transition must be traceable:

\[
SourceRecord
\rightarrow
RepresentationEvent
\rightarrow
TransitionTarget
\rightarrow
MechanismCandidate
\rightarrow
Execution
\rightarrow
Observation
\rightarrow
Verification
\rightarrow
Evidence
\rightarrow
Decision
\rightarrow
DecisionRevision
\]

No node may gain authority merely because it is reachable in this graph.

Reachability is not authority.

---

## 22. Portfolio and internal research integration

This model applies across the current research portfolio without forcing every project into a product-opportunity classification.

Examples:

### Opportunity research

\[
ObservedWorkflow
\rightarrow
TargetTransition
\rightarrow
Gap
\rightarrow
Mechanism
\rightarrow
Kill/Build
\]

### Capability Kernel

\[
RequestedTransition
\rightarrow
AuthorityCheck
\rightarrow
Approval
\rightarrow
Execution
\rightarrow
ObservedEffect
\rightarrow
Receipt
\]

### Direct Impact Guard

\[
Mutation
\rightarrow
BoundedDelta
\rightarrow
Postcondition
\rightarrow
Rollback/Commit
\]

### Durable Run

\[
Attempt
\rightarrow
StableTransitionIdentity
\rightarrow
Retry/Reconciliation
\]

### Android UNKNOWN-effect research

\[
ExternalEffect?
\rightarrow
UNKNOWN
\rightarrow
Reconciliation
\rightarrow
VerifiedEffectStatus
\]

### Experimental/scientific research

\[
ResearchState
\rightarrow
CandidateTransition
\rightarrow
Experiment
\rightarrow
Observation
\rightarrow
Verification
\rightarrow
Claim
\]

The same transition language is used, but a scientific research transition is not automatically a product opportunity.

---

## 23. Opportunity taxonomy

Each transition/mechanism combination must be classified as exactly one primary type:

- INTERNAL_PRIMITIVE
- RESEARCH_INSTRUMENT
- RESEARCH_CANDIDATE
- SMALL_TOOL_OPPORTUNITY
- PRODUCT_OPPORTUNITY
- NO_BUILD_RESULT

The classification must not be inferred from artifact size or implementation effort.

---

## 24. Decision gates

A research candidate may progress only when all applicable gates are satisfied:

\[
Reality
\rightarrow
Consequence
\rightarrow
Incumbent
\rightarrow
Counterfactual
\rightarrow
Mechanism
\rightarrow
Adoption
\rightarrow
KillTest
\rightarrow
MinimalIntervention
\rightarrow
Verification
\]

A failed gate can produce a complete result.

---

## 25. Method evaluation

The method itself remains experimental.

Measure not only candidate outcomes but representation quality:

- source coverage rate;
- unmapped-record rate;
- inferred-field rate;
- contradiction detection rate;
- representation regeneration determinism;
- provenance completeness;
- status-preservation violations;
- incumbent-miss rate;
- premature-build rate;
- false-survival rate;
- oracle-failure rate;
- post-build-kill rate;
- action/transition-delta rate.

The goal is not to maximize any single score. The goal is to detect systematic methodological failure.

---

## 26. Current rule

Do not begin a cycle with:

> What tool should we build?

Do not even begin with:

> What problem should we solve?

Begin with:

> **What consequential state transition is observed, missing, manual, fragile, or unreliable enough to justify investigation?**

Then test whether that transition is already realized by the strongest existing mechanism set.

---

## 27. Current epistemic rule

A regenerated representation must preserve the old state:

\[
Status_{new} \le Evidence_{available}
\]

No epistemic promotion can occur from:

- better wording;
- cleaner schema;
- repeated discussion;
- representation migration;
- model preference.

Only new evidence/verification may promote a claim.

---

## 28. Status

v0.3 is:

\[
\boxed{METHODOLOGY — OPEN / EXPERIMENTAL}
\]

It is itself subject to falsification.

The first required experiment is **representation replay** over the v0.2 opportunity state and audit.

Success criterion:

1. every prior candidate is accounted for;
2. no prior status is upgraded;
3. every newly stated transition is labeled by provenance class;
4. killed candidates retain their kill scope/reason;
5. the representation is deterministic;
6. the mapping exposes at least one materially useful distinction that v0.2 could not express cleanly.

Failure of these criteria is evidence against adopting v0.3 as the active representation.
