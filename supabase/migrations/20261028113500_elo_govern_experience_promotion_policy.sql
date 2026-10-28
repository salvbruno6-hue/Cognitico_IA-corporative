-- ELO experience semantic consolidation, phase 2.
-- Removes silent promotion authority from either physical threshold table.
-- Promotion is permitted only when the PT and EN transition contracts agree.

create or replace view elo_learning.vw_experience_promotion_policy
with (security_invoker = true)
as
select
  from_level,
  to_level,
  semantic_status,
  case
    when semantic_status = 'MATCH'
     and learning_active
     and coalesce(legacy_enabled, false)
      then 'READY'
    else 'GOVERNANCE_REQUIRED'
  end as policy_status,
  case when semantic_status = 'MATCH' then learning_min_validated_experiences end as min_validated_experiences,
  case when semantic_status = 'MATCH' then learning_min_confidence end as min_confidence,
  case when semantic_status = 'MATCH' then learning_min_domain_depth end as min_domain_depth,
  case when semantic_status = 'MATCH' then learning_required_independent_decisions end as required_independent_decisions,
  learning_min_validated_experiences,
  learning_min_confidence,
  learning_min_domain_depth,
  learning_required_independent_decisions,
  legacy_min_validated_experiences,
  legacy_min_confidence,
  legacy_min_domain_depth,
  legacy_required_independent_decisions,
  false as autonomous_threshold_selection,
  case
    when semantic_status = 'MATCH' then true
    else false
  end as canonical_promotion_authority
from elo_learning.vw_experience_transition_contract;

comment on view elo_learning.vw_experience_promotion_policy is
  'Canonical governed promotion policy. A transition is READY only when the PT and EN threshold contracts match; conflicts fail closed and require governance.';

create or replace function public.elo_refresh_learner_profile(p_learner_id uuid)
returns jsonb
language plpgsql
security definer
set search_path to 'elo_learning', 'public', 'pg_catalog'
as $function$
declare
  p public.elo_learner_profiles%rowtype;
  v_next_level text;
  policy record;
begin
  select * into p
  from public.elo_learner_profiles
  where id = p_learner_id;

  if not found then
    raise exception 'learner not found';
  end if;

  select level_code into v_next_level
  from elo_learning.vw_experience_level_contract
  where active
    and level_order > public.elo_level_order(p.current_level)
  order by level_order
  limit 1;

  if v_next_level is null then
    return jsonb_build_object(
      'status', 'AT_MAXIMUM_LEVEL',
      'level', p.current_level
    );
  end if;

  select * into policy
  from elo_learning.vw_experience_promotion_policy
  where from_level = p.current_level
    and to_level = v_next_level;

  if not found then
    return jsonb_build_object(
      'status', 'GOVERNANCE_REQUIRED',
      'reason', 'MISSING_PROMOTION_POLICY',
      'from_level', p.current_level,
      'to_level', v_next_level,
      'mutated', false
    );
  end if;

  if policy.policy_status <> 'READY' then
    return jsonb_build_object(
      'status', 'GOVERNANCE_REQUIRED',
      'reason', policy.semantic_status,
      'from_level', p.current_level,
      'to_level', v_next_level,
      'learning_thresholds', jsonb_build_object(
        'validated_experiences', policy.learning_min_validated_experiences,
        'confidence', policy.learning_min_confidence,
        'domain_depth', policy.learning_min_domain_depth,
        'independent_decisions', policy.learning_required_independent_decisions
      ),
      'legacy_thresholds', jsonb_build_object(
        'validated_experiences', policy.legacy_min_validated_experiences,
        'confidence', policy.legacy_min_confidence,
        'domain_depth', policy.legacy_min_domain_depth,
        'independent_decisions', policy.legacy_required_independent_decisions
      ),
      'mutated', false
    );
  end if;

  if p.validated_experiences >= policy.min_validated_experiences
     and p.confidence >= policy.min_confidence
     and p.domain_depth >= policy.min_domain_depth
     and p.independent_decisions >= policy.required_independent_decisions then
    update public.elo_learner_profiles
    set current_level = policy.to_level,
        updated_at = now()
    where id = p.id;

    insert into public.elo_evolution_events(
      event_type, from_level, to_level, evidence, decision_reason, confidence
    ) values (
      'LEVEL_REVIEW',
      p.current_level,
      policy.to_level,
      jsonb_build_array('validated_experiences','confidence','domain_depth','independent_decisions'),
      'governed canonical transition policy met',
      p.confidence
    );

    return jsonb_build_object(
      'status', 'ADVANCED',
      'from_level', p.current_level,
      'to_level', policy.to_level,
      'policy_status', policy.policy_status
    );
  end if;

  return jsonb_build_object(
    'status', 'HELD',
    'current_level', p.current_level,
    'required_level', policy.to_level,
    'required_experiences', policy.min_validated_experiences,
    'required_confidence', policy.min_confidence,
    'required_domain_depth', policy.min_domain_depth,
    'required_independent_decisions', policy.required_independent_decisions,
    'policy_status', policy.policy_status
  );
end;
$function$;
