# ELO-003 — Mainline Reconciliation

## Status
Reconciled against current `main` before PR creation.

## Decision
The prior ELO-003 branch diverged from current `main` and was superseded. This branch is rebuilt directly from the current `main` tip.

## Rules
- `src/elo/agents/governance.py` remains the canonical Agent Contract/Registry boundary.
- `src/elo/agents/orchestrator.py` remains the canonical Tool/Orchestration boundary.
- ELO-002 Evidence/Knowledge/Memory remains authoritative for agent output ingestion.
- No second Cognitive Core is introduced.
- Agent autonomy remains policy-bounded and explicit.
- Agent observations remain observations until governed validation.

## Verification gate
Before merge:

- compile source;
- run full pytest suite;
- verify ELO-001/ELO-002 regression;
- verify tenant/domain/agent identity isolation;
- verify tool authorization;
- verify autonomy enforcement;
- verify invalid executor output rejection.

Do not merge if any gate fails or if GitHub reports the branch as non-mergeable.