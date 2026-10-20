# Hermes Current Surface Delta — 2026-10-04

Fresh review of Hermes v0.21.x public release surfaces against ELO main.

## New candidate mechanisms

1. Wire-contract registry and server-to-client JSON-RPC.
2. MCP issuer-bound OAuth and re-auth health state.
3. Session DB reader/writer topology and handle registry.
4. Live delegation steering with partial results and output schemas.
5. Cron continuity with persistent memory, scratchpad and no-change short-circuit.
6. Protected instruction surfaces with explicit write approval and broader redaction.
7. Durable bot-to-bot peer messaging across profiles/gateways.
8. Desktop browser interaction as an externally-effectful capability.
9. Model capability metadata and training-tier selection warnings.

## Candidate rule

Every item is candidate-only and reuses an existing ELO owner. No new authority, memory authority, Evolution Gate, or autonomous promotion is created.

## Validation boundary

Only deterministic ELO-side metadata and invariant tests are permitted in this discovery. No Hermes runtime, external connector, browser, MCP server, cron job, peer agent or business system is invoked.

## Evidence

Hermes v0.21.1 introduced durable Bot Mode, peer messaging, persistent cron continuity, live subagent steering, MCP management and instruction-surface protection. Hermes v0.21.3 added Pydantic wire-contract/generated schema infrastructure, issuer-bound MCP OAuth refresh tokens and session DB writer-handle hardening. These are treated as source observations, not architectural authority.

## Production status

None of the nine mechanisms is classified as a production outcome by this change. Existing ELO runtime integrations remain unchanged.
