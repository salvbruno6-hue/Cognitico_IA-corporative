# MLT.M01 — Memória de cálculo da perda de estrutura metálica

Data de reconciliação: 2026-10-16  
Escopo: **estrutura metálica** do MLT.M01.  
Não inclui telha, drenagem, pintura, fechamentos ou demais componentes da estrutura modular.  
Esta reconciliação **não altera a BOM** e não promove automaticamente o item `PERDA-EST-MET`.

## Fontes validadas neste ciclo

- tabela de compra com 10 matérias-primas;
- tabela integral de peças fabricadas/aplicadas;
- validação do analista de que, para perfis UDC, `Peso un.` da compra é o peso da barra inteira de 6 m;
- apontamento complementar dos perfis Z externos em chapa 1,55 mm;
- confirmação de que a compra de 2,88 kg do COD `3200600124` corresponde ao acabamento de forro do teto.

## Regra de cálculo

- `saldo_kg = peso_comprado_kg - peso_aplicado_kg`;
- `% perda = saldo_kg / peso_comprado_kg * 100`;
- `impacto_rs = saldo_kg * custo_rs_kg`;
- perda bruta validada soma somente saldo positivo com `status_dado = RECONCILIADO`;
- material `PARCIAL` permanece visível, mas não integra `PERDA-EST-MET` até completar o apontamento;
- perfis UDC usam `peso_barra_6m / 6 * comprimento_aplicado` para equalizar a base física entre compra e fabricação.

## Reconciliação por material

| COD_PRODUTO | Peso comprado kg | Peso aplicado kg | Saldo kg | % saldo | R$/kg | Impacto R$ | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| 3200600291 | 47,754 | 12,894 | 34,860 | 73,00% | 8,12 | 283,07 | RECONCILIADO |
| 3200600289 | 116,100 | 112,574 | 3,526 | 3,04% | 8,12 | 28,63 | RECONCILIADO |
| 3200600288 | 72,000 | 72,000 | 0,000 | 0,00% | 8,12 | 0,00 | RECONCILIADO |
| 3200600335 | 108,510 | 101,758 | 6,752 | 6,22% | 8,12 | 54,82 | RECONCILIADO |
| 3200600075 | 147,744 | 141,530 | 6,214 | 4,21% | 7,78 | 48,34 | RECONCILIADO |
| 3200600239 | 56,160 | 29,050 | 27,110 | 48,27% | 8,78 | 238,03 | RECONCILIADO |
| 3200600260 | 27,942 | 18,820 | 9,122 | 32,65% | 6,00 | 54,73 | RECONCILIADO |
| 3200600124 | 2,880 | 2,250 | 0,630 | 21,88% | 21,21 | 13,36 | RECONCILIADO |
| 3200600065 | 44,640 | 28,335 | 16,305 | 36,52% | 8,00 | 130,44 | RECONCILIADO |
| 3200600100 | 28,800 | 10,030 | 18,770 | 65,17% | 12,00 | 225,24 | PARCIAL |

## Indicadores

- peso comprado em precisão de cálculo: **652,530 kg**;
- peso comprado consolidado arredondado informado: **652,5 kg**;
- peso aplicado/apontado atual: **529,241 kg**;
- perda bruta **validada** (somente reconciliados positivos): **104,519 kg**;
- impacto financeiro **validado**: **R$ 851,42**;
- percentual validado sobre peso comprado: **16,02%**;
- percentual financeiro validado sobre compra de R$ 5.370,13: **15,85%**;
- saldo total apontado, incluindo `3200600100` parcial: **123,289 kg / R$ 1.076,66** — indicador potencial/gerencial, não elegível integralmente para `PERDA-EST-MET`.

## Pendência remanescente

`3200600100 — CHAPA PRIMER BRANCA 0,50mm`: 10,03 kg estão comprovados como acabamento de coluna, porém a aplicação da compra também cita acabamento de canto e perfil U. O saldo de 18,77 kg permanece `PARCIAL` até o apontamento completo dessas peças ou confirmação explícita de que não foram utilizadas.

## Alteração de dados deste ciclo

`estrutura_metalica_20_componentes.PRTH01` foi corrigido de 7 para 2 peças, com peso de peças 12,88 kg e valor total R$ 104,58, conforme tabela integral fornecida.

A `public.vw_perda_estrutura_metalica_20` passou a conter os 10 materiais, `status_dado`, `metodo_calculo`, `elegivel_perda` e `impacto_validado_rs`, com `security_invoker = true`.
