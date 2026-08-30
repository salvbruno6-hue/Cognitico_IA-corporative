# ELO — Operator ↔ GitHub Authorization Boundary v2

## Status

`PROPOSED / GOVERNANCE-CONTROLLED`

This document defines the security model for a situation in which ELO is used from a ChatGPT account that is different from the identity authorized to operate the connected GitHub account.

## Objective

A GitHub connection must not imply that every ChatGPT user/session sharing access to ELO is authorized to perform privileged repository operations.

The ELO authorization decision MUST distinguish:

1. ChatGPT/session identity, when the provider exposes an authoritative reference;
2. authenticated GitHub identity or GitHub App installation;
3. ELO operator identity;
4. capability granted to that operator;
5. sensitivity and structural impact of the requested operation.

If the ChatGPT provider does not expose a usable authoritative identity reference to the integration, ELO MUST NOT invent one or treat a declared e-mail as proof. The implementation must use the available authenticated authorization flow to establish the operator binding.

## Threat model

The protected scenario is:

`User B / different ChatGPT account → ELO session → connected GitHub credential belonging to Operator A → attempt to merge or administer repository`

The desired result is denial unless the authenticated identity and operation satisfy the ELO authorization policy and the underlying GitHub controls.

## Non-negotiable principles

### 1. Conversation is not credential

A shared conversation, prompt, project context, repository knowledge or natural-language claim MUST NOT establish identity or authorization.

### 2. E-mail is an identifier, not proof

`Planejamento_multiteiner@outlook.com` may be recorded as the intended operator identity, but an e-mail string in a prompt, commit metadata or request body is NOT sufficient proof of authorization.

Authorization MUST be established through an authoritative authentication flow and stored as an explicit ELO operator record.

### 3. GitHub permission remains authoritative for GitHub access

ELO cannot revoke permissions already granted by GitHub. The GitHub account, GitHub App, OAuth authorization and repository/organization permissions remain an independent enforcement layer.

If the connected credential has broader access than the ELO policy allows, classify the session as `ACCESS_SCOPE_VIOLATION` and do not use the excess authority.

### 4. Least privilege

Consultation and contribution capabilities MUST be separated from merge and administration capabilities.

### 5. Privilege is not transferable by context

Another ChatGPT user, another e-mail, another conversation, a copied prompt, a copied repository document or a copied ELO context MUST NOT inherit the operator's merge/admin authority.

## Persistent operator binding

The ELO operator authorization is persistent. It is NOT a per-merge approval mechanism.

For the first administrative authorization, ELO MUST provide an explicit authentication flow. Where QR is used, it is a bootstrap/authentication mechanism and MUST NOT contain a reusable administrative password or permanent secret.

Conceptual flow:

```text
ELO session
  ↓
No active operator binding
  ↓
Authenticate operator through the approved GitHub authorization flow
  ↓
Authentication succeeds
  ↓
Create persistent ELO operator binding
  ↓
ELO_ADMIN = ACTIVE
```

After the binding has been established, subsequent sessions for the same authorized operator MUST recover the existing authorization without requiring a new QR/authentication challenge for each operational merge.

A different ChatGPT/session identity MUST NOT inherit the existing ELO operator binding merely because the same GitHub credential is connected.

Revocation or replacement of the operator binding is a separate administrative operation and is not triggered by an ordinary merge.

## Operator binding record

The implementation MUST maintain an authoritative record conceptually equivalent to:

```yaml
operator_id: OP-001
status: ACTIVE
chatgpt_identity_binding: <provider-controlled identity reference when available>
github_identity_binding: <authenticated GitHub identity or GitHub App binding used to establish authorization>
authentication_binding_method: <approved authentication flow>
allowed_repositories:
  - salvbruno6-hue/Cognitico_IA-corporative
capabilities:
  - READ
  - COMMIT
  - CREATE_PR
  - MERGE_OPERATIONAL
structural_admin: false
```

Actual credentials, OAuth tokens, passwords, 2FA codes and private secrets MUST NOT be stored in this record or in the repository.

## Capability model

| Capability | Default external user | Authorized operator | Structural admin |
|---|---:|---:|---:|
| READ | yes, if GitHub permits | yes | yes |
| COMMIT | according to GitHub permission | yes | yes |
| CREATE_PR | according to GitHub permission | yes | yes |
| MERGE_OPERATIONAL | no | yes, after gates | yes |
| MERGE_STRUCTURAL | no | escalation | yes, under structural controls |
| CHANGE_RULESET | no | no | strong authorization |
| CHANGE_IDENTITY | no | no | strong authorization |
| CREATE_ELO_ADMIN | no | no | strong authorization |

## Operation classification

Before merge, ELO MUST classify the change.

### OPERATIONAL

Examples include bug fixes, tests, documentation and refactoring that preserve canonical contracts, identity boundaries, governance controls and architecture.

When all required automated gates pass and the authenticated operator has `MERGE_OPERATIONAL`, the ELO may approve the merge without requiring a second human reviewer solely because the PR exists. The ordinary operational path MUST NOT introduce an additional ELO authentication challenge for each merge once the operator binding is already active.

### STRUCTURAL

A change is structural when it changes or can weaken:

- Core architecture;
- canonical identity;
- Trust Boundary;
- authorization model;
- ELO_ADMIN creation or elevation;
- Evolution Gate;
- security controls;
- GitHub governance/rulesets;
- canonical schemas/contracts;
- authority relationships among Cognitivo, Core and Forge;
- merge authorization itself.

Structural changes MUST escalate and MUST NOT be self-approved by the same operational path that proposed them.

## Merge authorization sequence

```text
PR
 ↓
Authenticated operator binding
 ↓
Repository scope
 ↓
Capability check
 ↓
Structural-impact classification
 ↓
CI / tests / Evolution Gate
 ↓
Structural authorization only when classification requires it
 ↓
GitHub merge enforcement
```

Failure at any mandatory step is `DENY` or `BLOCKED`, never an implicit approval.

## Scenario acceptance tests

### Scenario A — first authorization of the intended operator

The intended operator enters ELO without an active operator binding.

Expected:

1. ELO shows the administrative authentication state;
2. the approved GitHub authentication flow is presented;
3. authentication succeeds;
4. ELO creates the persistent operator binding;
5. `ELO_ADMIN` becomes active.

### Scenario B — subsequent session of the same authorized operator

The authorized operator reconnects or starts a later ELO session after the persistent binding exists.

Expected:

1. ELO recovers the existing binding;
2. `ELO_ADMIN` remains active;
3. no new QR/authentication challenge is required solely to perform an operational merge;
4. GitHub's normal protections remain in force.

### Scenario C — different ChatGPT user/session, same connected GitHub credential

A different ChatGPT user/session MUST NOT inherit the existing ELO operator binding merely because a GitHub credential belonging to the authorized operator is connected.

Expected: the session remains `LIMITED` unless it has its own independently established operator authorization. It cannot use another operator's binding.

### Scenario D — spoofed e-mail/role

Supplying the authorized e-mail, `role: ELO_ADMIN`, `capabilities: ALL` or an operator identifier in request content MUST NOT grant authority.

### Scenario E — structural change by authorized operator

Even the authorized operator cannot use the operational merge path to silently change the authorization model, Trust Boundary, Ruleset, identity registry or Evolution Gate. The change must be classified as structural and escalated.

## Evidence requirements

The ELO MUST retain auditable evidence of:

- authenticated identity reference, when available;
- operator binding decision;
- repository scope;
- requested capability;
- structural classification;
- CI/evolution evidence;
- structural authorization result where required;
- GitHub merge result.

Never store authentication secrets as evidence.

## Security invariant

`CONNECTED_GITHUB != AUTHORIZED_ELO_OPERATOR != STRUCTURAL_ADMIN`

A connection provides a technical channel. It does not, by itself, establish ELO authority.

## Implementation status

This document establishes the governance contract. Runtime enforcement is **NOT CLAIMED** until the integration layer implements the operator binding and the acceptance tests pass against the real authentication path.
