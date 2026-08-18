# ELO-092 — Baseline Evidence Gate

## Purpose

Turn the distinction between **GREEN BASELINE** and **EVIDENCED BASELINE** into a reproducible repository gate.

This gate does not declare Baseline v1.0. It verifies that the repository contains the canonical controls and executable evidence required before the ELO baseline can advance to formal review.

## Gate contract

The gate verifies four properties:

1. **Canonical ownership** — evidence remains attached to existing Core/governance contracts rather than creating a parallel authority.
2. **Executable evidence** — critical negative and positive controls exist as tests, not only as prose.
3. **Boundary integrity** — execution requires authorization, evidence and correlation context; contextual evidence remains scoped.
4. **Evidence integrity** — unavailable or insufficient evidence cannot be represented as successful execution or specialist authority.

## Required evidence

- execution boundary and adversarial tests;
- context/tenant isolation evidence;
- specialist handoff blocking when scoped evidence is insufficient;
- canonical baseline readiness definition;
- current issue/dependency registry;
- machine-readable manifest of the gate contract.

## Interpretation

A passing gate means `BASELINE_EVIDENCE_GATE = PASS`.

It does **not** mean:

- production ready;
- enterprise pilot ready;
- live external providers verified;
- specialist feedback received;
- all operational scenarios validated;
- Baseline v1.0 frozen.

Those states require their own evidence as defined by `ELO_BASELINE_CORPORATE_READINESS.md`.

## Failure policy

Any missing required path, test contract, governance invariant, malformed manifest or failed gate test blocks promotion. The correct response is to repair or explicitly defer the evidence; tests must not be weakened to obtain a green result.

## Evolution rule

This gate implements the existing #92 baseline-evidence responsibility. It does not create a second baseline authority. Future changes must first classify themselves as `REUSE | EXTEND | REFERENCE | CONSOLIDATE | NEW` against existing canonical contracts.
