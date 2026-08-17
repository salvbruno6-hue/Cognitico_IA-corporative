# ELO — Application and Infrastructure Contract

## Purpose

Allow ELO to adapt to corporate platforms without making those platforms part of ELO's canonical intelligence.

## External systems

Examples include ERP, CRM, BI, Git providers, databases, APIs, connectors, agents, dashboards and deployment platforms.

## Contract rule

External systems interact through defined interfaces/contracts. They may provide context, evidence, commands, events and execution results. They may not directly redefine ELO Cognitive canon or mutate Core canonical knowledge outside governed mechanisms.

## ELO App

ELO App modules belong to the Forge/application ecosystem. They can be composed for a company or sector and may evolve independently, provided they comply with Core contracts and canonical invariants.

## Tenant/company isolation

Enterprise-specific configuration, specialists, experiences, decisions and contextual parameters remain scoped to the appropriate enterprise context. One company's operational experience is not silently treated as another company's truth.

## Detachment test

A connector or application can be removed without:
- changing ELO Cognitive identity;
- changing Core canonical contracts;
- corrupting canonical memory;
- creating a parallel authority;
- rewriting historical provenance.

## Replacement test

A technical integration can be replaced by another implementation that satisfies the same contract without changing the cognitive model.

## Authority hierarchy

```text
ELO Cognitive canon
      ↓
Core governance/contracts
      ↓
Forge enterprise context
      ↓
Application modules
      ↓
Infrastructure adapters
```

The hierarchy is an authority boundary, not a dependency requirement. Lower layers can be replaced while higher layers remain stable.
