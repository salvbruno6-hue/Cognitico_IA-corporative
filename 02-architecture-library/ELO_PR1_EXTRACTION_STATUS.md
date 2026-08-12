# ELO PR #1 — Extraction Status

## Scope

This document tracks what has actually been extracted, reconciled, or intentionally left historical from PR #1.

## Current result

No executable code from the historical `ELO/` tree has been promoted into `src/elo/` by this reconciliation step.

This is intentional.

The purpose of the current step is to make the decision boundary explicit before any implementation migration.

## Documentation extraction candidates

| Artifact | Current treatment | Next action |
| --- | --- | --- |
| Official architecture library | ADAPT | Compare with current governance and canonical docs |
| Documentation relationship map | ADAPT | Keep one canonical map |
| Technical architecture master | ADAPT | Align with maturity and current implementation evidence |
| Agent development framework | ADAPT | Preserve boundaries, remove premature implementation claims |
| Database master design | ADAPT | Validate against current contracts |
| ADRs | REUSE/ADAPT | Check status and supersession |
| v6 roadmap | ROADMAP | Keep future-only |

## Executable extraction candidates

| Historical area | Current action |
| --- | --- |
| `ELO/core` | Do not promote; mine behaviors only |
| `ELO/agents` | Do not promote; preserve scenarios/domain taxonomy |
| `ELO/connectors` | Do not promote; compare with future integration contracts |
| `ELO/knowledge` | Do not promote; treat lexical/in-memory implementation as test/reference only |
| `ELO/security` | Do not promote; historical security model requires replacement with Tenant/Domain/Principal/Policy |
| `ELO/analytics` | Do not promote without explicit contract and test review |
| `tests/test_elo_architecture.py` | Candidate for test migration after contract mapping |

## Current gate

The reconciliation is **not complete** until every changed file in PR #1 has a documented classification and destination decision.

## Safety rule

Do not close PR #1 or remove historical material solely because it is classified as legacy. Close/retire only after evidence shows its useful content is preserved and no active dependency remains.
