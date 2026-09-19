# SKILL-002 — Decision Outcome Loop

- **skill_id:** `decision.outcome_loop`
- **owner:** ELO Core
- **executor:** DecisionLifecycle
- **authority:** ELO Core + contratos existentes
- **status:** CORE_PATTERN

## Função

Organizar o ciclo de uma decisão desde proposta até outcome, avaliação, atribuição, aprendizado candidato e fechamento.

## Relação na cadeia de ações

`DecisionRecord → proposed → approved → executed → observing → OutcomeFeedback → evaluated → attributed → learning candidate → closed`

Os ramos `escalated` e `reverted` permanecem governados.

## Limite crítico

O estado `LEARNED` representa que um **candidato de aprendizagem foi produzido pelo ciclo**. Não representa promoção de conhecimento canônico.

A promoção permanece em:

`LearningGovernance → avaliação → aprovação humana → Evolution Gate → materialização governada`

## Testes

Obrigatórios:

- transição inválida → bloqueio;
- outcome de outra decisão → bloqueio;
- outcome sem evidência → bloqueio;
- avaliação sem outcome → bloqueio;
- atribuição inválida → bloqueio;
- learning sem candidato → bloqueio;
- precedente de ciclo aberto → bloqueio;
- precedente sem evidência → bloqueio;
- handoff Symbiont sem correspondência de decision_id → bloqueio.

## Evidência

Cada mudança de estado relevante deve carregar evidência.

## Aprovação

A aprovação do DOL valida o ciclo estrutural. Não concede autorização empresarial e não altera o significado dos gates existentes.
