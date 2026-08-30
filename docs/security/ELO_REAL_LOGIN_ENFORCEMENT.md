# ELO — Real Login Enforcement

## Objective

Provide a login flow that registers an identity once, reuses that authoritative identity for subsequent sessions, and requires a new authentication event after logout or session expiry.

## Security contract

1. The provider subject is resolved from the authenticated provider context; it is not accepted as a self-declared role or capability.
2. The GitHub identity must match the authoritative registry binding.
3. Roles, capabilities, and scopes are read from the authoritative registry.
4. Every privileged operation is evaluated against the active session and its scope.
5. `MERGE` and `ADMIN` require an elevated role; ordinary users remain read/analyze/propose only.
6. Logout revokes the active session. Expiry also denies access.
7. A subsequent login creates a new session; it does not create a new user registration.
8. No test in this document claims to authenticate against GitHub or ChatGPT. Provider integration must be tested with real provider credentials in a protected CI/environment.

## UX variants

### Variant A — first access

`Provider login → resolve subject → match registry → establish session → ELO`

The registration screen is shown only when the subject has no authoritative record or when an administrator explicitly requests enrollment.

### Variant B — returning user

`Provider login → resolve subject → match registry → establish session → ELO`

No registration screen is shown.

### Variant C — logout

`Logout → revoke session → next access requires authentication`

### Variant D — session expiry

`Expired session → DENY → provider login → new session`

### Variant E — identity mismatch

`Provider subject + wrong GitHub identity → DENY`

### Variant F — valid identity, insufficient privilege

`Valid session + insufficient role/scope → DENY`

## Test matrix

| Scenario | Expected |
|---|---|
| First registered login | ALLOW + session |
| Returning login | ALLOW + new session, no re-registration |
| Wrong GitHub identity | DENY |
| Valid identity, read scope | ALLOW |
| Valid identity, missing scope | DENY |
| Analyst attempts MERGE | DENY |
| Release manager attempts MERGE | ALLOW |
| Logout then access | DENY |
| Expired session | DENY |

## Evidence boundary

The executable tests prove the local authentication/session/authorization contract. They deliberately do not fabricate external provider authentication. A future provider integration test must record the real provider subject, mapped GitHub login, authorization result, and audit event while keeping credentials and tokens out of repository history.
