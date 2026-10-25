# HANDOFF — GPT → ELO

## Objetivo

Definir o pacote mínimo e verificável que o GPT envia ao ELO antes de apresentar uma resposta operacional relacionada a um objetivo governado.

## Contrato

```yaml
handoff_type: GPT_TO_ELO
objective_id: string
workstream_id: string
expected_checkpoint_version: integer|null
user_message: string
progress_token: string
evidence_refs:
  - string
proposed_next_action: string
context_summary: string|null
```

## Regras

1. `objective_id` e `workstream_id` devem vir de estado canônico ou contexto já confirmado.
2. Para execução existente, `expected_checkpoint_version` é obrigatório.
3. `progress_token` deve representar progresso observado; não pode ser fabricado pelo GPT.
4. `evidence_refs` deve conter referências reais.
5. `proposed_next_action` é proposta de handoff; não equivale à decisão do ELO.
6. `context_summary` serve apenas para transporte de contexto e não pode substituir evidência.
7. O GPT não envia `authorization_state=VALID` como declaração própria. A autorização é resolvida pelo `elo-authz`.

## Pré-condição

Se os campos obrigatórios não puderem ser obtidos de forma verificável, o handoff não deve ser enviado. O GPT deve reportar o GAP correspondente.

## Invariante

`GPT_TO_ELO` nunca concede autoridade. Ele apenas solicita avaliação ao owner canônico.