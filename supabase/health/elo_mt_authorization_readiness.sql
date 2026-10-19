-- ELO MT authorization readiness probe
-- Read-only. This query does not assign scopes/capabilities, infer tenant
-- membership, or mutate authorization. It reports whether the currently live
-- identity/scope/capability + tenant-data state can support a governed MT
-- migration away from legacy literal-TRUE authenticated policies.

WITH eligible_google_identities AS (
  SELECT i.identity_id
  FROM public.elo_identity_registry i
  JOIN auth.users u ON u.id = i.auth_user_id
  WHERE i.active
    AND i.provider = 'google'
    AND i.auth_user_id IS NOT NULL
    AND i.authorized_email IS NOT NULL
    AND lower(trim(i.authorized_email)) = lower(trim(u.email))
),
enterprise_links AS (
  SELECT DISTINCT x.identity_id
  FROM public.elo_identity_scopes x
  JOIN public.elo_scopes s ON s.scope_id = x.scope_id
  JOIN eligible_google_identities i ON i.identity_id = x.identity_id
  WHERE s.active
    AND s.scope_type = 'ENTERPRISE'
    AND s.scope_key = 'MULTITEINER'
),
domain_links AS (
  SELECT DISTINCT x.identity_id
  FROM public.elo_identity_scopes x
  JOIN public.elo_scopes s ON s.scope_id = x.scope_id
  JOIN eligible_google_identities i ON i.identity_id = x.identity_id
  WHERE s.active
    AND s.scope_type = 'DOMAIN'
),
pcp_capabilities AS (
  SELECT DISTINCT ir.identity_id
  FROM public.elo_identity_roles ir
  JOIN public.elo_roles r
    ON r.role_id = ir.role_id
   AND r.active
  JOIN public.elo_role_capabilities rc ON rc.role_id = r.role_id
  JOIN public.elo_capabilities c
    ON c.capability_id = rc.capability_id
   AND c.active
  JOIN eligible_google_identities i ON i.identity_id = ir.identity_id
  WHERE c.code IN ('PCP_READ', 'PCP_UPDATE')
),
fully_ready_identities AS (
  SELECT i.identity_id
  FROM eligible_google_identities i
  JOIN enterprise_links e ON e.identity_id = i.identity_id
  JOIN domain_links d ON d.identity_id = i.identity_id
  JOIN pcp_capabilities p ON p.identity_id = i.identity_id
),
mt_gap AS (
  SELECT
    count(*) AS policy_objects,
    count(DISTINCT p.tablename) AS tables
  FROM pg_policies p
  WHERE p.schemaname = 'public'
    AND p.tablename LIKE 'mt\_%' ESCAPE '\'
    AND 'authenticated' = ANY (p.roles)
    AND (
      trim(coalesce(p.qual, '')) = 'true'
      OR trim(coalesce(p.with_check, '')) = 'true'
    )
),
tenant_data AS (
  SELECT
    (SELECT count(*) FROM public.mt_tenants) AS tenant_rows,
    (SELECT count(*) FROM public.mt_ordens_reparo) AS repair_rows,
    (SELECT count(*) FROM public.mt_ordens_reparo WHERE tenant_id IS NOT NULL) AS repair_rows_with_tenant
),
readiness AS (
  SELECT
    (SELECT count(*) FROM eligible_google_identities) AS eligible_google_identities,
    (SELECT count(*) FROM enterprise_links) AS enterprise_multiteiner_links,
    (SELECT count(*) FROM domain_links) AS identities_with_domain_scope,
    (SELECT count(*) FROM pcp_capabilities) AS identities_with_pcp_capability,
    (SELECT count(*) FROM fully_ready_identities) AS fully_ready_identities,
    tenant_data.tenant_rows,
    tenant_data.repair_rows,
    tenant_data.repair_rows_with_tenant,
    mt_gap.policy_objects,
    mt_gap.tables
  FROM mt_gap
  CROSS JOIN tenant_data
)
SELECT
  'AUTHZ_MT_OPERATOR_READINESS'::text AS finding,
  'public'::text AS schema_name,
  'mt_*'::text AS object_name,
  CASE
    WHEN policy_objects > 0 AND (
      fully_ready_identities = 0
      OR tenant_rows = 0
      OR (repair_rows > 0 AND repair_rows_with_tenant < repair_rows)
    ) THEN 'GAP_HIGH'::text
    ELSE 'PASS'::text
  END AS severity,
  eligible_google_identities,
  enterprise_multiteiner_links,
  identities_with_domain_scope,
  identities_with_pcp_capability,
  fully_ready_identities,
  tenant_rows,
  repair_rows,
  repair_rows_with_tenant,
  policy_objects AS legacy_policy_objects,
  tables AS legacy_tables,
  format(
    'legacy_policies=%s tables=%s eligible_google_identities=%s enterprise_multiteiner_links=%s identities_with_domain_scope=%s identities_with_pcp_capability=%s fully_ready_identities=%s tenant_rows=%s repair_rows=%s repair_rows_with_tenant=%s',
    policy_objects,
    tables,
    eligible_google_identities,
    enterprise_multiteiner_links,
    identities_with_domain_scope,
    identities_with_pcp_capability,
    fully_ready_identities,
    tenant_rows,
    repair_rows,
    repair_rows_with_tenant
  ) AS evidence
FROM readiness;
