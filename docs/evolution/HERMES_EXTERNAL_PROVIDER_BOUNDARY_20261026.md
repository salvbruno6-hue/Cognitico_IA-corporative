# Hermes external provider boundary — 2026-10-26

**Status:** CANDIDATE-ONLY  
**Owner:** ELO External Capability Gateway  
**Source evidence:** NousResearch/hermes-agent `0591b66f` / PR #144788 and catalog commit `9b904dcc`.

## Discovery

Hermes moved GitHub Copilot out of its core into a labs plugin and exposed a generic ACP external-process provider seam. The useful architectural mechanism is not Copilot itself: it is the explicit separation between canonical runtime ownership and replaceable specialist provider adapters.

## ELO adaptation

ELO already owns external capability admission through **ELO External Capability Gateway**. No provider registry, router, Core owner, memory owner, or Evolution Gate is added.

Candidate invariant:

`external provider metadata -> canonical owner check -> boundary classification -> authority check -> adapter eligibility`

Accepted boundaries are observationally limited to `adapter`, `external_process`, and `plugin`. Missing identity/owner/boundary fails closed. Any declaration of Core, Router/Routing, Memory, or Evolution Gate authority is rejected.

## Non-goals

- no Hermes mutation;
- no provider installation or activation;
- no GitHub Copilot execution;
- no ACP process execution;
- no routing mutation;
- no business operation;
- no Supabase mutation;
- no automatic promotion.

## Validation

Focused tests cover plugin and external-process adapter admission, incomplete metadata, owner mismatch, unknown boundary, and forbidden parallel authority. Promotion requires repository CI, review and Evolution Gate; production/runtime proof remains indeterminate until directly observed.
