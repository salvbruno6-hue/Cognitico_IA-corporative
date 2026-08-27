# ELO Cognitive Execution Loop — 2026-08

## Objective

Transform external research into bounded, executable ELO capabilities while preserving the Canon, tenant isolation and provider independence.

## Runtime loop

```text
request -> context -> memory -> routing -> reasoning -> verification -> decision -> experience
                                      ^                                      |
                                      |                                      v
                                      +----------- Forge / evaluation <-----+
```

## Adaptive principle

The first router is deterministic and safe. The adaptive router may learn from explicit execution feedback, but it cannot mutate the Canon. Experiences are scoped to capabilities and remain evidence, not truth.

## Promotion rule

```text
experience
  -> benchmark
  -> candidate
  -> regression
  -> governance
  -> canonical capability
```

A capability is never promoted solely because an external project is popular or because one execution scored well.

## Tenant boundary

Tenant memories are searchable only inside the matching tenant scope. Canonical memory cannot carry a tenant identifier. Enterprise information is therefore not a default input to canonical learning.

## Provider boundary

Inference remains behind an adapter. The cognitive engine does not depend on a specific LLM provider, vLLM, llama.cpp, MCP server or user interface.
