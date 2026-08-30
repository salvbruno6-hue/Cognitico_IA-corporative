# ELO — Google Authentication Flow

## Objective

Provide a low-friction first-login experience while keeping authentication separate from ELO authorization.

Google proves the external identity. ELO assigns the internal identity, role, capabilities, and scopes.

## Canonical flow

1. User selects `Continuar com Google`.
2. OAuth authorization is performed by the configured identity provider/Supabase Auth.
3. ELO accepts the callback only after the provider response is validated by the authentication layer.
4. The authoritative provider subject is mapped to one ELO identity.
5. If the ELO identity does not exist, bootstrap it once according to provisioning policy.
6. If it already exists, reuse the existing identity; do not create a second registration.
7. Create a session with an explicit expiration and server-side revocation state.
8. Every privileged operation is independently checked against role, capability, and scope.

## Required denial blocks

The request must be denied when any of these conditions is detected:

- provider issuer is not the configured issuer;
- token audience/client identifier is not the configured audience;
- provider subject is absent or cannot be mapped to an ELO identity;
- the provider subject is mapped to a different authoritative GitHub login than the one asserted by the session context;
- identity is inactive, suspended, or revoked;
- OAuth state/nonce/PKCE validation fails;
- session is expired or revoked;
- requested capability is absent;
- requested scope is outside the identity scope;
- operation is `MERGE` or `ADMIN` and the identity does not hold an elevated role;
- a second identity would be created for an already-authoritative provider subject.

## Comfortable login variants

### First access

`Google -> authenticate -> create/link ELO identity -> session -> ELO`

### Returning access

`Google -> authenticate -> find existing provider subject -> new session -> ELO`

No second registration is required.

### Logout

`logout -> revoke session -> privileged requests denied`

### Expired session

`expired session -> re-authentication required -> new session`

### Account mismatch

`valid Google authentication + wrong ELO/GitHub binding -> DENY`

### Limited user

`valid Google authentication + ANALYST role -> allowed scopes only; MERGE/ADMIN denied`

## Security boundary

This document does not claim that ChatGPT-to-GitHub identity binding is a real external integration. That claim requires protected provider credentials, a configured integration environment, and runtime evidence.

CI tests may validate the deterministic policy contract. Real provider tests must run separately with protected secrets and must never print tokens, authorization codes, client secrets, refresh tokens, or session cookies.

## Acceptance evidence

A production integration is considered demonstrated only when evidence shows:

- successful Google authentication;
- stable provider-subject-to-ELO-identity mapping;
- reuse of the existing identity on subsequent login;
- logout/session revocation;
- expiration enforcement;
- denial for mismatched identity;
- denial for insufficient capability/scope;
- denial for unauthorized MERGE/ADMIN;
- no secret material in logs or artifacts.
