# MLT.M01 — Associação de peças aos grupos de matéria-prima

Data: 2026-10-16

## Regra canônica

- `COD_PRODUT` continua sendo a autoridade da matéria-prima comprada.
- `grupo_material` classifica a família física da matéria-prima sem substituir `COD_PRODUT`.
- `grupo_peca` classifica a função da peça fabricada: colunas, longarinas, travessas, suportes, perfis T/Z, conectores, içamento, acabamentos etc.
- `fonte_associacao` preserva a proveniência da associação.
- A VW de perda continua decidindo o peso aplicado oficial; para UDC, a base oficial permanece normalizada pela barra comprada de 6 m.

## Associação consolidada

| COD_PRODUT | Grupo de peça | Componentes associados | Peso das peças da planilha | Peso aplicado oficial |
|---|---|---|---:|---:|
| 3200600065 | PERFIS_Z | 4 perfis Z externos 74x2080 + 8 perfis Z externos 74x2820 | 28,335 kg | 28,335 kg |
| 3200600075 | COLUNAS, PERFIS_Z, SUPORTES | 4 colunas; 8 suportes da travessa; 2 perfis Z laterais superiores; 2 perfis Z frontais superiores | 141,520 kg | 141,530 kg |
| 3200600100 | ACABAMENTOS | 4 acabamentos de coluna | 10,030 kg | 10,030 kg — PARCIAL |
| 3200600124 | ACABAMENTOS | 1 acabamento de teto | 2,250 kg | 2,250 kg |
| 3200600239 | PERFIS_T | 2 perfis T laterais + 2 perfis T frontais | 29,050 kg | 29,050 kg |
| 3200600260 | CONECTORES, ICAMENTO | conectores U/cantoneiras + triângulos de içamento | 18,820 kg | 18,820 kg |
| 3200600288 | LONGARINAS | 2 longarinas laterais inferiores UDC 6 | 73,560 kg | 72,000 kg |
| 3200600289 | LONGARINAS, REFORCOS, TRAVESSAS | longarina frontal inferior, travessas de piso e reforços | 133,780 kg | 112,574 kg |
| 3200600291 | PERFIS_TELHA | 2 perfis de telha UDC 3 | 12,880 kg | 12,894 kg |
| 3200600335 | LONGARINAS | longarinas superiores UDC 8 | 91,150 kg | 101,758 kg |

## Conectores associados ao 3200600260

- Conector U de um furo — 4 peças — 1,29 kg.
- Cantoneira com furo maior / coluna — 8 peças — 2,27 kg.
- Cantoneira com furo maior / base — 4 peças — 1,14 kg.
- Conector U de dois furos — 4 peças — 1,67 kg.
- Triângulo de içamento — 4 peças — 9,76 kg.
- Cantoneira com um furo menor / coluna — 8 peças — 1,79 kg.
- Cantoneira com um furo menor / base — 4 peças — 0,90 kg.

Total do grupo: **18,82 kg**.

## Acabamentos

- `3200600100`: acabamento de coluna — 4 peças — 10,03 kg. O material permanece `PARCIAL` na VW de perda porque a compra também referencia acabamento de canto/perfil U ainda não integralmente apontado.
- `3200600124`: acabamento de teto — 1 peça — 2,25 kg — reconciliado.

## Diferença entre peso da planilha e peso oficial

A associação de peças não altera a regra física de cálculo já validada. Nos perfis UDC, `peso_pecas` da planilha e massa comprada usam bases diferentes; por isso o peso oficial da perda continua calculado por `peso_barra_6m / 6 × comprimento_aplicado`.

As views `public.vw_estrutura_metalica_20_associacao_material` e `public.vw_estrutura_metalica_20_material_componentes_resumo` tornam essa diferença explícita, preservando o dado bruto da planilha e o peso oficial usado na análise de perda.