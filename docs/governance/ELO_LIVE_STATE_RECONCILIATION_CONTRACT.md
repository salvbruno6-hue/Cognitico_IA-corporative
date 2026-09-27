---
artifact_id: ELO-LIVE-STATE-RECONCILIATION-CONTRACT
title: ELO Live State Reconciliation Contract
family: docs/governance
layer: governance
type: contract
owner: ELO Governance
authority: reference
status: defined
version: 0.1.0
related:
  - ELO_BASELINE_AUDIT_CHECKLIST
  - ELO_GOVERNED_AUTONOMOUS_ISSUE_LOOP
  - AGENTS.md
  - ISSUE_413_LIVE_RECONCILIATION_GATE_2026-09-07
---

# ELO Live State Reconciliation Contract

## 1. Propósito

Definir como o ELO confronta o estado declarado (GitHub) com
o estado live (Supabase) para detectar drift.

## 2. Natureza

Reconciliação NÃO é correção. O contrato define:
- o que é estado esperado
- o que é estado live
- o que é drift
- como classificar o resultado

O contrato NÃO define correção automática. Correção é
governada por outro fluxo.

## 3. Estado esperado

Estado esperado é o que o cânone ELO declara como correto:
- migrations aplicadas
- RLS habilitado onde deve estar
- policies declaradas
- tabelas declaradas

O estado esperado vive em:
- supabase/migrations/*.sql (declaração)
- 09-governance/contracts/expected_state/*.yaml (consolidado)

## 4. Estado live

Estado live é o que efetivamente existe no Supabase:
- pg_catalog.pg_tables
- pg_catalog.pg_class.relrowsecurity
- pg_catalog.pg_policies
- supabase_migrations.schema_migrations

O estado live é observado, não inferido.

## 5. Classificações

Cada confronto produz uma das quatro classificações:

- **PASS** — estado live confere com o esperado
- **DRIFT** — estado live difere do esperado
- **UNKNOWN** — estado live não pôde ser lido
- **BLOCKED** — o confronto não pôde ser executado

Regra do ISSUE_413:
> "Missing rollback or checksum drift is BLOCKED, never PASS."

Portanto: ausência de leitura é BLOCKED, nunca PASS.

## 6. Read-only

O harness:
- Lê pg_catalog via SELECT
- Lê migrations via SELECT
- NUNCA executa ALTER/CREATE/DROP
- NUNCA executa DDL
- NUNCA modifica o Supabase

## 7. Não autoridade

O harness produz evidência para governança. Ele:
- Não promove
- Não corrige
- Não autoriza merge
- Não substitui o Evolution Gate

## 8. Escopo inicial

O primeiro escopo é RLS declarado vs RLS real.

Escopos futuros (não nesta versão):
- migrations aplicadas vs migrations versionadas
- policies declaradas vs policies reais
- tabelas declaradas vs tabelas reais

## 9. Vigência

Entra em vigor na aprovação da PR 27.1. Alterações exigem
ADR.
