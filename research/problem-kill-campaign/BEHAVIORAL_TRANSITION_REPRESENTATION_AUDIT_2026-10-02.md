# Behavioral Transition Re-Representation Audit — 2026-10-02

Status: REGENERATED / VALIDATION PENDING
Source methodology: Experimental Opportunity Protocol v0.2
Target representation: Behavioral Transition Protocol v0.3

## 1. Purpose

This document records the controlled re-representation of the 2026-10-01 opportunity corpus.

The migration does not claim that the new model is true because it is cleaner.

It tests whether the same prior corpus can be represented as explicit state transitions without:

- losing prior negative knowledge;
- upgrading epistemic status;
- erasing incumbent scope;
- turning inferred transitions into observations;
- confusing execution with outcome;
- making a new product opportunity appear through schema changes.

## 2. Immutable source snapshot

Repository: `Loofy147/Open-System-One`

Source branch:

`research/experimental-opportunity-v0.2`

Source commit:

`a52edc18ba321d6ac4847388791ec55a9894bbad`

Source snapshot:

`osone-opportunity-v0.2-2026-10-01`

Primary source records:

| Source | Blob SHA |
|---|---|
| `EXPERIMENTAL_OPPORTUNITY_PROTOCOL_v0.2.md` | `0ae374817921ce7b9bf051fe7295545d369f502f` |
| `EXPERIMENTAL_OPPORTUNITY_RECORD_TEMPLATES_v0.2.md` | `69d954bdbba0e2bb3a4e659f82139cfba16eccf6` |
| `CURRENT_OPPORTUNITY_STATE_2026-10-01.json` | `dcb37e1128beba818b4c6b82a54b9f8b045a91c0` |
| `OPPORTUNITY_PORTFOLIO_AUDIT_2026-10-01.md` | `4f9866703b0ee188551c925051e677133db4f5f2` |
| `OPPORTUNITY_COVERAGE_MATRIX_2026-10-01.json` | `e7dcfbc23d5ccf465cf356ed6a726e49f7b1cade` |

Mapping:

`research/problem-kill-campaign/TRANSITION_REPRESENTATION_MAPPING_v0.1.json`

Mapping version:

`bt-v0.3-reencode-v0.1`

Mapping digest:

`c439760c84a2eb01fe0aa8ef2cef80e42f6cbb08e2e03d11181ae3aa9222deac`

## 3. Accounting

The regenerated frontier currently contains:

- 12 legacy killed candidates from the portfolio audit;
- 2 current research candidates;
- 9 internal/research transitions;
- 1 methodology transition;
- 1 mathematical research transition.

The 12 killed candidates are not reconstructed as if they had originally been transition-recorded.

They are explicitly marked:

`INFERRED_FROM_AUDIT`

because the source audit stored their problem/candidate/kill representation rather than a first-class target-transition object.

## 4. Legacy candidate accounting

| Legacy candidate | v0.3 transition | Representation class | Prior decision preserved |
|---|---|---|---|
| GitHub review routing without premature notification | `bt-github-review-routing` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| SMB export-only reconciliation | `bt-smb-export-reconciliation` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic CSV/XLSX diff | `bt-generic-csv-xlsx-diff` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic pre-import CSV repair/validation | `bt-generic-preimport-validation` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic sandbox | `bt-generic-sandbox` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic policy/authorization | `bt-generic-policy-authorization` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic browser automation | `bt-generic-browser-automation` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic agent receipt/provenance | `bt-generic-agent-receipt-provenance` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic MCP discovery/validation | `bt-generic-mcp-discovery-validation` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic offline collection | `bt-generic-offline-collection` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic inventory/reorder from exports | `bt-generic-inventory-reorder` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |
| Generic Algerian WhatsApp/COD order management | `bt-generic-algeria-whatsapp-cod` | INFERRED_FROM_AUDIT | KILLED_AT_DESK |

## 5. Current research candidates

### C1

`bt-offline-conflict-causal-reconciliation`

The re-encoding makes the candidate's true uncertainty explicit:

- target transition: INFERRED;
- residual pain: EXPERIMENTALLY_SUPPORTED;
- current transition: UNKNOWN;
- action delta: HYPOTHESIS;
- incumbent set: preserved;
- decisive experiment: preserved.

The transition representation therefore does not accidentally convert the incumbent conflict metadata into proof of a gap.

### C2

`bt-semantic-file-handoff-breakage-preflight`

The re-encoding makes the unproven parts explicit:

- reality: OPEN;
- residual pain: HYPOTHESIS;
- gap: HYPOTHESIS;
- desired delta: HYPOTHESIS;
- current transition: UNKNOWN;
- incumbent set: preserved;
- decisive experiment: preserved.

No build permission is created by the representation.

## 6. Internal/research integration

The following transitions are represented as internal/research objects, not market opportunities:

- Open-System-One evidence/control surface;
- Capability Kernel authorization/effect boundary;
- Direct Impact bounded mutation;
- durable-run transition identity;
- Android UNKNOWN-effect reconciliation;
- Machine research-state verification;
- Wedgettok product hypothesis;
- la-rouine local digitization hypothesis;
- gap-closure rate model.

This is deliberately consistent with the v0.2 classification:

`INTERNAL_PRIMITIVE`,
`RESEARCH_INSTRUMENT`,
`PRODUCT_HYPOTHESIS`,
or `OPEN`.

## 7. What the new representation exposes

The re-encoding exposes distinctions that were implicit or distributed in v0.2:

1. **Target vs mechanism** — a tool is no longer the target object.
2. **Current vs desired transition** — the present workflow is represented independently from the desired state change.
3. **Execution vs outcome** — a successful run cannot satisfy the transition oracle by itself.
4. **Authority vs impact vs durability** — permission, actual state delta, and effect persistence are distinct.
5. **Oracle as first-class data** — expected truth is explicit and separately auditable.
6. **Re-encoding vs verification** — a cleaner representation cannot manufacture evidence.
7. **World revision / applicability** — a target transition is tied to the world in which it was observed or tested.
8. **Lineage** — a transition points back to the exact source record and representation event.

## 8. Known limitation of this first regeneration

The 2026-10-01 source corpus did not store a first-class `target_transition` for every legacy candidate.

Therefore the new transition fields for those records are reconstructions.

They are not historical observations.

This limitation must remain visible until a new direct observation or source artifact supports the field.

## 9. Validation contract

The representation passes only if:

[
	ext{mapped source coverage}=100%
]

[
	ext{status upgrades}=0
]

[
	ext{missing provenance}=0
]

for all required regenerated records, and:

[
R(source,mapping_v) = R(source,mapping_v)
]

under repeat generation.

Any failure creates a new negative result or contradiction; it does not justify editing the old snapshot.

## 10. Current conclusion

The v0.3 representation is **structurally useful but not yet methodologically validated**.

The next test is deterministic replay and field-provenance validation.

Only after that should we use v0.3 to rerun the C1/F1 and C2/F2 discriminating experiments.

No opportunity decision is changed by this migration alone.
