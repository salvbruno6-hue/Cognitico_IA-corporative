-- Indicador de demanda humana para operações externas.
-- Escopo: necessidade planejada de mão de obra por dia, ordem e função.
-- Não representa disponibilidade, jornada, escala ou GAP de RH.

create or replace view public.v_elo_pcp_demanda_humana_montagem_externa
with (security_invoker = true)
as
with base as (
  select
    e.ordem_montagem_externa_id,
    e.pessoa_id,
    e.funcao_montagem_id,
    e.inicio_planejado,
    e.fim_planejado,
    coalesce(e.horas_planejadas, 0)::numeric as horas_planejadas
  from public.mt_equipe_montagem_externa e
  where e.inicio_planejado is not null
    and e.fim_planejado is not null
    and e.fim_planejado >= e.inicio_planejado
    and coalesce(e.status, 'PLANEJADO') not in ('CANCELADO', 'CANCELADA')
),
dias as (
  select
    b.ordem_montagem_externa_id,
    b.pessoa_id,
    b.funcao_montagem_id,
    d.d::date as data_referencia,
    b.horas_planejadas /
      nullif(
        extract(epoch from (date_trunc('day', b.fim_planejado) - date_trunc('day', b.inicio_planejado))) / 86400 + 1,
        0
      ) as horas_planejadas_dia
  from base b
  cross join lateral generate_series(
    date_trunc('day', b.inicio_planejado),
    date_trunc('day', b.fim_planejado),
    '1 day'::interval
  ) d(d)
),
modulos as (
  select
    m.ordem_montagem_externa_id,
    count(*) filter (
      where coalesce(m.status, '') not in ('CANCELADO', 'CANCELADA')
    )::bigint as modulos_planejados
  from public.mt_montagem_externa_modulos m
  group by m.ordem_montagem_externa_id
)
select
  d.data_referencia,
  d.ordem_montagem_externa_id,
  o.numero_ordem,
  o.tipo_montagem,
  o.status,
  d.funcao_montagem_id,
  f.codigo as funcao_codigo,
  f.nome as funcao_nome,
  count(distinct d.pessoa_id)::bigint as colaboradores_necessarios,
  sum(d.horas_planejadas_dia)::numeric as horas_equipe_planejadas_dia,
  coalesce(m.modulos_planejados, 0)::bigint as modulos_planejados
from dias d
join public.mt_ordens_montagem_externa o
  on o.id = d.ordem_montagem_externa_id
left join public.mt_funcoes_montagem f
  on f.id = d.funcao_montagem_id
left join modulos m
  on m.ordem_montagem_externa_id = d.ordem_montagem_externa_id
group by
  d.data_referencia,
  d.ordem_montagem_externa_id,
  o.numero_ordem,
  o.tipo_montagem,
  o.status,
  d.funcao_montagem_id,
  f.codigo,
  f.nome,
  m.modulos_planejados;
