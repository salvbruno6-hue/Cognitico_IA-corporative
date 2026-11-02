-- CANDIDATE ONLY — NOT AN OFFICIAL MIGRATION / NOT AUTHORIZED FOR LIVE DDL.
-- Related: #1143, #1145, ADR-0017.
--
-- Resolves the orphan PCP_ADMIN authorization symbol without creating a
-- capability. Administrative role membership and capability possession become
-- separate predicates again.

CREATE SCHEMA IF NOT EXISTS elo_private;

-- Narrow role predicate for database RLS only.
CREATE OR REPLACE FUNCTION elo_private.has_admin_role()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.elo_identity_registry i
    JOIN public.elo_identity_roles ir ON ir.identity_id = i.identity_id
    JOIN public.elo_roles r
      ON r.role_id = ir.role_id
     AND r.active = true
    WHERE i.auth_user_id = auth.uid()
      AND i.active = true
      AND r.code IN ('ELO_ADMIN', 'CANONICAL_ADMIN')
  );
$$;

REVOKE ALL ON FUNCTION elo_private.has_admin_role() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION elo_private.has_admin_role() TO authenticated;

COMMENT ON FUNCTION elo_private.has_admin_role()
IS 'Internal ELO RLS predicate for active canonical administrative role membership. Does not grant or imply any capability and is not an elo-authz authorization receipt.';

-- Restore strict capability semantics: every normal capability must be material
-- in elo_role_capabilities -> elo_capabilities.
CREATE OR REPLACE FUNCTION elo_private.has_capability(p_code text)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.elo_identity_registry i
    JOIN public.elo_identity_roles ir ON ir.identity_id = i.identity_id
    JOIN public.elo_roles r
      ON r.role_id = ir.role_id
     AND r.active = true
    JOIN public.elo_role_capabilities rc ON rc.role_id = r.role_id
    JOIN public.elo_capabilities c
      ON c.capability_id = rc.capability_id
     AND c.active = true
    WHERE i.auth_user_id = auth.uid()
      AND i.active = true
      AND c.code = p_code
  );
$$;

REVOKE ALL ON FUNCTION elo_private.has_capability(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION elo_private.has_capability(text) TO authenticated;

COMMENT ON FUNCTION elo_private.has_capability(text)
IS 'Canonical ELO RLS capability resolver. Requires explicit active identity -> active role -> role capability -> active capability mapping.';

-- Exact audited snapshot from the live project on 2026-11-02.
-- Each row binds schema/table/policy/command/permissiveness/roles plus one of the
-- two exact legacy predicate shapes observed live. expected_qual and
-- expected_with_check are materialized from that shape before any ALTER POLICY.
DO $$
DECLARE
  r record;
  v_policy_count integer;
  v_expression_count integer;
  v_qual text;
  v_check text;
  v_jwt_or_admin text := '((COALESCE(((( SELECT auth.jwt() AS jwt) -> ''app_metadata''::text) ->> ''role''::text), ''''::text) = ''admin''::text) OR elo_private.has_capability(''PCP_ADMIN''::text))';
  v_admin_only text := '( SELECT elo_private.has_capability(''PCP_ADMIN''::text) AS has_capability)';
BEGIN
  CREATE TEMP TABLE expected_pcp_admin_policies (
    schemaname text NOT NULL,
    tablename text NOT NULL,
    policyname text NOT NULL,
    cmd text NOT NULL,
    permissive text NOT NULL,
    roles_text text NOT NULL,
    expected_qual text,
    expected_with_check text,
    PRIMARY KEY (schemaname, tablename, policyname)
  ) ON COMMIT DROP;

  INSERT INTO expected_pcp_admin_policies (
    schemaname, tablename, policyname, cmd, permissive, roles_text,
    expected_qual, expected_with_check
  )
  SELECT
    'public',
    v.tablename,
    v.policyname,
    v.cmd,
    'PERMISSIVE',
    '{authenticated}',
    CASE
      WHEN v.cmd IN ('DELETE', 'UPDATE') THEN
        CASE v.shape WHEN 'JWT_OR_ADMIN' THEN v_jwt_or_admin ELSE v_admin_only END
      ELSE NULL
    END,
    CASE
      WHEN v.cmd IN ('INSERT', 'UPDATE') THEN
        CASE v.shape WHEN 'JWT_OR_ADMIN' THEN v_jwt_or_admin ELSE v_admin_only END
      ELSE NULL
    END
  FROM (VALUES
    ('dimensoes','p_pcp_dimensoes_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('dimensoes','p_pcp_dimensoes_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('dimensoes','p_pcp_dimensoes_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('estrutura_metalica_20_componentes','p_m01_est_comp_delete','DELETE','ADMIN_ONLY'),
    ('estrutura_metalica_20_componentes','p_m01_est_comp_insert','INSERT','ADMIN_ONLY'),
    ('estrutura_metalica_20_componentes','p_m01_est_comp_update','UPDATE','ADMIN_ONLY'),
    ('fluxo_produtivo_modular','p_pcp_fluxo_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('fluxo_produtivo_modular','p_pcp_fluxo_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('fluxo_produtivo_modular','p_pcp_fluxo_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('fluxo_produtivo_modular_etapas','p_pcp_fluxo_etapas_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('fluxo_produtivo_modular_etapas','p_pcp_fluxo_etapas_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('fluxo_produtivo_modular_etapas','p_pcp_fluxo_etapas_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('kit_itens','p_pcp_kit_itens_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('kit_itens','p_pcp_kit_itens_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('kit_itens','p_pcp_kit_itens_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('kits','p_pcp_kits_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('kits','p_pcp_kits_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('kits','p_pcp_kits_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('lista_mae','p_pcp_lista_mae_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('lista_mae','p_pcp_lista_mae_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('lista_mae','p_pcp_lista_mae_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('modelos','p_pcp_modelos_admin_delete','DELETE','JWT_OR_ADMIN'),
    ('modelos','p_pcp_modelos_admin_insert','INSERT','JWT_OR_ADMIN'),
    ('modelos','p_pcp_modelos_admin_update','UPDATE','JWT_OR_ADMIN'),
    ('mt_lotes_estoque','p_pcp_lotes_delete_admin','DELETE','JWT_OR_ADMIN'),
    ('mt_mao_obra_kit_eletrico_m01','p_m01_mo_eletrico_delete','DELETE','ADMIN_ONLY'),
    ('mt_mao_obra_kit_eletrico_m01','p_m01_mo_eletrico_insert','INSERT','ADMIN_ONLY'),
    ('mt_mao_obra_kit_eletrico_m01','p_m01_mo_eletrico_update','UPDATE','ADMIN_ONLY'),
    ('mt_mao_obra_montagem_estrutura_modular_20','p_m01_mo_montagem_delete','DELETE','ADMIN_ONLY'),
    ('mt_mao_obra_montagem_estrutura_modular_20','p_m01_mo_montagem_insert','INSERT','ADMIN_ONLY'),
    ('mt_mao_obra_montagem_estrutura_modular_20','p_m01_mo_montagem_update','UPDATE','ADMIN_ONLY'),
    ('mt_mao_obra_solda_preparacao_estrutura_modular','p_m01_mo_solda_delete','DELETE','ADMIN_ONLY'),
    ('mt_mao_obra_solda_preparacao_estrutura_modular','p_m01_mo_solda_insert','INSERT','ADMIN_ONLY'),
    ('mt_mao_obra_solda_preparacao_estrutura_modular','p_m01_mo_solda_update','UPDATE','ADMIN_ONLY'),
    ('mt_ordens_reparo','p_pcp_reparo_delete_admin','DELETE','JWT_OR_ADMIN'),
    ('mt_tempo_fabricacao_estrutura_modular','p_m01_tempo_fab_delete','DELETE','ADMIN_ONLY'),
    ('mt_tempo_fabricacao_estrutura_modular','p_m01_tempo_fab_insert','INSERT','ADMIN_ONLY'),
    ('mt_tempo_fabricacao_estrutura_modular','p_m01_tempo_fab_update','UPDATE','ADMIN_ONLY')
  ) AS v(tablename, policyname, cmd, shape);

  SELECT
    count(*)::integer,
    coalesce(sum(
      ((length(coalesce(qual, '') || ' ' || coalesce(with_check, ''))
        - length(replace(coalesce(qual, '') || ' ' || coalesce(with_check, ''), 'PCP_ADMIN', '')))
       / length('PCP_ADMIN'))
    ), 0)::integer
  INTO v_policy_count, v_expression_count
  FROM pg_policies
  WHERE coalesce(qual, '') LIKE '%PCP_ADMIN%'
     OR coalesce(with_check, '') LIKE '%PCP_ADMIN%';

  IF v_policy_count <> 38 OR v_expression_count <> 50 THEN
    RAISE EXCEPTION
      'PCP_ADMIN policy graph changed: expected 38 policies / 50 expressions, observed % / %',
      v_policy_count, v_expression_count;
  END IF;

  -- Exact per-policy comparison. Same-count drift must fail before any rewrite.
  IF EXISTS (
    SELECT 1
    FROM expected_pcp_admin_policies e
    LEFT JOIN pg_policies p
      ON p.schemaname = e.schemaname
     AND p.tablename = e.tablename
     AND p.policyname = e.policyname
    WHERE p.policyname IS NULL
       OR p.cmd IS DISTINCT FROM e.cmd
       OR p.permissive IS DISTINCT FROM e.permissive
       OR p.roles::text IS DISTINCT FROM e.roles_text
       OR p.qual IS DISTINCT FROM e.expected_qual
       OR p.with_check IS DISTINCT FROM e.expected_with_check
  ) THEN
    RAISE EXCEPTION 'PCP_ADMIN audited policy definition drift detected; re-analysis required before rewrite';
  END IF;

  -- No extra legacy consumer is allowed outside the audited identity set.
  IF EXISTS (
    SELECT 1
    FROM pg_policies p
    LEFT JOIN expected_pcp_admin_policies e
      ON e.schemaname = p.schemaname
     AND e.tablename = p.tablename
     AND e.policyname = p.policyname
    WHERE (coalesce(p.qual, '') LIKE '%PCP_ADMIN%'
        OR coalesce(p.with_check, '') LIKE '%PCP_ADMIN%')
      AND e.policyname IS NULL
  ) THEN
    RAISE EXCEPTION 'Unexpected PCP_ADMIN policy outside audited snapshot; re-analysis required';
  END IF;

  FOR r IN
    SELECT
      p.schemaname,
      p.tablename,
      p.policyname,
      p.qual,
      p.with_check
    FROM pg_policies p
    JOIN expected_pcp_admin_policies e
      ON e.schemaname = p.schemaname
     AND e.tablename = p.tablename
     AND e.policyname = p.policyname
    ORDER BY p.schemaname, p.tablename, p.policyname
  LOOP
    v_qual := CASE
      WHEN r.qual IS NULL THEN NULL
      ELSE replace(
        r.qual,
        'elo_private.has_capability(''PCP_ADMIN''::text)',
        'elo_private.has_admin_role()'
      )
    END;
    v_check := CASE
      WHEN r.with_check IS NULL THEN NULL
      ELSE replace(
        r.with_check,
        'elo_private.has_capability(''PCP_ADMIN''::text)',
        'elo_private.has_admin_role()'
      )
    END;

    IF r.qual IS NOT NULL AND v_qual = r.qual THEN
      RAISE EXCEPTION 'Unexpected PCP_ADMIN USING expression in %.%.%', r.schemaname, r.tablename, r.policyname;
    END IF;
    IF r.with_check IS NOT NULL AND v_check = r.with_check THEN
      RAISE EXCEPTION 'Unexpected PCP_ADMIN WITH CHECK expression in %.%.%', r.schemaname, r.tablename, r.policyname;
    END IF;

    IF v_qual IS NOT NULL AND v_check IS NOT NULL THEN
      EXECUTE format(
        'ALTER POLICY %I ON %I.%I USING (%s) WITH CHECK (%s)',
        r.policyname, r.schemaname, r.tablename, v_qual, v_check
      );
    ELSIF v_qual IS NOT NULL THEN
      EXECUTE format(
        'ALTER POLICY %I ON %I.%I USING (%s)',
        r.policyname, r.schemaname, r.tablename, v_qual
      );
    ELSIF v_check IS NOT NULL THEN
      EXECUTE format(
        'ALTER POLICY %I ON %I.%I WITH CHECK (%s)',
        r.policyname, r.schemaname, r.tablename, v_check
      );
    ELSE
      RAISE EXCEPTION 'PCP_ADMIN policy without USING/WITH CHECK: %.%.%', r.schemaname, r.tablename, r.policyname;
    END IF;
  END LOOP;

  IF EXISTS (
    SELECT 1
    FROM pg_policies
    WHERE coalesce(qual, '') LIKE '%PCP_ADMIN%'
       OR coalesce(with_check, '') LIKE '%PCP_ADMIN%'
  ) THEN
    RAISE EXCEPTION 'PCP_ADMIN policy references remain after rewrite';
  END IF;
END;
$$;

-- Reconcile the Lista-Mãe trigger with ADR-0017 while removing the live-only
-- SECURITY DEFINER/current_user authorization bug. RLS remains the first DML
-- boundary and the audit row remains mandatory for accepted changes.
CREATE OR REPLACE FUNCTION public.lista_mae_guard()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'pg_catalog', 'public'
AS $function$
DECLARE
  v_aprovado text;
  v_tem_admin boolean;
  v_jwt_role text;
BEGIN
  v_aprovado := current_setting('app.lista_mae_aprovada', true);

  BEGIN
    v_tem_admin := elo_private.has_admin_role();
  EXCEPTION WHEN OTHERS THEN
    v_tem_admin := false;
  END;

  BEGIN
    v_jwt_role := auth.jwt() -> 'app_metadata' ->> 'role';
  EXCEPTION WHEN OTHERS THEN
    v_jwt_role := null;
  END;

  IF coalesce(v_aprovado, '') <> 'SIM'
     AND coalesce(v_tem_admin, false) = false
     AND coalesce(v_jwt_role, '') <> 'admin' THEN
    RAISE EXCEPTION
      'ALTERAÇÃO BLOQUEADA: a Lista-Mãe exige aprovação explícita ou identidade administrativa autorizada.';
  END IF;

  INSERT INTO public.lista_mae_alteracoes (
    operacao,
    cod_produt,
    dados_antes,
    dados_depois,
    aprovado,
    aprovado_em
  ) VALUES (
    tg_op,
    coalesce(new.cod_produt, old.cod_produt),
    CASE WHEN tg_op IN ('UPDATE', 'DELETE') THEN to_jsonb(old) ELSE null END,
    CASE WHEN tg_op IN ('INSERT', 'UPDATE') THEN to_jsonb(new) ELSE null END,
    true,
    now()
  );

  RETURN coalesce(new, old);
END;
$function$;

REVOKE ALL ON FUNCTION public.lista_mae_guard() FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.lista_mae_guard() TO service_role;

COMMENT ON FUNCTION public.lista_mae_guard()
IS 'Lista-Mãe audit guard. Authorization sources: explicit gateway approval, canonical administrative role, or authenticated JWT admin. Does not use current_user as caller identity.';

-- Final fail-closed assertions: the orphan symbol and SECURITY DEFINER caller
-- bypass must be gone from the governed database authorization surfaces.
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_policies
    WHERE coalesce(qual, '') LIKE '%PCP_ADMIN%'
       OR coalesce(with_check, '') LIKE '%PCP_ADMIN%'
  ) THEN
    RAISE EXCEPTION 'PCP_ADMIN still referenced by RLS';
  END IF;

  IF EXISTS (
    SELECT 1
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE p.prokind = 'f'
      AND n.nspname IN ('public', 'elo_private')
      AND pg_get_functiondef(p.oid) LIKE '%PCP_ADMIN%'
  ) THEN
    RAISE EXCEPTION 'PCP_ADMIN still referenced by authorization function body';
  END IF;

  IF EXISTS (
    SELECT 1
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE p.prokind = 'f'
      AND n.nspname = 'public'
      AND p.proname = 'lista_mae_guard'
      AND pg_get_functiondef(p.oid) LIKE '%current_user%'
  ) THEN
    RAISE EXCEPTION 'lista_mae_guard still uses current_user as authorization evidence';
  END IF;
END;
$$;
