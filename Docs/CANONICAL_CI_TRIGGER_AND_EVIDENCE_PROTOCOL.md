# ELO — Protocolo de Disparo e Evidência de CI da Consolidação Canônica

## Objetivo
Garantir que a consolidação canônica somente avance quando existir evidência verificável de execução do CI para o commit efetivamente avaliado pelo PR.

## Distinção terminológica obrigatória

Neste documento:

- **workflow run** = uma execução efetiva de um workflow do GitHub Actions;
- **`workflow_run` event** = evento específico do GitHub Actions que pode disparar outro workflow após a execução de um workflow;
- **status de CI** = resultado verificável associado ao commit/PR/workflow;
- **NO_EVIDENCE** = ausência de evidência suficiente para classificar o CI.

A existência de um **workflow run** não implica que tenha ocorrido um **`workflow_run` event** como gatilho de outro workflow.

## Situação observada
O commit `466213bf1de542d06f9620938a23a42f24fc39b1` não possuía workflow run nem status registrado no GitHub Actions. Isso foi tratado como `NO_EVIDENCE`, não como `PASS` ou `FAIL`.

## Regra

```text
NO_EVIDENCE != PASS
NO_EVIDENCE != FAIL
NO_EVIDENCE = BLOCKED
```

## Workflow canônico
Usar o `ELO Evolution Gate` existente. Não criar um segundo workflow concorrente apenas para a consolidação.

## Evidência mínima por commit avaliado

1. SHA do commit.
2. PR que contém o commit.
3. Workflow run associado.
4. Jobs associados.
5. Resultado de `compileall`.
6. Resultado da suíte `pytest`.
7. Resultado do gate de evolução.
8. Registro de falhas, quando houver.
9. Nova execução após correção, quando houver falha.

A evidência deve identificar o **workflow run**. O termo **`workflow_run` event** somente deve ser utilizado quando esse evento específico tiver sido configurado e efetivamente demonstrado.

## Estados possíveis

- `PASS`: workflow run registrado e todos os gates necessários passaram.
- `FAIL`: workflow run registrado e um ou mais gates falharam.
- `CANCELLED`: execução não produz evidência de aprovação.
- `NO_EVIDENCE`: nenhum run/status disponível.
- `BLOCKED`: não é permitido fazer merge/depreciação/remoção.

## Regra de correção
Se `FAIL`:

```text
falha
→ diagnóstico
→ correção mínima
→ novo commit
→ nova execução
→ revalidação
```

Nunca considerar a falha resolvida apenas por comentário ou aprovação manual.

## Registro histórico da investigação de trigger

A investigação realizada no ciclo de 2026-08-19 foi uma mudança mínima e não-runtime destinada a provocar uma nova execução do fluxo `pull_request` para o PR #267 depois da revisão das configurações do GitHub Actions.

Restrições aplicadas:

- somente documentação e configuração de workflow;
- nenhuma alteração de Core/runtime;
- nenhuma alteração do resolver;
- nenhum conteúdo de conhecimento alterado;
- nenhuma exclusão da árvore histórica;
- nenhuma migração semântica.

O HEAD observado antes dessa investigação foi `a6da38625cd2028e5fb17fcb0a6c69c1dde4ec74`.

A evidência esperada para o ciclo era:

```text
novo SHA
   ↓
workflow run associado
   ↓
jobs
   ↓
compileall / pytest / Evolution Gate
   ↓
evidência verificável
```

Até que o workflow run seja localizado especificamente para o HEAD avaliado:

```text
CI_HEAD = NO_EVIDENCE
MERGE = BLOCKED
```

A simples existência de execução antiga não satisfaz este gate.

## Regra de merge
O PR somente pode ser candidato a merge quando:

```text
CI = PASS
AND
T01–T10 = PASS
AND
nenhum conflito arquitetural pendente
AND
nenhuma referência crítica órfã
```

## Regra de depreciação
Mesmo com CI PASS, depreciação de caminho histórico exige validação de consumidores e proveniência.

## Regra de remoção
Remoção física exige todos os gates anteriores e confirmação de que não existe conteúdo exclusivo ou dependência histórica não preservada.

## Integração com ELO
A ausência de evidência de CI deve ser apresentada ao ELO como condição técnica bloqueante. O ELO pode decidir investigar a infraestrutura, mas não deve converter ausência de evidência em aprovação.
