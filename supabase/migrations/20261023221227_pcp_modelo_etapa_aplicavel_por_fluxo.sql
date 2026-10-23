create or replace view public.v_elo_pcp_modelo_etapa_aplicavel
with (security_invoker = true)
as
with fluxo_padrao as (
  select f.id, f.codigo
  from public.fluxo_produtivo_modular f
  where f.ativo is true
    and f.modelo_id is null
    and f.codigo = 'MLT.PROD.PADRAO.V2'
  limit 1
), fluxo_especifico as (
  select distinct on (f.modelo_id)
    f.modelo_id,
    f.id,
    f.codigo
  from public.fluxo_produtivo_modular f
  where f.ativo is true
    and f.modelo_id is not null
  order by f.modelo_id, f.updated_at desc, f.created_at desc
), modelos_ativos as (
  select
    m.id as modelo_id,
    m.codigo as modelo_codigo_canonico,
    case
      when upper(m.codigo) like 'MLT.M%' then substring(upper(m.codigo) from 5)
      else upper(m.codigo)
    end as modelo_codigo
  from public.modelos m
  where m.ativo is true
), fluxo_resolvido as (
  select
    m.modelo_id,
    m.modelo_codigo_canonico,
    m.modelo_codigo,
    coalesce(fe.id, fp.id) as fluxo_id,
    coalesce(fe.codigo, fp.codigo) as fluxo_codigo,
    (fe.id is not null) as fluxo_especifico
  from modelos_ativos m
  left join fluxo_especifico fe on fe.modelo_id = m.modelo_id
  cross join fluxo_padrao fp
)
select
  fr.modelo_id,
  fr.modelo_codigo_canonico,
  fr.modelo_codigo,
  fr.fluxo_codigo,
  fr.fluxo_especifico,
  e.ordem,
  upper(e.codigo_etapa) as codigo_etapa,
  e.nome as etapa_nome,
  true as etapa_aplicavel
from fluxo_resolvido fr
join public.fluxo_produtivo_modular_etapas e
  on e.fluxo_id = fr.fluxo_id
 and e.status = 'ATIVO';
