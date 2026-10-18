-- ELO MT tenant-data readiness probe
-- Read-only. This query reports whether MT tables that expose a tenant_id
-- column actually contain persisted tenant assignments. It does not create a
-- tenant, infer ownership, backfill tenant_id, or authorize any RLS rewrite.
-- Any populated direct-tenant table that is not explicitly verified below keeps
-- the readiness gap open; estimated statistics may prioritize verification but
-- can never clear tenant readiness by themselves.

WITH tenant_tables AS (
  SELECT c.oid, c.relname AS table_name
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname = 'public'
    AND c.relkind = 'r'
    AND c.relname LIKE 'mt\_%' ESCAPE '\'
    AND EXISTS (
      SELECT 1
      FROM pg_attribute a
      WHERE a.attrelid = c.oid
        AND a.attname = 'tenant_id'
        AND a.attnum > 0
        AND NOT a.attisdropped
    )
), tenant_catalog AS (
  SELECT
    count(*) AS tenant_rows,
    count(*) FILTER (WHERE ativo) AS active_tenants
  FROM public.mt_tenants
), table_stats AS (
  SELECT
    t.table_name,
    coalesce(s.n_live_tup, 0)::bigint AS estimated_rows
  FROM tenant_tables t
  LEFT JOIN pg_stat_user_tables s ON s.relid = t.oid
), populated_tables AS (
  SELECT table_name, estimated_rows
  FROM table_stats
  WHERE estimated_rows > 0
), repair_truth AS (
  -- mt_ordens_reparo is explicitly verified with exact counts because it is the
  -- only currently populated direct-tenant MT table in the observed inventory.
  -- If another direct-tenant table becomes populated, it remains unverified and
  -- this probe stays GAP_HIGH until an exact check is added for that table.
  SELECT
    count(*)::bigint AS total_rows,
    count(*) FILTER (WHERE tenant_id IS NOT NULL)::bigint AS rows_with_tenant,
    count(*) FILTER (WHERE tenant_id IS NULL)::bigint AS rows_without_tenant,
    count(DISTINCT tenant_id) FILTER (WHERE tenant_id IS NOT NULL)::bigint AS distinct_tenants
  FROM public.mt_ordens_reparo
), summary AS (
  SELECT
    (SELECT count(*) FROM tenant_tables) AS direct_tenant_tables,
    (SELECT count(*) FROM populated_tables) AS estimated_populated_tables,
    GREATEST(
      (SELECT count(*) FROM populated_tables)
      - CASE WHEN rt.total_rows > 0 THEN 1 ELSE 0 END,
      0
    ) AS unverified_populated_tables,
    tc.tenant_rows,
    tc.active_tenants,
    rt.total_rows AS repair_rows,
    rt.rows_with_tenant AS repair_rows_with_tenant,
    rt.rows_without_tenant AS repair_rows_without_tenant,
    rt.distinct_tenants AS repair_distinct_tenants
  FROM tenant_catalog tc
  CROSS JOIN repair_truth rt
)
SELECT
  'AUTHZ_MT_TENANT_DATA_READINESS'::text AS finding,
  'public'::text AS schema_name,
  'mt_*'::text AS object_name,
  'GAP_HIGH'::text AS severity,
  format(
    'direct_tenant_tables=%s estimated_populated_tables=%s unverified_populated_tables=%s tenant_rows=%s active_tenants=%s repair_rows=%s repair_rows_with_tenant=%s repair_rows_without_tenant=%s repair_distinct_tenants=%s',
    direct_tenant_tables,
    estimated_populated_tables,
    unverified_populated_tables,
    tenant_rows,
    active_tenants,
    repair_rows,
    repair_rows_with_tenant,
    repair_rows_without_tenant,
    repair_distinct_tenants
  ) AS evidence
FROM summary
WHERE tenant_rows = 0
   OR repair_rows_without_tenant > 0
   OR unverified_populated_tables > 0;
