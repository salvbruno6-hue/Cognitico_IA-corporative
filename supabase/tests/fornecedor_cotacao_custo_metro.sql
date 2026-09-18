-- Supabase validation for supplier quotation -> Lista Mãe loop.
-- Run in a controlled database session after the migration is applied.
begin;

do $$
declare
  v_supplier uuid;
  v_result jsonb;
  v_quote uuid;
begin
  select id into v_supplier from public.fornecedores limit 1;
  if v_supplier is null then
    raise exception 'No supplier available for quotation loop test';
  end if;

  v_result := public.registrar_cotacao_fornecedor(
    v_supplier,
    'TEST-ELO-COT-001',
    date '2026-09-18',
    'TEST',
    'A VISTA',
    2,
    2,
    null,
    20,
    null,
    null,
    null,
    'TEST ONLY',
    jsonb_build_array(
      jsonb_build_object(
        'codigo_item','TEST-01',
        'descricao','TEST METALON 50X30X1,20',
        'unidade','PÇ',
        'quantidade',2,
        'valor_unitario',86.10,
        'comprimento_m',6,
        'lista_mae_id',(select id from public.lista_mae where cod_item='EST042' limit 1)
      )
    )
  );

  v_quote := (v_result->>'cotacao_id')::uuid;

  if (v_result->>'itens_processados')::int <> 1 then
    raise exception 'Expected 1 processed item: %', v_result;
  end if;

  if not exists (
    select 1 from public.fornecedor_itens_cotacao
    where cotacao_id=v_quote and metros_totais=12
      and lista_mae_id=(select id from public.lista_mae where cod_item='EST042' limit 1)
  ) then
    raise exception 'Quotation item was not linked/calculated as expected';
  end if;
end $$;

rollback;
