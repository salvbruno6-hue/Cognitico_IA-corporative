# Symbiont MCP Test Harness

## Purpose

Provide an ELO-owned laboratory boundary for benchmarking an already-authorized MCP capability. The harness does not discover authority, grant authorization, mutate canonical knowledge, or promote learning.

## Canonical flow

```text
ELO Cognitive authorization
        |
        v
MCP descriptor + controlled test case
        |
        v
Symbiont MCP Test Harness
        |
        v
SymbiontHermesBridge
        |
        v
Hermes -> MCP tool
        |
        v
Evidence + Outcome + Metrics
        |
        v
BenchmarkResult(candidate_only)
        |
        v
Evolution Gate
```

## Invariants

1. Descriptor, test case and authorized request must identify the same capability.
2. Tenant scope must match at every boundary.
3. Test evidence requirements cannot exceed the ELO authorization envelope.
4. Tests are non-destructive by default; destructive tests require explicit review.
5. Tool-call bounds are enforced before execution.
6. Benchmark evidence must carry traceable evidence IDs; synthetic fallback is rejected.
7. Scores are normalized to `[0,1]` and remain measurements, not governance decisions.
8. A successful benchmark is `LAB_CANDIDATE`, never direct Core knowledge or authorization.
9. `SymbiontHermesBridge` remains the single execution transport boundary.
10. MCP does not replace, redefine, or absorb Symbiont governance.

## Relationship to legacy #459

This native implementation operationalizes the intent of the legacy MCP harness candidate without reviving its old code. Existing canonical MCP contracts and the existing Hermes bridge are reused. Hermes remains an execution provider/reference, while ELO retains authorization, evidence interpretation and Evolution Gate authority.
