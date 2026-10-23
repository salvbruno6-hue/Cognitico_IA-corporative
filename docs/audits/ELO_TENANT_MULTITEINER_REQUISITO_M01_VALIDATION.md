# ELO — Tenant MULTITEINER + requisito físico M01 — validação

Data: 2026-10-23

## Escopo

Criar a entidade operacional `MULTITEINER` em `public.mt_tenants` e associar somente o requisito físico confirmado de 300 unidades M01 até 2027-01-31.

Fora do escopo:
- backfill de `mt_ordens_reparo.tenant_id`;
- associação de identidades a `ENTERPRISE/MULTITEINER`;
- alteração de RLS/policies;
- inferência de tenant por prefixo, login ou contexto.

## Estado anterior

- `public.mt_tenants`: 0 linhas;
- requisito M01/300 com `tenant_id` nulo;
- origem: `CONFIRMACAO_USUARIO_CHAT_2026-10-21`;
- `mt_ordens_reparo`: 133 linhas, todas sem tenant;
- memberships `ENTERPRISE/MULTITEINER`: 0.

## Implementação

Migration reconciliada com a versão registrada em produção:

`supabase/migrations/20261023105854_tenant_multiteiner_requisito_m01.sql`.

A migration:
1. cria `MULTITEINER / Multiteiner / ativo=true` de forma idempotente;
2. não hardcodeia UUID;
3. valida conflito de identidade;
4. exige exatamente um requisito M01/300 com a proveniência esperada;
5. associa somente esse requisito ao tenant;
6. não modifica reparos;
7. não modifica escopos de identidade;
8. não altera autorização.

## Validação ao vivo

- tenant `MULTITEINER`: 1 registro ativo;
- requisito M01/300: associado a `MULTITEINER`;
- proveniência do requisito preservada;
- reparos: 133 total, 133 sem tenant, 0 com tenant;
- memberships `ENTERPRISE/MULTITEINER`: 0;
- migration live: `20261023105854 / tenant_multiteiner_requisito_m01`.

O Security Advisor mantém apenas findings preexistentes do projeto; não foi observada nova superfície de autorização decorrente desta mudança.

## Gate

Estado: `VALIDADO / RECONCILIADO`.

Os reparos e a autorização de identidades permanecem fail-closed e exigem ciclos próprios de proveniência/governança.
