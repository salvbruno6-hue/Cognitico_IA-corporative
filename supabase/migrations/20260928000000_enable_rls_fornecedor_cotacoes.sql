-- ELO governance fix: enable RLS on fornecedor_cotacoes.
--
-- Context:
-- - The table is exposed on the public API surface.
-- - 09-governance/contracts/expected_state/supabase_rls.yaml
--   declares expected_rls: true.
-- - No policy is declared anywhere for this table.
-- - Writes/reads go through the SECURITY DEFINER function
--   public.registrar_cotacao_fornecedor, which is executable
--   only by service_role.
--
-- Therefore: enable RLS with no policies (fail-closed).
-- Only service_role (which bypasses RLS) can access.
-- No permissive policy is created without a declared model.
--
-- This migration is additive and reversible.

alter table public.fornecedor_cotacoes enable row level security;

comment on table public.fornecedor_cotacoes
is 'Supplier quotations. RLS enabled, fail-closed. Access only through public.registrar_cotacao_fornecedor (SECURITY DEFINER, service_role only). See migration 20260928000000.';

-- Additive index hint: no new policies. No grants.
-- If a future use case requires authenticated read, add a
-- policy in a separate governed migration.
