-- MLT.M01 — perda por associação direta do peso das peças à matéria-prima.
-- Regra validada pelo analista: somar PESO PEÇAS por COD_PRODUT e calcular
-- peso_comprado - peso_utilizado = diferença.
-- Saldos negativos são divergência de apontamento, nunca perda negativa.
-- BOM não é alterada.

-- A planilha informa 109,95 kg para o conjunto de 4 colunas. O cadastro interno
-- divide esse conjunto em duas linhas simétricas; preservamos metade exata do total
-- em cada linha para que a soma retorne ao valor-fonte.
update public.estrutura_metalica_20_componentes
set peso_pecas = 54.975,
    updated_at = now()
where item in ('COL01','COL02')
  and cod_produt = '3200600075';

create or replace view public.vw_perda_estrutura_metalica_20
with (security_invoker = true)
as
with compra (
  cod_produt,
  material,
  aplicacao_principal,
  peso_comprado_kg,
  custo_rs_kg
) as (
  values
    ('3200600291'::text, 'PERFIL UDC ENRIJ 3" X 2,00MM (75ABA40X15) - 6m'::text, 'Travessa de fixação de telha'::text, 47.754::numeric, 8.12::numeric),
    ('3200600289'::text, 'PERFIL UDC ENRIJ 5" X 2,65MM (127ABA50X17) - 6m'::text, 'Longarina frontal inferior, travessas e reforços internos do assoalho'::text, 116.100::numeric, 8.12::numeric),
    ('3200600288'::text, 'PERFIL UDC ENRIJ 6" X 2,65MM (150ABA60X17) - 6m'::text, 'Longarinas laterais inferiores'::text, 72.000::numeric, 8.12::numeric),
    ('3200600335'::text, 'PERFIL UDC ENRIJ 8" X 2,00MM (200ABA75X20) - 6m'::text, 'Longarinas superiores'::text, 108.510::numeric, 8.12::numeric),
    ('3200600075'::text, 'Chapa 12 Galvanizada 2850X1200x2,70mm'::text, 'Colunas, suportes e perfis Z estruturais'::text, 147.744::numeric, 7.78::numeric),
    ('3200600239'::text, 'Chapa 14 Galvanizada 1200X3000x1,95mm'::text, 'Perfis T / limitadores do assoalho'::text, 56.160::numeric, 8.78::numeric),
    ('3200600260'::text, 'Chapa 1/4 (6,35) preta 1200x3000mm'::text, 'Suportes de içamento e conectores'::text, 27.942::numeric, 6.00::numeric),
    ('3200600124'::text, 'Chapa 26 0,5 primer stucco 1200X3000x0,5mm'::text, 'Perfil / acabamento de forro do teto'::text, 2.880::numeric, 21.21::numeric),
    ('3200600065'::text, 'Chapa 16 / 1,55mm 1200x3000x1,55mm'::text, 'Perfis Z externos de fixação / travamento das placas'::text, 44.640::numeric, 8.00::numeric),
    ('3200600100'::text, 'CHAPA PRIMER BRANCA 0,50mm'::text, 'Acabamento de coluna, canto e perfil U'::text, 28.800::numeric, 12.00::numeric)
),
aplicacao as (
  select
    cod_produt,
    round(sum(peso_pecas), 3) as peso_aplicado_kg,
    case when cod_produt = '3200600100' then 'PARCIAL'::text else 'RECONCILIADO'::text end as status_dado,
    'SOMA_PESO_PECAS_ASSOCIADAS'::text as metodo_calculo
  from public.estrutura_metalica_20_componentes
  where ativo
  group by cod_produt
),
calc as (
  select
    c.cod_produt,
    c.material,
    c.aplicacao_principal,
    c.peso_comprado_kg,
    a.peso_aplicado_kg,
    case when a.peso_aplicado_kg is null then null::numeric else c.peso_comprado_kg - a.peso_aplicado_kg end as saldo_kg,
    case
      when a.peso_aplicado_kg is null or c.peso_comprado_kg = 0 then null::numeric
      else ((c.peso_comprado_kg - a.peso_aplicado_kg) / c.peso_comprado_kg) * 100::numeric
    end as percentual_saldo,
    c.custo_rs_kg,
    coalesce(a.status_dado, 'PENDENTE_APONTAMENTO'::text) as status_dado,
    coalesce(a.metodo_calculo, 'SEM_APONTAMENTO'::text) as metodo_calculo
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
    when status_dado <> 'RECONCILIADO' then 'PENDENTE / PARCIAL'::text
    when saldo_kg < 0 then 'DIVERGÊNCIA / INSUFICIÊNCIA'::text
    when saldo_kg = 0 then 'SEM SALDO'::text
    when percentual_saldo >= 30 then 'SOBRA ALTA'::text
    when percentual_saldo >= 10 then 'SOBRA RELEVANTE'::text
    else 'SOBRA'::text
  end as classificacao,
  status_dado,
  metodo_calculo,
  (status_dado = 'RECONCILIADO' and saldo_kg > 0) as elegivel_perda,
  case
    when status_dado = 'RECONCILIADO' and saldo_kg > 0 then round(saldo_kg * custo_rs_kg, 2)
    else null::numeric
  end as impacto_validado_rs
from calc
order by cod_produt;

comment on view public.vw_perda_estrutura_metalica_20 is
'MLT.M01 — perda por associação direta das peças à matéria-prima: peso comprado - soma do PESO PEÇAS associado ao COD_PRODUT. Saldo negativo é divergência, não perda. 3200600100 permanece PARCIAL. Não altera BOM.';
