-- ELO / Multiteiner — cotação de fornecedores + custo por metro + loop de salvamento na Lista Mãe.
-- Escopo: DATA/MIGRATION + IMPLEMENTATION.

create table if not exists public.fornecedor_cotacoes (
  id uuid primary key default gen_random_uuid(),
  fornecedor_id uuid not null references public.fornecedores(id),
  numero_cotacao text,
  data_cotacao date not null,
  documento text,
  condicao_pagamento text,
  prazo_entrega_dias integer,
  validade_dias integer,
  frete_total numeric(14,2),
  frete_rateio_metodo text not null default 'VALOR_ITEM',
  icms_aliquota numeric(8,4),
  icms_incluso boolean,
  outros_tributos_aliquota numeric(8,4),
  outros_tributos_inclusos boolean,
  status text not null default 'REGISTRADA',
  observacoes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint fornecedor_cotacoes_rateio_ck check (frete_rateio_metodo in ('VALOR_ITEM','PESO','QUANTIDADE','METRAGEM','MANUAL')),
  constraint fornecedor_cotacoes_status_ck check (status in ('REGISTRADA','PENDENTE_VALIDACAO','VALIDADA','CANCELADA'))
);

create unique index if not exists ux_fornecedor_cotacoes_numero_data
  on public.fornecedor_cotacoes(fornecedor_id, numero_cotacao, data_cotacao)
  where numero_cotacao is not null;

create table if not exists public.fornecedor_itens_cotacao (
  id uuid primary key default gen_random_uuid(),
  fornecedor_id uuid not null references public.fornecedores(id),
  cotacao_id uuid references public.fornecedor_cotacoes(id),
  codigo_item text not null,
  categoria text not null default 'MATERIAL',
  descricao text not null,
  tipo text,
  largura_m numeric(14,6),
  altura_m numeric(14,6),
  quantidade numeric(14,4),
  area_unit_m2 numeric(14,6),
  area_total_m2 numeric(14,6),
  espessura_mm numeric(14,4),
  material text,
  acabamento text,
  caracteristicas text,
  valor_unitario numeric(14,2),
  valor_total numeric(14,2),
  unidade text,
  origem_so text,
  origem_documento text,
  status text not null default 'PENDENTE',
  observacao text,
  lista_mae_id uuid references public.lista_mae(id),
  comprimento_m numeric(14,6),
  metros_totais numeric(14,6),
  icms_aliquota numeric(8,4),
  icms_incluso boolean,
  outros_tributos_aliquota numeric(8,4),
  outros_tributos_inclusos boolean,
  frete_rateado numeric(14,2),
  tributos_adicionais numeric(14,2),
  custo_total_com_encargos numeric(14,2),
  custo_por_unidade_com_encargos numeric(14,4),
  custo_por_metro numeric(14,4),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.fornecedor_itens_cotacao add column if not exists cotacao_id uuid references public.fornecedor_cotacoes(id);
alter table public.fornecedor_itens_cotacao add column if not exists lista_mae_id uuid references public.lista_mae(id);
alter table public.fornecedor_itens_cotacao add column if not exists comprimento_m numeric(14,6);
alter table public.fornecedor_itens_cotacao add column if not exists metros_totais numeric(14,6);
alter table public.fornecedor_itens_cotacao add column if not exists icms_aliquota numeric(8,4);
alter table public.fornecedor_itens_cotacao add column if not exists icms_incluso boolean;
alter table public.fornecedor_itens_cotacao add column if not exists outros_tributos_aliquota numeric(8,4);
alter table public.fornecedor_itens_cotacao add column if not exists outros_tributos_inclusos boolean;
alter table public.fornecedor_itens_cotacao add column if not exists frete_rateado numeric(14,2);
alter table public.fornecedor_itens_cotacao add column if not exists tributos_adicionais numeric(14,2);
alter table public.fornecedor_itens_cotacao add column if not exists custo_total_com_encargos numeric(14,2);
alter table public.fornecedor_itens_cotacao add column if not exists custo_por_unidade_com_encargos numeric(14,4);
alter table public.fornecedor_itens_cotacao add column if not exists custo_por_metro numeric(14,4);
alter table public.fornecedor_itens_cotacao add column if not exists updated_at timestamptz not null default now();

create index if not exists ix_fornecedor_itens_cotacao_cotacao on public.fornecedor_itens_cotacao(cotacao_id);
create index if not exists ix_fornecedor_itens_cotacao_lista_mae on public.fornecedor_itens_cotacao(lista_mae_id);
create index if not exists ix_fornecedor_cotacoes_fornecedor_data on public.fornecedor_cotacoes(fornecedor_id, data_cotacao desc);

create or replace function public.registrar_cotacao_fornecedor(
  p_fornecedor_id uuid,
  p_numero_cotacao text,
  p_data_cotacao date,
  p_documento text,
  p_condicao_pagamento text,
  p_prazo_entrega_dias integer,
  p_validade_dias integer,
  p_frete_total numeric,
  p_icms_aliquota numeric,
  p_icms_incluso boolean,
  p_outros_tributos_aliquota numeric,
  p_outros_tributos_inclusos boolean,
  p_observacoes text,
  p_itens jsonb
) returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_cotacao_id uuid;
  v_item jsonb;
  v_lista_mae_id uuid;
  v_valor_total_itens numeric := 0;
  v_frete_rateado numeric;
  v_tributos numeric;
  v_custo_total numeric;
  v_metros numeric;
  v_processados integer := 0;
  v_vinculados integer := 0;
  v_sem_vinculo integer := 0;
begin
  if p_itens is null or jsonb_typeof(p_itens) <> 'array' or jsonb_array_length(p_itens) = 0 then
    raise exception 'p_itens deve ser um array JSONB não vazio';
  end if;

  insert into public.fornecedor_cotacoes (
    fornecedor_id, numero_cotacao, data_cotacao, documento,
    condicao_pagamento, prazo_entrega_dias, validade_dias,
    frete_total, frete_rateio_metodo, icms_aliquota, icms_incluso,
    outros_tributos_aliquota, outros_tributos_inclusos, status, observacoes
  ) values (
    p_fornecedor_id, p_numero_cotacao, p_data_cotacao, p_documento,
    p_condicao_pagamento, p_prazo_entrega_dias, p_validade_dias,
    p_frete_total, 'VALOR_ITEM', p_icms_aliquota, p_icms_incluso,
    p_outros_tributos_aliquota, p_outros_tributos_inclusos,
    case when p_frete_total is null or p_icms_incluso is null or p_outros_tributos_inclusos is null
         then 'PENDENTE_VALIDACAO' else 'REGISTRADA' end,
    p_observacoes
  ) returning id into v_cotacao_id;

  select coalesce(sum(coalesce((x->>'valor_total')::numeric,
                                (x->>'quantidade')::numeric * (x->>'valor_unitario')::numeric, 0)),0)
    into v_valor_total_itens
  from jsonb_array_elements(p_itens) x;

  for v_item in select value from jsonb_array_elements(p_itens)
  loop
    v_lista_mae_id := null;

    if nullif(v_item->>'lista_mae_id','') is not null then
      select id into v_lista_mae_id
      from public.lista_mae
      where id = (v_item->>'lista_mae_id')::uuid;
    elsif nullif(v_item->>'cod_produt','') is not null then
      select id into v_lista_mae_id
      from public.lista_mae
      where cod_produt = v_item->>'cod_produt';
    end if;

    if v_lista_mae_id is null then
      select id into v_lista_mae_id
      from public.lista_mae
      where upper(trim(descricao_oficial)) = upper(trim(v_item->>'descricao'))
        and coalesce(upper(trim(un)),'') = coalesce(upper(trim(v_item->>'unidade')),'')
      order by updated_at desc
      limit 1;
    end if;

    v_frete_rateado := case
      when p_frete_total is null or v_valor_total_itens = 0 then null
      else p_frete_total * coalesce((v_item->>'valor_total')::numeric,
             (v_item->>'quantidade')::numeric * (v_item->>'valor_unitario')::numeric, 0) / v_valor_total_itens
    end;

    v_tributos := case
      when p_icms_incluso is null or p_outros_tributos_inclusos is null then null
      else (case when p_icms_incluso = false then
             coalesce((v_item->>'valor_total')::numeric,
               (v_item->>'quantidade')::numeric * (v_item->>'valor_unitario')::numeric, 0)
             * coalesce(p_icms_aliquota,0) / 100 else 0 end)
           + (case when p_outros_tributos_inclusos = false then
             coalesce((v_item->>'valor_total')::numeric,
               (v_item->>'quantidade')::numeric * (v_item->>'valor_unitario')::numeric, 0)
             * coalesce(p_outros_tributos_aliquota,0) / 100 else 0 end)
    end;

    v_custo_total := case
      when p_frete_total is null or v_tributos is null then null
      else coalesce((v_item->>'valor_total')::numeric,
             (v_item->>'quantidade')::numeric * (v_item->>'valor_unitario')::numeric, 0)
           + coalesce(v_frete_rateado,0) + coalesce(v_tributos,0)
    end;

    v_metros := case
      when nullif(v_item->>'comprimento_m','') is not null then
        coalesce((v_item->>'quantidade')::numeric,0) * (v_item->>'comprimento_m')::numeric
      else null
    end;

    insert into public.fornecedor_itens_cotacao (
      fornecedor_id, cotacao_id, codigo_item, categoria, descricao, tipo,
      largura_m, altura_m, quantidade, area_unit_m2, area_total_m2,
      espessura_mm, material, acabamento, caracteristicas, valor_unitario,
      valor_total, unidade, origem_so, origem_documento, status, observacao,
      lista_mae_id, comprimento_m, metros_totais, icms_aliquota, icms_incluso,
      outros_tributos_aliquota, outros_tributos_inclusos, frete_rateado,
      tributos_adicionais, custo_total_com_encargos, custo_por_unidade_com_encargos,
      custo_por_metro
    ) values (
      p_fornecedor_id, v_cotacao_id, v_item->>'codigo_item', coalesce(v_item->>'categoria','MATERIAL'),
      v_item->>'descricao', v_item->>'tipo',
      nullif(v_item->>'largura_m','')::numeric, nullif(v_item->>'altura_m','')::numeric,
      nullif(v_item->>'quantidade','')::numeric, nullif(v_item->>'area_unit_m2','')::numeric,
      nullif(v_item->>'area_total_m2','')::numeric, nullif(v_item->>'espessura_mm','')::numeric,
      v_item->>'material', v_item->>'acabamento', v_item->>'caracteristicas',
      nullif(v_item->>'valor_unitario','')::numeric,
      coalesce(nullif(v_item->>'valor_total','')::numeric,
               nullif(v_item->>'quantidade','')::numeric * nullif(v_item->>'valor_unitario','')::numeric),
      v_item->>'unidade', v_item->>'origem_so', v_item->>'origem_documento',
      case when v_lista_mae_id is null then 'PENDENTE_VINCULO_LISTA_MAE' else 'VINCULADO_LISTA_MAE' end,
      v_item->>'observacao', v_lista_mae_id, nullif(v_item->>'comprimento_m','')::numeric,
      v_metros, p_icms_aliquota, p_icms_incluso, p_outros_tributos_aliquota,
      p_outros_tributos_inclusos, v_frete_rateado, v_tributos, v_custo_total,
      case when v_custo_total is null or coalesce((v_item->>'quantidade')::numeric,0)=0 then null
           else v_custo_total / (v_item->>'quantidade')::numeric end,
      case when v_custo_total is null or coalesce(v_metros,0)=0 then null
           else v_custo_total / v_metros end
    );

    v_processados := v_processados + 1;
    if v_lista_mae_id is not null then v_vinculados := v_vinculados + 1;
    else v_sem_vinculo := v_sem_vinculo + 1;
    end if;
  end loop;

  return jsonb_build_object(
    'cotacao_id', v_cotacao_id,
    'itens_processados', v_processados,
    'itens_vinculados_lista_mae', v_vinculados,
    'itens_pendentes_vinculo', v_sem_vinculo,
    'status', (select status from public.fornecedor_cotacoes where id=v_cotacao_id)
  );
end;
$$;

revoke all on function public.registrar_cotacao_fornecedor(uuid,text,date,text,text,integer,integer,numeric,numeric,boolean,numeric,boolean,text,jsonb) from public, anon, authenticated;
grant execute on function public.registrar_cotacao_fornecedor(uuid,text,date,text,text,integer,integer,numeric,numeric,boolean,numeric,boolean,text,jsonb) to service_role;

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
  i.status as status_item
from public.fornecedor_cotacoes c
join public.fornecedor_itens_cotacao i on i.cotacao_id=c.id
join public.fornecedores f on f.id=c.fornecedor_id;
