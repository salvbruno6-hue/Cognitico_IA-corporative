-- ELO MT repair provenance and reconciliation readiness probe
-- Read-only. This query does not create provenance, assign tenants, link units,
-- create models, or mutate repair records. It distinguishes contextual identity
-- evidence from canonical persistence readiness.

WITH repair_identity AS (
  SELECT
    r.id,
    r.tenant_id,
    r.unidade_modular_id,
    r.numero_container,
    regexp_replace(upper(coalesce(r.numero_container, '')), '[^A-Z0-9]', '', 'g') AS compact_code
  FROM public.mt_ordens_reparo r
), parsed_identity AS (
  SELECT
    ri.*,
    CASE
      WHEN compact_code ~ '^MLTM[0-9]{2}[0-9]+$'
      THEN 'M' || substring(compact_code from 5 for 2)
    END AS short_model_code
  FROM repair_identity ri
), mapped_identity AS (
  SELECT
    p.*,
    coalesce(m_direct.id, m_prefixed.id) AS model_id,
    coalesce(m_direct.codigo, m_prefixed.codigo) AS canonical_model_code
  FROM parsed_identity p
  LEFT JOIN public.modelos m_direct
    ON upper(m_direct.codigo) = p.short_model_code
   AND m_direct.ativo IS TRUE
  LEFT JOIN public.modelos m_prefixed
    ON upper(m_prefixed.codigo) = ('MLT.' || p.short_model_code)
   AND m_prefixed.ativo IS TRUE
), repair_truth AS (
  SELECT
    count(*)::bigint AS repair_rows,
    count(*) FILTER (WHERE tenant_id IS NULL)::bigint AS repair_rows_without_tenant,
    count(*) FILTER (WHERE unidade_modular_id IS NULL)::bigint AS repair_rows_without_unit,
    count(*) FILTER (WHERE numero_container IS NOT NULL AND btrim(numero_container) <> '')::bigint AS repair_rows_with_container
  FROM repair_identity
), identity_truth AS (
  SELECT
    count(*) FILTER (WHERE compact_code ~ '^MLTM[0-9]+$')::bigint AS repair_rows_with_mltm_numeric_id,
    count(*) FILTER (WHERE compact_code ~ '^MLTM[0-9]{6}$')::bigint AS repair_rows_with_six_digit_id,
    count(DISTINCT compact_code) FILTER (WHERE compact_code ~ '^MLTM[0-9]+$')::bigint AS distinct_mltm_identifiers,
    count(*) FILTER (WHERE model_id IS NOT NULL)::bigint AS repair_rows_with_registered_model,
    count(DISTINCT compact_code) FILTER (WHERE model_id IS NOT NULL)::bigint AS distinct_identifiers_with_registered_model,
    count(*) FILTER (WHERE short_model_code IS NOT NULL AND model_id IS NULL)::bigint AS repair_rows_without_registered_model,
    count(DISTINCT compact_code) FILTER (WHERE short_model_code IS NOT NULL AND model_id IS NULL)::bigint AS distinct_identifiers_without_registered_model,
    count(DISTINCT short_model_code) FILTER (WHERE short_model_code IS NOT NULL)::bigint AS distinct_identifier_model_codes,
    count(DISTINCT canonical_model_code) FILTER (WHERE model_id IS NOT NULL)::bigint AS registered_identifier_model_codes
  FROM mapped_identity
), unit_matches AS (
  SELECT
    m.id AS repair_id,
    count(u.id)::bigint AS unit_match_count
  FROM mapped_identity m
  LEFT JOIN public.mt_unidades_modulares u
    ON regexp_replace(upper(coalesce(u.codigo_unidade, '')), '[^A-Z0-9]', '', 'g') = m.compact_code
  GROUP BY m.id
), unit_truth AS (
  SELECT
    (SELECT count(*)::bigint FROM public.mt_unidades_modulares) AS modular_unit_rows,
    count(*) FILTER (WHERE unit_match_count = 1)::bigint AS repair_rows_with_exact_unit_match,
    count(*) FILTER (WHERE unit_match_count > 1)::bigint AS repair_rows_with_ambiguous_unit_match,
    count(*) FILTER (WHERE unit_match_count = 0)::bigint AS repair_rows_without_unit_match
  FROM unit_matches
), provenance_truth AS (
  SELECT
    count(DISTINCT r.id)::bigint AS repair_rows_with_provenance
  FROM public.mt_ordens_reparo r
  JOIN public.mt_proveniencia_registros p
    ON p.tabela_nome = 'mt_ordens_reparo'
   AND p.registro_id = r.id
), summary AS (
  SELECT
    rt.*,
    it.*,
    ut.*,
    pt.repair_rows_with_provenance,
    greatest(rt.repair_rows - pt.repair_rows_with_provenance, 0)::bigint AS repair_rows_without_provenance
  FROM repair_truth rt
  CROSS JOIN identity_truth it
  CROSS JOIN unit_truth ut
  CROSS JOIN provenance_truth pt
)
SELECT
  'AUTHZ_MT_REPAIR_PROVENANCE_GAP'::text AS finding,
  'public'::text AS schema_name,
  'mt_ordens_reparo'::text AS object_name,
  'GAP_HIGH'::text AS severity,
  'CONTEXT_CONFIRMED_PERSISTENCE_PENDING'::text AS reconciliation_state,
  format(
    'repair_rows=%s with_container=%s mltm_numeric_id=%s six_digit_id=%s distinct_mltm_identifiers=%s rows_with_registered_model=%s distinct_ids_with_registered_model=%s rows_without_registered_model=%s distinct_ids_without_registered_model=%s identifier_model_codes=%s registered_identifier_model_codes=%s modular_unit_rows=%s exact_unit_match=%s ambiguous_unit_match=%s without_unit_match=%s without_unit_fk=%s without_tenant=%s with_provenance=%s without_provenance=%s',
    repair_rows,
    repair_rows_with_container,
    repair_rows_with_mltm_numeric_id,
    repair_rows_with_six_digit_id,
    distinct_mltm_identifiers,
    repair_rows_with_registered_model,
    distinct_identifiers_with_registered_model,
    repair_rows_without_registered_model,
    distinct_identifiers_without_registered_model,
    distinct_identifier_model_codes,
    registered_identifier_model_codes,
    modular_unit_rows,
    repair_rows_with_exact_unit_match,
    repair_rows_with_ambiguous_unit_match,
    repair_rows_without_unit_match,
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
