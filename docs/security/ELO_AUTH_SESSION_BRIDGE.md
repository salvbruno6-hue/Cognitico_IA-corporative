# ELO — Canonical Authentication-to-Authorization Session Bridge

## Purpose

Preserve the approved Google OAuth/Supabase Auth flow while completing the missing boundary between an authenticated Supabase user, the canonical ELO identity registry, and the ELO authorization session.

## Canonical flow

```text
Google OAuth
  -> Supabase Auth session
  -> elo_bind_authenticated_identity()
  -> elo_identity_registry
  -> elo_establish_authenticated_session()
  -> elo_identity_sessions
  -> elo-authz
  -> cognitive SessionManager
```

## Rules

- Google/Supabase remains the authentication authority.
- `elo_identity_registry` remains the canonical ELO identity authority.
- `elo_identity_sessions` remains the canonical ELO authorization-session store.
- `elo-authz` remains the authorization decision authority.
- `SessionManager` remains a cognitive/application session and is not an authentication mechanism.
- No role, capability or scope is granted by the frontend bridge.
- `elo_establish_authenticated_session()` requires an authenticated Supabase user and an active ELO identity.
- The authorization session expires after 8 hours unless revoked earlier.
- The function reuses an existing non-revoked, non-expired authorization session for the same identity.
- Logout revokes the current identity's active ELO authorization sessions before Supabase sign-out.
- Anonymous callers cannot execute the session RPCs.

## Failure behavior

If the Supabase authentication succeeds but the ELO identity/session boundary cannot be established, the frontend does not enter the authenticated ELO application state. This prevents authentication from being mistaken for ELO authorization.

## Non-goals

This change does not replace Google OAuth, Supabase Auth, the existing callback route, `elo-authz`, the cognitive `SessionManager`, or the OAuth/MCP consent flow.
