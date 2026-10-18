# ELO — MT Authorization Readiness — 2026-10-18

Status: `GAP_HIGH / PREPARED, NOT LIVE`

## Purpose

Record the live prerequisites that must exist before legacy permissive `mt_*` RLS policies can be replaced by governed identity/scope/capability authorization.

This document does not assign an identity, create a scope, grant a capability, choose a tenant mapping or authorize a policy rewrite.

## Canonical boundary

GitHub remains the operational authority for authorization contracts and migrations. Supabase remains the persistent authority for live identity, scope, capability and policy evidence.

The existing decisions remain authoritative:

- `ELO_AUTHORITY_SEPARATION_DECISION_20261009.md`: operational table writes require registered Google identity -> active role -> explicit scope -> domain-specific capability -> `elo-authz` ALLOW -> bounded writer/action.
- `ELO_OKR_ENTERPRISE_TENANT_SCOPE_DECISION_20261009.md`: `ENTERPRISE/MULTITEINER` is prepared but is not live tenant authority by itself.
- `RLS_AUTHORIZATION_AUDIT_2026-10-08.md`: literal-TRUE MT policies do not certify tenant isolation or ordinary-user authorization.

## Live evidence

The read-only probe `supabase/health/elo_mt_authorization_readiness.sql` currently reports:

| Signal | Live value | Interpretation |
|---|---:|---|
| Legacy literal-TRUE MT policy objects | 168 | unresolved authorization surface |
| MT tables represented | 71 | broad legacy scope |
| Eligible active Google-bound identities | 1 | identity prerequisite exists |
| Eligible identities linked to `ENTERPRISE/MULTITEINER` | 0 | tenant boundary is not activated |
| Eligible identities with any active DOMAIN scope | 0 | no live domain authorization scope |
| Eligible identities receiving `PCP_READ` or `PCP_UPDATE` through active roles | 0 | no live PCP operator capability |

Therefore a tenant-aware/domain-aware replacement policy cannot yet be made live without either denying all human operators or inventing authorization semantics. Neither is acceptable as an implicit migration side effect.

## Pilot evidence — `mt_ordens_reparo`

`mt_ordens_reparo` is the best-observed pilot candidate because it has real data/activity and a direct `tenant_id`, but the current consumer evidence must be separated by authority path:

- canonical Forge adapter `elo-virtual-core/integracoes/supabase_elo_forge.py` is server-side, read-only and uses the service-role credential;
- repository search shows governed repair-domain consumption through Forge and PCP analytical views rather than a proven direct authenticated browser writer;
- live dependent views `v_elo_pcp_cobertura_demanda_externa` and `v_indice_modelos_reparados_mes` are `security_invoker=true` and currently have no effective SELECT grant to `anon` or `authenticated`;
- the observed 24-hour Supabase request-log window contained no direct `/rest/v1/mt_ordens_reparo` request;
- absence from one log window is not proof that no legitimate client consumer exists, so it is evidence for narrowing the pilot, not permission to revoke access automatically.

## Existing capability model

The canonical model already contains `PCP_READ` and `PCP_UPDATE`. They must not be automatically generalized to all MT resources. A repair-table write contract must first prove that the resource is PCP-governed and identify the exact DOMAIN scope that governs it.

Creating a new repair capability or tenant registry merely to make the pilot work is prohibited unless a later governed decision proves the existing model insufficient.

## Required conditions before the first MT policy rewrite

All of the following must be proven for the selected pilot resource:

1. the real human/client consumer is identified, or client access is explicitly classified as unsupported;
2. the selected identity is explicitly linked to the intended live scope by authorized governance action;
3. the selected role already carries the required existing capability, or a separate governed capability decision is approved;
4. `elo-authz` can evaluate the action/resource/scope contract and fail closed when any prerequisite is absent;
5. allow and deny behavior is covered by tests before the legacy permissive policy is removed;
6. service-role/server workflows are shown not to depend on the authenticated policy path;
7. post-deployment Health Gate evidence confirms the legacy gap decreased without expanding another authority path.

## Current decision boundary

The technical work can continue through read-only tracing and test design. The first assignment of an identity to `ENTERPRISE/MULTITEINER`, a DOMAIN scope, or a role/capability combination is a real authorization decision and must not be inferred from the existence of the identity itself.
