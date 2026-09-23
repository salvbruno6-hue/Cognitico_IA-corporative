# OPERAÇÃO 02 — PLANEJAMENTO

## Papel no fluxo

Transforma a demanda recebida em uma configuração operacional: padrão ou personalizada, lista-mãe/estrutura necessária, roteiro e ordens de produção/reparo.

## Sequência do fluxograma

`Analisar AF → módulo padrão ou personalizado → gerar L.M. e O.S. → enviar lista de excedentes → eventualmente gerar O.S. de reparo`

## Tabelas primárias

- `mt_planos_pcp`
- `mt_linhas_plano_pcp`
- `mt_versoes_roteiro_personalizado`
- `mt_operacoes_roteiro_personalizado`
- `lista_mae`
- `kits`
- `kit_itens`
- `excedentes`
- `excedente_itens`
- `excedente_mao_obra`
- `mt_ordens_reparo`

## O que o especialista deve ensinar

- critérios de padrão/personalização;
- como a L.M. é formada;
- como o roteiro padrão é escolhido;
- como uma personalização altera o roteiro;
- como excedente é identificado;
- quando uma necessidade vira compra;
- quando uma falha vira ordem de reparo;
- quais gates precisam de aprovação humana.

## Regra de decisão

O ELO não escolhe automaticamente entre padrão e personalizado sem evidência do pedido/projeto ou regra validada.

## Planejamento × execução

Planejamento registra intenção, datas, quantidades e configuração. Execução será registrada nas tabelas operacionais correspondentes. Nunca substituir realizado por planejado.

## Saída

Plano e instruções operacionais rastreáveis para almoxarifado, compras, produção e reparo.

## Evidência mínima

Pedido/item, projeto, modelo, roteiro, lista-mãe, aprovação e justificativa para exceções.
