# ELO — 8 Candidates Operational Evidence

## Stage

`SUCCESS → SELECT → EXECUTE → HISTORICAL EVIDENCE → EVOLUTION GATE`

## Purpose

Close the operational loop after a candidate passes the native functional promotion test. A successful execution can be recorded through the existing `PersistentMemoryStore` as `kind="historical"` evidence.

## Evidence contract

Each recorded execution contains:

- capability identifier;
- tenant scope;
- execution domain;
- immutable historical identity;
- execution status and selection state;
- source/provenance;
- execution result representation;
- operational promotion state;
- explicit `canonical_mutation=false` boundary.

## Authority boundaries

- `CapabilityRegistry` remains the discovery/availability authority.
- `CapabilitySelector` remains the selection mechanism.
- `OperationalCapabilityRuntime` performs execution.
- `PersistentMemoryStore` is reused for historical evidence; no second memory authority is introduced.
- Evolution Gate remains the authority for canonical evolution decisions.
- `SUCCESS` does not imply `CANONICAL`.

## Validation criterion

A candidate is operationally evidenced only when:

1. it is selected from an available registered capability;
2. the existing native mechanism executes successfully;
3. the execution produces an immutable historical evidence record;
4. the evidence can be retrieved and replayed in the same tenant/domain scope;
5. canonical mutation remains explicitly false.

## Boundary

This stage is repository-local and testable. It does not claim production deployment, persistent cloud execution, or external Hermes/OpenClaw execution. Those require their own evidence.

## Next gate

The next transition is not automatic canonization. The evidence must be evaluated against the existing Evolution Gate and the established Core-pillar/generalization requirements. Only that governed path can change the learning state toward `CANONICAL`.
