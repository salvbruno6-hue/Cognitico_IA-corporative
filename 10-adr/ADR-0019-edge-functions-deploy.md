---
artifact_id: ADR-0019-edge-functions-deploy
title: Deploy de Edge Functions
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Infrastructure
date: 2026-09-27
supersedes: null
superseded_by: null
related:
  - ADR-0018-multi-tenant-model
  - ELO-012_MULTITEINER_TENANT_OPERATING_MODEL
  - AGENTS.md
---

# ADR-0019 — Deploy de Edge Functions

## Contexto

O ELO possui três Edge Functions em produção no Supabase:

- `elo-data-gateway` (v3)
- `elo-authz` (v14)
- `elo-mcp` (v4)

O repositório mantém o código canônico dessas funções em
`supabase/functions/`. Contudo, a auditoria estrutural
(PASSO 42.2) revelou:

- não existe workflow de deploy de Edge Functions
- não existe documentação formal de deploy
- não existe `supabase/config.toml` versionado
- não existe `SUPABASE_ACCESS_TOKEN` em nenhum workflow
- as versões em produção não podem ser rastreadas a um
  commit específico
- existem divergências entre main e produção:
  - `elo-data-gateway`: main tem `lista_mae_insert`;
    produção v3 não tem
  - `elo-mcp`: main tem v0.2.0 com 3 tools cognitivas;
    produção tem v0.1.0 com 2 tools

Isso não é um problema de código. É um **GAP de processo**:
os deploys acontecem, mas por mecanismo não formalizado e
não rastreável.

## Decisão

Adotar o seguinte padrão de deploy de Edge Functions:

### 1. Fonte canônica

O código-fonte das Edge Functions vive exclusivamente em
`supabase/functions/<nome>/` no GitHub.

Nenhum deploy pode partir de código que não esteja em main.

### 2. Método oficial

O método oficial é a CLI do Supabase via GitHub Actions:
```bash
supabase functions deploy <nome> \
  --project-ref <ref> \
  --use-api
```

O parâmetro `--use-api` dispensa Docker local e é compatível
com o plano gratuito.

### 3. Workflow único

Existirá um único workflow:

.github/workflows/elo-deploy-functions.yml

Características:

- `workflow_dispatch` (execução manual, sob demanda)
- input: qual função deployar (`elo-data-gateway`,
  `elo-authz`, `elo-mcp`, ou `all`)
- usa secret `SUPABASE_ACCESS_TOKEN` (token pessoal gerado
  no dashboard Supabase)
- usa `supabase/setup-cli` para instalar a CLI no runner
- não roda automaticamente em push (por segurança)

### 4. Autorização

O deploy é uma **operação governada**:

- requer autorização humana explícita (disparo manual)
- o workflow registra quem disparou (via GitHub Actions log)
- o `SUPABASE_ACCESS_TOKEN` é revogável a qualquer momento
- deploys automáticos só podem ser considerados depois de ADR
  próprio

### 5. Rastreabilidade

Cada deploy gera:

- run_id do GitHub Actions
- SHA do commit em main
- versão da função resultante no Supabase
- timestamp e operador

Nenhum deploy deve ocorrer fora desse fluxo.

### 6. Exceções

Deploys manuais via Dashboard só podem ocorrer em
emergência declarada, e devem ser seguidos de:

- registro em issue de governança
- sincronização do commit correspondente em main (se o
  código divergir)
- PR reconciliando o estado

### 7. Não objetivos

Este ADR **não**:

- reescreve a história dos deploys anteriores
- exige rollback das versões atuais
- cria deploy automático em push
- substitui o Evolution Gate
- altera o código das funções

## Consequências

### Positivas

- deploy deixa de ser prática não rastreável
- qualquer pessoa autorizada pode deployar sem instalar CLI
  localmente
- o `SUPABASE_ACCESS_TOKEN` é o único ponto de autorização
- o workflow é versionado e revisável

### Negativas

- o token precisa ser criado e mantido no GitHub
- o workflow depende de disponibilidade do Supabase CLI
- exige disciplina para não deployar fora do fluxo

### Neutras

- nenhuma estrutura é movida
- nenhum código é alterado
- nenhuma função é alterada por este ADR

## Conformidade

- Regra de duplicidade: `NEW` (formaliza processo inexistente)
- Camadas: Governança (ADR) + Infraestrutura (workflow)
- Princípio fundador: preservado — deploys exigem
  autorização humana explícita

## Status

Aceito. O workflow e a documentação correspondentes são
implementados no PASSO 43.1.

FIM DO CONTEÚDO.