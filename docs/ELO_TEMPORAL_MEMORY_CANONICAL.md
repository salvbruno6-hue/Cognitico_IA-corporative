# ELO Temporal Conversation Memory — Canonical

## Purpose

Temporal Conversation Memory is the mandatory session-scoped working layer for an authorized ELO consulting conversation.

When the `elo` trigger is activated, the current authorized conversation becomes temporal context. Information obtained by ELO from GPT, Claude, Gemini, GitHub, documents, or other authorized providers during that investigation is also temporal context first.

## Invariants

1. Temporal memory is not canonical identity.
2. Temporal memory is not Evolution Memory.
3. External provider output is never permanent merely because it was returned.
4. Every retained temporal record requires authorization and provenance.
5. Temporal context may contain facts, hypotheses, analyses, alternatives, evidence candidates, provider responses and provisional decisions.
6. Promotion requires explicit admission/governance after analysis.
7. ELO Soul cannot be changed by temporal content.
8. Temporal memory is tenant/domain/session scoped and must not cross those boundaries.

## Lifecycle

```text
`elo` trigger
  -> temporal conversation
  -> internal lookup
  -> external consultation when needed
  -> provider response enters temporal memory
  -> analysis / comparison / evidence assessment
  -> promotion decision
  -> Evolution Memory / Evidence / Knowledge / Decision
  -> canonical architectural change only through governance
```

## Provider rule

When internal ELO knowledge is insufficient, an authorized provider may be consulted. The provider response must enter the same temporal session with provenance identifying the provider and request. The provider is an information source, not an authority over ELO identity.

## Retention rule

At session completion, temporal material is either expired/archived or explicitly promoted. No automatic promotion to Evolution Memory occurs solely because content was useful during the session.

## Example

For `Multiteiner`: ELO may consult GPT because internal knowledge is insufficient. The GPT response, sources and analysis remain in Temporal Memory. Only after an admission/promotion decision does selected information become Evolution Memory, Evidence, Knowledge or Decision.
