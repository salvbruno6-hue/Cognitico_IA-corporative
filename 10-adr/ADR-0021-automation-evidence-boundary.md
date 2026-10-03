---
artifact_id: ADR-0021-automation-evidence-boundary
title: Automation Evidence Boundary — Composição dos Owners Canônicos
family: 10-adr
status: proposed
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
date: 2026-09-28
supersedes: null
superseded_by: null
related:
  - ELO_WORKFLOW_AUTOMATION_CONTRACT
  - ADR-0014-cognitive-runtime-loop
  - ADR-0012-decision-outcome-loop
---

# ADR-0021 — Automation Evidence Boundary — Composição dos Owners Canônicos

## Pergunta

**Existe alguma informação necessária ao loop de automação que NÃO pode ser representada pela composição WorkflowRun + ExecutionOutcome + RuntimeOperationalEvidence + SymbiontLabObservation?**

## Decisão

**VERDICTO: INDETERMINADO → NÃO IMPLEMENTAR AutomationEvidence por enquanto.**

A composição dos quatro owners canônicos existentes cobre as dimensões essenciais do loop de automação:

- `WorkflowRun` — identidade e estado da execução do workflow, contexto do trigger, tenant, request, capabilities, actions, evidências e resposta;
- `ExecutionOutcome` — resultado governado da execução, identidade da requisição, status, execução efetiva, autorização referenciada, correlação, provenance, evidências e timestamp;
- `RuntimeOperationalEvidence` — evidência operacional, atribuição, métrica, baseline, valor observado, provenance, regressão e repetibilidade;
- `SymbiontLabObservation` — observação cognitiva vinculada à execução, decisão, evidências, baseline, hipótese, experimento, resultado, regressão, generalização, risco e escopo.

As lacunas identificadas no PASSO 48.4.1 são reais, porém não constituem justificativa para uma quinta camada concorrente de evidência.

As dimensões temporais `started_at`, `finished_at` e `duration`, caso precisem ser formalizadas posteriormente, pertencem semanticamente ao owner `WorkflowRun`.

A formalização de `retry/recovery`, caso necessária, também pertence ao `WorkflowRun`, como semântica própria da execução do workflow, e não como uma nova autoridade de evidência.

As informações relativas à emissão, binding e expiração de autorização permanecem sob a autoridade canônica de autorização. Não devem ser duplicadas nos quatro owners de workflow, execução, evidência operacional ou laboratório.

Portanto, o estado atual permanece **INDETERMINADO**, sem criação de `AutomationEvidence` e sem criação de novo contrato de automação.

## Regra de não duplicidade

É proibida a criação de uma quinta camada concorrente de evidência denominada `AutomationEvidence` para suprir as lacunas identificadas neste registro.

Qualquer proposta futura de criação dessa camada exige **nova decisão humana explícita**, precedida de demonstração objetiva de que os owners canônicos existentes não podem ser reutilizados, estendidos ou compostos sem perda semântica ou arquitetural.

A decisão presente não autoriza implementação, alteração de contrato ou criação de novo owner.

## Regra de autoridade de autorização

A emissão, o binding, a validade e a expiração de autorizações permanecem sob o **owner canônico de autorização**.

`WorkflowRun`, `ExecutionOutcome`, `RuntimeOperationalEvidence` e `SymbiontLabObservation` não constituem autoridade de autorização e não devem assumir esse papel.

Uma referência a uma autorização em um resultado de execução não transforma o owner que contém a referência em autoridade emissora ou validadora da autorização.

## Limite da automação

A decisão está alinhada ao contrato canônico:

`automation/ELO_WORKFLOW_AUTOMATION_CONTRACT.md`, linhas 18–22.

O contrato estabelece que a automação invoca capacidades existentes do ELO e não se torna fonte de verdade nem autoridade. Ações consequenciais exigem resultado explícito de autorização.

Consequentemente, o loop de automação deve continuar compondo os owners canônicos existentes, sem introduzir uma autoridade paralela de evidência ou autorização.

## Base da decisão

Esta decisão é fundamentada no **PASSO 48.4.1 — Fechamento conceitual da lacuna AutomationEvidence**, que avaliou a capacidade representacional de:

`WorkflowRun + ExecutionOutcome + RuntimeOperationalEvidence + SymbiontLabObservation`.

O PASSO 48.4.1 concluiu que as lacunas identificadas não demonstram necessidade arquitetural suficiente para criação de `AutomationEvidence`.

Este ADR formaliza essa conclusão para impedir a reabertura indevida do mesmo GAP como se fosse uma necessidade de implementação.

## Consequências

### Positivas

- preservação dos owners canônicos existentes;
- ausência de uma quinta camada concorrente de evidência;
- manutenção da separação entre execução, evidência operacional, laboratório e autorização;
- prevenção de duplicidade semântica;
- futuras lacunas de temporalidade e retry/recovery permanecem direcionadas ao owner correto;
- autorização continua centralizada em sua autoridade canônica.

### Negativas

- algumas dimensões permanecem semanticamente não formalizadas enquanto não houver necessidade comprovada de extensão de `WorkflowRun`;
- o estado permanece `INDETERMINADO` até que nova evidência ou decisão humana justifique alteração arquitetural.

## Conformidade

- Regra de duplicidade: **REUSE / COMPOSE**
- Camada: **Governança (ADR)**
- Não cria capacidade nova.
- Não cria novo owner.
- Não cria novo contrato.
- Não cria `AutomationEvidence`.
- Não altera `WorkflowRun`.
- Não altera `ExecutionOutcome`.
- Não altera `RuntimeOperationalEvidence`.
- Não altera `SymbiontLabObservation`.
- Não altera a autoridade canônica de autorização.

## Status

**Proposto.**

O presente ADR registra exclusivamente a decisão conceitual de **não implementar `AutomationEvidence` por enquanto**.

Nenhuma implementação é autorizada por este ADR.

FIM DO CONTEÚDO.
