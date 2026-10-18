-- ELO RLS initPlan optimization.
--
-- Semantics-preserving performance change only:
-- - keeps the same policy names, commands, roles and PCP_ADMIN fallback;
-- - changes only direct auth.jwt() evaluation to a scalar SELECT so PostgreSQL
--   can initialize the row-independent JWT value once per statement;
-- - does not alter tenant, identity, capability, grants or table access.

ALTER POLICY p_pcp_lista_mae_admin_write ON public.lista_mae
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_modelos_admin_write ON public.modelos
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_dimensoes_admin_write ON public.dimensoes
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_kits_admin_write ON public.kits
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_kit_itens_admin_write ON public.kit_itens
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_fluxo_admin_write ON public.fluxo_produtivo_modular
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_fluxo_etapas_admin_write ON public.fluxo_produtivo_modular_etapas
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_reparo_delete_admin ON public.mt_ordens_reparo
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

ALTER POLICY p_pcp_lotes_delete_admin ON public.mt_lotes_estoque
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
