-- ELO MT repair provenance readiness probe
-- Read-only. This query does not create provenance, assign tenants, link units,
-- create models, or mutate repair records. It reports whether persisted repair
-- rows can be promoted beyond governed Forge experience evidence.

WITH repair_identity AS (
  SELECT
    r.id,
    regexp_replace(upper(coalesce(r.numero_container, '')), '[^A-Z0-9]', '', 'g') AS compact_code
  FROM public.mt_ordens_reparo r
), repair_truth AS (
  SELECT
    count(*)::bigint AS repair_rows,
    count(*) FILTER (WHERE tenant_id IS NULL)::bigint AS repair_rows_without_tenant,
    count(*) FILTER (WHERE unidade_modular_id IS NULL)::bigint AS repair_rows_without_unit,
    count(*) FILTER (WHERE numero_container IS NOT NULL AND btrim(numero_container) <> '')::bigint AS repair_rows_with_container
  FROM public.mt_ordens_reparo
), identity_truth AS (
  SELECT
    count(*) FILTER (WHERE compact_code ~ '^MLTM[0-9]+$')::bigint AS repair_rows_with_mltm_numeric_id,
    count(*) FILTER (WHERE compact_code ~ '^MLTM[0-9]{6}$')::bigint AS repair_rows_with_six_digit_id,
    count(DISTINCT ('M' || substring(compact_code from 5 for 2))) FILTER (
      WHERE compact_code ~ '^MLTM[0-9]{2}[0-9]+$'
    )::bigint AS distinct_identifier_model_codes
  FROM repair_identity
), identifier_models AS (
  SELECT DISTINCT ('M' || substring(compact_code from 5 for 2)) AS model_code
  FROM repair_identity
  WHERE compact_code ~ '^MLTM[0-9]{2}[0-9]+$'
), model_truth AS (
  SELECT
    count(*)::bigint AS registered_identifier_model_codes
  FROM identifier_models im
  JOIN public.modelos m
    ON upper(m.codigo) = im.model_code
   AND m.ativo IS TRUE
), unit_truth AS (
  SELECT count(*)::bigint AS modular_unit_rows
  FROM public.mt_unidades_modulares
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
    it.repair_rows_with_mltm_numeric_id,
    it.repair_rows_with_six_digit_id,
    it.distinct_identifier_model_codes,
    mt.registered_identifier_model_codes,
    ut.modular_unit_rows,
    pt.repair_rows_with_provenance,
    greatest(rt.repair_rows - pt.repair_rows_with_provenance, 0)::bigint AS repair_rows_without_provenance
  FROM repair_truth rt
  CROSS JOIN identity_truth it
  CROSS JOIN model_truth mt
  CROSS JOIN unit_truth ut
  CROSS JOIN provenance_truth pt
)
SELECT
  'AUTHZ_MT_REPAIR_PROVENANCE_GAP'::text AS finding,
  'public'::text AS schema_name,
  'mt_ordens_reparo'::text AS object_name,
  'GAP_HIGH'::text AS severity,
  format(
    'repair_rows=%s with_container=%s mltm_numeric_id=%s six_digit_id=%s identifier_model_codes=%s registered_identifier_model_codes=%s modular_unit_rows=%s without_unit=%s without_tenant=%s with_provenance=%s without_provenance=%s',
    repair_rows,
    repair_rows_with_container,
    repair_rows_with_mltm_numeric_id,
    repair_rows_with_six_digit_id,
    distinct_identifier_model_codes,
    registered_identifier_model_codes,
    modular_unit_rows,
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
