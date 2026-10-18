-- ELO System Health Gate
-- Read-only diagnostics. GitHub remains the operational authority; Supabase
-- provides current persistent evidence. A result row is a finding to govern.

-- 1) SECURITY: RLS without policy is a blocking finding only when a client role
-- has EFFECTIVE table privileges. has_table_privilege() includes privileges
-- inherited through role membership or PUBLIC, unlike direct-grant inventory.
WITH policies AS (
  SELECT schemaname, tablename, count(*) AS policy_count
  FROM pg_policies
  GROUP BY 1, 2
), effective_access AS (
  SELECT
    c.oid AS table_oid,
    has_table_privilege('anon', c.oid, 'SELECT')
      OR has_table_privilege('anon', c.oid, 'INSERT')
      OR has_table_privilege('anon', c.oid, 'UPDATE')
      OR has_table_privilege('anon', c.oid, 'DELETE') AS anon_has_dml,
    has_table_privilege('authenticated', c.oid, 'SELECT')
      OR has_table_privilege('authenticated', c.oid, 'INSERT')
      OR has_table_privilege('authenticated', c.oid, 'UPDATE')
      OR has_table_privilege('authenticated', c.oid, 'DELETE') AS authenticated_has_dml
  FROM pg_class c
)
SELECT
  'SECURITY_RLS_NO_POLICY_EXPOSED'::text AS finding,
  n.nspname AS schema_name,
  c.relname AS object_name,
  'BLOCK'::text AS severity,
  format(
    'effective_dml anon=%s authenticated=%s',
    coalesce(a.anon_has_dml, false),
    coalesce(a.authenticated_has_dml, false)
  ) AS evidence
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN policies p ON p.schemaname = n.nspname AND p.tablename = c.relname
LEFT JOIN effective_access a ON a.table_oid = c.oid
WHERE c.relkind = 'r'
  AND c.relrowsecurity
  AND n.nspname IN ('public', 'elo_core', 'elo_private')
  AND coalesce(p.policy_count, 0) = 0
  AND (coalesce(a.anon_has_dml, false) OR coalesce(a.authenticated_has_dml, false))
ORDER BY 2, 3;

-- 2) PERFORMANCE/GOVERNANCE: duplicate indexes are reported only when their
-- material pg_index semantics match. This remains a review finding, never an
-- automatic DROP instruction: provenance must identify the canonical name.
SELECT
  'DUPLICATE_INDEX'::text AS finding,
  ns.nspname AS schema_name,
  tbl.relname AS object_name,
  'REVIEW'::text AS severity,
  string_agg(idx.relname, ', ' ORDER BY idx.relname) AS evidence
FROM pg_index i
JOIN pg_class idx ON idx.oid = i.indexrelid
JOIN pg_class tbl ON tbl.oid = i.indrelid
JOIN pg_namespace ns ON ns.oid = tbl.relnamespace
WHERE ns.nspname IN ('public', 'elo_core', 'elo_private')
  AND NOT i.indisprimary
GROUP BY
  ns.nspname,
  tbl.oid,
  tbl.relname,
  i.indnatts,
  i.indnkeyatts,
  i.indisunique,
  i.indnullsnotdistinct,
  i.indisexclusion,
  i.indimmediate,
  i.indisvalid,
  i.indisready,
  i.indkey,
  i.indclass,
  i.indcollation,
  i.indoption,
  pg_get_expr(i.indexprs, i.indrelid),
  pg_get_expr(i.indpred, i.indrelid)
HAVING count(*) > 1
ORDER BY 2, 3;

-- 3) AUTHORIZATION GOVERNANCE: legacy MT policies that reduce an authenticated
-- predicate to literal TRUE are an explicit high-priority GAP until elo-authz
-- proves the caller's canonical identity, ENTERPRISE scope membership and the
-- resource/action contract. This query does NOT infer a replacement policy and
-- does NOT turn ENTERPRISE/MULTITEINER into live tenant authority by itself.
WITH mt_true_policies AS (
  SELECT
    p.tablename,
    p.policyname,
    p.cmd,
    p.qual,
    p.with_check
  FROM pg_policies p
  WHERE p.schemaname = 'public'
    AND p.tablename LIKE 'mt\_%' ESCAPE '\'
    AND 'authenticated' = ANY (p.roles)
    AND (
      trim(coalesce(p.qual, '')) = 'true'
      OR trim(coalesce(p.with_check, '')) = 'true'
    )
), mt_tables AS (
  SELECT
    c.oid,
    c.relname,
    EXISTS (
      SELECT 1
      FROM pg_attribute a
      WHERE a.attrelid = c.oid
        AND a.attname = 'tenant_id'
        AND NOT a.attisdropped
    ) AS has_tenant_id
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname = 'public'
    AND c.relkind = 'r'
)
SELECT
  'AUTHZ_MT_PERMISSIVE_TRUE'::text AS finding,
  'public'::text AS schema_name,
  p.tablename AS object_name,
  'GAP_HIGH'::text AS severity,
  format(
    'policies=%s tenant_id=%s effective_select=%s effective_write=%s',
    count(*),
    t.has_tenant_id,
    has_table_privilege('authenticated', t.oid, 'SELECT'),
    has_table_privilege('authenticated', t.oid, 'INSERT')
      OR has_table_privilege('authenticated', t.oid, 'UPDATE')
      OR has_table_privilege('authenticated', t.oid, 'DELETE')
  ) AS evidence
FROM mt_true_policies p
JOIN mt_tables t ON t.relname = p.tablename
GROUP BY p.tablename, t.oid, t.has_tenant_id
ORDER BY t.has_tenant_id DESC, p.tablename;
