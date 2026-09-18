---
artifact_id: ADR-0012-decision-outcome-loop
title: Decision Outcome Loop como padrão estrutural de aprendizado cognitivo
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
  - ELO Infrastructure
date: 2026-09-18
supersedes: null
superseded_by: null
related:
  - ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md
  - ELO_AUTHORIZED_ACCESS_POLICY.md
  - ELO_AUTHORIZED_SPECIALIST_ACCESS_STANDARD.md
---

# ADR-0012 — Decision Outcome Loop

## Contexto

O ELO já possui `DecisionRecord` e `OutcomeFeedback` como limites canônicos para decisão e resultado, além de memória evolutiva, raciocínio causal e governança de evolução. A proposta original de um novo ledger, observers, calibração e índice de precedentes deve, portanto, ser implementada sem criar uma segunda autoridade ou duplicar esses contratos.

O problema estrutural permanece: uma decisão precisa ser acompanhada por resultado observado, avaliação, atribuição, aprendizado e possibilidade de consulta como precedente.

## Decisão

Adotar o **Decision Outcome Loop (DOL)** como padrão estrutural do Core, reutilizando `DecisionRecord` e `OutcomeFeedback`.

O DOL não é agente, não é especialista autônomo e não é uma nova autoridade de memória. Ele fornece:

- máquina de estados explícita para o ciclo da decisão;
- trilha de transições com evidência;
- vínculo obrigatório entre decisão e outcome observado;
- atribuição normalizada como avaliação, não como causalidade automática;
- calibração estatística baseada em outcomes sem reescrever a confiança histórica;
- índice de precedentes somente para ciclos fechados e evidenciados.

Estados:

`proposed → approved → executed → observing → evaluated → attributed → learned → closed`

com ramos governados para `escalated` e `reverted`.

## Regras canônicas

1. `DecisionRecord` continua sendo o contrato de decisão.
2. `OutcomeFeedback` continua sendo o contrato de resultado.
3. `DecisionLifecycle` somente organiza o ciclo; não executa ação empresarial.
4. `0.70` continua sendo limiar de governança quando aplicável; não é requisito para registrar aprendizado.
5. Calibração mede confiança declarada contra outcomes observados e não altera retroativamente decisões históricas.
6. Atribuição é uma avaliação ponderada e evidenciada; não constitui prova causal por si só.
7. Precedente só pode ser criado de um ciclo `closed` com outcome e evidência.
8. Nenhuma implementação do DOL concede escrita genérica no banco corporativo.
9. Promoção de aprendizado para conhecimento canônico continua subordinada ao Evolution Gate e às regras existentes de governança.
10. Persistência canônica deve seguir a autoridade de memória já estabelecida; este ADR não cria `memory/ledger/` como segunda fonte de verdade.

## Implementação desta fase

Foram adicionados ao Core:

- `src/elo/core/decision_outcome_loop.py`;
- `src/elo/core/calibration.py`;
- `src/elo/core/precedent_index.py`;
- testes unitários correspondentes.

A integração MCP, observers específicos da Corporate Decision Skill e qualquer persistência durável ficam bloqueados até que os contratos/runtime existentes sejam localizados e integrados, evitando duplicação.

## Critérios de aceitação

- transições inválidas são bloqueadas;
- avaliação, atribuição e aprendizado exigem evidência;
- outcome pertence à mesma decisão;
- precedentes não podem nascer de ciclos abertos;
- confiança histórica não é mutada pela calibração;
- nenhuma operação do DOL executa ação empresarial ou concede autoridade.

## Status

Aceito como padrão arquitetural. Implementação inicial do Core concluída em branch de mudança; integração adicional depende da reconciliação dos limites canônicos existentes.
