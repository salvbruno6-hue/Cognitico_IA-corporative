# ELO — Canonical Reconciliation Contract

## Purpose

Provide an executable evidence stage for the existing ELO Maintenance Coordinator. This is **not** a second architectural authority.

## Required chain

```text
PR/DIFF
→ INVENTORY
→ CONCEPT IDENTITY
→ EXISTING CAPABILITY SEARCH
→ OWNER / SOURCE OF TRUTH
→ PRODUCERS / CONSUMERS / REFERENCES
→ DUPLICATE / PARALLEL CHECK
→ CONTRACT CONFLICT CHECK
→ CLASSIFICATION
→ EVENT FACTS
→ canonicality_gate()
```

## Conservative semantics

- `UNKNOWN` is never equivalent to `TRUE`.
- Missing owner, source of truth, identity or reuse evidence produces `WAITING_FOR_EVIDENCE`.
- Absence of an exact name is not proof of absence of a capability.
- Unreferenced does not automatically mean obsolete or removable.
- A candidate implementation must be reconciled before `CREATE` is admissible.

## Classification

```text
REUSE → STRENGTHEN → REFACTOR → DEPRECATE → CREATE
```

`CREATE` is valid only when repository evidence proves no existing canonical capability can satisfy the requirement and ownership/source-of-truth are explicit.

## Regression scenarios

The executable suite must cover at minimum:

1. existing equivalent capability → `REUSE`;
2. unresolved owner/source → `WAITING_FOR_EVIDENCE`;
3. unresolved duplicate state → `WAITING_FOR_EVIDENCE`;
4. contract conflict → blocking gate;
5. obsolete scaffold candidate must not be deleted solely because it is unreferenced;
6. functional `context`/`evidence` implementations remain protected when consumers exist;
7. a newly named parallel memory/router/auth implementation cannot bypass reconciliation.
