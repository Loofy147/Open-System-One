# Transition Burden Elimination Protocol v0.4

Status: METHODOLOGY — OPEN / EXPERIMENTAL
Date: 2026-10-02
Parent: Behavioral Transition Protocol v0.3

## 0. Purpose

v0.4 adds a compulsory burden-elimination layer over all current work.

A **burden** is any recurring or unresolved cost imposed on the system, operator, research process, implementation, maintenance, attention, uncertainty, or future decisions.

Examples:

- repeated manual work;
- duplicated investigations;
- stale or conflicting records;
- unresolved verification debt;
- ambiguous ownership;
- fragile integration;
- repeated context reconstruction;
- unnecessary architecture;
- unsupported claims that require later cleanup;
- open experiments with no discriminating action;
- maintenance caused by a mechanism that no longer justifies itself.

The objective is not to maximize automation.

The objective is:

\[
\boxed{
	ext{eliminate unjustified burden, absorb justified burden into the smallest stable mechanism, and expose every remaining burden explicitly.}
}
\]

## 1. Hard rule: no unclassified burden

After each burden sweep:

\[
\boxed{
\forall b:\
b \in \{KILL, MERGE, ABSORB, AUTOMATE, BOUND, PROVE, DEFER, REBASE\}
}
\]

There is no terminal or durable state named merely:

OPEN.

An unresolved item must have a concrete disposition and a wake condition or next discriminating action.

## 2. Burden model

Represent each burden as:

\[
B=(W,C,S,\Delta S^*,K,O,E,D,R,L)
\]

where:

- \(W\): world/revision;
- \(C\): context;
- \(S\): current burden-bearing state;
- \(\Delta S^*\): target burden-reducing state transition;
- \(K\): invariants;
- \(O\): oracle;
- \(E\): evidence;
- \(D\): disposition;
- \(R\): resolution condition;
- \(L\): lineage.

## 3. Burden classes

Use one primary class:

- REDUNDANCY — duplicate work or overlapping artifacts;
- MANUAL_REPETITION — repeated human execution;
- EPISTEMIC_DEBT — unresolved claim, uncertainty, contradiction, or missing evidence;
- VERIFICATION_DEBT — behavior claimed but not independently verified;
- INTEGRATION_FRICTION — boundary causing recurring coordination or translation work;
- MAINTENANCE_DEBT — recurring cost of keeping a mechanism alive;
- CONTEXT_DEBT — repeated reconstruction of prior state/history;
- ARCHITECTURE_DEBT — complexity without demonstrated boundary value;
- ADOPTION_DEBT — setup/migration/permission/training cost;
- SAFETY_BOUNDARY — required control that must remain;
- OBSERVABILITY_DEBT — inability to reconstruct important state/effect;
- COMPUTATION_DEBT — avoidable resource/time cost;
- COVERAGE_DEBT — an important area has not been inspected sufficiently.

## 4. Mandatory burden sweep

A complete sweep traverses, at minimum:

1. active repository work;
2. open experiments and validation tasks;
3. current decisions and unknowns;
4. technical debt and limitations;
5. opportunity candidates;
6. duplicated or stale research;
7. conversation-only research that has not been promoted or killed;
8. dependencies and external blockers;
9. current project artifacts and branches;
10. audit coverage gaps.

The sweep is complete only when every discovered burden has a record.

## 5. Forced filtering order

Every burden is processed in this order:

### F0 — Existence

Is the burden directly observed, explicitly reported, or mechanically derivable?

If not, mark UNKNOWN and create the cheapest evidence action.

### F1 — Necessity

If the burden disappeared, would an invariant, requirement, or required capability be violated?

If no:

\[
D=KILL
\]

### F2 — Duplication

Is an equivalent burden already tracked elsewhere?

If yes:

\[
D=MERGE
\]

and retain both source references.

### F3 — Existing mechanism

Can an existing mechanism already remove the burden?

If yes:

\[
D=ABSORB
\]

No new mechanism is justified.

### F4 — Automation opportunity

Does a specific recurring transition exist that can be made automatic with measurable benefit?

If yes, define:

\[
S_0\rightarrow S_1
\]

and test it before building.

### F5 — Required control

If the burden is a necessary safety, authority, durability, or observability boundary, do not eliminate it blindly.

Use:

\[
D=BOUND
\]

and minimize its operational cost without weakening its invariant.

### F6 — Decisive experiment

If the burden is a genuine unresolved research question:

\[
D=PROVE
\]

with one discriminating experiment, frozen oracle, expected observation, failure condition, and terminal outcome.

### F7 — External dependency

If no action is possible until an external condition changes:

\[
D=DEFER
\]

but only with:

- explicit blocker;
- wake condition;
- review date/event;
- no hidden work while deferred.

### F8 — Historical/stale

If the burden exists only because an obsolete representation or decision is still active:

\[
D=REBASE
\]

The historical record remains preserved.

## 6. Consequence gate

Do not prioritize a burden merely because it is annoying.

Record:

- consequence if unresolved;
- consequence if eliminated incorrectly;
- frequency;
- stakes;
- recoverability;
- reversibility.

Low-consequence discomfort is not sufficient justification for new architecture.

## 7. Burden-reducing transition

Every non-killed burden must define an explicit target transition.

Example:

Current:

\[
S_0 = \text{manual reconstruction of prior execution state}
\]

Target:

\[
S_1 = \text{state reconstructed from durable evidence}
\]

Mechanism candidates then become:

- existing log;
- receipt;
- database;
- script;
- capability;
- new tool.

The tool is not the target.

## 8. Counterfactual baseline

Compare:

\[
A=\text{current state}
\]

\[
B=\text{best existing/no-build workaround}
\]

\[
C=\text{proposed intervention}
\]

The intervention survives only if:

\[
C\neq B
\]

in a consequential, observable dimension.

## 9. Forced kill tests

Every burden that might justify code must have:

- kill hypothesis;
- cheapest incumbent/no-build test;
- independent oracle;
- failure condition;
- survival condition.

The default outcome is KILL.

Building is an exception that requires surviving evidence.

## 10. No-build and absorb-first rule

Before adding code, inspect:

- existing product features;
- current repository capability;
- scripts/CLI/library;
- CI/hook;
- OS primitive;
- existing database/query;
- existing receipt/evidence;
- human procedure;
- removing the underlying requirement.

The smallest mechanism wins only after the target transition is established.

## 11. Burden budget

Do not collapse burden into one arbitrary numeric score.

Instead maintain hard ceilings and explicit counts:

- unclassified burdens = 0;
- duplicate burdens without owner = 0;
- unresolved burdens without next action = 0;
- mechanism candidates without kill test = 0;
- decisions without evidence refs = 0 where evidence is required;
- stale decisions used as current authority = 0;
- unbounded deferred items = 0.

These are invariants, not a quality score.

## 12. Resolution states

Allowed states:

- KILLED;
- MERGED;
- ABSORBED;
- AUTOMATION_TESTED;
- BOUNDED;
- PROVING;
- DEFERRED;
- REBASED;
- RESOLVED;
- UNKNOWN_WITH_ACTION.

Every non-terminal state must have a next discriminating action or wake condition.

## 13. Re-representation contract

A burden may be regenerated from old records:

\[
R_{old}\xrightarrow{mapping\_version}R_{new}
\]

Re-generation must preserve:

- original burden;
- original source;
- original disposition;
- original kill scope;
- original evidence status.

It may add:

- a new transition interpretation;
- new contradiction;
- new coverage gap.

It must not silently convert an old KILLED item into an active candidate.

Reopening requires new evidence or changed scope.

## 14. Conversation-only work

Conversation-only work is valid input to the sweep but remains:

CONVERSATION_ONLY

until a repository or external evidence artifact exists.

A conversation does not establish:

- execution;
- benchmark;
- demand;
- implementation;
- external-world observation.

However, conversation-only work may create a burden record such as:

COVERAGE_DEBT
or
EPISTEMIC_DEBT

so it is not forgotten.

## 15. Current-system integration

The burden filter overlays the transition stack:

World
-> Observation
-> Target Transition
-> Burden Assessment
-> Mechanism Set
-> Authority
-> Impact
-> Durable Execution
-> Observation
-> Verification
-> Evidence
-> Decision

Examples:

### Opportunity research
Unresolved manual workflow
-> target transition
-> incumbent kill test
-> no-build / mechanism decision.

### Gap Engine
Unclear or manually repeated rate estimation
-> fitted transition model
-> target closure
-> mechanism plan
-> observed effect
-> calibration.

### Capability Kernel
Repeated authority ambiguity
-> explicit authorization state
-> execution boundary
-> receipt.

### Direct Impact Guard
Unbounded mutation risk
-> declared impact boundary
-> observed delta
-> rollback/commit.

### Durable Run
Retry ambiguity
-> stable transition identity
-> reconciliation.

### Research
Repeated uncertainty without discriminating experiment
-> explicit experiment
-> oracle
-> evidence
-> decision.

## 16. Forced global sweep result

A sweep is complete when:

\[
\boxed{
U=0
}
\]

where U is the number of unclassified, ownerless, actionless, or silently deferred burdens.

This does NOT mean:

\[
B=0
\]

Some burdens are required invariants.

The objective is:

\[
\boxed{
\text{Unjustified burden}=0
}
\]

and:

\[
\boxed{
\text{Every justified burden is explicit, bounded, and revalidated.}
}
\]

## 17. Method self-test

The method itself must be tested on a known corpus.

Minimum adversarial corpus:

- duplicate task;
- obsolete decision;
- real safety invariant;
- vague complaint;
- repeated manual step;
- already-solved burden;
- external blocker;
- conflicting sources;
- stale prior-art result;
- conversation-only claim;
- missing oracle;
- mechanism that executes but does not remove the burden.

Expected outcome must be frozen before running the filter.

## 18. Status

METHODOLOGY — OPEN / EXPERIMENTAL

The forced burden filter is not a claim that all burdens can be eliminated. It is a contract that no burden may remain invisible or unjustified merely because it is embedded in the way work is currently done.
