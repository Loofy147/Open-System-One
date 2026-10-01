# Problem Kill Campaign v0.1

Status: RESEARCH_ONLY — NO_MVP_AUTHORIZED
Governed by: docs/research/EXPERIMENTAL_OPPORTUNITY_PROTOCOL_v0.2.md
Date: 2026-10-01

## Core rule

problem candidate -> evidence -> existing solutions -> kill -> status

A candidate is never promoted because the problem sounds painful or because implementation looks easy.

SURVIVED_DESK_KILL means only that a plausible residual gap remains. It is not build authorization.

## Desk-kill results

### Killed

Developer tooling — reproducible environment bootstrap: devcontainers/Codespaces, package locks and uv locking already cover the generic problem.
Developer tooling — duplicate issue triage: GitHub now has duplicate-issue detection and native duplicate handling.
Developer tooling — required review without notification blast: GitHub supports team-notification controls, while Mergify supports conditional request_reviews and required-review enforcement. The remaining workflow can be composed without a new product primitive, so the generic problem is killed at desk stage.
Small business — receipt capture: QuickBooks and comparable accounting/expense products already cover capture, extraction and reconciliation.
Small business — generic connectorless reconciliation: the exact file-first problem is now directly covered by current products such as Reconcile, including CSV/Excel/JSON, multi-file reconciliation, mapping and discrepancy reports without ERP/API onboarding.
Files/documents — duplicate cleanup: Czkawka and dupeGuru cover the generic problem.
Files/documents — generic version confusion: cloud document systems already provide version/activity history and conflict mechanisms.
Data handling — generic schema validation: Soda, Pandera, Frictionless and Data Contract tooling cover the general case.
Data handling — generic CSV/XLSX diff: current browser-local and CLI tools already compare rows, keys, headers and cell-level changes.
Local/offline — generic offline collection: ODK already covers offline collection and synchronization.
Consumer utilities — warranty/receipt organizer: current apps already combine receipts, warranties and expiry reminders.
Consumer utilities — recurring reminder: calendar/task products already support recurrence.
Previously examined agent/OSS landscape — generic sandbox, policy, identity, browser automation and agent evaluation: OpenShell/OpenSandbox, OPA/OpenFGA/Cedar/SPIRE, Playwright MCP and AgentDojo cover these as established primitives.

### Two finalists for pre-build falsification

1. Local/offline conflict causal reconciliation

Problem boundary: when multiple offline branches update the same record, the user needs to determine the causal branches, conflicting properties, authoritative state and correct resolution without reconstructing the history manually.

Why it survived desk kill: ODK exposes conflict state, baseVersion, branchId, conflictingProperties, creator/user-agent metadata and version history, but its documentation notes that complex offline conflicts can remain hard to understand. CouchDB preserves conflicting revisions but does not retain which peer a particular revision came from.

2. Independent agent-effect verification

Problem boundary: after an agent acts through any external runtime, an independent layer should be able to prove what authoritative state changed, under which authority/approval, within what declared impact envelope, and whether the result remained valid or was compensated.

Why it survived desk kill: audit/provenance, rollback and agent action logging are increasingly available. MAP explicitly provides full before/after state, tamper-evident ledgering, rollback strategies, persistent stores and verification. Therefore the residual gap is not 'audit logs are missing'; it is the stricter independence and cross-surface verification contract.

The current Direct Impact Guard is research evidence for the hypothesis, not proof of market need.

## Pre-build falsification rule

For each finalist, do not implement the proposed tool.

Instead ask:

What is the cheapest experiment that could prove this tool is unnecessary?

The experiment must use the strongest existing solution or the smallest possible configuration of it.

A finalist is killed when the existing system can satisfy the operational requirement with no material loss of correctness, evidence, control, or operator effort.

## Falsification experiment F1 — offline conflict

Fixture: 5 deterministic conflict cases: same-property parallel update; independent-property parallel update; chained offline branch; out-of-order create/update; three-way concurrent branch.

Procedure: use only the existing ODK conflict UI/API metadata and history.

For every case ask the operator to produce: causal branch explanation; exact conflicting properties; authoritative/current state; resolution action; source/version references supporting the decision.

Kill threshold: if an operator can produce all five answers correctly for at least 4 of 5 cases, without manually reconstructing state outside ODK, the separate tool is killed.

Survival threshold: if at least 2 cases cannot be explained correctly from existing evidence, and the missing evidence is a repeatable structural deficiency rather than UI preference, continue.

No code for the candidate is permitted during F1.

## Falsification experiment F2 — independent agent-effect verification

Fixture: one harmless state-changing action plus one undeclared side effect, one partial failure, and one authority revoke/replay case.

Strongest existing comparison: MAP or an equivalent agent audit/rollback system.

Procedure: for each run ask whether the existing system alone can independently reconstruct: actor/agent identity; authority and approval at execution; authoritative pre-state; authoritative post-state; exact delta and blast radius; rollback/compensation result; replay/revocation behavior; a receipt verifiable outside the acting agent.

Kill threshold: if the existing stack can satisfy all eight for the full fixture without trusting the acting agent's narrative and without adding our control-plane semantics, kill the candidate.

Survival threshold: if one or more required facts remain unavailable or are only inferred from agent-reported traces, continue.

No product UI or MVP is to be built for F2. Only an adapter fixture is permitted.

## Experimental-winner rule

Only after F1/F2 leave one surviving candidate may we build the experimental winner.

The winner build is not an MVP and not a launch candidate.

Its sole purpose is to answer the accumulated research questions from this work:

### Evidence / epistemics

Live World@revision R -> applicability -> versioned observation -> evidence -> verification event -> claim -> gate -> decision/revision.

Historical applicability must not be mistaken for current authority.

Every experiment must record source, exact revision/ref/commit, execution environment, run_id, input/state digest, result digest, observation event, independent verification, failures and negative results.

Conversation-only observations do not become repository evidence until reproduced and recorded.

### Control and authority

The experimental winner must use task/action identity, capability contract, policy/relationship authorization, request-scoped approval, authority revalidation before replay, explicit idempotency, bounded impact, post-state verification and receipt reconstruction.

The current native primitives are inputs, not assumptions: CapabilityKernel and Direct Impact Guard.

### Execution surface neutrality

External systems remain adapters:
external capability -> narrow adapter -> capability contract -> receipt -> independent verification -> promote/reject

GitHub, SQLite, browser, cloud agent, sandbox or any single vendor must not become architectural authority.

### Storage / durability

Where persistence is needed, use the intended split: BlobStore / TransactionalStore / QueryStore, with versioned contracts and schema identity.

Do not use an external product's memory or history as the authority source.

### Agent-surface characterization

The experimental winner must be compatible with A0-A10: identity, read-only observation, untrusted content, scope, evidence fidelity, reversible mutation, approval, stop, duplicate request, environment identity and receipt reconstruction.

### Research questions inherited from the previous work

- Can an external agent capability be adopted without surrendering authority?
- Can historical authorization remain historically true after current revocation?
- Can idempotency be safe under authority changes and state drift?
- Can impact be bounded independently of model intent?
- Can unauthorized or unexpected changes be detected after execution?
- Can rollback or compensation be proven rather than asserted?
- Can agent traces remain distinct from authoritative evidence?
- Can browser, sandbox, policy and identity surfaces be composed without vendor-specific leakage into the core?
- Can a run be reconstructed after interruption or partial failure?
- Can the same logical action be verified across different execution backends?
- Can the system distinguish current authority from historical applicability?
- Which parts of the proposed architecture are actually necessary after existing solutions are placed under adversarial comparison?

## Hard stop

No MVP authorization, pricing work, launch work, branding work or feature expansion follows from surviving desk research.

The only next state is:

PRE-BUILD FALSIFICATION -> one candidate survives -> EXPERIMENTAL WINNER -> evidence -> revalidation -> only then consider whether an MVP is warranted.

## v0.2 enforcement

This campaign is now subordinate to Experimental Opportunity Protocol v0.2. The current finalists must pass Action Delta and Pre-build Kill Test gates before any BUILD_ALLOWED state. A surviving candidate is not an MVP opportunity until the falsification experiment fails to kill the intervention.
