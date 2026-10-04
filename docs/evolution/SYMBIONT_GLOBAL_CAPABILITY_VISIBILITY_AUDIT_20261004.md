# ELO — Global Capability Visibility Audit — 2026-10-04

## Purpose

Global reconciliation of the ELO capability/resource landscape before adding any new capability or authority.

This audit is read-only in meaning. It does not create a second registry, router, Evolution Gate, memory or execution authority.

## Canonical sources inspected

- `ELO_CAPABILITY_REGISTRY.yaml` — conservative capability inventory.
- `01-meta-architecture/cognitive-architecture/ELO_REAL_CAPABILITY_MAP.md` — executable/contractual capability map.
- `docs/testing/ELO_REAL_CAPABILITY_AUDIT_MATRIX.md` — evidence-state matrix.
- `src/elo/core/capability_registry.py` — runtime availability registry.
- `src/elo/cognitive/reasoning/capability_selection.py` — canonical capability selector.
- `src/elo/agent_intake/symbiont_implementation_view.py` — implementation/governance read model.
- `src/elo/cognitive/symbiont_capability_evolution.py` — evolution review/read model.
- canonical execution authorities: `ExecutionRouter`, `AgentOrchestrator`, `ExecutionBoundary`.
- Hermes/runtime candidate adapters and integration evidence.

## Reconciled architecture

```
Capability inventory / source code
        ↓
Capability Registry
        ↓
Capability Selector
        ↓
Canonical Owner
        ↓
Symbiont Implementation View
        ↓
ExecutionRouter / AgentOrchestrator
        ↓
ExecutionBoundary
        ↓
Runtime Operational Evidence
        ↓
Evolution / Evolution Gate
```

The Symbiont is a visibility and coordination layer. Registration means **visibility in the existing canonical registry**, not authorization or promotion.

## Global findings

### 1. There is already a canonical registry

`CapabilityRegistry` supports registration, snapshots and availability probing.

The repository does **not** currently show a broad production bootstrap that automatically registers every ELO capability into this runtime registry. Most direct `CapabilityRegistry(...)` construction found by repository search is in tests.

**Classification:** `EXISTING_BUT_UNWIRED` at global bootstrap level.

### 2. The canonical selector already consumes the same registry

`CapabilitySelector` reads `CapabilityRegistry` and selects only available registered capabilities.

The Symbiont registration bridge added in this branch writes to that same registry and verifies that the selector can immediately select the newly registered capability.

**Classification:** `INTEGRATED` for the registration → registry → selector path.

### 3. The repository has a second, static capability inventory — but it is not a second runtime authority

`ELO_CAPABILITY_REGISTRY.yaml` is explicitly a conservative audit/inventory artifact. It contains historical/architectural capability entries and maturity evidence.

It must remain an audit/read model and must not be treated as the runtime selector registry.

**Classification:** `CANONICAL_READ_MODEL / AUDIT`, not runtime authority.

### 4. The implementation visibility model already exists

`SymbiontImplementationView` already carries:

- implementation identity;
- candidate identity;
- owner;
- capability;
- source and commit;
- dependencies;
- evidence references;
- environment;
- loop stage/result;
- ownership resolution;
- runtime status;
- Evolution Gate status;
- governance status.

Therefore a new global implementation graph would duplicate an existing read model.

**Classification:** `REUSE`.

### 5. Evolution visibility already exists

`CapabilityEvolutionReview` already consumes governed capability measurements and produces read-only actions. It explicitly does not create another Evolution Gate or mutate canonical state.

**Classification:** `REUSE`.

### 6. Canonical execution authorities already exist

The repository contains distinct canonical responsibilities:

| Resource | Canonical responsibility | Global status |
|---|---|---|
| Capability Registry | availability/discovery | implemented |
| Capability Selector | capability selection | implemented |
| ExecutionRouter | model/tool routing | canonical |
| AgentOrchestrator | agent delegation | canonical |
| ExecutionBoundary | governed execution | canonical |
| Runtime Operational Evidence | runtime evidence | canonical |
| Evolution Gate | evolution/promotion authority | canonical |
| SymbiontImplementationView | implementation visibility | canonical read model |
| CapabilityEvolutionReview | capability evolution diagnosis | canonical read model |

No additional orchestrator/router/gate should be created by this work.

## Capability landscape

The repository exposes several overlapping but distinct inventories:

### Architectural/capability families

- Context resolution
- Persistent memory / RAG
- Source discovery and authorized adapters
- Provider consultation
- Core cognitive loop
- Multi-scenario diagnosis
- Systemic/cross-domain reasoning
- Governed execution
- Agent ecosystem
- Execution supervision/resilience
- Budgeting/quotation
- Pricing/source resolution
- Logistics
- Budget × actual
- Learning / Evolution Gate
- Provenance
- Tenant isolation
- Integration contracts/events
- Quality/testing
- Observability
- Production readiness
- Decision Outcome Loop
- Calibration
- Precedent Index
- Causal Reasoning
- Learning Governance
- Knowledge Promotion
- Progressive Tool Schema Disclosure

The older architectural map also records duplicated scenario ownership as an explicit consolidation issue. This remains a governance finding, not a reason to create another scenario authority.

### Hermes candidate/resource families

The repository also contains candidate-specific resources such as:

- EXT-CRON-HERMES
- EXT-PROFILE-HERMES
- EXT-CONTEXT-PLUGIN-HERMES
- EXT-WORKTREE-HERMES
- EXT-MULTIAGENT-HERMES
- EXT-TOOL-SEARCH-HERMES
- EXT-ROUTE-HERMES
- EXT-BATCH-HERMES
- EXT-MEMPROVIDER-HERMES
- EXT-CHECKPOINT-HERMES
- EXT-CONTEXTREF-HERMES
- EXT-LEARN-HERMES
- EXT-LEARNING-GRAPH-HERMES
- EXT-HOOK-HERMES
- and the previously registered candidate-only Hermes surfaces.

These are not independent ELO authorities. They are extensions/adapters around canonical capabilities.

## Isolation / invisibility findings

The scan identifies the following classes that the Symbiont must expose:

| Condition | Finding | Required treatment |
|---|---|---|
| Implemented but not runtime-connected | Present in multiple candidate families | mark runtime gap; do not infer production |
| Registered capability without consumer | possible when runtime registry is constructed locally | expose as unconsumed |
| Implemented capability not in runtime registry | present at repository/static level | expose as `EXISTING_BUT_UNWIRED` |
| Runtime evidence without evolution relation | possible at adapter level | relate to existing evolution read model |
| Capability without resolved owner | governance metadata may be incomplete | `UNRESOLVED` / `WAITING_FOR_EVIDENCE` |
| Duplicate/overlapping authority | scenario family is explicitly documented | consolidate/reuse; do not create parallel authority |
| Candidate-only capability | many Hermes candidates | retain candidate state |
| Controlled evidence without runtime evidence | several Hermes candidates | do not relabel as operational/production |
| Runtime integrated but production not proven | #870/#890/#891/#913/#918/#919/#920 families | retain runtime-integrated / production-pending state |

## Critical result

The global problem is **not absence of orchestration components**.

The principal gap is **visibility/reconciliation across layers**:

```
repository capability
      ≠ automatically
runtime registry
      ≠ automatically
selector-visible resource
      ≠ automatically
runtime-connected capability
      ≠ automatically
operationally evidenced capability
      ≠ automatically
evolution-ready capability
```

The Symbiont should make these transitions explicit and traceable.

## Required next implementation boundary

The next justified evolution is not a new registry.

It is a **global reconciliation/read path** over the existing sources that can answer:

```
WHAT EXISTS
→ WHAT IT DOES
→ OWNER
→ SOURCE
→ REGISTERED?
→ SELECTABLE?
→ CONSUMER
→ CANONICAL ROUTE
→ EXECUTION BOUNDARY
→ RUNTIME STATUS
→ EVIDENCE
→ EVOLUTION STATUS
→ BLOCKER
→ NEXT ACTION
```

The read path must classify each resource conservatively as applicable:

- `CANONICAL`
- `INTEGRATION`
- `EXISTING_BUT_UNWIRED`
- `PARTIAL`
- `MISSING`
- `DUPLICATE`
- `CONFLICT`
- `UNRESOLVED`

No status may be inferred merely from file existence.

## Anti-duplication decision

No new global registry, capability graph, router, Evolution Gate, memory or execution authority is justified by this scan.

The correct implementation path is:

```
REUSE existing registry
+ REUSE existing selector
+ REUSE existing implementation view
+ REUSE existing execution authorities
+ REUSE existing runtime evidence
+ REUSE existing evolution review
→ strengthen global visibility/reconciliation
```

## Evidence boundary

This audit establishes repository-level structural findings. It does **not** establish production outcomes.

For the Hermes candidates, runtime integration and production proof remain separate states. In particular, the existence of deterministic harnesses, unit tests or runtime adapters is not converted into production evidence.

## Status

`GLOBAL_SCAN_COMPLETE`

Next justified intervention: strengthen the existing Symbiont visibility layer so it can reconcile all discovered capability resources against the canonical registry/selector and existing implementation/evolution read models, without creating a parallel authority.
