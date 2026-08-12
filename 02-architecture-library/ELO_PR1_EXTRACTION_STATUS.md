# ELO PR #1 — Extraction Status

## Scope

This document records what has been reconciled, what remains historical, and what is explicitly prohibited from direct promotion from historical PR #1.

## Reconciliation result

The 59 changed files of historical PR #1 now have explicit file-level classifications in `ELO_PR1_FILE_DECISION_REGISTER.yaml`.

- Classified: 59/59
- Unclassified: 0
- Historical executable tree promoted into `src/elo/`: 0
- Current executable root: `src/elo/`

This is intentional. The historical `ELO/` package is not treated as a second implementation of the ELO.

## Documentation treatment

| Artifact | Treatment | Migration rule |
| --- | --- | --- |
| Official architecture library | ADAPT | Preserve useful constitutional material after authority review. |
| Documentation relationship map | ADAPT | Maintain one canonical relationship map. |
| Technical architecture master | ADAPT | Align with current maturity, contracts and implementation evidence. |
| Agent development framework | ADAPT | Preserve boundaries; remove premature runtime claims. |
| Database master design | ADAPT | Validate against current data contracts before adoption. |
| ADRs | REUSE / HISTORICAL | Retain valid decisions; explicitly mark superseded decisions. |
| v6 roadmap | SUPERSEDE / ROADMAP | Keep future direction separate from implementation authority. |

## Executable treatment

| Historical area | Treatment | Rule |
| --- | --- | --- |
| `ELO/core` | REJECT/HISTORICAL | Mine behaviors and concepts only; do not create a competing core. |
| `ELO/agents` | HISTORICAL | Preserve specialist scenarios; implement agents only through approved runtime gates. |
| `ELO/connectors` | HISTORICAL | Preserve adapter ideas; current integration contracts govern implementation. |
| `ELO/knowledge` | HISTORICAL | In-memory/lexical retrieval is prototype evidence, not production Knowledge. |
| `ELO/security` | REJECT/ADAPT | Historical permission model cannot become current security authority. |
| `ELO/analytics` | HISTORICAL | Reuse only after current contract and test review. |
| `ELO/doors` | HISTORICAL | Preserve interface scenarios; current interface contracts govern. |
| `tests/test_elo_architecture.py` | ADAPT | Candidate behavioral scenarios must be rewritten against canonical contracts. |

## Current gate

**COMPLETE FOR FILE-LEVEL RECONCILIATION.**

All 59 PR #1 files have an explicit decision. This does not authorize migration. Any `REUSE` or `ADAPT` item must pass contract comparison, security/provenance review, tests, and verification before becoming current implementation or normative authority.

## Safety rule

Do not close or delete historical material solely because it is classified as legacy. Retirement requires evidence that useful content is preserved and no active dependency remains.

## Next gate

The next step is not another reconciliation PR. It is selective promotion of only those artifacts that demonstrably fill an identified gap in the canonical repository, with promotion performed in the appropriate existing PR/branch and covered by tests or architectural evidence where applicable.
