-- PCP: fator de demanda, aplicação à demanda humana histórica externa e gatilho do loop ELO.
CREATE OR REPLACE VIEW public.v_elo_pcp_referencia_demanda_comparavel
WITH (security_invoker = true)
AS
WITH parametros AS (
  SELECT DATE '2025-09-01' historico_inicio, DATE '2026-02-28' historico_fim,
         DATE '2026-09-01' previsao_inicio, DATE '2027-02-28' previsao_fim
), historico AS (
  SELECT dh.tenant_id,dh.modelo_id,dh.natureza_demanda,dh.chave_comparabilidade,SUM(dh.quantidade_real) quantidade_historica
  FROM public.mt_demanda_historico dh CROSS JOIN parametros p
  WHERE dh.modelo_id IS NOT NULL AND dh.periodo_inicio>=p.historico_inicio AND dh.periodo_fim<=p.historico_fim
    AND dh.quantidade_real IS NOT NULL AND dh.quantidade_real>=0
  GROUP BY dh.tenant_id,dh.modelo_id,dh.natureza_demanda,dh.chave_comparabilidade
), previsao AS (
  SELECT pd.tenant_id,pd.modelo_id,pd.natureza_demanda,pd.chave_comparabilidade,SUM(pd.quantidade_prevista) quantidade_prevista
  FROM public.mt_previsoes_demanda pd CROSS JOIN parametros p
  WHERE pd.modelo_id IS NOT NULL AND pd.periodo_inicio>=p.previsao_inicio AND pd.periodo_fim<=p.previsao_fim
    AND pd.quantidade_prevista IS NOT NULL AND pd.quantidade_prevista>=0
  GROUP BY pd.tenant_id,pd.modelo_id,pd.natureza_demanda,pd.chave_comparabilidade
), comparavel AS (
  SELECT COALESCE(h.tenant_id,p.tenant_id) tenant_id,COALESCE(h.modelo_id,p.modelo_id) modelo_id,
         COALESCE(h.natureza_demanda,p.natureza_demanda) natureza_demanda,
         COALESCE(h.chave_comparabilidade,p.chave_comparabilidade) chave_comparabilidade,
         h.quantidade_historica,p.quantidade_prevista,
         CASE
           WHEN COALESCE(h.natureza_demanda,p.natureza_demanda) IS NULL THEN 'SEM_NATUREZA'
           WHEN upper(COALESCE(h.natureza_demanda,p.natureza_demanda)) IN ('EVENTO','SPOT')
                AND COALESCE(h.chave_comparabilidade,p.chave_comparabilidade) IS NULL THEN 'SEM_CHAVE_COMPARABILIDADE'
           WHEN h.modelo_id IS NULL THEN 'SEM_HISTORICO'
           WHEN p.modelo_id IS NULL THEN 'SEM_PREVISAO'
           ELSE 'COMPARAVEL_POTENCIAL'
         END estado_comparabilidade
  FROM historico h FULL OUTER JOIN previsao p
    ON p.tenant_id=h.tenant_id AND p.modelo_id=h.modelo_id
   AND p.natureza_demanda IS NOT DISTINCT FROM h.natureza_demanda
   AND (p.chave_comparabilidade=h.chave_comparabilidade OR
        (p.chave_comparabilidade IS NULL AND h.chave_comparabilidade IS NULL
         AND upper(COALESCE(p.natureza_demanda,h.natureza_demanda)) NOT IN ('EVENTO','SPOT')))
)
SELECT c.tenant_id,c.modelo_id,m.codigo modelo_codigo,m.nome modelo_nome,m.familia modelo_familia,
       t.id taxonomia_id,t.codigo taxonomia_codigo,t.familia taxonomia_familia,t.tipo taxonomia_tipo,
       c.natureza_demanda,c.chave_comparabilidade,
       DATE '2025-09-01' historico_periodo_inicio,DATE '2026-02-28' historico_periodo_fim,c.quantidade_historica,
       DATE '2026-09-01' previsao_periodo_inicio,DATE '2027-02-28' previsao_periodo_fim,c.quantidade_prevista,
       c.estado_comparabilidade,
       CASE WHEN c.estado_comparabilidade='COMPARAVEL_POTENCIAL' AND c.quantidade_historica>0 AND c.quantidade_prevista IS NOT NULL
            THEN c.quantidade_prevista/c.quantidade_historica END fator_demanda,
       CASE WHEN c.estado_comparabilidade='COMPARAVEL_POTENCIAL' AND c.quantidade_historica>0 AND c.quantidade_prevista IS NOT NULL
            THEN ((c.quantidade_prevista/c.quantidade_historica)-1)*100 END variacao_percentual,
       CASE WHEN c.estado_comparabilidade<>'COMPARAVEL_POTENCIAL' THEN c.estado_comparabilidade
            WHEN c.quantidade_historica IS NULL THEN 'SEM_HISTORICO'
            WHEN c.quantidade_historica=0 THEN 'HISTORICO_ZERO'
            WHEN c.quantidade_prevista IS NULL THEN 'SEM_PREVISAO'
            ELSE 'FATOR_CALCULADO' END estado_fator
FROM comparavel c JOIN public.modelos m ON m.id=c.modelo_id LEFT JOIN public.taxonomia t ON t.id=m.taxonomia_id;
ALTER VIEW public.v_elo_pcp_referencia_demanda_comparavel SET (security_invoker=true);
COMMENT ON VIEW public.v_elo_pcp_referencia_demanda_comparavel IS
'Referencia comparavel Sep/2025-Feb/2026 versus Sep/2026-Feb/2027. Fator = demanda futura comparavel / demanda historica comparavel. Nao aplica fator ao quadro de RH.';

CREATE OR REPLACE VIEW public.v_elo_pcp_demanda_humana_historica_externa
WITH (security_invoker=true)
AS
WITH ordem_modelo AS (
  SELECT o.id ordem_montagem_externa_id,o.tenant_id,o.pedido_venda_id,COUNT(DISTINCT i.modelo_id) qtd_modelos_distintos,
         (ARRAY_AGG(DISTINCT i.modelo_id ORDER BY i.modelo_id) FILTER (WHERE i.modelo_id IS NOT NULL))[1] modelo_id
  FROM public.mt_ordens_montagem_externa o JOIN public.mt_pedidos_venda_itens i ON i.pedido_venda_id=o.pedido_venda_id
  GROUP BY o.id,o.tenant_id,o.pedido_venda_id
), base AS (
  SELECT o.tenant_id,o.ordem_montagem_externa_id,o.modelo_id,pv.natureza_demanda,pv.chave_comparabilidade,
         e.pessoa_id,e.funcao_montagem_id,e.inicio_planejado,e.fim_planejado,COALESCE(e.horas_planejadas,0) horas_planejadas
  FROM ordem_modelo o JOIN public.mt_equipe_montagem_externa e ON e.ordem_montagem_externa_id=o.ordem_montagem_externa_id
  JOIN public.mt_pedidos_venda pv ON pv.id=o.pedido_venda_id
  WHERE o.qtd_modelos_distintos=1 AND e.inicio_planejado IS NOT NULL AND e.fim_planejado IS NOT NULL AND e.fim_planejado>=e.inicio_planejado
    AND e.inicio_planejado::date<=DATE '2026-02-28' AND e.fim_planejado::date>=DATE '2025-09-01'
    AND COALESCE(e.status,'PLANEJADO') NOT IN ('CANCELADO','CANCELADA') AND COALESCE(pv.status,'') NOT IN ('CANCELADO','CANCELADA')
), dias AS (
  SELECT b.tenant_id,b.ordem_montagem_externa_id,b.modelo_id,b.natureza_demanda,b.chave_comparabilidade,b.pessoa_id,b.funcao_montagem_id,
         d.data_referencia::date data_referencia,
         b.horas_planejadas/NULLIF(EXTRACT(EPOCH FROM(date_trunc('day',b.fim_planejado)-date_trunc('day',b.inicio_planejado)))/86400+1,0) horas_planejadas_dia
  FROM base b CROSS JOIN LATERAL generate_series(
    GREATEST(date_trunc('day',b.inicio_planejado),DATE '2025-09-01'::timestamp),
    LEAST(date_trunc('day',b.fim_planejado),DATE '2026-02-28'::timestamp),'1 day'::interval) d(data_referencia)
), diaria AS (
  SELECT tenant_id,modelo_id,natureza_demanda,chave_comparabilidade,funcao_montagem_id,data_referencia,
         COUNT(DISTINCT pessoa_id) demanda_colaboradores_dia,COUNT(DISTINCT ordem_montagem_externa_id) ordens_com_demanda_dia,SUM(horas_planejadas_dia) horas_demanda_dia
  FROM dias GROUP BY tenant_id,modelo_id,natureza_demanda,chave_comparabilidade,funcao_montagem_id,data_referencia
)
SELECT d.tenant_id,d.modelo_id,m.codigo modelo_codigo,m.nome modelo_nome,d.natureza_demanda,d.chave_comparabilidade,d.funcao_montagem_id,
       f.codigo funcao_codigo,f.nome funcao_nome,DATE '2025-09-01' historico_periodo_inicio,DATE '2026-02-28' historico_periodo_fim,
       AVG(d.demanda_colaboradores_dia)::numeric demanda_colaboradores_media_dia,MAX(d.demanda_colaboradores_dia) demanda_colaboradores_pico_dia,
       SUM(d.demanda_colaboradores_dia) colaboradores_dia_acumulados,SUM(d.horas_demanda_dia) horas_demanda_acumuladas,COUNT(*) dias_com_demanda
FROM diaria d JOIN public.modelos m ON m.id=d.modelo_id LEFT JOIN public.mt_funcoes_montagem f ON f.id=d.funcao_montagem_id
GROUP BY d.tenant_id,d.modelo_id,m.codigo,m.nome,d.natureza_demanda,d.chave_comparabilidade,d.funcao_montagem_id,f.codigo,f.nome;
ALTER VIEW public.v_elo_pcp_demanda_humana_historica_externa SET (security_invoker=true);
COMMENT ON VIEW public.v_elo_pcp_demanda_humana_historica_externa IS
'Demanda humana historica externa por modelo e funcao. So usa ordens cujo pedido possui exatamente um modelo; nao faz rateio inferido entre varios modelos.';

CREATE OR REPLACE VIEW public.v_elo_pcp_gap_composicao_humana_externa
WITH (security_invoker=true)
AS
SELECT o.tenant_id,o.id ordem_montagem_externa_id,o.pedido_venda_id,COUNT(DISTINCT i.modelo_id) qtd_modelos_distintos,
       ARRAY_AGG(DISTINCT i.modelo_id) FILTER (WHERE i.modelo_id IS NOT NULL) modelos_ids,'GAP_PEDIDO_MULTI_MODELO'::text estado_gap
FROM public.mt_ordens_montagem_externa o JOIN public.mt_pedidos_venda_itens i ON i.pedido_venda_id=o.pedido_venda_id
WHERE o.inicio_planejado::date<=DATE '2026-02-28' AND o.fim_planejado::date>=DATE '2025-09-01'
GROUP BY o.tenant_id,o.id,o.pedido_venda_id HAVING COUNT(DISTINCT i.modelo_id)>1;
ALTER VIEW public.v_elo_pcp_gap_composicao_humana_externa SET (security_invoker=true);

CREATE OR REPLACE VIEW public.v_elo_pcp_demanda_humana_projetada_externa
WITH (security_invoker=true)
AS
SELECT COALESCE(f.tenant_id,h.tenant_id) tenant_id,COALESCE(f.modelo_id,h.modelo_id) modelo_id,
       COALESCE(f.modelo_codigo,h.modelo_codigo) modelo_codigo,COALESCE(f.modelo_nome,h.modelo_nome) modelo_nome,f.taxonomia_tipo,
       COALESCE(f.natureza_demanda,h.natureza_demanda) natureza_demanda,COALESCE(f.chave_comparabilidade,h.chave_comparabilidade) chave_comparabilidade,
       h.funcao_montagem_id,h.funcao_codigo,h.funcao_nome,h.demanda_colaboradores_media_dia demanda_humana_historica_media_dia,
       f.quantidade_historica,f.quantidade_prevista,f.fator_demanda,f.variacao_percentual,
       CASE WHEN f.estado_fator='FATOR_CALCULADO' AND h.demanda_colaboradores_media_dia IS NOT NULL
            THEN h.demanda_colaboradores_media_dia*f.fator_demanda END demanda_humana_projetada_media_dia,
       CASE WHEN f.estado_fator IS NULL THEN 'SEM_REFERENCIA_DEMANDA'
            WHEN f.estado_fator<>'FATOR_CALCULADO' THEN f.estado_fator
            WHEN h.demanda_colaboradores_media_dia IS NULL THEN 'GAP_SEM_HISTORICO_HUMANO'
            ELSE 'DEMANDA_HUMANA_PROJETADA' END estado_projecao
FROM public.v_elo_pcp_referencia_demanda_comparavel f FULL OUTER JOIN public.v_elo_pcp_demanda_humana_historica_externa h
  ON h.tenant_id=f.tenant_id AND h.modelo_id=f.modelo_id AND h.natureza_demanda IS NOT DISTINCT FROM f.natureza_demanda
 AND h.chave_comparabilidade IS NOT DISTINCT FROM f.chave_comparabilidade;
ALTER VIEW public.v_elo_pcp_demanda_humana_projetada_externa SET (security_invoker=true);
COMMENT ON VIEW public.v_elo_pcp_demanda_humana_projetada_externa IS
'Aplica o fator de produto comparavel a demanda humana historica da mesma funcao. Nao usa quadro de RH. Sem composicao rastreavel, retorna GAP em vez de rateio.';

INSERT INTO public.elo_automation_registry(code,name,purpose,trigger_type,schedule,source_table,target_action,enabled,requires_validation)
SELECT 'elo_pcp_demanda_crossing','ELO PCP - Cruzamento de demanda e demanda humana',
       'Quando historico e previsao dos horizontes do PCP estiverem presentes, criar uma execucao pendente para o ELO pedir a confirmacao do cruzamento antes do calculo da demanda humana projetada.',
       'EVENT',NULL,'mt_demanda_historico + mt_previsoes_demanda','ASK_PCP_CROSSING_CONFIRMATION',true,true
WHERE NOT EXISTS (SELECT 1 FROM public.elo_automation_registry WHERE code='elo_pcp_demanda_crossing');

CREATE OR REPLACE FUNCTION public.elo_pcp_disparar_crossing_demanda()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path=''
AS $$
DECLARE v_automation_id uuid; v_hist integer; v_prev integer;
BEGIN
  PERFORM pg_advisory_xact_lock(hashtextextended('elo_pcp_demanda_crossing',0));
  SELECT id INTO v_automation_id FROM public.elo_automation_registry WHERE code='elo_pcp_demanda_crossing' AND enabled=true LIMIT 1;
  IF v_automation_id IS NULL THEN RETURN NULL; END IF;
  SELECT COUNT(*) INTO v_hist FROM public.mt_demanda_historico WHERE periodo_inicio>=DATE '2025-09-01' AND periodo_fim<=DATE '2026-02-28' AND quantidade_real IS NOT NULL;
  SELECT COUNT(*) INTO v_prev FROM public.mt_previsoes_demanda WHERE periodo_inicio>=DATE '2026-09-01' AND periodo_fim<=DATE '2027-02-28' AND quantidade_prevista IS NOT NULL;
  IF v_hist=0 OR v_prev=0 THEN RETURN NULL; END IF;
  IF EXISTS (SELECT 1 FROM public.elo_automation_runs r WHERE r.automation_id=v_automation_id AND r.status IN ('PENDING_INPUT','RUNNING') AND COALESCE(r.details->>'intent','')='PCP_DEMANDA_CROSSING') THEN RETURN NULL; END IF;
  INSERT INTO public.elo_automation_runs(automation_id,started_at,status,rows_affected,details)
  VALUES(v_automation_id,now(),'PENDING_INPUT',v_hist+v_prev,jsonb_build_object(
    'intent','PCP_DEMANDA_CROSSING','historico_registros',v_hist,'previsao_registros',v_prev,
    'historico_inicio','2025-09-01','historico_fim','2026-02-28','previsao_inicio','2026-09-01','previsao_fim','2027-02-28',
    'next_question','Os dados historicos e a previsao foram inseridos. Posso cruzar os produtos comparaveis, calcular os fatores de crescimento/reducao e aplicar esses fatores a demanda humana historica por funcao?',
    'rule','Nao aplicar o fator ao quadro de RH; aplicar somente a demanda humana historica correspondente, apos validar comparabilidade.'));
  RETURN NULL;
END;
$$;
REVOKE ALL ON FUNCTION public.elo_pcp_disparar_crossing_demanda() FROM PUBLIC;
DROP TRIGGER IF EXISTS trg_elo_pcp_demanda_historico_crossing ON public.mt_demanda_historico;
CREATE TRIGGER trg_elo_pcp_demanda_historico_crossing AFTER INSERT OR UPDATE OR DELETE ON public.mt_demanda_historico FOR EACH STATEMENT EXECUTE FUNCTION public.elo_pcp_disparar_crossing_demanda();
DROP TRIGGER IF EXISTS trg_elo_pcp_previsoes_crossing ON public.mt_previsoes_demanda;
CREATE TRIGGER trg_elo_pcp_previsoes_crossing AFTER INSERT OR UPDATE OR DELETE ON public.mt_previsoes_demanda FOR EACH STATEMENT EXECUTE FUNCTION public.elo_pcp_disparar_crossing_demanda();
COMMENT ON FUNCTION public.elo_pcp_disparar_crossing_demanda() IS
'Gatilho do loop PCP: quando os dois horizontes possuem dados, cria PENDING_INPUT com a pergunta de cruzamento. Nao calcula nem altera demanda humana automaticamente.';
