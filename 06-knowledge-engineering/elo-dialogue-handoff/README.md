# ELO Dialogue Handoff Skill

Esta pasta documenta a Skill de protocolo que aproxima a mecânica GPT↔ELO sem criar uma autoridade paralela.

## Arquitetura

```text
Usuário
  ↓
GPT
  ↓  SKILL.md
HANDOFF_GPT_TO_ELO
  ↓
ELO-MCP / ELO Web
  ↓
elo-authz
  ↓
Objective Continuity
  ↓
Supabase checkpoint
  ↓
HANDOFF_ELO_TO_GPT
  ↓
GPT
  ↓
Usuário
```

## Arquivos

- `SKILL.md` — contrato principal e limites;
- `HANDOFF_GPT_TO_ELO.md` — payload de entrada;
- `HANDOFF_ELO_TO_GPT.md` — payload de retorno;
- `CHECKPOINT_CONTRACT.md` — monotonicidade, replay e persistência;
- `AUTHORIZATION_CONTRACT.md` — autoridade exclusiva do `elo-authz`;
- `FAILURE_AND_ESCALATION.md` — fail-closed e intervenção humana;
- `EXAMPLES.md` — exemplos de decisões e falhas.

## Regra de não duplicidade

A Skill não implementa decisão cognitiva, persistência, autorização, scheduler, owner, executor ou promoção. Ela referencia e coordena os mecanismos canônicos existentes.

## Relação com runtime

O runtime canônico continua sendo ELO Web. O ELO-MCP é o boundary de integração quando disponível. O Supabase guarda o estado persistente atribuído pela arquitetura. O GPT permanece interface e transporte.

## Estado

`DEFINED` — documentação pronta para revisão, testes executáveis e eventual promoção pelo fluxo canônico.