# Hermes MCP spend governance candidate — 2026-10-21

## Source observation
Hermes introduced declared per-tool MCP costs and per-chat spend limits, then hardened the mechanism so totals survive session rotation, cron runs receive independent scope, parallel approval prompts are serialized, in-flight reservations follow multiplex rekeys, and malformed/unknown declarations do not silently widen authority.

## ELO adaptation
Candidate invariant only: **external capability + declared cost + scoped accumulated spend + limit -> pre-dispatch decision**.

Canonical ownership remains with ELO External Capability Gateway / governed execution. This candidate does not dispatch tools, approve costs, create a second execution authority, mutate memory, or perform business operations.

## Fail-closed rules
- malformed or negative policy: block;
- within declared limit: eligible to continue through existing execution governance;
- above limit in interactive context: require human approval, without dispatch;
- above limit unattended: block;
- absent declaration: preserve existing behavior rather than invent a cost.

## Validation target
The candidate is not canonical merely because this document or implementation exists. It requires controlled tests, regression checks, Evolution Gate and governed merge. Supabase persistence must not be fabricated; current cognitive tables contain no Hermes-labelled rows, so GitHub/Supabase representation remains a GAP for separate governance.
