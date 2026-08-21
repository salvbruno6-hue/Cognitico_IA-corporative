# ELO Identity & Trust Boundary

## Purpose

Define the canonical ELO boundary between an authenticated external provider identity (for example, GitHub) and authority inside ELO.

Authentication is not authorization.

## Model

`Provider Identity → ELO Identity → Authoritative Identity Record → Role/Context/Scope/Capabilities → Action → Evolution Gate`

## Rules

1. An authenticated GitHub account is not automatically an ELO identity.
2. The provider subject is only the lookup anchor; it does not itself grant ELO authority.
3. Role, enterprise context, repository scope, capabilities and active state are authoritative registry attributes, not trusted request claims.
4. A request whose identity claims differ from the authoritative identity record fails closed.
5. Repository scope must be explicit.
6. Capability scope must be explicit.
7. Missing identity, scope or capability fails closed.
8. External consultation defaults to read-only through the existing access policy.
9. Specialists may provide scoped technical feedback but cannot directly promote to Core.
10. Canonical Core, identity, security and protected-merge changes require canonical authority.
11. The ELO policy does not grant or revoke GitHub permissions; GitHub/App/organization controls remain authoritative for repository access.
12. No secrets, credentials or provider tokens are stored in this contract.
13. A successful trust decision never bypasses the Evolution Gate or governed execution boundary.

## Security boundary

The ELO layer protects semantic authority. GitHub protects the actual repository and credential boundary. Both layers are required; one does not substitute for the other.

## Multi-account requirement

A second GitHub account can be authenticated successfully and still be denied by ELO when its provider subject is not registered or when its requested identity claims do not match the authoritative registry record. Authentication alone never promotes an account to canonical authority.

## Non-goals

This contract does not attempt to implement GitHub permissions, 2FA, passkeys, SSH keys, OAuth, PATs, organization membership, branch protection or network controls. Those remain infrastructure/provider responsibilities.
