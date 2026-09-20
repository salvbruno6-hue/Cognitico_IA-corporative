# ELO — Implementation Loop Start Gate

**Date:** 2026-09-20  
**Status:** PRE-FLIGHT / GOVERNED

## Purpose

Make the transition from isolated candidate evaluations to the governed
implementation loop explicit and deterministic.

This gate does not deploy, merge, promote, mutate canonical memory, or alter
authorization.

## Entry contract

A candidate may enter the implementation loop only when all are present:

1. candidate remains bounded and candidate-only;
2. controlled evidence is valid;
3. baseline and adapted metrics exist;
4. at least one common metric exists;
5. every measured metric has explicit direction: `maximize` or `minimize`;
6. no regression or governance-boundary violation exists;
7. repeatability is proven;
8. provenance and owner mapping are available from the evaluation record.

## Loop

`OBSERVED → CANDIDATE → CONTROLLED_TEST → MEASURED_GAIN → REPEATABLE → EVOLUTION_GATE → ELO_REVIEW → IMPLEMENTATION_AUTHORIZED`

Implementation authorization is not canonical mutation. Actual canonical
change remains a separate governed merge/implementation action.

## Current project position

The implementation-loop engine already exists and its regression ordering is
tested. The start gate now provides an explicit pre-flight contract so the
first full loop cannot start from incomplete evidence.

The current Hermes sequence continues independently until the candidates have
their controlled evidence. A `RETEST` result does not satisfy the gain gate;
it returns the candidate to controlled experimentation.

## First-loop rule

The first complete loop must use a candidate with:

- measured positive gain;
- explicit metric direction;
- zero regressions;
- repeatable result;
- valid provenance;
- Evolution Gate approval;
- explicit ELO authorization before implementation.

No candidate is activated merely because its evaluation PR was merged.
