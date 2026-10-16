-- MLT.M01 — associação canônica das peças aos grupos de matéria-prima.
-- A autoridade material permanece COD_PRODUT; grupo_material e grupo_peca são classificações auxiliares.
-- Inclui os acabamentos da planilha e os perfis Z externos do apontamento complementar validado.

alter table public.estrutura_metalica_20_componentes
  add column if not exists grupo_material text,
  add column if not exists grupo_peca text,
  add column if not exists fonte_associacao text;

update public.estrutura_metalica_20_componentes
set
  grupo_material = case cod_produt
    when '3200600075' then 'CHAPA_GALVANIZADA_2_70'
    when '3200600288' then 'PERFIL_UDC_6'
    when '3200600289' then 'PERFIL_UDC_5'
    when '3200600335' then 'PERFIL_UDC_8'
    when '3200600291' then 'PERFIL_UDC_3'
    when '3200600239' then 'CHAPA_GALVANIZADA_1_95'
    when '3200600260' then 'CHAPA_PRETA_6_35'
    else grupo_material
  end,
  grupo_peca = case
    when item in ('COL01','COL02') then 'COLUNAS'
    when item in ('LGIL06','LGIF0244','LGSF244','LGSL06') then 'LONGARINAS'
    when item = 'TRV01' then 'TRAVESSAS'
    when item = 'SPT01' then 'SUPORTES'
    when item = 'PRTH01' then 'PERFIS_TELHA'
    when item in ('PRTL01','PRTF02') then 'PERFIS_T'
    when item in ('PRZ01','PRZ02') then 'PERFIS_Z'
    when item in ('CNU01','CNUC01','CNUC02','CNUC03','CNUC05','CNUC06') then 'CONECTORES'
    when item = 'CNUC04' then 'ICAMENTO'
    when item in ('RFLI01','RFLI02') then 'REFORCOS'
    else grupo_peca
  end,
  fonte_associacao = coalesce(fonte_associacao, 'PLANILHA_PECAS_MLT_M01_2026-10-16'),
  updated_at = now();

update public.estrutura_metalica_20_componentes
set descricao = case item
  when 'CNU01' then 'Conector U de um furo'
  when 'CNUC01' then 'Conector cantoneira com furo maior — coluna'
  when 'CNUC02' then 'Conector cantoneira com furo maior — base'
  when 'CNUC03' then 'Conector U de dois furos'
  when 'CNUC04' then 'Triângulo de içamento'
  when 'CNUC05' then 'Conector cantoneira com um furo menor — coluna'
  when 'CNUC06' then 'Conector cantoneira com um furo menor — base'
  else descricao
end,
updated_at = now()
where item in ('CNU01','CNUC01','CNUC02','CNUC03','CNUC04','CNUC05','CNUC06');

insert into public.estrutura_metalica_20_componentes
  (item,cod_produt,descricao,quantidade,peso_unitario,peso_pecas,rs_kg_peca,valor_unitario_peca,valor_pecas,ativo,grupo_material,grupo_peca,fonte_associacao)
values
  ('ACAB_COLUNA','3200600100','Acabamento de coluna em chapa primer branca 0,50 mm',4,2.51,10.03,12.00,30.09,120.37,true,'CHAPA_PRIMER_BRANCA_0_50','ACABAMENTOS','PLANILHA_PECAS_MLT_M01_2026-10-16'),
  ('ACAB_TETO','3200600124','Acabamento de teto em chapa primer stucco 0,50 mm',1,2.25,2.25,12.00,27.04,27.04,true,'CHAPA_PRIMER_STUCCO_0_50','ACABAMENTOS','PLANILHA_PECAS_MLT_M01_2026-10-16'),
  ('PRZ_EXT_2080','3200600065','Perfil Z externo 74x2080 mm — chapa 1,55 mm',4,1.908608,7.634432,null,null,null,true,'CHAPA_1_55_PERFIS_Z_EXTERNOS','PERFIS_Z','APONTAMENTO_COMPLEMENTAR_VALIDADO_2026-10-16'),
  ('PRZ_EXT_2820','3200600065','Perfil Z externo 74x2820 mm — chapa 1,55 mm',8,2.587632,20.701056,null,null,null,true,'CHAPA_1_55_PERFIS_Z_EXTERNOS','PERFIS_Z','APONTAMENTO_COMPLEMENTAR_VALIDADO_2026-10-16')
on conflict (item) do update set
  cod_produt = excluded.cod_produt,
  descricao = excluded.descricao,
  quantidade = excluded.quantidade,
  peso_unitario = excluded.peso_unitario,
  peso_pecas = excluded.peso_pecas,
  rs_kg_peca = excluded.rs_kg_peca,
  valor_unitario_peca = excluded.valor_unitario_peca,
  valor_pecas = excluded.valor_pecas,
  ativo = excluded.ativo,
  grupo_material = excluded.grupo_material,
  grupo_peca = excluded.grupo_peca,
  fonte_associacao = excluded.fonte_associacao,
  updated_at = now();

alter table public.estrutura_metalica_20_componentes
  alter column grupo_material set not null,
  alter column grupo_peca set not null,
  alter column fonte_associacao set not null;

create or replace view public.vw_estrutura_metalica_20_associacao_material
with (security_invoker = true)
as
select
  c.item,
  c.cod_produt,
  p.material,
  c.grupo_material,
  c.grupo_peca,
  c.descricao,
  c.quantidade,
  c.peso_unitario,
  c.peso_pecas,
  c.rs_kg_peca,
  c.valor_unitario_peca,
  c.valor_pecas,
  c.fonte_associacao,
  p.peso_aplicado_kg as peso_aplicado_oficial_material_kg,
  p.status_dado as status_material,
  p.metodo_calculo as metodo_calculo_material
from public.estrutura_metalica_20_componentes c
left join public.vw_perda_estrutura_metalica_20 p using (cod_produt)
where c.ativo;

create or replace view public.vw_estrutura_metalica_20_material_componentes_resumo
with (security_invoker = true)
as
with componentes as (
  select
    cod_produt,
    max(material) as material,
    string_agg(distinct grupo_material, ', ' order by grupo_material) as grupos_material,
    string_agg(distinct grupo_peca, ', ' order by grupo_peca) as grupos_peca,
    count(*)::integer as itens_componentes,
    sum(quantidade) as quantidade_pecas,
    round(sum(coalesce(peso_pecas,0)),3) as peso_pecas_planilha_kg,
    string_agg(item || ' — ' || descricao, ' | ' order by item) as componentes,
    string_agg(distinct fonte_associacao, ', ' order by fonte_associacao) as fontes_associacao
  from public.vw_estrutura_metalica_20_associacao_material
  group by cod_produt
)
select
  c.cod_produt,
  c.material,
  c.grupos_material,
  c.grupos_peca,
  c.itens_componentes,
  c.quantidade_pecas,
  c.peso_pecas_planilha_kg,
  p.peso_aplicado_kg as peso_aplicado_oficial_kg,
  round(c.peso_pecas_planilha_kg - p.peso_aplicado_kg,3) as delta_base_calculo_kg,
  p.metodo_calculo,
  p.status_dado,
  c.componentes,
  c.fontes_associacao
from componentes c
join public.vw_perda_estrutura_metalica_20 p using (cod_produt)
order by c.cod_produt;

comment on column public.estrutura_metalica_20_componentes.grupo_material is
'Grupo da matéria-prima associado ao COD_PRODUT; não substitui o código canônico de compra.';
comment on column public.estrutura_metalica_20_componentes.grupo_peca is
'Família funcional da peça: conectores, acabamentos, perfis, longarinas, reforços etc.';
comment on column public.estrutura_metalica_20_componentes.fonte_associacao is
'Proveniência da associação peça → matéria-prima/grupo.';
comment on view public.vw_estrutura_metalica_20_associacao_material is
'MLT.M01 — associação canônica peça → COD_PRODUT → grupo de material/grupo de peça, com método oficial da VW de perda.';
comment on view public.vw_estrutura_metalica_20_material_componentes_resumo is
'MLT.M01 — resumo por matéria-prima mostrando quais componentes pertencem ao material e a diferença entre peso bruto da planilha de peças e peso aplicado oficial quando há normalização de base.';