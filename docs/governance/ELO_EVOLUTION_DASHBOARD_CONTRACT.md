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
