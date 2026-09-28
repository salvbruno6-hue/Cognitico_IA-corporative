---
artifact_id: ADR-0020-end-to-end-cycle
title: Ciclo End-to-End do ELO
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
  - ELO Infrastructure
date: 2026-09-28
supersedes: null
superseded_by: null
related:
  - ADR-0018-multi-tenant-model
  - ADR-0019-edge-functions-deploy
  - ELO_GOVERNED_AUTONOMOUS_ISSUE_LOOP
  - ELO_OPERATOR_GITHUB_BINDING_RUNTIME
  - AGENTS.md
---

# ADR-0020 — Ciclo End-to-End do ELO

## Contexto

O ELO possui todas as peças do ciclo governado:

- `elo-agent-loop.yml` — recebe issue elegível, executa
  correção, obtém aprovação (`APPROVE_COMMIT`), cria PR
- `elo-evolution-gate.yml` — validação técnica em cada PR
- `elo-merge-coordinator.yml` — executa merge quando as
  condições são satisfeitas e `elo-merge-authorized` está
  ativa
- `elo-authz` — emite e valida autorizações
- `elo_authorization_grants` — persiste as autorizações no
  Supabase
- `ELO_Live_Reconciliation` — verifica continuamente que
  produção coincide com o cânone

Contudo, **não existia um ADR único** que:

- declarasse o ciclo completo como padrão canônico
- documentasse o procedimento de emissão de
  `elo-merge-authorized`
- definisse quem pode autorizar merge
- descrevesse o rollback e o tratamento de falhas

Isso significa que o ciclo funciona, mas por prática
distribuída — não por decisão arquitetural explícita.

Este ADR preenche essa lacuna.

## Decisão

Adotar o **Ciclo End-to-End do ELO** como padrão canônico:

### 1. Fluxo canônico

O ciclo completo é:

```text
Issue elegível (label `codex-ready`)
  → Context resolution (ELO lê cânone, contratos, ADRs)
  → Plan
  → Implementation (via agent loop)
  → Tests
  → Evidence
  → Evolution Gate (validação técnica)
  → ELO Governance Review (`ELO_DECISION`)
  → Correção (se `CORRECT`, até 3 ciclos)
  → `APPROVE_COMMIT`
  → Commit
  → PR
  → Repository Gates (CI, baseline, behavioral, maintenance)
  → `APPROVE_MERGE` (`elo-merge-authorized`)
  → Git Merge
  → Post-merge verify
  → Learning
  → Issue closure
```

Cada transição é auditável e produz evidência em
`elo_audit_log` quando aplicável.

### 2. Elegibilidade

Uma issue é elegível para processamento autônomo quando:

- tem label `codex-ready`
- tem escopo dentro do cânone ELO
- não modifica autoridade, identidade, autorização ou
  governança fora do escopo permitido
- não requer decisão protegida (mudar branch protection,
  alterar políticas, promover contexto para Core)
- não depende de evidência externa indisponível

Se qualquer condição falhar, a issue é escalada.

### 3. Autorização de commit

O commit só ocorre após:

- `ELO_DECISION=APPROVE_COMMIT` no `elo-governance.txt`
- `elo-commit-authorized` ativa em
  `elo_authorization_grants`
- Virtual Laboratory PASS (quando aplicável — mudanças de
  budget learning)
- Todos os gates declarados terem passado

Se qualquer condição falhar, o commit não ocorre. A issue
permanece aberta.

### 4. Autorização de merge (`elo-merge-authorized`)

**Quem pode emitir:** operador autenticado com role
`CANONICAL_ADMIN` via `elo-authz`, ação
`issue_authorization_grant`, com
`authorization_state: elo-merge-authorized`.

**Pré-requisitos para emissão:**

- binding ativo em `elo_operator_github_bindings`
- sessão autenticada válida
- repository scope autorizado
- operação declarada (`execute`)

**Validade:** entre 60 segundos e 24 horas
(`expiresIn` bounded).

**Revogação:** o grant pode ser revogado em qualquer momento
via `revoked_at`; o Merge Coordinator revalida antes de agir.

**Efeito:** sem `elo-merge-authorized` ativa no momento do
merge, o Merge Coordinator não executa o merge — ele comenta
na PR e aguarda.

### 5. Merge Coordinator

O workflow `elo-merge-coordinator.yml` verifica sete
condições antes de mergear:

1. PR aberta com `PR-ready` marker
2. Todos os checks da PR concluídos sem failure
3. Nenhum review bloqueante (`CHANGES_REQUESTED`)
4. `mergeable = true` e `mergeable_state` em clean ou
   unstable
5. `elo-merge-authorized` ativa em `elo_authorization_grants`
6. Bindings e roles coerentes
7. Sem operação protegida pendente

Se qualquer condição falhar, o coordinator **não mergeia**.
Comenta na PR com o motivo e para.

### 6. Post-merge

Após o merge:

- verificar que main foi atualizado
- reconciliar a issue com o estado de main
- registrar evidência em `elo_audit_log`
- se o change produz experiência, rotear via `ELO Aprender`
- fechar a issue somente se todos os critérios foram
  satisfeitos

Um merge não equivale automaticamente ao fechamento da
issue.

### 7. Rollback e falhas

Se após o merge algo quebrar:

- a reversão é feita via PR de revert (não via push
  direto em main)
- a PR de revert segue o mesmo ciclo end-to-end
- a issue original é reaberta com contexto
- o Evolution Gate é novamente executado

Não existe push direto em main. Nunca.

Se durante o ciclo:

- um gate falha de forma determinística e corrigível: o
  agent loop corrige e reexecuta
- um gate falha de forma não corrigível: escalar para
  humano
- limite de 3 ciclos de correção atingido: escalar

### 8. Canais de autorização

Existem três estados de autorização, cada um com escopo
próprio:

- `elo-execution-authorized` — autoriza execução técnica
- `elo-commit-authorized` — autoriza commit
- `elo-merge-authorized` — autoriza merge

Cada um é emitido separadamente. Nenhum é inferido a partir
de outro. Nenhum é criado por saída de agente.

### 9. Não objetivos

Este ADR **não**:

- executa nenhum passo do ciclo
- altera workflows existentes
- cria novos workflows
- muda a política de autorização
- substitui `AGENTS.md`
- concede autorização a ninguém

### 10. Estado atual da adoção

| Componente | Status |
|---|---|
| Agent Loop | ativo (em main) |
| Evolution Gate | ativo |
| Merge Coordinator | ativo (em main) |
| elo-authz | ativo (v14 em produção) |
| elo_authorization_grants | schema ativo |
| `elo-merge-authorized` emitida em produção | **não emitida ainda** |
| Ciclo executado ponta a ponta | **não comprovado ainda** |

O ciclo está **implementado**, mas ainda **não exercitado
end-to-end em produção**. A primeira execução requer emissão
manual de `elo-merge-authorized` por operador com
`CANONICAL_ADMIN`.

## Consequências

### Positivas

- ciclo de contribuição governado, auditável e rastreável
- autorização explícita para cada operação crítica
- rollback via PR (nunca via push)
- escalonamento humano embutido
- política clara de elegibilidade

### Negativas

- requer operador `CANONICAL_ADMIN` para emitir autorização
- requer binding ativo no Supabase
- exige monitoramento contínuo dos grants
- introduz latência (autorizações expiram em 24h)

### Neutras

- nenhum workflow é alterado
- nenhum código é alterado
- nenhuma migration é alterada

## Conformidade

- Regra de duplicidade: `NEW` (formaliza ciclo existente)
- Camadas: Governança (ADR)
- Princípio fundador: preservado — nenhuma autoridade
  humana é substituída; autorizações são explícitas e
  revogáveis

## Status

Aceito. Serve de referência canônica para o funcionamento do
ciclo end-to-end.

A primeira execução comprovada do ciclo está pendente de
emissão manual de `elo-merge-authorized` por operador
`CANONICAL_ADMIN`.
