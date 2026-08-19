# ELO — Pré-auditoria das Famílias Bilingues — 2026-08-19

## Escopo

Este documento registra somente fatos explicitamente confirmados pelo ADR `ADR-2026-08-19-BILINGUAL-TREE-CONSOLIDATION.md`. Ele não substitui a auditoria arquivo-a-arquivo e não transforma assimetria de volume em equivalência semântica.

## Regra de evidência

```text
ADR-confirmed fact
    ↓
PREAUDIT
    ↓
fetch each tree
    ↓
content comparison
    ↓
classification
    ↓
artifact identity / references
    ↓
decision
```

## Família 01 — Meta Arquitetura

### Evidência confirmada

O ADR informa que `01-meta-arquitetura/` contém material substantivo de:

- inteligência de demanda;
- mapa de domínios;
- glossário;
- modelo conceitual;
- entidades;
- relacionamentos;
- regras de negócio;
- arquitetura mestre.

A árvore `01-meta-architecture/` é descrita como contendo README, `.gitkeep` e a subárvore `cognitive-architecture`.

### Classificação provisória

```text
PT tree = CONTENT_RICH / AUDIT_REQUIRED
EN tree = CANONICAL_LOCATION_CANDIDATE / CONTENT_REVIEW_REQUIRED
semantic equivalence = NOT_PROVEN
migration = BLOCKED
removal = BLOCKED
```

### Risco

Alto. A árvore portuguesa não pode ser descartada como duplicada porque o ADR confirma conteúdo substantivo.

## Família 05 — Cognitivo / Cognitive Platform

### Evidência confirmada

O ADR informa que `05-cognitivo-plataforma/` contém fundamentos cognitivos, filosofia, recursos estratégicos, inteligência de demanda, modelo de conhecimento e RAG.

`05-cognitive-platform/` contém a estrutura operacional mais recente, incluindo engine cognitivo, decision engine, memory/reasoning, especialistas e contratos Multiteiner.

### Classificação provisória

```text
PT tree = CONTENT_RICH / AUDIT_REQUIRED
EN tree = CURRENT_OPERATIONAL_CANDIDATE / CONTENT_REVIEW_REQUIRED
relationship = POTENTIALLY_COMPLEMENTARY
semantic equivalence = NOT_PROVEN
migration = BLOCKED
removal = BLOCKED
```

### Risco

Crítico. Os conteúdos aparentam ter finalidades diferentes e podem ser complementares. Não realizar merge textual automático.

## Família 07 — Engenharia de Dados

### Evidência confirmada

`07-engenharia-de dados/` contém modelo lógico, dicionário, SQLite, APIs, eventos e master de engenharia de dados.

`07-data-engineering/` possui scaffolding/README/AGENTS.

### Classificação provisória

```text
PT tree = CONTENT_RICH / AUDIT_REQUIRED
EN tree = CANONICAL_LOCATION_CANDIDATE / SCAFFOLDING
semantic equivalence = NOT_PROVEN
migration = BLOCKED
removal = BLOCKED
```

### Risco

Alto. O conteúdo português deve ser inventariado antes de qualquer consolidação física.

## Família 11 — Models

### Evidência confirmada

`11-modelos/` contém `MODELS_LIBRARY_MASTER.md`.

`11-models-library/` possui `.gitkeep`.

### Classificação provisória

```text
PT tree = CONTENT_RICH / AUDIT_REQUIRED
EN tree = CANONICAL_LOCATION_CANDIDATE / SCAFFOLDING
semantic equivalence = NOT_PROVEN
migration = BLOCKED
removal = BLOCKED
```

### Risco

Médio/alto. Um master único pode conter conteúdo normativo ou estrutural que precisa de identidade própria antes da migração.

## Família 12 — Systems

### Evidência confirmada

`12-sistemas/` contém `SYSTEMS_ENGINEERING_MASTER.md`.

`12-system-engineering/` possui `.gitkeep`.

### Classificação provisória

```text
PT tree = CONTENT_RICH / AUDIT_REQUIRED
EN tree = CANONICAL_LOCATION_CANDIDATE / SCAFFOLDING
semantic equivalence = NOT_PROVEN
migration = BLOCKED
removal = BLOCKED
```

### Risco

Médio/alto. O master precisa ser comparado com a arquitetura e contratos atuais antes de qualquer decisão de destino.

## Famílias 13, 14 e 15

O ADR consultado não fornece evidência suficiente para atribuir conteúdo, equivalência ou autoridade a essas três famílias. Portanto:

```text
13 = NO_EVIDENCE_FROM_THIS_SOURCE
14 = NO_EVIDENCE_FROM_THIS_SOURCE
15 = NO_EVIDENCE_FROM_THIS_SOURCE
```

Isso não significa que as árvores não existam; significa somente que o documento-base desta pré-auditoria não comprova sua situação.

## Matriz consolidada

| Família | Evidência ADR | PT conteúdo | EN estado | Equivalência | Migração |
|---|---|---|---|---|---|
| 01 | confirmada | substantivo | menor + cognitive-architecture | não provada | bloqueada |
| 05 | confirmada | substantivo | operacional mais recente | potencialmente complementar | bloqueada |
| 07 | confirmada | substantivo | scaffolding | não provada | bloqueada |
| 11 | confirmada | master | `.gitkeep` | não provada | bloqueada |
| 12 | confirmada | master | `.gitkeep` | não provada | bloqueada |
| 13 | insuficiente | não inferir | não inferir | não inferir | bloqueada |
| 14 | insuficiente | não inferir | não inferir | não inferir | bloqueada |
| 15 | insuficiente | não inferir | não inferir | não inferir | bloqueada |

## Próximo lote de evidência

Para 01, 05, 07, 11 e 12, a próxima ação deve ser fetch dos arquivos efetivamente presentes em ambas as árvores e comparação de conteúdo.

Para 13, 14 e 15, primeiro executar descoberta de paths; somente depois realizar fetch.

## Gate

```text
PREAUDIT = PASS
CONTENT_COMPARISON = PENDING
REFERENCE_MAPPING = PENDING
CONSUMER_MAPPING = PENDING
MIGRATION = BLOCKED
REMOVAL = BLOCKED
```
