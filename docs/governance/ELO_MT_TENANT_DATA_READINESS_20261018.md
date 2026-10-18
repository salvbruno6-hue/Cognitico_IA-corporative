# ELO — MT Tenant Data Readiness — 2026-10-18

Status: `GAP_HIGH / DATA BOUNDARY NOT LIVE`

## Scope

This evidence is narrower than the MT permissive-policy inventory.

- The authorization gap currently covers 168 literal-TRUE policy objects across 71 `mt_*` tables.
- The live catalog currently contains **31** `mt_*` tables with a direct `tenant_id` column.
- Those are different sets and must not be conflated.

## Live evidence

The read-only probe `supabase/health/elo_mt_tenant_data_readiness.sql` currently reports:

| Signal | Value |
|---|---:|
| MT tables with direct `tenant_id` | 31 |
| Estimated populated direct-tenant MT tables | 1 |
| Rows in `mt_tenants` | 0 |
| Active rows in `mt_tenants` | 0 |
| Rows in `mt_ordens_reparo` | 133 |
| Repair rows with non-null `tenant_id` | 0 |
| Repair rows with null `tenant_id` | 133 |
| Distinct tenant IDs in repair rows | 0 |

The only currently populated direct-tenant MT table identified by live statistics is `mt_ordens_reparo`. Exact counts on that table confirm that none of its persisted rows has a tenant assignment.

## Interpretation

The schema contains tenant-shaped columns and foreign keys, but tenant ownership is not yet persisted in operational data. Therefore the existence of `tenant_id` does not prove a live tenant-isolation contract.

A future policy such as `row.tenant_id = authorized_tenant` cannot be promoted safely before the data-governance problem is solved. With the current state it would make all 133 existing repair rows inaccessible through the governed human path.

## Prohibited inference

This evidence does not authorize any of the following:

- creating a synthetic/default tenant;
- mapping all current rows to `ENTERPRISE/MULTITEINER` automatically;
- inferring tenant from repository scope, email, role or successful login;
- backfilling `tenant_id` without provenance;
- removing service-role/server access;
- replacing permissive policies before allow/deny behavior is proven.

## Decision boundary

Before a tenant-aware MT pilot can become live, governance must identify the real tenant entity (or entities), establish how each existing operational record maps to it, and separately authorize the operator identity/scope/capability contract.

Until then, the safe autonomous work is limited to read-only tracing, diagnostics, tests and provenance reconstruction.
