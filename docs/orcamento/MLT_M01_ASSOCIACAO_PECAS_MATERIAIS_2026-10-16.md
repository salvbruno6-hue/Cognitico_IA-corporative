# MLT.M01 — Associação de peças aos grupos de matéria-prima

Data: 2026-10-16

## Regra canônica

- `COD_PRODUT` continua sendo a autoridade da matéria-prima comprada.
- `grupo_material` classifica a família física da matéria-prima sem substituir `COD_PRODUT`.
- `grupo_peca` classifica a função da peça fabricada: colunas, longarinas, travessas, suportes, perfis T/Z, conectores, içamento, acabamentos etc.
- `fonte_associacao` preserva a proveniência da associação.
- o peso utilizado na VW de perdas é a **soma do `PESO PEÇAS` das peças associadas ao material**;
- `diferença = peso comprado - peso utilizado`;
- diferença negativa é divergência de apontamento e não perda negativa.

## Associação consolidada

| COD_PRODUT | Grupo de peça | Componentes associados | Peso utilizado associado |
|---|---|---|---:|
| 3200600065 | PERFIS_Z | 4 perfis Z externos 74x2080 + 8 perfis Z externos 74x2820 | 28,335 kg |
| 3200600075 | COLUNAS, PERFIS_Z, SUPORTES | 4 colunas; 8 suportes da travessa; 2 perfis Z laterais superiores; 2 perfis Z frontais superiores | 141,530 kg |
| 3200600100 | ACABAMENTOS | 4 acabamentos de coluna | 10,030 kg — PARCIAL |
| 3200600124 | ACABAMENTOS | 1 acabamento de teto | 2,250 kg |
| 3200600239 | PERFIS_T | 2 perfis T laterais + 2 perfis T frontais | 29,050 kg |
| 3200600260 | CONECTORES, ICAMENTO | conectores U/cantoneiras + triângulos de içamento | 18,820 kg |
| 3200600288 | LONGARINAS | 2 longarinas laterais inferiores UDC 6 | 73,560 kg |
| 3200600289 | LONGARINAS, REFORCOS, TRAVESSAS | longarina frontal inferior, travessas de piso e reforços | 133,780 kg |
| 3200600291 | PERFIS_TELHA | 2 perfis de telha UDC 3 | 12,880 kg |
| 3200600335 | LONGARINAS | longarinas superiores UDC 8 | 91,150 kg |

## Tabela principal de peças

As 23 linhas fornecidas na planilha somam **513,050 kg** em `PESO PEÇAS`. Esse total é distribuído pelos materiais abaixo:

| COD_PRODUT | Peças da tabela principal | Peso |
|---|---|---:|
| 3200600075 | coluna + suporte da travessa + perfis Z superiores | 141,530 kg |
| 3200600288 | longarina UDC 6 | 73,560 kg |
| 3200600289 | longarina UDC 5 + travessas + reforços | 133,780 kg |
| 3200600335 | longarinas UDC 8 | 91,150 kg |
| 3200600291 | perfil de telha UDC 3 | 12,880 kg |
| 3200600239 | perfis T | 29,050 kg |
| 3200600260 | conectores + içamento | 18,820 kg |
| 3200600100 | acabamento de coluna | 10,030 kg |
| 3200600124 | acabamento de teto | 2,250 kg |
| **TOTAL** |  | **513,050 kg** |

O `3200600065` foi informado em apontamento complementar e adiciona **28,335 kg** de perfis Z externos. Assim, o peso utilizado total associado aos 10 materiais é **541,385 kg**.

## Conectores associados ao 3200600260

- Conector U de um furo — 4 peças — 1,29 kg.
- Cantoneira com furo maior / coluna — 8 peças — 2,27 kg.
- Cantoneira com furo maior / base — 4 peças — 1,14 kg.
- Conector U de dois furos — 4 peças — 1,67 kg.
- Triângulo de içamento — 4 peças — 9,76 kg.
- Cantoneira com um furo menor / coluna — 8 peças — 1,79 kg.
- Cantoneira com um furo menor / base — 4 peças — 0,90 kg.

Total do grupo: **18,820 kg**.

## Acabamentos

- `3200600100`: acabamento de coluna — 4 peças — **10,030 kg**. Continua `PARCIAL` porque a compra também referencia acabamento de canto/perfil U ainda não integralmente apontados.
- `3200600124`: acabamento de teto — 1 peça — **2,250 kg** — reconciliado.

## UDC

A VW de perda não normaliza mais os UDC pelo peso da barra de 6 m. Para esta análise, o valor utilizado é o `PESO PEÇAS` fornecido e associado ao material. Portanto:

- `3200600288`: comprado 72,000 kg; utilizado 73,560 kg; diferença **-1,560 kg** — divergência;
- `3200600289`: comprado 116,100 kg; utilizado 133,780 kg; diferença **-17,680 kg** — divergência;
- `3200600291`: comprado 47,754 kg; utilizado 12,880 kg; diferença **34,874 kg**;
- `3200600335`: comprado 108,510 kg; utilizado 91,150 kg; diferença **17,360 kg**.

As views `public.vw_estrutura_metalica_20_associacao_material`, `public.vw_estrutura_metalica_20_material_componentes_resumo` e `public.vw_perda_estrutura_metalica_20` preservam a associação peça → material e deixam a diferença explícita. A BOM não é alterada.
