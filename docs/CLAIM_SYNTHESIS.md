# Cross-Experiment Claim Synthesis Layer v0.1

This is NON-CANONICAL research/control-plane infrastructure.

## Purpose

Layer 11 consumes the immutable AdaptiveFrontierState produced by Layer 10 and creates a second, explicit boundary:

Evidence assessments
-> cross-experiment synthesis
-> contradiction detection
-> explicit ClaimRevision

The layer does not alter experiment receipts, hypothesis priors, or execution authority.

## Claim contract

A ClaimSpec binds:

- claim key
- human-readable statement
- one hypothesis key
- one explicit scope

The binding is explicit. A claim is not inferred from a string match or from reachability in the experiment graph.

## Cross-experiment synthesis

For a claim, the layer collects all scoped HypothesisAssessment events for the claim's hypothesis.

The derived disposition is:

- NO_EVIDENCE: no assessment exists
- UNRESOLVED: only unresolved assessments exist
- SUPPORTED: support exists with no contradiction or unresolved assessment
- CONTRADICTED: contradiction exists with no support or unresolved assessment
- SUPPORTED_WITH_UNRESOLVED: support exists, but at least one assessment is unresolved
- CONTRADICTED_WITH_UNRESOLVED: contradiction exists, but at least one assessment is unresolved
- CONFLICTED: both support and contradiction exist

This synthesis is a deterministic evidence summary, not a probabilistic posterior.

## Contradiction handling

A contradiction is retained as evidence. The layer does not pick a winning experiment and does not delete or rewrite earlier assessments.

A conflict is therefore represented explicitly until a later experiment or an explicit claim revision resolves it.

## Claim revision

A ClaimRevision is the explicit act of changing a claim's control-plane status.

For EXPERIMENTALLY_SUPPORTED, the current scoped synthesis must be exactly SUPPORTED.

For CONTRADICTED, the current scoped synthesis must be exactly CONTRADICTED.

For CONFLICTED, support and contradiction must both be present.

For UNKNOWN, the current scoped synthesis must contain no identifying support or contradiction.

For these decision statuses, the revision must account for the full current evidence set. This prevents support-only cherry-picking when contradictory evidence is already present in the frontier.

Each revision records:

- parent revision
- deterministic revision id
- claim and hypothesis identity
- scope
- complete relevant evidence ids
- complete relevant assessment ids
- supporting, contradicting, and unresolved evidence ids
- rationale
- limitations
- next discriminating test

The parent revision is an optimistic-concurrency boundary. A stale parent cannot overwrite a newer claim ledger revision.

Replaying the exact same revision request against the same parent is idempotent.

## Epistemic boundary

The layer does not:

- change adaptive priors
- manufacture evidence
- infer posterior probabilities
- resolve contradictory evidence automatically
- grant execution authority
- create a Gate or DecisionRevision

Gate/verification remains a subsequent control-plane layer.
