# ELO Baseline Governance Index

## Canonical framework

`ELO_BASELINE_MATURITY_AND_TRACEABILITY_FRAMEWORK.md`

Defines the maturity scale, evidence model, authority model, gates, traceability, audit rules and lifecycle.

## Operational registry

`ELO_CAPABILITY_REGISTRY.yaml`

Initial inventory of ELO capabilities. It is deliberately conservative and does not claim verification without evidence.

## Traceability record

`ELO_TRACEABILITY_RECORD_TEMPLATE.yaml`

Template for individual capability/requirement/contract/change records.

## Snapshot

`ELO_BASELINE_MATURITY_SNAPSHOT_TEMPLATE.md`

Template for a fixed-commit maturity snapshot.

## Audit checklist

`ELO_BASELINE_AUDIT_CHECKLIST.md`

Checklist for baseline preparation and freeze.

## Decision record

`10-adr/ADR-0010-maturity-and-traceability-framework.md`

Proposed architectural/governance decision establishing the framework.

## Entry point

`ELO_BASELINE_README.md`

Short navigation page for humans and AI agents.

---

## Canonical sequence

```text
Repository Navigation
        ↓
Artifact Metadata
        ↓
Capability Registry
        ↓
Requirement / Contract
        ↓
ADR when needed
        ↓
Implementation
        ↓
Tests
        ↓
Evidence
        ↓
Maturity
        ↓
Snapshot
        ↓
Baseline
```

The sequence is a governance model, not an automatic workflow. Each transition requires the evidence and approval appropriate to its risk.
