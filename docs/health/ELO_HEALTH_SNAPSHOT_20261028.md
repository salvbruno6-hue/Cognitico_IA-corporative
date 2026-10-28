# ELO Health Snapshot — 2026-10-28

## Scope

Live read-only reconciliation of GitHub `main` and Supabase `Elo-forge` covering architecture, integration, database integrity, duplication, capabilities, relations and Objective Continuity.

## Executive state

| Area | State | Evidence |
|---|---|---|
| GitHub / deploy | HEALTHY | `main` at `f97ed82b5c0e4c95a0c4b5d66d36914b674a0bdc`; Vercel `elo-web` status success |
| Database structure | HEALTHY | 221 tables; 174 public; 298 FKs; 0 public tables without RLS |
| RLS fail-closed | HEALTHY_WITH_REVIEW | RLS/no-policy tables exist, but exposure must be judged by effective grants; Health Gate remains authority |
| Duplicate indexes | HEALTHY | live exact-duplicate index query returned zero groups |
| MT authorization | GAP_HIGH | legacy literal-true authenticated policies remain an unresolved authorization boundary |
| Duplicate permissive policies | REVIEW | 10 exact duplicate role/action groups remain across repair/stock tables; provenance still unresolved |
| FK performance | REVIEW_BOUNDED | 145 advisor findings remain, but current workload ranking isolates five high-evidence paths for batch 2 |
| Experience architecture | CONFLICT | English v1 and Portuguese learning families share level codes but all four adjacent transition thresholds diverge |
| Capabilities | HEALTHY | 15 registered capabilities, all active |
| Objective Continuity | READY_UNEXERCISED | persistence owner is live, but currently contains zero checkpoints |
| Cognitive relations | PARTIAL | knowledge exists while `elo_conhecimento_vinculos` and `elo_cognitive_relations` are currently empty |

## Hot FK batch 2 evidence

The live ranking on 2026-10-28 identified the next bounded candidates:

- `mt_unidades_modulares(ordem_producao_id)` — 124 estimated rows, 35 seq scans, 124 writes;
- `mt_unidades_modulares(modelo_id)` — same table activity;
- `mt_unidades_modulares(pedido_venda_item_id)` — same table activity;
- `mt_unidades_modulares(local_atual_id)` — same table activity;
- `elo_automation_runs(automation_id)` — 48 estimated rows, 22 seq scans, 96 writes.

No bulk attempt is made to drive the advisor count to zero.

## Duplicate policy disposition

The 10 remaining multiple-permissive findings are exact predicate duplicates, but the canonical surviving policy family is still not proven by repository provenance. This snapshot does not authorize dropping either family.

## Experience-model disposition

`elo_cognitive_experience_architecture_v1` predates `elo_aprendizado_levels_patterns_and_specializations`. The later Portuguese learning family is used by later learning/extraction/writer migrations, while the English v1 family remains used by runtime guidance/readiness functions and views. Because transition thresholds differ materially, the pair is classified as `GOVERNED_CONFLICT`, not duplicate cleanup.

Canonical promotion remains Symbiont -> Evolution Gate -> Governed Learning -> required human approval. Neither database transition table becomes promotion authority merely because it exists.

## Intuitive health surface

`supabase/health/elo_intuitive_health_summary.sql` is the single compact read-only surface for the main live signals. It complements, rather than replaces, `supabase/health/elo_system_health_gate.sql`.

The compact surface emits: area, status, severity, evidence and next action, so an operator or ELO/GPT handoff can distinguish immediately between healthy, partial, review, conflict and blocking conditions.
