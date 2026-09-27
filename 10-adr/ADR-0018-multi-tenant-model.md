---
artifact_id: ADR-0018-multi-tenant-model
title: Modelo Multi-Tenant do ELO
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
  - ELO Infrastructure
date: 2026-09-27
supersedes: null
superseded_by: null
related:
  - ADR-0017-lista-mae-editable-by-admin
  - ELO-012_MULTITEINER_TENANT_OPERATING_MODEL
  - ELO_SO_DOSSIER_PROTOCOL
  - ELO_AUTHORIZATION_ENFORCEMENT_STANDARD
  - ELO_AUTHORIZED_ACCESS_POLICY
  - ELO_MEMBER_CONTRACT
  - SCHEMA_NO_DUPLICATE_CREATION_CONTRACT
  - ELO_MATURE_MULTITEINER_DATA_GOVERNANCE
---

# ADR-0018 — Modelo Multi-Tenant do ELO

## Contexto

O ELO é uma plataforma cognitiva que opera sobre universos
corporativos. Desde sua origem, o repositório contém duas
naturezas de artefato:

- o **cânone ELO** — genérico, reutilizável, provider-neutral
- o **contexto corporativo** — específico de cada tenant

O primeiro tenant corporativo é a **Multiteiner**, com o
setor **PCP** entre seus domínios operacionais.

O conceito de isolamento já existe em várias peças:

- `docs/ELO-012_MULTITEINER_TENANT_OPERATING_MODEL.md`
  formaliza "Tenant Isolation" e regras de privacidade
- `09-governance/contracts/protocols/ELO_SO_DOSSIER_PROTOCOL.md`
  define `tenant_id`, `domain`, `scope_state`
- `09-governance/contracts/standards/ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md`
  exige `SCOPE` no modelo de autorização
- `07-data-engineering/tenant-multiteiner-data-model/`
  contém modelo conceitual e lógico (draft, reference)
- `members/ELO-ORG/ELO_MEMBER_CONTRACT.md`
  obriga preservação de tenant/domain scope
- `10-adr/ADR-0017-lista-mae-editable-by-admin.md`
  reconhece Multiteiner como tenant e `p_pcp_*` como
  policies corretas

Contudo, **não existia** um ADR único que consolidasse esse
modelo e definisse:

- a fronteira explícita entre cânone e tenant
- as convenções de nomenclatura
- a organização de migrations por camada
- o tratamento histórico do que já está em produção

A auditoria estrutural (PASSO 39.1) revelou que:

- 29 migrations existem no GitHub
- 144 migrations existem em produção
- apenas 13 estão em ambos (SYNC)
- 16 estão apenas no GitHub (GITHUB_ONLY)
- 131 estão apenas em produção (PROD_ONLY)

O número elevado de migrations não versionadas reflete
desenvolvimento iterativo direto em produção — legítimo
enquanto o modelo multi-tenant não estava formalizado.

## Decisão

Adotar um **modelo multi-tenant unificado com separação por
camada**, mantendo o GitHub como fonte canônica e o Supabase
como execução.

### 1. Fronteira explícita
