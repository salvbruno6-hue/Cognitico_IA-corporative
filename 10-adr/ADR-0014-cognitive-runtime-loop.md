---
artifact_id: ADR-0014-cognitive-runtime-loop
title: Cognitive Runtime Loop como orquestrador dos loops governados
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
  - ELO Infrastructure
date: 2026-09-21
supersedes: null
superseded_by: null
related:
  - ADR-0012-decision-outcome-loop
  - ADR-0013-external-ai-authority-contract
  - ELO_EXTERNAL_AI_AUTHORITY_CONTRACT
  - src/elo/core/decision_outcome_loop.py
  - src/elo/agent_intake/implementation_loop.py
  - src/elo/agentic/orchestrator.py
  - src/elo/agents/runtime.py
  - src/elo/core/core_loop.py
---

# ADR-0014 — Cognitive Runtime Loop (CRL)

## Contexto

O ELO já possui múltiplos loops executáveis:

- `src/elo/core/decision_outcome_loop.py` (DOL)
- `src/elo/core/core_loop.py`
- `src/elo/agent_intake/implementation_loop.py`
- `src/elo/agent_intake/batch_loop_integration.py`
- `src/elo/agentic/orchestrator.py`
- `src/elo/agents/runtime.py`

Esses loops existem de forma especializada, mas não há um
orquestrador único que os coordene como um ciclo cognitivo
contínuo. O README declara o ciclo canônico:

OBSERVE → CONTEXTUALIZE → ANALYZE → FORMULATE → DECIDE
→ EXECUTE → MONITOR → LEARN → FOLLOW-UP → REASSESS

Mas não há mecanismo que faça esse ciclo rodar como processo.

## Decisão

Adotar o Cognitive Runtime Loop (CRL) como orquestrador — não
como novo runtime. O CRL:

1. Não substitui nenhum loop existente.
2. Orquestra os loops governados já implementados.
3. Respeita o evolution_gate em toda promoção.
4. Persiste em memory/ como os loops existentes.
5. É declarativo — não introduz nova autoridade cognitiva.

## Mapeamento de estágios

| Estágio | Loop despachado |
|---|---|
| OBSERVE | src/elo/agent_intake/batch_loop_integration.py |
| CONTEXTUALIZE | src/elo/agentic/context_assembly.py |
| ANALYZE | src/elo/cognitive/autonomous_reasoning.py |
| FORMULATE | src/elo/core/decision_outcome_loop.py (propose) |
| DECIDE | src/elo/core/decision_outcome_loop.py (approve) |
| EXECUTE | src/elo/agents/runtime.py |
| MONITOR | src/elo/core/decision_outcome_loop.py (observe) |
| LEARN | src/elo/core/decision_outcome_loop.py (learn) |
| FOLLOW-UP | src/elo/core/precedent_index.py |
| REASSESS | src/elo/core/calibration.py |

## Estrutura

src/elo/cognitive/runtime/
├── __init__.py
├── crl.py              # orquestrador principal
└── README.md

O CRL não implementa os estágios — apenas despacha.

## Consequências

### Positivas
- Ciclo cognitivo contínuo sem novo runtime
- Reuso máximo de loops existentes
- Rastreabilidade total (cada estágio auditável)
- Zero duplicidade com decision_outcome_loop

### Negativas
- Requer orquestração cuidadosa (dependências entre loops)
- Requer testes end-to-end do ciclo completo
- Requer scheduler (fase 2, ADR próprio)

## Implementação faseada

1. Fase 1 (este ADR): dispatcher sem scheduler
2. Fase 2: scheduler simples (cron/APScheduler)
3. Fase 3: event bus (quando justificado)

Fases 2 e 3 exigem ADRs próprios.

## Conformidade

- Regra de duplicidade: NEW (orquestrador) que REUSA loops
  existentes
- Camadas: Core (não substitui nenhum loop)
- Princípio fundador: preservado

## Status

Aceito. Skeleton em implementação (Fase 1).
---