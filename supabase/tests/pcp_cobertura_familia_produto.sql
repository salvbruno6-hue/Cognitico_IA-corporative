do $$
begin
  if not exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'v_elo_pcp_cobertura_demanda_externa'
      and column_name = 'familia_produto'
  ) then
    raise exception 'v_elo_pcp_cobertura_demanda_externa sem coluna familia_produto';
  end if;

  if exists (
    select 1
    from public.v_elo_pcp_cobertura_demanda_externa
    where familia_produto not in ('MODULO','CONTEINER','OUTRO')
       or familia_produto is null
  ) then
    raise exception 'familia_produto possui valor fora da taxonomia analitica permitida';
  end if;
end
$$;
