---
artifact_id: ADR-0017-lista-mae-editable-by-admin
title: Lista-Mãe editável pelo admin da Multiteiner
status: accepted
date: 2026-09-27
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - Multiteiner tenant governance
---

# ADR-0017 — Lista-Mãe editável pelo admin

## Contexto

A auditoria 37.0/38.0 revelou que:

- `lista_mae` é uma tabela corporativa da Multiteiner ligada ao PCP
- O canon `elo_access_tiers` (20260919220406) declara policies
  `elo_*` que nunca foram aplicadas em produção
- Produção tem `p_pcp_*` ativos com modelo permissivo
- O trigger `lista_mae_guard` exige `app.lista_mae_aprovada = 'SIM'`
  para qualquer INSERT/UPDATE/DELETE, mas o gateway não seta esse GUC
- Resultado: **admin autorizado não consegue editar** a Lista-Mãe
  pelo portal

## Decisão

1. **Canon reconhece** que `lista_mae` é tabela Multiteiner/PCP.
   As policies corretas são `p_pcp_*` (já em produção).
   As policies `elo_*` do canon antigo são retiradas como autoridade
   sobre esta tabela.

2. **Trigger `lista_mae_guard` passa a aceitar três fundamentos**:
   - `app.lista_mae_aprovada = 'SIM'` (via gateway autorizado)
   - `elo_private.has_capability('PCP_ADMIN')`
   - `auth.jwt() -> 'app_metadata' ->> 'role' = 'admin'`

   A auditoria continua obrigatória — todo INSERT/UPDATE/DELETE
   registra em `lista_mae_alteracoes`.

3. **Gateway permanece com `userClient + JWT`** para manter
   auditoria humana e RLS. O trigger resolve a autorização.

4. **Capabilities não mudam**:
   - `COLABORADOR` mantém `LISTA_MAE_INSERT` (INSERT)
   - `admin` via `app_metadata` (INSERT/UPDATE/DELETE)
   - `PCP_ADMIN` fica como dívida técnica registrada

## Consequências

### Positivas
- Admin volta a poder editar a Lista-Mãe
- Auditoria preservada
- RLS mantida
- Canon reconhece PCP como dono

### Negativas
- Trigger fica mais complexo (3 condições)
- `PCP_ADMIN` continua órfã

### Neutras
- YAML `supabase_rls.yaml` atualizado para refletir `p_pcp_*`

## Conformidade

- Regra de duplicidade: `EXTEND` (corrige canon existente,
  não cria nova autoridade)
- Camadas: Governança (ADR) + Infraestrutura (migration)
- Princípio fundador: preservado (admin humano decide)

## Status

Aceito. Migration vinculada à PR 38; aplicação em produção fica condicionada ao merge e ao gate de CI.
