-- ELO System Health Gate
-- Read-only diagnostics. GitHub remains the operational authority; Supabase
-- provides current persistent evidence. A result row is a finding to govern.

-- 1) SECURITY: RLS without policy is a blocking finding only when client roles
-- also have table privileges. RLS-without-policy + zero client grants is
-- deliberate fail-closed and is not treated as exposure.
WITH policies AS (
  SELECT schemaname, tablename, count(*) AS policy_count
  FROM pg_policies
  GROUP BY 1, 2
), grants AS (
  SELECT table_schema, table_name,
         count(*) FILTER (WHERE grantee = 'anon') AS anon_privileges,
         count(*) FILTER (WHERE grantee = 'authenticated') AS authenticated_privileges
  FROM information_schema.role_table_grants
  GROUP BY 1, 2
)
SELECT
  'SECURITY_RLS_NO_POLICY_EXPOSED'::text AS finding,
  n.nspname AS schema_name,
  c.relname AS object_name,
  'BLOCK'::text AS severity,
  format('anon=%s authenticated=%s', coalesce(g.anon_privileges, 0), coalesce(g.authenticated_privileges, 0)) AS evidence
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN policies p ON p.schemaname = n.nspname AND p.tablename = c.relname
LEFT JOIN grants g ON g.table_schema = n.nspname AND g.table_name = c.relname
WHERE c.relkind = 'r'
  AND c.relrowsecurity
  AND n.nspname IN ('public', 'elo_core', 'elo_private')
  AND coalesce(p.policy_count, 0) = 0
  AND (coalesce(g.anon_privileges, 0) > 0 OR coalesce(g.authenticated_privileges, 0) > 0)
ORDER BY 2, 3;

-- 2) PERFORMANCE/GOVERNANCE: exact duplicate ordinary indexes. This is a
-- review finding, not an automatic DROP instruction: provenance must identify
-- which index name is canonical before mutation.
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
GROUP BY ns.nspname, tbl.oid, tbl.relname,
         i.indisunique, i.indkey, i.indclass, i.indcollation, i.indoption,
         pg_get_expr(i.indexprs, i.indrelid), pg_get_expr(i.indpred, i.indrelid)
HAVING count(*) > 1
ORDER BY 2, 3;
