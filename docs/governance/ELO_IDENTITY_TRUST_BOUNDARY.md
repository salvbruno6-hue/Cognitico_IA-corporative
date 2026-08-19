# ELO Identity & Trust Boundary

## Purpose

Define the canonical ELO boundary between an authenticated external provider identity (for example, GitHub) and authority inside ELO.

Authentication is not authorization.

## Model

`Provider Identity → ELO Identity → Role → Enterprise Context → Repository Scope → Capability → Action → Evolution Gate`

## Rules

1. An authenticated GitHub account is not automatically an ELO identity.
2. Repository scope must be explicit.
3. Capability scope must be explicit.
4. Missing identity, scope or capability fails closed.
5. External consultation defaults to read-only through the existing access policy.
6. Specialists may provide scoped technical feedback but cannot directly promote to Core.
7. Canonical Core, identity, security and protected-merge changes require canonical authority.
8. The ELO policy does not grant or revoke GitHub permissions; GitHub/App/organization controls remain authoritative for repository access.
9. No secrets, credentials or provider tokens are stored in this contract.
10. A successful trust decision never bypasses the Evolution Gate or governed execution boundary.

## Security boundary

The ELO layer protects semantic authority. GitHub protects the actual repository and credential boundary. Both layers are required; one does not substitute for the other.

## Multi-account requirement

A second GitHub account can be authenticated successfully and still be denied by ELO when its provider subject, repository scope or capability is not registered. This prevents an authenticated identity from being treated as canonical merely because it can reach a provider.

## Non-goals

This contract does not attempt to implement GitHub permissions, 2FA, passkeys, SSH keys, OAuth, PATs, organization membership, branch protection or network controls. Those remain infrastructure/provider responsibilities.
