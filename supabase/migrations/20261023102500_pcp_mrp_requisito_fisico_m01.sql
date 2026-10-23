-- Tenant layer / PCP read-model.
-- Reutiliza a view M01/120 apenas como fonte de consumo unitário e metadados de BOM.
-- Não promove estoque, necessidade líquida, pedido ou compra sem evidência operacional.

create or replace view public.v_elo_pcp_mrp_requisito_fisico_m01
with (security_invoker = true)
as
select
  r.id as requisito_id,
  r.tenant_id,
  r.modelo_id,
  r.modelo_codigo,
  r.modelo_nome,
  r.natureza_demanda,
  r.quantidade_objetivo,
  r.quantidade_restante,
  r.data_limite,
  b.ordem,
  b.processo,
  b.origem_bom,
  b.cod_item,
  b.cod_produt,
  b.descricao,
  b.consumo_unitario,
  b.un_consumo,
  b.qtd_planejada as qtd_planejada_origem_readmodel,
  (b.consumo_unitario * r.quantidade_restante) as necessidade_bruta_requisito,
  b.un_pedido,
  b.fator_embalagem,
  b.unidade_fator,
  case
    when b.cod_produt is null then 'GAP_COD_PRODUTO'
    else 'CONSUMO_UNITARIO_LOCALIZADO'
  end as estado_cadastro_item,
  'PARCIAL_4_PROCESSOS'::text as cobertura_bom,
  'NECESSIDADE_BRUTA_CALCULADA'::text as estado_necessidade_bruta,
  case
    when r.tenant_id is null then 'BLOQUEADO_GAP_TENANT_E_ESTOQUE'
    else 'BLOQUEADO_SEM_ESTOQUE_RESERVAS_PEDIDOS_SALDO_TECNICO'
  end as estado_mrp_liquido,
  'A view não calcula necessidade líquida nem autoriza compra. Estoque, reservas, saldo técnico, pedidos abertos e lead time devem ser confrontados nas autoridades operacionais antes de qualquer instrução de compras.'::text as governanca
from public.v_elo_pcp_requisito_fisico_planejamento r
cross join public.vw_pcp_bom_almox_pedido_compras_m01_120 b
where r.modelo_codigo = 'M01'
  and r.quantidade_restante > 0;

comment on view public.v_elo_pcp_mrp_requisito_fisico_m01 is
'PCP read-model: liga requisito físico M01 à necessidade bruta usando consumos unitários existentes. Não substitui BOM canônica, estoque, reservas, pedidos, saldo técnico ou MRP líquido.';
