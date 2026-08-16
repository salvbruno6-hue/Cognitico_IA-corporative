# ELO-017 — Simulação operacional da Empresa Digital Multiteiner

## Objetivo

Transformar o cenário ELO-016 em ciclos operacionais sintéticos, rastreáveis e repetíveis, sem criar novo Core, memória, Orchestrator ou estrutura organizacional-semente.

## Ciclo

Demanda → Produto/Módulo → Planejamento → Orçamento → Relações entre domínios → Gestão à Vista → Observe → Analyze → Project → Decide/Handoff → Execute (quando autorizado) → Monitor → Resultado → Learn/Evolve.

## Regras

- Todo dado usado pelo cenário é sintético e deve ser identificado como tal.
- Inferências preservam evidência e proveniência.
- Gestão à Vista é camada de observação, não fonte absoluta de verdade.
- Execução exige autoridade válida.
- Conhecimento não validado não se torna canônico.
- Tenant, domínio, principal e correlação permanecem delimitados.
- Repetições do ciclo devem ser comparáveis.
- Alterações devem ser classificadas como faculdade, overlay, gap ou conflito antes de promoção.

## Cenários mínimos

1. Demanda → planejamento → orçamento.
2. Alteração de produto/módulo e propagação de impacto.
3. Desvio observado na Gestão à Vista e investigação de relações.
4. Conflito entre especialistas.
5. Evidência insuficiente.
6. Ação sem autorização.
7. Execução autorizada e monitoramento.
8. Segundo ciclo com variação controlada e classificação faculdade versus overlay.

## Evidência esperada

Cada ciclo deve preservar: cenário, ciclo, estado anterior, observações, evidências, proveniência, especialistas envolvidos, decisão, autoridade, ação, estado posterior, resultado e classificação de aprendizado.

## Gates

CI PASS + Behavioral Validation PASS + Evolution Gate PASS + Canonical validation PASS + ausência de conflito canônico não resolvido.

## Fonte arquitetural

A simulação é um artefato experimental/testável sobre os contratos canônicos existentes. A localização e a autoridade seguem `AGENTS.md` e `ELO_REPOSITORY_NAVIGATION_RULES.md`.
