# Forge — MLT.M01 — Fonte de perda da estrutura metálica

## Status

Fonte validada pelo usuário em 2026-10-16 para o módulo MLT.M01 / M01 — Habitacional Amplo 20 pés.

Esta fonte substitui interpretações anteriores baseadas em normalização de perfis para fins da VW de perdas. A regra oficial desta fonte é:

1. associar cada peça ao `COD_PRODUT` da matéria-prima;
2. somar `PESO PEÇAS` por matéria-prima;
3. calcular `peso_comprado - peso_utilizado`;
4. saldo negativo = divergência / insuficiência de apontamento, não perda negativa;
5. diferenças negativas não compensam diferenças positivas;
6. `PERDA-EST-MET` usa a soma financeira das diferenças positivas.

## Fonte principal de peças

| COD_PRODUT | Grupo / peças | Peso utilizado (kg) |
|---|---|---:|
| 3200600075 | Coluna esquerda + coluna direita + perfis Z superiores + suporte da travessa | 141.520 |
| 3200600288 | Longarina lateral inferior UDC 6" | 73.560 |
| 3200600289 | Longarina frontal inferior + reforços + travessa de piso UDC 5" | 133.780 |
| 3200600335 | Longarinas superiores UDC 8" | 91.150 |
| 3200600291 | Travessas de telha UDC 3" | 45.080 |
| 3200600239 | Perfis T lateral e frontal | 29.050 |
| 3200600260 | Conectores + triângulo de içamento | 18.820 |
| 3200600100 | Acabamento de coluna | 10.030 |
| 3200600124 | Acabamento de teto | 2.250 |

Total da tabela principal: **545.240 kg**.

## Complemento validado

| COD_PRODUT | Grupo / peças | Peso utilizado (kg) |
|---|---|---:|
| 3200600065 | Perfis Z externos frontal e lateral em chapa 1,55 mm | 28.335 |

Total utilizado associado, incluindo complemento: **573.575 kg**.

## Compra e diferenças

Peso total comprado: **652.530 kg**.

Diferenças negativas identificadas:

- `3200600288`: **-1.560 kg**;
- `3200600289`: **-17.680 kg**.

Essas divergências não reduzem a perda bruta positiva.

Diferenças positivas somadas: **98.195 kg**.

Percentual sobre o peso comprado: **15.05%**.

Impacto financeiro com precisão por material e arredondamento final: **R$ 872,90**.

A soma dos impactos já arredondados linha a linha na VW resulta em R$ 872,89; o item `PERDA-EST-MET` utiliza o cálculo com precisão antes do arredondamento final.

## Item promovido

| Código | Descrição | UN | Quantidade | Valor unitário | Valor total | Curva | Obrig. | Aplicação |
|---|---|---|---:|---:|---:|---|---|---|
| PERDA-EST-MET | Perda de matéria-prima da estrutura metálica 20 pés | % | 15.05 | R$ 872,90 | R$ 872,90 | A | P | Perda/aproveitamento de aço no corte e fabricação |

## Referência operacional

- Supabase migration: `20261016172338_m01_promove_perda_est_met_fonte_forge.sql`
- VW: `public.vw_perda_estrutura_metalica_20`
- Componentes: `public.estrutura_metalica_20_componentes`
- Identidade do item: `public.lista_mae`
- Composição M01: `public.kit_itens` / `KIT-M01`
