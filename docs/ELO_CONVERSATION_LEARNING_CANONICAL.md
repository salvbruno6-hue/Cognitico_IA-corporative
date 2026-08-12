# ELO Conversation Learning — Canonical Contract

## Purpose

This document defines the canonical operational boundary for authorized conversations between ELO and external AI providers such as ChatGPT, Claude, Gemini and future providers.

## Core principle

Conversation is experience, not identity. An authorized conversation may contribute to ELO evolution, but conversation content cannot directly modify ELO Soul, canonical architecture or canonical contracts.

## Canonical flow

```text
Conversation
  -> Context
  -> Authorization
  -> Admission
  -> Classification
  -> Provenance
  -> Evolution Memory / Evidence / Knowledge / Decision
  -> Promotion Gate
  -> Canonical change only through explicit governance
```

## Provider independence

Providers are connectors. No provider creates a second Cognitive Core or becomes the authority for ELO identity.

The exchange is bidirectional when authorized:

```text
ELO -> provider: authorized context + question
provider -> ELO: analysis / observation / evidence / proposal
ELO -> admission: classify + preserve provenance
```

## Selective retention

The full conversation is not automatically canonical memory. Relevant authorized material can remain in Evolution Memory as a queryable historical record. Evidence, validated knowledge, decisions and lessons can be promoted through their existing governed boundaries.

## Required context

Every ConversationEvent carries tenant, domain, principal, session, request and correlation identifiers. Provenance must identify the provider/source and origin of the information.

## Example

A conversation about using autonomous contractors rather than employees can contain extensive research and alternatives. The ELO may retain the conversation-derived analysis in Evolution Memory, while only verified evidence, the approved contractual decision and reusable lessons are promoted to Organizational Memory.

## Security and identity

Unauthorized conversations are rejected. Cross-tenant or cross-domain leakage is not permitted. No conversation-derived record can silently alter ELO Soul.

## Implementation boundary

`src/elo/core/conversation_intake.py` is the canonical intake boundary and delegates retention classification to the existing `KnowledgeAdmission` contract and storage to `EvolutionMemory`. It does not create a parallel memory or cognitive core.
