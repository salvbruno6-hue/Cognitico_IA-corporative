# ELO-012 — Modular Flow Ingestion Protocol

## Objective

Use the Multiteiner modular-flow material as an operational knowledge source while preserving source authority and epistemic boundaries.

## Extraction model

```text
Source document
  → process
  → stage
  → activity
  → input
  → resource
  → person/role
  → equipment
  → material
  → dependency
  → constraint
  → output
  → risk
  → evidence reference
```

## Interpretation rules

- The source is authoritative only for what it explicitly establishes.
- Inferences must be marked as inference.
- Missing process steps remain unknown.
- Conflicting sources create a contradiction state.
- Current observed behavior may differ from documented design and must be represented as a process deviation, not silently overwrite the documented process.

## Cross-sector links

The extracted flow can be linked to:

- purchasing lead time;
- stock availability;
- production orders;
- maintenance events;
- quality records;
- logistics movements;
- financial costs;
- commercial deadlines;
- workforce capability and allocation.

These links create hypotheses for investigation. They do not establish causality without evidence.

## Example investigation

```text
Observation: high equipment maintenance cost
        ↓
Potential relations:
  route / floor condition / usage / maintenance practice / equipment condition
        ↓
Evidence search:
  maintenance history + movement events + operational context
        ↓
Information gaps
        ↓
Specialist questions
        ↓
Scenario comparison
        ↓
Recommendation
```

The ELO must not declare a person, sector or supplier responsible solely from correlation.
