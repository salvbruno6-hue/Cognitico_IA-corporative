# Hermes → Symbiont functional handoff

## Purpose

The Hermes candidate loop is an experimental intake path of the existing
Symbiont architecture. It does not create a second Evolution Gate, learning
store, authority model, or canonical mutation path.

## Functional-value rule

A candidate may cross the governed handoff only with structured
`FunctionalValueEvidence`.

The old boolean-style assertion is intentionally removed. Functional proof is
derived from:

- positive task-level gain;
- explicit metric direction;
- repeatability;
- zero regressions;
- candidate attribution;
- provenance references.

Contract integrity alone remains insufficient.

## Current controlled evidence

| Candidate | Functional proof |
|---|---|
| EXT-CONTEXT-PLUGIN-HERMES | Candidate-attributed controlled task gain |
| EXT-HOOK-HERMES | Candidate-attributed lifecycle guardrail detection gain |
| Contract-only candidates | Blocked at RETEST_FUNCTIONAL_VALUE |
| Owner-attributed candidates | Blocked until candidate-specific attribution is isolated |

## Hook experiment

The hook experiment uses five controlled lifecycle events. Baseline detection
is 0.00 and the adapted candidate-specific detection is 1.00, with repeatable
results and no execution/canonical authority.

This is controlled functional evidence, not production outcome evidence.

## Composition

`hermes_secondary_loop_integration` supplies the candidate experiment and
structured evidence to `hermes_governed_loop`.

The governed loop then:

1. validates functional evidence;
2. runs existing implementation-loop readiness;
3. applies existing Evolution Gate/ELO review boundaries;
4. exposes Symbiont implementation start/end views;
5. never mutates canonical state during controlled validation.

Therefore the Hermes loop composes the Symbiont's experimentation and
implementation handoff, while the broader Symbiont remains the surrounding
cognitive evolution architecture.
