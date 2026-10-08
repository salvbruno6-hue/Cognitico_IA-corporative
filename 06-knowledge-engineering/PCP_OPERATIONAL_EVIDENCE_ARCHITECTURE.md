# PCP operational evidence architecture

## Purpose

The PCP analytical layer remains independent from Symbiont while exposing a
canonical evidence handoff.

## Flow

`operational data -> PCP dimensions -> confrontation -> integrated diagnosis -> evidence package -> canonical handoff -> DecisionLifecycle -> SymbiontSkillRuntime -> SymbiontLabAdapter -> EvolutionGate`

## Ownership

- PCP: deterministic calculations, confrontation and domain evidence packaging.
- Supabase: canonical operational/data authority.
- PCP handoff: translation boundary only.
- DecisionLifecycle: governed decision state transitions.
- SymbiontSkillRuntime: thin dispatch boundary.
- SymbiontLabAdapter: laboratory evaluation and governed-learning bridge.
- EvolutionGate: evolution classification.
- Human governance: approval/escalation and promotion decisions.

## Non-inference rules

1. Missing planned or actual data remains `NAO_LOCALIZADO`.
2. A variance does not establish its cause.
3. Cause requires explicit evidence.
4. Dates are not converted into lead time unless the source explicitly supplies
   the semantic duration needed for that calculation.
5. Material allocated and material purchased remain separate facts.
6. PCP cannot manufacture laboratory hypothesis, experiment, regression,
   generalization or risk state.
7. PCP cannot create or promote learning.
8. A real Symbiont handoff requires a decision already in `ATTRIBUTED`
   with outcome, attribution and evidence.

## Operational readiness

The analytical and handoff structures can be tested structurally. Full
operational execution remains pending until canonical PCP operational records
exist in Supabase.

Current verified PCP operational tables contain zero records in the controlled
environment for plans, plan lines, production orders, operations, daily
capacity, material requirements, stock lots and modular flow events.
