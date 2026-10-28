# ELO — Dual Experience Architecture Reconciliation — 2026-10-28

## Classification

Status: `GOVERNED_CONFLICT / NO_DESTRUCTIVE_MIGRATION_YET`

This audit reconciles two live experience/learning structures that share the same five level codes but do not express the same transition thresholds.

## Provenance

Supabase migration history proves two independently created families:

1. `20260913230800 elo_cognitive_experience_architecture_v1`
   - `elo_experience_levels`
   - `elo_experience_level_transitions`
   - `elo_experience_records`
   - `elo_reasoning_patterns`
   - `elo_specializations`
   - runtime functions/views for guidance, readiness and evolution.
2. `20260913232015 elo_aprendizado_levels_patterns_and_specializations`
   - `elo_experiencia_niveis`
   - `elo_experiencia_transicoes`
   - `elo_aprendizado_padroes_raciocinio`
   - enrichment of `elo_aprendizado_especializacoes`.

The Portuguese learning family is referenced by several later learning/extraction/writer migrations. The English v1 family remains referenced by live runtime functions and views, including `elo_level_order`, `elo_build_guidance_plan`, `elo_refresh_learner_profile`, `elo_specialization_readiness` and `elo_cognitive_architecture_map`.

Therefore the structures are not safe to collapse by table name alone.

## Material conflict

Both transition tables use the same semantic level codes, but all four adjacent transition thresholds differ in at least one material criterion.

Examples observed live:

- `iniciante -> aprendiz_orientado`: v1 requires 2 validated experiences / 0.70 confidence; learning taxonomy requires 3 / 0.70.
- `aprendiz_orientado -> intermediario`: v1 requires 4 / 0.75; learning taxonomy requires 5 / 0.78.
- `intermediario -> experiente`: v1 requires 6 / 0.80; learning taxonomy requires 8 / 0.85.
- `experiente -> especialista`: v1 requires 10 / 0.90; learning taxonomy requires 12 / 0.90.

This is a semantic conflict, not an exact duplicate.

## Authority boundary

Until consumer migration is complete:

- neither transition table may be treated as an automatic canonical promotion authority;
- canonical learning/promotion continues through the governed code path: Symbiont -> Evolution Gate -> Governed Learning -> required human approval;
- the English family remains a legacy runtime experience/guidance subsystem;
- the Portuguese family remains the later learning taxonomy/writer subsystem;
- no row, function, view or table is dropped by this reconciliation;
- new functionality must not introduce a third level/transition owner.

## Consolidation path

1. inventory every runtime/database consumer of both families;
2. define a single governed transition-threshold contract;
3. migrate consumers behind that contract;
4. prove behavioral equivalence or deliberate threshold change;
5. only then deprecate the superseded physical tables/functions;
6. run Evolution Gate and post-production regression before removal.

The ELO intuitive health summary reports this state as `COGNITIVE_EXPERIENCE_MODEL = CONFLICT` while the live threshold mismatch remains.
