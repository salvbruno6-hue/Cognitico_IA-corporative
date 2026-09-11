# Symbiont MCP Test Harness

## Purpose

The harness is the first executable experimental layer after the MCP contracts. It turns a governed `MCPCapabilityDescriptor` + `MCPCapabilityTestCase` + already-authorized `HermesExecutionRequest` into a traceable `MCPCapabilityBenchmarkResult`.

It does not install MCP servers, manage credentials, authorize missions, mutate Core, or decide promotion.

## Execution boundary

```text
MCPCapabilityDescriptor
        +
MCPCapabilityTestCase
        +
ELO-authorized HermesExecutionRequest
        |
        v
SymbiontMCPTestHarness
        |
        v
SymbiontHermesBridge
        |
        v
Hermes runtime
        |
        v
MCP tool
        |
        v
HermesExecutionResult
        |
        v
MCPCapabilityBenchmarkResult (candidate_only)
```

## Harness invariants

1. Capability identity must match across descriptor, test case and authorized request.
2. Tenant scope must match across all three inputs.
3. Test evidence requirements cannot exceed the ELO request evidence contract.
4. Tests are non-destructive by default.
5. Destructive tests require explicit review in the test constraints.
6. Hermes tool usage cannot exceed `max_tool_calls`.
7. Evidence must contain traceable evidence IDs; synthetic fallback IDs are not accepted.
8. Scores are normalized to `[0, 1]` and are descriptive only.
9. A successful benchmark becomes `LAB_CANDIDATE`, never Core knowledge.
10. The existing SymbiontHermesBridge remains the only transport boundary.

## Initial experimental matrix

The harness should first be exercised with representative capabilities:

| Family | Safe first experiment | Evidence | Expected outcome |
|---|---|---|---|
| Sheets | read controlled fixture | rows + execution trace | structured extraction |
| Browser/Web | navigate and extract controlled page | URL + extraction trace | deterministic extraction |
| YouTube | search controlled query and retrieve metadata/transcript | result IDs + execution trace | structured metadata |

The matrix is intentionally small. Capability breadth is expanded only after the evidence pattern is stable.

## Promotion boundary

A benchmark result is an experimental observation. The result must subsequently enter the existing ELO learning/evolution governance and Evolution Gate. The harness never invokes a second gate and never promotes a candidate automatically.

## Runtime note

For local tests, the harness accepts an injected transport. This permits deterministic integration tests without requiring a live Hermes or MCP server. The production path uses the configured Hermes endpoint through the existing runtime client.
