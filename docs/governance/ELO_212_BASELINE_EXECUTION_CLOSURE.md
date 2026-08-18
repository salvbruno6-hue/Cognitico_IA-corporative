# ELO-212 — Baseline Execution Closure

Status: **implementation candidate; merge only after repository validation is green**.

## Objective

Close the next gap after ELO-200→211 by making the execution boundary explicit and testable. ELO may recommend, classify, validate, authorize and prepare an action, but an external side effect occurs only through a governed execution adapter.

## Canonical lifecycle

`OBSERVE → ANALYZE → DECIDE → AUTHORIZE → EXECUTE → MONITOR → FEEDBACK`

The stages are not interchangeable:

- **OBSERVE** collects scoped evidence and provenance.
- **ANALYZE** produces reasoning, alternatives and uncertainty.
- **DECIDE** records the canonical decision or recommendation.
- **AUTHORIZE** establishes the principal and authorization boundary.
- **EXECUTE** delegates the side effect to an explicit adapter.
- **MONITOR** records the result and deviation.
- **FEEDBACK** produces append-only evidence for future evolution.

## ELO authority model

| Layer | Authority | May mutate canonical state? |
|---|---|---|
| Cognitive / Core | identity, semantics, reasoning, governance | only through governed canonical contracts |
| Forge | domain execution skills and calculations | no direct Core promotion |
| Provider / adapter | external capability | no ELO identity authority |
| Execution adapter | authorized side effect | only the scoped external target |
| Evolution Gate | compatibility/evolution classification | no automatic canonical mutation |

## Execution invariants

1. No execution without tenant, principal, action, authorization and correlation context.
2. No execution without evidence references.
3. A blocked request is a successful governance outcome, not an execution failure to be bypassed.
4. An unavailable adapter produces `DEGRADED`/`BLOCKED` evidence rather than simulated success.
5. Every executed action retains request, authorization, principal and correlation provenance.
6. Consultation remains advisory and cannot manufacture execution authority.
7. Forge cannot promote a result directly into canonical Core state.
8. Historical feedback remains append-only.

## Baseline acceptance

The baseline can only be declared when all of the following have evidence:

- [x] canonical Source Discovery and capability mapping;
- [x] provider-neutral Evolution Gate;
- [x] hybrid provider selection and degradation;
- [x] bounded consultative orchestration;
- [x] governed Forge skill packs;
- [x] append-only specialist feedback;
- [x] secret-free local capability probes;
- [x] retrieved evidence → canonical BudgetInput bridge;
- [x] canonical scenario ownership;
- [x] explicit non-executing degradation;
- [x] governed execution boundary with adversarial tests;
- [ ] repository CI evidence for the final merge commit;
- [ ] live-provider execution evidence where credentials and authorization exist;
- [ ] post-execution monitoring evidence from at least one real adapter;
- [ ] formal naming/duplicate-directory migration plan completed without semantic collision.

## Naming and repository structure

Directories with Portuguese/English or singular/plural duplicates must not be merged merely because their names look equivalent. Before consolidation, each directory requires an inventory of files, import references, ownership and semantic purpose. The canonical name is selected by function, not language preference. A rename is accepted only when references, tests, documentation and deployment paths are migrated and the old path is removed or explicitly retained as a compatibility alias.

## Merge rule

This document does not declare Baseline v1.0. It defines the evidence required to make that declaration defensible. Missing live credentials are represented as `UNAVAILABLE/DEFERRED`; they must never be simulated as green execution evidence.
