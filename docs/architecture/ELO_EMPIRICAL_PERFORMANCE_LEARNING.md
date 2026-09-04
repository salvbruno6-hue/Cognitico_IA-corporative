# ELO Empirical Performance Learning

## Objective

Allow ELO to accumulate empirical evidence about which execution configuration performs better for each mission class.

## Configuration signature

`mission_type + specialist + model + tools + context_profile + method`

The signature is observed, not predetermined as permanently optimal.

## Measurement model

Each execution may contribute:

- result status;
- quality score;
- observed outcome score;
- latency;
- cost;
- evidence identifiers;
- tenant and provenance metadata.

The current baseline empirical score is the mean of available quality and outcome scores. Missing scores are preserved as missing and are not fabricated.

## Governance

PerformanceMemory is evidence, not policy. It MUST NOT replace `ExecutionRouter`, `ModelSelector`, `ToolSelector`, canonical memory, or the Evolution Gate.

Historical observations remain tenant-scoped. A result from one tenant cannot become evidence for another tenant.

## Learning path

`Execution → PerformanceObservation → aggregation → routing evidence → governed candidate → validation → Evolution Gate`

The routing layer may consume validated performance evidence, but a single observation must not permanently change routing behavior.

## POC target

Budget Intelligence is the first mission class for empirical measurement because it already has governed budgeting, provenance and outcome boundaries in the repository.
