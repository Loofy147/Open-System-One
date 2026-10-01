# Gap Engine Stochastic Planner Addendum v0.1

Date: 2026-10-02

## Critical distinction

The deterministic model

G(X) = sum_i D_i exp(-(k_i + K_i X)T)

supports monotonicity and submodularity results when D_i > 0, K_i >= 0, T > 0.

The implemented planner does not optimize G directly. It optimizes a risk-adjusted closure margin containing estimated uncertainty:

margin_i(X) = epsilon_i_log - [mean_i(X) + z_i sd_i(X)].

Because sd_i(X) changes with the selected mechanisms, adding a mechanism can increase the uncertainty penalty. Therefore deterministic monotonicity/submodularity cannot be inherited automatically.

## Consequence

The following inference is invalid without a separate proof/test:

R3 deterministic submodularity
=> greedy guarantee for risk-adjusted planner.

Likewise:

R7 deterministic submodular-knapsack behavior
!=
risk-adjusted planner approximation guarantee.

## Required experiment

For small M where exact enumeration is possible:

1. generate independent mechanism-effect standard errors;
2. compute the full risk-adjusted margin for every subset;
3. test monotonicity of the closure gain;
4. test diminishing returns;
5. compare greedy risk-margin selection to the exact risk-margin optimum;
6. stress high uncertainty, low cost, redundant mechanisms, and correlated effects.

Record separately:
- deterministic objective result;
- risk-adjusted objective result;
- exact optimum for each objective;
- greedy ratio;
- feasibility error.

## Decision rule

If risk-adjusted gains violate monotonicity/submodularity, retain the deterministic theorem only for the deterministic residual objective and classify the planner as a heuristic/robust optimization procedure.

Do not transfer a theorem across objectives merely because both use the same mechanism matrix.
