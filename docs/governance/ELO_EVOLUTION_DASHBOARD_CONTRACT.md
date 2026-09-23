# ELO Evolution Dashboard Contract

## Purpose

Provide an evidence-driven read model of ELO evolution. The dashboard must not invent maturity scores or replace governance decisions.

## Technical dimensions

- architecture coverage;
- capability maturity;
- implementation coverage;
- executable test coverage;
- verified evidence;
- automation coverage;
- observability;
- integration readiness.

## Cognitive/corporate dimensions

- contextual relevance;
- evidence-backed decisions;
- provenance completeness;
- validated learning;
- observed outcomes;
- detected risks/deviations;
- reduction of rework/errors when measurable;
- demonstrated corporate value.

## Evidence rule

Every metric must identify its source, measurement period, calculation rule and evidence references. Undefined metrics remain `NOT_MEASURED`, not zero and not an assumed score.

## Monthly history

Store immutable monthly snapshots so technical evolution can be compared with adherence to ELO's corporate purpose.

## Suggested states

`NOT_MEASURED`, `PROPOSED`, `IMPLEMENTED`, `TESTED`, `VERIFIED`, `REGRESSED`, `BLOCKED`.

## Relationship to Evolution Gate

The dashboard reports the state produced by governed processes. It does not approve promotions, alter the Soul or change canonical architecture.


## Symbiont trigger — EVOLUÇÃO_DE_CAPACIDADES

During production observation, the Symbiont may invoke the read-only trigger
EVOLUÇÃO_DE_CAPACIDADES. It consumes capability metrics that were explicitly
emitted by existing governed production mechanisms.

The diagnostic returns:

CURVATURA → ITEM → ESTADO → EVIDÊNCIA → AÇÃO EXATA → PRIORIDADE → ONDE COMEÇAR

Curvature is derived only from baseline/current values, declared metric
direction, measurement period and evidence. Missing or invalid evidence remains
NOT_MEASURED and is never converted into zero or an assumed trend.

The trigger is analytical only. An approved analyst may interpret its output,
but any proposed improvement must return to the existing governed path:

DIAGNÓSTICO → PROPOSTA → EVIDÊNCIA → TESTE → EVOLUTION GATE → GOVERNANÇA → EVENTUAL PROMOÇÃO

The trigger has no canonical mutation, learning-promotion or deployment authority.
