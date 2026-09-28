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


### 2. Convenções de nomenclatura

| Prefixo | Significado | Autoridade |
|---|---|---|
| `elo_*` | Estruturas canônicas do ELO | Cânone (GitHub) |
| `mt_*` | Estruturas operacionais do tenant Multiteiner | Tenant |
| `p_pcp_*` | Policies do domínio PCP | Tenant |
| `elo_private.*` | Helpers internos do ELO | Cânone |

Estas convenções passam a ser **regra** para novos artefatos.
Artefatos existentes são preservados como estão.

### 3. Organização de migrations

Migrações passam a ser classificadas por camada:

- **Cânone:** migrations que alteram estruturas `elo_*`,
  funções genéricas do ELO, RLS de tabelas de plataforma
- **Tenant:** migrations que alteram estruturas `mt_*`,
  tabelas operacionais, policies específicas (`p_pcp_*`)

A separação **não exige subdiretórios físicos** neste momento.
A classificação é feita por:
- nome da migration
- prefixo das estruturas afetadas
- comentário no topo do arquivo declarando a camada

Uma futura reorganização em subdiretórios pode ser
considerada por ADR próprio, se necessário.

### 4. Isolamento entre tenants

Regras obrigatórias:

- `tenant_id` deve estar presente em toda tabela
  operacional (padrão já observado em `mt_*`)
- consultas cross-tenant são proibidas sem
  relacionamento governado explícito
- RLS é obrigatório em tabelas expostas na API
- policies devem refletir o modelo de autorização do tenant

### 5. Onboarding de novo tenant

Quando um segundo tenant for onboarded:

1. Novo ADR registra o tenant
2. Novo bloco de tabelas com prefixo próprio
3. Modelo de referência em
   `07-data-engineering/tenant-<nome>-data-model/`
4. Policies próprias (padrão `p_<domínio>_*`)
5. Isolamento explícito por `tenant_id`
6. Contexto corporativo em pasta própria ou subpasta de
   `members/`

O modelo não presume que o próximo tenant use
`mt_*`. O prefixo é decisão do tenant.

### 6. Tratamento das 131 migrations históricas

As migrations PROD_ONLY **não são descartadas** nem tratadas
como autoridade canônica.

São classificadas em três grupos:

| Grupo | Descrição | Ação |
|---|---|---|
| **Histórico legítimo** | Migrations que representam evolução real do tenant ou do cânone | Reincorporar ao GitHub via absorção documentada |
| **Superseded** | Migrations cujos efeitos foram substituídos por outras | Registrar como histórico, marcar como obsoletas |
| **Não reconciliáveis** | Migrations cujo efeito não é mais observável no estado atual | Registrar como evidência histórica, sem reexecução |

A reincorporação é **não destrutiva**:
- nenhuma migration é reexecutada
- nenhuma migration é apagada
- nenhuma estrutura é removida

Cada bloco reincorporado é acompanhado de:
- comentário declarando origem (`PROD_ONLY`)
- classificação de camada (cânone ou tenant)
- referência ao estado observado

A ordem de reincorporação é definida caso a caso, em PRs
próprias. Este ADR apenas estabelece o padrão.

### 7. Fonte canônica

- **GitHub** permanece a fonte canônica documental
- **Supabase** é o ambiente de execução
- reconciliação entre os dois é feita pelo workflow
  `ELO Live Reconciliation`
- divergências são reportadas, nunca corrigidas
  automaticamente

### 8. Proibições

- não criar novo ADR de tenant sem justificar GAP
- não criar segunda autoridade de cânone
- não mover migrations existentes sem ADR próprio
- não reexecutar migrations históricas
- não apagar migrations de produção
- não presumir prefixo para tenant futuro sem decisão dele

FIM DO BLOCO 2.