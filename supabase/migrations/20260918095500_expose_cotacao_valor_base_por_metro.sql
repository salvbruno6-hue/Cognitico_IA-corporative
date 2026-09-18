-- ELO / Multiteiner — expose raw supplier cost per meter without conflating it with landed cost.

create or replace view public.vw_cotacoes_itens_custo as
select
  c.id as cotacao_id,
  c.numero_cotacao,
  c.data_cotacao,
  c.fornecedor_id,
  f.nome as fornecedor_nome,
  c.frete_total,
  c.icms_aliquota,
  c.icms_incluso,
  c.outros_tributos_aliquota,
  c.outros_tributos_inclusos,
  i.id as item_id,
  i.lista_mae_id,
  i.codigo_item,
  i.descricao,
  i.unidade,
  i.quantidade,
  i.comprimento_m,
  i.metros_totais,
  i.valor_unitario,
  i.valor_total,
  i.frete_rateado,
  i.tributos_adicionais,
  i.custo_total_com_encargos,
  i.custo_por_unidade_com_encargos,
  i.custo_por_metro,
  i.status as status_item,
  c.frete_rateio_metodo,
  c.status as status_cotacao,
  case
    when coalesce(i.metros_totais,0) > 0 then i.valor_total / i.metros_totais
    else null
  end as valor_base_por_metro
from public.fornecedor_cotacoes c
join public.fornecedor_itens_cotacao i on i.cotacao_id=c.id
join public.fornecedores f on f.id=c.fornecedor_id;
