# ELO MT unit materialization readiness — 2026-10-23

## Objetivo

Governar a reconciliação dos identificadores físicos legados de `mt_ordens_reparo` com `mt_unidades_modulares`, preservando bloqueios onde o catálogo canônico de modelos ainda não permite materialização segura.

## Regra de identidade confirmada

A semântica de negócio foi explicitamente confirmada pelo usuário:

- `MLTM` identifica uma unidade modular física da Multiteiner;
- os dois primeiros dígitos após `MLTM` identificam o modelo (`01` = M01 Amplo, `02` = M02 Suíte e assim por diante conforme catálogo); 
- os dígitos restantes identificam individualmente a unidade dentro do modelo;
- a quantidade de dígitos da sequência individual não precisa ser fixa, portanto `MLTM 09001` continua sendo uma identidade válida do modelo M09.

A forma persistida de `codigo_unidade` é normalizada como `MLTM <parte numérica>`, preservando o conteúdo numérico original.

## Estado live após reconciliação

- 133 ordens de reparo;
- 124 identificadores `MLTM...` distintos;
- 133/133 reparos vinculados ao tenant `MULTITEINER`;
- 97 unidades físicas materializadas em `mt_unidades_modulares`;
- 103/133 reparos ligados por `unidade_modular_id` à unidade física canônica;
- 30/133 reparos permanecem sem unidade canônica porque o modelo correspondente ainda não existe no catálogo;
- 27/124 identificadores permanecem bloqueados por modelo ausente.

### Unidades materializadas

As 97 unidades materializadas pertencem aos códigos de modelo já reconhecidos de forma unívoca no catálogo ativo:

- M01
- M02
- M04
- M05
- M06
- M09
- M10
- M18
- M20

Cada código possuía exatamente uma correspondência ativa em `modelos` durante a reconciliação.

### Bloqueados

Os 27 identificadores ainda bloqueados são:

- M14: 21 unidades distintas / 24 reparos;
- M15: 5 unidades distintas / 5 reparos;
- M16: 1 unidade distinta / 1 reparo.

A identidade física desses registros é reconhecida como Multiteiner e o `tenant_id` já está persistido, porém `mt_unidades_modulares.modelo_id` é obrigatório. Portanto eles não são materializados até que M14/M15/M16 tenham representação canônica no catálogo de modelos.

Evidência textual legado associa parcialmente M14 a `Sanitário 7 Vasos` e M15 a `Sanitário 9 Mictórios`; M16 permanece sem descrição suficiente. Esses indícios não autorizam criação automática de modelos.

## Estado conservador das unidades materializadas

Nenhuma origem operacional foi inventada. As 97 unidades foram criadas sem ordem de produção, pedido de venda ou localização e mantêm os defaults conservadores existentes:

- `status = EM_PREPARACAO`;
- `status_qualidade = NAO_INSPECIONADO`;
- `disponivel_montagem = false`;
- `disponivel_expedicao = false`;
- `ordem_producao_id = null`;
- `pedido_venda_item_id = null`;
- `local_atual_id = null`.

Esses campos não devem ser interpretados como reconstrução histórica do estado real do módulo; são apenas o estado inicial fail-closed da entidade canônica.

## Governança de tenant

A confirmação de que `MLTM` identifica módulos da Multiteiner, combinada com o tenant operacional `MULTITEINER` já estabelecido, encerra o GAP de tenant para os 133 reparos. Isso não cria nem altera identidade de usuário, `elo_scopes`, memberships ou RLS.

## Proveniência

A materialização da identidade física não fabrica proveniência histórica. `mt_proveniencia_registros` continua sem linhagem linha a linha para esses 133 reparos. O GAP de proveniência permanece separado e aberto.

## Probe

`supabase/health/elo_mt_unit_materialization_readiness.sql` continua classificando os identificadores como:

- `ALREADY_MATERIALIZED` para as 97 unidades reconciliadas;
- `BLOCKED_MODEL_GAP` para as 27 unidades M14/M15/M16.

O probe permanece somente leitura.
