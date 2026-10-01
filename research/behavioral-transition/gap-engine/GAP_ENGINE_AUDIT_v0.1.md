# Gap Engine Audit — Transition Integration v0.1

Date: 2026-10-02
Status: REVIEWED / NOT INDEPENDENTLY EXECUTED IN THIS REPO
Source: user-supplied gap_engine.py and reported 1500-world selftest

## 1. Scope

The supplied engine implements:

Observed measurements
-> rate estimation
-> target tolerance/rate threshold
-> automation-gap classification
-> mechanism selection
-> missing-rate reporting
-> post-execution aggregate effect reconciliation

It is compatible with the transition-centered model because it produces an explicit target condition and an executable mechanism plan.

## 2. Correct conceptual placement

The engine should be treated as:

Transition analysis / mechanism planning

not as:

Opportunity proof
market-demand proof
product proof

The engine can establish properties of a modeled transition and can support execution planning. It cannot establish external demand by simulation.

## 3. Mathematical checks

For normalized residual d_i and additive mechanism rates K_im:

log d_i(t) = alpha_i - k_i t + noise

Forecast under a selected mechanism set X:

log residual = log(w_i) + ybar_i - k_i tau - T L_i(X)

This is algebraically coherent under the declared model.

The forecast variance:

s_i^2/n_i + tau_i^2 SE(k_i)^2 + T^2 Var(L_i(X))

is coherent under the stated independence assumptions.

Required explicit assumptions:

- homoscedastic log-noise;
- Gaussian errors where t-based inference is used;
- fixed observation times;
- independence of ybar and k from centered OLS;
- independent mechanism-effect estimates unless covariance is supplied;
- additive mechanism-effect variance unless interaction covariance is modeled.

## 4. Critical epistemic corrections

### 4.1 Plan confidence is not an exact confidence guarantee

The confidence value is Bonferroni-adjusted across dimensions for the fitted rate component, but the full plan margin also contains estimated residual variance, estimated mechanism-effect variance, optional interactions, forecast horizon, and dependence assumptions.

Therefore a declared confidence such as 0.9 must not be described as a formal 90% joint coverage guarantee for the complete plan unless a joint statistical derivation and validation establish it.

Recommended status:

PLAN_COVERAGE = EMPIRICALLY_SUPPORTED_ON_GENERATOR

not:

PLAN_COVERAGE = THEOREM.

### 4.2 Feedback identifies aggregate selected-set lift, not individual mechanism effects

The feedback estimates aggregate selected-set lift and the current update rescales every selected mechanism proportionally.

This is a calibration heuristic. It does not identify which mechanism caused the deviation and cannot separate individual effect error, mechanism interaction, pilot bias, or drift.

Recommended name:

aggregate_lift_calibration

rather than mechanism_identification.

### 4.3 Missing-rate semantics

max(0, -margin) / T is the deterministic additional rate required if the added rate has no uncertainty and does not alter existing uncertainty terms.

It is not generally the exact minimum rate of a new uncertain mechanism.

Recommended field:

missing_rate_deterministic_lower_bound

### 4.4 Cause attribution

attribute() is explicitly non-identifiable from rate data alone.

Keep it as ASSUMPTION / MODEL-DERIVED and never promote the shares to measured causal contribution.

## 5. Self-test oracle audit

The synthetic oracle is conceptually appropriate because world truth is generated separately from the engine.

However the source of truth must be frozen and versioned independently.

The current self-test intentionally evaluates interference not supplied to the planner via true_lift(W, X, f), while world_spec() omits that interaction from the planner model.

This is a valid adversarial test for model misspecification, but it must be labeled explicitly as:

UNMODELED_INTERFERENCE_STRESS_TEST

rather than mixed with the nominal success table.

## 6. Self-test coverage limits

The generator fixes:

- NDIM = 4;
- NM = 8;
- NPRE = 8;
- TH = 20;
- log-noise = 0.08;
- pilot relative error = 25%;
- one interaction pair;
- binary mechanism selection.

This validates the engine over the chosen synthetic distribution, not over the general real-world space.

The reported 1500-world results are therefore:

USER_REPORTED / SIMULATION_SUPPORTED

until an independent repository execution record exists.

## 7. M > 16 branch

The engine switches from exact enumeration to greedy + prune for M > 16.

That branch is not covered by the reported 1500-world default because the self-test uses NM=8.

Required separate experiment:

- M in {17, 24, 32, 64};
- exact oracle on reduced instances;
- adversarial cost/effect distributions;
- compare feasibility, cost ratio, false-closable, false-unclosable.

Until then the large-M planner status is UNKNOWN.

## 8. Required representation for transition lineage

A complete engine run must preserve separate immutable records:

RawObservationSet
-> FittedTransitionModel
-> TargetTransition
-> GapAssessment
-> MechanismCandidateSet
-> Plan
-> Execution
-> ObservedEffect
-> Verification
-> FeedbackUpdate
-> DecisionRevision

The plan must never overwrite the fitted model.

The feedback update must create a new model revision.

## 9. Required deterministic identity

Every run should bind:

- source_snapshot_id;
- transition_id;
- model_version;
- mechanism_set;
- confidence;
- horizon;
- spec_digest;
- code_revision;
- oracle_version.

The same immutable inputs must reproduce the same planning result, subject only to declared numerical nondeterminism.

## 10. Required experimental split

Keep three different claims separate:

A. Model correctness
Does the implementation match the equations?

B. Statistical calibration
Does declared coverage match empirical coverage on known-truth worlds?

C. Operational usefulness
Does the resulting transition change a real workflow against the strongest no-build baseline?

Passing A or B does not establish C.

## 11. Current evidence disposition

User-reported 1500-world results:
- rate recovery: USER_REPORTED / SIMULATION_SUPPORTED
- gap detection: USER_REPORTED / SIMULATION_SUPPORTED
- plan success vs confidence: USER_REPORTED / SIMULATION_SUPPORTED
- feedback calibration: USER_REPORTED / SIMULATION_SUPPORTED

Repository-independent execution:
- UNKNOWN

Real-world validity:
- UNKNOWN

Opportunity validity:
- NOT TESTED

## 12. Required next verification set

V1 — reproduce the exact supplied self-test from a pinned repository revision.

V2 — run a second independent generator family with different parameter ranges.

V3 — test model misspecification separately from nominal calibration.

V4 — test M > 16 planner against exact reduced-instance oracle.

V5 — test correlated mechanism-effect uncertainty.

V6 — test feedback on individually identifiable pilots and with interaction terms.

V7 — replay one real transition record, preserving raw observations and decision lineage.

Only V7 can begin to connect the mathematical engine to the transition/opportunity layer.
