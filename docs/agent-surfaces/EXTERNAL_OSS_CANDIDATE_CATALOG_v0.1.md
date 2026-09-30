# External Open-Source Agent/AI Infrastructure Candidate Catalog v0.1

Status: CANDIDATE_UNIVERSE
Date: 2026-09-30

## Scope

This catalog contains external open-source projects that may provide reusable primitives for Open-System-One.

None of these projects is part of the user's portfolio by default.

"Candidate" means:
- public source is available;
- the project exposes a potentially useful capability;
- current usefulness still requires inspection, license review, dependency review, and an explicit proof.

Do not infer that inclusion means adoption.

## A. Agent runtimes and SDKs

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| OpenHands / Software Agent SDK | agent loop, state, tools, workspace, skills, MCP | typed action/observation lifecycle |
| Letta | stateful agents and memory | state/memory abstraction, durable agent identity |
| LangGraph | stateful orchestration/checkpointing | graph execution, checkpoint/resume patterns |
| Pydantic AI | typed agent framework | typed dependencies, tools, structured outputs |
| CrewAI | Crews + event-driven Flows | event-driven orchestration patterns |
| Agno | agent platform + AgentOS | service/control-plane integration ideas |
| Qwen-Agent | open-source agent framework with tool/planning/memory | lightweight model/tool harness |
| smolagents | compact code-oriented agent framework | minimal agent loop and code-action patterns |
| AutoGen / AG2 | multi-agent orchestration | collaboration/handoff patterns |
| DSPy | declarative LM programs | optimizer/evaluation/compilation patterns |
| OpenClaw | local user-owned agent runtime | local control, channels, daemon/runtime patterns |
| Gemini CLI | terminal-first open-source agent | CLI/tool/MCP integration |
| goose | open-source developer agent | extensible local agent/harness |
| Aider | terminal coding agent | git-aware edit/test loop |
| mini-SWE-agent | minimal coding agent | minimal ACI and trajectory model |
| Continue | open-source coding agent | IDE/CLI/CI agent integration; note project maintenance status |

## B. Coding-agent and agent-computer research

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| OpenHands | full software-agent stack | trajectory, workspace and tool abstractions |
| mini-SWE-agent | minimal agent-computer interface | simple tool/observation loop |
| SWE-agent | research-oriented ACI + sandboxed execution | ACI and trajectory inspection ideas |
| Aider | git-native coding workflow | repository mapping and reversible git workflow |
| Continue | IDE/CLI/CI agent | agent surface integration patterns |

Important:
The current SWE-agent project recommends mini-SWE-agent for new work. Continue's main repository states that it is no longer actively maintained and had a final 2.0.0 release. Treat it as historical/reference material unless a maintained fork is independently verified.

## C. Sandbox / execution isolation

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| NVIDIA OpenShell | agent sandbox + declarative filesystem/network/process policy | policy enforcement below application level |
| SWE-ReX | sandboxed execution backend used by SWE-agent | remote/reproducible execution boundary |
| OpenSandbox | general sandbox infrastructure | execution isolation abstraction |
| Docker / container runtimes | process/filesystem isolation | disposable execution substrate |
| gVisor | user-space kernel isolation | stronger container isolation option |
| Firecracker | microVM isolation | high-isolation disposable workloads |

Do not treat a container as a security boundary without measuring the required threat model.

## D. Durable execution / workflow

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| Temporal | durable workflows, activities, retries | stable run identity and recovery |
| Trigger.dev | long-running AI tasks, retries, queues, idempotency, HITL | practical agent job runtime |
| LangGraph | checkpoint/resume execution | state recovery |
| Hatchet | distributed task/workflow execution | event/task orchestration |
| Prefect | workflow engine | execution and retry primitives |
| Dagster | durable data/workflow orchestration | artifact/data lineage patterns |

The reusable target is not the whole workflow engine. It is the smallest primitive that closes a measured durability gap.

## E. Memory / context / knowledge state

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| Letta | stateful agent memory | core/archival memory model |
| Graphiti | temporal knowledge graph | historical relation validity |
| Mem0 | memory layer | controlled memory write/update/delete decisions |
| Cognee | graph + vector memory pipeline | ingestion/graph construction |
| Zep | managed context platform using Graphiti | reference architecture only where OSS boundary is clear |
| Memory-Fort | local cross-tool memory vault | portable local memory pattern |

Memory integration requires an authority test:
persisted recall is not evidence and is not a claim by itself.

## F. Browser / computer-use

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| Browser Use | open-source browser agent + local/cloud browser | browser capability layer |
| Playwright MCP | deterministic browser capability through MCP | narrow browser activation |
| Stagehand | AI actions on Playwright | semantic action layer with deterministic Playwright fallback |
| Browser Harness | browser control for existing agents | surface-level browser activation |
| agent-browser | accessibility-tree browser interface | token-efficient semantic browser observation |
| Browser Use workflow-use | workflow/RPA browser automation | deterministic browser workflows |

Browser activations must separately record:
browser session identity, cookies/auth state, action trace, screenshots/DOM where available, and final external state.

## G. Interoperability protocols

| Project/spec | Boundary | Candidate extraction |
|---|---|---|
| MCP | agent -> tools/data | portable capability interface |
| A2A | agent -> agent | delegated/inter-agent execution |
| AG-UI | agent -> user-facing application | streaming/user interaction events |
| ACP | editor -> coding agent | coding-agent client boundary |

Protocol support must be characterized at the level of:
identity, correlation IDs, errors, cancellation, authorization, artifact references, and version negotiation.

## H. Observability / evaluation

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| OpenTelemetry | telemetry standards and SDKs | cross-runtime correlation |
| OpenInference | AI-specific semantic conventions/instrumentation | LLM/tool/retrieval spans |
| Langfuse | OSS tracing/evals/datasets | agent traces + evaluation store |
| Arize Phoenix | OSS observability/evaluation | tracing + experiments + evals |
| OpenLLMetry | OpenTelemetry-based LLM instrumentation | provider-neutral traces |
| TruLens | evaluation/feedback | evaluation primitives |

Telemetry is observation, not proof. Proof requires an explicit proposition and verification.

## I. Model/provider interchangeability

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| LiteLLM | provider/model gateway | normalized model invocation |
| vLLM | high-performance serving | self-hosted model execution |
| Ollama | local model runtime | local provider backend |
| llama.cpp | CPU/GPU local inference | portable local inference |
| SGLang | structured/high-throughput serving | production model serving |
| OpenRouter-compatible adapters | provider switching | external routing boundary |

Provider gateways belong below the authority layer.

## J. Evaluation / adversarial testing

| Project | Primary reusable surface | Candidate extraction |
|---|---|---|
| SWE-bench | real software task benchmark | agent evaluation harness |
| AgentBench-family projects | multi-domain agent evaluation | task/evaluation schema ideas |
| Inspect AI | evaluation framework | reproducible agent eval execution |
| Promptfoo | model/agent evaluation + red teaming | automated regression/attack matrix |
| Giskard | AI testing/evaluation | adversarial testing patterns |
| Garak | LLM vulnerability scanner | model/application probing |
| PyRIT | AI red-team automation | structured attack orchestration |

## K. Small protocol/tool activations

These are preferred as first extraction targets because they can be tested in isolation.

- Context7 MCP
- Playwright MCP
- GitHub MCP / native GitHub adapter
- OpenTelemetry/OpenInference instrumentation
- A2A Inspector
- A2A TCK
- AG-UI adapter
- ACP client/server bridge
- Browser Use CLI/library
- Stagehand Playwright integration
- OpenShell policy adapter

## Extraction policy

For each external candidate:

1. inspect source and current status;
2. capture exact repository/ref/release;
3. inspect license and dependency constraints;
4. identify one primitive, not the whole product;
5. define a minimal capability contract;
6. implement an adapter or isolated extraction;
7. run a positive test;
8. run a negative/kill test;
9. record evidence;
10. verify independently;
11. test removal.

## Acceptance states

CANDIDATE
INSPECTED
PROTOTYPED
EXPERIMENTALLY_SUPPORTED
INTEGRATED
REJECTED
FROZEN
UNKNOWN

## No vendor lock-in rule

External source code may provide implementation material.

External product semantics must not become the authority model.

The invariant is:

external project
  -> isolated capability
  -> capability contract
  -> evidence
  -> verification
  -> optional integration

## Source index

Agent runtimes:
- https://github.com/OpenHands/OpenHands
- https://github.com/OpenHands/software-agent-sdk
- https://github.com/letta-ai/letta
- https://github.com/langchain-ai/langgraph
- https://github.com/pydantic/pydantic-ai
- https://github.com/crewAIInc/crewAI
- https://github.com/agno-agi/agno
- https://github.com/QwenLM/Qwen-Agent
- https://github.com/huggingface/smolagents
- https://github.com/microsoft/autogen
- https://github.com/stanfordnlp/dspy
- https://github.com/Aider-AI/aider
- https://github.com/SWE-agent/mini-swe-agent
- https://github.com/SWE-agent/SWE-agent
- https://github.com/continuedev/continue

Sandbox/durable:
- https://github.com/NVIDIA/OpenShell
- https://github.com/temporalio/temporal
- https://github.com/triggerdotdev/trigger.dev
- https://github.com/hatchet-dev/hatchet
- https://github.com/PrefectHQ/prefect

Memory:
- https://github.com/Memory-Agents/graphiti
- https://github.com/mem0ai/mem0
- https://github.com/topoteretes/cognee
- https://github.com/letta-ai/letta

Browser:
- https://github.com/browser-use/browser-use
- https://github.com/microsoft/playwright-mcp
- https://github.com/browserbase/stagehand
- https://github.com/browser-use/browser-harness

Protocols:
- https://github.com/modelcontextprotocol/modelcontextprotocol
- https://github.com/a2aproject/A2A
- https://github.com/ag-ui-protocol/ag-ui
- https://github.com/agentclientprotocol

Observability:
- https://github.com/open-telemetry/opentelemetry-specification
- https://github.com/Arize-ai/openinference
- https://github.com/langfuse/langfuse
- https://github.com/Arize-ai/phoenix

Provider/model:
- https://github.com/BerriAI/litellm
- https://github.com/vllm-project/vllm
- https://github.com/ollama/ollama
- https://github.com/ggml-org/llama.cpp

Evaluation/security:
- https://github.com/UKGovernmentBEIS/inspect_ai
- https://github.com/promptfoo/promptfoo
- https://github.com/Giskard-AI/giskard-oss
- https://github.com/NVIDIA/garak
- https://github.com/Azure/PyRIT
- https://github.com/swe-bench/SWE-bench

## Verification warning

This is a research candidate catalog, not a legal or dependency clearance.

Before importing code, re-check:
- current repository state;
- exact license at the target revision;
- transitive licenses;
- security advisories;
- maintenance status;
- reproducibility;
- data/telemetry behavior;
- secrets handling.

Do not upgrade a candidate to INTEGRATED without a proof card.
