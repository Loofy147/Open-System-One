# Problem Kill Campaign v0.1

Status: RESEARCH_ONLY — NO_MVP_AUTHORIZED
Date: 2026-10-01

Rule:
problem candidate -> evidence -> existing solutions -> kill -> status

KILLED_AT_DESK means current solutions materially cover the stated problem, or evidence is too weak.
SURVIVED_DESK_KILL means a plausible gap remains after current-source review. It is not MVP approval.

## Developer tooling

A. Required review without notification blast
Evidence: GitHub community discussions still report the exact requirement in 2026; users want required team approval without prematurely subscribing/notifying the whole team.
Existing solutions: GitHub team notification controls, CODEOWNERS, required-review rulesets; Mergify can request reviews conditionally and enforce review-related merge conditions.
Kill: test whether GitHub + Mergify can implement peer review -> delayed senior-team request -> enforceable approval without changing the trust model.
Status: SURVIVED_DESK_KILL.

B. Reproducible environment bootstrap
Existing solutions: GitHub devcontainers/Codespaces, npm package-lock, uv locking.
Kill: a standalone tool would duplicate mature environment reproducibility mechanisms.
Status: KILLED_AT_DESK.

C. Duplicate issue triage
Existing solution: GitHub duplicate-issue detection and native duplicate handling.
Status: KILLED_AT_DESK.

## Small business operations

A. Receipt capture
Evidence: current SME research reports meaningful finance-admin burden.
Existing solutions: QuickBooks, Expensify, Dext, Zoho Expense and similar products already capture receipts, extract data and match transactions.
Status: KILLED_AT_DESK.

B. Connectorless export-based exception reconciliation
Problem: a small business exports CSV/XLSX/PDF from several systems and needs only the mismatches, without API integration setup.
Evidence: Sage reported 52 digital tools, 27 logins and 19 working days/year lost to moving/re-entering information; an Irish SME survey reported five financial tools on average, 65% combining sources for a full picture and 43% re-entering the same information.
Existing solutions: Zapier, n8n and accounting integrations cover many API-based workflows.
Gap hypothesis: local, export-only, exception-first reconciliation may remain underserved.
Status: SURVIVED_DESK_KILL.
Next kill: compare against spreadsheet imports, accounting reconciliation, Zapier/n8n and low-cost products using the same export-only fixtures.

C. Client onboarding / missing-information chase
Existing solutions: HubSpot, Jotform-style portals and CRM workflows already support forms, uploads, reminders and follow-up.
Status: KILLED_AT_DESK.

## Files and documents

A. Duplicate-file cleanup
Existing solutions: Czkawka and dupeGuru already provide cross-platform duplicate detection, protected reference folders, dry runs and safe deletion workflows.
Status: KILLED_AT_DESK.

B. Generic version confusion
Existing solutions: SharePoint/OneDrive and Google Drive provide version/activity history; duplicate finders and sync systems address many conflict cases.
Status: KILLED_AT_DESK.

## Data handling

A. Generic schema validation
Existing solutions: Soda data contracts, Pandera, Frictionless and Data Contract CLI cover schema, type and constraint validation.
Status: KILLED_AT_DESK.

B. Non-engineer file-handoff change explainer
Problem: a person receiving recurring CSV/XLSX exports wants a deterministic pre-import report of structural changes and likely breakage.
Evidence: Frictionless has active 2026 requests around provider schema transitions and optional/default columns, plus current CSV edge cases.
Existing solutions: developer-oriented validators exist, but they generally require schemas/code/configuration.
Gap hypothesis: a zero-setup local report may serve a different operator workflow.
Status: SURVIVED_DESK_KILL.
Next kill: test whether Excel/Sheets import previews or existing validator tooling can produce the same reliable decision with comparable effort.

## Local / offline workflows

A. Generic offline collection
Existing solutions: ODK Collect/Central already supports offline collection and later synchronization.
Status: KILLED_AT_DESK.

B. Explain and reconcile offline conflicts
Evidence: ODK documents offline Entity conflicts and notes that resulting differences can be shown without always knowing the exact actions that caused them.
Existing solutions: conflict labels/history and configurable offline database conflict handlers.
Gap hypothesis: a narrow causal-diff artifact for human review may still be useful.
Status: SURVIVED_DESK_KILL.
Next kill: real offline conflict fixtures against ODK/RxDB/PouchDB-style workflows.

## Consumer utilities

A. Warranty/receipt organizer
Existing solutions: current App Store products already combine receipt capture, warranty dates and expiry reminders.
Status: KILLED_AT_DESK.

B. Recurring reminder utility
Existing solutions: Google Tasks and Google Calendar support repeating tasks/events.
Status: KILLED_AT_DESK.

## Previously examined agent / OSS landscape

Sandbox / execution isolation:
OpenShell and OpenSandbox directly cover sandbox runtime and lifecycle.
Status: KILLED_AT_DESK as a generic standalone product problem.

Policy / authorization:
OPA, OpenFGA, Cedar and SPIFFE/SPIRE cover policy decisions, relation authorization, policy language and workload identity/attestation.
Status: KILLED_AT_DESK as a generic missing primitive.

Browser automation:
Playwright MCP already provides a browser automation surface.
Status: KILLED_AT_DESK.

Agent security / evaluation:
AgentDojo already provides dynamic prompt-injection attack/defense evaluation; other benchmark systems cover evaluation.
Status: KILLED_AT_DESK.

Independent effect verification:
Problem: external agents can have policy, sandbox, browser, identity and traces, while a durable control plane still needs an independent statement of what authoritative state actually changed.
Desk finding: I did not find a common cross-surface contract combining observed post-state delta, bounded impact, rollback/compensation and authority revalidation.
Status: SURVIVED_DESK_KILL.
Existing research artifact: research/direct-impact-guard-v0.1.
Constraint: this is not product validation; the current artifact still needs real external backends and fresh CI evidence.

## Current survivor set

1. Developer review routing without premature notification.
2. Small-business export-only exception reconciliation.
3. Human-readable file-handoff change explainer.
4. Offline conflict causal diff/reconciliation.
5. Independent agent-effect verification.

## MVP gate

No MVP is authorized until a survivor passes:
- multiple independent pain signals or direct operational evidence;
- a measurable failure definition;
- hands-on kill against the strongest existing alternatives;
- a precise residual gap;
- a narrow user/workflow boundary;
- a reversible prototype experiment with explicit pass/fail thresholds;
- independent verification of the claimed result.

No candidate is currently MVP-authorized.
