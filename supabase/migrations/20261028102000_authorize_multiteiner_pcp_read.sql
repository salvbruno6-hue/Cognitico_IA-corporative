-- Governed operator authorization approved in chat on 2026-10-28.
-- Reuses canonical identity/scope/role/capability primitives only.
-- Least privilege: ENTERPRISE/MULTITEINER + DOMAIN/PCP-LISTA-MAE + PCP_READ.
-- No PCP_UPDATE, LISTA_MAE_INSERT, role creation, scope creation, or RLS rewrite.

DO $$
DECLARE
  v_identity uuid;
  v_identity_count integer;
  v_enterprise_scope uuid;
  v_pcp_scope uuid;
  v_role uuid;
  v_role_identity_count integer;
  v_pcp_read uuid;
  v_correlation uuid := gen_random_uuid();
BEGIN
  SELECT count(*) INTO v_identity_count
  FROM public.elo_identity_registry i
  JOIN auth.users u ON u.id = i.auth_user_id
  WHERE i.active
    AND i.provider = 'google'
    AND i.authorized_email IS NOT NULL
    AND lower(trim(i.authorized_email)) = lower(trim(u.email));

  IF v_identity_count <> 1 THEN
    RAISE EXCEPTION 'Expected exactly 1 eligible verified Google identity, found %', v_identity_count;
  END IF;

  SELECT i.identity_id INTO v_identity
  FROM public.elo_identity_registry i
  JOIN auth.users u ON u.id = i.auth_user_id
  WHERE i.active
    AND i.provider = 'google'
    AND i.authorized_email IS NOT NULL
    AND lower(trim(i.authorized_email)) = lower(trim(u.email))
  LIMIT 1;

  SELECT scope_id INTO v_enterprise_scope
  FROM public.elo_scopes
  WHERE active AND scope_type = 'ENTERPRISE' AND scope_key = 'MULTITEINER';
  IF v_enterprise_scope IS NULL THEN
    RAISE EXCEPTION 'Active ENTERPRISE/MULTITEINER scope not found';
  END IF;

  SELECT scope_id INTO v_pcp_scope
  FROM public.elo_scopes
  WHERE active AND scope_type = 'DOMAIN' AND scope_key = 'PCP-LISTA-MAE';
  IF v_pcp_scope IS NULL THEN
    RAISE EXCEPTION 'Active DOMAIN/PCP-LISTA-MAE scope not found';
  END IF;

  SELECT role_id INTO v_role
  FROM public.elo_roles
  WHERE active AND code = 'ELO_ADMIN';
  IF v_role IS NULL THEN
    RAISE EXCEPTION 'Active ELO_ADMIN role not found';
  END IF;

  SELECT count(*) INTO v_role_identity_count
  FROM public.elo_identity_roles
  WHERE role_id = v_role;

  IF v_role_identity_count <> 1 OR NOT EXISTS (
    SELECT 1
    FROM public.elo_identity_roles
    WHERE role_id = v_role AND identity_id = v_identity
  ) THEN
    RAISE EXCEPTION 'ELO_ADMIN is not exclusively bound to the verified operator identity';
  END IF;

  SELECT capability_id INTO v_pcp_read
  FROM public.elo_capabilities
  WHERE active AND code = 'PCP_READ';
  IF v_pcp_read IS NULL THEN
    RAISE EXCEPTION 'Active PCP_READ capability not found';
  END IF;

  INSERT INTO public.elo_identity_scopes(identity_id, scope_id)
  VALUES (v_identity, v_enterprise_scope), (v_identity, v_pcp_scope)
  ON CONFLICT DO NOTHING;

  INSERT INTO public.elo_role_capabilities(role_id, capability_id)
  VALUES (v_role, v_pcp_read)
  ON CONFLICT DO NOTHING;

  INSERT INTO public.elo_audit_log(
    correlation_id, actor_type, operation, entity_type, entity_id,
    request_summary, status, metadata
  )
  SELECT
    v_correlation,
    'HUMAN_AUTHORIZATION',
    'AUTHORIZE_MT_PCP_READ',
    'elo_identity_registry',
    v_identity,
    'Explicit authorization for ENTERPRISE/MULTITEINER + DOMAIN/PCP-LISTA-MAE + PCP_READ',
    'SUCCESS',
    jsonb_build_object(
      'enterprise_scope', 'MULTITEINER',
      'domain_scope', 'PCP-LISTA-MAE',
      'capability', 'PCP_READ',
      'role', 'ELO_ADMIN',
      'authorized_in_chat', true
    )
  WHERE NOT EXISTS (
    SELECT 1
    FROM public.elo_audit_log a
    WHERE a.operation = 'AUTHORIZE_MT_PCP_READ'
      AND a.entity_type = 'elo_identity_registry'
      AND a.entity_id = v_identity
      AND a.status = 'SUCCESS'
      AND a.metadata ->> 'enterprise_scope' = 'MULTITEINER'
      AND a.metadata ->> 'domain_scope' = 'PCP-LISTA-MAE'
      AND a.metadata ->> 'capability' = 'PCP_READ'
  );
END $$;
