# OPERAÇÃO 01 — LOCAÇÃO / COMERCIAL

## Papel no fluxo

Ponto de entrada do processo integrado. Recebe a solicitação/AF, identifica a demanda e entrega ao planejamento uma necessidade operacional suficientemente definida.

## Sequência do fluxograma

`Início → Recebimento de AF → análise da demanda → devolução/projeto`

## Dados que precisam existir

- cliente e localização;
- pedido/origem;
- modelo ou família;
- quantidade;
- data solicitada;
- indicação de personalização;
- requisitos que alterem escopo;
- status do gate de PCP.

## Tabelas primárias

- `mt_pedidos_venda`
- `mt_pedidos_venda_itens`
- `mt_contratos_locacao`
- `modelos`

## O que o especialista deve ensinar ao ELO

1. Como uma AF chega e é formalizada.
2. Quais informações são obrigatórias para o PCP.
3. O que caracteriza módulo padrão versus personalizado.
4. Quais informações podem mudar o fluxo, prazo ou materiais.
5. Qual evento autoriza o envio ao planejamento.

## Regra de inserção

O ELO deve perguntar campo a campo quando a fonte não estiver estruturada. Não deve completar cliente, quantidade, prazo, modelo ou personalização por plausibilidade.

## Saída para a próxima operação

Uma demanda identificada, rastreável e pronta para análise do planejamento.

## Evidência mínima

Documento/registro da AF, pedido, item do pedido, projeto aprovado quando aplicável e informação explícita do especialista.

## Estado sem evidência

`DADOS_INCOMPLETOS` — o ELO deve apontar a tabela, campo, responsável e pergunta necessária.
