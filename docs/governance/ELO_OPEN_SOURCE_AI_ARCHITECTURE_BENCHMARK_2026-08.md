# ELO — Open-Source AI Architecture Benchmark — 2026-08

## Purpose

Provide a governed comparison of four open-source ecosystems named by ELO-125: Letta, Mem0, LiteLLM and LangGraph.

This document is **comparative evidence**, not a proposal to replace a canonical ELO component.

## Evaluation rule

An external project may be considered for ELO use only as an adapter, capability, library or implementation means. It does not become Cognitive/Core authority by adoption.

The comparison therefore evaluates:

- memory/state capability;
- routing/provider abstraction;
- durable execution;
- specialist/skill extensibility;
- observability/governance implications;
- fit with the existing ELO Cognitive/Core/Forge/Application/Infrastructure separation;
- migration risk and duplication risk.

## Evidence snapshot

### Letta

Official documentation describes Letta as a platform for stateful agents, with an open-source agent harness, memory, skills and a self-hostable runtime option.

**ELO interpretation:** strong candidate for experimental evaluation of stateful-agent and memory patterns. It must remain an external capability/adapter. Its agent harness must not become a second ELO Cognitive Core.

### Mem0

Official documentation describes Mem0 as a memory layer for LLM applications, with hosted and open-source/self-hosted options and integrations with multiple agent frameworks.

**ELO interpretation:** candidate for a bounded memory-component experiment, especially retrieval/long-term-memory patterns. It must not bypass ELO Temporal Memory, admission, provenance, authorization or promotion governance.

### LiteLLM

Official documentation describes LiteLLM as a unified interface/gateway for many LLM providers, with routing, retry/fallback, authentication/authorization, spend tracking and observability features.

**ELO interpretation:** strong candidate for provider-adapter/gateway experiments. It belongs below the ELO authority boundary as an infrastructure/application capability. It must not decide canonical ELO identity, evidence truth or governance outcomes.

### LangGraph

Official documentation describes LangGraph as a low-level orchestration runtime focused on durable execution, persistence, streaming and human-in-the-loop workflows. Its persistence model uses checkpoints and stores, and its execution model explicitly addresses retry/recovery and resumability.

**ELO interpretation:** strong candidate for workflow-runtime experiments. It may implement execution mechanics underneath an ELO-owned orchestration contract, but it must not become a second decision authority or redefine ELO lifecycle semantics.

## Comparative matrix

| Capability | Letta | Mem0 | LiteLLM | LangGraph | ELO relevance |
|---|---|---|---|---|---|
| Stateful agent runtime | Strong | Limited/indirect | No | Strong | Evaluate Letta/LangGraph |
| Long-term memory | Strong | Strong | No | Strong via Store integrations | Preserve ELO memory governance |
| Provider routing | Via model/provider configuration | Indirect | Strong | Through model integrations | Prefer adapter boundary |
| Durable workflow execution | Runtime-dependent | No primary focus | No | Strong | Evaluate LangGraph |
| Human-in-loop | Supported through agent workflows | Application-dependent | Gateway controls | First-class | Preserve ELO authorization boundary |
| Cost/provider controls | Not primary | Not primary | Strong | External/runtime dependent | LiteLLM is infrastructure candidate |
| Specialist skills/tools | Strong | Integrations | Proxy/hooks | Nodes/tools/subgraphs | Forge remains canonical specialist owner |
| Self-hosting | Supported | Supported | Supported | Open-source runtime | Positive for controlled experiments |
| Canonical ELO authority | **No** | **No** | **No** | **No** | Non-negotiable |

## Recommended experiments

### Experiment A — Provider gateway

Evaluate LiteLLM behind the existing provider/capability boundary for:

- provider routing;
- retry/fallback;
- cost accounting;
- unavailable-provider behavior;
- provenance preservation;
- tenant/domain/principal authorization.

**Decision gate:** no provider result may bypass ELO evidence/admission governance.

### Experiment B — Durable workflow runtime

Evaluate LangGraph as an implementation means for a bounded workflow behind the existing orchestration contract:

`Intent → Context → Evidence → Reasoning → Decision → Authorization → Execution → Monitoring`.

**Decision gate:** the runtime may execute the workflow but cannot redefine the canonical ELO lifecycle or decision authority.

### Experiment C — Memory component

Compare Mem0 and Letta memory patterns against the existing ELO Temporal Memory and governed promotion model.

**Decision gate:** external memory must not become a general-purpose accumulation bucket and must preserve provenance, authorization, tenant/domain scope, temporal validity and governed promotion.

### Experiment D — Stateful agent harness

Evaluate Letta for bounded specialist-agent experiments where Forge remains the owner of domain skill and Core remains the shared cognitive faculty.

**Decision gate:** removal of Letta must not remove ELO identity, Core reasoning contracts or canonical enterprise knowledge.

## Architectural decision

**No replacement is approved by this benchmark.**

The current ELO architecture remains canonical. The external projects are classified as potential means:

- **Letta:** candidate stateful-agent/skill runtime;
- **Mem0:** candidate memory component;
- **LiteLLM:** candidate provider gateway/router;
- **LangGraph:** candidate durable workflow runtime.

Any adoption requires a separate implementation proposal, repository inventory, compatibility/security review, executable evidence and Evolution Gate classification.

## Evidence sources

The benchmark uses the official documentation of each project as the primary external evidence source, reviewed in August 2026:

- Letta Documentation — stateful agents, memory, skills and self-hosted runtime.
- Mem0 Documentation — managed and open-source memory platform.
- LiteLLM Documentation — multi-provider gateway, routing, fallback, authentication, cost tracking and observability.
- LangGraph Documentation — durable execution, persistence/checkpointing, human-in-the-loop and fault-tolerant workflow execution.

## Status

`BENCHMARKED — NO CANONICAL REPLACEMENT`

The issue can be closed for the research/benchmark phase. Concrete integration remains optional and must be governed independently.