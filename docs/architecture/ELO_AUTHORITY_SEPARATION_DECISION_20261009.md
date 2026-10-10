# ELO — Structural vs Delegated Authority Boundary

Status: PREPARED / NOT LIVE
Date: 2026-10-09

## Decision

Only ADM/Developer authority may create or alter ELO capabilities, security policy, Core/canonical structures, role/scope definitions, permission models, protected promotion paths or other system-level governance.

Ordinary authorized operators such as Samuel may use existing capabilities assigned to them through the canonical identity + role + scope + `elo-authz` model, but they do not acquire structural authority by receiving operational or strategic capabilities.

## Structural-only authority

Reserved to the existing ADM/Developer authority boundary:

- `ADMIN`;
- `CANONICAL_WRITE`;
- create/alter capability definitions;
- create/alter role definitions;
- create/alter scope definitions or permission policy;
- modify Core/cognitive identity/security policy;
- promote knowledge to canonical Core;
- protected structural maintenance;
- system configuration and governance changes.

`strategic_okr_write` maps to `CANONICAL_WRITE` and therefore remains structural-only.

## Delegable operator capabilities

A registered Google identity may receive these only when explicitly assigned and when the requested scope/resource also passes `elo-authz`:

- `READ` / `PORTAL_READ`;
- `PCP_READ`;
- `PCP_UPDATE` for PCP-governed resources only;
- `PROPOSE` for Objective/KR proposals;
- `REVIEW` for governed review/binding operations;
- `APPROVE` for Objective/KR approval workflows;
- other domain-specific capabilities explicitly authorized later.

These capabilities do not grant permission to create capabilities, change roles/scopes, change security policy or perform canonical structural writes.

## Samuel / ordinary authorized operator model

Samuel and future explicitly authorized operators may:

- act in PCP when they hold the PCP scope + matching capability;
- use `strategic_okr` read/query capabilities;
- propose/review/approve Objective/KR according to `PROPOSE`/`REVIEW`/`APPROVE`;
- modify governed operational data only through a domain-specific writer/action for which they hold the matching capability and scope;
- receive `ENTERPRISE/MULTITEINER` tenant scope;
- execute `GovernedOrchestrator` actions that resolve to capabilities they are authorized to use.

They may not:

- create or alter ELO capability definitions;
- create or alter roles/scopes/authorization policy;
- use `ADMIN`;
- use `CANONICAL_WRITE`;
- perform Core/security/system-governance changes;
- bypass `elo-authz` with `service_role`, direct table access, prompt-provided role or caller-provided capability.

## Table-write rule

"Alter governed tables" never means generic SQL/table mutation authority.

It means:

```text
registered Google identity
  -> canonical ELO identity
  -> active role
  -> explicit scope
  -> domain-specific capability
  -> elo-authz ALLOW
  -> bounded writer/action
  -> only approved table/resource
```

Examples:

- PCP data update -> `PCP_UPDATE` + PCP scope;
- Objective proposal -> `PROPOSE` + `ENTERPRISE/MULTITEINER` + objective resource receipt;
- KR review/binding -> `REVIEW` + tenant/resource receipt;
- KR approval -> `APPROVE` + tenant/resource receipt;
- canonical/system write -> denied unless structural ADM/Developer authority.

## Important capability collision control

`APPROVE` may also appear in critical system actions. Receiving `APPROVE` for strategic workflows does not grant structural approval automatically. Critical system actions must continue to require the existing additional canonical-admin boundary in `elo-authz`.

## Identity prerequisite

Authorization is available only to identities already registered canonically and authenticated through Google:

- active `elo_identity_registry` row;
- `provider = google`;
- valid `auth_user_id`;
- `authorized_email` equals the authenticated Google email.

A Google Auth user that is not yet linked to `elo_identity_registry` remains unable to act through governed ELO flows.

## Live state

No role/capability/scope assignment, identity link, Edge Function deployment or database permission mutation is applied live by this decision.
