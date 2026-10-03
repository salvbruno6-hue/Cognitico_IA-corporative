CREATE OR REPLACE VIEW public.v_elo_pcp_referencia_demanda_comparavel
WITH (security_invoker = true)
AS
WITH parametros AS (
  SELECT
    DATE '2025-09-01' AS historico_inicio,
    DATE '2026-02-28' AS historico_fim,
    DATE '2026-09-01' AS previsao_inicio,
    DATE '2027-02-28' AS previsao_fim
),
historico AS (
  SELECT
    dh.tenant_id,
    dh.modelo_id,
    dh.natureza_demanda,
    dh.chave_comparabilidade,
    SUM(dh.quantidade_real) AS quantidade_historica
  FROM public.mt_demanda_historico dh
  CROSS JOIN parametros p
  WHERE dh.modelo_id IS NOT NULL
    AND dh.periodo_inicio >= p.historico_inicio
    AND dh.periodo_fim <= p.historico_fim
    AND dh.quantidade_real IS NOT NULL
    AND dh.quantidade_real >= 0
  GROUP BY dh.tenant_id, dh.modelo_id, dh.natureza_demanda, dh.chave_comparabilidade
),
previsao AS (
  SELECT
    pd.tenant_id,
    pd.modelo_id,
    pd.natureza_demanda,
    pd.chave_comparabilidade,
    SUM(pd.quantidade_prevista) AS quantidade_prevista
  FROM public.mt_previsoes_demanda pd
  CROSS JOIN parametros p
  WHERE pd.modelo_id IS NOT NULL
    AND pd.periodo_inicio >= p.previsao_inicio
    AND pd.periodo_fim <= p.previsao_fim
    AND pd.quantidade_prevista IS NOT NULL
    AND pd.quantidade_prevista >= 0
  GROUP BY pd.tenant_id, pd.modelo_id, pd.natureza_demanda, pd.chave_comparabilidade
),
comparavel AS (
  SELECT
    COALESCE(h.tenant_id, p.tenant_id) AS tenant_id,
    COALESCE(h.modelo_id, p.modelo_id) AS modelo_id,
    COALESCE(h.natureza_demanda, p.natureza_demanda) AS natureza_demanda,
    COALESCE(h.chave_comparabilidade, p.chave_comparabilidade) AS chave_comparabilidade,
    h.quantidade_historica,
    p.quantidade_prevista,
    CASE
      WHEN COALESCE(h.natureza_demanda, p.natureza_demanda) IS NULL
        THEN 'SEM_NATUREZA'
      WHEN upper(COALESCE(h.natureza_demanda, p.natureza_demanda)) IN ('EVENTO','SPOT')
       AND COALESCE(h.chave_comparabilidade, p.chave_comparabilidade) IS NULL
        THEN 'SEM_CHAVE_COMPARABILIDADE'
      WHEN h.modelo_id IS NULL THEN 'SEM_HISTORICO'
      WHEN p.modelo_id IS NULL THEN 'SEM_PREVISAO'
      ELSE 'COMPARAVEL_POTENCIAL'
    END AS estado_comparabilidade
  FROM historico h
  FULL OUTER JOIN previsao p
    ON p.tenant_id = h.tenant_id
   AND p.modelo_id = h.modelo_id
   AND p.natureza_demanda IS NOT DISTINCT FROM h.natureza_demanda
   AND (
        p.chave_comparabilidade = h.chave_comparabilidade
        OR (
          p.chave_comparabilidade IS NULL
          AND h.chave_comparabilidade IS NULL
          AND upper(COALESCE(p.natureza_demanda, h.natureza_demanda)) NOT IN ('EVENTO','SPOT')
        )
   )
)
SELECT
  c.tenant_id,
  c.modelo_id,
  m.codigo AS modelo_codigo,
  m.nome AS modelo_nome,
  m.familia AS modelo_familia,
  t.id AS taxonomia_id,
  t.codigo AS taxonomia_codigo,
  t.familia AS taxonomia_familia,
  t.tipo AS taxonomia_tipo,
  c.natureza_demanda,
  c.chave_comparabilidade,
  DATE '2025-09-01' AS historico_periodo_inicio,
  DATE '2026-02-28' AS historico_periodo_fim,
  c.quantidade_historica,
  DATE '2026-09-01' AS previsao_periodo_inicio,
  DATE '2027-02-28' AS previsao_periodo_fim,
  c.quantidade_prevista,
  c.estado_comparabilidade
FROM comparavel c
JOIN public.modelos m ON m.id = c.modelo_id
LEFT JOIN public.taxonomia t ON t.id = m.taxonomia_id;

ALTER VIEW public.v_elo_pcp_referencia_demanda_comparavel
  SET (security_invoker = true);

COMMENT ON VIEW public.v_elo_pcp_referencia_demanda_comparavel IS
'Referencia comparavel do ciclo de crescimento Sep/2025-Feb/2026 versus Sep/2026-Feb/2027. Agrega a demanda historica e a previsao dentro de cada horizonte, preservando tenant, modelo, natureza e chave de comparabilidade. EVENTO e SPOT sem chave sao GAP. Nao calcula fator, produtividade ou demanda humana.';
