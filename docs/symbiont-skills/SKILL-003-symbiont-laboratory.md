# SKILL-003 — Symbiont Laboratory

- **skill_id:** `symbiont.lab`
- **owner:** ELO Cognitive
- **executor:** SymbiontLabAdapter
- **authority:** Evolution Gate + GovernedLearningService
- **status:** LAB_BOUNDARY

## Função

Receber observações experimentais com identidade, tenant, proveniência, evidência, baseline, experimento, resultado, regressão, generalização e risco.

## Relação na cadeia de ações

`outcome → laboratory observation → validation → Evolution Gate → experience/candidate`

## Bloqueios

- identidade incompleta;
- evidência ausente;
- tenant incompatível;
- proveniência ausente;
- regressão;
- generalização não suportada;
- risco crítico;
- evolução incompatível/conflitante/duplicada.

## Generalização

- `CONFIRMED`: pode prosseguir conforme os gates;
- `PARTIAL`: pode representar maturidade intermediária de candidato;
- `UNCONFIRMED`: não pode produzir aprendizado;
- capacidade absorvida exige generalização confirmada.

## Testes

Aprovação exige testes de:

- identidade/proveniência;
- isolamento de tenant;
- evidência;
- regressão;
- generalização;
- risco;
- classificação do Evolution Gate;
- ausência de promoção automática.

## Saída

A saída é evidência laboratorial, experiência ou candidato governado. Nunca é promoção canônica automática.


## Aprovação

A skill somente avança quando identidade, tenant/scope, proveniência, evidência, regressão, generalização, risco e Evolution Gate estiverem validados. A documentação não concede aprovação nem promoção canônica.
