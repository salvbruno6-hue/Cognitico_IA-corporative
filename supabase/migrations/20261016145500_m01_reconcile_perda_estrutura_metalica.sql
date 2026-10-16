-- MLT.M01 — reconciliação da perda de matéria-prima da estrutura metálica.
-- Fonte: tabelas de compra e peças fornecidas/validadas pelo analista em 2026-10-16.
-- Escopo: estrutura metálica. Não altera BOM nem promove PERDA-EST-MET.
--
-- Regras:
-- 1. Compra considera 10 COD_PRODUTO e 652,530 kg em precisão de cálculo
--    (652,5 kg no consolidado arredondado informado pelo analista).
-- 2. Perfis UDC usam como autoridade de massa o peso da barra comprada de 6 m;
--    o peso aplicado é normalizado por comprimento efetivamente utilizado.
-- 3. Ausência ou incompletude de apontamento não é convertida em perda validada.
-- 4. 3200600100 permanece PARCIAL: há 10,03 kg comprovados de acabamento de coluna,
--    mas a compra também referencia acabamentos de canto/perfil U ainda não integralmente apontados.
-- 5. Saldos negativos, se surgirem em futuras revisões, são divergência e não perda.

-- Correção de evidência já identificada na tabela de componentes:
-- o perfil de telha UDC 3" possui 2 peças, não 7.
update public.estrutura_metalica_20_componentes
set quantidade = 2,
    peso_unitario = 6.44,
    peso_pecas = 12.88,
    rs_kg_peca = 8.12,
    valor_unitario_peca = 52.29,
    valor_pecas = 104.58,
    updated_at = now()
where item = 'PRTH01'
  and cod_produt = '3200600291';

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
aplicacao (
  cod_produt,
  peso_aplicado_kg,
  status_dado,
  metodo_calculo
) as (
  values
    -- UDC 3": (15,918 kg / 6 m) * (2 * 2,43 m)
    ('3200600291'::text, ((15.918::numeric / 6::numeric) * (2::numeric * 2.43::numeric)), 'RECONCILIADO'::text, 'PESO_BARRA_6M_X_COMPRIMENTO_APLICADO'::text),
    -- UDC 5": (25,8 / 6) * [(2*2,44)+(4*2,435)+(8*1,15)+(2*1,18)]
    ('3200600289'::text, ((25.8::numeric / 6::numeric) * ((2::numeric * 2.44::numeric) + (4::numeric * 2.435::numeric) + (8::numeric * 1.15::numeric) + (2::numeric * 1.18::numeric))), 'RECONCILIADO'::text, 'PESO_BARRA_6M_X_COMPRIMENTO_APLICADO'::text),
    -- UDC 6": (36 / 6) * (2 * 6 m)
    ('3200600288'::text, ((36::numeric / 6::numeric) * (2::numeric * 6::numeric)), 'RECONCILIADO'::text, 'PESO_BARRA_6M_X_COMPRIMENTO_APLICADO'::text),
    -- UDC 8": (36,17 / 6) * [(2*6)+(2*2,44)]
    ('3200600335'::text, ((36.17::numeric / 6::numeric) * ((2::numeric * 6::numeric) + (2::numeric * 2.44::numeric))), 'RECONCILIADO'::text, 'PESO_BARRA_6M_X_COMPRIMENTO_APLICADO'::text),
    -- Chapa 2,70: coluna 109,95 + suporte 1,52 + perfis Z 21,93 + 8,13
    ('3200600075'::text, (109.95::numeric + 1.52::numeric + 21.93::numeric + 8.13::numeric), 'RECONCILIADO'::text, 'SOMA_PESOS_PECAS'::text),
    -- Chapa 1,95: perfis T 21,19 + 7,86
    ('3200600239'::text, (21.19::numeric + 7.86::numeric), 'RECONCILIADO'::text, 'SOMA_PESOS_PECAS'::text),
    -- Chapa 6,35: conectores/triângulo = 18,82 kg
    ('3200600260'::text, 18.82::numeric, 'RECONCILIADO'::text, 'SOMA_PESOS_PECAS'::text),
    -- Chapa primer stucco 0,50: acabamento de teto confirmado = 2,25 kg
    ('3200600124'::text, 2.25::numeric, 'RECONCILIADO'::text, 'PESO_PECA_CONFIRMADO'::text),
    -- Chapa 1,55: 4 perfis 74x2080 + 8 perfis 74x2820; densidade derivada da compra = 44,64/3,60 = 12,4 kg/m²
    ('3200600065'::text, ((((0.074::numeric * 2.080::numeric) * 4::numeric) + ((0.074::numeric * 2.820::numeric) * 8::numeric)) * (44.64::numeric / (1.2::numeric * 3.0::numeric))), 'RECONCILIADO'::text, 'AREA_PECAS_X_KG_M2_DERIVADO_COMPRA'::text),
    -- Chapa primer branca: somente acabamento de coluna comprovado; canto/perfil U seguem pendentes.
    ('3200600100'::text, 10.03::numeric, 'PARCIAL'::text, 'APONTAMENTO_PARCIAL_PESO_PECA'::text)
),
calc as (
  select
    c.cod_produt,
    c.material,
    c.aplicacao_principal,
    c.peso_comprado_kg,
    a.peso_aplicado_kg,
    (c.peso_comprado_kg - a.peso_aplicado_kg) as saldo_kg,
    case
      when c.peso_comprado_kg = 0 then null::numeric
      else ((c.peso_comprado_kg - a.peso_aplicado_kg) / c.peso_comprado_kg) * 100::numeric
    end as percentual_saldo,
    c.custo_rs_kg,
    a.status_dado,
    a.metodo_calculo
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
  round(saldo_kg * custo_rs_kg, 2) as impacto_rs,
  case
    when status_dado is distinct from 'RECONCILIADO' then 'PENDENTE / PARCIAL'::text
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
    when status_dado = 'RECONCILIADO' and saldo_kg > 0
      then round(saldo_kg * custo_rs_kg, 2)
    else null::numeric
  end as impacto_validado_rs
from calc
order by cod_produt;

comment on view public.vw_perda_estrutura_metalica_20 is
'MLT.M01 — reconciliação de 10 matérias-primas da estrutura metálica. Mantém saldo potencial visível, mas somente status RECONCILIADO com saldo positivo é elegível para perda validada. 3200600100 permanece PARCIAL até completar apontamento de canto/perfil U. Não altera BOM.';
