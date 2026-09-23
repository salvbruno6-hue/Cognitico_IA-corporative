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

## Symbiont trigger — EVOLUÇÃO_DE_CAPACIDADES

When ELO is under production observation, the Symbiont may invoke the read-only trigger `EVOLUÇÃO_DE_CAPACIDADES`. It consumes governed production metrics, baseline/current measurements and evidence already produced by existing mechanisms.

The trigger returns:

`CURVATURA → ITEM → ESTADO → EVIDÊNCIA → AÇÃO EXATA → PRIORIDADE → ONDE COMEÇAR`.

Curvature is evidence-derived:
- positive: measured improvement in the declared metric direction;
- stable: no material measured improvement;
- negative: measured regression;
- critical: severe regression;
- not measured: missing baseline/current/evidence/period or invalid metric direction.

The trigger must never convert missing evidence into zero, an assumed score, or a positive trend.

GPT or another approved analyst may interpret this read model and produce an improvement proposal. The proposal must return to the existing governed flow:

`DIAGNÓSTICO → PROPOSTA → EVIDÊNCIA → TESTE → EVOLUTION GATE → GOVERNANÇA → EVENTUAL PROMOÇÃO`.

The trigger itself has no canonical mutation authority.

## Relationship to Evolution Gate

The dashboard and `EVOLUÇÃO_DE_CAPACIDADES` report states produced by governed processes. They do not approve promotions, alter the Soul or change canonical architecture.
