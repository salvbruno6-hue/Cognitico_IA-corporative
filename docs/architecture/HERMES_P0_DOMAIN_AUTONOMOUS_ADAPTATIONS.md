# ELO native capabilities: Domain Intelligence + Autonomous Reasoning

## Architectural correction

These candidates are **ELO capabilities**, not Hermes integrations. Hermes is only a discovery/reference/provider source used to identify mechanisms worth generalizing.

The native contract must remain usable when Hermes is absent.

```text
Hermes evidence / other evidence sources
        ↓
mechanism extraction + generalization
        ↓
ELO native capability
  ├─ Domain Intelligence
  └─ Autonomous Reasoning
        ↓
Symbiont Pattern Intake
        ↓
Evolution Gate
        ↓
LAB_CANDIDATE / REUSE / BLOCK
        ↓
validated promotion to the appropriate ELO layer
```

## Domain Intelligence

`src/elo/cognitive/domain_intelligence.py` owns the provider-neutral contract for evidence-bearing domain observations. It models target, provenance, evidence, observations, confidence, limitations and risk. It does not perform network acquisition and does not depend on Hermes.

Acquisition providers may populate the contract, but provider-specific names, credentials and execution semantics remain outside the ELO capability.

## Autonomous Reasoning

`src/elo/cognitive/autonomous_reasoning.py` owns a bounded planning contract: objective, ordered actions, constraints, expected and observed outcome, evidence, limitations, provenance and risk. The native capability validates and classifies the reasoning experience; it does not grant permissions or execute tools.

This deliberately generalizes mechanisms such as bounded planning, explicit constraints, outcome observation and evidence-backed recovery/learning without making Hermes the owner.

## Governance and reuse

Both capabilities reuse the canonical `SymbiontPatternIntake` and `EvolutionGate`. No second candidate registry, provider authority, canonical write path or evolution engine is introduced.

`source_ref` and `source_commit` preserve evidence lineage. They identify where a mechanism was observed; they do not identify that provider as the ELO owner.

## Test criterion

The native tests must instantiate both capabilities without importing Hermes, making network calls or requiring provider credentials. A separate comparative test may feed a real authorized Hermes observation into the native contracts, but that is evidence for validation rather than a runtime dependency.

## Source lineage

The mechanisms were derived from an audit of `salvbruno6-hue/ELO-Hermes-Agent`, including its domain-intelligence and autonomous-agent capability families. The source lineage is retained for traceability while the resulting contracts remain ELO-owned and provider-neutral.
