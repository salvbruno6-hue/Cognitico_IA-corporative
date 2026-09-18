-- ELO schema governance: no duplicate table creation.
-- This audit is intentionally read-only. It must be run before introducing a table.
-- Existing canonical tables must be ALTERed/reused; only genuinely absent relations may be created.

do $$
declare
  v_expected text[] := array[
    'public.fornecedores',
    'public.fornecedor_itens_cotacao',
    'public.lista_mae',
    'public.compras_fornecedor',
    'public.compras_fornecedor_itens',
    'public.mt_fornecedor_itens',
    'public.mt_ordens_compra',
    'public.mt_ordens_compra_itens'
  ];
  v_name text;
  v_schema text;
  v_table text;
begin
  foreach v_name in array v_expected loop
    v_schema := split_part(v_name,'.',1);
    v_table := split_part(v_name,'.',2);

    if not exists (
      select 1 from pg_catalog.pg_tables
      where schemaname=v_schema and tablename=v_table
    ) then
      raise exception 'CANONICAL_SCHEMA_GAP: expected existing table % is absent. Do not create a parallel table; investigate migration state first.', v_name;
    end if;
  end loop;
end $$;

-- Semantic duplication guard for the supplier/procurement domain.
-- These are different canonical concepts and therefore must not be collapsed or duplicated:
-- fornecedor_itens_cotacao = quotation snapshot/item;
-- compras_fornecedor_itens = purchase item;
-- mt_fornecedor_itens = supplier/material relationship.
