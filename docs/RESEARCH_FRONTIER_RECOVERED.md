# Research Frontier — Recovered 2026-09-24

This is the recovered research frontier. It is broader than the minimal current contract.

## Active research surface
Contract: typed Choice/Score/Noul, finite outcomes, stable IDs, batch-first evaluation, schema-safe answers.
Model paths: causal-logit, diffusion read-slot protocol, compact learned student.
Scorers: pairwise, marker/shared, set-aware, Set Transformer, relational, conditional mixture.
Uncertainty: temperature scaling, conformal sets, abstention/selective policy.
Scalability: shortlist/prefilter plus rerank.
Machine-native primitives: 12 single primitives and 5 registered pair interactions.

## Current evidence tiers
ESTABLISHED: contract semantics, separation of model output from execution authority, probability normalization, ordinal Score semantics.
EXPERIMENTALLY_SUPPORTED: v0.3 structural suite 31/31; primitive probes 12/12; scorer permutation/masking properties; calibration/selective implementations; oracle shortlist behavior.
USER_REPORTED: browser MiniLM single-decision receipt and 12-case benchmark receipt.
OPEN: real pretrained encoder superiority; set-aware real-data advantage; conditional real-data advantage; real-backend batch independence; shift calibration; real embedding shortlist recall; learned student versus generic embedding baseline.

## Critical interpretation
Conditional mixture is not a failed idea. Small synthetic batches show repeated Brier improvements in several tasks, sometimes with a small accuracy tradeoff.
Set-aware is not a winner. It has a strong representative interaction result but loses in other settings.
The next experiments must distinguish accuracy, probability quality, calibration, candidate interaction, retrieval, and compute cost.