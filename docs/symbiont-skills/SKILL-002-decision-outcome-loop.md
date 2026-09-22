# SKILL-002 — Decision Outcome Loop

- **skill_id:** `decision.outcome_loop`
- **owner:** ELO Core
- **executor:** `DecisionLifecycle`
- **authority:** ELO Core + contratos existentes
- **status:** CORE_PATTERN
- **composition:** existing canonical components only
- **canonicality:** this skill is a reusable procedure, not a new authority

## Função

Organizar o ciclo de uma decisão desde proposta até outcome, avaliação, atribuição, aprendizado candidato e fechamento.

A Skill existe porque há uma sequência operacional recorrente que compõe capacidades já canônicas. Ela **não substitui nem duplica** essas capacidades.

## Composição canônica

| Etapa da Skill | Componente existente | Autoridade |
|---|---|---|
| decisão e transições | `elo.core.decision_outcome_loop.DecisionLifecycle` | ELO Core |
| outcome/evidência | `OutcomeFeedback` | contrato de decisão/outcome existente |
| handoff para aprendizagem | `DecisionLifecycle.handoff_to_symbiont()` | ELO Core |
| laboratório/adaptação | `SymbiontLabAdapter` | ELO Cognitive |
| experiência/candidato/evaluação | `GovernedLearningService` | Learning Governance |
| compatibilidade/evolução | `EvolutionGate` | Evolution Gate |
| persistência operacional | `DecisionStore` / memória canônica existente | respectivos owners |

### Regra de composição

A Skill somente **coordena o procedimento**. Não cria:

- segunda memória;
- segundo Evolution Gate;
- segunda Learning Governance;
- segundo Decision Lifecycle;
- novo registry de Skills;
- novo runtime de automação;
- nova autoridade de promoção.

Se um componente canônico já atende uma etapa, a Skill deve reutilizá-lo.

## Relação na cadeia de ações

`DecisionRecord → proposed → approved → executed → observing → OutcomeFeedback → evaluated → attributed → learning candidate → closed`

Os ramos `escalated` e `reverted` permanecem governados.

## Entradas autorizadas

- `DecisionRecord`;
- `OutcomeFeedback` compatível com o `decision_id`;
- evidências identificáveis;
- atribuição de causas/pesos válida;
- candidato de aprendizagem;
- observação Symbiont compatível quando houver handoff;
- `principal_id` e `dataset_version` quando o laboratório for acionado.

## Saídas

A Skill produz somente resultados do procedimento:

- transições de estado;
- histórico de transições;
- outcome associado;
- atribuição;
- learning candidate;
- avaliação/handoff do laboratório;
- estado de fechamento ou escalonamento.

Ela **não promove conhecimento canônico por si só**.

## Limite crítico

O estado `LEARNED` representa que um **candidato de aprendizagem foi produzido pelo ciclo**. Não representa promoção de conhecimento canônico.

A promoção permanece em:

`LearningGovernance → avaliação → aprovação humana → Evolution Gate → materialização governada`

## Relação com automação

Automação pode executar ou disparar etapas do procedimento, mas não ganha autoridade de aprendizagem por isso.

O runtime de automação existente permanece apenas mecanismo de execução/orquestração. A autoridade continua nos owners canônicos.

Não criar `LearningAutomationRunner` como uma nova autoridade apenas para materializar esta Skill.

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
- handoff Symbiont sem correspondência de `decision_id` → bloqueio;
- handoff sem evidência → bloqueio;
- candidato produzido pelo handoff → ciclo pode entrar em `LEARNED`;
- ausência de candidato → ciclo não entra em `LEARNED`.

## Evidência

Cada mudança de estado relevante deve carregar evidência.

A evidência deve permanecer vinculada ao ciclo e às decisões que a produziram; a Skill não cria uma memória paralela para armazená-la.

## Aprovação

A aprovação do DOL valida o ciclo estrutural. Não concede autorização empresarial e não altera o significado dos gates existentes.

## Critério de não-duplicação

Antes de criar qualquer nova Skill para o mesmo domínio, verificar:

1. se o procedimento já está coberto por `decision.outcome_loop`;
2. se o novo pedido é apenas uma composição diferente dos mesmos componentes;
3. se a diferença é somente contextual/paramétrica;
4. se existe uma etapa realmente nova, reutilizável e com contrato próprio.

Se 1–3 forem verdadeiros, **evoluir esta Skill ou o componente responsável**. Não criar outra Skill semanticamente equivalente.

## Maturidade

A Skill é um `CORE_PATTERN` porque o procedimento e seus limites já possuem implementação e testes no ELO.

Qualquer extensão nova deve seguir:

`evidence → implementation → tests → Evolution Gate → governed promotion`
