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

  INSERT INTO public.elo_authorization_audit(
    identity_id, action, resource, decision, reason, request_id
  )
  SELECT
    v_identity,
    'AUTHORIZE_MT_PCP_READ',
    'ENTERPRISE/MULTITEINER|DOMAIN/PCP-LISTA-MAE',
    'ALLOW',
    'Explicit chat authorization; least privilege via existing ELO_ADMIN + PCP_READ',
    'chat://2026-10-28/authorize-multiteiner-pcp-read'
  WHERE NOT EXISTS (
    SELECT 1
    FROM public.elo_authorization_audit a
    WHERE a.identity_id = v_identity
      AND a.action = 'AUTHORIZE_MT_PCP_READ'
      AND a.resource = 'ENTERPRISE/MULTITEINER|DOMAIN/PCP-LISTA-MAE'
      AND a.decision = 'ALLOW'
      AND a.request_id = 'chat://2026-10-28/authorize-multiteiner-pcp-read'
  );
END $$;
