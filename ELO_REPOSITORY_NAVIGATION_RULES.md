# ELO — Repository Navigation and Authority Rules

## 1. Purpose

This document defines how humans and AI agents must interpret the ELO repository structure.

The repository currently contains both English and Portuguese directory variants in some layers. This is a known structural condition. Until an explicit consolidation decision is made, agents must not assume that two similarly named directories represent two independent architectures.

The current root README identifies the principal high-level structure and `src/elo/` as the implementation core.

## 2. Authority model

Folder location is a navigation signal, not sufficient proof of authority.

Authority is determined in this order:

1. Constitutional/enterprise manifest;
2. approved architecture baseline;
3. approved ADR;
4. canonical contract/schema;
5. governance/security policy;
6. implementation;
7. tests and runtime evidence;
8. roadmap/proposal.

When two artifacts conflict, the lower-authority artifact must not silently override the higher-authority artifact.

## 3. Semantic layers

### 00 — Enterprise Manifest

Purpose:
- enterprise identity;
- mission;
- principles;
- constitutional boundaries;
- organizational intent.

Do not place implementation details here.

### 01 — Meta Architecture

Purpose:
- architectural principles;
- meta-models;
- architectural language;
- system-of-systems framing.

Do not place executable implementation here.

### 02 — Architecture Library

Purpose:
- canonical architecture;
- component boundaries;
- architecture contracts;
- reference structures;
- architecture patterns.

This layer is normative when an artifact is explicitly approved as baseline/canonical.

### 03 — Process Library

Purpose:
- business processes;
- workflows;
- process states;
- responsibilities;
- operational procedures.

Do not use this layer as a substitute for domain contracts or security policy.

### 04 — Knowledge Handbook

Purpose:
- curated knowledge;
- manuals;
- reference knowledge;
- organizational explanations;
- validated knowledge material.

Distinguish source knowledge from lessons learned and recommendations.

### 05 — Cognitive Platform

Purpose:
- Cognitive Core;
- Context;
- Knowledge interaction;
- Memory interaction;
- Reasoning;
- Evidence;
- Recommendation;
- Decision support;
- Agent boundaries;
- cognitive orchestration.

This layer describes the cognitive platform. Executable implementation belongs in `src/elo/` unless an explicit architecture decision says otherwise.

### 06 — Knowledge Engineering

Purpose:
- knowledge ingestion;
- normalization;
- semantic structures;
- retrieval preparation;
- provenance of knowledge;
- knowledge quality.

Do not silently convert external information into authoritative organizational truth.

### 07 — Data Engineering

Purpose:
- data contracts;
- ingestion;
- transformation;
- quality;
- storage;
- pipelines;
- data lifecycle.

Data engineering must preserve tenant/domain boundaries when applicable.

### 08 — AI

Purpose:
- AI provider architecture;
- model policies;
- AI Gateway concepts;
- provider abstraction;
- evaluation;
- model governance.

Do not embed provider-specific behavior into unrelated cognitive components.

### 09 — Governance

Purpose:
- security;
- identity;
- tenant isolation;
- policy;
- privacy;
- compliance;
- audit;
- provenance;
- risk controls.

Governance is cross-cutting and has authority over unsafe implementation shortcuts.

### 10 — ADR

Purpose:
- explicit architecture decisions;
- alternatives considered;
- rationale;
- consequences;
- decision status.

Use ADRs for durable decisions. Do not create an ADR for every implementation detail.

### 11 — Models

Purpose:
- domain models;
- analytical models;
- reference models;
- reusable schemas where not owned by a more specific layer.

### 12 — Systems

Purpose:
- executable systems engineering;
- runtime structure;
- testing/quality;
- observability;
- deployment/operations;
- system integration.

### 13 — References

Purpose:
- external references;
- reference architectures;
- standards;
- benchmarks;
- supporting material.

External references are not automatically ELO policy.

### 14 — Roadmap

Purpose:
- future phases;
- proposals;
- sequencing;
- milestones;
- backlog framing.

Roadmap status does not equal implementation status.

### 15 — Assets

Purpose:
- reusable templates;
- prompts;
- fixtures;
- examples;
- controlled assets.

Each asset must identify its intended use and authority.

### Docs

Purpose:
- evolving project documentation;
- working notes;
- migration records;
- non-canonical supporting documentation.

Do not place normative architecture here when a canonical architecture location exists.

### src/elo

Purpose:
- canonical executable implementation of the ELO runtime/prototype.

Code must map to an approved architectural capability or an explicitly marked experimental area.

## 4. Duplicate directory rule

The repository currently contains parallel naming variants such as Portuguese and English directories.

Examples include:

- `00-empresa-manifesto/` and `00-enterprise-manifest/`;
- `01-meta-arquitetura/` and `01-meta-architecture/`;
- `05-cognitivo-plataforma/` and `05-cognitive-platform/`;
- `07-engenharia-de dados/` and `07-data-engineering/`.

Until a consolidation ADR is approved:

1. do not create new duplicate folders;
2. do not copy documents from one variant to another merely for symmetry;
3. use the English operational path named by the current README for new canonical artifacts unless an existing document explicitly owns the Portuguese path;
4. preserve existing Portuguese content until reviewed;
5. record conflicts as structural debt rather than silently deleting content;
6. propose consolidation through an ADR before moving large document sets.

## 5. Artifact placement decision tree

Before creating an artifact ask:

1. Is it constitutional? → `00-enterprise-manifest/`
2. Is it meta-architecture? → `01-meta-architecture/`
3. Is it architecture? → `02-architecture-library/`
4. Is it a business process? → `03-process-library/`
5. Is it curated knowledge? → `04-knowledge-handbook/`
6. Is it cognitive capability design? → `05-cognitive-platform/`
7. Is it knowledge engineering? → `06-knowledge-engineering/`
8. Is it data engineering? → `07-data-engineering/`
9. Is it AI/provider governance? → `08-ai/`
10. Is it governance/security/policy? → `09-governance/`
11. Is it a durable architecture decision? → `10-adr/`
12. Is it a model? → `11-models` or existing approved model owner
13. Is it executable system engineering? → `12-systems/` or `src/elo/` as appropriate
14. Is it an external reference? → `13-references/`
15. Is it future work? → `14-roadmap/`
16. Is it a reusable controlled asset? → `15-assets/`
17. Is it working/evolving documentation? → `Docs/`
18. Is it executable Python implementation? → `src/elo/`

## 6. No-duplication rule

Before adding a concept, search for:

- exact name;
- synonyms;
- abbreviations;
- equivalent contract;
- equivalent ADR;
- existing implementation;
- existing test;
- existing roadmap item.

Classify the result:

REUSE
EXTEND
RELOCATE
CONSOLIDATE
NEW
CONFLICT

Do not choose NEW until the other classifications have been rejected.

## 7. Status vocabulary

Use these statuses consistently:

- PROPOSED — concept proposed but not approved;
- DRAFT — under development;
- NORMATIVE — approved rule/architecture;
- IMPLEMENTED — code exists;
- TESTED — behavior has executable evidence;
- VERIFIED — independently reviewed/validated;
- EXPERIMENTAL — intentionally non-canonical;
- DEPRECATED — retained for historical compatibility;
- SUPERSEDED — replaced by a newer approved artifact;
- ROADMAP — future capability;
- BLOCKED — dependency prevents progress.

## 8. Core rule

The repository must evolve toward:

requirement
→ architecture
→ contract
→ implementation
→ test
→ evidence
→ operational status

not:

idea
→ file
→ assumed truth.
