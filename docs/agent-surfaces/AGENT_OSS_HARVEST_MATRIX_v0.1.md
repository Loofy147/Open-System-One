# Agent OSS Harvest Matrix v0.1

Status: PREPARED_FOR_HARVEST
Date: 2026-09-30

## Decision semantics
This is not a product ranking. Priority is investigation order for a specific architectural gap.

Priority: P0 immediate proof value; P1 important infrastructure/reference; P2 comparative research; P3 reference only.
Disposition: PROVE_PRIMITIVE / ADAPTER_PROOF / REFERENCE / DO_NOT_IMPORT_YET / UNKNOWN

## Internal overlap
Existing internal assets already cover meaningful portions of durability, mobile agent runtime and action-policy-approval boundaries, typed decision/evidence contracts, and research provenance.
External harvesting must demonstrate a missing capability or a strictly better independently verified implementation for a specific boundary.

## P0 — immediate primitive proofs

| Gap | Candidate | Primitive | First proof | Disposition |
|---|---|---|---|---|
| sandboxed agent execution | NVIDIA OpenShell | declarative filesystem/network/process policy | disposable agent; verify denied file/network action | PROVE_PRIMITIVE |
| generic sandbox lifecycle | Alibaba OpenSandbox | SDK + unified sandbox API + Docker/Kubernetes backends | create/inspect/execute/terminate and reconstruct lifecycle | PROVE_PRIMITIVE |
| policy decision point | Open Policy Agent | externalized allow/deny policy evaluation | versioned policy/data input and deny-path receipt | PROVE_PRIMITIVE |
| relationship authorization | OpenFGA | ReBAC over agent/resource/user graph | user∩agent capability plus revocation | PROVE_PRIMITIVE |
| policy language | Cedar | typed policy evaluation | equivalent authorization corpus against OPA | PROVE_PRIMITIVE |
| workload identity | SPIFFE/SPIRE | cryptographic workload identity | identity issuance and peer authentication in disposable workloads | PROVE_PRIMITIVE |
| browser capability | Playwright MCP | narrow browser action/observation interface | disposable test site + action trace | ADAPTER_PROOF |
| AI observability | OpenInference + OpenTelemetry | standardized agent/tool/LLM spans | correlate tool span to our run_id | PROVE_PRIMITIVE |
| agent evaluation | Inspect AI | reproducible evaluation runner | fixed agent task + saved config/result | PROVE_PRIMITIVE |
| browser evaluation | BrowserGym | browser environment + benchmark/trace path | one isolated benchmark task | PROVE_PRIMITIVE |
| prompt-injection evaluation | AgentDojo | dynamic tool/user/attack benchmark | injection fixture + expected security disposition | PROVE_PRIMITIVE |
| agent protocol validation | A2A Inspector/TCK | protocol compatibility/conformance | minimal agent conformance case | PROVE_PRIMITIVE |

## P1 — durability and execution

| Candidate | Primitive | Why test | Disposition |
|---|---|---|---|
| Temporal | durable workflow/activity execution | crash/restart, retry and side-effect semantics | REFERENCE_THEN_PROVE |
| Trigger.dev | long-running tasks, checkpointing, retries, idempotency, HITL | compare duplicate trigger and pause/resume | REFERENCE_THEN_PROVE |
| Restate | journaled durable execution and idempotency | ambiguous network failure + duplicate invocation | PROVE_PRIMITIVE |
| LangGraph | checkpoint/resume/interrupt | interrupted node + resume without duplicated effect | PROVE_PRIMITIVE |
| Hatchet | distributed task/event execution | cancellation + retry + scheduling | REFERENCE |

Do not replace m0-durable-run unless a proof closes a measured gap.

## P1 — memory and state

| Candidate | Primitive | First proof | Disposition |
|---|---|---|---|
| Letta | stateful identity + memory | correct/delete one fact; test temporal provenance | PROVE_PRIMITIVE |
| Graphiti | temporal knowledge graph | conflicting facts at different timestamps; current vs historical query | PROVE_PRIMITIVE |
| Mem0 | memory write/update/retrieval | compare recalled fact to durable evidence and correction | REFERENCE |
| Cognee | graph/vector memory pipeline | ingest -> graph -> retrieve -> correction/delete | REFERENCE |

Memory is never authoritative. Persisted recall is not a Claim.

## P1 — runtime references

| Candidate | Primitive or lesson | Disposition |
|---|---|---|
| OpenHands Software Agent SDK | agents/tools/workspaces/events/REST-WebSocket | PROVE_PRIMITIVE |
| OpenAI Agents SDK | tools, handoffs, guardrails, approvals, sessions, MCP | PROVE_PRIMITIVE |
| Claude Agent SDK | permissions/hooks/MCP | PROVE_PRIMITIVE |
| Google ADK | agent/workflow runtime + A2A | PROVE_PRIMITIVE |
| Microsoft Agent Framework | post-AutoGen/Semantic Kernel convergence | REFERENCE |
| AWS Strands Agents | provider-neutral agent SDK and tools | REFERENCE |
| Pydantic AI | typed tools/dependencies/structured outputs | PROVE_PRIMITIVE |
| smolagents | minimal code-agent loop | REFERENCE |
| Agno | agent/service/interfaces/approval/A2A/AGUI | REFERENCE |
| CrewAI | Crews/Flows event-driven orchestration | REFERENCE |
| OpenClaw | local daemon/runtime/channels/model interchangeability | PROVE_PRIMITIVE |
| Gemini CLI | terminal-first local agent + MCP/tool loop | PROVE_PRIMITIVE |
| goose | local developer agent/harness | REFERENCE |
| Aider | git-aware coding loop | REFERENCE |
| mini-SWE-agent | minimal agent-computer interface | PROVE_PRIMITIVE |

## P1 — governance and identity support

| Candidate | Primitive | First proof | Disposition |
|---|---|---|---|
| OPA | policy-as-code PDP | versioned decision + deny reason | PROVE_PRIMITIVE |
| OpenFGA | ReBAC | agent/user/resource intersection + revocation | PROVE_PRIMITIVE |
| Cedar | policy evaluation | equivalent policy corpus | PROVE_PRIMITIVE |
| SPIFFE/SPIRE | workload identity | attestation and rotation | PROVE_PRIMITIVE |
| OpenBao | secrets/credential broker | short-lived test credential; no secret in agent process | REFERENCE_THEN_PROVE |
| microsoft/identity-spiffe | agent identity + sidecar enforcement | inspect end-to-end enforcement chain | REFERENCE |
| Azure/kars | Kubernetes agent reference stack | inspect sandbox/policy/audit/agent-mesh composition | REFERENCE |

## P2 — evaluation, red team, environments

| Candidate | Primitive or lesson | Disposition |
|---|---|---|
| WebArena | realistic browser task environment | PROVE_PRIMITIVE |
| OSWorld | computer-use benchmark | PROVE_PRIMITIVE |
| Online-Mind2Web | online web-agent evaluation methodology | REFERENCE |
| ClawBench | live-site write interception | PROVE_PRIMITIVE |
| SWE-bench | real repository issue benchmark | PROVE_PRIMITIVE |
| Promptfoo | agent/model eval and red-team automation | PROVE_PRIMITIVE |
| garak | LLM vulnerability probing | PROVE_PRIMITIVE |
| PyRIT | structured AI red-team orchestration | REFERENCE_THEN_PROVE |
| Giskard | AI testing/evaluation patterns | REFERENCE |

## Provider/model substrate
LiteLLM, vLLM, llama.cpp, Ollama and SGLang remain below the authority layer. Their relevance is provider/model interchangeability, not task/evidence semantics.

## Micro-activation queue
1. Playwright MCP
2. Context7
3. OpenInference instrumentation
4. A2A Inspector/TCK
5. AG-UI bridge
6. ACP bridge
7. GitHub capability adapter
8. OpenShell policy adapter
9. OpenFGA adapter
10. OPA adapter

## Internal reuse rule
Before importing external source, inspect the nearest internal implementation:
- durability -> m0-durable-run
- action/policy/approval -> Llms-mcp-android
- decision/evidence -> Open-System-One
- research provenance -> Machine

If the external candidate does not close a measured gap, prefer a documented reference over code import.

## Harvest gate
source/revision captured; license cleared; primitive identified; positive test; negative/kill test; receipt; independent verification; removal test.

## Current state
Cataloged. Matrix prepared. No external source code is promoted to integrated status by this matrix.
Next step: execute proof cards for P0 candidates; do not accumulate dependencies without evidence.