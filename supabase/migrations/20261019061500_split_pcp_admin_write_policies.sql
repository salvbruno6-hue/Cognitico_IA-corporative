-- Split seven PCP FOR ALL admin-write policies into command-specific write
-- policies. This removes SELECT overlap with the existing authenticated SELECT
-- policies while preserving the exact write predicate and roles.
--
-- Scope is intentionally limited to non-MT PCP catalog/flow tables whose live
-- policy shape is proven as:
--   SELECT TO authenticated USING (true)
--   ALL    TO authenticated USING/WITH CHECK (admin OR PCP_ADMIN)
--
-- No grants, revokes, tenant semantics, capability assignments or MT policies
-- are changed by this migration.

-- Shared authorization predicate (repeated explicitly so each PostgreSQL policy
-- remains independently inspectable):
-- COALESCE((((SELECT auth.jwt()) -> 'app_metadata') ->> 'role'), '') = 'admin'
-- OR elo_private.has_capability('PCP_ADMIN')

DROP POLICY p_pcp_lista_mae_admin_write ON public.lista_mae;
CREATE POLICY p_pcp_lista_mae_admin_insert ON public.lista_mae
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_lista_mae_admin_update ON public.lista_mae
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_lista_mae_admin_delete ON public.lista_mae
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

DROP POLICY p_pcp_modelos_admin_write ON public.modelos;
CREATE POLICY p_pcp_modelos_admin_insert ON public.modelos
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_modelos_admin_update ON public.modelos
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_modelos_admin_delete ON public.modelos
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

DROP POLICY p_pcp_dimensoes_admin_write ON public.dimensoes;
CREATE POLICY p_pcp_dimensoes_admin_insert ON public.dimensoes
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_dimensoes_admin_update ON public.dimensoes
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_dimensoes_admin_delete ON public.dimensoes
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

DROP POLICY p_pcp_kits_admin_write ON public.kits;
CREATE POLICY p_pcp_kits_admin_insert ON public.kits
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_kits_admin_update ON public.kits
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_kits_admin_delete ON public.kits
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

DROP POLICY p_pcp_kit_itens_admin_write ON public.kit_itens;
CREATE POLICY p_pcp_kit_itens_admin_insert ON public.kit_itens
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_kit_itens_admin_update ON public.kit_itens
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_kit_itens_admin_delete ON public.kit_itens
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

DROP POLICY p_pcp_fluxo_admin_write ON public.fluxo_produtivo_modular;
CREATE POLICY p_pcp_fluxo_admin_insert ON public.fluxo_produtivo_modular
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_fluxo_admin_update ON public.fluxo_produtivo_modular
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_fluxo_admin_delete ON public.fluxo_produtivo_modular
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);

DROP POLICY p_pcp_fluxo_etapas_admin_write ON public.fluxo_produtivo_modular_etapas;
CREATE POLICY p_pcp_fluxo_etapas_admin_insert ON public.fluxo_produtivo_modular_etapas
FOR INSERT TO authenticated
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_fluxo_etapas_admin_update ON public.fluxo_produtivo_modular_etapas
FOR UPDATE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
)
WITH CHECK (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
CREATE POLICY p_pcp_fluxo_etapas_admin_delete ON public.fluxo_produtivo_modular_etapas
FOR DELETE TO authenticated
USING (
  COALESCE((((SELECT auth.jwt()) -> 'app_metadata'::text) ->> 'role'::text), ''::text) = 'admin'::text
  OR elo_private.has_capability('PCP_ADMIN'::text)
);
