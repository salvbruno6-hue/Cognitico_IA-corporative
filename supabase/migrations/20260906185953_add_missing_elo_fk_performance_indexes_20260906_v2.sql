-- Reconcile live Supabase migration history into version control.
-- Performance-only indexes for foreign-key access paths. No application data changes.

CREATE INDEX IF NOT EXISTS idx_excedente_itens_cod_produt
  ON public.excedente_itens (cod_produt);
CREATE INDEX IF NOT EXISTS idx_excedente_itens_excedente_id
  ON public.excedente_itens (excedente_id);
CREATE INDEX IF NOT EXISTS idx_excedente_mao_obra_excedente_id
  ON public.excedente_mao_obra (excedente_id);
CREATE INDEX IF NOT EXISTS idx_elo_identity_roles_role_id
  ON public.elo_identity_roles (role_id);
CREATE INDEX IF NOT EXISTS idx_elo_identity_scopes_scope_id
  ON public.elo_identity_scopes (scope_id);
