# ELO Analytical Integrity Framework — EAIF v1.0

## Status

Candidate implementation aligned to existing ELO reasoning/governance. It does not create a second Cognitive Core, a new source of truth, or a new promotion authority.

## Purpose

Reduce analytical error by detecting when valid evidence is used in an invalid way.

The framework complements, rather than replaces:

- `ELO_AI_AGENT_WORKING_RULES.md`;
- `src/elo/cognitive/reasoning/requirement_analysis.py`;
- domain reasoning such as `SKILL_PLANEJAMENTO_MULTITEINER`;
- Orchestrator diagnosis;
- Symbiont evidence observation;
- Evolution Gate promotion/governance.

## External methodological references

The design was refined from open/reference material discussed for ELO:

- Prompt - Analise de Dados: data-quality, null/error, relational and interpretation checks;
- Microsoft PromptKit anti-hallucination patterns: distinguish known/inferred/assumed information;
- Agent Reliability Engineering patterns: non-goals, escalation, failure/regression testing and observability;
- Praxen/agent behavior verification: declared controls vs observed behavior;
- prompt-audit patterns: failure taxonomy and correction-oriented anti-patterns;
- authorization/trust-boundary patterns: evidence must not silently increase action authority.

These are references, not ELO authorities. Their principles must pass ELO governance before promotion.

## Reuse analysis

The repository already contains governed epistemic states in `requirement_analysis.py`:

`KNOWN`, `DOCUMENTED`, `RETRIEVED`, `CALCULATED`, `INFERRED`, `ASSUMPTION_REQUIRED`, `CONFLICT`, `MISSING`, gap and human-validation states.

Therefore EAIF does **not** duplicate those states. It evaluates whether their *use* is valid.

## Core separation

Four dimensions must remain separate:

```text
source reliability
!= evidence state
!= decision authority
!= action authorization
```

A reliable external source may prove a fact without granting authority to execute an action.

## Initial anti-pattern controls

| Code | Anti-pattern | Correct behavior |
|---|---|---|
| ELO-AI-001 | unresolved/missing evidence used as fact | remain unresolved and request next evidence |
| ELO-AI-002 | inference/assumption used without label | label uncertainty and preserve validation boundary |
| ELO-AI-003 | conflict silently resolved | preserve contradiction until governed resolution |
| ELO-AI-004 | historical evidence promoted to current state | revalidate current state or retain historical label |
| ELO-AI-005 | theoretical value promoted to realized performance | compare theory with observed evidence |
| ELO-AI-006 | evidence used as action authorization | resolve authorization through governed authority boundary |

## Behavioral conformance

EAIF also supports a minimal deterministic comparison:

```text
declared control
vs
observed behavior
=> CONFORMANT | DIVERGENT
```

This is evidence for Symbiont/Evolution analysis. It is not itself a promotion decision.

## PCP examples

### Historical capacity

Known historical fiber capacity cannot be reported as current capacity without revalidation.

### Theoretical capacity

A theoretical cut/bend capacity cannot be presented as realized production performance.

### MRP

Gross need may support analysis, but it does not authorize a purchase. Stock, reservations, open orders, lead time and the action authority boundary remain separate.

### Missing data

Missing stock is not zero stock. It remains unresolved until evidence is located.

## Non-goals

EAIF does not:

- choose a winner between conflicting sources;
- create business facts;
- retrieve or persist operational data;
- execute purchases, production orders or other business actions;
- replace domain skills;
- replace the Orchestrator;
- replace Symbiont or Evolution Gate;
- turn external methodological references into canonical authority.

## Integration direction

Recommended path:

```text
objective
-> context/evidence classification
-> requirement sufficiency
-> domain reasoning
-> EAIF evidence-usage check
-> recommendation
-> authorization gate when action is requested
-> observed behavior
-> Symbiont/Evolution validation
-> governed learning
```

The first implementation intentionally remains deterministic and side-effect free so it can be reused across PCP, Commercial, Budgeting, Engineering and other analytical domains without creating parallel authority.
