# ELO External Entity + AI Relationship Architecture

## Purpose

This document defines how ELO establishes a real, governed relationship with external companies/entities and external AI providers.

The canonical example is:

> "What does ELO know about Multiteiner?"

Multiteiner is treated as an external company/entity, not as the technical concept of multi-tenancy.

## Core principle

ELO does not need to know every external entity before a consultation. It must know how to determine what it already knows, detect knowledge gaps, consult an authorized provider, preserve provenance, distinguish external claims from validated ELO knowledge, and retain only what policy permits.

## Flow

```text
User question
  -> Entity resolution
  -> ELO internal Knowledge/Evidence/Memory lookup
  -> Sufficiency check
  -> if insufficient and authorized: Provider Gateway
  -> GPT / Claude / Gemini / other approved provider
  -> provenance + source attribution
  -> contradiction detection
  -> Knowledge Admission
  -> Evolution Memory / Evidence / Knowledge / Decision
  -> Consultant response
```

## Internal-first rule

External consultation is a fallback, not the default source of truth.

1. Search canonical identity and current ELO state when relevant.
2. Search entity knowledge.
3. Search evidence.
4. Search organizational memory.
5. Search evolution memory for historical context.
6. Decide whether evidence is sufficient.
7. Consult an external provider only when authorized and necessary.

## Provider independence

GPT, Claude, Gemini and future providers implement the same provider boundary. The ELO Core does not depend on a specific vendor.

Providers are connectors/adapters, not Cognitive Cores.

## Consultant behavior

The ELO must answer as a consultant:

- objective;
- context;
- facts;
- evidence;
- assumptions;
- analysis;
- alternatives;
- risks;
- recommendation when justified;
- decision required;
- next actions;
- provenance;
- uncertainty.

It must distinguish facts from inference and recommendation from decision.

## Retention

A provider response does not automatically become knowledge.

Authorized external results pass through Knowledge Admission. Non-canonical useful experience is retained in Evolution Memory. Validated durable information may later be promoted into Organizational Memory. Architectural changes require a separate governance gate and cannot be performed by provider output.

## Relationship lifecycle

```text
Unknown entity
  -> Discovered entity
  -> Externally described
  -> Evidence collected
  -> Contextualized to tenant/domain
  -> Candidate knowledge
  -> Validated knowledge
  -> Organizational relationship
  -> Decisions
  -> Outcomes
  -> Lessons learned
```

This lifecycle allows ELO to build a progressively richer relationship with a company without contaminating the canonical identity of ELO.

## Failure behavior

If no provider is configured or all providers fail, ELO must not invent facts. It returns `INSUFFICIENT_EVIDENCE`, identifies the gap, and preserves the request/provenance when retention is authorized.

## Isolation

Every request carries tenant/domain/principal/session/request/correlation context. External knowledge must never cross tenant boundaries merely because a provider returned it.

## Security and trust

Provider output is untrusted input until admitted. The system must preserve source attribution, provider identity, request identity, and evidence references. Contradictory sources remain contradictory until resolved by evidence, policy, or authorized decision.
