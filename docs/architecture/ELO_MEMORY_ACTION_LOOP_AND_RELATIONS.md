# ELO — Memory, Relations and Action Loop

## 1. Canonical database reference

The official persistence reference for this architecture is the Supabase project **Elo-forge** (`fxbpevjrkwhbicpmecow`).

This document does not introduce a second memory database. It describes how the existing Elo-forge tables compose into a governed cognitive loop.

## 2. Core distinction

ELO must distinguish four different things:

1. **Knowledge** — what is institutionally known or governed.
2. **Experience** — what happened, including input, actions, decisions, verification, result, errors and corrections.
3. **Relations** — how experiences, concepts, patterns, specializations and decisions are connected.
4. **Action execution** — what ELO/Hermes actually executed and what evidence resulted.

Persistence of an experience is not promotion to knowledge.

## 3. Memory-to-action loop

```text
REQUEST
  ↓
INTENT / CONTEXT
  ↓
CONTEXT ASSEMBLY
  ↓
KNOWLEDGE + EXPERIENCE + RELATIONS
  ↓
COGNITIVE INTERPRETATION
  ↓
DECISION / ROUTING
  ↓
ACTION PLAN
  ↓
HERMES / OPERATIONAL EXECUTION
  ↓
EVIDENCE + RESULT + ERRORS + CORRECTIONS
  ↓
EXPERIENCE RECORD
  ↓
EXTRACTION / ASSOCIATION
  ↓
CONCEPT / REASONING PATTERN / SPECIALIZATION CANDIDATE
  ↓
GOVERNANCE + EVOLUTION GATE
  ↓
VALIDATED LEARNING
  ↓
NEXT CONTEXT ASSEMBLY
```

The loop is continuous, but the learning transition is gated.

## 4. Verified Elo-forge relational backbone

### Experience

`elo_experience_records` is the canonical English experience record used by the cognitive architecture.

It already contains the fields required to preserve the action loop: `input_structure`, `decomposition`, `sequence_steps`, `dependencies`, `capability_ids`, `knowledge_ids`, `decisions`, `verification`, `result`, `errors`, `corrections`, `extracted_patterns`, `extracted_knowledge`, and promotion/validation state.

Its declared relations include experience level references and links through `elo_experience_pattern_links` to `elo_reasoning_patterns`.

### Learning pipeline

The Portuguese learning model is explicitly relational:

```text
elo_aprendizado_fontes
        ↓
elo_aprendizado_extracoes
        ↓
elo_aprendizado_experiencias
        ↓
elo_aprendizado_conceitos
        ↓
elo_aprendizado_padroes_raciocinio
        ↓
elo_aprendizado_especializacoes
```

`elo_aprendizado_relacoes` is the typed relationship fabric for learning entities. It is polymorphic (`origem_tipo/origem_id → destino_tipo/destino_id`) and therefore must be treated as a governed graph edge rather than pretending every edge is a physical PostgreSQL foreign key.

### Canonical knowledge

```text
elo_conhecimento_nucleos
        ↓
elo_conhecimento_itens
        ↓
elo_conhecimento_vinculos
```

Routing is defined through `elo_conhecimento_regras_routing`, while sources are registered in `elo_conhecimento_fontes`.

This layer remains the institutional/canonical knowledge boundary. Learning records do not become canonical merely because they exist.

### Evolution

`elo_evolution_events` connects governed evolution evidence to source experiences, reasoning patterns, target specializations and experience levels.

Therefore the intended promotion direction is:

`experience → pattern/learning evidence → evolution event → specialization/validated learning → Core when explicitly justified`.

### Orçamento

The verified budget path is:

```text
elo_orcamentos
   ↓
elo_orcamento_memoria
   ↓
elo_orcamento_calculos_aprendidos
   ├── elo_orcamento_calculo_evidencias
   └── elo_orcamento_calculo_similaridades
   ↓
elo_orcamento_associacoes
   ↓
elo_orcamento_decisoes
```

`elo_orcamento_decisoes.arbitrado_por` and `elo_orcamento_associacoes.decisoes_arbitradas` provide the arbitration signal that must be preserved when a budget experience becomes a learning candidate.

`elo_orcamento_calculos_aprendidos` also references `elo_orcamento_memoria`, `elo_orcamento_calculo_varreduras` and `elo_orcamentos` through declared foreign keys.

## 5. Action-loop persistence

Operational execution history is separated from learning memory:

```text
elo_automation_registry → elo_automation_runs
elo_aprendizado_automacoes → elo_aprendizado_automacao_execucoes
```

The first pair represents the general automation runtime. The second pair represents learning-oriented automation. Neither table pair is itself the learning authority.

`elo_audit_log` provides a correlation/entity-oriented audit trail. It should be used to connect an operational event to the responsible actor, operation and entity without copying the entire experience into the audit record.

## 6. Context assembly rule

The context assembler remains a composition boundary over `KnowledgeOrchestrator`. It must not become a second retrieval/planning authority.

Recommended order:

1. Soul/Core invariants
2. governed canonical knowledge
3. current operational context
4. domain-specific memory
5. experience records
6. reasoning patterns
7. validated learning candidates
8. prior decisions/arbitration
9. evidence
10. explicit gaps/uncertainties

Unknown requirements must remain unresolved. The assembler must never invent a table, rule or relation to fill a gap.

## 7. Relationship rules

### Physical foreign keys

Use PostgreSQL foreign keys for stable, typed ownership relationships. The verified Elo-forge schema already provides these for domains, specializations, concepts, experiences, patterns, evolution, identity, authorization, automation and the main budget chain.

### Polymorphic learning graph

`elo_aprendizado_relacoes` remains the graph edge for cross-entity learning relations. Its `origem_tipo/origem_id` and `destino_tipo/destino_id` must be validated by the application/governance layer because PostgreSQL cannot enforce a conventional FK against multiple target tables.

### No duplicated relation engines

Do not create another generic relation table for the same learning graph. Do not create a second universal memory table. Do not duplicate Orçamento memory in a generic table.

## 8. Action → experience capture contract

Every meaningful governed action should be representable as:

- objective/context
- input structure
- decomposition
- ordered action sequence
- dependencies/capabilities used
- knowledge consulted
- decision(s)
- verification
- result
- errors
- corrections
- evidence/source reference
- validation status
- promotion status

When these fields are absent, the event may still be operationally logged, but it is not sufficient by itself to become a generalized learning record.

## 9. Learning gate

The minimum learning path is:

```text
OBSERVED
→ EVIDENCED
→ ASSOCIATED
→ HYPOTHESIS
→ TESTED
→ REFINED
→ LEARNING_CANDIDATE
→ GOVERNED_LEARNING
→ EVOLUTION_GATE
→ VALIDATED_LEARNING
```

A single successful execution does not generalize a method.

Failed experiments remain evidence. They are not silently deleted because they explain why a candidate was rejected or refined.

## 10. Implementation boundary

The current GitHub adapter is read-only and maps only verified Elo-forge table names. It does not open a Supabase connection and does not write data.

Database migrations should be limited to gaps proven by schema analysis. Before adding a new table, first verify whether an existing Elo-forge table already owns the function.

This keeps the architecture relational, explainable, queryable and compatible with Supabase/Postgres foreign-key introspection and nested relational queries.
