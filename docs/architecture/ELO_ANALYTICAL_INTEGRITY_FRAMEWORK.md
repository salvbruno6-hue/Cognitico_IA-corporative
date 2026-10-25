# ELO Analytical Integrity Framework — EAIF v1.1

## Status

Governed implementation aligned to existing ELO reasoning/governance. It does not create a second Cognitive Core, a new source of truth, or a new promotion authority.

EAIF v1.0 introduced evidence-use guards and behavioral conformance. EAIF v1.1 adds contextual activation so refinement is applied only when structured risk signals justify it.

## Purpose

Reduce analytical error by detecting when valid evidence is used in an invalid way and by selectively increasing analytical scrutiny when a decision context is materially riskier.

The framework complements, rather than replaces:

- `ELO_AI_AGENT_WORKING_RULES.md`;
- `src/elo/cognitive/reasoning/requirement_analysis.py`;
- `src/elo/core/consultative_orchestration.py`;
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
| ELO-AI-001 | unresolved/missing/human-validation-required evidence used as fact | remain unresolved and request the next evidence/validation |
| ELO-AI-002 | inference/assumption used without label | label uncertainty and preserve validation boundary |
| ELO-AI-003 | conflict silently resolved | preserve contradiction until governed resolution |
| ELO-AI-004 | historical evidence promoted to current state | revalidate current state or retain historical label |
| ELO-AI-005 | theoretical value promoted to realized performance | compare theory with observed evidence |
| ELO-AI-006 | evidence used as action authorization | resolve authorization through governed authority boundary |
| ELO-AI-007 | inference/assumption used to establish current fact or authorize action | keep it analytical/recommendatory until governed validation |

## Contextual refinement selector

EAIF is not a mandatory heavy-weight pass for every query. The selector accepts only already-structured signals; it does **not** infer risk from free-form keywords in the user's question.

Possible levels:

| Level | Meaning |
|---|---|
| `NONE` | no additional EAIF refinement is needed |
| `TARGETED` | verify only the integrity dimensions implicated by the context |
| `DEEP` | perform explicit counterevidence / falsification-oriented challenge before recommendation |

Structured signals currently include:

- active decision boundary;
- contemplated consequential action;
- unresolved context/evidence integrity gaps;
- material uncertainties;
- explicit conflicts;
- explicitly classified historical/theoretical/stale temporal evidence;
- evidence below the sufficiency threshold.

Selection rules are deterministic:

```text
no relevant signal
=> NONE

ordinary integrity risk
=> TARGETED

explicit conflict
=> DEEP

consequential action + another integrity risk
=> DEEP

three or more independent risk families
=> DEEP
```

A consequential action alone activates `TARGETED`, because evidence and action authority must remain distinct even when the underlying evidence appears clean.

### Orchestration boundary

The canonical consultative path prepares the refinement decision before the specialist handoff:

```text
ContextPack
  -> structured risk signals
  -> EAIF selector
  -> NONE | TARGETED | DEEP
  -> GPTDecisionHandoff
  -> specialist analysis
  -> ELO evaluation
```

This does not alter model/tool routing and does not grant any action authority. `ExecutionRouter` remains the routing authority for model/tool selection.

The legacy `elo-virtual-core/regras/orquestrador.py` simulation is not used as the EAIF integration point.

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

Known historical fiber capacity cannot be reported as current capacity without revalidation. A consultative request carrying that temporal classification receives targeted refinement.

### Theoretical capacity

A theoretical cut/bend capacity cannot be presented as realized production performance.

### MRP

Gross need may support analysis, but it does not authorize a purchase. Stock, reservations, open orders, lead time and the action authority boundary remain separate. If a purchase is contemplated while a required balance is unresolved, the selector escalates to deep refinement.

### Missing data

Missing stock is not zero stock. It remains unresolved until evidence is located.

### Conflicting sources

When two governed sources disagree on a material quantity or capacity, the selector chooses deep refinement; the specialist must preserve the contradiction and search for counterevidence instead of silently choosing one value.

## Non-goals

EAIF does not:

- choose a winner between conflicting sources;
- create business facts;
- retrieve or persist operational data;
- execute purchases, production orders or other business actions;
- select AI models or tools;
- replace domain skills;
- replace the Orchestrator;
- replace Symbiont or Evolution Gate;
- turn external methodological references into canonical authority;
- infer risk merely from words present in a user question.

## Integration direction

```text
objective
-> context/evidence classification
-> requirement sufficiency
-> domain reasoning
-> contextual EAIF selection
-> evidence-usage checks / challenge when selected
-> recommendation
-> authorization gate when action is requested
-> observed behavior
-> Symbiont/Evolution validation
-> governed learning
```

The implementation remains deterministic and side-effect free so it can be reused across PCP, Commercial, Budgeting, Engineering and other analytical domains without creating parallel authority.
