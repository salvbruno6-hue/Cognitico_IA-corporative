# ELO Identity & Trust Boundary

## Purpose

Define the canonical ELO boundary between an authenticated external provider identity and semantic authority inside ELO.

Authentication is not authorization.

## Canonical model

```text
Provider assertion
      ↓
provider + subject
      ↓
authoritative identity registry
      ↓
role / enterprise context / repository scope / capabilities / active
      ↓
request claims comparison
      ↓
ALLOW / DENY
      ↓
Evolution Gate
      ↓
governed execution / protected merge
```

## Rules

1. An authenticated provider account is not automatically an ELO identity.
2. The provider subject is only the lookup anchor; it does not itself grant ELO authority.
3. Role, enterprise context, repository scope, capabilities and active state come from the authoritative identity registry.
4. Request-supplied privileged claims are assertions to be compared, never authority to be trusted.
5. Any mismatch between request claims and the authoritative record fails closed.
6. Repository scope must be explicit and must match the requested repository.
7. Capability scope must be explicit and must match the requested action.
8. Missing identity, scope or capability fails closed.
9. An inactive authoritative identity fails closed.
10. External consultation defaults to read-only through the existing access policy.
11. Specialists may provide scoped technical feedback but cannot directly promote knowledge to Core.
12. Canonical Core, identity, security and protected-merge changes require canonical authority and the applicable repository governance.
13. The ELO semantic policy does not grant or revoke GitHub permissions. GitHub/App/organization controls remain authoritative for repository access.
14. No secrets, credentials or provider tokens are stored in this contract.
15. A successful trust decision never bypasses the Evolution Gate, governed execution boundary or protected `main` ruleset.

## Decision invariants

The following invariants are mandatory and testable:

```text
same provider + subject + authoritative record
    → same resolved authority

request role/scope/capability differs from authority
    → DENY

provider subject not registered
    → DENY

identity inactive
    → DENY

repository outside authoritative scope
    → DENY

capability outside authoritative grants
    → DENY

sensitive canonical action without canonical authority
    → DENY
```

The trust layer must be deterministic for the same authoritative snapshot and request. It must not infer authority from naming conventions, repository ownership, historical success, specialist status or previous experience.

## Authority lifecycle

Identity changes follow the same governed evolution model as other canonical changes:

```text
proposal
  ↓
authoritative identity change
  ↓
tests / evidence
  ↓
Evolution Gate
  ↓
protected PR
  ↓
independent review
  ↓
merge
  ↓
post-merge validation
```

A runtime identity object is not itself a registry. A registry entry is not evidence of GitHub permission. A successful GitHub authentication is not evidence of ELO canonical authority.

## Multi-account requirement

A second GitHub account can authenticate successfully and still be denied by ELO when its provider subject is not registered or when requested identity claims do not match the authoritative registry record. Authentication alone never promotes an account to canonical authority.

## Evidence requirements

For a trust-boundary change, the minimum evidence is:

- provider subject resolution;
- authoritative-record lookup;
- scope validation;
- capability validation;
- active-state validation;
- forged-claim rejection;
- sensitive-action authority validation;
- regression tests;
- CI evidence for the evaluated commit.

Absence of CI evidence is `NO_EVIDENCE`, therefore `BLOCKED`; it is never converted to `PASS` by documentation or manual assertion.

## Security boundary

The ELO layer protects semantic authority. GitHub protects repository, credential and branch boundaries. Both layers are required; one does not substitute for the other.

## Non-goals

This contract does not implement GitHub permissions, 2FA, passkeys, SSH keys, OAuth, PATs, organization membership, branch protection or network controls. Those remain infrastructure/provider responsibilities and are governed separately by #262.
