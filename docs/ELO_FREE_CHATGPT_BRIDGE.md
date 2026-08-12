# ELO Free ChatGPT Bridge

## Purpose

Provide a first real, zero-infrastructure-cost relationship between the ChatGPT side of the ELO workflow and the ELO repository.

## What this solves

The ChatGPT/GitHub integration can read the ELO repository. The ELO already has `ConversationIntake`, `KnowledgeAdmission` and `EvolutionMemory`, but the repository previously lacked a concrete transport/persistence boundary for an authorized conversation.

This design adds that boundary without creating a second Cognitive Core.

## Canonical flow

```text
ChatGPT
  |
  | authorized conversation event
  v
GitHub conversation inbox
  |
  v
GitHub Actions / bridge worker
  |
  v
ChatBridge -> ConversationIntake
  |
  v
KnowledgeAdmission
  |
  +--> REJECT / ARCHIVE
  |
  +--> Evolution Memory
  +--> Evidence / Knowledge / Decision through existing governed boundaries
```

## Cost model

The first implementation uses only repository storage and GitHub Actions available to the repository. It does not require a paid API server, database, vector store, or always-on runtime.

## Important boundary

This does **not** give repository code magical access to private ChatGPT history. A conversation must be explicitly authorized and serialized as a `ChatBridgeEvent`. In the current ChatGPT/GitHub workflow, the assistant can perform that handoff using the GitHub connector when the user authorizes it. A future Action/connector can automate the same contract without changing the Core.

## Event contract

The event is stored under:

`events/conversations/inbox/*.json`

Required fields:

- conversation_id
- tenant_id
- domain
- principal
- session_id
- request_id
- correlation_id
- source_id
- content
- authorized
- provenance

`source_type` identifies ChatGPT, Claude, Gemini or another approved provider.

## Retention

Conversation text is not canonical memory. Admission decides whether it is rejected, archived, retained as observation/evidence, or later promoted. Evolution Memory remains non-canonical and cannot alter ELO Soul automatically.

## Operational usage

1. Authorize a conversation for ELO learning.
2. Serialize the authorized conversation into the bridge event contract.
3. Persist the JSON event in the inbox.
4. GitHub Actions validates and runs the canonical intake.
5. Admitted experience is projected to `memory/evolution/`.
6. Future ELO queries can use the persisted records through a repository/memory adapter.

## Future provider integration

The bridge is provider-neutral. GPT, Claude and Gemini adapters can later be connected to `ProviderGateway` without changing ELO Soul, ConversationIntake, KnowledgeAdmission or the Cognitive Core.
