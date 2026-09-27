---
artifact_id: ELO-BUG-REPRODUCTION-LOOP
title: ELO Bug Reproduction Loop
family: docs/governance
layer: governance
type: contract
owner: ELO Governance
authority: reference
status: defined
version: 0.1.0
related:
  - ELO_GOVERNED_AUTONOMOUS_ISSUE_LOOP
  - ELO_COGNITIVE_EXECUTION_CONTRACT
  - AGENTS.md
---

# ELO Bug Reproduction Loop

## 1. Propósito

Definir o ciclo canônico de tratamento de bug no ELO como composição de
componentes existentes, sem criar novo orquestrador.

## 2. Natureza

O bug loop NÃO é um componente novo. É a composição formal de quatro peças
que já existem:

| Peça | Responsabilidade |
|---|---|
| `EngineeringCycle` (`src/elo/core/software_engineering.py`) | Estrutura: diagnóstico, causa raiz, hipótese, mudança proposta |
| `run_symbiont_autonomous_adjustment_loop` (`src/elo/agent_intake/implementation_loop.py`) | Motor: ajustar → avaliar → retestar |
| gates de `implementation_loop` | Regressão + repetibilidade |
| `ELO_DECISION=CORRECT` no `elo-agent-loop` | Governança: correção autorizada |

## 3. Ciclo canônico

```text
BUG/FINDING
  ↓
REPRODUCE
  ↓
CAPTURE REPRODUCTION EVIDENCE
  ↓
DIAGNOSE + ROOT CAUSE
  ↓
PROPOSE CHANGE
  ↓
CORRECT
  ↓
RUN REGRESSION TEST
  ↓
RETEST / REPEAT
  ↓
VALIDATE
  ↓
ELO GOVERNANCE
```

O ciclo é uma composição de contratos e mecanismos existentes. Nenhuma etapa
cria uma nova autoridade de execução ou governança.

## 4. Extensão verificável do EngineeringCycle

`EngineeringCycle` preserva seus campos existentes e adiciona três referências
explícitas:

- `reproduction_evidence_ids`: evidências que demonstram a reprodução do
  comportamento defeituoso;
- `regression_test_ids`: testes que codificam a falha para impedir regressão;
- `validation_evidence_ids`: evidências produzidas após a correção e o
  reteste.

Esses campos são referências de evidência, não uma nova memória ou autoridade.

## 5. Invariantes

### Invariante 1 — reprodução verificável

Um ciclo não pode ser preparado como bug cycle sem pelo menos uma evidência de
reprodução e pelo menos um teste de regressão identificado.

```text
reproduction_evidence_ids != ∅
AND
regression_test_ids != ∅
```

### Invariante 2 — validação antes da governança

Um ciclo somente pode atingir `READY_FOR_GOVERNANCE` quando os testes passaram,
a regressão passou e existe evidência de validação do reteste.

```text
tests_passed
AND regression_passed
AND validation_evidence_ids != ∅
```

Falha de teste ou regressão nunca pode ser convertida diretamente em
`READY_FOR_GOVERNANCE`.

## 6. Relação com a Simbionte

A Simbionte fornece o mecanismo iterativo:

```text
adjust → evaluate → RETEST → adjust → evaluate → SUCCESS
```

O bug contract não substitui esse mecanismo. Ele fornece a semântica de
reprodução, evidência e validação necessária para que o resultado seja
interpretável como correção de defeito.

## 7. Relação com o agent-loop

Quando ELO identifica uma correção necessária:

```text
ELO_DECISION=CORRECT
→ ELO correction loop
→ validation
→ ELO governance re-review
```

A correção permanece subordinada aos gates existentes e ao limite de ciclos
configurado pelo contrato operacional.

## 8. Limites

Este contrato não cria:

- novo workflow;
- novo orquestrador;
- novo harness;
- nova memória;
- nova autoridade de testes;
- nova autoridade de merge;
- nova autoridade de aprendizagem.

GitHub continua sendo o ledger operacional e ELO continua sendo a autoridade
cognitiva/governança.

## 9. Critério de encerramento

O bug loop pode sair para governança somente quando:

1. a reprodução foi registrada;
2. a causa raiz foi explicitada;
3. a mudança proposta foi aplicada;
4. o teste de regressão foi executado;
5. o teste e a regressão passaram;
6. a validação do reteste foi registrada;
7. os gates existentes permanecem satisfeitos.

Caso qualquer condição permaneça falsa, o ciclo retorna a correção/reteste ou
segue para bloqueio/escalonamento conforme os contratos existentes.

## 10. Não-duplicação

A formalização é `EXTEND`, não `CREATE`. O contrato somente compõe e torna
verificáveis mecanismos já existentes.

A sequência canônica permanece:

`INSPECT → REUSE → EXTEND → RELATE → REFACTOR/MIGRATE → CREATE ONLY IF INDISPENSABLE`.
