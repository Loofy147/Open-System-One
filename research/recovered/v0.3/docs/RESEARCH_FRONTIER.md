# Research Frontier — Decision / Primitive Sweep

This is an experimental frontier, not a final architecture.

## Current tested core

State -> independent typed questions -> finite outcome spaces -> batch scorer -> probabilities -> calibration -> deterministic policy.

## Current implementation status

- Pairwise scorer: baseline.
- DeepSets-style scorer: structural pass; performance unresolved.
- Set Transformer: structural pass; performance unresolved.
- Explicit relational scorer: structural pass; performance unresolved.
- Conditional mixture scorer: promising on one synthetic interaction family; not universal.
- Candidate shortlist: promising scalability primitive; only oracle-vector evidence so far.
- Temperature scaling: implemented.
- Split conformal sets: implemented; broad distribution-shift validation pending.

## Kill-test rule

No primitive enters the core merely because an upstream project uses it. It needs:

1. a machine-checkable contract,
2. property/kill tests,
3. an isolated effect on a controlled task,
4. an ablation against the smallest baseline,
5. a known failure mode,
6. provenance to the external mechanism when applicable.

## Open questions

1. Does candidate interaction improve real decision quality after controlling for parameter count and training budget?
2. Can a conditional scorer recover most of the interaction benefit while preserving pairwise behavior on independent tasks?
3. What shortlist recall is required before downstream scoring becomes statistically unsafe?
4. Do calibration and conformal coverage survive language/domain/task shift?
5. Does marker/shared-context conditioning outperform generic set mechanisms after transfer to a real encoder?
