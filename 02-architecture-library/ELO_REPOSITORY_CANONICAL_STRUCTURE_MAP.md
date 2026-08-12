# ELO Repository Canonical Structure Map

## Purpose

Define the current semantic role of each top-level directory so humans and AI agents can navigate the ELO repository without interpreting similar Portuguese/English directories as independent authorities.

## Authority model

The physical directory is not itself authority. Authority is determined by:

1. approved baseline/constitution;
2. ADRs;
3. canonical artifact metadata;
4. implementation evidence;
5. tests and verification.

## Current structure

| Path family | Semantic owner | Intended content | Current treatment |
| --- | --- | --- | --- |
| `00-enterprise-manifest/` | Enterprise Constitution | permanent principles and constitutional artifacts | canonical candidate |
| `00-empresa-manifesto/` | Historical/Portuguese enterprise foundation | legacy foundation material | preserve; do not create new duplicates |
| `01-meta-architecture/` | Meta Architecture | architectural relationships and patterns | canonical candidate |
| `01-meta-arquitetura/` | Historical/Portuguese meta architecture | legacy material | preserve; consolidate by ADR later |
| `02-architecture-library/` | Architecture Library | canonical architecture details, maps, standards | active canonical architecture library |
| `03-process-library/` | Process | process definitions | active |
| `04-knowledge-handbook/` | Knowledge | knowledge handbook and operating guidance | active |
| `05-cognitive-platform/` | Cognitive Platform | cognitive boundaries and normative design | active canonical cognitive design |
| `05-cognitivo-plataforma/` | Historical/Portuguese cognitive platform | legacy material | preserve; no new duplicates |
| `06-knowledge-engineering/` | Knowledge Engineering | acquisition, normalization, retrieval, evidence | active |
| `07-data-engineering/` | Data Engineering | data contracts, schemas, lineage, quality | active |
| `07-engenharia-de dados/` | Historical/Portuguese data engineering | legacy material | preserve; no new duplicates |
| `08-ai/` | AI | provider and model governance | active |
| `09-governance/` | Governance | security, policy, privacy, provenance, audit | active |
| `10-adr/` | ADR | architectural decisions | active canonical decisions |
| `11-models-library/` or `11-modelos/` | Models | reusable models | reconcile naming later |
| `12-system-engineering/` or `12-sistemas/` | System Engineering | runtime and deployment | reconcile naming later |
| `13-reference-architecture/` or `13-referências/` | Reference Architecture | reusable reference structures | reconcile naming later |
| `14-roadmap/` or `14-roteiros/` | Roadmap | future work and evolution | roadmap only |
| `15-assets/` or `15-ativos/` | Assets | reusable assets | reconcile naming later |
| `Docs/` | Documentation | evolution/supporting docs | supporting only unless explicitly made canonical |
| `src/elo/` | Executable ELO | current implementation core | canonical executable root for current evolution |
| `tests/` | Verification | automated tests and behavioral evidence | canonical test root |

## Naming rule

Do not create a new top-level folder when an existing semantic owner already exists.

Before renaming/consolidating Portuguese/English variants:

- inventory files;
- identify references;
- check links/imports;
- assess history/provenance;
- define target authority;
- create ADR when structural impact is material;
- migrate with compatibility where required.

## Executable rule

`src/elo/` is the current executable nucleus referenced by the active README and governance model. The historical `ELO/` tree from PR #1 is not automatically canonical.

## Future consolidation

A future ADR should decide whether Portuguese/English duplicate directory families are:

- consolidated;
- redirected through canonical README/index files;
- formally deprecated;
- or retained as historical archives.
