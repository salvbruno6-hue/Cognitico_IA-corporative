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

-- 4) PERFORMANCE: direct auth.jwt() calls inside RLS predicates are evaluated
-- in row context and are reported by the Supabase auth_rls_initplan advisor.
-- Scalar SELECT wrappers are deliberately stripped before looking for any
-- residual auth.jwt() call. PostgreSQL may deparse a scalar subquery with an
-- optional column alias (for example, SELECT auth.jwt() AS jwt), so the removal
-- pattern accepts that representation as well.
-- A finding is a performance REVIEW, not permission to alter authorization
-- semantics. Any remediation must preserve the exact predicate and only change
-- evaluation shape.
WITH normalized_policy_expr AS (
  SELECT
    p.*,
    regexp_replace(
      coalesce(p.qual, ''),
      '\(\s*SELECT\s+auth\.jwt\(\)(\s+AS\s+[A-Za-z_][A-Za-z0-9_]*)?\s*\)',
      '',
      'gi'
    ) AS qual_without_scalar_jwt,
    regexp_replace(
      coalesce(p.with_check, ''),
      '\(\s*SELECT\s+auth\.jwt\(\)(\s+AS\s+[A-Za-z_][A-Za-z0-9_]*)?\s*\)',
      '',
      'gi'
    ) AS check_without_scalar_jwt
  FROM pg_policies p
  WHERE p.schemaname IN ('public', 'elo_core', 'elo_private')
)
SELECT
  'PERF_RLS_AUTH_JWT_PER_ROW'::text AS finding,
  p.schemaname AS schema_name,
  p.tablename AS object_name,
  'REVIEW'::text AS severity,
  format('policy=%s command=%s roles=%s', p.policyname, p.cmd, p.roles::text) AS evidence
FROM normalized_policy_expr p
WHERE p.qual_without_scalar_jwt ~* 'auth\.jwt\(\)'
   OR p.check_without_scalar_jwt ~* 'auth\.jwt\(\)'
ORDER BY p.schemaname, p.tablename, p.policyname;

-- 5) PERFORMANCE/GOVERNANCE: multiple permissive policies for the same role and
-- action have different remediation semantics. ALL_PLUS_SPECIFIC means a FOR ALL
-- policy overlaps a command-specific policy; EXACT_DUPLICATE means specific
-- policies have identical row predicates. MULTIPLE_DISTINCT means the policies
-- are not semantically identical and must not be collapsed by name alone.
WITH expanded AS (
  SELECT
    p.schemaname,
    p.tablename,
    p.policyname,
    p.cmd,
    p.qual,
    p.with_check,
    unnest(
      CASE
        WHEN p.cmd = 'ALL' THEN ARRAY['SELECT','INSERT','UPDATE','DELETE']::text[]
        ELSE ARRAY[p.cmd]::text[]
      END
    ) AS action
  FROM pg_policies p
  WHERE p.schemaname IN ('public', 'elo_core', 'elo_private')
    AND 'authenticated' = ANY (p.roles)
), grouped AS (
  SELECT
    schemaname,
    tablename,
    action,
    count(*) AS policy_count,
    array_agg(policyname ORDER BY policyname) AS policies,
    count(*) FILTER (WHERE cmd = 'ALL') AS all_policy_count,
    count(DISTINCT coalesce(qual, '<null>') || '|' || coalesce(with_check, '<null>')) AS predicate_variants
  FROM expanded
  GROUP BY schemaname, tablename, action
  HAVING count(*) > 1
)
SELECT
  'PERF_RLS_PERMISSIVE_OVERLAP'::text AS finding,
  schemaname AS schema_name,
  tablename AS object_name,
  'REVIEW'::text AS severity,
  format(
    'action=%s type=%s policies=%s',
    action,
    CASE
      WHEN all_policy_count > 0 THEN 'ALL_PLUS_SPECIFIC'
      WHEN predicate_variants = 1 THEN 'EXACT_DUPLICATE'
      ELSE 'MULTIPLE_DISTINCT'
    END,
    array_to_string(policies, ',')
  ) AS evidence
FROM grouped
ORDER BY schemaname, tablename, action;

-- 6) PERFORMANCE/GOVERNANCE: an unindexed foreign key is not an instruction to
-- create an index blindly. Rank unresolved FK paths by live table evidence so
-- remediation can be bounded to relations that actually have data/activity.
-- pg_stat_user_tables is cumulative and can reset; the output is prioritization
-- evidence, not a permanent importance score or automatic CREATE INDEX command.
WITH foreign_keys AS (
  SELECT
    con.oid AS constraint_oid,
    n.nspname AS schema_name,
    rel.relname AS table_name,
    con.conname AS fk_name,
    con.conrelid,
    con.conkey,
    array_agg(att.attname ORDER BY u.ord) AS fk_columns
  FROM pg_constraint con
  JOIN pg_class rel ON rel.oid = con.conrelid
  JOIN pg_namespace n ON n.oid = rel.relnamespace
  JOIN unnest(con.conkey) WITH ORDINALITY AS u(attnum, ord) ON true
  JOIN pg_attribute att
    ON att.attrelid = con.conrelid
   AND att.attnum = u.attnum
  WHERE con.contype = 'f'
    AND n.nspname IN ('public', 'elo_core', 'elo_private')
  GROUP BY
    con.oid,
    n.nspname,
    rel.relname,
    con.conname,
    con.conrelid,
    con.conkey
), unindexed_foreign_keys AS (
  SELECT fk.*
  FROM foreign_keys fk
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_index i
    WHERE i.indrelid = fk.conrelid
      AND i.indisvalid
      AND i.indisready
      AND (i.indkey::smallint[])[0:cardinality(fk.conkey)-1] = fk.conkey
  )
)
SELECT
  'PERF_UNINDEXED_FK_PRIORITY'::text AS finding,
  u.schema_name,
  u.table_name AS object_name,
  'REVIEW'::text AS severity,
  format(
    'fk=%s columns=%s rows=%s seq_scans=%s index_scans=%s writes=%s',
    u.fk_name,
    array_to_string(u.fk_columns, ','),
    coalesce(s.n_live_tup, 0),
    coalesce(s.seq_scan, 0),
    coalesce(s.idx_scan, 0),
    coalesce(s.n_tup_ins, 0) + coalesce(s.n_tup_upd, 0) + coalesce(s.n_tup_del, 0)
  ) AS evidence
FROM unindexed_foreign_keys u
LEFT JOIN pg_stat_user_tables s ON s.relid = u.conrelid
ORDER BY
  coalesce(s.n_live_tup, 0) DESC,
  coalesce(s.seq_scan, 0) DESC,
  (coalesce(s.n_tup_ins, 0) + coalesce(s.n_tup_upd, 0) + coalesce(s.n_tup_del, 0)) DESC,
  u.schema_name,
  u.table_name,
  u.fk_name;
