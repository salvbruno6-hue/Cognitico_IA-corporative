CREATE OR REPLACE VIEW public.v_elo_pcp_demanda_comercial AS
SELECT
  pv.id AS pedido_venda_id,
  pv.tenant_id,
  pv.numero_pedido,
  pv.tipo_pedido,
  pv.status,
  pv.data_entrega_solicitada,
  pv.natureza_demanda,
  pv.chave_comparabilidade,
  pvi.id AS pedido_venda_item_id,
  pvi.modelo_id,
  pvi.lista_mae_id,
  pvi.quantidade,
  pvi.data_solicitada,
  pvi.personalizado
FROM public.mt_pedidos_venda pv
JOIN public.mt_pedidos_venda_itens pvi
  ON pvi.pedido_venda_id = pv.id
WHERE COALESCE(pv.status, '') NOT IN ('CANCELADO', 'CANCELADA');

ALTER VIEW public.v_elo_pcp_demanda_comercial
  SET (security_invoker = true);

COMMENT ON VIEW public.v_elo_pcp_demanda_comercial IS
'Fonte analítica da demanda comercial para PCP. Reutiliza mt_pedidos_venda e mt_pedidos_venda_itens; não representa demanda humana nem disponibilidade de RH.';
