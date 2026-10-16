-- MLT.M01 — promove a fonte validada de perda da estrutura metálica.
-- Fonte: Forge MLT.M01, tabelas de compra e peças validadas pelo usuário em 2026-10-16.
-- Regra: agrupar PESO PEÇAS por COD_PRODUT; diferença = comprado - utilizado;
-- diferenças negativas são divergências e não compensam saldos positivos.

create or replace view public.vw_perda_estrutura_metalica_20
with (security_invoker = true) as
with compra(cod_produt, material, aplicacao_principal, peso_comprado_kg, custo_rs_kg) as (
  values
    ('3200600291'::text,'PERFIL UDC ENRIJ 3" X 2,00MM (75ABA40X15) - 6m'::text,'Travessa de fixação de telha'::text,47.754::numeric,8.12::numeric),
    ('3200600289'::text,'PERFIL UDC ENRIJ 5" X 2,65MM (127ABA50X17) - 6m'::text,'Longarina frontal inferior, travessas e reforços internos do assoalho'::text,116.100::numeric,8.12::numeric),
    ('3200600288'::text,'PERFIL UDC ENRIJ 6" X 2,65MM (150ABA60X17) - 6m'::text,'Longarinas laterais inferiores'::text,72.000::numeric,8.12::numeric),
    ('3200600335'::text,'PERFIL UDC ENRIJ 8" X 2,00MM (200ABA75X20) - 6m'::text,'Longarinas superiores'::text,108.510::numeric,8.12::numeric),
    ('3200600075'::text,'Chapa 12 Galvanizada 2850X1200x2,70mm'::text,'Colunas, suportes e perfis Z estruturais'::text,147.744::numeric,7.78::numeric),
    ('3200600239'::text,'Chapa 14 Galvanizada 1200X3000x1,95mm'::text,'Perfis T / limitadores do assoalho'::text,56.160::numeric,8.78::numeric),
    ('3200600260'::text,'Chapa 1/4 (6,35) preta 1200x3000mm'::text,'Suportes de içamento e conectores'::text,27.942::numeric,6.00::numeric),
    ('3200600124'::text,'Chapa 26 0,5 primer stucco 1200X3000x0,5mm'::text,'Perfil / acabamento de forro do teto'::text,2.880::numeric,21.21::numeric),
    ('3200600065'::text,'Chapa 16 / 1,55mm 1200x3000x1,55mm'::text,'Perfis Z externos de fixação / travamento das placas'::text,44.640::numeric,8.00::numeric),
    ('3200600100'::text,'CHAPA PRIMER BRANCA 0,50mm'::text,'Acabamento de coluna, canto e perfil U'::text,28.800::numeric,12.00::numeric)
), aplicacao as (
  select
    cod_produt,
    round(sum(peso_pecas), 3) as peso_aplicado_kg,
    'RECONCILIADO'::text as status_dado,
    'SOMA_PESO_PECAS_ASSOCIADAS'::text as metodo_calculo
  from public.estrutura_metalica_20_componentes
  where ativo
  group by cod_produt
), calc as (
  select
    c.cod_produt,
    c.material,
    c.aplicacao_principal,
    c.peso_comprado_kg,
    a.peso_aplicado_kg,
    case when a.peso_aplicado_kg is null then null::numeric else c.peso_comprado_kg - a.peso_aplicado_kg end as saldo_kg,
    case when a.peso_aplicado_kg is null or c.peso_comprado_kg = 0 then null::numeric else (c.peso_comprado_kg - a.peso_aplicado_kg) / c.peso_comprado_kg * 100 end as percentual_saldo,
    c.custo_rs_kg,
    coalesce(a.status_dado, 'PENDENTE_APONTAMENTO') as status_dado,
    coalesce(a.metodo_calculo, 'SEM_APONTAMENTO') as metodo_calculo
  from compra c
  left join aplicacao a using (cod_produt)
)
select
  cod_produt,
  material,
  aplicacao_principal,
  round(peso_comprado_kg, 3) as peso_comprado_kg,
  round(peso_aplicado_kg, 3) as peso_aplicado_kg,
  round(saldo_kg, 3) as saldo_kg,
  round(percentual_saldo, 2) as percentual_saldo,
  custo_rs_kg,
  case when saldo_kg is null then null::numeric else round(saldo_kg * custo_rs_kg, 2) end as impacto_rs,
  case
    when status_dado <> 'RECONCILIADO' then 'PENDENTE / PARCIAL'
    when saldo_kg < 0 then 'DIVERGÊNCIA / INSUFICIÊNCIA'
    when saldo_kg = 0 then 'SEM SALDO'
    when percentual_saldo >= 30 then 'SOBRA ALTA'
    when percentual_saldo >= 10 then 'SOBRA RELEVANTE'
    else 'SOBRA'
  end as classificacao,
  status_dado,
  metodo_calculo,
  status_dado = 'RECONCILIADO' and saldo_kg > 0 as elegivel_perda,
  case when status_dado = 'RECONCILIADO' and saldo_kg > 0 then round(saldo_kg * custo_rs_kg, 2) else null::numeric end as impacto_validado_rs
from calc
order by cod_produt;

insert into public.lista_mae (
  cod_item, cod_produt, descricao_oficial, aplicacao, un, valor_unitario,
  curva, modelos_aplicaveis, ativo, obrigatoriedade, updated_at
)
values (
  'PERDA-EST-MET', null,
  'Perda de matéria-prima da estrutura metálica 20 pés',
  'Perda/aproveitamento de aço no corte e fabricação',
  '%', 872.90, 'A', 'M01', true, 'P', now()
)
on conflict (cod_item) do update set
  descricao_oficial = excluded.descricao_oficial,
  aplicacao = excluded.aplicacao,
  un = excluded.un,
  valor_unitario = excluded.valor_unitario,
  curva = excluded.curva,
  modelos_aplicaveis = excluded.modelos_aplicaveis,
  ativo = true,
  obrigatoriedade = excluded.obrigatoriedade,
  updated_at = now();

with alvo as (
  select lm.id as lista_mae_id, k.id as kit_id
  from public.lista_mae lm
  cross join public.kits k
  where lm.cod_item = 'PERDA-EST-MET'
    and k.codigo = 'KIT-M01'
), atualiza as (
  update public.kit_itens ki
  set
    lista_mae_id = a.lista_mae_id,
    cod_item = 'PERDA-EST-MET',
    cod_produt = null,
    descricao_oficial = 'Perda de matéria-prima da estrutura metálica 20 pés',
    un = '%',
    quantidade = 15.05,
    qtd_uni = 15.05,
    quant_total = 15.05,
    valor_unitario = 872.90,
    valor_total = 872.90,
    curva = 'A',
    obrigatoriedade = 'P',
    instalacao = 'Estrutura',
    fonte = 'forge_mlt_m01_estrutura_metalica_2026_10_16',
    observacao = '98,195 kg de diferenças positivas sobre 652,530 kg comprados = 15,05%; impacto financeiro calculado = R$ 872,90. Diferenças negativas de UDC 5 e UDC 6 permanecem divergências e não compensam a perda bruta.',
    vinculo_status = 'VALIDADO',
    vinculo_confianca = 1.0,
    vinculo_observacao = 'Fonte validada pelo usuário e promovida a partir do Forge MLT.M01.',
    elo_situacao = 'VALIDADO',
    elo_confianca = 1.0,
    elo_justificativa = 'Perda calculada por associação peça → matéria-prima → soma de peso utilizado → saldo positivo por material.',
    elo_referencia = 'FORGE:MLT.M01:PERDA-EST-MET:2026-10-16',
    snapshot_origem = 'forge_mlt_m01_estrutura_metalica_2026_10_16',
    snapshot_at = now(),
    vinculo_at = now(),
    ativo = true
  from alvo a
  where ki.kit_id = a.kit_id and ki.cod_item = 'PERDA-EST-MET'
  returning ki.id
)
insert into public.kit_itens (
  id, kit_id, lista_mae_id, cod_item, cod_produt, descricao_oficial,
  un, quantidade, qtd_uni, quant_total, valor_unitario, valor_total,
  curva, obrigatoriedade, instalacao, fonte, ordem, observacao,
  vinculo_status, vinculo_confianca, vinculo_observacao,
  elo_situacao, elo_confianca, elo_justificativa, elo_referencia,
  snapshot_origem, snapshot_at, vinculo_at, ativo
)
select
  gen_random_uuid(), a.kit_id, a.lista_mae_id, 'PERDA-EST-MET', null,
  'Perda de matéria-prima da estrutura metálica 20 pés',
  '%', 15.05, 15.05, 15.05, 872.90, 872.90,
  'A', 'P', 'Estrutura', 'forge_mlt_m01_estrutura_metalica_2026_10_16', 41,
  '98,195 kg de diferenças positivas sobre 652,530 kg comprados = 15,05%; impacto financeiro calculado = R$ 872,90. Diferenças negativas de UDC 5 e UDC 6 permanecem divergências e não compensam a perda bruta.',
  'VALIDADO', 1.0, 'Fonte validada pelo usuário e promovida a partir do Forge MLT.M01.',
  'VALIDADO', 1.0, 'Perda calculada por associação peça → matéria-prima → soma de peso utilizado → saldo positivo por material.',
  'FORGE:MLT.M01:PERDA-EST-MET:2026-10-16',
  'forge_mlt_m01_estrutura_metalica_2026_10_16', now(), now(), true
from alvo a
where not exists (select 1 from atualiza)
  and not exists (
    select 1 from public.kit_itens ki
    where ki.kit_id = a.kit_id and ki.cod_item = 'PERDA-EST-MET'
  );