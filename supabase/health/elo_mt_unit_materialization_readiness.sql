-- ELO MT modular-unit materialization readiness probe
-- Read-only. This query does not create units, models, provenance, tenant links,
-- production orders, locations, or authorization state.
-- It classifies legacy repair identifiers by whether a canonical active model
-- already exists and whether a physical unit is already materialized.

WITH tenant AS (
  SELECT id
  FROM public.mt_tenants
  WHERE codigo = 'MULTITEINER'
    AND ativo IS TRUE
  LIMIT 1
), repair_ids AS (
  SELECT
    regexp_replace(upper(r.numero_container), '[^A-Z0-9]', '', 'g') AS compact_code,
    'M' || substring(
      regexp_replace(upper(r.numero_container), '[^A-Z0-9]', '', 'g')
      FROM 5 FOR 2
    ) AS parsed_model_code
  FROM public.mt_ordens_reparo r
  WHERE r.numero_container IS NOT NULL
    AND regexp_replace(upper(r.numero_container), '[^A-Z0-9]', '', 'g') ~ '^MLTM[0-9]{2}[0-9]+$'
), distinct_ids AS (
  SELECT DISTINCT compact_code, parsed_model_code
  FROM repair_ids
), resolved AS (
  SELECT
    d.compact_code,
    d.parsed_model_code,
    m.id AS model_id,
    m.codigo AS canonical_model_code,
    u.id AS unit_id,
    CASE
      WHEN m.id IS NULL THEN 'BLOCKED_MODEL_GAP'
      WHEN u.id IS NOT NULL THEN 'ALREADY_MATERIALIZED'
      ELSE 'CANDIDATE_MODEL_MATCH'
    END AS materialization_state
  FROM distinct_ids d
  LEFT JOIN LATERAL (
    SELECT m1.id, m1.codigo
    FROM public.modelos m1
    WHERE m1.ativo IS TRUE
      AND (
        upper(m1.codigo) = d.parsed_model_code
        OR upper(m1.codigo) = 'MLT.' || d.parsed_model_code
      )
    ORDER BY CASE WHEN upper(m1.codigo) = d.parsed_model_code THEN 0 ELSE 1 END
    LIMIT 1
  ) m ON TRUE
  LEFT JOIN tenant t ON TRUE
  LEFT JOIN public.mt_unidades_modulares u
    ON u.tenant_id = t.id
   AND regexp_replace(upper(u.codigo_unidade), '[^A-Z0-9]', '', 'g') = d.compact_code
)
SELECT
  materialization_state,
  count(*)::bigint AS distinct_identifiers,
  count(*) FILTER (WHERE canonical_model_code IS NOT NULL)::bigint AS with_canonical_model,
  count(*) FILTER (WHERE unit_id IS NOT NULL)::bigint AS already_materialized,
  array_agg(DISTINCT parsed_model_code ORDER BY parsed_model_code) AS parsed_model_codes
FROM resolved
GROUP BY materialization_state
ORDER BY materialization_state;
