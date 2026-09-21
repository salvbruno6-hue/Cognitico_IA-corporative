---
artifact_id: ADR-0013-external-ai-authority-contract
title: Contrato de Autoridade para IA Externa
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
  - ELO Infrastructure
date: 2026-09-21
supersedes: null
superseded_by: null
related:
  - ELO_EXTERNAL_AI_AUTHORITY_CONTRACT
  - ELO_AUTHORIZATION_ENFORCEMENT_STANDARD
  - ELO_AUTHORIZED_ACCESS_POLICY
  - ELO_AUTHORIZED_SPECIALIST_ACCESS_STANDARD
---

# ADR-0013 — Contrato de Autoridade para IA Externa

## Contexto

O ELO possui autorização real via `elo-authz`,
`elo_identity_registry`, role `ELO_ADMIN` e RFC 9728. Falta
o documento canônico que declara a autoridade, deveres e
proibições da IA externa.

## Decisão

Adotar `ELO_EXTERNAL_AI_AUTHORITY_CONTRACT.md` como contrato
normativo, reconciliado com `elo-authz`, `elo_identity_registry`,
role `ELO_ADMIN` e RFC 9728.

- **Não cria** novo mecanismo
- **Não substitui** `elo-authz`
- **Documenta** o que existe
- **Padroniza** tiers READ, ANALYZE, PROPOSE, OPERATE

## Alternativas consideradas

A. Não documentar → dificulta onboarding e auditoria
B. Criar novo mecanismo → viola reuso, duplica elo-authz
C. Só README do elo-mcp → fragmenta autoridade

## Consequências

Positivas: autoridade auditável, tiers padronizados, revogação
normativa, zero duplicidade.

Negativas: manutenção ao evoluir tiers.

## Conformidade

Regra de duplicidade: `EXTEND`. Camadas: Governança.
Princípio fundador preservado.

## Status

Aceito. Contrato em vigor.
---