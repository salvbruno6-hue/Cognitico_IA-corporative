# MLT.M01 — Memória de cálculo da perda de estrutura metálica

Data de reconciliação: 2026-10-16  
Escopo: **estrutura metálica** do MLT.M01.  
Não inclui telha, drenagem, pintura, fechamentos ou demais componentes da estrutura modular.  
Esta reconciliação **não altera a BOM** e não promove automaticamente o item `PERDA-EST-MET`.

## Fontes validadas

- tabela de compra com 10 matérias-primas e **652,530 kg** em precisão de cálculo;
- tabela de 23 linhas de peças fabricadas com **513,050 kg** em `PESO PEÇAS`;
- associação explícita de cada peça ao `COD_PRODUT` da matéria-prima;
- apontamento complementar dos perfis Z externos em chapa 1,55 mm: **28,335 kg**;
- confirmação de que `3200600124` corresponde ao acabamento de teto de **2,250 kg**;
- `3200600100` permanece parcial: **10,030 kg** comprovados de acabamento de coluna.

## Regra canônica de cálculo

A VW de perda passa a usar diretamente o peso das peças associadas ao material:

1. associar cada peça ao `COD_PRODUT` da matéria-prima;
2. `peso_utilizado_kg = soma(PESO PEÇAS)` por `COD_PRODUT`;
3. `diferenca_kg = peso_comprado_kg - peso_utilizado_kg`;
4. `% diferenca = diferenca_kg / peso_comprado_kg * 100`;
5. `impacto_rs = diferenca_kg * custo_rs_kg`;
6. diferença negativa = **DIVERGÊNCIA / INSUFICIÊNCIA DE APONTAMENTO**, nunca perda negativa;
7. perda bruta validada soma somente diferenças positivas com `status_dado = RECONCILIADO`;
8. diferenças negativas não compensam diferenças positivas na perda bruta;
9. material `PARCIAL` fica visível, mas não integra `PERDA-EST-MET` até o apontamento ser fechado.

A normalização anterior de UDC por peso da barra de 6 m fica **superada para esta VW de perdas**. O peso da barra pode continuar como dado diagnóstico, mas o peso utilizado oficial desta análise é o `PESO PEÇAS` associado ao material.

## Associação e diferença por material

| COD_PRODUTO | Peso comprado kg | Peso utilizado kg | Diferença kg | % diferença | R$/kg | Impacto R$ | Classificação | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 3200600291 | 47,754 | 12,880 | 34,874 | 73,03% | 8,12 | 283,18 | SOBRA ALTA | RECONCILIADO |
| 3200600289 | 116,100 | 133,780 | -17,680 | -15,23% | 8,12 | -143,56 | DIVERGÊNCIA / INSUFICIÊNCIA | RECONCILIADO |
| 3200600288 | 72,000 | 73,560 | -1,560 | -2,17% | 8,12 | -12,67 | DIVERGÊNCIA / INSUFICIÊNCIA | RECONCILIADO |
| 3200600335 | 108,510 | 91,150 | 17,360 | 16,00% | 8,12 | 140,96 | SOBRA RELEVANTE | RECONCILIADO |
| 3200600075 | 147,744 | 141,530 | 6,214 | 4,21% | 7,78 | 48,34 | SOBRA | RECONCILIADO |
| 3200600239 | 56,160 | 29,050 | 27,110 | 48,27% | 8,78 | 238,03 | SOBRA ALTA | RECONCILIADO |
| 3200600260 | 27,942 | 18,820 | 9,122 | 32,65% | 6,00 | 54,73 | SOBRA ALTA | RECONCILIADO |
| 3200600124 | 2,880 | 2,250 | 0,630 | 21,88% | 21,21 | 13,36 | SOBRA RELEVANTE | RECONCILIADO |
| 3200600065 | 44,640 | 28,335 | 16,305 | 36,53% | 8,00 | 130,44 | SOBRA ALTA | RECONCILIADO |
| 3200600100 | 28,800 | 10,030 | 18,770 | 65,17% | 12,00 | 225,24 | PENDENTE / PARCIAL | PARCIAL |

## Fechamento de massa

- tabela principal de 23 peças: **513,050 kg**;
- perfis Z externos complementares `3200600065`: **28,335 kg**;
- peso utilizado/apontado total: **541,385 kg**;
- peso comprado total: **652,530 kg**;
- diferença líquida `comprado - utilizado`: **111,145 kg**;
- divergências negativas: **-19,240 kg** (`3200600289` + `3200600288`);
- diferenças positivas totais, incluindo `3200600100` parcial: **130,385 kg**;
- perda bruta validada, excluindo divergências e o parcial: **111,615 kg**;
- impacto financeiro validado pela VW: **R$ 909,04**;
- perda bruta validada / peso comprado: **17,10%**;
- impacto validado / compra de R$ 5.370,13: **16,93%**.

A diferença líquida é um indicador gerencial de balanço de massa. Para perda bruta não se compensam diferenças positivas com diferenças negativas.

## Pendência remanescente

`3200600100 — CHAPA PRIMER BRANCA 0,50mm`: **10,030 kg** estão comprovados como acabamento de coluna. Como a aplicação da compra também cita acabamento de canto e perfil U, a diferença de **18,770 kg / R$ 225,24** permanece `PARCIAL` e não é elegível para `PERDA-EST-MET` enquanto o apontamento não for fechado.

## Implementação

A `public.vw_perda_estrutura_metalica_20` usa `SOMA_PESO_PECAS_ASSOCIADAS`, mantém `security_invoker = true`, expõe `status_dado`, `metodo_calculo`, `elegivel_perda` e `impacto_validado_rs`, e classifica diferenças negativas como divergência. A BOM não foi alterada.
