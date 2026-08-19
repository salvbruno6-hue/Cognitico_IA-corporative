# ELO — Protocolo de Disparo e Evidência de CI da Consolidação Canônica

## Objetivo
Garantir que a consolidação canônica somente avance quando existir evidência verificável de execução do CI para o commit efetivamente avaliado pelo PR.

## Situação observada
O commit `466213bf1de542d06f9620938a23a42f24fc39b1` não possui workflow run nem status registrado no GitHub Actions. Isso é tratado como `NO_EVIDENCE`, não como `PASS` ou `FAIL`.

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

## Estados possíveis

- `PASS`: execução registrada e todos os gates necessários passaram.
- `FAIL`: execução registrada e um ou mais gates falharam.
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
