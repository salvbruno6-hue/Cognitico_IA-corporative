# HANDOFF — ELO → GPT

## Objetivo

Definir o retorno que o GPT deve aceitar do runtime canônico após um ciclo governado, sem exigir campos que o ELO Web não retorna.

## Resposta canônica do runtime

```yaml
final_message: string
decision: CONTINUE|CORRECT|REPLAN|ESCALATE|COMPLETE
next_action: string|null
progress_token: string
checkpoint_version: integer
should_continue_automatically: boolean
human_required: boolean
evidence_refs:
  - string
scenario_code: string
replay_count: integer
authorization_authority: elo-authz
authorization_evidence_ref: string
authorization_operation: string
request_id: string
next_trigger: null|object
```

Quando presente, `next_trigger` deve seguir:

```yaml
trigger_type: CONTINUE_OBJECTIVE
objective_id: string
workstream_id: string
checkpoint_version: integer
next_action: string
progress_token: string
```

## Correlação de identidade

`tenant_id`, `objective_id` e `workstream_id` pertencem ao contexto do handoff GPT→ELO. O GPT deve preservá-los para correlacionar a resposta. Eles **não são campos obrigatórios no topo da resposta atual do ELO Web**.

Quando houver `next_trigger`, `objective_id` e `workstream_id` nele devem coincidir com a requisição original.

## Validações obrigatórias

1. `checkpoint_version` deve avançar monotonicamente em relação ao checkpoint esperado quando houver retomada.
2. `decision` deve ser uma decisão canônica do ELO.
3. `authorization_authority` deve identificar `elo-authz`; o GPT não substitui essa evidência por autorização conversacional.
4. `authorization_operation` deve corresponder ao objetivo da requisição, no formato governado `continue_objective:<objective_id>`.
5. `human_required=true` implica `should_continue_automatically=false` e ausência de trigger de continuidade.
6. `COMPLETE` implica ausência de novo trigger.
7. `ESCALATE` implica ausência de novo trigger.
8. `CONTINUE`, `CORRECT` e `REPLAN` só podem gerar `next_trigger` quando `should_continue_automatically=true`.
9. Se houver `next_trigger`, seu `checkpoint_version`, `progress_token`, `next_action`, `objective_id` e `workstream_id` devem ser consistentes com a resposta e com a requisição original.
10. `replay_count` não pode exceder o limite definido pela Skill; nesta versão, `max_replays_per_turn = 1`.

## Regra de apresentação

O GPT pode adaptar a linguagem para clareza, mas não pode alterar decisão, checkpoint, progress token, próxima ação, requisito humano ou evidência de autorização.

## Erros do runtime

Respostas HTTP de erro, como `CHECKPOINT_VERSION_REQUIRED`, `STALE_CHECKPOINT`, ausência/negação de autorização ou indisponibilidade do store, não devem ser convertidas em `ELO_TO_GPT` de sucesso. Devem seguir `FAILURE_AND_ESCALATION.md`.

## Rejeição

Se uma resposta de sucesso violar o contrato, o GPT deve tratá-la como `INVALID_ELO_RETURN` e não prosseguir automaticamente.
