# ELO Cognitive Architecture

## Purpose

This directory organizes the proposed cognitive-evolution architecture for ELO. It is a **reference and architectural proposal**, not an approval to implement every capability described here.

## Reading order

AI agents and human reviewers should read the repository governance and authority documents before this directory:

1. `AGENTS.md`
2. `ELO_REPOSITORY_NAVIGATION_RULES.md`
3. `ELO_ARTIFACT_METADATA_STANDARD.md` when adding or relocating artifacts
4. approved architecture baselines and ADRs
5. `01-meta-architecture/cognitive-architecture/README.md` — this orientation document
6. `ELO_COGNITIVE_EVOLUTION_ARCHITECTURE.md` — the detailed proposal
7. existing cognitive-platform, knowledge, data, governance, model, roadmap and implementation artifacts referenced by the proposal

The repository rules state that folder location is a navigation signal, not sufficient proof of authority, and that roadmap/proposal material has lower authority than approved architecture, ADRs, contracts and governance. Therefore this document must not be interpreted as silently changing the canonical architecture. fileciteturn36file0L2-L2

## Architectural intent

The proposal defines an evolutionary cognitive capability for ELO that connects:

**context → knowledge → evidence → reasoning → scenario analysis → recommendation → human decision → execution → observation → learning → replanning**

Its central concern is adaptive planning: when a master plan, production plan, capacity plan, purchasing plan, objective or operational condition changes, ELO should be able to understand the event, propagate impacts through dependencies and constraints, compare alternatives, support a governed decision, generate a coherent revised plan and monitor the outcome.

## What this document is not

It is not:

- an instruction to create a monolithic cognitive component;
- a replacement for the existing Cognitive Core;
- a new security boundary;
- a certification claim;
- an implementation specification for every proposed capability;
- permission to bypass existing contracts, governance, provenance, tenant isolation or the AI Gateway.

The existing repository rules explicitly require separation among Context, Knowledge, Memory, Evidence, Reasoning, Recommendation, Decision, Policy, Provenance, Agents, AI Gateway and Integration. fileciteturn29file0L2-L2

## How to interpret the detailed document

Each capability in `ELO_COGNITIVE_EVOLUTION_ARCHITECTURE.md` should be classified before implementation as one of:

- **REUSE** — an existing canonical capability already satisfies the need;
- **EXTEND** — an existing capability should be expanded;
- **NEW** — a genuinely new architectural capability is justified;
- **ROADMAP** — conceptually valid but not currently implementable within the approved phase;
- **DUPLICATE** — an equivalent artifact already exists;
- **CONFLICT** — the proposal conflicts with a higher-authority artifact and requires architectural resolution.

## Expected architectural reading

The detailed document should be read from left to right as a causal system, not as a list of independent modules:

**Business context**
→ **current state**
→ **expected state**
→ **deviation/event**
→ **causes and dependencies**
→ **impact and risk**
→ **scenarios and alternatives**
→ **decision support**
→ **replanning**
→ **execution**
→ **measurement**
→ **learning**
→ **next planning cycle**

This is the intended cognitive nervous system of the proposal.

## Relationship to existing ELO architecture

The proposal assumes that the Cognitive Core acts primarily as an orchestrator of cognitive capabilities rather than becoming a repository for all domain logic. The detailed architecture must therefore be reconciled with the existing Cognitive Core, Context, Knowledge, Memory, Reasoning, Decision Support, Provenance, Agent and Integration boundaries before implementation.

The current repository roadmap also establishes explicit execution gates from ELO-001 through ELO-013. A later capability must not be implemented as though an earlier gate were complete without explicit approval. fileciteturn29file0L2-L2

## Status

**PROPOSED / REFERENCE**

This status is intentional. The document describes an architectural target and analysis framework. Durable changes to canonical architecture require the repository's normal architecture-review and ADR process.
