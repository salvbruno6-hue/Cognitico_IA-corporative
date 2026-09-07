# Issue #413 — Live Reconciliation Gate — 2026-09-07

## Purpose

Close the canonical reconciliation gap tracked by Issue #413 without creating a parallel authority.

## Canonical rule

`REUSE → STRENGTHEN → REFACTOR → DEPRECATE → CREATE`

Creation is permitted only after an equivalent canonical mechanism has been searched for and rejected with evidence.

## Required reconciliation gates

1. **Canonical identity and ownership**
   - one authoritative owner per contract;
   - no parallel Core, Memory, Router, Engine, Provider Registry or Evolution Gate;
   - Soul/invariants remain untouched.

2. **GitHub main × Supabase migrations**
   - every live structural migration that belongs to ELO must have a corresponding versioned representation or an explicit governed reconciliation record;
   - no silent renaming or synthetic equivalence;
   - production schema changes remain forward-only and versioned.

3. **Authorization**
   - proof must follow the explicit chain `SESSION → GITHUB IDENTITY → ELO OPERATOR → CAPABILITY → SCOPE`;
   - `ELO_ADMIN`, prompt, email or conversational context alone are not structural authorization;
   - no privileges/scopes are inserted by inference.

4. **Core learning boundary**
   - `elo_core.execucoes`, `avaliacoes`, `correcoes`, `baselines` and `regras` are internal learning structures;
   - access remains fail-closed for public client roles unless a later governed policy explicitly requires otherwise;
   - RLS status must be tested after structural changes.

5. **End-to-end evidence**
   - distinguish laboratory evidence from live evidence;
   - validate the chain:
     `Multiteiner → Forge → Context → Retrieval → Knowledge → Cognitive → Reasoning → Decision → Experience → Evaluation → Learning Candidate → Governed Learning → Evolution Gate → Decoupling → Capability → New Context`;
   - no synthetic evidence may be represented as live operational proof.

6. **Learning integrity**
   - evidence/provenance is mandatory;
   - a better result is not automatically learning;
   - candidate, experience, evaluation and promotion remain distinct states;
   - material evolution requires measurable baseline comparison, confidence, comparable runs and no regression before promotion.

## Efficiency gate

The reconciliation loop must minimize repeated work without weakening any gate. Execute checks in this order:

```text
1. STATIC OWNERSHIP / DUPLICATION
        ↓
2. GITHUB MAIN × MIGRATION HISTORY
        ↓
3. AUTHORIZATION BOUNDARY
        ↓
4. RLS / SECURITY BOUNDARY
        ↓
5. STRUCTURAL + BEHAVIORAL TESTS
        ↓
6. LAB EVIDENCE → LIVE EVIDENCE
        ↓
7. LEARNING / EVOLUTION GATE
        ↓
8. POST-CHANGE AUDIT
```

Stop early when a prerequisite gate fails. Do not spend runtime or database operations proving downstream gates that cannot yet pass. Re-run only the affected gate plus its dependent downstream gates after a correction. A full audit is required only at the final closure pass.

This optimization changes execution order only; it does not lower evidence requirements, authorization requirements, security boundaries or promotion criteria.

## Current implementation posture

The repository already contains the canonical runtime and governance mechanisms required for these boundaries. This document records the closure criteria for Issue #413; it does not create an additional runtime authority.

Supabase live migration history currently contains the recent hardening sequence, including identity/session RPC restrictions, privilege fail-closed controls, and the 2026-09-07 `elo_core` learning-boundary RLS hardening. The corresponding GitHub reconciliation must preserve one traceable migration history.

## Closure rule

Issue #413 may be closed only after:

- migration reconciliation is evidenced;
- authorization policy is evidenced without inferred grants;
- live Forge→Cognitive flow evidence is real and provenance-preserving;
- no contract duplication or parallel authority remains;
- structural/functional tests pass on the current GitHub HEAD;
- Supabase security/performance advisors are reviewed and only accepted residual warnings remain;
- post-change audit confirms zero new orphaned references and no regression.

A CI pass alone is insufficient for closure.
