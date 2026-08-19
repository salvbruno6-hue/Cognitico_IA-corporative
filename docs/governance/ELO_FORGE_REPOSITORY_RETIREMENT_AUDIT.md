# ELO-Forge External Repository Retirement Audit

**Status:** CONTROLLED TRANSITION — external repository not yet deleted

## 1. Architectural decision

`Cognitico_IA-corporative` is the sole canonical repository for the ELO architecture and operational cognitive source.

The internal `forge/` directory is the canonical Forge layer. It is part of the ELO Cognitivo repository and is not a second architectural authority.

The external repository `salvbruno6-hue/ELO-Forge` is treated only as a historical/transition source. It must not be used as a canonical dependency.

## 2. External repository observed state

The external repository currently contains, among other paths:

- `ELO_Blueprint_v1.0.md`
- `agents/`
- `api/`
- `automation/`
- `dashboards/`
- `doc/`
- `docs/`
- `prompts/`
- `schemas/`
- `sql/`
- `supabase/`

It is public, uses `main`, contains two open issues, and is still described by its GitHub metadata as an operational official ELO source. That description is obsolete relative to the current architecture and must not be interpreted as authority.

## 3. Disposition matrix

| External material | Disposition | Rule |
|---|---|---|
| Architectural concepts already represented in `01-meta-architecture/` | ALREADY MIGRATED | Do not duplicate. Reconcile only if a gap is proven. |
| Internal Forge role, promotion and skill registry | ALREADY MIGRATED | Canonical owner is `forge/`. |
| Prompts and agent ideas | REVIEW / EXTRACT | Migrate only if useful and compatible with the canonical contracts. |
| API/adapters | REVIEW / EXTRACT | Promote only through existing Source Resolver/adapter boundaries. |
| Automation | REVIEW / EXTRACT | Must use canonical governance and execution boundaries. |
| Schemas | REVIEW / EXTRACT | Compare against current canonical schemas before promotion. |
| SQL / migrations / operational database artifacts | DO NOT AUTO-MIGRATE | Require explicit architectural and operational validation; existence in Forge is not evidence of canonical validity. |
| Supabase artifacts | DO NOT AUTO-MIGRATE | Validate against current Core/application/infrastructure boundaries. |
| Dashboards | REVIEW / EXTRACT | Treat as application/observability material, not cognitive authority. |
| Historical documents | ARCHIVE / REFERENCE | Preserve provenance where useful; do not make historical text canonical automatically. |
| Duplicate implementations | REJECT / SUPERSEDE | Prefer the current canonical owner in Cognitico. |

## 4. Deletion preconditions

The external repository must not be deleted until all of the following are true:

- [ ] Search in `Cognitico_IA-corporative` finds no required runtime dependency on `ELO-Forge`.
- [ ] No workflow, script, adapter, submodule, badge, documentation link, webhook or deployment references the external repository as an operational dependency.
- [ ] The two open external issues are reviewed and either migrated or explicitly closed as historical/non-canonical.
- [ ] Relevant source material has been classified as `ALREADY_MIGRATED`, `REVIEW/EXTRACT`, `ARCHIVE`, or `REJECT/SUPERSEDE`.
- [ ] Required provenance/commit references have been preserved for material that influenced the canonical repository.
- [ ] Canonical CI/gates pass after the final reconciliation.
- [ ] The Cognitivo repository documentation identifies the internal Forge as the canonical Forge layer.
- [ ] A final no-dependency audit is recorded.

## 5. Consequence of deletion

Deleting the external repository does **not** remove the Forge capability from ELO. The internal `forge/` layer remains part of `Cognitico_IA-corporative`.

The primary consequence is loss of direct GitHub navigation to the external repository's independent history and artifacts. Therefore useful historical provenance must be preserved before deletion.

Deletion must not be used to hide divergence. Divergent material must be classified and recorded first.

## 6. Canonical flow after retirement

```text
Cognitico_IA-corporative
│
├── Canonical / Cognitive
│   └── Core
│
├── forge/
│   ├── construction
│   ├── experiments
│   ├── specialist skills
│   ├── tests
│   └── promotion candidates
│
└── Applications / Infrastructure
```

```text
Forge construction
      ↓
Validation
      ↓
Evolution Gate
      ↓
Promote / Adapt / Reject
      ↓
Canonical ELO
```

## 7. Non-negotiable rules

1. The external repository is never a second Core.
2. The external repository is never a source of canonical truth after retirement.
3. SQL, migrations and operational data are not promoted merely because they exist externally.
4. Historical evidence is not silently rewritten.
5. Deletion occurs only after the no-dependency gate passes.
6. The internal Forge remains governed by the Cognitivo canonical contracts.

## 8. Final retirement state

Target state:

`ELO-Forge external = DEPRECATED / ARCHIVED / DELETED`

`Cognitico_IA-corporative/forge = CANONICAL INTERNAL FORGE LAYER`

This document is the retirement control record and should remain in the canonical repository after the external repository is retired.
