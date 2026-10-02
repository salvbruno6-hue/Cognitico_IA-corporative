CREATE OR REPLACE VIEW public.v_elo_pcp_carga_capacidade_periodo
WITH (security_invoker = true)
AS
WITH linhas AS (
  SELECT
    l.id AS linha_plano_id,
    l.modelo_id,
    l.quantidade_planejada,
    l.inicio_planejado,
    l.fim_planejado
  FROM public.mt_linhas_plano_pcp l
  WHERE COALESCE(l.quantidade_planejada, 0) > 0
    AND l.inicio_planejado IS NOT NULL
    AND l.fim_planejado IS NOT NULL
    AND l.fim_planejado >= l.inicio_planejado
),
roteiro AS (
  SELECT
    r.modelo_id,
    r.centro_trabalho_id,
    SUM(COALESCE(r.minutos_padrao, 0) + COALESCE(r.minutos_setup, 0)) AS minutos_por_unidade
  FROM public.mt_operacoes_roteiro r
  GROUP BY r.modelo_id, r.centro_trabalho_id
),
carga_diaria AS (
  SELECT
    l.inicio_planejado + gs.dia AS data_referencia,
    r.centro_trabalho_id,
    SUM(l.quantidade_planejada) AS quantidade_planejada,
    SUM(
      (l.quantidade_planejada * r.minutos_por_unidade)
      / NULLIF((l.fim_planejado - l.inicio_planejado + 1), 0)
    ) / 60.0 AS carga_horas_planejada
  FROM linhas l
  JOIN roteiro r ON r.modelo_id = l.modelo_id
  CROSS JOIN LATERAL generate_series(
    0,
    (l.fim_planejado - l.inicio_planejado)
  ) AS gs(dia)
  GROUP BY l.inicio_planejado + gs.dia, r.centro_trabalho_id
),
capacidade AS (
  SELECT
    c.data_capacidade AS data_referencia,
    c.centro_trabalho_id,
    SUM(COALESCE(c.quantidade_disponivel, 0)) AS capacidade_disponivel,
    SUM(COALESCE(c.quantidade_padrao, 0)) AS capacidade_padrao,
    SUM(COALESCE(c.quantidade_recuperacao, 0)) AS capacidade_recuperacao,
    SUM(COALESCE(c.quantidade_bloqueada, 0)) AS capacidade_bloqueada
  FROM public.mt_capacidade_diaria c
  GROUP BY c.data_capacidade, c.centro_trabalho_id
)
SELECT
  COALESCE(c.data_referencia, d.data_referencia) AS data_referencia,
  ct.id AS centro_trabalho_id,
  ct.codigo AS centro_trabalho_codigo,
  ct.nome AS centro_trabalho_nome,
  ct.unidade_capacidade,
  COALESCE(d.quantidade_planejada, 0) AS quantidade_planejada,
  COALESCE(d.carga_horas_planejada, 0) AS carga_horas_planejada,
  COALESCE(c.capacidade_disponivel, 0) AS capacidade_disponivel,
  COALESCE(c.capacidade_padrao, 0) AS capacidade_padrao,
  COALESCE(c.capacidade_recuperacao, 0) AS capacidade_recuperacao,
  COALESCE(c.capacidade_bloqueada, 0) AS capacidade_bloqueada,
  CASE
    WHEN lower(COALESCE(ct.unidade_capacidade, '')) IN ('h', 'hora', 'horas')
    THEN COALESCE(c.capacidade_disponivel, 0) - COALESCE(d.carga_horas_planejada, 0)
    ELSE NULL
  END AS folga_horas,
  CASE
    WHEN lower(COALESCE(ct.unidade_capacidade, '')) IN ('h', 'hora', 'horas')
     AND COALESCE(c.capacidade_disponivel, 0) > 0
    THEN ROUND(
      100.0 * COALESCE(d.carga_horas_planejada, 0)
      / c.capacidade_disponivel, 2
    )
    ELSE NULL
  END AS utilizacao_pct,
  CASE
    WHEN lower(COALESCE(ct.unidade_capacidade, '')) IN ('h', 'hora', 'horas')
     AND COALESCE(c.capacidade_disponivel, 0) < COALESCE(d.carga_horas_planejada, 0)
    THEN true
    WHEN lower(COALESCE(ct.unidade_capacidade, '')) IN ('h', 'hora', 'horas')
    THEN false
    ELSE NULL
  END AS excesso_carga
FROM capacidade c
FULL OUTER JOIN carga_diaria d
  ON d.data_referencia = c.data_referencia
 AND d.centro_trabalho_id = c.centro_trabalho_id
JOIN public.mt_centros_trabalho ct
  ON ct.id = COALESCE(c.centro_trabalho_id, d.centro_trabalho_id);

COMMENT ON VIEW public.v_elo_pcp_carga_capacidade_periodo IS
'PCP — carga teórica diária por centro de trabalho versus capacidade diária disponível. A carga é distribuída linearmente entre as datas planejadas e só é comparada em horas quando a unidade do centro indica horas.';
