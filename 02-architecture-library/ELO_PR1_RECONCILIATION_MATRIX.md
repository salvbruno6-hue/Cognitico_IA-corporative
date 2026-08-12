# ELO PR #1 Reconciliation Matrix

## Status

**State:** working baseline for reconciliation
**Source:** PR #1 (`codex/evoluir-codigo-para-arquitetura-elo-3.0`)
**Target implementation root:** `src/elo/`
**Rule:** do not merge PR #1 wholesale.

## Purpose

This matrix identifies how the historical PR #1 should be treated relative to the current ELO repository. The objective is to preserve useful knowledge while preventing duplicate executable architectures.

## Classification vocabulary

- **REUSE** — can be retained as-is because it fills a real gap and does not conflict with current authority.
- **ADAPT** — useful concept/content that must be rewritten or relocated to current contracts/structure.
- **SUPERSEDE** — replaced by a newer canonical artifact; preserve history but do not treat as current authority.
- **HISTORICAL** — useful as provenance or reference, not an implementation target.
- **REJECT** — conflicts with current architecture or would create unsafe duplication.

## High-level decisions

| PR #1 area | Decision | Reason |
| --- | --- | --- |
| Official architecture library | ADAPT | Current governance layer provides stronger authority/navigation rules. |
| Documentation relationship map | ADAPT | Keep only one canonical relationship map. |
| Technical architecture master | ADAPT | Must align with current maturity/gate model and actual `src/elo` state. |
| Agent development framework | ADAPT | Preserve conceptual boundaries; do not treat historical agent runtime as current implementation. |
| Database master design | ADAPT | Must be reconciled with current contracts and actual persistence state. |
| ADRs | REUSE/ADAPT | Retain valid decisions; mark superseded decisions explicitly. |
| v6 Self Learning roadmap | SUPERSEDE as implementation authority | Roadmap remains future direction, not current execution requirement. |
| `ELO/core/*` | REJECT as current runtime | Would create a second executable core alongside `src/elo`. |
| `ELO/agents/*` | REJECT as current runtime | Historical scaffolds; current agent runtime must follow approved phase/gates. |
| `ELO/connectors/*` | HISTORICAL/ADAPT | Useful examples only; do not duplicate current integration contracts. |
| `ELO/knowledge/*` | HISTORICAL/ADAPT | In-memory RAG is not production Knowledge implementation. |
| `ELO/security/*` | REJECT as current authority | Historical security model used `department`; current boundary is Tenant/Domain/Principal/Policy. |
| `tests/test_elo_architecture.py` | ADAPT | Preserve useful scenarios but rewrite tests around current canonical contracts. |
| scripts/configure_github_origin.sh | HISTORICAL | Operational utility is not an ELO capability and should not govern architecture. |

## File-level reconciliation

The complete historical PR #1 inventory must be evaluated against this matrix before any content is promoted. The canonical decision record for each file is the combination of:

1. source path in PR #1;
2. target path in current tree, if any;
3. classification;
4. reason;
5. evidence that the destination is authoritative;
6. whether an ADR is required.

## Executable-core rule

No historical file under `ELO/` should be copied into `src/elo/` solely because names appear equivalent.

Required sequence:

`historical implementation`
→ `contract comparison`
→ `behavior comparison`
→ `test coverage`
→ `security/provenance review`
→ `ADAPT/REJECT/REUSE decision`

## Completion criteria

This matrix is considered complete only when every changed file in PR #1 has an explicit classification and destination decision.
