# ELO Operator ↔ GitHub Binding Runtime

Status: IMPLEMENTATION / GOVERNED

## Purpose

Provide the persistent runtime boundary required by ELO_OPERATOR_GITHUB_BINDING_V2 without creating a second authorization authority.

The binding records the relationship between an ELO identity and an authenticated GitHub identity for a specific repository. Authorization states are persisted as short-lived grants and are consumed by execution layers.

## Invariants

- GitHub repository permission is technical access, not ELO authority.
- An ELO operator binding is persistent and repository-scoped.
- Authorization states are explicit:
  - `elo-execution-authorized`
  - `elo-commit-authorized`
  - `elo-merge-authorized`
- Codex output never creates an authorization state.
- Supabase persists canonical authorization evidence; `elo-authz` remains the authorization authority.
- Grants expire and can be revoked.
- No credentials, OAuth tokens or 2FA material are persisted in the binding.

## Runtime transition

```text
authenticated GitHub identity
        +
persistent ELO operator binding
        +
repository scope
        +
explicit ELO authorization grant
        ↓
elo-authz
        ↓
execution layer consumes explicit state
```

The binding and grant records are intentionally separate. A GitHub connection or declared role therefore cannot become an implicit commit or merge authorization.

## Current limitation

This change establishes the persistent contract and validation boundary. It deliberately does not seed a personal identity or privileged grant.

The first binding/grant must be created through an authorized canonical administrative path. No migration hard-codes a human email, GitHub account, OAuth token or privileged grant.

## Relationship to #532

Issue #532 consumes these explicit states. It must not infer them from Codex output such as `ELO_DECISION=APPROVE_COMMIT`.

The three authorization states are evidence emitted by the canonical authorization layer and remain outside the Codex decision channel.


## Canonical administrative issuer

The runtime issuer is exposed only through `elo-authz`:

- `create_operator_binding`: requires an authenticated active ELO session and the `CANONICAL_ADMIN` role; the administrator explicitly supplies the target ELO identity, GitHub user ID/login, repository and operation class.
- `issue_authorization_grant`: requires `CANONICAL_ADMIN`, an active binding, a supported authorization state, operation, repository and bounded expiry (60 seconds to 24 hours).
- Every issuance is audited by `elo-authz`.
- GitHub authentication alone does not create a binding.
- Codex output cannot create a binding or grant.
- No production grant is seeded by migration.

The issuer therefore establishes the missing administrative transition without creating a parallel authorization authority.
