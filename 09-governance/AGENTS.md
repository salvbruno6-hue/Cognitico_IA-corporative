# ELO Governance — Local Agent Rules

## Scope

This directory defines governance constraints that may override implementation convenience.

## Mandatory concepts

Where applicable, preserve:

- Tenant
- Domain
- Principal
- Policy
- Permission
- Provenance
- Audit
- Privacy
- Compliance
- Risk

## Security boundary

`department` is a business attribute, not the primary security boundary.

Tenant isolation must be explicit and testable.

## Need-to-know

The existence of data does not authorize its use. A cognitive investigation must establish relevance and authorization before accessing data across domains or organizational units.

## Audit versus provenance

Do not collapse:

AuditEvent != ProvenanceRecord != Evidence

Audit records answer what happened. Provenance records explain origin/lineage. Evidence supports a claim or conclusion.

## Human accountability

The ELO may detect, correlate, explain, recommend, and escalate. It must not silently assume authority to punish, terminate, accuse, or make irreversible personnel decisions.

## AI governance

Provider/model use must be attributable when required. Do not expose secrets or sensitive internal data to external providers without an authorized policy path.

## Change control

Security, tenant, identity, policy, privacy, or decision-authority changes require explicit review and must not be merged automatically.
