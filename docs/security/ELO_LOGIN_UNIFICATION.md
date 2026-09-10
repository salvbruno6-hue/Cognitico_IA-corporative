# ELO — Unified Login Boundary

## Decision

The existing ELO login page is the single user-facing entry point. The Google OAuth implementation originally completed for GitHub Pages is reused beneath that page; no second login UI or parallel authentication authority is introduced.

## Canonical flow

```text
ELO Login page
  -> Google OAuth
  -> Supabase Auth
  -> authenticated user
  -> elo_bind_authenticated_identity()
  -> elo_identity_registry
  -> elo_establish_authenticated_session()
  -> elo_identity_sessions
  -> elo-authz
  -> ELO Web / ELO Cognitive
  -> Hermes / Symbiont (downstream execution only)
```

## Existing assets reused

- `frontend/src/auth/ELOGoogleLogin.tsx`
- `frontend/src/auth/ELOAuthCallback.tsx`
- `frontend/src/auth/ELOOAuthConsent.tsx`
- `frontend/src/App.tsx`
- `frontend/src/auth/README_PAGES_OAUTH.md`
- `docs/security/ELO_GOOGLE_AUTH_FLOW.md`
- `docs/security/ELO_AUTH_SESSION_BRIDGE.md`
- `public.elo_identity_registry`
- `public.elo_identity_sessions`
- `public.elo_bind_authenticated_identity()`
- `public.elo_establish_authenticated_session()`
- `public.elo_revoke_authenticated_session()`
- `supabase/functions/elo-authz`

## Boundary rules

1. Google/Supabase authenticates the external identity.
2. `elo_identity_registry` identifies the corresponding ELO identity.
3. The existing ELO login page does not assign role, capability, scope, tenant, or administrative privilege.
4. `elo-authz` remains the authorization authority.
5. ELO Web cannot bypass the existing authentication/session bridge.
6. ELO Cognitive receives authenticated/authorized context; it does not become an authentication mechanism.
7. Hermes and Symbiont cannot establish or escalate identity and authorization.
8. A returning provider subject reuses the existing ELO identity; no duplicate user registration is created.
9. GitHub Pages and Vercel may use the same identity boundary while their redirect/base paths differ.
10. Any mismatch or missing authoritative identity fails closed.

## Intended implementation

The current ELO login UI remains visually and functionally the entry page. Existing Google/Supabase code is the implementation beneath it. The next application integrations should consume the established session/authorization result rather than implement a second login flow.

## Non-goals

This document does not create a new user table, a new OAuth provider, a second role system, or a browser-side authorization store.
