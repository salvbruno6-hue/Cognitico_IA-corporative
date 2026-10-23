# ELO MT unit materialization readiness — 2026-10-23

## Objetivo

Separar os identificadores físicos legados presentes em `mt_ordens_reparo` entre candidatos estruturais à materialização em `mt_unidades_modulares` e casos ainda bloqueados por ausência de modelo canônico.

## Estado live validado

- 133 ordens de reparo;
- 124 identificadores `MLTM...` distintos;
- `mt_unidades_modulares`: 0 registros;
- 97/124 identificadores possuem modelo ativo canônico reconhecido por normalização `Mxx` / `MLT.Mxx`;
- 27/124 permanecem bloqueados por ausência de modelo canônico correspondente.

### Candidatos estruturais

97 identificadores estão em `CANDIDATE_MODEL_MATCH`, distribuídos pelos códigos parseados:

- M01
- M02
- M04
- M05
- M06
- M09
- M10
- M18
- M20

Nenhum deles já está materializado em `mt_unidades_modulares`.

### Bloqueados

27 identificadores estão em `BLOCKED_MODEL_GAP`:

- M14: 21 unidades distintas / 24 reparos;
- M15: 5 unidades distintas / 5 reparos;
- M16: 1 unidade distinta / 1 reparo.

M14 possui evidência textual legado parcialmente associada a `Sanitário 7 Vasos`; M15 a `Sanitário 9 Mictórios`; M16 não possui evidência textual suficiente. Esses indícios não são usados para criar modelos automaticamente.

## Contrato real de `mt_unidades_modulares`

Campos obrigatórios para uma unidade física:

- `tenant_id`;
- `modelo_id`;
- `codigo_unidade`.

Campos de ordem de produção, pedido de venda e localização podem permanecer nulos. Defaults existentes preservam estado conservador:

- `status = EM_PREPARACAO`;
- `status_qualidade = NAO_INSPECIONADO`;
- `disponivel_montagem = false`;
- `disponivel_expedicao = false`.

Existe unicidade por `(tenant_id, codigo_unidade)`.

## Limite de governança

`CANDIDATE_MODEL_MATCH` não significa autorização automática para inserir a unidade. Materializar os 97 identificadores faria o ELO adotar o parser `MLTM + código de modelo + sequência` como regra canônica de identidade física para os registros legados.

Esse passo deve ser tratado como decisão de semântica de negócio, não como simples correção técnica.

Até essa decisão:

- nenhum registro é criado em `mt_unidades_modulares`;
- nenhum `unidade_modular_id` é preenchido em `mt_ordens_reparo`;
- nenhum `tenant_id` de reparo é alterado;
- nenhuma proveniência histórica é fabricada;
- M14/M15/M16 permanecem bloqueados.

## Probe

`supabase/health/elo_mt_unit_materialization_readiness.sql` classifica cada identificador distinto como:

- `CANDIDATE_MODEL_MATCH`;
- `ALREADY_MATERIALIZED`;
- `BLOCKED_MODEL_GAP`.

O probe é somente leitura.
