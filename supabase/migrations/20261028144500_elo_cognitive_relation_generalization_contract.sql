-- ELO cognitive relation generalization contract.
-- Computes readiness evidence from existing governed learning relations and
-- validated/incorporated learning experiences. It creates no new evidence owner
-- and performs no canonical promotion.

create schema if not exists elo_learning;

create or replace view elo_learning.vw_cognitive_relation_generalization
with (security_invoker = true)
as
with relation_codes as (
  select
    r.id as relation_id,
    r.tipo_relacao as relation_type,
    r.status as relation_status,
    r.ativo as relation_active,
    r.confianca as relation_confidence,
    coalesce(source_concept.codigo, source_pattern.codigo) as source_code,
    coalesce(target_concept.codigo, target_pattern.codigo) as target_code
  from public.elo_aprendizado_relacoes r
  left join public.elo_aprendizado_conceitos source_concept
    on r.origem_tipo = 'conceito' and source_concept.id = r.origem_id
  left join public.elo_aprendizado_padroes_raciocinio source_pattern
    on r.origem_tipo = 'padrao_raciocinio' and source_pattern.id = r.origem_id
  left join public.elo_aprendizado_conceitos target_concept
    on r.destino_tipo = 'conceito' and target_concept.id = r.destino_id
  left join public.elo_aprendizado_padroes_raciocinio target_pattern
    on r.destino_tipo = 'padrao_raciocinio' and target_pattern.id = r.destino_id
),
validated_evidence as (
  select
    rc.relation_id,
    e.id as experience_id,
    e.origem_referencia as source_reference,
    e.status_validacao as validation_status
  from relation_codes rc
  join public.elo_aprendizado_experiencias e
    on e.status_validacao in ('VALIDADA', 'INCORPORADA')
  where rc.relation_active
    and rc.source_code is not null
    and rc.target_code is not null
    and e.origem_referencia is not null
    and exists (
      select 1
      from jsonb_path_query(
        coalesce(e.conhecimentos_utilizados, 'null'::jsonb),
        '$.** ? (@.type() == "string")'
      ) as source_value(value)
      where source_value.value #>> '{}' = rc.source_code
    )
    and exists (
      select 1
      from jsonb_path_query(
        coalesce(e.conhecimentos_utilizados, 'null'::jsonb),
        '$.** ? (@.type() == "string")'
      ) as target_value(value)
      where target_value.value #>> '{}' = rc.target_code
    )
),
aggregated as (
  select
    rc.relation_id,
    rc.relation_type,
    rc.relation_status,
    rc.relation_active,
    rc.relation_confidence,
    rc.source_code,
    rc.target_code,
    count(distinct ve.source_reference) as independent_validated_contexts,
    count(distinct ve.experience_id) as supporting_validated_experiences,
    coalesce(
      array_agg(distinct ve.source_reference) filter (where ve.source_reference is not null),
      array[]::text[]
    ) as supporting_source_references
  from relation_codes rc
  left join validated_evidence ve on ve.relation_id = rc.relation_id
  group by
    rc.relation_id,
    rc.relation_type,
    rc.relation_status,
    rc.relation_active,
    rc.relation_confidence,
    rc.source_code,
    rc.target_code
)
select
  relation_id,
  relation_type,
  relation_status,
  relation_active,
  relation_confidence,
  source_code,
  target_code,
  independent_validated_contexts,
  supporting_validated_experiences,
  supporting_source_references,
  case
    when not relation_active then 'BLOCK'
    when source_code is null or target_code is null then 'BLOCK'
    when independent_validated_contexts >= 2 then 'CONFIRMED'
    when independent_validated_contexts = 1 then 'PARTIAL'
    else 'UNCONFIRMED'
  end as generalization_status,
  case
    when not relation_active then 'BLOCK'
    when source_code is null or target_code is null then 'BLOCK'
    when independent_validated_contexts >= 2 then 'READY_FOR_SYMBIONT_REVIEW'
    else 'STRENGTHEN'
  end as readiness_status,
  false as canonical_mutation_allowed
from aggregated;

comment on view elo_learning.vw_cognitive_relation_generalization is
  'Fail-closed generalization contract for cognitive relation candidates. CONFIRMED requires at least two distinct validated/incorporated source contexts explicitly referencing both relation endpoint codes. The view never promotes or mutates canonical relations.';
