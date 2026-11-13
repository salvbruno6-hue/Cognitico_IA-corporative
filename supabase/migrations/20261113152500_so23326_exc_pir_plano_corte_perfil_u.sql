-- SO 233.26 — COMPLEMENTO DE PLANO DE CORTE DO PERFIL U NA VIEW DOS EXC-042/043.
-- Estende a VIEW canônica já existente SEM criar catálogo concorrente, sem alterar preços de EXC.
-- M30 da Lista-Mãe contém comprimento nominal de 2.650mm, com preço por metro.
-- 600: 4×0,60m = 2,40m líquidos, 1 barra 2,65m, sobra 0,25m.
-- 800: 4×0,80m = 3,20m líquidos, 2 barras 2,65m, sobra bruta 2,10m.
-- HIPÓTESES: quatro segmentos iguais, nenhuma perda de serra (kerf) e aquisição de barras integrais.
-- Sobra pode ser aproveitada; a alternativa PEND-GUIA-U-001 tem preço igual,
-- mas não possui equivalência física comprovada e não substitui M30 no EXC.
-- Não criar prejuízo fictício: compra bruta é CENÁRIO, não novo custo APLICADO.
CREATE OR REPLACE VIEW public.vw_elo_orcar_exc_painel_pir_basculantes
WITH (security_invoker = true) AS
SELECT
  e.codigo_excedente,
  e.id AS excedente_id,
  e.descricao AS descricao_excedente,
  e.tipo_instalacao,
  e.unidade,
  e.ativo,
  e.inclui_mao_obra,
  e.memoria_calculo_id,
  c.learning_id,
  c.status AS status_calculo_aprendido,
  m.status_conceito AS status_memoria,
  m.memoria_calculo,
  m.evidencias AS evidencias_memoria,
  v.configuracao,
  v.largura_mm,
  v.altura_mm,
  v.area_abertura_m2,
  v.perimetro_perfil_u_m,
  v.cod_item_basculante,
  v.preco_basculante_lista_mae_brl,
  v.cod_item_perfil_u_candidato,
  v.preco_perfil_u_lista_mae_brl_m,
  v.custo_abertura_historico_brl,
  v.custo_mo_historica_brl,
  v.custo_painel_pir_novo_brl,
  v.custo_total_com_painel_novo_brl,
  v.status_equivalencia_perfil,
  v.status_servicos,
  v.status_validacao_calculo,
  v.aplicar_automaticamente_no_m05,
  coalesce(mat.materiais_e_servicos,'[]'::jsonb) AS itens_materiais_servicos_painel,
  mat.total_itens_brl AS custo_materiais_servicos_cadastrado_brl,
  coalesce(mob.mao_obra,'[]'::jsonb) AS mao_obra_detalhada,
  mob.total_mao_obra_brl AS custo_mao_obra_cadastrada_brl,
  e.custo_total AS custo_excedente_cadastrado_brl,
  v.custo_adequacao_painel_existente_referencial_brl AS custo_referencial_dinamico_brl,
  round(v.custo_adequacao_painel_existente_referencial_brl-e.custo_total,2) AS diferenca_referencia_e_cadastro_brl,
  CASE
    WHEN v.custo_adequacao_painel_existente_referencial_brl IS NULL THEN 'GAP_PRECO_CATALOGO'
    WHEN e.custo_total IS NULL THEN 'GAP_CUSTO_CADASTRADO'
    WHEN abs(v.custo_adequacao_painel_existente_referencial_brl-e.custo_total)>0.01 THEN 'DIVERGENCIA_PRECO_REVISAR_EXC'
    ELSE 'CONSISTENTE_APENAS_ARITMETICAMENTE'
  END AS status_conciliacao,
  'PENDING_VALIDATION | EXC INATIVA | PIR NOVO EXCLUIDO | PERFIL M30 CANDIDATO | MO 2023 NAO HOMOLOGADA | NAO SOMAR AUTOMATICAMENTE AO M05'::text AS gate_de_uso,
  2.65::numeric AS perfil_m30_comprimento_barra_nominal_m,
  4::integer AS perfil_segmentos_por_conjunto,
  round(v.largura_mm::numeric/1000,3) AS perfil_segmento_comprimento_m,
  corte.segmentos_por_barra_sem_kerf,
  corte.barras_minimas_sem_kerf,
  round((corte.barras_minimas_sem_kerf*2.65)::numeric,2) AS perfil_compra_bruta_m,
  round((corte.barras_minimas_sem_kerf*2.65-v.perimetro_perfil_u_m)::numeric,2) AS perfil_sobra_bruta_teorica_m,
  CASE WHEN v.preco_perfil_u_lista_mae_brl_m IS NOT NULL
       THEN round((corte.barras_minimas_sem_kerf*2.65*v.preco_perfil_u_lista_mae_brl_m)::numeric,2)
       ELSE NULL::numeric END AS perfil_compra_barras_inteiras_brl,
  CASE WHEN v.preco_perfil_u_lista_mae_brl_m IS NOT NULL
       THEN round(((corte.barras_minimas_sem_kerf*2.65-v.perimetro_perfil_u_m)*v.preco_perfil_u_lista_mae_brl_m)::numeric,2)
       ELSE NULL::numeric END AS perfil_delta_compra_menos_consumo_brl,
  CASE WHEN v.preco_perfil_u_lista_mae_brl_m IS NOT NULL AND e.custo_total IS NOT NULL
       THEN round((e.custo_total+(corte.barras_minimas_sem_kerf*2.65-v.perimetro_perfil_u_m)*v.preco_perfil_u_lista_mae_brl_m)::numeric,2)
       ELSE NULL::numeric END AS custo_exc_se_compra_integral_alocada_brl,
  'ESTIMATIVA DE AQUISICAO: 4 segmentos iguais, barras M30 nominal 2,65m, SEM perda de serra; estoque, corte e aproveitamento a verificar. NAO REPRECIFICAR EXC.'::text AS status_plano_corte,
  (SELECT lm.valor_unitario FROM public.lista_mae lm WHERE lm.cod_item='PEND-GUIA-U-001' AND lm.ativo IS TRUE) AS preco_guia_u_alternativa_nao_homologada_brl_m
FROM public.excedentes e
JOIN public.elo_orcamento_memoria m ON m.id=e.memoria_calculo_id
JOIN public.elo_orcamento_calculos_aprendidos c
  ON c.learning_id=m.memoria_calculo->>'calculo_aprendido_learning_id'
 AND c.origem_so=m.origem_so
JOIN public.vw_elo_orcar_painel_pir_basculantes v
  ON v.learning_id=c.learning_id
 AND v.largura_mm=(m.memoria_calculo->>'lado_m')::numeric*1000
LEFT JOIN LATERAL (
 SELECT
   jsonb_agg(jsonb_build_object(
     'sequencia',i.sequencia,'tipo_componente',i.tipo_componente,
     'cod_item',i.cod_item,'descricao',i.descricao,'unidade',i.unidade,
     'quantidade',i.quantidade,'valor_unitario',i.valor_unitario,
     'valor_parcial',case when i.tipo_componente='REFERENCIA_NAO_FATURAVEL' then NULL ELSE i.valor_parcial END,
     'valor_total',i.valor_total,'observacao',i.observacao
   ) ORDER BY i.sequencia) AS materiais_e_servicos,
   round(sum(i.valor_total),2) AS total_itens_brl
 FROM public.excedente_itens i WHERE i.excedente_id=e.id
) mat ON true
LEFT JOIN LATERAL (
 SELECT
   jsonb_agg(jsonb_build_object(
     'sequencia',x.sequencia,'funcao',x.funcao,'quantidade',x.quantidade,
     'tempo',x.tempo,'unidade_tempo',x.unidade_tempo,'valor_unitario',x.valor_unitario,
     'valor_parcial',x.valor_parcial,'observacao',x.observacao
   ) ORDER BY x.sequencia) AS mao_obra,
   round(sum(x.valor_parcial),2) AS total_mao_obra_brl
 FROM public.excedente_mao_obra x WHERE x.excedente_id=e.id
) mob ON true
LEFT JOIN LATERAL (
  SELECT
    floor(2.65::numeric/nullif(v.largura_mm::numeric/1000,0))::integer AS segmentos_por_barra_sem_kerf,
    ceil(4::numeric/nullif(floor(2.65::numeric/nullif(v.largura_mm::numeric/1000,0)),0))::integer AS barras_minimas_sem_kerf
) corte ON true
WHERE e.codigo_excedente IN ('EXC-042','EXC-043')
 AND e.origem LIKE 'SO 233.26 | QA01%';


COMMENT ON VIEW public.vw_elo_orcar_exc_painel_pir_basculantes IS
'EXC-042/043 painel PIR existente: memoria, materiais, MO e plano teorico de corte de perfil M30 barra 2,65m. Preco do EXC usa consumo liquido, compra integral apenas cenario de suprimentos; kerf, saldos, equivalencia e mao de obra nao homologados. Service-role somente.';
REVOKE ALL ON public.vw_elo_orcar_exc_painel_pir_basculantes FROM PUBLIC, anon, authenticated;
GRANT SELECT ON public.vw_elo_orcar_exc_painel_pir_basculantes TO service_role;
-- Teste: SELECT codigo_excedente,perfil_segmentos_por_conjunto,segmentos_por_barra_sem_kerf,barras_minimas_sem_kerf,perfil_compra_bruta_m,perfil_sobra_bruta_teorica_m,perfil_compra_barras_inteiras_brl,perfil_delta_compra_menos_consumo_brl,custo_excedente_cadastrado_brl,custo_exc_se_compra_integral_alocada_brl FROM public.vw_elo_orcar_exc_painel_pir_basculantes ORDER BY largura_mm;
