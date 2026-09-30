# Agent Surface Registry v0.1

Status: PREPARED_FOR_CHARACTERIZATION
Date: 2026-09-30

## Purpose

Track external agent products and runtimes that may become execution surfaces for Open-System-One.

The registry does not rank products. It classifies observable architecture and defines what must be characterized before integration.

## Common boundary

Open-System-One remains the durable authority for:
- task/decision contracts;
- claims and evidence;
- experiments and verification;
- artifacts and lineage;
- run identity;
- promotion and rollback decisions.

An external agent surface is an executor.

## Registry

| Surface | Class | Execution substrate | Persistence | Connected tools | Computer/local access | Background work | Primary characterization |
|---|---|---|---|---|---|---|---|
| OpenAI Dots | general agent | cloud agent + cloud computer | ongoing | connected apps | cloud; exact local boundary to observe | documented | authority boundary, persistence, approvals, provenance |
| Claude | agent/work workspace | cloud sessions + desktop VM/local bridge | sessions/projects/scheduled work | connectors, skills/plugins | desktop/local + cloud | documented | local/cloud separation, computer use, scheduled work |
| Perplexity Computer | general digital worker | cloud computer + subagents | long-running; recurring | Gmail, Slack, Notion, Calendar and many others | cloud; Personal Computer adds local machine path | documented | orchestration, subagents, model switching, persistence |
| Microsoft 365 Copilot Cowork | enterprise workspace agent | cloud | long-running/scheduled | M365 + plugins/connectors | Edge/browser; enterprise-controlled | documented | Work IQ grounding, governance, multi-model execution |
| Manus | general agent | persistent cloud VM | persistent cloud computer | integrations/tools | local and cloud variants | documented | persistent VM, credentials, local boundary, recovery |
| Cursor Cloud Agents | coding agent | isolated cloud VM | agent/session/branch | code tools + remote desktop | local/cloud handoff | background | VM isolation, artifact evidence, branch/diff/test loop |
| GitHub Copilot Cloud Agent | coding agent | GitHub-hosted cloud development environment | async session + repo history | GitHub tools/actions | cloud | background | repository authority, branch/PR boundary, tool trace |
| Devin | coding agent | cloud development environment + desktop/macOS variants | ongoing workspaces | plugins/MCP/subagents | cloud; macOS support | background | agentic software loop, environment identity, verification |
| OpenClaw | local/open-source agent runtime | local gateway + agent runtime | local state/memory | many channels/plugins/models | native local | daemon/background | user-owned control plane, policy, model interchangeability |
| Gemini computer use / Agent Platform | developer agent surface | model/tool platform | application-defined | browser/desktop/mobile tools; enterprise integrations | application-defined | application-defined | capability API, orchestration, governance, reproducibility |

## Evidence classes

For each surface distinguish:

PRODUCT_FACT
- supported by current vendor documentation.

OBSERVED
- directly observed in an account/runtime.

EXPERIMENTALLY_SUPPORTED
- observed under a declared test with reproducible evidence.

INFERENCE
- architectural interpretation derived from observed behavior.

UNKNOWN
- not directly established.

## Integration rule

Never add a product-specific dependency to the Open-System-One authority layer merely because a product exposes a convenient memory, project, or task history.

The integration boundary should remain:

AgentSurface
  -> Task Contract
  -> Execution
  -> Observation
  -> Receipt
  -> Independent Verification

## Characterization priorities

Priority here means test-order value, not product quality.

### Lane A — general persistent agents

- OpenAI Dots
- Claude
- Perplexity Computer
- Manus

Shared questions:
- persistence;
- background execution;
- connected app scope;
- approval gates;
- cloud/local boundary;
- task interruption;
- evidence reconstruction.

### Lane B — enterprise/workspace agents

- Microsoft 365 Copilot Cowork
- Gemini Enterprise Agent Platform

Shared questions:
- organization trust boundary;
- delegated permissions;
- connectors;
- governance;
- model selection;
- retention/audit;
- policy inheritance.

### Lane C — software-engineering agents

- Cursor Cloud Agents
- GitHub Copilot Cloud Agent
- Devin

Shared questions:
- repository identity;
- branch isolation;
- environment reproducibility;
- tool traces;
- test execution;
- artifact evidence;
- merge/PR authority;
- rollback.

### Lane D — user-owned/local runtime

- OpenClaw

Shared questions:
- who owns state and credentials;
- policy enforcement location;
- model interchangeability;
- plugin/MCP trust;
- local process isolation;
- daemon persistence;
- recoverability and backup.

## Common first-run gate

For every surface:

1. identity/access;
2. read-only observation;
3. untrusted-content/prompt-injection kill test;
4. scope containment;
5. evidence-fidelity test;
6. reversible mutation;
7. approval-boundary test;
8. stop/interruption test;
9. receipt completeness;
10. independent verification.

No surface enters normal Open-System-One workflows until the applicable gate passes.

## Sources checked 2026-09-30

OpenAI Dots:
https://chatgpt.com/features/dots/
https://help.openai.com/en/articles/20001530-getting-started-with-your-dot

Claude:
https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork

Perplexity Computer:
https://www.perplexity.ai/products/computer

Microsoft 365 Copilot Cowork:
https://www.microsoft.com/en-us/copilot/features/cowork
https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/whats-new

Manus:
https://help.manus.im/en/articles/15392111-what-is-the-cloud-computer
https://help.manus.im/en/articles/14178443-what-is-the-my-computer-feature-capable-of

Cursor:
https://cursor.com/cloud
https://prod.cursor.com/blog/agent-computer-use

GitHub Copilot Cloud Agent:
https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/

Devin:
https://devin.ai/blog/bringing-macos-to-devin
https://devin.ai/blog/governing-ai-agents-at-scale-with-blackrock

OpenClaw:
https://github.com/openclaw/openclaw
https://github.com/openclaw/openclaw/blob/main/docs/concepts/agent.md

Google Gemini:
https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/
https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-enterprise-agent-platform/
