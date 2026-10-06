# Hermes MCP Issuer-Bound Authentication → ELO

## Decision

Hermes exposes issuer-bound refresh-token handling and re-authentication health as a useful security refinement. ELO adapts only the evidence boundary: credential identity must remain bound to its expected issuer and provenance must be present.

The existing ELO External Capability Gateway remains the authorization owner. This candidate does not issue, refresh, revoke, store, or authorize tokens.

## Validation contract

A binding is valid only when credential reference, issuer, bound issuer and provenance exist; issuer and bound issuer match; and re-authentication-required state is not treated as valid.

A valid assessment explicitly has authorization_permitted=False.

## Boundaries

No Hermes modification, no real MCP connection, no credential access, no business operation, no new authorization authority, and no automatic promotion.
