---
artifact_id: ELO-TEST-HARNESS-CONTRACT
title: ELO Test Harness Contract
family: docs/testing
layer: testing
status: normative
owner: ELO Quality Engineering
authority: reference
version: 1.0.0
related:
  - COGNITIVE_HARNESS
  - SYMBIONT_MCP_TEST_HARNESS
  - ADR-0014-cognitive-runtime-loop
  - ELO_BUG_REPRODUCTION_LOOP
---

# ELO Test Harness Contract

## 1. Propósito

Definir o Harness de Teste do ELO — o orquestrador que
valida, em conjunto, os componentes críticos do sistema.

O Harness de Teste é o **Pilar 2** da arquitetura de
validação do ELO:

- Pilar 1 — Harness Cognitivo (CRL completo)
- Pilar 2 — Harness de Teste (composição)
- Pilar 3 — Reconciliação Live (GitHub vs Supabase)

## 2. Natureza

O Harness de Teste **não é um novo harness**. Ele é um
orquestrador que:

- chama os 4 harnesses existentes
- valida módulos do Core
- produz report consolidado

Ele não duplica lógica, não substitui harnesses, não cria
autoridade paralela.

## 3. Harnesses orquestrados

| Harness | Localização | O que mede |
|---|---|---|
| cognitive_harness | src/elo/cognitive/runtime/ | CRL 10 estágios |
| hook_loop_harness | src/elo/agent_intake/ | Guardrail EXT-HOOK |
| checkpoint_loop_harness | src/elo/agent_intake/ | Replay guard |
| symbiont_mcp_test_harness | src/elo/cognitive/ | MCP capability |

## 4. Módulos Core validados

O Harness de Teste valida que os módulos abaixo importam,
instanciam e respondem:

- decision_outcome_loop (DOL)
- calibration
- precedent_index
- engineering_cycle (bug loop)

A validação verifica disponibilidade e integridade, não
reexecuta lógica.

## 5. Isolamento

- Usa tempfile.TemporaryDirectory() como cwd
- Não acessa Supabase
- Não acessa MCP
- Não acessa rede
- Não escreve em memory/cognitive/ do repositório

## 6. Report consolidado

O report produz:

- status geral (PASS / FAIL / BLOCKED)
- resultado por harness (PASS / FAIL / SKIPPED)
- resultado por módulo Core (AVAILABLE / MISSING / ERROR)
- duração por harness
- timestamp

## 7. Não objetivos

Este contrato NÃO:

- cria novo harness
- substitui testes unitários existentes
- substitui o CI
- substitui o Evolution Gate
- promove aprendizado
- acessa produção

## 8. Vigência

Entra em vigor na aprovação da PR do Harness de Teste.
Alterações exigem ADR.
