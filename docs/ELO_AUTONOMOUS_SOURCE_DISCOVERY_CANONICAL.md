# ELO Autonomous Source Discovery — Canonical

## Purpose

The user must not be required to specify repository paths, project folders, document names or provider routes for ordinary consulting requests. ELO interprets the question, derives intent and entities, creates a source-neutral discovery plan, and asks authorized adapters to retrieve relevant information.

## Canonical lifecycle

```text
User question
  -> Intent / entity resolution
  -> inspect ELO temporal + permanent knowledge
  -> autonomous source discovery
  -> authorized source adapters
       - ELO memory
       - GitHub
       - ChatGPT Projects (when an authorized connector exists)
       - documents
       - web
       - GPT / Claude / Gemini
  -> retrieved material enters Temporal Conversation Memory
  -> provenance + evidence assessment
  -> consultant analysis
  -> explicit admission/promotion decision
  -> Evolution Memory / Evidence / Knowledge / Decision
```

## Provider role

GPT or another model may act as an interpreter/reasoner for intent and source selection and may provide external information. It is not the authority for ELO identity or permanent truth. Provider output enters temporal memory first.

## Access rule

Semantic discovery does not bypass permissions. If a candidate source is not connected or the current principal is not authorized, ELO must report the access gap and continue with available sources rather than fabricate retrieval.

## No hard-coded user paths

The ELO contract is semantic: users say what they need, not where the information lives. Source paths, project names and document locations are implementation details of authorized adapters and indexes.

## Temporal rule

Every retrieved external result used during an active investigation is temporary context first. It is never promoted to Evolution Memory merely because it was found or returned by an AI provider.

## Example

For `"elo, analise a Multiteiner como possível cliente"`, ELO should infer an external-entity/commercial-analysis intent, search its own memory and GitHub, use connected ChatGPT Project/document sources if available, consult web or an AI provider when necessary, and combine the results in temporal memory before producing a recommendation.
