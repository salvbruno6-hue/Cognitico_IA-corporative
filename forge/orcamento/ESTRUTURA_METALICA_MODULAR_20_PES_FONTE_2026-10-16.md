# Forge — Estrutura metálica modular 20 pés — fonte de perda

## Status

Fonte validada pelo usuário em 2026-10-16 para a **estrutura metálica modular padrão de 20 pés**.

**Escopo canônico:** `Todos os módulos 20 pés` que utilizem esta estrutura. O dado não pertence exclusivamente ao MLT.M01/M01; o M01 é apenas um dos modelos que consomem esta estrutura.

A regra oficial desta fonte é:

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

- Peso total comprado: **652.530 kg**.
- Saldo líquido: **78.955 kg**.
- Divergências negativas: **19.240 kg** (`3200600288 = -1.560 kg`; `3200600289 = -17.680 kg`).
- Diferenças positivas somadas: **98.195 kg**.
- Percentual de perda: **15.05%**.
- Impacto financeiro canônico, com precisão antes do arredondamento final: **R$ 872,90**.
- Soma dos impactos já arredondados linha a linha na VW: **R$ 872,89**.

## Item canônico

| Código | Descrição | UN | Quantidade | Valor unitário | Valor total | Curva | Obrig. | Modelos aplicáveis |
|---|---|---|---:|---:|---:|---|---|---|
| PERDA-EST-MET | Perda de matéria-prima da estrutura metálica modular 20 pés | % | 15.05 | R$ 872,90 | R$ 872,90 | A | P | Todos os módulos 20 pés |

## Memória cognitiva

A memória está registrada em `public.elo_orcamento_memoria` com:

- `conceito_key = PERDA_ESTRUTURA_METALICA_MODULAR_20_PES`;
- `classificacao = PRECEDENT`;
- `status_conceito = VALIDADA`;
- confiança `1.0`;
- escopo `TODOS_OS_MODULOS_20_PES`.

## Referência operacional

- Supabase migration: `20261016175407_generaliza_perda_est_met_todos_modulos_20_e_memoria.sql`
- VW: `public.vw_perda_estrutura_metalica_20`
- Componentes: `public.estrutura_metalica_20_componentes`
- Memória: `public.elo_orcamento_memoria`
- Identidade do item: `public.lista_mae`
- O vínculo atual em `KIT-M01` representa o uso no M01; a regra e o item são transversais a todos os módulos 20 pés. A propagação para outros kits deve respeitar a composição de cada modelo e não é feita por duplicação automática desta fonte.
