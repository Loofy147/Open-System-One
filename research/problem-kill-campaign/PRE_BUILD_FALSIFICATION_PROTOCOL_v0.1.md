# Pre-Build Falsification Protocol v0.1

Status: MANDATORY_GATE / NO_MVP

## Objective

Before writing an MVP, attempt to make the candidate unnecessary using the cheapest credible experiment.

Cost order:
1. configuration-only or documentation proof;
2. existing-product hands-on fixture;
3. small adapter/fixture;
4. only then experimental implementation.

Never move upward in cost while a lower-cost falsification remains unanswered.

## Experiment design

Each falsification test needs:
- candidate problem statement;
- strongest incumbent solution;
- minimal fixture that exposes the alleged gap;
- observable success criterion for the incumbent;
- kill threshold;
- survival threshold;
- exact failure evidence;
- environment/revision/run identity.

Ambiguous results remain OPEN. Repetition is not independent evidence.

## F1 — offline conflict causal reconciliation

Incumbent: ODK Central entity conflict UI/API.
Fixture: five deterministic cases: same-property parallel update, independent-property parallel update, chained offline branch, out-of-order create/update, three-way concurrent branch.

Questions the incumbent must answer without external reconstruction:
1. Which branches/events caused the conflict?
2. Which exact properties conflict?
3. Which current version is authoritative and why?
4. Which resolution action is appropriate?
5. Which version/actor/source metadata supports the decision?

Kill threshold: 4/5 cases fully correct by an operator using only ODK evidence.
Survival threshold: at least 2/5 cases require manual reconstruction, and the missing causal evidence is structural.
Stop condition: if the problem is merely presentation preference, kill.

## F2 — independent agent-effect verification

Incumbent: strongest available agent provenance/rollback system, currently MAP for open-source comparison.
Fixture: harmless state-changing action; undeclared side effect; partial failure; authority revoke followed by retry.

Questions the incumbent must independently reconstruct:
1. actor/agent identity;
2. authority and approval at execution;
3. authoritative pre-state;
4. authoritative post-state;
5. exact delta and blast radius;
6. rollback/compensation result;
7. replay/revocation behavior;
8. externally verifiable receipt.

Kill threshold: incumbent satisfies all 8 without relying on agent narrative and without importing our authority semantics.
Survival threshold: at least one required fact is unavailable, only inferred, or cannot be independently verified across the execution boundary.
MAP must be treated as a serious prior-art kill candidate: its current repo describes before/after state snapshots, hash-chained provenance, rollback, persistent SQLite/Postgres stores and cross-language verification.

## No-build rule

During F1/F2 do not create:
- product UI;
- public API;
- marketing or pricing;
- user onboarding;
- generalized platform infrastructure.

Allowed work is limited to fixtures, adapters required to exercise an incumbent, measurement, evidence capture and analysis.

## Promotion

Only one candidate may enter EXPERIMENTAL_WINNER unless all candidates are killed.
An all-killed result is a valid research result: no MVP.
An experimentally built winner remains a research instrument until its evidence answers the accumulated questions and independent verification passes.