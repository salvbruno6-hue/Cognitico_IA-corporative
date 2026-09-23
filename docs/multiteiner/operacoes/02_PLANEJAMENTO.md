# OPERAÇÃO 02 — PLANEJAMENTO

## Papel no fluxo

Transforma a demanda recebida em uma configuração operacional: padrão ou personalizada, lista-mãe/estrutura necessária, roteiro e ordens de produção/reparo.

## Sequência do fluxograma

`Analisar AF → módulo padrão ou personalizado → gerar L.M. e O.S. → enviar lista de excedentes → eventualmente gerar O.S. de reparo`

## Ponto crítico: fabricação customizada

A decisão **padrão × customizado** é uma decisão de planejamento que altera o caminho posterior da produção.

Quando o item é customizado, o ELO deve preservar a cadeia:

`pedido/item → evidência da customização → versão do roteiro personalizado → operações personalizadas → aprovação → produção`

Não é permitido registrar uma customização apenas porque o especialista considera que “é diferente”. O motivo, origem e aprovação devem ser identificáveis.

### Tabelas diretamente envolvidas

- `mt_pedidos_venda_itens`
- `mt_versoes_roteiro_personalizado`
- `mt_operacoes_roteiro_personalizado`
- `mt_planos_pcp`
- `mt_linhas_plano_pcp`
- `mt_ordens_producao`

### Perguntas ao especialista

1. Qual característica da AF/projeto determina que o módulo será customizado?
2. Onde essa característica é documentada?
3. Quem valida a customização?
4. Como a versão personalizada é identificada?
5. Como se decide quais operações padrão permanecem?
6. Como novas operações são descritas?
7. Como materiais adicionais entram na L.M.?
8. Como o prazo e a capacidade são reavaliados?
9. Qual aprovação libera a fabricação?
10. Como uma mudança posterior na customização é versionada?

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
