-- ELO MT repair provenance readiness probe
-- Read-only. This query does not create provenance, assign tenants, link units,
-- or mutate repair records. It reports whether persisted repair rows can be
-- promoted beyond governed Forge experience evidence.

WITH repair_truth AS (
  SELECT
    count(*)::bigint AS repair_rows,
    count(*) FILTER (WHERE tenant_id IS NULL)::bigint AS repair_rows_without_tenant,
    count(*) FILTER (WHERE unidade_modular_id IS NULL)::bigint AS repair_rows_without_unit,
    count(*) FILTER (WHERE numero_container IS NOT NULL AND btrim(numero_container) <> '')::bigint AS repair_rows_with_container
  FROM public.mt_ordens_reparo
), provenance_truth AS (
  SELECT
    count(DISTINCT r.id)::bigint AS repair_rows_with_provenance
  FROM public.mt_ordens_reparo r
  JOIN public.mt_proveniencia_registros p
    ON p.tabela_nome = 'mt_ordens_reparo'
   AND p.registro_id = r.id
), summary AS (
  SELECT
    rt.repair_rows,
    rt.repair_rows_without_tenant,
    rt.repair_rows_without_unit,
    rt.repair_rows_with_container,
    pt.repair_rows_with_provenance,
    greatest(rt.repair_rows - pt.repair_rows_with_provenance, 0)::bigint AS repair_rows_without_provenance
  FROM repair_truth rt
  CROSS JOIN provenance_truth pt
)
SELECT
  'AUTHZ_MT_REPAIR_PROVENANCE_GAP'::text AS finding,
  'public'::text AS schema_name,
  'mt_ordens_reparo'::text AS object_name,
  'GAP_HIGH'::text AS severity,
  format(
    'repair_rows=%s with_container=%s without_unit=%s without_tenant=%s with_provenance=%s without_provenance=%s',
    repair_rows,
    repair_rows_with_container,
    repair_rows_without_unit,
    repair_rows_without_tenant,
    repair_rows_with_provenance,
    repair_rows_without_provenance
  ) AS evidence
FROM summary
WHERE repair_rows > 0
  AND (
    repair_rows_without_unit > 0
    OR repair_rows_without_provenance > 0
  );
