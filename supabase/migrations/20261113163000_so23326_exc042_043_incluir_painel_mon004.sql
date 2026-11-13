-- SO 233.26: correcao supervisionada: preco de PAINEL PIR 40mm esta na Lista-Mae.
-- MON004 = PAINEL FRIGO PIRAP AP 40MM 1130X2650MM, preco R$164,12/m².
-- Uma placa inteira 1,13m×2,65m=2,9945m² => custo R$491,46. Sem assumir custo zero.
-- Composicao EXC042=R$277,66+R$491,46=R$769,12; EXC043=R$387,96+R$491,46=R$879,42.
-- Fronteira: passa de ADEQUACAO SOBRE PAINEL EXISTENTE para FORNECIMENTO
-- DE UM PAINEL INTEIRO MON004 COM BASCULANTE, ainda INATIVO.
-- O painel historico 2023 STUC PIR 40mm e o produto MON004 requerem equivalencia tecnica;
-- uma placa inteira por conjunto e premissa de fornecimento, sujeita a engenharia.
-- Nenhuma aplicacao no M05: basculantes e RH ja parcialmente orcadas.
-- Mantem demonstrativo_individual_v1 preservado, cria v2 com fonte MON004.
DO $pir_mono$
DECLARE
 v_preco numeric; v_un text; v_atualizados integer; v_count integer;
BEGIN
 SELECT valor_unitario,un INTO v_preco,v_un
 FROM public.lista_mae
 WHERE cod_item='MON004' AND ativo IS TRUE;
 IF v_preco IS NULL OR v_preco<=0 OR v_un<>'m²' THEN
   RAISE EXCEPTION 'MON004 nao esta vigente ou unidade do painel nao e m²; revisar antes de compor EXC';
 END IF;
 SELECT count(*) INTO v_count FROM public.excedentes e
 WHERE e.codigo_excedente IN ('EXC-042','EXC-043') AND e.ativo=false
   AND e.memoria_calculo_id IS NOT NULL;
 IF v_count <> 2 THEN RAISE EXCEPTION 'EXC042/043 inexistente, ativa ou sem memoria; abortando'; END IF;
 SELECT count(*) INTO v_count FROM public.excedente_itens i
 JOIN public.excedentes e ON e.id=i.excedente_id
 WHERE e.codigo_excedente IN ('EXC-042','EXC-043') AND i.sequencia=4
   AND i.tipo_componente='REFERENCIA_NAO_FATURAVEL'
   AND i.cod_item IS NULL AND i.quantidade=1;
 IF v_count=2 THEN
   UPDATE public.excedente_itens i SET
     cod_item='MON004', tipo_componente='MATERIAL',
     quantidade=(1.13::numeric*2.65::numeric),
     observacao='1 painel PIR 40mm MON004 novo 1130×2650 por conjunto, 2,9945 m² × preço Lista-Mãe. Compatibilidade com STUC 2023 e necessidade de placa inteira pendentes de validação.'
   FROM public.excedentes e
   WHERE i.excedente_id=e.id AND e.codigo_excedente IN ('EXC-042','EXC-043')
      AND e.ativo=false AND i.sequencia=4 AND i.tipo_componente='REFERENCIA_NAO_FATURAVEL';
   GET DIAGNOSTICS v_atualizados = ROW_COUNT;
   IF v_atualizados<>2 THEN RAISE EXCEPTION 'Quantidade de linhas MON004 atualizadas inesperada %',v_atualizados; END IF;
 ELSIF v_count=0 THEN
   SELECT count(*) INTO v_count FROM public.excedente_itens i
   JOIN public.excedentes e ON e.id=i.excedente_id
   WHERE e.codigo_excedente IN ('EXC-042','EXC-043') AND i.sequencia=4
     AND i.cod_item='MON004' AND i.quantidade=2.9945 AND i.tipo_componente='MATERIAL';
   IF v_count<>2 THEN RAISE EXCEPTION 'Estado intermediario/legado invalido dos paineis EXC; abortar e investigar'; END IF;
 ELSE
   RAISE EXCEPTION 'Estado parcial dos EXC042/043: % placeholders; investigar',v_count;
 END IF;
 UPDATE public.excedentes e SET
   descricao=replace(replace(e.descricao,'Painel PIR 40mm EXISTENTE — abertura e fixacao',
                                      'Painel PIR 40mm NOVO MON004 — fornecimento, abertura e fixacao'),
                                      'PAINEL PIR 40mm EXISTENTE','PAINEL PIR 40mm NOVO MON004'),
   observacao=coalesce(e.observacao,'')||' | CORRECAO: MON004 painel PIR40 novo 1130×2650, 2,9945 m² ao preco Lista-Mãe, registrado na linha material seq4. Valor mudou com custo de painel, EXC ainda inativa. Memoria v1 preservada e v2 detalhada.',
   ativo=false
 WHERE e.codigo_excedente IN('EXC-042','EXC-043')
 AND e.ativo=false AND e.descricao LIKE '%EXISTENTE%';
 SELECT count(*) INTO v_count FROM public.excedentes e
 WHERE e.codigo_excedente IN('EXC-042','EXC-043')
   AND e.ativo=false
   AND ((e.codigo_excedente='EXC-042' AND e.custo_total=round(277.66+2.9945*v_preco,2))
     OR(e.codigo_excedente='EXC-043' AND e.custo_total=round(387.96+2.9945*v_preco,2)));
 IF v_count<>2 THEN RAISE EXCEPTION 'Custo EXC com painel nao reconciliou: %/2',v_count; END IF;
END;
$pir_mono$;

-- Atualiza individualmente cada memoria usando seu proprio codigo EXC.
-- Preserva demonstrativo_individual_v1 para os custos de adaptacao anterior.
UPDATE public.elo_orcamento_memoria m
SET
 memoria_calculo = m.memoria_calculo || jsonb_build_object(
  'painel_pir_novo_incluso',true,
  'painel_pir_novo_codigo','MON004',
  'painel_pir_novo_area_m2',2.9945,
  'painel_pir_novo_preco_lista_mae_m2_brl',
   (SELECT valor_unitario FROM public.lista_mae WHERE cod_item='MON004' AND ativo),
  'custo_painel_pir_novo_brl',pir.custo_painel_brl,
  'custo_referencial_snapshot_com_pir_novo_brl',e.custo_total,
  'escopo_novo','1 PAINEL PIR NOVO MON004 1130×2650 COM BASCULANTE; base anterior v1 para adaptacao painel existente',
  'fonte_correcao','Analista: valor do painel PIR consta na Lista-Mãe. SKU MON004 identificado e calculado.',
  'painel_STUC_e_MON004_equivalencia_comprovada',false,
  'uma_placa_inteira_necessaria_comprovada',false,
  'estado','PENDING_VALIDATION',
  'demonstrativo_individual_v2',jsonb_build_object(
    'identificacao',jsonb_build_object('codigo_excedente',e.codigo_excedente,
      'memoria_individual_id',m.id,'origem_so','SO 233.26',
      'dimensao_basculante_mm',case when e.codigo_excedente='EXC-042' then 600 else 800 end,
      'calculo_base_geral_id',124,'escopo','PIR NOVO MON004 + BASCULANTE',
      'status','PENDING_VALIDATION'),
    'materiais_e_abertura',(SELECT coalesce(jsonb_agg(jsonb_build_object(
      'seq',i.sequencia,'descricao',i.descricao,'codigo_lista_mae',i.cod_item,
      'tipo',i.tipo_componente,'quantidade',i.quantidade,'unidade',i.unidade,
      'preco_unitario_brl',i.valor_unitario,'parcial_brl',i.valor_parcial)
      ORDER BY i.sequencia),'[]'::jsonb) FROM public.excedente_itens i WHERE i.excedente_id=e.id),
    'mao_de_obra',(SELECT coalesce(jsonb_agg(jsonb_build_object(
      'seq',z.sequencia,'funcao',z.funcao,'profissionais',z.quantidade,
      'tempo_por_profissional_dia',z.tempo,'valor_dia_brl',z.valor_unitario,
      'subtotal_brl',z.valor_parcial)
      ORDER BY z.sequencia),'[]'::jsonb) FROM public.excedente_mao_obra z WHERE z.excedente_id=e.id),
    'subtotal_material_e_abertura_brl',
      (SELECT round(coalesce(sum(i.valor_total),0),2) FROM public.excedente_itens i WHERE i.excedente_id=e.id),
    'subtotal_mao_de_obra_brl',
      (SELECT round(coalesce(sum(z.valor_parcial),0),2) FROM public.excedente_mao_obra z WHERE z.excedente_id=e.id),
    'custo_unitario_cadastrado_brl',e.custo_total,
    'formula_painel','1.13 m x 2.65 m = 2.9945 m²; x MON004 R$164.12/m² = R$491.46',
    'formula_total_custo','Basculante ESQ006/ESQ007 + perimetro U M30 x preço/m + abertura vao 25.59 + MO historica 51.17 + MON004 2.9945m² x preco/m²',
    'custo_sem_pir_novo_referencial_brl',case when e.codigo_excedente='EXC-042' then 277.66 else 387.96 end,
    'custo_painel_pir_novo_brl',pir.custo_painel_brl,
    'painel_pir_novo_incluso',true,
    'equivalencia_tecnica_STUC_MON004_validada',false,
    'preco_homologado',false,
    'aplicado_m05',false,
    'observacoes',jsonb_build_array(
      'Uma placa MON004 inteira por EXC é premissa de orçamento, sem prova de necessidade exata.',
      'Painel PIR 40mm MON004 tem preço identificado na Lista-Mãe; não confundir com painel histórico STUC 2023.',
      'Abertura e MO são referências de 2023; perfil U M30 ainda requer equivalência. EXC permanece inativa.')
  )
 ),
 evidencias=coalesce(m.evidencias,'{}'::jsonb)||jsonb_build_object(
  'painel_catalogo_codigo','MON004',
  'painel_catalogo_fonte','public.lista_mae, unidade m²',
  'versao_memoria_atual','demonstrativo_individual_v2',
  'memoria_anterior_preservada',true,
  'validacao_tecnica_pendente',true),
 resultado='Composicao COMPLETA REFERENCIAL para painel PIR novo MON004 1 placa mais basculante: R$'||to_char(e.custo_total,'FM99999990.00')||'/UN; fonte catalogo, escopo de placa inteira e equivalencia a STUC ainda sujeitos a validacao.'
FROM public.excedentes e
JOIN LATERAL (SELECT i.valor_parcial AS custo_painel_brl FROM public.excedente_itens i
   WHERE i.excedente_id=e.id AND i.cod_item='MON004' LIMIT 1) pir ON true
WHERE m.id=e.memoria_calculo_id
  AND e.codigo_excedente IN ('EXC-042','EXC-043')
  AND m.origem_so='SO 233.26'
  AND NOT (m.memoria_calculo ? 'demonstrativo_individual_v2');

-- Fonte do aprendizado não é uma regra do Core: registra o avanço de custo e limitações.
UPDATE public.elo_orcamento_calculos_aprendidos c
 SET resultado=coalesce(c.resultado,'{}'::jsonb)||jsonb_build_object(
 'MON004_painel_PIR_novo_catalogo',jsonb_build_object(
   'codigo','MON004','descricao','PAINEL FRIGO PIRAP AP 40MM 1130X2650MM',
   'area_m2',2.9945,'unidade_preco','m²',
   'preco_unitario_atual_lista_mae_brl_m2',164.12,
   'custo_painel_completo_brl',491.46,
   'EXC-042_total_brl',769.12,'EXC-043_total_brl',879.42,
   'memorias_versionadas','demonstrativo_individual_v2',
   'composicoes_inativas',true,
   'painel_STUC_equivalencia_validada',false,
   'compra_placa_inteira_confirmada',false,
   'financeiro_M05_alterado',false,
   'status','CUSTO_CATALOGADO_INCLUIDO_REFERENCIAL_VALIDACAO_TECNICA_PENDENTE'),
 'painel_pir_novo_incluido',true,
 'preco_de_painel_PIR_novo_disponivel',true
 )
WHERE c.learning_id='SO23326-PIR-BASC-800-600-20261113'
AND c.origem_so='SO 233.26' AND c.status='PENDING_VALIDATION'
AND NOT (c.resultado ? 'MON004_painel_PIR_novo_catalogo');

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
  pir.custo_painel_novo_cadastrado_brl::numeric AS custo_painel_pir_novo_brl,
  CASE WHEN pir.custo_painel_novo_atual_brl IS NOT NULL
       AND v.custo_adequacao_painel_existente_referencial_brl IS NOT NULL
       THEN round(v.custo_adequacao_painel_existente_referencial_brl+pir.custo_painel_novo_atual_brl,2)
       ELSE NULL::numeric END AS custo_total_com_painel_novo_brl,
  v.status_equivalencia_perfil,
  v.status_servicos,
  v.status_validacao_calculo,
  v.aplicar_automaticamente_no_m05,
  coalesce(mat.materiais_e_servicos,'[]'::jsonb) AS itens_materiais_servicos_painel,
  mat.total_itens_brl AS custo_materiais_servicos_cadastrado_brl,
  coalesce(mob.mao_obra,'[]'::jsonb) AS mao_obra_detalhada,
  mob.total_mao_obra_brl AS custo_mao_obra_cadastrada_brl,
  e.custo_total AS custo_excedente_cadastrado_brl,
  CASE WHEN pir.custo_painel_novo_atual_brl IS NOT NULL
             AND v.custo_adequacao_painel_existente_referencial_brl IS NOT NULL
       THEN round(v.custo_adequacao_painel_existente_referencial_brl+pir.custo_painel_novo_atual_brl,2)
       ELSE NULL::numeric END AS custo_referencial_dinamico_brl,
  CASE WHEN pir.custo_painel_novo_atual_brl IS NOT NULL
             AND v.custo_adequacao_painel_existente_referencial_brl IS NOT NULL
       THEN round(v.custo_adequacao_painel_existente_referencial_brl+pir.custo_painel_novo_atual_brl-e.custo_total,2)
       ELSE NULL::numeric END AS diferenca_referencia_e_cadastro_brl,
  CASE
    WHEN pir.custo_painel_novo_atual_brl IS NULL THEN 'GAP_PRECO_CATALOGO_PIR'
    WHEN v.custo_adequacao_painel_existente_referencial_brl IS NULL THEN 'GAP_PRECO_OUTROS_COMPONENTES'
    WHEN e.custo_total IS NULL THEN 'GAP_CUSTO_CADASTRADO'
    WHEN abs(v.custo_adequacao_painel_existente_referencial_brl+pir.custo_painel_novo_atual_brl-e.custo_total)>0.01 THEN 'DIVERGENCIA_PRECO_REVISAR_EXC'
    ELSE 'CONSISTENTE_APENAS_ARITMETICAMENTE'
  END AS status_conciliacao,
  'PENDING_VALIDATION | EXC INATIVA | MON004 PAINEL PIR NOVO INCLUSO 1 PECA 1130X2650 | PERFIL M30 CANDIDATO | MO 2023 NAO HOMOLOGADA | NAO SOMAR AUTOMATICAMENTE AO M05'::text AS gate_de_uso,
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
  (SELECT lm.valor_unitario FROM public.lista_mae lm WHERE lm.cod_item='PEND-GUIA-U-001' AND lm.ativo IS TRUE) AS preco_guia_u_alternativa_nao_homologada_brl_m,
  m.memoria_calculo->'demonstrativo_individual_v2' AS memoria_calculo_individual,
  m.memoria_calculo#>>'{demonstrativo_individual_v2,identificacao,codigo_excedente}' AS codigo_exc_na_memoria_individual,
  (m.memoria_calculo#>>'{demonstrativo_individual_v2,custo_unitario_cadastrado_brl}')::numeric AS valor_unitario_da_memoria_individual_brl,
  m.memoria_calculo#>>'{demonstrativo_individual_v2,formula_total_custo}' AS formula_total_memoria_individual,
  v.custo_adequacao_painel_existente_referencial_brl AS custo_adequacao_sem_painel_novo_referencial_brl,
  pir.cod_item_painel AS cod_item_painel_pir_novo,
  pir.area_painel_m2 AS quantidade_painel_pir_novo_m2,
  pir.preco_painel_atual_m2 AS preco_painel_pir_lista_mae_atual_brl_m2,
  pir.custo_painel_novo_atual_brl AS custo_painel_pir_lista_mae_atual_brl,
  '1 PAINEL PIR NOVO MON004 1130X2650 POR CONJUNTO; EQUIVALENCIA COM STUC HISTORICO PENDENTE'::text AS escopo_painel
FROM public.excedentes e
LEFT JOIN LATERAL (
  SELECT i.cod_item AS cod_item_painel, i.quantidade AS area_painel_m2,
    i.valor_parcial AS custo_painel_novo_cadastrado_brl,
    lm.valor_unitario AS preco_painel_atual_m2,
    round(i.quantidade*lm.valor_unitario,2) AS custo_painel_novo_atual_brl
  FROM public.excedente_itens i
  LEFT JOIN public.lista_mae lm ON lm.cod_item=i.cod_item AND lm.ativo IS TRUE
  WHERE i.excedente_id=e.id AND i.cod_item='MON004' AND i.tipo_componente='MATERIAL'
  ORDER BY i.sequencia
  LIMIT 1
) pir ON true
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
'EXC042 painel PIR novo MON004 1130x2650 2,9945m² + basculante 600; EXC043 mesmo PIR + basculante 800. Custos completos R$769,12 / R$879,42 com abertura e MO historicos, perfil M30 sob validacao; memoria individual v2 1:1 preserva v1 antigo; EXCs inativas e sem aplicacao M05.';
REVOKE ALL ON public.vw_elo_orcar_exc_painel_pir_basculantes FROM PUBLIC, anon, authenticated;
GRANT SELECT ON public.vw_elo_orcar_exc_painel_pir_basculantes TO service_role;
-- Validar SELECT codigo_excedente, ativo, custo_painel_pir_novo_brl,
-- custo_adequacao_sem_painel_novo_referencial_brl, custo_excedente_cadastrado_brl,
-- custo_referencial_dinamico_brl, custo_total_com_painel_novo_brl,
-- memoria_calculo_id, valor_unitario_da_memoria_individual_brl, status_conciliacao
-- FROM public.vw_elo_orcar_exc_painel_pir_basculantes ORDER BY largura_mm;
