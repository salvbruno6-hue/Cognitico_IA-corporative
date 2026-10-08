# OPERAÇÃO 03 — ALMOXARIFADO

## Papel no fluxo

Recebe, confere, registra, armazena e disponibiliza materiais e kits para a execução.

## Sequência do fluxograma

`Gate logístico → recebimento/conferência → packing → registro no CD → verificar excedente → picking → kits → verificar base móvel`

## Tabelas primárias

- `mt_locais`
- `mt_lotes_estoque`
- `mt_movimentacoes_estoque`
- `lista_mae`
- `kits`
- `kit_itens`
- `mt_ordens_compra_itens`

## O que o especialista deve ensinar

- como um material é recebido;
- como lote/serial é identificado;
- como ocorre a conferência;
- quais locais representam CD, estoque, picking e base móvel;
- como ocorre a separação;
- como kits são montados;
- como uma movimentação é registrada;
- quais bloqueios impedem disponibilização.

## Regra de estoque

Saldo disponível, reservado e movimentado devem permanecer distintos. O ELO não deve considerar material disponível apenas porque existe uma linha de compra.

## Evidência mínima

Documento de recebimento/conferência, lote, local, quantidade e movimentação registrada.

## Saída

Material fisicamente identificado e disponível para o processo seguinte, ou gap explicitamente registrado.
