-- EXC-023 / SPDA: versao aprovada pelo usuario em 2026-11-11.
-- Registro persistente: public.tb_elo_eventos_governanca id=6.
-- Aprovacao de apresentacao; nao constitui validacao dos coeficientes.
-- Historico SO 169.26 (memoria 56) e ramificacao SO-230/2026 (153/154).
CREATE OR REPLACE VIEW public.vw_exc023_memoria_escavacao_reaterro AS
SELECT 'EXC-023'::text AS codigo_excedente,
 CASE WHEN m.id=153 THEN 'CIV-ESC-001' ELSE 'CIV-REA-001' END AS codigo_lista_mae,
 CASE WHEN m.id=153 THEN 'ESCAVACAO_MANUAL' ELSE 'REATERRO_COMPACTACAO' END AS servico,
 m.id AS memoria_id,m.origem_so,m.aplicacao,m.memoria_calculo,m.evidencias,m.resultado,
 m.status_conceito,m.decisao_governanca,lm.descricao_oficial,
 lm.valor_unitario AS preco_unitario_lista_mae,lm.un AS unidade_lista_mae,
 (m.memoria_calculo->>'custo_ajudante_brl_hh')::numeric AS custo_hh_reaterro,
 CASE WHEN m.id=153 THEN (m.memoria_calculo->>'custo_hh_brl')::numeric ELSE (m.memoria_calculo->>'custo_ajudante_brl_hh')::numeric END AS custo_hh,
 CASE WHEN m.id=153 THEN (m.memoria_calculo->>'coeficiente_hh_m3')::numeric ELSE (m.memoria_calculo->>'coeficiente_hh_m3_inferido_do_preco')::numeric END AS coeficiente_hh_m3,
 CASE WHEN m.id=153 THEN (m.memoria_calculo->>'volume_m3')::numeric ELSE (m.memoria_calculo->>'volume_reaterro_orcamento_m3')::numeric END AS volume_projeto_m3,
 CASE WHEN m.id=153 THEN (m.memoria_calculo->>'total_planilha_brl')::numeric ELSE (m.memoria_calculo->>'total_orcamentario_brl')::numeric END AS total_projeto_brl
FROM public.elo_orcamento_memoria m
JOIN public.lista_mae lm ON lm.cod_item=CASE WHEN m.id=153 THEN 'CIV-ESC-001' ELSE 'CIV-REA-001' END
WHERE m.id IN (153,154) AND
 ((m.id=153 AND m.evidencias->>'excedente_id'=(SELECT id::text FROM public.excedentes WHERE codigo_excedente='EXC-023'))
 OR (m.id=154 AND m.evidencias->>'memoria_escavacao_relacionada_id'='153'));

CREATE OR REPLACE VIEW public.vw_exc023_spda_composicao_integral AS
SELECT v.*,
 'public.vw_exc023_memoria_escavacao_reaterro'::text AS view_memoria_civil,
 (SELECT jsonb_agg(to_jsonb(m) ORDER BY m.memoria_id) FROM public.vw_exc023_memoria_escavacao_reaterro m WHERE m.codigo_excedente=v.codigo_excedente) AS memorias_civis_detalhadas,
 EXISTS(SELECT 1 FROM public.excedente_itens i WHERE i.excedente_id=(SELECT id FROM public.excedentes WHERE codigo_excedente=v.codigo_excedente) AND i.cod_item='CIV-REA-001') AS reaterro_incorporado,
 'GAP: quantitativos de SO 169.26 e SO-230/2026 distintos; memória 56 contém custos anteriores; reaterro não incorporado'::text AS gap_consolidacao
FROM public.vw_excedentes_memoria_completa v WHERE v.codigo_excedente='EXC-023';

-- Verificacao: 11 itens materiais/servicos, 3 de apoio, 2 memorias civis.
-- SELECT codigo_excedente,valor_total,jsonb_array_length(memorias_civis_detalhadas)
-- FROM public.vw_exc023_spda_composicao_integral;
