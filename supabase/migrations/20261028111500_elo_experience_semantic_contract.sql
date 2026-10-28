-- ELO experience semantic consolidation, phase 1.
-- Unifies shared level identity/order while preserving conflicting transition
-- thresholds as an explicit governed dual-state. No destructive migration.

create schema if not exists elo_learning;

create or replace view elo_learning.vw_experience_level_contract
with (security_invoker = true)
as
select
  pt.codigo as level_code,
  pt.ordem as level_order,
  pt.nome as level_name,
  pt.descricao as description,
  pt.ativo as active,
  en.autonomy_mode,
  case
    when en.level_code is null then 'PT_ONLY'
    when en.level_order <> pt.ordem then 'ORDER_CONFLICT'
    else 'UNIFIED'
  end as semantic_status,
  'elo_experiencia_niveis'::text as canonical_level_owner,
  'elo_experience_levels'::text as compatibility_level_owner
from public.elo_experiencia_niveis pt
left join public.elo_experience_levels en
  on en.level_code = pt.codigo;

create or replace view elo_learning.vw_experience_transition_contract
with (security_invoker = true)
as
select
  pt.nivel_origem as from_level,
  pt.nivel_destino as to_level,
  pt.experiencias_minimas as learning_min_validated_experiences,
  pt.confianca_minima as learning_min_confidence,
  pt.profundidade_minima as learning_min_domain_depth,
  pt.decisoes_independentes_minimas as learning_required_independent_decisions,
  pt.ativa as learning_active,
  en.min_validated_experiences as legacy_min_validated_experiences,
  en.min_confidence as legacy_min_confidence,
  en.min_domain_depth as legacy_min_domain_depth,
  en.required_independent_decisions as legacy_required_independent_decisions,
  en.enabled as legacy_enabled,
  case
    when en.from_level is null then 'PT_ONLY'
    when en.min_validated_experiences = pt.experiencias_minimas
     and en.min_confidence = pt.confianca_minima
     and en.min_domain_depth = pt.profundidade_minima
     and en.required_independent_decisions = pt.decisoes_independentes_minimas
      then 'MATCH'
    else 'GOVERNED_CONFLICT'
  end as semantic_status,
  false as canonical_promotion_authority,
  'Symbiont -> Evolution Gate -> Governed Learning -> required approval'::text as promotion_authority
from public.elo_experiencia_transicoes pt
left join public.elo_experience_level_transitions en
  on en.from_level = pt.nivel_origem
 and en.to_level = pt.nivel_destino;

create or replace function public.elo_level_order(p_level text)
returns integer
language sql
stable
set search_path to 'elo_learning', 'public', 'pg_catalog'
as $function$
  select level_order
  from elo_learning.vw_experience_level_contract
  where level_code = p_level
    and active;
$function$;

comment on view elo_learning.vw_experience_level_contract is
  'Canonical read contract for shared ELO experience level semantics. Portuguese learning taxonomy owns level identity/order; English family remains compatibility metadata during migration.';
comment on view elo_learning.vw_experience_transition_contract is
  'Governed comparison contract for conflicting transition thresholds. Explicitly non-authoritative for promotion.';
