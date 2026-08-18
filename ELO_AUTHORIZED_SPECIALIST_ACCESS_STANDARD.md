# ELO — Authorized Specialist Access Standard

## Purpose

Define how an authenticated specialist operating from another account may work with ELO without becoming a parallel authority.

## Identity

An authorized specialist session is identified by:

`IDENTITY + ROLE + DOMAIN + ENTERPRISE_CONTEXT + SCOPE + PERMISSIONS`

Authentication alone does not grant specialist authority.

## Default boundary

`AUTHORIZED_SPECIALIST` is domain-scoped. The specialist may consult and contribute within the assigned domain and enterprise context, subject to permissions granted by the external access-control system.

The specialist must not modify ELO Cognitivo, canonical identity, Core, canonical memory, governance, security policy, or Evolution Gate directly.

## Allowed specialist actions

- consult authorized business information;
- search domain knowledge and approved experiences;
- answer ELO GAPs;
- provide technical facts, assumptions and feedback;
- validate domain-specific results when explicitly assigned;
- propose parameters and learning candidates;
- propose changes and operational recommendations;
- participate in governed workflows.

## Restricted actions

- direct Core promotion;
- changing canonical identity or invariants;
- deleting historical evidence or experience;
- changing provenance;
- changing security or access policy;
- changing another specialist's permissions;
- bypassing review, validation or Evolution Gate;
- executing production actions outside the assigned scope.

## Learning boundary

`SPECIALIST INPUT → PROVENANCE → ANALYSIS → VALIDATION → RESULT → LEARNING CANDIDATE → EVOLUTION GATE → CORE`

The specialist contributes evidence and expertise; the specialist does not promote knowledge directly to Core.

## External account model

Specialists may operate from separate GitHub/AI accounts. ELO should treat the account as an authenticated principal and resolve its assigned role, domain, enterprise context and scope through an external authorization layer.

Do not embed personal credentials, tokens, passwords or account secrets in the repository.

## GitHub security requirement

Repository documentation cannot prevent a GitHub account from opening other repositories. That control must be enforced outside ELO by GitHub organization/repository permissions, SSO/team membership, fine-grained tokens or GitHub App installation scope.

For specialist consultation, use least-privilege credentials with access only to the ELO repository and the minimum required actions. Prefer read-only credentials for consultation and narrowly scoped write permissions for governed specialist workflows.

## Site isolation

A specialist's authorization to operate with ELO must not imply authorization to access the owner's other GitHub repositories, sites, deployments, secrets, or infrastructure. Those permissions must be denied by the external identity/access-control system unless separately granted.

## Security events

Attempts to access unauthorized repositories, internal topology, secrets, credentials, governance controls or unrelated infrastructure are security events and must not be fulfilled through the ELO consultation interface.
