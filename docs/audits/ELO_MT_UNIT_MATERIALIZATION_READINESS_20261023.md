# ELO MT unit materialization readiness — 2026-10-23

## Objetivo

Governar a reconciliação dos identificadores físicos legados de `mt_ordens_reparo` com `mt_unidades_modulares`, preservando bloqueios apenas onde o catálogo canônico de modelos ainda não permite materialização segura.

## Regra de identidade confirmada

A semântica de negócio foi explicitamente confirmada pelo usuário:

- `MLTM` identifica uma unidade modular física da Multiteiner;
- os dois primeiros dígitos após `MLTM` identificam o modelo (`01` = M01 Amplo, `02` = M02 Suíte e assim por diante conforme catálogo);
- os dígitos restantes identificam individualmente a unidade dentro do modelo;
- a quantidade de dígitos da sequência individual não precisa ser fixa, portanto `MLTM 09001` continua sendo uma identidade válida do modelo M09.

A forma persistida de `codigo_unidade` é normalizada sem alterar a parte numérica da identidade.

## Estado live após promoção M14/M15

- 133 ordens de reparo;
- 124 identificadores `MLTM...` distintos;
- 133/133 reparos vinculados ao tenant `MULTITEINER`;
- 123 unidades físicas materializadas em `mt_unidades_modulares`;
- 132/133 reparos ligados por `unidade_modular_id` à unidade física canônica;
- 1/133 reparo permanece sem unidade canônica;
- 1/124 identificador permanece bloqueado por ausência de modelo canônico: M16.

## Promoção de M14 e M15

A evidência legada foi reavaliada antes da promoção.

### M14

- 24 reparos;
- 21 unidades distintas;
- 22 linhas possuem `tipo_modulo` preenchido;
- existe exatamente 1 nome não nulo distinto: `Módulo Habitacional 20pés Sanitário 7 Vasos`;
- nenhum nome conflitante foi encontrado.

Foi criado o modelo ativo `MLT.M14` com esse nome e as 21 unidades foram materializadas.

### M15

- 5 reparos;
- 5 unidades distintas;
- 3 linhas possuem `tipo_modulo` preenchido;
- existe exatamente 1 nome não nulo distinto: `Módulo Habitacional 20pés Sanitário 9 Mictórios`;
- nenhum nome conflitante foi encontrado.

Foi criado o modelo ativo `MLT.M15` com esse nome e as 5 unidades foram materializadas.

Nenhum tempo padrão, BOM, custo, dimensão, localização, ordem de produção ou disponibilidade foi inferido durante essa promoção.

## Bloqueio remanescente — M16

Existe somente uma unidade M16 nos reparos:

- `MLTM 160082`;
- `tipo_modulo = null`;
- `tipo_reparo = MANUTENCAO/REPARO`;
- status de reparo `CONCLUIDA`;
- observação disponível: `Status fonte: Pátio de ok`.

Essa evidência confirma a identidade física M16, mas não informa nome/configuração suficiente para criar um modelo canônico. Portanto:

- M16 não foi criado no catálogo;
- `MLTM 160082` permanece sem registro em `mt_unidades_modulares`;
- seu reparo permanece sem `unidade_modular_id`;
- o tenant `MULTITEINER` permanece corretamente vinculado.

## Estado conservador das unidades materializadas

As unidades materializadas não recebem reconstrução histórica inventada. Permanecem com defaults fail-closed:

- `status = EM_PREPARACAO`;
- `status_qualidade = NAO_INSPECIONADO`;
- `disponivel_montagem = false`;
- `disponivel_expedicao = false`;
- `ordem_producao_id = null` quando não há evidência;
- `pedido_venda_item_id = null` quando não há evidência;
- `local_atual_id = null` quando não há evidência.

## Governança de tenant

O GAP de tenant está encerrado para os 133 reparos. A promoção M14/M15 não altera identidade de usuário, `elo_scopes`, memberships ou RLS.

## Proveniência

A materialização da identidade física não fabrica proveniência histórica. `mt_proveniencia_registros` continua sem linhagem linha a linha para esses reparos. O GAP de proveniência permanece separado e aberto.

## Probe

`supabase/health/elo_mt_unit_materialization_readiness.sql` deve agora apresentar:

- `ALREADY_MATERIALIZED`: 123 identificadores;
- `BLOCKED_MODEL_GAP`: 1 identificador (`M16`).

O probe permanece somente leitura.
