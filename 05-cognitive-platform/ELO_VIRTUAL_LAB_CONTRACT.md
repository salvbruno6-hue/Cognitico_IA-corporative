# ELO Virtual Lab Contract

The Virtual Lab is the Forge's controlled environment for testing cognitive strategies before operational adoption.

## Experiment dimensions

- tenant method fidelity;
- task correctness;
- grounding/evidence;
- calculation accuracy;
- model/tool selection;
- latency;
- cost;
- failure recovery;
- regression;
- privacy boundary preservation.

## Experiment rule

```text
BASELINE -> CANDIDATE -> REPLAY -> MEASURE -> REGRESSION -> GOVERNANCE
```

A candidate that improves a metric but violates tenant methodology, privacy, safety or Core invariants fails the gate.

The Virtual Lab may use synthetic or authorized historical scenarios. Private tenant data must remain within its authorized scope.
