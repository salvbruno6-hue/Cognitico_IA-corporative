# ELO APRENDER — Roteamento Canônico de Aprendizados de Orçamento

## Regra obrigatória do gatilho

Quando `ELO APRENDER` processar uma experiência cuja origem seja uma **Solicitação de Orçamento (SO)** e o conhecimento pertencer ao domínio do **Especialista de Orçamento**, o artefato de aprendizado deve ser criado ou consolidado exclusivamente em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/`

## Proibição de destinos paralelos

O gatilho não deve criar novos aprendizados de orçamento em:

- `memory/solicitations/<SO>/LEARNING.md`
- `memory/solicitations_learning/`
- `04-knowledge-handbook/`
- qualquer outro diretório paralelo de aprendizado de orçamento.

Arquivos históricos existentes nesses locais devem ser tratados como fontes legadas para migração/consolidação, preservando sua proveniência; não devem gerar novos artefatos nesses destinos.

## Decisão de roteamento

1. Identificar a SO e o documento de origem.
2. Reconstruir SO / PTS Técnica / Orçamento / PTS Pós quando disponíveis.
3. Classificar o domínio do conhecimento.
4. Se for aprendizado do Especialista de Orçamento, resolver o destino canônico acima.
5. Consultar a memória existente antes de criar conteúdo.
6. Se o conceito já existir, agregar evidência ao conhecimento existente; se `VALIDATED_LEARNING`, reutilizar sem duplicar.
7. Preservar `SO → documento → evidência → classificação → decisão → commit/PR/merge`.
8. Commit só após a governança e os testes aplicáveis.

## Supabase

Supabase permanece **memória consultiva**, especialmente para cálculos e evidências estruturadas. Ele fornece informação ao ELO, mas não determina o destino do aprendizado nem substitui a governança cognitiva do ELO.

## Proveniência de referências

Informação recuperada de outra SO é referência consultiva, nunca origem da SO corrente. O ELO deve apresentar fonte, contexto original, informação recuperada, motivo da busca, motivo da possível aplicação, premissas/equivalências e validação necessária.

## Promoção

`PRECEDENT` não é promovido automaticamente a `RULE`. Conhecimento `CONCEPTUAL_KNOWLEDGE` ou `INSTRUCTIONAL_KNOWLEDGE` não deve ser confundido com regra operacional. O destino físico não determina a classificação cognitiva.

## Critério de conclusão

A experiência só pode ser considerada consolidada quando o commit aplicável estiver confirmado. Se o commit falhar, permanecerá pendente para retomada.
