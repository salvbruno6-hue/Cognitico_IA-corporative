# ELO Virtual Capability Audit — 2026-08-27

## Purpose

Audit the current executable capability surface through the existing `elo-virtual-core` laboratory, without creating a second scenario engine or a second connector authority.

The laboratory validates behavior using deterministic virtual adapters. It does **not** claim live connectivity to Excel, Supabase, MCP or external providers.

## Capability waves

| Capability | Virtual test | Expected state |
|---|---|---|
| Connector discovery | Excel/Supabase/MCP capability declarations | PASS when capability matches adapter |
| Tabular exchange | Excel-like read/write/export contract | PASS |
| Structured retrieval | Supabase-like historical query contract | PASS |
| Tool handoff | MCP-like tool call contract | PASS |
| Budget calculation | Decimal arithmetic and item traceability | PASS |
| Cross-information | shared-key reconciliation | PASS; conflicts remain explicit |
| Missing information | absent quantity | PASS; remains UNKNOWN |
| Tenant isolation | A/B records | PASS; no cross-tenant leakage |
| Connector failure | unsupported capability | PASS; explicit failure |

## What this proves

1. The virtual environment can exercise connector capability matching.
2. Budget calculations can be tested deterministically without an LLM performing arithmetic.
3. Information from different sources can be crossed by a shared semantic key while preserving source provenance.
4. Conflicting values are not silently resolved.
5. Missing information remains unknown rather than being invented.
6. Tenant scope is preserved during cross-information operations.
7. A missing connector capability fails explicitly.

## What this does not prove

- live Excel integration;
- live Supabase connectivity;
- live MCP transport;
- production credentials or authorization;
- production latency, availability or resilience;
- real company methodology beyond the fixtures supplied to the lab.

Those remain external-evidence gates under the existing maturity program.

## Architectural decision

The existing `elo-virtual-core/testes/` surface is extended rather than creating another laboratory. The production Core remains separate from the sandbox. The virtual environment is a controlled experiment surface for capability validation.

## Next progression gate

After this deterministic wave, real connector evidence can be admitted one connector at a time:

`connector identity → authorization → read/write scope → provenance → transformation → cross-reference → verification → performance evidence → Forge evaluation`.

No live provider result should be promoted to Canon or tenant methodology without the existing governance gates.
