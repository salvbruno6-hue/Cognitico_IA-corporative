# ELO External Repository Boundary

**Status:** Canonical
**Authority:** ELO Cognitivo
**Effective:** 2026-09-12

## 1. Purpose

This document defines the repository boundary of ELO Cognitivo.

The ELO architecture, governance, memory model, directives, contracts, specialist knowledge, decision rules and evolution criteria must be constructed and maintained inside the canonical ELO repository:

`salvbruno6-hue/Cognitico_IA-corporative`

ELO must not depend on a second repository as a parallel cognitive authority.

## 2. Sole external repository connection

The only external repository intentionally connected to ELO is:

`salvbruno6-hue/ELO-Hermes-Agent`

Hermes is an execution/extension boundary (symbiont), not the canonical authority for ELO knowledge or governance.

The dependency direction is:

`ELO Cognitivo → ELO-Hermes-Agent`

not the inverse.

## 3. Cognitico AI boundary

`salvbruno6-hue/cognitico-ai` is **not** an ELO repository, ELO authority, ELO dependency, ELO memory source, ELO architecture source, or ELO execution provider.

No ELO contract, routing rule, memory policy, specialist definition, governance decision or architectural dependency may be introduced there as a prerequisite for ELO operation.

Existing references that merely point to the canonical repository are historical/project lineage and must not be interpreted as an architectural dependency.

## 4. Construction rule

When new information, architecture, specialist behavior, directives, schemas, contracts, tests, evidence or governance rules are created for ELO:

1. Build and validate them in `Cognitico_IA-corporative`.
2. Persist cognitive state in the governed ELO data layer when applicable.
3. Use Hermes only for execution, integration, tooling or edge capabilities explicitly governed by ELO.
4. Do not copy ELO cognitive authority into another repository.
5. Do not create a parallel repository authority to compensate for missing ELO capabilities.

## 5. Decoupling objective

The target state is that ELO can operate as a coherent cognitive system without `cognitico-ai`.

Decoupling is complete only when dependency/reference audits and runtime tests show that removal or unavailability of `cognitico-ai` does not prevent ELO from loading its canonical architecture, governance, memory contracts, specialists, routing and approved execution path through Hermes.

## 6. Authority model

| Layer | Authority | Role |
|---|---|---|
| ELO Cognitivo | `Cognitico_IA-corporative` | Canonical cognitive architecture and governance |
| ELO persisted cognitive state | Governed Supabase layer | Persistent memory/state |
| Hermes | `ELO-Hermes-Agent` | External execution/extension symbiont |
| Cognitico AI | None for ELO | Independent/non-authoritative project |

## 7. Prohibited states

- ELO depending on `cognitico-ai` for startup or cognition.
- `cognitico-ai` becoming a hidden source of ELO rules or memory.
- Duplicating canonical ELO architecture in Hermes.
- Treating Hermes as an independent cognitive authority.
- Recreating deleted legacy ELO repositories as parallel authorities.

## 8. Governance principle

If a capability currently exists only outside `Cognitico_IA-corporative` and is required for ELO cognition, first migrate/generalize the required knowledge, contract or architecture into ELO Cognitivo, validate it, and only then retain an external implementation at the execution edge if necessary.
