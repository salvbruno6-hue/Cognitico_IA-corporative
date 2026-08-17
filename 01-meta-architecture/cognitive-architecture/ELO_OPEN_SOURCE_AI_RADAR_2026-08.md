# ELO Open-Source AI Architecture Radar — 2026-08

## Purpose

Identify free/open-source GitHub projects whose architecture can increase ELO capability, agility, autonomy, memory, routing, execution, inference or verification.

This radar evaluates reusable architectural ideas and components. It does not authorize blind adoption.

## Current shortlist

| Project | Primary capability | License | ELO relevance | Decision |
|---|---|---|---|---|
| LangGraph | Stateful/graph-based agent orchestration | MIT | High for explicit state transitions, checkpoints and durable workflows | STUDY / ADAPT |
| CrewAI | Multi-agent crews and event-driven Flows | MIT | High for specialist collaboration and event-driven orchestration | STUDY / EXPERIMENT |
| Letta | Stateful agents and long-term memory | Apache-2.0 | Very high for persistent agent state and memory architecture | STUDY / EXPERIMENT |
| Mem0 | Long-term memory layer, retrieval and memory evaluation | Apache-2.0 | Very high for memory extraction/retrieval patterns | EXPERIMENT |
| OpenHands | Open-source coding/software agent | MIT for core; enterprise directory has separate license | High for autonomous engineering execution and sandboxed coding workflows | STUDY / ADAPT |
| Aider | Codebase mapping, terminal coding agent and Git integration | Apache-2.0 | High for repository-aware coding and change loops | STUDY / ADAPT |
| vLLM | High-throughput, memory-efficient inference/serving | Apache-2.0 | High if ELO operates self-hosted/open models | STUDY / EXPERIMENT |
| llama.cpp | Local inference, GGUF, OpenAI-compatible server | MIT | High for local/offline model execution and lightweight fallback | STUDY / EXPERIMENT |
| LiteLLM | AI gateway, provider abstraction, routing, fallbacks and logging | MIT | Very high for model/provider routing and AI Gateway | STUDY / ADAPT |

## Evidence notes

### LangGraph

GitHub describes LangGraph as a framework for building resilient agents and reports an MIT license. Its graph model is useful to ELO because cognitive steps can be represented as explicit state transitions, conditional routing and checkpoints rather than hidden control flow. citehttps://github.com/langchain-ai/langgraph

### CrewAI

CrewAI is an MIT-licensed multi-agent framework. Its current architecture separates Crews for autonomous collaboration from Flows for production/event-driven orchestration. This is relevant to ELO's specialist and governed execution model. citehttps://github.com/crewAIInc/crewAI

### Letta

Letta is an open-source, model-agnostic framework for stateful agents with advanced reasoning and transparent long-term memory. The repository is Apache-2.0. This is one of the strongest candidates for studying persistent agent state and memory boundaries. citehttps://github.com/letta-ai/letta

### Mem0

Mem0 describes itself as a universal memory layer for AI agents and is Apache-2.0. Its current repository includes memory extraction/retrieval infrastructure and a separate memory-benchmarks project. It is relevant to ELO's existing memory/evidence architecture, but should be benchmarked against the canonical ELO memory model rather than copied. citeturn1search6turn1search4

### OpenHands

OpenHands is an open-source software-development agent platform. Its repository states that the core and agent-server are MIT-licensed, while the enterprise directory has a separate license. Its agent can modify code, run commands, browse and call APIs. This makes it useful as an execution-pattern reference, not as a replacement for ELO governance. citeturn1search15turn0search4

### Aider

Aider is an open-source terminal pair-programming tool that maps the codebase and integrates with Git. Its architecture is useful for studying repository-aware coding loops and small, auditable change sets. citeturn0search12

### vLLM

vLLM is an Apache-2.0 inference and serving engine focused on high-throughput and memory-efficient LLM serving. It is relevant if ELO needs a self-hosted model execution tier. citeturn1search11

### llama.cpp

llama.cpp provides local LLM inference in C/C++, supports GGUF models and an OpenAI-compatible server, and distributes prebuilt binaries. It is useful as a lightweight local/offline execution fallback. citeturn0search13

### LiteLLM

LiteLLM provides an AI gateway abstraction across many model providers with cost tracking, guardrails, load balancing and logging. Its repository is actively maintained. It is highly relevant to the ELO model-routing/AI-Gateway concept, but ELO governance must remain above the gateway. citeturn1search1

## Priority for ELO

### Tier A — investigate first

1. Letta — persistent agent state and memory architecture.
2. Mem0 — memory extraction/retrieval and evaluation patterns.
3. LiteLLM — model/provider routing and gateway patterns.
4. LangGraph — durable state-machine/graph execution patterns.

### Tier B — execution acceleration

5. OpenHands — autonomous coding agent patterns.
6. Aider — repository mapping and Git-aware coding patterns.
7. vLLM — self-hosted inference tier.
8. llama.cpp — lightweight local inference fallback.
9. CrewAI — multi-specialist orchestration patterns.

## What ELO should extract

Do not ask only whether a project should be installed. Ask:

- What architectural mechanism creates its advantage?
- Can ELO reproduce that mechanism without adopting the project?
- Can the mechanism extend an existing ELO capability?
- Does it create a new specialist, memory layer, router, execution tier or validation mechanism?
- Does it reduce latency, cost or context pressure?
- Does it increase autonomous work duration?
- Does it improve recoverability after failure?
- Does it improve evidence and auditability?
- Does it introduce a new dependency or security boundary?

## Proposed experiment queue

### ELO-OSS-001 — Memory comparison

Compare ELO's canonical memory approach with Letta and Mem0 patterns using the same representative tasks. Measure recall, precision, stale-memory behavior, provenance, latency, token use and correction behavior.

### ELO-OSS-002 — Model routing

Prototype a routing layer inspired by LiteLLM. Route coding, reasoning, extraction and fast-response tasks to different model classes. Measure quality, cost, latency and failure recovery.

### ELO-OSS-003 — Durable cognitive graph

Prototype explicit ELO state transitions using graph/checkpoint patterns inspired by LangGraph, without replacing the ELO Cognitive Core.

### ELO-OSS-004 — Autonomous coding sandbox

Compare Codex/ELO execution with OpenHands/Aider patterns for repository mapping, tool use, test execution, correction and Git evidence.

### ELO-OSS-005 — Local inference tier

Evaluate llama.cpp and vLLM as possible local/fallback execution layers for open-weight models. Measure hardware requirements, latency, concurrency, quality and operational cost.

### ELO-OSS-006 — Specialist collaboration

Compare ELO's specialist orchestration with CrewAI-style crew/flow patterns. Preserve ELO's governance and decision authority.

## License rule

"Free to download" does not mean "unconditionally free to use in every context". Before incorporation, ELO must check the repository license, model-weight license, dataset license, dependencies, commercial restrictions, attribution requirements and any separate enterprise directories or components.

## Decision rule

No external project becomes canonical merely because it is popular, has many stars, claims a larger context window, or benchmarks well.

Promotion requires:

1. primary-source evidence;
2. license review;
3. architecture extraction;
4. reproducible experiment;
5. comparison against ELO baseline;
6. security/privacy review;
7. rollback path;
8. ELO decision and traceability.

## Immediate conclusion

The strongest architectural opportunities are not a single new model. They are the combination of:

```text
Persistent memory
+
Explicit durable state
+
Model/provider routing
+
Autonomous execution
+
Specialist collaboration
+
Local/fallback inference
+
Evidence-driven verification
```

That combination can increase ELO's agility while keeping the ELO Cognitive Core as the canonical decision authority.
