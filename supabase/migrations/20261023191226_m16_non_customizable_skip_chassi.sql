do $$
declare
  v_m16 uuid;
  v_base_flow uuid;
  v_m16_flow uuid;
begin
  select id into v_m16
  from public.modelos
  where upper(codigo) in ('M16','MLT.M16')
    and ativo is true
  order by case when upper(codigo)='MLT.M16' then 0 else 1 end
  limit 1;

  if v_m16 is null then
    raise exception 'M16 canonical model not found';
  end if;

  update public.modelos
     set nome = 'Habitacional Amplo 20 pés — Não Alterável',
         descricao = 'Equivalente ao M01 Habitacional Amplo 20 pés em configuração base, porém NÃO ALTERÁVEL conforme regra de negócio confirmada. Não admite customização. Para fabricação de chassi/estrutura metálica, M16 NÃO gera fabricação de CHASSI; usar fluxo específico MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1.',
         updated_at = now()
   where id = v_m16;

  select id into v_base_flow
  from public.fluxo_produtivo_modular
  where codigo='MLT.PROD.PADRAO.V2'
    and ativo is true
  limit 1;

  if v_base_flow is null then
    raise exception 'Base flow MLT.PROD.PADRAO.V2 not found';
  end if;

  insert into public.fluxo_produtivo_modular
    (codigo,nome,modelo_id,versao,descricao,lead_time_dias,capacidade_referencia,unidade_capacidade,ativo,observacoes)
  values
    ('MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1','Fluxo produtivo M16 não customizável',v_m16,'1.0','Fluxo específico do M16. Derivado do fluxo padrão V2, com exclusão explícita da etapa CHASSI por regra de negócio. Não inferir exclusão de outras etapas sem nova evidência.',null,null,null,true,'M16 é equivalente conceitualmente ao M01 em configuração base, porém não customizável. Não gera fabricação de chassi/estrutura metálica.')
  on conflict (codigo) do update
    set nome=excluded.nome,
        modelo_id=excluded.modelo_id,
        versao=excluded.versao,
        descricao=excluded.descricao,
        ativo=true,
        observacoes=excluded.observacoes,
        updated_at=now()
  returning id into v_m16_flow;

  delete from public.fluxo_produtivo_modular_etapas
  where fluxo_id=v_m16_flow;

  insert into public.fluxo_produtivo_modular_etapas
    (fluxo_id,ordem,codigo_etapa,nome,setor,processo,recurso,tempo_setup_min,tempo_unitario_min,capacidade,unidade_capacidade,dependencias,materiais,criterios_qualidade,status,observacoes)
  select
    v_m16_flow,
    row_number() over (order by e.ordem)::int,
    e.codigo_etapa,e.nome,e.setor,e.processo,e.recurso,e.tempo_setup_min,e.tempo_unitario_min,e.capacidade,e.unidade_capacidade,e.dependencias,e.materiais,e.criterios_qualidade,e.status,
    case when e.codigo_etapa='CORTE_DOBRA'
      then coalesce(e.observacoes,'') || ' M16 não deve ser interpretado como autorização para fabricar CHASSI; a etapa CHASSI é excluída neste fluxo específico.'
      else e.observacoes
    end
  from public.fluxo_produtivo_modular_etapas e
  where e.fluxo_id=v_base_flow
    and e.status='ATIVO'
    and e.codigo_etapa <> 'CHASSI'
  order by e.ordem;
end $$;
