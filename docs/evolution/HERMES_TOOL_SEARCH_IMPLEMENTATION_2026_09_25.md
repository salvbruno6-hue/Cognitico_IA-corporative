# Hermes Tool Search — Governed Implementation — 2026-09-25

## Status

- Candidate: `EXT-TOOL-SEARCH-HERMES`
- Existing owner: `ELO Model/Tool Routing`
- Implementation authorization: `APPROVE`
- Authorization reference: Issue #734
- Evolution Gate: required
- Canonical mutation: `false`
- Runtime tool execution: `false`

## Implemented behavior

The existing candidate contract now contains the governed progressive disclosure implementation:

1. normalize the query;
2. inspect only the existing allowlisted schema catalog;
3. select schemas whose name or schema text matches a query token;
4. preserve catalog order;
5. enforce an explicit result limit;
6. return only selected schemas;
7. never invoke the selected tool.

This is an ELO-side routing adaptation. It does not modify Hermes and does not create a second routing authority.

## Governance

The implementation remains under the existing `ELO Model/Tool Routing` owner.

The implementation path must continue through the existing governed implementation loop and Evolution Gate. This change does not promote the candidate to Core and does not create a runtime execution hook.

## Evidence

- PR #730: controlled task-quality validation.
- PR #732: repeatability validation.
- PR #733: existing ELO Review handoff.
- Issue #734: explicit implementation authorization.

The controlled evidence showed preserved task quality and a repeatable representation-footprint reduction. The 90% reduction remains a controlled representation metric and is not a production token-savings claim.

## Acceptance boundary

The implementation is accepted only as a bounded schema-selection capability. Production Hermes execution, automatic activation, canonical promotion, and Core mutation remain separate governed decisions.
