# SKILL-004 — Native Capability Absorption

- **skill_id:** `symbiont.capability_absorption`
- **owner:** ELO Cognitive
- **executor:** NativeCapabilityAbsorption
- **authority:** Evolution Gate + governança de aprendizado
- **status:** CANDIDATE_GENERATION

## Função

Transformar uma observação laboratorial já validada em um candidato de capacidade, preservando evidência e proveniência.

## Relação na cadeia de ações

`laboratory observation → regression PASS → generalization CONFIRMED → capability candidate → governance`

## Pré-condições

- evidência presente;
- tenant compatível;
- regressão PASS;
- generalização CONFIRMED;
- risco não crítico;
- proveniência completa.

## Não faz

- registrar provider;
- conceder autorização;
- escrever Core;
- promover memória;
- substituir Evolution Gate.

## Testes

- ausência de evidência → bloqueio;
- tenant mismatch → bloqueio;
- regression != PASS → bloqueio;
- generalização != CONFIRMED → bloqueio;
- risco crítico → bloqueio;
- candidato válido → `CANDIDATE_ONLY`.

## Aprovação

A aprovação significa apenas que o candidato satisfaz os pré-requisitos de absorção. A promoção continua sendo uma decisão posterior e governada.
