# ADR-0011 — Reconcile Historical ELO Runtime with Canonical `src/elo`

## Status

Proposed

## Date

2026-08-12

## Context

Historical PR #1 introduced an executable package under `ELO/` containing core, agents, connectors, knowledge, analytics, doors, security, and tests. The current repository identifies `src/elo/` as the executable implementation core and now has explicit agent/repository governance rules.

Merging the historical package wholesale would create competing executable roots and would reintroduce previously identified architectural problems, including a security model based on `department`, in-memory knowledge/memory being treated as production capability, and agents forming a parallel cognitive stack.

## Decision

The historical `ELO/` implementation is treated as reference/provenance material, not as the canonical runtime.

The current executable root is `src/elo/` until a later ADR explicitly changes that decision.

Historical components may be mined for:

- useful behavior examples;
- domain vocabulary;
- tests/scenarios;
- connector patterns;
- analytics ideas;
- documentation;
- migration candidates.

No historical component is promoted into `src/elo/` solely because it appears functionally similar. Promotion requires contract comparison, tests, governance review, and migration analysis.

## Consequences

### Positive

- prevents two executable ELO cores;
- preserves historical work without treating it as production truth;
- allows incremental extraction of useful behaviors;
- strengthens auditability.

### Negative

- some historical code will remain unused;
- additional reconciliation work is required;
- future contributors must understand current versus historical artifacts.

## Alternatives considered

### A. Merge PR #1 wholesale

Rejected because it would create architectural and executable duplication.

### B. Delete PR #1 entirely

Rejected because it would lose provenance and potentially useful architectural/scenario material.

### C. Copy all historical code into `src/elo`

Rejected because naming similarity does not prove contract compatibility and would create hidden coupling.

## Migration rule

For each historical component:

`identify`
→ `classify`
→ `compare contracts`
→ `identify reusable behavior`
→ `implement or adapt in canonical root`
→ `test`
→ `verify`
→ `retire historical implementation when safe`

## Related artifacts

- `02-architecture-library/ELO_PR1_RECONCILIATION_MATRIX.md`
- `02-architecture-library/ELO_PR1_FILE_DECISION_REGISTER.yaml`
- `02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md`
- `AGENTS.md`
- `ELO_REPOSITORY_NAVIGATION_RULES.md`
