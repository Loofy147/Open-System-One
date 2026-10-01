# Agent Gap Map v0.1

Status: PREPARED
Date: 2026-09-30

## Objective

Cover direct, infrastructural, and indirect gaps around Open-System-One's external-agent integration without making any vendor runtime canonical.

## Layer 0 — Authority

Owned by Open-System-One.

Responsibilities:
- task and action contracts;
- run identity;
- policy decisions;
- evidence;
- verification;
- artifact lineage;
- claim/decision state;
- promotion and rollback.

No external product is allowed to become the source of truth for these records.

## Layer 1 — Agent surfaces

Purpose: execute goals.

Examples:
- OpenAI Dots
- Claude / Cowork
- Perplexity Computer
- Manus
- Cursor Cloud Agents
- GitHub Copilot Cloud Agent
- Devin

Question answered:
"What can an agent actually do for us?"

Primary gaps:
- persistence;
- computer access;
- application access;
- background execution;
- interruption;
- approval semantics;
- scope containment;
- action observability.

## Layer 2 — Agent runtimes / harnesses

Purpose: build or host agents independently of a product surface.

Examples:
- Letta / Letta Code
- OpenHands
- SWE-agent / mini-SWE-agent
- Pydantic AI
- LangGraph
- OpenClaw
- Gemini CLI
- goose

Question:
"What runtime do we own or control?"

This layer is where model interchangeability, state ownership, subagents, tool calls, and runtime composition can be tested.

## Layer 3 — Execution substrate / sandbox

Purpose: contain consequences.

Examples:
- NVIDIA OpenShell
- SWE-ReX / sandboxed coding environments
- container/VM based execution

Question:
"Where does agent code execute, and what can escape?"

Required characterization:
- filesystem boundary;
- network egress policy;
- credential boundary;
- process privileges;
- environment identity;
- logs;
- kill/stop path;
- recovery.

NVIDIA OpenShell is particularly relevant because it explicitly separates supervisor, sandbox, and agent-child trust levels and enforces policy at filesystem/network/process layers.

## Layer 4 — Durable execution

Purpose: survive failure, interruption, and long-running work.

Examples:
- Temporal
- Trigger.dev
- LangGraph persistence/checkpointing
- Pydantic AI durable execution integrations

Question:
"What survives a crash, retry, pause, or human approval?"

Required characterization:
- stable run identity;
- checkpoint semantics;
- retry behavior;
- idempotency;
- exactly-once vs at-least-once side effects;
- resume semantics;
- human approval pause;
- cancellation.

Important negative-space test:
A runtime that can resume state but can repeat external side effects is not sufficient by itself.

## Layer 5 — Memory / state

Purpose: long-lived context and historical recall.

Examples:
- Letta / MemFS
- Mem0
- Zep / Graphiti
- Cognee
- other verifiable/local memory substrates

Question:
"What is remembered, where, with what temporal semantics, and under whose authority?"

Required characterization:
- append vs mutable;
- temporal validity;
- source provenance;
- deletion;
- correction;
- conflict handling;
- cross-session identity;
- portability.

Memory must remain subordinate to Evidence/Claim authority. A remembered statement is not established merely because it persists.

## Layer 6 — Interoperability protocols

Purpose: connect independent runtimes without coupling their internals.

Examples:
- MCP — agent/tool/data boundary
- A2A — agent/agent boundary
- AG-UI — agent/user application boundary
- ACP — editor/agent boundary

These are complementary rather than interchangeable:
MCP connects agents to tools/data; A2A connects agents; AG-UI connects agents to user-facing applications; ACP connects coding agents to editors.

This layer should be the preferred location for portable adapters.

## Layer 7 — Browser / computer-use primitives

Purpose: make the agent capable of acting on real interfaces.

Examples:
- Playwright MCP
- Browser Use
- Stagehand

Question:
"Can we turn computer use into a controlled capability instead of an opaque superpower?"

Characterize:
- target selection;
- browser/session identity;
- credential persistence;
- action trace;
- screenshots/DOM evidence;
- deterministic fallbacks;
- recovery.

## Layer 8 — Observability / evaluation

Purpose: make agent behavior inspectable and testable.

Examples:
- Langfuse
- OpenInference / Phoenix
- LangSmith
- OpenTelemetry-based instrumentation

Question:
"Can we reconstruct what happened and independently evaluate it?"

Required:
- trace identity;
- tool spans;
- inputs/outputs;
- cost/usage;
- model/runtime identity;
- evaluation records;
- correlation to our run_id.

Do not equate telemetry with evidence. Telemetry is raw observation; evidence requires a declared proposition and verification.

## Layer 9 — Automation / scheduling

Purpose: connect agent work to external events and recurring execution.

Examples:
- n8n
- Activepieces
- Windmill
- Trigger.dev
- GitHub Actions

Question:
"What starts the run, and what guarantees that it does not become an uncontrolled loop?"

Characterize:
- trigger identity;
- schedule;
- retries;
- deduplication;
- cancellation;
- external-event provenance;
- secret scope.

## Layer 10 — Small activations

Small activations are deliberately narrow capability connectors, not systems.

Initial candidates:
- Context7 MCP — version-specific documentation retrieval
- Playwright MCP — browser execution
- GitHub MCP / native GitHub integration — repository actions
- filesystem MCP or equivalent sandboxed file capability
- Notion/Dropbox/Slack/Teams connectors where the source is explicitly authorized
- OpenInference instrumentation
- A2A inspector/TCK
- ACP client/agent bridge
- AG-UI HTTP/event bridge

Each activation gets its own proof card and can be enabled or removed independently.

## Direct gap coverage

### Goal execution
Use Dots / Claude / Perplexity / Manus characterization.

### Software engineering execution
Use Cursor / Copilot Cloud Agent / Devin / OpenHands / SWE-agent characterization.

### Local ownership
Use OpenClaw / Letta Code / Gemini CLI / goose characterization.

## Infrastructure gap coverage

- safety boundary: OpenShell;
- durable execution: Temporal / Trigger.dev / LangGraph;
- memory: Letta / Graphiti / Mem0;
- observability: OpenTelemetry + OpenInference + Langfuse/Phoenix;
- browser: Playwright MCP + Browser Use + Stagehand;
- interoperability: MCP + A2A + AG-UI + ACP.

## Indirect gap coverage

Indirect systems are those that increase reach, evidence quality, portability, or control without being the primary agent.

Examples:
- Context7 reduces stale-documentation errors;
- GitHub actions provide deterministic postconditions;
- browser harnesses expose UI actions as testable events;
- observability converts opaque runs into traceable executions;
- workflow engines provide cancellation/retry/scheduling;
- protocol bridges reduce vendor coupling.

## Existing internal assets

Relevant current portfolio projects already cover portions of these layers:

### Llms-mcp-android
Native mobile agent runtime/control plane. Its documented canonical path is:
Surface -> Activation/reasoning request -> Action -> Policy -> Approval -> Egress -> Run -> CapabilityInvocation -> CapabilityExecutor -> Observation -> Verification -> Evidence.

### m0-durable-run
Minimal durable Run/Evidence substrate with demonstrated same-run retry idempotency and process-restart persistence.

### Open-System-One
Typed decision substrate, replaceable model/runtime backends, research/evidence layer, and now external-agent characterization.

### Machine
Machine-native primitives and evidence/branch handling research.

### ACE-Agentic-Context-Engineering
Generator -> Reflector -> Curator loop, persistent playbook, self-healing/context evolution experiments. Treat existing claims as repository evidence that still require current verification before integration.

### Ai-evaluation-system
Real runtime causality/evidence methodology for controlled evaluation.

### Global-redteam / meta-secure-framework
Adversarial testing and self-hardening components that can provide negative tests for agent/tool boundaries.

### Rust-agents
Hierarchical orchestration prototype with replaceable LLM and tool traits.

### gemini-cli / context7
Existing portfolio anchors for a provider-agnostic CLI agent and version-specific documentation retrieval.

### Portfolio-Repository-Inventory
Cross-project provenance and relationship layer.

## Integration principle

Do not "merge everything".

Instead:

external capability
  -> narrow adapter
  -> capability contract
  -> receipt
  -> independent verification
  -> promote / reject

The reusable boundary is the evidence-backed capability, not the vendor product.

## Current open questions

1. Which agent surfaces expose enough action/event information to generate complete receipts?
2. Which runtimes guarantee or only approximate idempotency for side effects?
3. Which memory systems preserve temporal provenance rather than only recall?
4. Which sandbox runtimes enforce policy below the application layer?
5. Which protocols carry enough correlation metadata for end-to-end run reconstruction?
6. Can the same task execute through three different surfaces while producing equivalent evidence semantics?
7. Which small activations deliver a measurable reliability gain at low coupling cost?

## Promotion rule

A component is integrated only when:
- its boundary is explicit;
- its inputs/outputs are typed enough for the use case;
- its action scope is constrained;
- failures are observable;
- its output can enter our receipt/evidence chain;
- a kill test exists;
- removal does not corrupt the authority layer.
