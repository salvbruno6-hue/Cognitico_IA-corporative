-- SO 233.26 / QA01 / ELO ORCAR. Vista contextual, NAO catalogo de EXC e NAO regra Core.
-- FONTE: public.elo_orcamento_calculos_aprendidos, learning_id SO23326-PIR-BASC-800-600-20261113.
-- Precos da bascula e do perfil consultados ao vivo na Lista-Mae. Abertura e M.O. sao valores de 2023.
-- O painel PIR 40mm existente NAO possui custo comprovado; painel novo nao e precificado.
-- Riscos: o perfil M30 ainda NAO tem equivalencia tecnica comprovada com o U da memoria.
-- Apenas 2 variantes: 600x600 e 800x800. Sem aplicacao automatica ao M05.
CREATE OR REPLACE VIEW public.vw_elo_orcar_painel_pir_basculantes
WITH (security_invoker = true)
AS
WITH variantes (largura_mm, altura_mm, cod_item_basculante, chave_memoria) AS (
  VALUES
    (600, 600, 'ESQ006'::text, 'atual_600'::text),
    (800, 800, 'ESQ007'::text, 'atual_800'::text)
),
referencias AS (
  SELECT
    c.id AS memoria_calculo_id,
    c.learning_id,
    c.origem_so,
    c.status AS status_validacao_calculo,
    v.largura_mm,
    v.altura_mm,
    v.cod_item_basculante,
    b.descricao_oficial AS basculante_descricao,
    b.valor_unitario AS preco_basculante_lista_mae_brl,
    b.un AS basculante_unidade,
    'M30'::text AS cod_item_perfil_u_candidato,
    u.descricao_oficial AS perfil_u_descricao_candidato,
    u.valor_unitario AS preco_perfil_u_lista_mae_brl_m,
    u.un AS perfil_u_unidade,
    (c.subcalculo -> v.chave_memoria ->> 'abertura_historica_brl')::numeric AS custo_abertura_un_2023_brl,
    (c.subcalculo -> v.chave_memoria ->> 'mo_historica_brl')::numeric AS custo_mo_rateada_un_2023_brl,
    (c.subcalculo -> 'historico_800' ->> 'total_brl')::numeric AS total_historico_800_2023_brl,
    (c.subcalculo -> 'historico_800' ->> 'esquadria_brl')::numeric AS preco_basculante_800_2023_brl
  FROM public.elo_orcamento_calculos_aprendidos c
  CROSS JOIN variantes v
  LEFT JOIN public.lista_mae b ON b.cod_item = v.cod_item_basculante AND b.ativo IS TRUE
  LEFT JOIN public.lista_mae u ON u.cod_item = 'M30' AND u.ativo IS TRUE
  WHERE c.learning_id = 'SO23326-PIR-BASC-800-600-20261113'
    AND c.origem_so = 'SO 233.26'
),
base AS (
  SELECT
    r.*,
    round((r.largura_mm::numeric * r.altura_mm::numeric) / 1000000, 4) AS area_abertura_m2,
    round((2 * (r.largura_mm + r.altura_mm))::numeric / 1000, 3) AS perimetro_perfil_u_m,
    CASE
      WHEN r.basculante_unidade = 'PÇ' AND lower(r.perfil_u_unidade) = 'm'
       AND r.preco_basculante_lista_mae_brl IS NOT NULL
       AND r.preco_perfil_u_lista_mae_brl_m IS NOT NULL
      THEN 'ITENS_CATALOGADOS_IDENTIFICADOS'::text
      ELSE 'GAP_CATALOGO_OU_UNIDADE'::text
    END AS validacao_itens_catalogo
  FROM referencias r
)
SELECT
  origem_so,
  memoria_calculo_id,
  learning_id,
  'PIR-BASC-' || largura_mm::text || 'X' || altura_mm::text AS configuracao,
  'PAINEL PIR 40MM EXISTENTE COM BASCULANTE ' || largura_mm::text || 'X' || altura_mm::text || 'MM' AS descricao,
  'CONJUNTO'::text AS unidade,
  1::integer AS quantidade_painel_pir_existente,
  40::integer AS espessura_painel_pir_mm,
  largura_mm,
  altura_mm,
  area_abertura_m2,
  perimetro_perfil_u_m,
  cod_item_basculante,
  basculante_descricao,
  preco_basculante_lista_mae_brl,
  cod_item_perfil_u_candidato,
  perfil_u_descricao_candidato,
  preco_perfil_u_lista_mae_brl_m,
  CASE WHEN validacao_itens_catalogo = 'ITENS_CATALOGADOS_IDENTIFICADOS'
    THEN round(perimetro_perfil_u_m * preco_perfil_u_lista_mae_brl_m, 2)
    ELSE NULL::numeric END AS custo_perfil_u_referencial_brl,
  custo_abertura_un_2023_brl AS custo_abertura_historico_brl,
  custo_mo_rateada_un_2023_brl AS custo_mo_historica_brl,
  CASE WHEN validacao_itens_catalogo = 'ITENS_CATALOGADOS_IDENTIFICADOS'
        AND custo_abertura_un_2023_brl IS NOT NULL
        AND custo_mo_rateada_un_2023_brl IS NOT NULL
    THEN round(preco_basculante_lista_mae_brl
       + perimetro_perfil_u_m * preco_perfil_u_lista_mae_brl_m
       + custo_abertura_un_2023_brl
       + custo_mo_rateada_un_2023_brl, 2)
    ELSE NULL::numeric END AS custo_adequacao_painel_existente_referencial_brl,
  CASE WHEN largura_mm = 800 THEN preco_basculante_800_2023_brl ELSE NULL::numeric END AS preco_basculante_historico_2023_brl,
  CASE WHEN largura_mm = 800 THEN total_historico_800_2023_brl ELSE NULL::numeric END AS custo_conjunto_historico_2023_brl,
  NULL::numeric AS custo_painel_pir_novo_brl,
  NULL::numeric AS custo_total_com_painel_novo_brl,
  false AS painel_pir_novo_incluso,
  'PAINEL EXISTENTE; CUSTO DE PAINEL NOVO NAO COMPROVADO'::text AS condicao_painel,
  'PENDENTE_EQUIVALENCIA_TECNICA_PERFIL_M30_U_HISTORICO'::text AS status_equivalencia_perfil,
  'ABERTURA_E_MAO_DE_OBRA_REFERENCIAS_2023_SEM_VALIDACAO_ATUAL'::text AS status_servicos,
  validacao_itens_catalogo,
  status_validacao_calculo,
  false AS aplicar_automaticamente_no_m05,
  'PRECO DE BASCULANTE E U: LISTA-MAE ATUAL; ABERTURA E MO: MEMORIA DE 24/10/2023. NAO SOMAR EM M05 SEM CONCILIAR +2 ESQ006 E RH.'::text AS ressalva_aplicacao
FROM base;

COMMENT ON VIEW public.vw_elo_orcar_painel_pir_basculantes IS
'VIEW contextual ELO ORCAR SO233.26 QA01: 2 dimensoes, PIR 40mm EXISTENTE e custo de adequacao referencial. Basculante ESQ006/ESQ007 e M30 consultados na Lista-Mae dinamicamente; abertura e MO sao memoria 2023. PIR novo, equivalencia de perfil e instalacao do M05 NAO homologados; sem insercao automatica em EXC.';

REVOKE ALL ON public.vw_elo_orcar_painel_pir_basculantes FROM PUBLIC, anon, authenticated;
GRANT SELECT ON public.vw_elo_orcar_painel_pir_basculantes TO service_role;

-- Testes de regressao apos aplicar:
-- SELECT configuracao, area_abertura_m2, perimetro_perfil_u_m,
--        custo_adequacao_painel_existente_referencial_brl, custo_painel_pir_novo_brl,
--        status_validacao_calculo
-- FROM public.vw_elo_orcar_painel_pir_basculantes ORDER BY largura_mm;
-- Esperado nos precos atuais: 600x600 => 0,3600m2, 2,400m, R$277,66;
--                            800x800 => 0,6400m2, 3,200m, R$387,96.
-- Verificar security_invoker e ausencia de permissao publica/autenticada.
