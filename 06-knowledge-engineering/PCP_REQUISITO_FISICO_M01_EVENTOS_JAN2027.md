# PCP — Requisito físico M01 para eventos até janeiro/2027

## Status

- tipo: evidência de planejamento confirmada pelo usuário;
- natureza: EVENTO;
- modelo canônico: `M01 — Habitacional Amplo 20 pés`;
- quantidade objetivo: **300 unidades físicas**;
- prazo limite: **31/01/2027**;
- quantidade iniciada: **0**;
- quantidade concluída: **0**;
- quantidade restante: **300**;
- distribuição mensal: `AGUARDANDO_CAPACIDADE_VALIDADA`;
- não substitui AF, pedido, plano PCP ou ordem de produção.

## Regra de interpretação

Este requisito representa uma necessidade física confirmada de planejamento. O ELO deve preservá-lo sem convertê-lo automaticamente em pedido operacional, OP ou estoque disponível.

A cadeia governada é:

```text
REQUISITO FÍSICO CONFIRMADO
→ capacidade validada do fluxo M01
→ distribuição no calendário
→ plano PCP
→ ordens de produção
→ execução por etapa
→ testes/qualidade/liberação
→ unidade física
→ pátio
```

## Regra de programação

As 300 unidades **não devem ser rateadas mecanicamente** entre outubro, novembro, dezembro e janeiro.

A distribuição deve resultar da capacidade validada do fluxo produtivo modular, considerando pelo menos:

- roteiro do M01;
- capacidade por etapa/gargalo;
- tempos e lead time completos;
- calendário operacional;
- materiais e restrições;
- produção já iniciada/concluída;
- expedições comprometidas;
- estoque físico atual;
- retornos efetivamente liberáveis;
- reparos efetivamente liberáveis.

Enquanto a capacidade não estiver validada, o estado deve permanecer:

`AGUARDANDO_CAPACIDADE_VALIDADA`.

## Relação com disponibilidade de pátio

O requisito de 300 unidades não significa 300 unidades em pátio em janeiro.

A disponibilidade física precisa ser calculada a partir de unidades rastreáveis:

```text
PÁTIO FÍSICO ATUAL
+ PRODUÇÃO CONCLUÍDA E LIBERADA
+ RETORNOS RECEBIDOS E LIBERADOS
+ REPAROS CONCLUÍDOS E LIBERADOS
- EXPEDIÇÕES/COMPROMISSOS
= DISPONIBILIDADE PROJETADA DE PÁTIO
```

Regras obrigatórias:

- `OP planejada != módulo disponível`;
- `retorno previsto != estoque livre`;
- `reparo concluído sem unidade física reconciliada != estoque disponível`;
- `REGISTRO_EQUIVALENTE != UNIDADE_FISICA`.

## Evidência atual do fluxo

O fluxo produtivo modular de referência possui 17 etapas, porém a base operacional ainda não possui tempos/capacidades completos por etapa nem roteiro operacional M01 cadastrado.

Há evidência parcial de fabricação da estrutura modular de 20 pés em `mt_tempo_fabricacao_estrutura_modular`, mas ela não representa o lead time completo de um M01 e não deve ser extrapolada para capacidade total da fábrica.

## Relação com reparos e qualidade

Na base de reparos existem registros textuais com descrição compatível com `Módulo Habitacional 20pés Amplo`.

No estado verificado em 21/10/2026:

- 10 registros textuais compatíveis estavam concluídos;
- 0 desses registros estava vinculado a `mt_unidades_modulares`;
- portanto, eles são evidência de reparo, não 10 unidades comprovadamente disponíveis.

As tabelas canônicas de inspeção/não conformidade ainda não possuem registros operacionais suficientes para transformar esse conjunto em saldo físico de pátio.

## Fonte runtime

Tabela privada:

`elo_private.pcp_requisitos_fisicos_planejamento`

Read-model:

`public.v_elo_pcp_requisito_fisico_planejamento`

A view deve ser consultada junto de:

`public.v_elo_pcp_demanda_fluxo_patio`

para responder perguntas como:

- quantas unidades M01 faltam para a meta de janeiro/2027?;
- a produção já começou?;
- qual é o GAP que impede programar as 300 unidades?;
- quantos módulos estarão fisicamente disponíveis em pátio?;
- quais dados ainda faltam para responder com precisão?

## Próximos dados aguardados

Ainda devem ser incorporados ao cálculo físico:

1. estoque atual volátil de M01 em pátio;
2. compromissos/expedições de eventos e SPOT;
3. retornos previstos e depois realizados por unidade/modelo;
4. reconciliação dos reparos com unidade física;
5. capacidade validada do fluxo produtivo M01.

Até esses dados existirem, o ELO pode afirmar a meta física de 300 unidades, mas não deve afirmar o saldo final de pátio nem uma distribuição mensal de produção.