# CHECKPOINT CONTRACT

## Objetivo

Preservar continuidade monotônica, evitar replay stale e impedir que o diálogo seja tratado como estado persistente.

## Identidade

A chave lógica mínima do checkpoint é:

```text
(tenant_id, objective_id, workstream_id)
```

## Regras

1. `state_version` inicia no runtime persistente e só avança por ciclo governado aceito.
2. Ao retomar execução existente, o chamador deve fornecer `expected_checkpoint_version`.
3. Se `expected_checkpoint_version != state_version observado`, retornar `STALE_CHECKPOINT`.
4. O GPT não pode estimar ou reconstruir `state_version` a partir da conversa.
5. O `progress_token` deve refletir progresso observado e persistido.
6. Repetição do mesmo token não equivale automaticamente a novo progresso.
7. Estados terminais (`COMPLETED`, `HUMAN_APPROVAL_REQUIRED`, `BLOCKED`, `FAILED`) não podem ser avançados por continuidade automática comum.
8. Escrita concorrente deve usar compare-and-set/versão esperada.
9. Um turno conversacional produz no máximo um avanço de checkpoint pela skill.

## Fail-closed

Sem persistência durável ou sem leitura inequívoca do checkpoint, não continuar automaticamente.