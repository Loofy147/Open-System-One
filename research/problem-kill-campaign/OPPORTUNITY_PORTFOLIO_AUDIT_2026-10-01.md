# Opportunity Portfolio Audit — 2026-10-01

Status: RESEARCH_ONLY / NO_MVP_AUTHORIZED

## Executive conclusion

The current opportunity set was re-audited across the original six domains, the previously inspected agent/OSS landscape, and the user's active research repositories.

Result:

- no confirmed product opportunity;
- several previous finalists are now killed by stronger current prior art;
- one previous survivor remains only as NEEDS_DECISIVE_EXPERIMENT;
- one narrower data-hand-off candidate is reopened as OPEN / NEEDS_DECISIVE_EXPERIMENT;
- internal research frontiers are explicitly separated from external product opportunities.

This is a valid outcome. No candidate is promoted merely to preserve momentum.

## 1. Opportunity taxonomy

Every item is classified as one of:

INTERNAL_PRIMITIVE
RESEARCH_INSTRUMENT
RESEARCH_CANDIDATE
SMALL_TOOL_OPPORTUNITY
PRODUCT_OPPORTUNITY

A project can contain a useful primitive without constituting a product opportunity.

## 2. Re-audit of previous candidate set

| Candidate | Current state | Reason |
|---|---|---|
| GitHub review routing without premature notification | KILLED_AT_DESK | GitHub + Mergify cover conditional review request / required-review workflow sufficiently for the generic problem. |
| SMB export-only reconciliation | KILLED_AT_DESK | Current file-first reconciliation products already ingest CSV/Excel/JSON and produce discrepancy outputs. |
| Generic CSV/XLSX diff | KILLED_AT_DESK | Current browser/CLI tools cover structure and row/cell comparison. |
| Generic pre-import CSV repair/validation | KILLED_AT_DESK | Current tools directly provide browser-local validation, repair, suspicious-value detection and import-risk reports. |
| Generic sandbox | KILLED_AT_DESK | OpenShell/OpenSandbox cover isolation/runtime lifecycle. |
| Generic policy/authorization | KILLED_AT_DESK | OPA/OpenFGA/Cedar/SPIRE cover the major primitives. |
| Generic browser automation | KILLED_AT_DESK | Playwright MCP already provides a mature browser capability surface. |
| Generic agent receipt/provenance | KILLED_AT_DESK | NOA Receipt, AERF, CAVA, AgentProvenance and related protocols substantially overlap signed receipts, canonical action identity, provenance and independent verification. |
| Generic MCP discovery/validation | KILLED_AT_DESK | Official MCP Registry + Inspector now cover discovery, schema validation and conformance-oriented tooling. |
| Generic offline collection | KILLED_AT_DESK | ODK already provides mature offline collection/synchronization. |
| Generic inventory/reorder from exports | KILLED_AT_DESK | Current spreadsheet templates, CSV-first products and reorder tools cover the workflow. |
| Generic Algerian WhatsApp/COD order management | KILLED_AT_DESK | Multiple Algeria-focused products now target DM/WhatsApp/COD order capture, validation and tracking. |

## 3. Candidate retained for decisive falsification

### C1 — Offline conflict causal reconciliation

Boundary:

When two or more offline branches update shared state, an operator needs to determine:
- causal branch/version structure;
- conflicting properties;
- current authoritative state;
- resolution action;
- evidence supporting the decision.

Why it remains open:

ODK exposes conflict metadata and history; RxDB supports configurable conflict handlers and CRDTs; CouchDB preserves conflicting revisions. Therefore the residual gap cannot be stated as "conflicts are not supported".

The only plausible remaining gap is operator-facing causal reconstruction across cases where the incumbent evidence is technically sufficient for synchronization but insufficient for safe human explanation.

State:
- Reality: ESTABLISHED
- Residual pain: EXPERIMENTALLY_SUPPORTED at platform/documentation level
- Gap: INFERENCE
- Action delta: HYPOTHESIS
- Opportunity: NEEDS_DECISIVE_EXPERIMENT

Required kill experiment:
Use incumbent evidence only on a fixed 5-case corpus. No candidate tool code.

## 4. Candidate reopened at narrower scope

### C2 — Semantic file-handoff breakage preflight

Boundary:

A recurring recipient receives CSV/XLSX files from a producer and needs to know before import:

- what structurally changed;
- which expected fields/values/rules are affected;
- whether the change is merely cosmetic or will change a downstream action;
- whether to accept, reject, or request correction.

This is deliberately narrower than "CSV validation" or "schema diff".

Why generic versions are killed:

Current tools already repair/validate CSV and Excel files and show import risks. Current data-platform products also perform lineage and impact analysis. Therefore a useful gap would need to live specifically in the boundary between unregistered file handoffs and downstream operational decisions.

State:
- Reality: OPEN
- Residual pain: HYPOTHESIS
- Gap: HYPOTHESIS
- Action delta: HYPOTHESIS
- Opportunity: NEEDS_DECISIVE_EXPERIMENT

Required kill experiment:
Create a 10-case corpus containing header removal/rename, type change, unit change, category-value change and structural-only changes. Compare:
1. Excel/Sheets + built-in import behavior;
2. ImportFix / current file validators;
3. a schema/lineage system where setup is feasible.

Kill if the incumbent workflow can produce the same accept/reject/request-correction decision on >=8/10 cases without material configuration burden.

Survive only if the missing result is repeatable, decision-changing, and not merely a nicer report.

## 5. Previously inspected repositories — opportunity status

### Open-System-One
INTERNAL_PRIMITIVE / RESEARCH_AUTHORITY.
It is the current control/evidence integration surface. It is not itself evidence of market demand.

### Machine
RESEARCH_INSTRUMENT.
The current work concerns experimental methodology and machine-native mechanisms. The existence of open research frontiers is not external demand evidence.

### Llms-mcp-android
RESEARCH_INSTRUMENT / INTERNAL_RUNTIME.
The documented UNKNOWN-effect and caller-side recovery problems are real technical frontiers. Existing Android/agent execution infrastructure must be tested before treating them as standalone developer-product opportunities.

### m0-durable-run
RESEARCH_INSTRUMENT.
Process-restart persistence and idempotent run behavior are experimentally useful, but generic durable execution is an established architectural category.

### Wedgettok
PRODUCT_HYPOTHESIS.
The repository has a substantial verified prototype boundary, but it still lacks external demand evidence for creator supply, retention, user preference and product-market fit.

### la-rouine-platform
PRODUCT_HYPOTHESIS / LOCAL EXPERIMENT.
The local-business digitization direction has an implementation surface, but current market search shows multiple Algerian tools already cover ERP/invoicing/inventory/WhatsApp/COD workflows. A product claim therefore needs a much narrower problem statement and independent evidence.

### Portfolio-Repository-Inventory
INTERNAL_KNOWLEDGE_SYSTEM.
It is valuable as the portfolio evidence system, not as a product opportunity by itself.

### PyPI / older packages
RESEARCH_ARTIFACTS until an external problem statement and user workflow is independently evidenced. Package existence is not demand evidence.

## 6. New methodological findings

### 6.1 Add an Opportunity Coverage Reserve

Every cycle must include at least one candidate from outside the prior favorite domains, and at least one workflow where the pain is likely under-indexed online.

Example domains:
- field/service operations;
- procurement/back-office;
- education/administration;
- privacy/local computing;
- small-team coordination.

### 6.2 Add a Workaround Strength Gate

A workaround is not merely another competitor.

Record:
- setup time;
- operator skill;
- recurrence;
- error exposure;
- reversibility;
- maintenance burden.

The comparison baseline is the strongest practical workaround, not the weakest incumbent.

### 6.3 Add a Buyer/Adoption Counterfactual

Before BUILD_ALLOWED, record:
- who experiences the pain;
- who can authorize the intervention;
- who pays or bears adoption cost;
- what must change in their workflow;
- what can remain unchanged.

An action delta with high adoption cost can still be NOT_WORTH_BUILDING.

### 6.4 Add an Action-Consequence Gate

Not every action delta matters.

Record:
- action change;
- consequence if wrong;
- consequence if absent;
- reversibility.

Low-stakes cosmetic changes are not sufficient evidence of opportunity.

### 6.5 Add a Prior-Art Freshness Gate

For fast-moving software categories:
- re-run incumbent search immediately before BUILD_ALLOWED;
- re-run after any major prototype pivot;
- preserve the previous result rather than overwriting it.

### 6.6 Add an Oracle-Independence Gate

Where feasible, oracle creation and tool implementation should be separated.

The oracle must not derive expected truth from the candidate's own output.

### 6.7 Add a No-Build Result Class

The cycle may end with:

NO_MVP / ALL_KILLED

and this must be treated as a complete research result.

## 7. Current decision state

Current external product-opportunity state:

NO_CONFIRMED_PRODUCT_OPPORTUNITY

Current research candidates requiring decisive experiments:

C1 — offline conflict causal reconciliation
C2 — semantic file-handoff breakage preflight

Current internal research instruments:

CapabilityKernel
Direct Impact Guard
Machine experiments
Android recovery experiments
M0 durable-run

No item is BUILD_ALLOWED.

## 8. Next discriminating actions

C1:
run the 5-case incumbent-only offline conflict falsification.

C2:
run the 10-case incumbent comparison for semantic file-handoff breakage.

Whichever candidates survive these tests must then pass:
- evidence multiplicity;
- residual pain;
- action consequence;
- adoption counterfactual;
- oracle integrity.

Only after that may one become an experimental winner.

## 9. Negative knowledge rule

All killed candidates remain recorded with their kill reason.

A future cycle may reopen one only when:
- the external environment changed;
- a new user population is identified;
- the previous kill scope was materially narrower/different;
- new evidence contradicts the previous kill.

Otherwise do not repeat the search.
