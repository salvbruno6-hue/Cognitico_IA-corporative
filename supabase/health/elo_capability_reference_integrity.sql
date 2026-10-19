-- ELO capability-reference integrity probe
-- Read-only. Detects capability codes referenced by RLS policies through
-- elo_private.has_capability(...) and confronts them with the canonical
-- elo_capabilities catalog. A missing/inactive capability is a REVIEW finding:
-- it is evidence of contract drift, never permission to create/assign it.

WITH policy_text AS (
  SELECT
    p.schemaname,
    p.tablename,
    p.policyname,
    coalesce(p.qual, '') || ' ' || coalesce(p.with_check, '') AS expression
  FROM pg_policies p
  WHERE p.schemaname IN ('public', 'elo_core', 'elo_private')
), references AS (
  SELECT
    p.schemaname,
    p.tablename,
    p.policyname,
    match[1] AS capability_code
  FROM policy_text p
  CROSS JOIN LATERAL regexp_matches(
    p.expression,
    'has_capability\(''([^'']+)''',
    'g'
  ) AS match
), summary AS (
  SELECT
    r.capability_code,
    count(*)::bigint AS reference_count,
    count(DISTINCT (r.schemaname, r.tablename))::bigint AS object_count,
    count(c.capability_id) > 0 AS exists_in_catalog,
    bool_or(coalesce(c.active, false)) AS active_in_catalog
  FROM references r
  LEFT JOIN public.elo_capabilities c ON c.code = r.capability_code
  GROUP BY r.capability_code
)
SELECT
  'AUTHZ_CAPABILITY_REFERENCE_INTEGRITY'::text AS finding,
  'elo-authz'::text AS schema_name,
  capability_code AS object_name,
  CASE
    WHEN exists_in_catalog AND active_in_catalog THEN 'PASS'::text
    ELSE 'REVIEW'::text
  END AS severity,
  format(
    'capability=%s references=%s objects=%s exists_in_catalog=%s active_in_catalog=%s',
    capability_code,
    reference_count,
    object_count,
    exists_in_catalog,
    active_in_catalog
  ) AS evidence
FROM summary
ORDER BY
  CASE WHEN exists_in_catalog AND active_in_catalog THEN 1 ELSE 0 END,
  capability_code;
