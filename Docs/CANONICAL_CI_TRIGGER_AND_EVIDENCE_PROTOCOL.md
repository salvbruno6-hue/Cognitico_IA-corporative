# ELO — Protocolo de Disparo e Evidência de CI da Consolidação Canônica

## Objetivo

Garantir que a consolidação canônica somente avance quando existir evidência verificável de execução do CI para o commit efetivamente avaliado pelo PR.

## Distinção terminológica obrigatória

- **workflow run** = execução efetiva de um workflow do GitHub Actions;
- **`workflow_run` event** = evento específico do GitHub Actions que dispara outro workflow após uma execução;
- **status de CI** = resultado verificável associado ao commit/PR/workflow;
- **NO_EVIDENCE** = ausência de evidência suficiente para classificar o CI.

A existência de um workflow run não implica que tenha ocorrido um `workflow_run` event.

## Regra de evidência

```text
NO_EVIDENCE != PASS
NO_EVIDENCE != FAIL
NO_EVIDENCE = BLOCKED
```

A regra vale por **HEAD do PR**. Evidência de um commit anterior não pode ser reutilizada como evidência do HEAD atual quando o conteúdo avaliado mudou.

## Workflow canônico

Usar o `ELO Evolution Gate` existente. Não criar um segundo workflow concorrente apenas para a consolidação.

O workflow permanece responsável pela validação técnica. A decisão de compatibilidade canônica continua pertencendo ao processo governado do ELO.

## Evidência mínima por commit avaliado

1. SHA do commit.
2. PR que contém o commit.
3. Workflow run associado ao SHA.
4. Jobs associados.
5. Resultado de compilação.
6. Resultado da suíte de testes aplicável.
7. Resultado do Evolution Gate.
8. Falhas e diagnóstico, quando houver.
9. Nova execução após correção, quando houver falha.
10. Confirmação de que o resultado corresponde ao HEAD atualmente proposto para merge.

## Diagnóstico de `NO_EVIDENCE`

Quando o HEAD não possuir workflow run verificável, diagnosticar nesta ordem, sem alterar Core/runtime para contornar o bloqueio:

```text
HEAD
 ↓
workflow existente e válido?
 ↓ não → corrigir somente workflow/configuração
 ↓ sim
trigger compatível com os arquivos alterados?
 ↓ não → ajustar trigger/path quando semanticamente correto
 ↓ sim
Actions disponíveis/ativas para o repositório?
 ↓ não → registrar bloqueio administrativo
 ↓ sim
nova execução
 ↓
workflow run + jobs + status
```

Nenhum teste documental ou comentário manual substitui um workflow run real.

## Estados possíveis

- `PASS`: workflow run registrado e todos os gates necessários passaram.
- `FAIL`: workflow run registrado e um ou mais gates falharam.
- `CANCELLED`: execução não produz evidência de aprovação.
- `NO_EVIDENCE`: nenhum run/status disponível para o HEAD.
- `BLOCKED`: não é permitido fazer merge, depreciação ou remoção.

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

Se `NO_EVIDENCE`:

```text
investigar trigger/infraestrutura
→ corrigir somente o mecanismo de evidência
→ novo commit
→ nova execução
→ revalidação
```

Nunca considerar a condição resolvida apenas por comentário ou aprovação manual.

## Consolidação de conhecimento

O registry documental é instrumento de identidade, auditoria, proveniência e reconciliação. Ele não substitui o `SourceResolver` existente nem cria uma segunda autoridade runtime.

Para cada artefato consolidável, preservar:

- `artifact_id` estável;
- `concept_id` estável;
- canonical path;
- legacy paths/aliases;
- status real;
- versão;
- content hash;
- autoridade;
- domínio;
- idioma;
- proveniência;
- referências e consumidores.

Famílias `scaffold`, `discovery`, `pending` ou equivalentes não devem ser preenchidas artificialmente para produzir aparência de completude.

## Regra de merge

O PR somente pode ser candidato a merge quando:

```text
CI = PASS
AND
T01–T10 = PASS quando aplicável
AND
nenhum conflito arquitetural pendente
AND
nenhuma referência crítica órfã
AND
nenhuma autoridade duplicada criada
AND
revisão independente exigida pelo Ruleset concluída
```

## Regra de depreciação

Mesmo com CI PASS, depreciação de caminho histórico exige validação de consumidores, identidade e proveniência.

## Regra de remoção

Remoção física exige todos os gates anteriores e confirmação de que não existe conteúdo exclusivo ou dependência histórica não preservada.

## Integração com ELO

A ausência de evidência de CI deve ser apresentada ao ELO como condição técnica bloqueante. O ELO pode investigar a infraestrutura e propor correção, mas não deve converter ausência de evidência em aprovação.

## Objetivo de evolução

Esta frente melhora coerência, rastreabilidade, identidade e manutenção do conhecimento existente. Não deve reinventar o ELO, criar uma segunda autoridade ou promover conteúdo somente para satisfazer o CI.
