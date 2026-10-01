# OSS P0 Proof Campaign v0.1

Status: READY_FOR_EXECUTION
Date: 2026-09-30

## Rule
Every P0 candidate must prove one narrow capability. Installation success is not acceptance.

## P0.01 OpenShell
Question: can an agent execute inside a policy-enforced sandbox without exceeding declared filesystem/network/process scope?
Test: create disposable sandbox; allow one known file read; deny one outside path and one undeclared network destination; execute agent action.
Pass: denied operations are actually denied and the denial is observable.
Evidence: policy revision, sandbox identity, action trace, denial result, final filesystem/network state.

## P0.02 OpenSandbox
Question: can sandbox lifecycle be controlled through a stable SDK/API abstraction?
Test: create -> inspect -> execute -> collect artifact -> terminate one sandbox.
Pass: all lifecycle states are observable and termination leaves no unexpected active workload.
Evidence: sandbox ID, API requests, runtime/provider identity, artifact reference, terminal state.

## P0.03 OPA
Question: can policy decisions be externalized from agent execution?
Test: evaluate one allow and one deny request against versioned Rego policy and input.
Pass: decision is deterministic for the fixed policy/input and policy revision is recordable.
Evidence: policy digest, input digest, decision, deny reason, evaluation timestamp.

## P0.04 OpenFGA
Question: can permissions encode the relation between user, agent, capability and resource?
Test: grant a user permission to a resource, grant the agent a narrower capability, test intersection; revoke one relationship and repeat.
Pass: effective access changes exactly with the declared relationship mutation.
Evidence: model version, tuples/relationships, authorization decisions, revocation observation.

## P0.05 Cedar
Question: can a typed policy model express the same bounded authorization cases independently of the application?
Test: implement the P0.03/P0.04 decision corpus in Cedar.
Pass: expected decisions agree on the fixed corpus and all policy revisions are recorded.
Evidence: policy source/digest, entities, request, decision, errors.

## P0.06 SPIFFE/SPIRE
Question: can workload identity replace long-lived shared credentials at the execution boundary?
Test: two disposable workloads obtain identities; workload A requests B; rotate/revoke identity and repeat.
Pass: valid identity is accepted, invalid/revoked identity is denied.
Evidence: trust domain, SVID identity, rotation event, mTLS outcome, policy decision.

## P0.07 Playwright MCP
Question: can browser capability remain a narrow, inspectable tool boundary?
Test: use a disposable website with read-only pages and one intentionally blocked external action.
Pass: allowed navigation/read succeeds; blocked action is denied or requires explicit approval; action sequence is reconstructible.
Evidence: browser/session identity, tool calls, target URLs, final page state, screenshots/DOM where available.

## P0.08 OpenInference
Question: can heterogeneous agent/tool execution share a trace identity that maps to our run_id?
Test: instrument one agent -> tool -> result path.
Pass: one trace contains the expected hierarchy and can be correlated to the external run identifier.
Evidence: trace ID, span IDs, model/tool identity, timestamps, correlation attributes.

## P0.09 Inspect AI
Question: can an agent experiment be defined, executed and reproduced as a durable evaluation artifact?
Test: fixed task/config/model stub where possible; run twice.
Pass: configuration and outputs are captured sufficiently to explain differences.
Evidence: eval spec, environment, run IDs, outputs, scorer, result artifact.

## P0.10 BrowserGym
Question: can browser-agent behavior be evaluated in a repeatable environment rather than by narrative review?
Test: run one supported benchmark task in an isolated environment.
Pass: environment reset, task input, action trace and score/artifact are recoverable.
Evidence: benchmark/task ID, environment version, trajectory, result.

## P0.11 AgentDojo
Question: can prompt-injection/tool-integrity failures be exercised systematically?
Test: run a benign task with injected malicious instructions targeting tools or data.
Pass: expected security disposition is observed and tool side effects remain within the test contract.
Evidence: scenario ID, injection content reference, tool calls, security outcome, final state.

## P0.12 A2A TCK / Inspector
Question: can a minimal agent surface be checked for protocol compatibility independently of the agent implementation?
Test: expose a minimal A2A service and run TCK/Inspector checks.
Pass: mandatory compatibility tests produce machine-readable results and agent-card identity is captured.
Evidence: protocol version, agent card, transport, test results, implementation revision.

## Promotion
Each candidate moves from P0 to integrated status only after:
source/revision captured -> license cleared -> positive test PASS -> negative test PASS -> durable receipt -> independent verification -> removal test.

## Important comparison
Do not compare candidates by product quality.
Compare whether each closes a measured architectural gap at the narrowest reusable boundary.

## Stop conditions
Stop the campaign for a candidate if it causes unauthorized external mutation, exposes credentials, expands permissions, cannot be isolated, or cannot produce enough evidence to reconstruct a consequential action.

## Expected output
For each candidate produce:
capability | prerequisite | test | observed behavior | evidence | limitation | disposition