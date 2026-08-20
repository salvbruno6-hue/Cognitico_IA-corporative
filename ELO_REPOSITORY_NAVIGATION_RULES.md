# ELO — Repository Navigation and Authority Rules

## 1. Purpose

This document defines how humans and AI agents must interpret and maintain the ELO repository.

The repository may contain historical naming variants during controlled consolidation. Similar names do not imply independent architectures. The canonical owner is determined by the authority model, approved decisions, contracts, implementation evidence, and the current repository tree.

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

- `00-enterprise-manifest/` — enterprise identity, mission, principles and constitutional boundaries.
- `01-meta-architecture/` — architectural principles, meta-models and architectural language.
- `02-architecture-library/` — canonical architecture, component boundaries, contracts and patterns.
- `03-process-library/` — business processes, workflows, responsibilities and procedures.
- `04-knowledge-handbook/` — curated and validated organizational knowledge.
- `05-cognitive-platform/` — Cognitive Core, Context, Knowledge, Memory, Reasoning, Evidence, Recommendation, Decision Support and cognitive orchestration.
- `06-knowledge-engineering/` — ingestion, normalization, semantic structures, retrieval preparation and knowledge quality.
- `07-data-engineering/` — data contracts, ingestion, transformation, quality, storage, APIs, events and data lifecycle.
- `08-ai/` — AI provider architecture, model policies, provider abstraction, evaluation and governance.
- `09-governance/` — security, identity, tenant isolation, policy, privacy, compliance, audit and risk controls.
- `10-adr/` — durable architecture decisions.
- `11-models-library/` — domain, analytical and reusable models.
- `12-system-engineering/` — executable systems engineering, runtime, quality and operations.
- `13-reference-architecture/` — external references, standards, benchmarks and reference architectures.
- `14-roadmap/` — future phases, proposals, sequencing and milestones.
- `15-assets/` — reusable controlled assets.
- `Docs/` — evolving documentation, migration records and non-canonical support material.
- `src/elo/` — canonical executable implementation.

## 4. Duplicate directory rule

A duplicate directory is any parallel path that claims or historically claimed the same semantic layer or owner.

Rules:

1. Do not create new duplicate folders.
2. Do not copy content merely to obtain bilingual or structural symmetry.
3. Preserve historical content until it is audited.
4. Determine the canonical owner before moving content.
5. Absorb useful content semantically; do not overwrite or discard information merely because filenames differ.
6. Reconcile `artifact_id`, `legacy_path`, aliases, references and consumers before removal.
7. Remove a legacy path only after semantic absorption and validation gates succeed.
8. After physical removal, rerun resolution/integrity checks and confirm that no orphan references remain.
9. Update README and navigation records from the actual `main` tree, not from assumptions.

## 5. Loop de Conclusão — manutenção arquitetural ELO

O **Loop de Conclusão** é uma diretriz permanente de manutenção da arquitetura. Ele deve ser aplicado a qualquer duplicidade estrutural, artefato concorrente, migração canônica ou aposentadoria de legado.

```text
DETECTAR
  ↓
AUDITAR
  ↓
CLASSIFICAR ARQUIVO A ARQUIVO
  ↓
DEFINIR OWNER CANÔNICO
  ↓
ABSORVER SEMANTICAMENTE
  ↓
REORGANIZAR PARA FLUXO E COERÊNCIA
  ↓
RECONCILIAR IDs / LEGACY PATHS / ALIASES / REFERÊNCIAS / CONSUMIDORES
  ↓
ATUALIZAR README / ÍNDICES / MAPAS / EVIDÊNCIAS
  ↓
TESTAR RESOLUÇÃO E INTEGRIDADE
  ↓
EXECUTAR GATES
  ↓
SE GATES APROVADOS → REMOVER FISICAMENTE O LEGADO
  ↓
VALIDAR NOVAMENTE APÓS A REMOÇÃO
  ↓
CONFIRMAR ZERO REFERÊNCIAS ÓRFÃS / ZERO PERDA SEMÂNTICA
  ↓
MERGE
  ↓
VALIDAR MAIN
  ↓
REVARrer A ÁRVORE
  ↓
SE HOUVER NOVA PENDÊNCIA → RETORNAR AO INÍCIO
  ↓
SE NÃO HOUVER → ENCERRAR O CICLO
```

### Critérios obrigatórios de conclusão

Um ciclo só pode ser declarado concluído quando:

- todo conteúdo relevante do legado foi classificado;
- conteúdo válido foi absorvido pelo owner canônico;
- a organização interna do owner possui fluxo e sentido;
- referências e consumidores apontam para o caminho canônico;
- aliases e `artifact_id`/`legacy_path` foram reconciliados quando aplicáveis;
- README e registros de governança refletem a árvore real;
- testes e gates aplicáveis estão verdes;
- a remoção física do legado foi realizada somente após os gates;
- a validação pós-remoção não encontrou órfãos ou regressões;
- o merge foi realizado e o `main` foi validado;
- uma nova varredura confirmou o próximo estado arquitetural.

**Não existe conclusão parcial quando a etapa pendente é necessária para segurança estrutural. O ELO permanece no loop até que a condição de saída seja comprovada.**

## 6. Artifact placement decision tree

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
12. Is it a model? → `11-models-library/`
13. Is it executable system engineering? → `12-system-engineering/` or `src/elo/` as appropriate
14. Is it an external reference? → `13-reference-architecture/`
15. Is it future work? → `14-roadmap/`
16. Is it a reusable controlled asset? → `15-assets/`
17. Is it working/evolving documentation? → `Docs/`
18. Is it executable Python implementation? → `src/elo/`

## 7. No-duplication rule

Before adding a concept, search for:

- exact name;
- synonyms;
- abbreviations;
- equivalent contract;
- equivalent ADR;
- existing implementation;
- existing test;
- existing roadmap item.

Classify the result as:

`REUSE` · `EXTEND` · `RELOCATE` · `CONSOLIDATE` · `NEW` · `CONFLICT`

Do not choose `NEW` until the other classifications have been rejected.

## 8. Status vocabulary

- `PROPOSED` — proposed but not approved;
- `DRAFT` — under development;
- `NORMATIVE` — approved rule/architecture;
- `IMPLEMENTED` — code exists;
- `TESTED` — executable evidence exists;
- `VERIFIED` — independently validated;
- `EXPERIMENTAL` — intentionally non-canonical;
- `DEPRECATED` — retained for historical compatibility;
- `SUPERSEDED` — replaced by a newer approved artifact;
- `ROADMAP` — future capability;
- `BLOCKED` — dependency prevents progress.

## 9. Core rule

The repository must evolve toward:

```text
requirement
→ architecture
→ contract
→ implementation
→ test
→ evidence
→ operational status
```

not:

```text
idea
→ file
→ assumed truth
```
