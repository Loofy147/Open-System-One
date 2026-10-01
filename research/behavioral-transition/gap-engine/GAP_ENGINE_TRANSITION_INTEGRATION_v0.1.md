# Gap Engine ↔ Behavioral Transition Integration v0.1

Date: 2026-10-02
Status: DESIGN / REVIEWED
Related methodology: Behavioral Transition Protocol v0.3

## 1. Role

Gap Engine is the quantitative operator for a TransitionTarget.

It maps:

RawObservationSet
-> FittedTransitionModel
-> TargetTransition forecast
-> GapAssessment
-> MechanismPlan
-> FeedbackObservation

It is not itself the opportunity decision engine.

## 2. Canonical mapping

### Raw observations

Input:
- observation time;
- observed value;
- target;
- scale;
- weight;
- tolerance.

Canonical transition fields:
- world_reference;
- observed_context;
- pre_state;
- source observations.

Status:
DIRECT_OBSERVATION for supplied measurements.

### Fitted transition model

Output from fit_dim:
- n;
- tbar;
- tlast;
- ybar;
- k_hat;
- residual scale s;
- SE(k_hat);
- degrees of freedom.

Canonical role:
current_transition model parameterization.

Status:
DERIVED from observations.

It must carry:
- source snapshot;
- model version;
- estimator version;
- fit settings.

### Target transition

The target is represented as the required residual condition at horizon T:

residual_i(T) <= epsilon_i

This is a quantitative target delta.

Status:
DERIVED when target/tolerance/horizon are supplied.

### Gap assessment

Gap quantity:

R_i = k_c,i - k_hat_i

The classification:
- NO GAP
- UNCERTAIN
- GAP

is an inference based on the declared statistical model and confidence procedure.

It must not be stored as direct observation.

### Mechanism plan

For mechanism subset X:

PLAN = argmin cost(X)
subject to the declared forecast closure rule.

This is a DERIVED/OPTIMIZATION result.

It must preserve:
- mechanism set;
- costs;
- confidence parameter;
- forecast;
- margin;
- lift;
- uncertainty;
- solver/algorithm revision.

### Feedback

reconcile() observes aggregate selected-set lift:

L_obs(selected set)

and compares it with L_pred(selected set).

This is:

aggregate_lift_calibration

not individual mechanism identification.

A feedback update creates a new model revision and never overwrites the prior model.

## 3. Critical model correction: weight cancellation

Current build uses:

mean = ln(w_i) + model
lneps = ln(w_i * tolerance/scale)

Therefore w_i cancels from the closure inequality.

If weights are intended to express importance, they are currently mathematically inactive in:
- gap size;
- gap classification;
- plan feasibility;
- plan selection.

This must be resolved explicitly before treating weights as meaningful.

Choose one semantic contract:

A. Weighted residual objective:
  weighted residual = w_i * d_i
  threshold = epsilon_i independent of w_i.

B. Per-dimension tolerance:
  d_i <= tol_i
  weights are used only for a separate objective/priority policy.

Do not claim the current implementation uses weights for closure until one contract is selected and verified.

## 4. Critical statistical correction

The confidence parameter in plan() is not, by itself, a formal joint forecast-coverage guarantee because the margin combines:
- OLS mean;
- estimated variance;
- k uncertainty;
- mechanism-effect uncertainty;
- optional interaction uncertainty.

Current evidence can support:

EMPIRICAL PLAN COVERAGE UNDER GENERATOR

not universal coverage.

## 5. Model-boundary checks required before real use

### 5.1 Zero residuals

fit_dim() drops exact target hits because log(0) is undefined.

This can introduce selection/censoring bias.

Required future contract:
- measurement floor, or
- censored observation model, or
- explicit exclusion rule with evidence of non-informative censoring.

### 5.2 Target crossing / overshoot

d = abs(value-target) assumes monotone approach toward the target.

If the process crosses the target, absolute distance can increase again and constant-rate log decay may be invalid.

Required field:
direction = absolute | upper | lower

or an explicit monotonicity assumption.

### 5.3 Nonstationary rates

k is assumed constant over the fitted period and forecast.

Drift/change-point behavior must be separately tested.

### 5.4 Correlated mechanism estimates

Var(L) currently assumes independent effect estimates unless covariance is supplied.

Future schema should allow:
effect_covariance or a joint pilot design.

### 5.5 Interaction parameters

An interaction supplied as a rate plus scalar variance is not enough to estimate covariance with main effects.

Interactions require explicit parameterization and covariance where claimed.

## 6. Missing-rate semantics

Current:

max(0, -margin) / T

is a deterministic equivalent-rate lower bound when new lift is treated as uncertainty-free.

Canonical field:

missing_rate_deterministic_lower_bound

not exact minimum new-mechanism rate.

## 7. Real representation lineage

A full run becomes:

RawObservationSet
  -> FittedTransitionModel
  -> TargetTransition
  -> GapAssessment
  -> MechanismCandidateSet
  -> MechanismPlan
  -> Execution
  -> ObservedEffect
  -> Verification
  -> ModelRevision
  -> DecisionRevision

Each arrow is a lineage edge.

## 8. Reproducibility identity

Bind every engine run to:

- transition_id;
- source_snapshot_id;
- spec_digest;
- mapping_version;
- model_version;
- planner_version;
- oracle_version;
- confidence;
- horizon;
- mechanism-set representation;
- code revision.

Same source snapshot + same versions + same parameters must regenerate the same canonical plan, subject to declared numeric tolerance.

## 9. Evidence separation

Keep three evidence families separate:

A. MODEL_CORRECTNESS
Equation/code agreement.

B. STATISTICAL_CALIBRATION
Known-truth simulation coverage.

C. OPERATIONAL_TRANSITION
Real workflow outcome against strongest no-build baseline.

A/B do not promote C.

## 10. Current user-reported evidence

The 1500-world results supplied on 2026-10-02 are recorded as:

USER_REPORTED / SIMULATION_SUPPORTED

They are not repository-executed evidence in this record.

## 11. Required validation sequence

V1 exact reproduction of supplied self-test from pinned source.
V2 independent generator family.
V3 weighted-semantics test after correction.
V4 zero-residual/censoring test.
V5 overshoot/direction test.
V6 nonstationary-rate stress test.
V7 correlated mechanism-effect covariance test.
V8 interaction-identification test.
V9 M > 16 exact-small-instance oracle comparison.
V10 one real transition replay with raw observations and no-build baseline.

No opportunity claim may be promoted before V10.
