# Symbiont Skill — Evidence Matrix

Esta matriz liga cada skill documentada ao código canônico e aos testes localizados em `main`. Ela registra evidência; não concede aprovação humana nem promoção canônica.

| Skill | Código | Testes | Estado |
|---|---|---|---|
| SKILL-001 `symbiont.operational_boundary` | `src/elo/cognitive/symbiont_operational_contract.py` | `tests/cognitive/test_symbiont_operational_contract.py` | **GREEN** |
| SKILL-002 `decision.outcome_loop` | `src/elo/core/decision_outcome_loop.py` | `tests/core/test_decision_outcome_loop.py` | **GREEN** |
| SKILL-003 `symbiont.lab` | `src/elo/cognitive/symbionte_lab.py` | `tests/evolution/test_symbionte_lab_adapter.py`, `test_symbionte_lab_gate_order.py`, `test_symbionte_lab_evidence_boundary.py`, `test_symbionte_lab_execution_contract.py` | **GREEN** |
| SKILL-004 `symbiont.capability_absorption` | `src/elo/cognitive/capability_absorption.py` | `tests/cognitive/test_process_view_and_capability_absorption.py` | **GREEN** |

## SKILL-001 — finalidade internalizada no código

A finalidade operacional da skill possui contrato executável:

- operações permitidas: metadata/read/query/scenario/risk/KPI;
- operações de escrita, DDL, DML, alteração de schema e registro direto de decisão são bloqueadas;
- Symbiont não recebe autoridade de mutação canônica;
- autoridade permanece `recommend`;
- tenant scope é obrigatório;
- confiança é limitada a 0–1;
- confiança >= 0.70 exige evidência;
- confiança < 0.70, alto risco, impacto financeiro, conflito com o cânone ou evidência insuficiente exigem escalonamento humano.

O código é deliberadamente um **guard**, não um executor, roteador, registry, memória ou Evolution Gate.

## SKILL-002 — evidência operacional existente

A implementação canônica do Decision Outcome Loop está em `main` e possui testes específicos cobrindo:

- sequência ordenada do lifecycle;
- bloqueio de transições inválidas;
- outcome vinculado à decisão e com evidência;
- attribution normalizada e validada;
- handoff para o Symbiont Lab existente;
- geração de learning candidate;
- fechamento e criação de precedente.

**Importante:** o estado `LEARNED` continua significando que um learning candidate foi produzido. Não significa promoção de conhecimento canônico.

## SKILL-003 — evidência operacional existente

A base canônica possui testes específicos do adapter cobrindo:

- reutilização do owner existente;
- evidência obrigatória;
- generalização não confirmada;
- tenant scope;
- source kind;
- regressão/risco;
- classificação compatível;
- permanência do learning candidate fora do estado canônico.

## SKILL-004 — evidência operacional existente

A base canônica possui testes para:

- preservação da linhagem;
- `source_ref`;
- `source_commit`;
- `evidence_ids`;
- `CANDIDATE_ONLY`;
- bloqueio sem regression PASS;
- bloqueio sem generalização CONFIRMED.

## Critério de GREEN

GREEN significa que existe implementação identificável e cobertura de testes correspondente. Não significa:

- aprovação humana;
- autorização de promoção;
- merge;
- mutação do Core;
- alteração do Evolution Gate.

A promoção continua dependente de evidência, avaliação, Evolution Gate e aprovação conforme os contratos canônicos.
