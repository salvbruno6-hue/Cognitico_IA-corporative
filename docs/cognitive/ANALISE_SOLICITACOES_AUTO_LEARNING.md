# ELO — Automated Learning from Análise de Solicitações

## Objective

Create a governed, incremental pipeline that transforms authorized conversations from the Análise de Solicitações domain into structured context, evidence, experience and learning, without treating raw chats as corporate truth.

## Canonical flow

```text
AUTHORIZED CONVERSATION EVENT
        ↓
ADMISSION / POLICY CHECK
        ↓
CONVERSATION SCOPE
        ↓
SO/LIC IDENTIFICATION
        ↓
NORMALIZATION
        ↓
EVENT EXTRACTION
        ↓
EVIDENCE + DECISIONS + QUESTIONS + ANSWERS
        ↓
EXPERIENCE CANDIDATE
        ↓
EVOLUTION MEMORY
        ↓
PATTERN / RECURRENCE ANALYSIS
        ↓
LEARNING CANDIDATE
        ↓
VALIDATION
        ↓
PUBLISHED KNOWLEDGE / PRECEDENT / RULE
```

## Core rule

A client-specific answer or one-off technical solution is initially a PRECEDENT, never an automatic global rule.

```text
OBSERVATION
→ EVIDENCE
→ PRECEDENT
→ RECURRENCE / VALIDATION
→ LEARNING CANDIDATE
→ APPROVED KNOWLEDGE
→ ELO RULE (only when explicitly approved)
```

## Incremental learning

The system must learn while a solicitation is being analyzed, not only after closure.

On each authorized conversation update:
1. resolve or create solicitation scope;
2. extract new facts, questions, answers, decisions and technical equivalences;
3. compare with the existing solicitation context;
4. update the Evolution Memory projection idempotently;
5. emit learning candidates only when new evidence or decisions justify them.

On solicitation closure:
- consolidate the complete context;
- build an Experience Case candidate;
- reconcile questions and official answers;
- reconcile TR requirements to budget evidence when available;
- calculate recurrence and reusable-learning candidates.

## Weekly consolidation

Run a weekly job over recently admitted solicitation events since the previous successful run.

Aggregate by:
- family;
- model;
- client;
- solution;
- occurrence;
- requirement;
- question;
- answer;
- risk;
- decision;
- outcome.

Detect:
- recurring questions;
- recurring technical equivalences;
- recurring risks;
- recurring scope ambiguities;
- family/model recurrence;
- change in recurring patterns;
- candidates for reusable knowledge.

Do not silently rewrite authoritative documents.

## Data classes

- `RAW_CONVERSATION`
- `EXTRACTED_FACT`
- `INTERPRETATION`
- `DECISION`
- `QUESTION`
- `OFFICIAL_ANSWER`
- `PRECEDENT`
- `EXPERIENCE_CASE`
- `LEARNING_CANDIDATE`
- `VALIDATED_LEARNING`
- `ELO_RULE`

## Minimum Experience Case

```yaml
experience_case:
  experience_id:
  solicitation_id:
  tenant_id:
  domain: ANALISE_SOLICITACOES
  problem:
  context:
  requirements: []
  constraints: []
  questions: []
  official_answers: []
  alternatives: []
  selected_solution:
  budget_effect:
  decision:
  outcome:
  lessons_learned: []
  applicable_conditions: []
  non_applicable_conditions: []
  provenance: {}
  validation_status:
```

## Learning candidate contract

```yaml
learning_candidate:
  learning_id:
  solicitation_ids: []
  category:
  statement:
  evidence_refs: []
  recurrence_count:
  distinct_clients:
  accepted_count:
  rejected_count:
  impact:
  applicability:
  exceptions: []
  confidence:
  validation_status:
  provenance: {}
```

## Provenance requirements

Every extracted learning item must retain:
- conversation/source identifier;
- solicitation identifier;
- source type;
- timestamp;
- tenant/domain;
- original evidence reference;
- transformation step;
- validation status;
- confidence where applicable.

## Architecture alignment

This capability must reuse the repository's existing conversation bridge and Evolution Memory mechanisms rather than introduce a second persistence path.

Expected boundaries:
- Conversation Bridge: authorized event intake;
- Conversation Intake / Knowledge Admission: admissibility and policy controls;
- Context Resolution: solicitation/context identity;
- Evolution Memory: admitted learning projection;
- Reasoning: hypotheses and recurrence interpretation;
- Decision Memory: decision capture where applicable;
- Provenance: traceability;
- Cognitive Core: orchestration.

Do not introduce a monolithic solicitation-learning engine when existing capabilities can be composed.

## Automation triggers

### Trigger A — conversation update
A new authorized conversation event for an in-scope solicitation starts incremental processing.

### Trigger B — solicitation closure
Closure triggers Experience Case consolidation and final learning-candidate extraction.

### Trigger C — weekly learning consolidation
Scheduled consolidation compares recently admitted solicitation records with historical memory and ranks learning candidates.

## Non-goals

This capability does not authorize:
- autonomous contract decisions;
- automatic replacement of TR requirements;
- automatic pricing changes outside the budgeting workflow;
- personnel judgments;
- cross-tenant learning without policy authorization;
- publication of an ELO rule without validation.

## Acceptance criteria

- authorized solicitation events can be ingested;
- solicitation scope is resolved;
- idempotent memory projection exists;
- incremental extraction works;
- closure produces an Experience Case candidate;
- weekly consolidation exists;
- precedents remain separate from rules;
- provenance is preserved;
- tests cover duplicate events, missing SO identity, conflicting answers and rejected admissions.
