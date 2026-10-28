-- ELO experience semantic health probe.
-- Reports separately the shared level semantics and the still-governed
-- transition threshold conflict.

with levels as (
  select
    count(*) as total,
    count(*) filter (where semantic_status = 'UNIFIED') as unified,
    count(*) filter (where semantic_status <> 'UNIFIED') as divergent
  from elo_learning.vw_experience_level_contract
),
transitions as (
  select
    count(*) as total,
    count(*) filter (where semantic_status = 'MATCH') as matched,
    count(*) filter (where semantic_status = 'GOVERNED_CONFLICT') as conflicts,
    count(*) filter (where semantic_status = 'PT_ONLY') as missing_counterparts,
    bool_or(canonical_promotion_authority) as any_direct_authority
  from elo_learning.vw_experience_transition_contract
)
select
  'EXPERIENCE_LEVEL_SEMANTICS'::text as area,
  case when divergent = 0 and total > 0 then 'HEALTHY' else 'REVIEW' end as status,
  format('levels=%s unified=%s divergent=%s', total, unified, divergent) as evidence,
  case when divergent = 0 and total > 0 then 'shared identity/order consolidated' else 'reconcile level identity/order before migration' end as next_action
from levels
union all
select
  'EXPERIENCE_TRANSITION_POLICY',
  case
    when coalesce(any_direct_authority,false) then 'BLOCK'
    when total = 0 or missing_counterparts > 0 then 'REVIEW'
    when conflicts > 0 then 'GOVERNED_CONFLICT'
    when matched = total then 'HEALTHY'
    else 'REVIEW'
  end,
  format(
    'transitions=%s matched=%s conflicts=%s missing_counterparts=%s direct_authority=%s',
    total, matched, conflicts, missing_counterparts, coalesce(any_direct_authority,false)
  ),
  case
    when coalesce(any_direct_authority,false) then 'remove direct table authority; restore governed promotion path'
    when total = 0 then 'restore transition evidence before any consumer migration'
    when missing_counterparts > 0 then 'reconcile missing transition counterparts before choosing threshold policy'
    when conflicts > 0 then 'choose or derive threshold policy through governed evidence before migrating promotion runtime'
    when matched = total then 'migrate remaining consumers behind canonical contract'
    else 'review transition contract completeness'
  end
from transitions;
