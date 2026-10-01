# Gap Engine Correction Patch Contract v0.1

Date: 2026-10-02
Status: REQUIRED BEFORE REAL-WORLD USE

## 1. Weight semantics

The current implementation multiplies both forecast residual and threshold by w_i, causing cancellation.

Required weighted-demand contract:

q_i(t) = w_i * |value_i(t) - target_i| / scale_i

and the closure threshold must be independent of w_i:

q_i(T) <= tolerance_i / scale_i

Therefore the log forecast keeps +log(w_i), while the log threshold does not contain log(w_i).

Regression requirement:
- changing w_i changes the gap/planning quantities;
- setting all w_i = 1 recovers the unweighted model;
- scaling every weight by a common factor changes priority consistently with the declared contract.

## 2. Confidence naming

Until a joint predictive-coverage theorem is established, retain the input for compatibility but report it as a target confidence/risk parameter, not as a universal coverage guarantee.

Preferred semantic name:
forecast_coverage_target

Optional compatibility alias:
confidence

## 3. Risk-adjusted planner objective

Do not inherit deterministic submodularity claims into the risk-adjusted margin objective.

For M <= 16:
- exact enumeration remains the reference planner;
- test whether risk-margin gains are monotone/submodular;
- compare greedy against the exact risk-margin optimum.

For M > 16:
- greedy/prune is explicitly heuristic until separately benchmarked.

## 4. Mechanism uncertainty

Support either:
- independent effect SEs with an explicit independence contract;
- or a full per-dimension covariance matrix.

Do not silently treat correlated pilot estimates as independent.

## 5. Interaction uncertainty

Represent main effects and interaction effects as separate estimable parameters.
Their covariance must be modeled when the pilot design couples them.

## 6. Zero residual policy

Do not silently drop zero residuals in a production run.
Choose one:
- explicit measurement floor with documented meaning;
- censored model;
- reject the fit with a machine-readable reason.

## 7. Direction / crossing

Add explicit transition mode:
- ABSOLUTE_DISTANCE;
- UPPER_BOUND;
- LOWER_BOUND.

For ABSOLUTE_DISTANCE, crossing behavior must be validated before assuming log-linear decay remains valid.

## 8. Rate stationarity

The model must expose the stationarity assumption and provide a stress test or detector for drift/change points.

## 9. Feedback

Rename feedback to aggregate_lift_calibration.
It updates a selected-set calibration record or a model revision.
It must not rewrite individual K_im values unless the experiment design identifies those effects.

## 10. Missing-rate output

Use:
missing_rate_deterministic_lower_bound

and document the assumptions under which it is valid.

## 11. Reproducibility

Every execution artifact must bind:
- code revision;
- spec digest;
- seed;
- world generator version;
- oracle version;
- planner version;
- source snapshot;
- mapping version.

Same immutable inputs must reproduce the same canonical result within declared numerical tolerance.

## 12. Compatibility rule

The corrected implementation must preserve the old implementation/result as a historical comparator.
Do not overwrite the old model or its simulation result.
