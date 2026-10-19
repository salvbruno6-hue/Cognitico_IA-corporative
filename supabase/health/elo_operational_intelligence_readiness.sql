-- ELO operational-intelligence readiness probe
-- Read-only. Measures whether the operational evidence chain needed for PCP
-- learning exists. It does not create plans, capacity, stock, units, events or
-- learning records and does not infer missing facts.

SELECT
  'OPERATIONAL_INTELLIGENCE_READINESS'::text AS finding,
  'public'::text AS schema_name,
  'mt_* + elo_aprendizado_*'::text AS object_name,
  (SELECT count(*) FROM public.mt_demanda_historico)::bigint AS demand_history_rows,
  (SELECT count(*) FROM public.mt_previsoes_demanda)::bigint AS demand_forecast_rows,
  (SELECT count(*) FROM public.mt_regras_capacidade)::bigint AS capacity_rule_rows,
  (SELECT count(*) FROM public.mt_capacidade_diaria)::bigint AS capacity_daily_rows,
  (SELECT count(*) FROM public.mt_capacidade_componentes)::bigint AS capacity_component_rows,
  (SELECT count(*) FROM public.mt_necessidades_materiais)::bigint AS material_need_rows,
  (SELECT count(*) FROM public.mt_lotes_estoque)::bigint AS material_stock_rows,
  (SELECT count(*) FROM public.mt_planos_pcp)::bigint AS plan_rows,
  (SELECT count(*) FROM public.mt_linhas_plano_pcp)::bigint AS plan_line_rows,
  (SELECT count(*) FROM public.mt_ordens_producao)::bigint AS production_order_rows,
  (SELECT count(*) FROM public.mt_operacoes_ordem_producao)::bigint AS production_operation_rows,
  (SELECT count(*) FROM public.mt_eventos_fluxo_modular)::bigint AS flow_event_rows,
  (SELECT count(*) FROM public.mt_unidades_modulares)::bigint AS modular_unit_rows,
  (SELECT count(*) FROM public.elo_aprendizado_pcp_planejamento)::bigint AS learning_pcp_rows,
  (SELECT count(*) FROM public.elo_aprendizado_producao_fluxo_modular)::bigint AS learning_flow_rows;
