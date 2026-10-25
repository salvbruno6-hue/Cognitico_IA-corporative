# HANDOFF — ELO → GPT

## Objetivo

Definir o retorno mínimo que o GPT deve aceitar do ELO após um ciclo governado.

## Contrato

```yaml
handoff_type: ELO_TO_GPT
objective_id: string
workstream_id: string
checkpoint_version: integer
decision: CONTINUE|CORRECT|REPLAN|ESCALATE|COMPLETE
progress_token: string
next_action: string
human_required: boolean
should_continue_automatically: boolean
evidence_refs:
  - string
final_message: string
next_trigger:
  trigger_type: CONTINUE_OBJECTIVE
  objective_id: string
  workstream_id: string
  checkpoint_version: integer
  next_action: string
  progress_token: string
  # null quando não houver continuidade permitida
```

## Validações obrigatórias

1. `objective_id` e `workstream_id` devem coincidir com o handoff enviado.
2. `checkpoint_version` deve avançar monotonicamente.
3. `decision` deve ser uma decisão canônica do ELO.
4. `human_required=true` implica `should_continue_automatically=false` e `next_trigger=null`.
5. `COMPLETE` implica ausência de novo trigger.
6. `ESCALATE` implica ausência de novo trigger.
7. `CONTINUE`, `CORRECT` e `REPLAN` só podem gerar trigger quando `should_continue_automatically=true`.
8. `evidence_refs` não pode ser vazio para um ciclo executado.

## Regra de apresentação

O GPT pode adaptar a linguagem para clareza, mas não pode alterar a decisão, o checkpoint, o progress token, a próxima ação ou o requisito humano.

## Rejeição

Se o retorno violar o contrato, o GPT deve tratá-lo como `INVALID_ELO_RETURN` e não prosseguir automaticamente.