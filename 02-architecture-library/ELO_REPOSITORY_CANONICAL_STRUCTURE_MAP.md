# ELO Repository Canonical Structure Map

## Purpose

Define the semantic owner of each top-level directory and the controlled consolidation of historical Portuguese/English variants.

## Authority model

The physical directory is not itself authority. Authority is determined by:

1. approved baseline/constitution;
2. ADRs;
3. canonical artifact metadata;
4. implementation evidence;
5. tests and verification.

## Canonical ownership

| Path family | Semantic owner | Intended content | Treatment |
| --- | --- | --- | --- |
| `00-enterprise-manifest/` | Enterprise Constitution | permanent principles and constitutional artifacts | canonical |
| `00-empresa-manifesto/` | Enterprise Constitution | historical Portuguese foundation | migration source; no new artifacts |
| `01-meta-architecture/` | Meta Architecture | architectural relationships and patterns | canonical |
| `01-meta-arquitetura/` | Meta Architecture | historical Portuguese meta architecture | migration source; content review required |
| `02-architecture-library/` | Architecture Library | canonical architecture details, maps, standards | canonical |
| `03-process-library/` | Process | process definitions | canonical |
| `04-knowledge-handbook/` | Knowledge | knowledge handbook and operating guidance | canonical |
| `05-cognitive-platform/` | Cognitive Platform | cognitive boundaries and normative design | canonical |
| `05-cognitivo-plataforma/` | Cognitive Platform | historical Portuguese cognitive material | migration source; content review required |
| `06-knowledge-engineering/` | Knowledge Engineering | acquisition, normalization, retrieval, evidence | canonical |
| `07-data-engineering/` | Data Engineering | data contracts, schemas, lineage, quality | canonical |
| `07-engenharia-de dados/` | Data Engineering | historical Portuguese data engineering | migration source; content review required |
| `08-ai/` | AI | provider and model governance | canonical |
| `09-governance/` | Governance | security, policy, privacy, provenance, audit | canonical |
| `10-adr/` | ADR | architectural decisions | canonical |
| `11-models-library/` | Models | reusable models | canonical |
| `11-modelos/` | Models | historical Portuguese model library | migration source; review before removal |
| `12-system-engineering/` | System Engineering | runtime and deployment | canonical |
| `12-sistemas/` | System Engineering | historical Portuguese system engineering | migration source; review before removal |
| `13-reference-architecture/` | Reference Architecture | reusable reference structures | canonical |
| `13-referências/` | Reference Architecture | historical Portuguese references | migration source; review before removal |
| `14-roadmap/` | Roadmap | future work and evolution | canonical |
| `14-roteiros/` | Roadmap | historical Portuguese roadmap | migration source; review before removal |
| `15-assets/` | Assets | reusable assets | canonical |
| `15-ativos/` | Assets | historical Portuguese assets | migration source; review before removal |
| `Docs/` | Documentation | evolution/supporting docs | supporting only unless explicitly canonical |
| `src/elo/` | Executable ELO | current implementation core | canonical executable root |
| `tests/` | Verification | automated tests and behavioral evidence | canonical test root |

## Consolidation policy

ADR `ADR-2026-08-19-BILINGUAL-TREE-CONSOLIDATION.md` approves controlled consolidation. The target state is one canonical owner per concept. Existing Portuguese content must first be classified as equivalent, complementary, conflicting, exclusive, or historical before migration/removal.

No deletion is authorized solely because a directory is Portuguese. Content must be preserved or migrated before the historical path is removed.

## Migration rule

For each pair:

1. inventory files;
2. compare semantic purpose and content;
3. migrate equivalent/complementary content into the canonical owner;
4. resolve conflicts explicitly;
5. update references/indexes;
6. run CI and relevant gates;
7. mark the historical path DEPRECATED/SUPERSEDED or remove it only when empty and safe.

## Executable rule

`src/elo/` is the current executable nucleus. Historical trees do not create a second runtime Core.

## Target state

`one concept → one canonical owner → preserved provenance → no parallel authority`.

Portuguese and English are documentation languages, not independent architectural authorities.
