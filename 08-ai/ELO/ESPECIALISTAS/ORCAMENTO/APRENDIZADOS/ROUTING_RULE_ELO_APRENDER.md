# ELO APRENDER — Roteamento Canônico de Aprendizados de Orçamento

## Regra obrigatória do gatilho

Quando `ELO APRENDER` processar uma experiência cuja origem seja uma **Solicitação de Orçamento (SO)** e o conhecimento pertencer ao domínio do **Especialista de Orçamento**, o artefato de aprendizado deve ser criado ou consolidado exclusivamente em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/`

O arquivo `ELO_RETORNO_CANONICO.md` define também o padrão obrigatório de retorno ao consultar ou aprender uma SO.

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
8. Executar a varredura de cálculos prevista no fluxo de `ELO APRENDER` e persistir os cálculos aplicáveis no Supabase.
9. Commit só após a governança e os testes aplicáveis.

## Retorno canônico

Ao receber `ELO APRENDER` ou uma consulta do tipo `ELO — o que sabemos sobre a SO X`, o retorno deve integrar:

- identificação e escopo da SO;
- PTS Técnica;
- tratamento do orçamento;
- excedentes e composições;
- PTS Pós-Orçamento;
- decisões e resoluções;
- conhecimento cognitivo/instrucional armazenado no Git;
- memória de cálculo armazenada no Supabase;
- referências externas/entre SOs com fonte e motivo de aplicabilidade.

Quando houver memória de cálculo no Supabase, apresentá-la obrigatoriamente no padrão definido em `ELO_RETORNO_CANONICO.md`, com: `ID`, `ID Memória`, `Categoria`, `Item`, `Fonte`, `Entrada/Base`, `Unidade`, `Parâmetro/Premissa`, `Fórmula`, `Subcálculo`, `Resultado`, `Unidade Resultado`, `Validação` e `Origem`.

## Supabase

Supabase permanece a camada canônica da **memória quantitativa/de cálculo** do orçamento. Ele fornece informação ao ELO e recebe os cálculos estruturados extraídos pelo subfluxo de varredura; não determina o destino do aprendizado cognitivo nem substitui a governança do ELO.

## Proveniência de referências

Informação recuperada de outra SO é referência consultiva, nunca origem da SO corrente. O ELO deve apresentar fonte, contexto original, informação recuperada, motivo da busca, motivo da possível aplicação, premissas/equivalências e validação necessária.

## Promoção

`PRECEDENT` não é promovido automaticamente a `RULE`. Conhecimento `CONCEPTUAL_KNOWLEDGE` ou `INSTRUCTIONAL_KNOWLEDGE` não deve ser confundido com regra operacional. O destino físico não determina a classificação cognitiva.

## Critério de conclusão

A experiência só pode ser considerada consolidada quando o commit aplicável estiver confirmado. Se o commit falhar, permanecerá pendente para retomada.
