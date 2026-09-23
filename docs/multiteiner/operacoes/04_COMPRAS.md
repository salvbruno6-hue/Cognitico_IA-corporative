# OPERAÇÃO 04 — COMPRAS

## Papel no fluxo

Transforma excedentes e faltas de materiais em aquisição controlada e acompanha a chegada até que o material possa entrar no estoque.

## Sequência do fluxograma

`Gerar ordem de compra para excedentes → aguardar chegada → retorno ao fluxo de picking`

## Tabelas primárias

- `mt_ordens_compra`
- `mt_ordens_compra_itens`
- `compras_fornecedor`
- `compras_fornecedor_itens`
- `excedentes`
- `excedente_itens`
- `lista_mae`

## O que o especialista deve ensinar

- quando um excedente gera compra;
- como fornecedor é selecionado;
- qual é a data prometida;
- como quantidade pedida e recebida são controladas;
- como atraso de compra é reconhecido;
- quando o item recebido pode ser disponibilizado ao almoxarifado.

## Regra

Pedido de compra não equivale a material disponível. O ELO deve separar solicitado, prometido, recebido e fisicamente disponível.

## Evidência mínima

Ordem/compra, item, quantidade, fornecedor, previsão e recebimento efetivo.

## Saída

Material recebido e rastreável no estoque, ou pendência de suprimento explicitamente localizada.
