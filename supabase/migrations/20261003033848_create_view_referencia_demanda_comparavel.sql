CREATE OR REPLACE VIEW public.v_elo_pcp_referencia_demanda_comparavel
WITH (security_invoker = true)
AS
WITH historico AS (
  SELECT
    dh.tenant_id,
    dh.modelo_id,
    dh.natureza_demanda,
    dh.chave_comparabilidade,
    dh.periodo_inicio,
    dh.periodo_fim,
    SUM(dh.quantidade_real) AS quantidade_historica
  FROM public.mt_demanda_historico dh
  WHERE dh.modelo_id IS NOT NULL
    AND dh.periodo_inicio IS NOT NULL
    AND dh.periodo_fim IS NOT NULL
    AND dh.quantidade_real IS NOT NULL
    AND dh.quantidade_real >= 0
  GROUP BY dh.tenant_id, dh.modelo_id, dh.natureza_demanda,
           dh.chave_comparabilidade, dh.periodo_inicio, dh.periodo_fim
),
previsao AS (
  SELECT
    pd.tenant_id,
    pd.modelo_id,
    pd.natureza_demanda,
    pd.chave_comparabilidade,
    pd.periodo_inicio,
    pd.periodo_fim,
    SUM(pd.quantidade_prevista) AS quantidade_prevista
  FROM public.mt_previsoes_demanda pd
  WHERE pd.modelo_id IS NOT NULL
    AND pd.periodo_inicio IS NOT NULL
    AND pd.periodo_fim IS NOT NULL
    AND pd.quantidade_prevista IS NOT NULL
    AND pd.quantidade_prevista >= 0
  GROUP BY pd.tenant_id, pd.modelo_id, pd.natureza_demanda,
           pd.chave_comparabilidade, pd.periodo_inicio, pd.periodo_fim
),
comparavel AS (
  SELECT
    COALESCE(h.tenant_id, p.tenant_id) AS tenant_id,
    COALESCE(h.modelo_id, p.modelo_id) AS modelo_id,
    COALESCE(h.natureza_demanda, p.natureza_demanda) AS natureza_demanda,
    COALESCE(h.chave_comparabilidade, p.chave_comparabilidade) AS chave_comparabilidade,
    h.periodo_inicio AS historico_periodo_inicio,
    h.periodo_fim AS historico_periodo_fim,
    h.quantidade_historica,
    p.periodo_inicio AS previsao_periodo_inicio,
    p.periodo_fim AS previsao_periodo_fim,
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
  c.historico_periodo_inicio,
  c.historico_periodo_fim,
  c.quantidade_historica,
  c.previsao_periodo_inicio,
  c.previsao_periodo_fim,
  c.quantidade_prevista,
  c.estado_comparabilidade
FROM comparavel c
JOIN public.modelos m ON m.id = c.modelo_id
LEFT JOIN public.taxonomia t ON t.id = m.taxonomia_id;

ALTER VIEW public.v_elo_pcp_referencia_demanda_comparavel
  SET (security_invoker = true);

COMMENT ON VIEW public.v_elo_pcp_referencia_demanda_comparavel IS
'Base analitica para reconstruir referencia historica comparavel entre demanda realizada e previsao. Compara por tenant, modelo, natureza e chave quando necessaria. EVENTO e SPOT sem chave sao GAP; outras naturezas sem chave podem ser comparadas apenas como potencial e exigem validacao. Nao calcula fator, produtividade ou demanda humana.';
