# ELO — CI Trigger Probe

## Finalidade
Mudança mínima e não-runtime utilizada para gerar uma nova execução do `pull_request` para o PR #267 depois da revisão das configurações do GitHub Actions.

## Distinção terminológica

Este documento espera um **workflow run** do `ELO Evolution Gate` associado ao SHA do PR.

Ele não exige nem pressupõe um evento GitHub Actions chamado **`workflow_run`**. Esse evento é um mecanismo de gatilho distinto e somente deve ser mencionado se existir um workflow configurado explicitamente para utilizá-lo.

## Restrições de segurança

- somente documentação;
- nenhuma alteração de Core/runtime;
- nenhuma alteração do resolver;
- nenhum conteúdo de conhecimento alterado;
- nenhuma exclusão da árvore histórica;
- nenhuma migração semântica.

## Evidência esperada

O novo commit deve produzir um **workflow run** do `ELO Evolution Gate` associado ao SHA do PR.

Ausência de workflow run permanece:

```text
NO_EVIDENCE = BLOCKED
```

e não pode ser interpretada como teste aprovado ou reprovado.

## Próximos gates

1. Confirmar o workflow run associado ao SHA.
2. Inspecionar jobs e etapas.
3. Inspecionar `compileall` e `pytest`.
4. Executar/validar os testes canônicos T01–T10 quando materializados.
5. Corrigir falhas e repetir a validação até obter evidência verde.
6. Somente então avaliar prontidão para merge.

## Controle desta rodada — PR #267

O HEAD observado antes desta alteração era:

```text
a6da38625cd2028e5fb17fcb0a6c69c1dde4ec74
```

Esta alteração é deliberadamente limitada a documentação para provocar uma nova execução do fluxo `pull_request`, sem tocar no runtime ou no conteúdo canônico.

Após o commit, o novo SHA deverá ser consultado e o `ELO Evolution Gate` deverá ser localizado especificamente por esse SHA. A simples existência de uma execução antiga não satisfaz este gate.

```text
NOVO SHA
   ↓
workflow run associado
   ↓
jobs
   ↓
testes
   ↓
evidência
```

Até essa verificação:

```text
CI_HEAD = NO_EVIDENCE
MERGE = BLOCKED
```
