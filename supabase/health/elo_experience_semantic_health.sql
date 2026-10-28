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
    bool_or(canonical_promotion_authority) as any_direct_authority
  from elo_learning.vw_experience_transition_contract
)
select
  'EXPERIENCE_LEVEL_SEMANTICS'::text as area,
  case when divergent = 0 and total > 0 then 'HEALTHY' else 'REVIEW' end as status,
  format('levels=%s unified=%s divergent=%s', total, unified, divergent) as evidence,
  case when divergent = 0 then 'shared identity/order consolidated' else 'reconcile level identity/order before migration' end as next_action
from levels
union all
select
  'EXPERIENCE_TRANSITION_POLICY',
  case
    when any_direct_authority then 'BLOCK'
    when conflicts > 0 then 'GOVERNED_CONFLICT'
    else 'HEALTHY'
  end,
  format('transitions=%s matched=%s conflicts=%s direct_authority=%s', total, matched, conflicts, coalesce(any_direct_authority,false)),
  case
    when any_direct_authority then 'remove direct table authority; restore governed promotion path'
    when conflicts > 0 then 'choose or derive threshold policy through governed evidence before migrating promotion runtime'
    else 'migrate remaining consumers behind canonical contract'
  end
from transitions;
