-- SO 233.26 / ELO ORCAR / QA01 e L11.
-- CANONE: duas composicoes EXC (600/800 mm), memorias individuais e VIEW de auditoria.
-- LEARNING: elo_orcamento_calculos_aprendidos.learning_id='SO23326-PIR-BASC-800-600-20261113'
-- NAO trocar a fonte historica de 2023 por validacao de produtividade ou por preco homologado.
-- Os novos EXCs permanecem INATIVOS (ativo=false) ate validacao tecnica e governance.
-- Os preços de referência de ESQ006/ESQ007/M30 são extraídos da Lista-Mãe vigente na inserção.
-- O perfil M30 (40x42x40) e um CANDIDATO ao perfil U da memoria antiga.
-- O custo de painel PIR 40 mm novo nao foi fornecido: NULL / NAO INCLUSO, sem assumir gratis.
DO $exc_pir$
DECLARE
  r record;
  v_mem_id bigint;
  v_exc_id uuid;
  v_calc_id bigint;
  v_unit_esq numeric;
  v_unit_u numeric;
  v_total numeric;
  v_evidence text := 'PRODUCAO INTERNA/MRC MULTITEINER, BRUNO E SAMUEL, PAINEL BASCULANTE 800X800, 24/10/2023; QA01 SO 233.26';
BEGIN
  SELECT id INTO v_calc_id
  FROM public.elo_orcamento_calculos_aprendidos
  WHERE learning_id='SO23326-PIR-BASC-800-600-20261113'
    AND origem_so='SO 233.26'
    AND status='PENDING_VALIDATION';
  IF v_calc_id IS NULL THEN
    RAISE EXCEPTION 'Calculo observado QA01 da SO 233.26 nao existe; nao criar EXC orfa';
  END IF;

  FOR r IN
    SELECT * FROM (VALUES
      ('EXC-042'::text, 600::int, 'ESQ006'::text, 'atual_600'::text, 2.40::numeric),
      ('EXC-043'::text, 800::int, 'ESQ007'::text, 'atual_800'::text, 3.20::numeric)
    ) AS x(codigo,lado_mm,cod_basculante,chave_calculo,perimetro_m)
  LOOP
    SELECT lm.valor_unitario INTO v_unit_esq
    FROM public.lista_mae lm WHERE lm.cod_item=r.cod_basculante AND lm.ativo IS TRUE;
    SELECT lm.valor_unitario INTO v_unit_u
    FROM public.lista_mae lm WHERE lm.cod_item='M30' AND lm.ativo IS TRUE;
    IF v_unit_esq IS NULL OR v_unit_u IS NULL THEN
      RAISE EXCEPTION 'Catalogo sem preco vigente para % ou M30',r.cod_basculante;
    END IF;
    v_total := round(v_unit_esq + r.perimetro_m*v_unit_u + 25.59 + 51.17,2);

    SELECT e.id INTO v_exc_id
    FROM public.excedentes e WHERE e.codigo_excedente=r.codigo;
    IF v_exc_id IS NOT NULL THEN
      IF NOT EXISTS (
        SELECT 1 FROM public.excedentes e
        WHERE e.id=v_exc_id AND e.ativo IS FALSE
          AND e.memoria_calculo_id IS NOT NULL
          AND e.origem LIKE 'SO 233.26 | QA01%'
      ) THEN
        RAISE EXCEPTION 'Codigo % ja usado com outra autoridade ou ativado: investigar, nao sobrescrever',r.codigo;
      END IF;
      CONTINUE; -- Idempotencia sem atualizar retroativamente valores ou parcelas historicas.
    END IF;

    SELECT m.id INTO v_mem_id
    FROM public.elo_orcamento_memoria m
    WHERE m.conceito_key='so23326_pir_basculante_'||r.lado_mm::text||'_exc'
      AND m.origem_so='SO 233.26';
    IF v_mem_id IS NULL THEN
      INSERT INTO public.elo_orcamento_memoria
      (id,orcamento_id,tipo_memoria,aplicacao,necessidade,contexto,
       memoria_calculo,evidencias,resultado,valor_aprendizado,confianca,
       origem_so,origem_documento,classificacao,conceito_key,titulo_conceito,
       conceito,tipo_conhecimento,decisao_governanca,status_conceito)
      VALUES
      (nextval('public.elo_orcamento_memoria_id_seq'),'SO 233.26','CALCULO',
       'EXC em painel PIR existente: basculante '||r.lado_mm||'x'||r.lado_mm||' mm',
       'Registrar a composicao historica de abertura, perfil, basculante e instalacao, sem supor custo de painel novo ou duplicar a equipe M05.',
       'QA01 — experiencia ELO APRENDER observada; EXC ainda inativa',
       jsonb_build_object(
         'unidade','UN','codigo_excedente',r.codigo,
         'basculante_codigo',r.cod_basculante,'lado_m',r.lado_mm::numeric/1000,
         'area_m2',round((r.lado_mm::numeric/1000)^2,4),
         'perimetro_perfil_u_m',r.perimetro_m,
         'custo_basculante_lista_mae_snapshot_brl',v_unit_esq,
         'perfil_u_codigo_candidato','M30',
         'custo_perfil_u_m_lista_mae_snapshot_brl',v_unit_u,
         'custo_perfil_u_snapshot_brl',round(r.perimetro_m*v_unit_u,2),
         'abertura_historica_por_un_brl',25.59,
         'mao_obra_historica_por_un_brl',51.17,
         'profissional_dia_historico_brl',275.82,
         'ajudante_dia_historico_brl',235.92,
         'tempo_rateado_cada_profissional_dia',0.10,
         'formula_mo_historica','(275.82+235.92)/10=51.174, arredondado 51.17; produtividade nao comprovada',
         'formula_total','basculante + (perimetro_m x preco_U_m) + abertura_historica + MO_historica',
         'custo_referencial_snapshot_sem_pir_novo_brl',v_total,
         'custo_painel_pir_novo_brl',NULL,
         'painel_pir_novo_incluso',false,
         'perfil_M30_equivalencia_validada',false,
         'abertura_e_produtividade_atualizadas',false,
         'calculo_aprendido_origem_id',v_calc_id,
         'calculo_aprendido_learning_id','SO23326-PIR-BASC-800-600-20261113',
         'caso_M05','Nao somar automaticamente: M05 ja possui +2 ESQ006 600x600 e RH agregada.',
         'status','PENDING_VALIDATION'),
       jsonb_build_object(
         'origem_2023',v_evidence,
         'catalogo','lista_mae ESQ006/ESQ007/M30, consultada em 13/11/2026',
         'calculo_aprendido_id',v_calc_id,
         'cod_excedente_proposto',r.codigo,
         'limitacoes',jsonb_build_array(
           'Memoria original 2023 descreve 800x800; a variante 600x600 e simulacao parametrica.',
           'Perfil M30 e candidato, sem equivalencia provada com o perfil U de 2023.',
           'Preco de painel PIR novo nao informado; base existente sem novo custo.',
           'Abertura e mao de obra de 2023 nao foram revalidadas para 2026.',
           'Nao aplicar automaticamente no M05, que ja possui ESQ006 em materiais.')),
       'Composicao EXC preliminar/inativa, custo de adequacao do painel PIR existente: R$'||to_char(v_total,'FM999999990.00')||'/UN; painel PIR novo pendente.',
       0,0.25,'SO 233.26',v_evidence,'LEARNING_CANDIDATE',
       'so23326_pir_basculante_'||r.lado_mm::text||'_exc',
       'EXC painel PIR 40 mm com basculante '||r.lado_mm||'x'||r.lado_mm,
       'Adequacao do vao em painel PIR existente: basculante, abertura, perfil U e fixacao historica.',
       'EXPERIENCIA_CONTEXTUAL',
       'PENDENTE OWNER E EVOLUTION GATE; EXC INATIVA, REFERENCIA DE CUSTO NAO HOMOLOGADA, NAO REAPLICAR EM M05.',
       'PENDENTE_VALIDACAO'
      )
      RETURNING id INTO v_mem_id;
    END IF;

    INSERT INTO public.excedentes
    (codigo_excedente,tipo_instalacao,descricao,unidade,custo_total,
     inclui_mao_obra,origem,observacao,ativo,possui_mao_obra_detalhada,
     valor_total,memoria_calculo_id)
    VALUES
    (r.codigo,'ADEQUACAO_PAINEL_PIR',
     'Painel PIR 40mm EXISTENTE — abertura e fixacao de basculante '||r.lado_mm||'x'||r.lado_mm||' mm',
     'UN',NULL,true,
     'SO 233.26 | QA01 | referencia de producao interna de 24/10/2023',
     'EXC INATIVA/PENDING_VALIDATION; adequacao sobre PIR existente. Composicao de material, abertura e MO rateada historica. PERFIL U M30 apenas candidato. Painel PIR NOVO NAO INCLUIDO; M05 ja possui duas ESQ006 extras. Calculo aprendido '||v_calc_id::text||'.',
     false,true,NULL,v_mem_id)
    RETURNING id INTO v_exc_id;

    -- Item 1: componente de serie ESQ006/ESQ007; o trigger cadastral recupera cod_produt e o preco.
    INSERT INTO public.excedente_itens
    (excedente_id,cod_excedente,sequencia,cod_item,descricao,unidade,quantidade,
     valor_unitario,valor_parcial,valor_total,tipo_componente,observacao)
    VALUES
    (v_exc_id,r.codigo,1,r.cod_basculante,
     'Basculante de aluminio '||r.lado_mm||'x'||r.lado_mm||' mm',
     'PÇ',1,v_unit_esq,v_unit_esq,v_unit_esq,'MATERIAL',
     'Preco da Lista-Mae na data do cadastro. Revisar se preco se alterar; nao confundir 800mm ESQ007 com 600mm ESQ006.');

    -- Item 2: perfil U de acabamento pelo perimetro, com equivalencia geometrica condicionada.
    INSERT INTO public.excedente_itens
    (excedente_id,cod_excedente,sequencia,cod_item,descricao,unidade,quantidade,
     valor_unitario,valor_parcial,valor_total,tipo_componente,observacao)
    VALUES
    (v_exc_id,r.codigo,2,'M30','Perfil U de contorno de basculante — candidato M30','m',
     r.perimetro_m,v_unit_u,round(r.perimetro_m*v_unit_u,2),
     round(r.perimetro_m*v_unit_u,2),'MATERIAL',
     'Perfil de catalogo M30 40x42x40mm e CANDIDATO ao U historico; seccao real/fixacao a validar. Comprimento =4x lado.');

    -- Item 3: custo historico de abertura de vao por UN, sem equivalencia automatica ao EXC-016 aco.
    INSERT INTO public.excedente_itens
    (excedente_id,cod_excedente,sequencia,descricao,unidade,quantidade,
     valor_unitario,valor_parcial,valor_total,tipo_componente,observacao)
    VALUES
    (v_exc_id,r.codigo,3,'Abertura do vao em PAINEL PIR 40mm — memoria 2023','UN',1,
     25.59,25.59,25.59,'SERVICO',
     'R$25,59/UN na memoria 2023; custo e produtividade nao revalidados. Diferente de corte em aco EXC-016.');

    -- Item 4: painel base preexistente, sem criar custo ficticio zero de painel novo.
    INSERT INTO public.excedente_itens
    (excedente_id,cod_excedente,sequencia,descricao,unidade,quantidade,
     valor_unitario,valor_parcial,valor_total,tipo_componente,observacao)
    VALUES
    (v_exc_id,r.codigo,4,'PAINEL PIR 40mm EXISTENTE — elemento de base, nao fornecido','UN',1,
     NULL,NULL,NULL,'REFERENCIA_NAO_FATURAVEL',
     'Linha informativa: memoria 2023 mostra painel STUC PIR40mm com parcial 0. Custo de painel novo DESCONHECIDO, NAO INCLUSO e NAO HOMOLOGADO.');

    -- A fonte 2023 traz RH de uma dupla por dia, apropriada em 1/10 de dia por painel.
    -- 0,10 x 275,82 = 27,58; 0,10 x 235,92 = 23,59. Soma = 51,17.
    INSERT INTO public.excedente_mao_obra
    (excedente_id,sequencia,funcao,quantidade,tempo,unidade_tempo,
     valor_unitario,valor_parcial,valor_total,observacao)
    VALUES
    (v_exc_id,1,'Profissional',1,0.10,'DIA',275.82,27.58,275.82,
     'Valor DIA historico 2023, rateado por 10; produtividade de 10 un/dia NAO comprovada. Potencial sobreposicao com equipe M05.'),
    (v_exc_id,2,'Ajudante',1,0.10,'DIA',235.92,23.59,235.92,
     'Valor DIA historico 2023, rateado por 10; produtividade de 10 un/dia NAO comprovada. Potencial sobreposicao com equipe M05.');
  END LOOP;
END;
$exc_pir$;

-- VIEW composta: a EXC e a autoridade da composicao, a memoria e a origem de formula,
-- e a VIEW de QA01 original e o referencial dinamico de catalogo. Nenhuma duplicacao do Core.
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
  'PENDING_VALIDATION | EXC INATIVA | PIR NOVO EXCLUIDO | PERFIL M30 CANDIDATO | MO 2023 NAO HOMOLOGADA | NAO SOMAR AUTOMATICAMENTE AO M05'::text AS gate_de_uso
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
WHERE e.codigo_excedente IN ('EXC-042','EXC-043')
 AND e.origem LIKE 'SO 233.26 | QA01%';

COMMENT ON VIEW public.vw_elo_orcar_exc_painel_pir_basculantes IS
'SO 233.26: EXC-042 painel PIR existente + basculante 600, EXC-043 painel PIR existente + basculante 800. Composicao, materiais, MO historica, memoria governada e comparacao dinamica Lista-Mae. EXC inativas; custo PIR novo desconhecido; sem uso automatico.';

REVOKE ALL ON public.vw_elo_orcar_exc_painel_pir_basculantes FROM PUBLIC, anon, authenticated;
GRANT SELECT ON public.vw_elo_orcar_exc_painel_pir_basculantes TO service_role;

-- Testes apos apply_migration (nao executar automaticamente em transacoes de producao):
-- SELECT codigo_excedente,configuracao,ativo,memoria_calculo_id,
--   custo_materiais_servicos_cadastrado_brl,custo_mao_obra_cadastrada_brl,
--   custo_excedente_cadastrado_brl,custo_referencial_dinamico_brl,status_conciliacao
-- FROM public.vw_elo_orcar_exc_painel_pir_basculantes ORDER BY largura_mm;
-- Esperado: EXC-042: 226,49 + 51,17 = 277,66; EXC-043: 336,79 + 51,17 = 387,96.
-- Sempre verificar contagem 4 itens (1 PIR apenas referencia) +2 funcoes de MO por EXC.
-- A migração nao deve alterar itens I02-M05, valor-base M05 nem Lista-Mae.
