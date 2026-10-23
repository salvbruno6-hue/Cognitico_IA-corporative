# ELO MT unit materialization validation — 2026-10-23

## Decisão de negócio aplicada

Foi confirmada a regra canônica de identidade física dos módulos legados:

`MLTM + código de modelo de dois dígitos + sequência individual`

Exemplos:

- `MLTM 010030` → modelo M01, unidade individual 0030;
- `MLTM 020189` → modelo M02, unidade individual 0189;
- `MLTM 09001` → modelo M09, unidade individual 001.

`MLTM` identifica módulo físico Multiteiner. A sequência individual pode ter comprimento variável; os dois primeiros dígitos numéricos após `MLTM` são o código do modelo.

## Operação governada

A reconciliação live no Supabase foi executada com precondições fail-closed:

- exatamente 133 reparos;
- 133/133 identificadores no padrão MLTM numérico;
- nenhum tenant conflitante;
- exatamente 97 identificadores com modelo ativo unívoco;
- exatamente 103 linhas de reparo mapeáveis a esses 97 identificadores;
- exatamente 27 identificadores bloqueados por ausência de modelo canônico.

A operação:

1. materializou 97 unidades em `mt_unidades_modulares`;
2. vinculou as 97 unidades ao tenant `MULTITEINER`;
3. persistiu `tenant_id = MULTITEINER` nos 133 reparos;
4. vinculou 103 reparos às unidades canônicas via `unidade_modular_id`;
5. manteve 30 reparos sem `unidade_modular_id`, correspondentes a 27 unidades M14/M15/M16 sem modelo canônico no catálogo;
6. não criou modelos, proveniência, ordens de produção, pedidos, localizações, permissões ou políticas.

## Validação live posterior

- `mt_unidades_modulares`: 97;
- reparos Multiteiner: 133/133;
- reparos com unidade física: 103/133;
- reparos sem unidade física: 30/133;
- identificadores físicos materializados: 97/124;
- identificadores bloqueados: 27/124;
- unidades disponíveis para montagem: 0;
- unidades disponíveis para expedição: 0;
- unidades com ordem de produção inventada: 0;
- unidades com pedido inventado: 0;
- unidades com localização inventada: 0.

Todos os registros materializados permanecem fail-closed nos defaults existentes: `EM_PREPARACAO`, `NAO_INSPECIONADO`, sem disponibilidade operacional.

## Bloqueio residual

O bloqueio de unidade física não está mais relacionado a tenant ou ao parser MLTM. Está concentrado exclusivamente no catálogo de modelos:

- M14: 21 unidades / 24 reparos;
- M15: 5 unidades / 5 reparos;
- M16: 1 unidade / 1 reparo.

Esses 30 reparos já pertencem formalmente ao tenant Multiteiner, mas não recebem `unidade_modular_id` até existir `modelo_id` canônico obrigatório.

## Proveniência

A reconciliação de identidade física não fabrica linhagem histórica. Os 133 reparos continuam sem proveniência linha a linha em `mt_proveniencia_registros`.

Estado governado após validação:

`TENANT_RECONCILED_UNIT_PARTIAL_PROVENANCE_PENDING`
