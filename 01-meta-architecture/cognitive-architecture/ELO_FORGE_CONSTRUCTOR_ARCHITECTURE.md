# ELO Forge Constructor Architecture

## Status

Normative architectural proposal for review.

## Purpose

Define ELO-Forge as the **constructor plane inside the canonical Cognitico repository**, not as a second ELO, second Core, second memory, or independent architectural authority.

The Cognitico repository remains the canonical source of truth. Forge is the controlled execution/building area used by ELO to construct, test, reconcile, and prepare changes for promotion into the canonical architecture.

## Canonical relationship

```text
Cognitico_IA-corporative
│
├── Canonical ELO
│   ├── Architecture
│   ├── Governance
│   ├── Contracts
│   ├── Knowledge
│   ├── Memory
│   ├── Reasoning
│   ├── Decision
│   ├── Agents
│   └── Policies
│
└── Forge Constructor Plane
    ├── Build
    ├── Experiment
    ├── Prototype
    ├── Test
    ├── Reconcile
    └── Prepare promotion
```

The recommended Git representation is a dedicated Forge branch namespace such as `forge/*`, created from the canonical `main` and merged only through the governed PR process.

## Authority rule

**ELO/Cognitico decides. Forge constructs.**

Forge has no authority to redefine the canonical architecture by itself.

A Forge result becomes canonical only after:

1. canonical comparison;
2. architectural validation;
3. required specialist review;
4. required tests/evidence;
5. ELO approval;
6. governed merge.

## Constructor lifecycle

```text
OBJECTIVE
  ↓
CANONICAL INSPECTION
  ↓
FORGE TASK
  ↓
BUILD / EXPERIMENT
  ↓
TEST
  ↓
CANONICAL COMPARISON
  ↓
DIVERGENCE?
 ├── NO → REVIEW → PROMOTE
 └── YES
       ↓
   CLASSIFY
       ├── implementation defect → correct
       ├── contract mismatch → adapt
       ├── duplication → consolidate
       ├── naming/location issue → reconcile
       ├── architectural conflict → escalate/ADR
       └── insufficient evidence → investigate
       ↓
   REVALIDATE
       ↺
```

## Canonical-first construction

Before constructing anything, Forge must identify:

- canonical owner;
- applicable contract;
- architecture boundary;
- current implementation;
- tests;
- ADRs;
- security constraints;
- tenant/identity boundaries;
- provenance requirements;
- acceptance criteria.

Forge must prefer extension or correction of an existing canonical capability over creating a parallel implementation.

## Operational artifacts are not automatically promoted

The following remain constructor-plane implementation unless explicitly adopted through a governed architectural decision:

- SQL operational code;
- database migrations;
- runtime configuration;
- infrastructure scripts;
- deployment manifests;
- generated artifacts;
- dashboards;
- temporary experiments;
- operational data;
- provider-specific implementation details.

These artifacts may be **examined as evidence**, but their mere existence in Forge does not make them canonical knowledge or architecture.

## Important distinction: inspection is not promotion

Forge may inspect operational artifacts to discover useful facts, contracts, behavior, or defects.

However:

```text
inspect ≠ promote

observe SQL
      ↓
extract relevant rule/contract if justified
      ↓
compare with canonical architecture
      ↓
ELO decision
      ↓
only then promote the derived knowledge
```

This prevents legacy or divergent implementation details from contaminating the canonical ELO architecture.

## Knowledge promotion

Knowledge extracted from Forge must preserve provenance and be classified as one of:

- FACT
- EVIDENCE
- INFERENCE
- HISTORICAL
- HYPOTHESIS
- CANONICAL RULE
- PROPOSAL

A historical or experimental Forge artifact must never silently become a canonical rule.

## Branch model

Recommended branch semantics:

```text
main
 │
 ├── forge/<task-id>-<purpose>
 ├── forge/<experiment-id>
 └── forge/<migration-id>
```

Every Forge branch must have a clear objective and must eventually reach one of:

- PROMOTED
- REJECTED
- EXPERIMENTAL/RETAINED
- SUPERSEDED
- ABANDONED

Long-lived Forge branches must not become shadow mains.

## Merge model

```text
Forge branch
    ↓
Pull Request
    ↓
CI
    ↓
Specialist review
    ↓
ELO architectural review
    ↓
Acceptance criteria
    ↓
APPROVE_MERGE
    ↓
main
```

Automatic merge is permitted only under the existing ELO governed agent loop and repository protections. Forge itself never bypasses those gates.

## Autonomy

Forge is the place where ELO can remain active for longer periods without user intervention:

- decompose a task;
- construct an implementation;
- run tests;
- inspect failures;
- consult specialists;
- compare against canonical architecture;
- correct implementation;
- repeat bounded validation cycles;
- prepare the PR;
- request or execute governed merge when authorized;
- verify the result after merge.

The autonomous loop must stop when a genuine architectural conflict, missing authority, insufficient evidence, security boundary, or configured retry limit is reached.

## Relationship with external AI architecture intelligence

The Forge constructor plane is the execution environment for bounded experiments identified by the ELO External AI Architecture Intelligence capability.

External technology remains evidence/candidate material. Forge can benchmark or prototype it; only the canonical ELO governance process can promote it.

## Relationship with ELO-Forge repository

The standalone `ELO-Forge` repository is treated as a historical and candidate source during the transition.

Its useful knowledge and proven implementation patterns may be promoted selectively into the canonical repository. The standalone repository is not the canonical authority after the constructor-plane transition.

No mass copy is required.

## Design principle

> **The Forge should make the ELO faster at building, not make the architecture less coherent.**

The constructor plane exists to increase execution capacity while preserving one canonical architecture, one governance authority, and one promotion path.
