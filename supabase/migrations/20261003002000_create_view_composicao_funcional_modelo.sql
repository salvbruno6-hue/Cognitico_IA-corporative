CREATE OR REPLACE VIEW public.v_elo_pcp_composicao_funcional_modelo
WITH (security_invoker = true)
AS
SELECT
  emi.modelo_id,
  emi.funcao,
  count(*)::integer AS itens_com_funcao,
  sum(COALESCE(emi.quantidade, 0::numeric)) AS quantidade_itens,
  sum(sum(COALESCE(emi.quantidade, 0::numeric))) OVER (PARTITION BY emi.modelo_id) AS quantidade_total_itens,
  CASE
    WHEN sum(sum(COALESCE(emi.quantidade, 0::numeric))) OVER (PARTITION BY emi.modelo_id) > 0
    THEN sum(COALESCE(emi.quantidade, 0::numeric))
         / sum(sum(COALESCE(emi.quantidade, 0::numeric))) OVER (PARTITION BY emi.modelo_id)
    ELSE NULL::numeric
  END AS participacao_quantitativa
FROM public.estrutura_modular_itens emi
WHERE emi.ativo IS DISTINCT FROM false
  AND emi.modelo_id IS NOT NULL
  AND NULLIF(btrim(emi.funcao), '') IS NOT NULL
GROUP BY emi.modelo_id, emi.funcao;

ALTER VIEW public.v_elo_pcp_composicao_funcional_modelo
  SET (security_invoker = true);

COMMENT ON VIEW public.v_elo_pcp_composicao_funcional_modelo IS
'Camada analitica de evidencia da composicao funcional declarada na estrutura modular por modelo. Reutiliza estrutura_modular_itens; nao representa produtividade, demanda humana, disponibilidade ou contratacao e nao deve ser interpretada como participacao de mao de obra sem validacao operacional.';
