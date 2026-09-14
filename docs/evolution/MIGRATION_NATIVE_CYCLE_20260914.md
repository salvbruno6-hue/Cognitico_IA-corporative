# ELO — Native Migration Cycle 2026-09-14

## Decision

Operationalize Migration as a native, provider-neutral Forge capability. It prepares and verifies transformations; it does not become a database, deployment, or migration authority.

## Ecosystem relation

`Forge migration plan → authorized adapter → infrastructure/data system → before/after evidence → verification → Governance/Evolution Gate`

The existing ELO data model remains canonical. For the current quarantine/repair requirement, the live Supabase schema already contains `elo_dom_return`, `elo_return_inspection`, `elo_repair_order` and `elo_repair_event`, including the return → inspection → repair relationships. Therefore a new `quarentena_reparos` table is not promoted merely because the operational label differs.

Classification for the proposed quarantine control: **EXTEND/REUSE**, pending any domain-specific evidence that an additional transaction is genuinely required.

## Native capability

`src/elo/forge/migration.py` provides:

- deterministic SHA-256 before/after checksums;
- tenant-scoped migration identity;
- source and target references;
- explicit rollback reference;
- idempotency key;
- provenance;
- fail-closed rejection of secret-bearing metadata;
- verification requiring matching before state, expected after state and rollback availability.

It deliberately does not execute SQL, mutate Supabase, deploy infrastructure, or bypass Governance.

## Instructions / invariants

1. Inventory the target system before migration.
2. Reuse/extend existing canonical structures before creating new ones.
3. Preserve tenant and source provenance.
4. Never treat a changed label as proof of a new entity.
5. Require before/after evidence and deterministic checksum comparison.
6. Require a tested or explicitly available rollback path.
7. Missing rollback or checksum drift is `BLOCKED`, never PASS.
8. Secrets are never accepted as migration provenance.
9. Execution remains with the authorized infrastructure/data adapter.
10. Any structural promotion follows Evolution Gate and repository governance.

## Potencialização para o ELO

This implementation gives ELO a reusable mechanism for **safe transformation of data and systems**: it can compare states objectively, detect migration drift, preserve rollback readiness and produce evidence for governance. This strengthens future schema/data evolution without creating another authority over Supabase or infrastructure.

## Current quarantine case

The live schema inspection found canonical repair structures already connected to the operational flow. The proposed monthly quarantine indicator should therefore derive from the existing return/inspection/repair lifecycle where its semantics match, rather than creating a parallel transaction table by name alone. Historical spreadsheet records remain evidence to reconcile against canonical records; they are not inserted as synthetic production facts by this cycle.
