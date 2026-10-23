create or replace view public.v_elo_pcp_bom_referencia_m16
with (security_invoker = true)
as
with base_m01 as (
  select
    1000 + b.ordem as ordem,
    b.processo,
    b.origem_bom,
    b.cod_item,
    b.cod_produt,
    b.descricao,
    b.consumo_unitario,
    b.un_consumo,
    case
      when b.cod_produt is null then 'GAP_COD_PRODUTO'
      else 'CONSUMO_UNITARIO_LOCALIZADO'
    end as estado_cadastro_item,
    'M01'::text as modelo_origem,
    'M16_EQ_M01_BASE_SEM_ESTRUTURA_METALICA'::text as regra_heranca,
    'HERDADO_M01_NAO_ESTRUTURAL'::text as natureza_referencia,
    'Referência unitária para M16 derivada do M01. ESTRUTURA_METALICA foi excluída porque M16 não gera fabricação de CHASSI. Esta view não representa demanda, estoque, necessidade líquida nem autorização de compra.'::text as governanca
  from public.vw_pcp_bom_almox_pedido_compras_m01_120 b
  where upper(b.processo) <> 'ESTRUTURA_METALICA'
), eletrica_m01 as (
  select
    2000 + e.ordem as ordem,
    'ELETRICA_M01'::text as processo,
    'vw_kit_eletrico_m01_completo'::text as origem_bom,
    e.cod_item,
    coalesce(e.cod_produto_lista_mae, e.cod_produto_kit) as cod_produt,
    coalesce(e.descricao_lista_mae, e.descricao_kit) as descricao,
    e.quantidade as consumo_unitario,
    e.un as un_consumo,
    case
      when coalesce(e.cod_produto_lista_mae, e.cod_produto_kit) is null then 'GAP_COD_PRODUTO'
      when e.elo_situacao = 'SEM_CORRESPONDÊNCIA' then 'CONFLITO_VINCULO'
      when e.elo_situacao = 'DÚVIDA' or coalesce(e.vinculo_confianca, 0) < 1 then 'EVIDENCIA_PARCIAL'
      else 'CONSUMO_UNITARIO_LOCALIZADO'
    end as estado_cadastro_item,
    'M01'::text as modelo_origem,
    'M16_EQ_M01_BASE_SEM_ESTRUTURA_METALICA'::text as regra_heranca,
    'HERDADO_M01_ELETRICA'::text as natureza_referencia,
    'Referência unitária elétrica para M16 derivada do M01 pela equivalência de configuração base confirmada. Linhas com dúvida, conflito ou gap de código permanecem não promovíveis. Esta view não representa demanda nem autorização de compra.'::text as governanca
  from public.vw_kit_eletrico_m01_completo e
  where e.ativo is true
)
select * from base_m01
union all
select * from eletrica_m01;
