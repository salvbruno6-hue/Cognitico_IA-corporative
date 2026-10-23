-- PCP/MRP: corrige classificação de necessidade bruta quando falta cod_produt.
-- O cálculo técnico pode existir, mas não deve ser promovido como necessidade definitiva de compra.

create or replace view public.v_elo_pcp_mrp_requisito_fisico_m01
with (security_invoker = true)
as
with requisito as (
  select *
  from public.v_elo_pcp_requisito_fisico_planejamento
  where modelo_codigo = 'M01'
    and quantidade_restante > 0
), base_existente as (
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
    'PARCIAL_5_PROCESSOS'::text as cobertura_bom,
    case
      when b.cod_produt is null then 'CALCULO_BRUTO_COM_GAP_CADASTRO_NAO_PROMOVER'
      else 'NECESSIDADE_BRUTA_CALCULADA'
    end as estado_necessidade_bruta,
    case
      when r.tenant_id is null then 'BLOQUEADO_GAP_TENANT_E_ESTOQUE'
      else 'BLOQUEADO_SEM_ESTOQUE_RESERVAS_PEDIDOS_SALDO_TECNICO'
    end as estado_mrp_liquido,
    'A view não calcula necessidade líquida nem autoriza compra. Itens sem cod_produt mantêm cálculo técnico referencial, mas não podem ser promovidos a instrução de compra.'::text as governanca
  from requisito r
  cross join public.vw_pcp_bom_almox_pedido_compras_m01_120 b
), eletrica as (
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
    (400 + e.ordem)::integer as ordem,
    'ELETRICA_M01'::text as processo,
    'vw_kit_eletrico_m01_completo'::text as origem_bom,
    e.cod_item,
    coalesce(e.cod_produto_lista_mae,e.cod_produto_kit) as cod_produt,
    coalesce(e.descricao_lista_mae,e.descricao_kit) as descricao,
    e.quantidade as consumo_unitario,
    e.un as un_consumo,
    r.quantidade_restante as qtd_planejada_origem_readmodel,
    (e.quantidade * r.quantidade_restante) as necessidade_bruta_requisito,
    e.un as un_pedido,
    null::numeric as fator_embalagem,
    null::text as unidade_fator,
    case
      when coalesce(e.cod_produto_lista_mae,e.cod_produto_kit) is null then 'GAP_COD_PRODUTO'
      when e.elo_situacao = 'SEM_CORRESPONDÊNCIA' then 'CONFLITO_VINCULO'
      when e.elo_situacao = 'DÚVIDA' or coalesce(e.vinculo_confianca,0) < 1 then 'EVIDENCIA_PARCIAL'
      else 'CONSUMO_UNITARIO_LOCALIZADO'
    end as estado_cadastro_item,
    'PARCIAL_5_PROCESSOS'::text as cobertura_bom,
    case
      when coalesce(e.cod_produto_lista_mae,e.cod_produto_kit) is null then 'CALCULO_BRUTO_COM_GAP_CADASTRO_NAO_PROMOVER'
      when e.elo_situacao = 'SEM_CORRESPONDÊNCIA' then 'CALCULO_REFERENCIAL_CONFLITO_NAO_PROMOVER'
      when e.elo_situacao = 'DÚVIDA' or coalesce(e.vinculo_confianca,0) < 1 then 'CALCULO_REFERENCIAL_PARCIAL_NAO_PROMOVER'
      else 'NECESSIDADE_BRUTA_CALCULADA'
    end as estado_necessidade_bruta,
    case
      when r.tenant_id is null then 'BLOQUEADO_GAP_TENANT_E_ESTOQUE'
      else 'BLOQUEADO_SEM_ESTOQUE_RESERVAS_PEDIDOS_SALDO_TECNICO'
    end as estado_mrp_liquido,
    'Consumo elétrico reutilizado da view viva M01. Linhas com DÚVIDA, SEM_CORRESPONDÊNCIA, confiança de vínculo inferior a 1 ou ausência de cod_produt permanecem referenciais e não podem ser promovidas a compra definitiva.'::text as governanca
  from requisito r
  cross join public.vw_kit_eletrico_m01_completo e
  where e.ativo = true
)
select * from base_existente
union all
select * from eletrica;

comment on view public.v_elo_pcp_mrp_requisito_fisico_m01 is
'PCP read-model: necessidade bruta M01 a partir do requisito físico e fontes vigentes. Cobertura parcial de estrutura, montagem, piso, fibra e elétrica; GAPs e conflitos permanecem classificados. Não substitui BOM canônica nem MRP líquido.';
