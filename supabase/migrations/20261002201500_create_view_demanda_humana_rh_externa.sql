-- Consolidação para consumo do RH.
-- Mede demanda humana diária por função nas operações externas.
-- Não representa disponibilidade, jornada, escala ou GAP de RH.

create view public.v_elo_pcp_demanda_humana_rh_externa
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
)
select
  d.data_referencia,
  d.funcao_montagem_id,
  f.codigo as funcao_codigo,
  f.nome as funcao_nome,
  count(distinct d.pessoa_id)::bigint as demanda_colaboradores,
  count(distinct d.ordem_montagem_externa_id)::bigint as ordens_com_demanda,
  sum(d.horas_planejadas_dia)::numeric as horas_demanda_dia
from dias d
left join public.mt_funcoes_montagem f
  on f.id = d.funcao_montagem_id
group by
  d.data_referencia,
  d.funcao_montagem_id,
  f.codigo,
  f.nome;
