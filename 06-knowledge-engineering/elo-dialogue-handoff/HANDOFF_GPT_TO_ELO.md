# HANDOFF — GPT → ELO

## Objetivo

Definir o pacote mínimo e verificável que o GPT envia ao ELO antes de apresentar uma resposta operacional relacionada a um objetivo governado.

## Contrato de transporte

A skill transporta apenas campos aceitos pelo runtime canônico `POST /api/elo/chat/prefinalize`. Ela não cria uma segunda API nem um envelope que substitua o contrato do ELO Web.

```yaml
tenant_id: string
objective_id: string
workstream_id: string
progress_token: string
proposed_next_action: string
evidence_refs:
  - string
objective_title: string|null
expected_checkpoint_version: integer|null
objective_satisfied: boolean|null
within_scope: boolean|null
authority_available: boolean|null
risk_level: LOW|MEDIUM|HIGH|CRITICAL|null
max_cycles: integer|null
```

A mensagem do usuário e o resumo conversacional podem ser usados pelo GPT para construir o handoff, mas não são campos do endpoint canônico e não devem ser enviados como se fossem parte do contrato do runtime.

## Regras

1. `tenant_id`, `objective_id` e `workstream_id` devem vir de estado canônico ou contexto já confirmado; nenhum deles pode ser inventado.
2. Para execução existente, `expected_checkpoint_version` é obrigatório.
3. `progress_token` deve representar progresso observado; não pode ser fabricado pelo GPT.
4. `evidence_refs` deve conter referências reais.
5. `proposed_next_action` é proposta de handoff; não equivale à decisão do ELO.
6. `objective_satisfied`, `within_scope`, `authority_available`, `risk_level` e `max_cycles` são somente sinais de contexto aceitos pelo runtime; não concedem autorização.
7. O GPT não envia `authorization_state=VALID` nem qualquer declaração equivalente como prova própria. A autorização é resolvida pelo `elo-authz` dentro do ELO Web.
8. A correlação de resposta deve preservar localmente `tenant_id`, `objective_id` e `workstream_id`, porque o runtime não é obrigado a ecoar os três campos no topo da resposta.

## Pré-condição

Se os campos obrigatórios não puderem ser obtidos de forma verificável, o handoff não deve ser enviado. O GPT deve reportar o GAP correspondente.

## Invariante

`GPT_TO_ELO` nunca concede autoridade. Ele apenas solicita avaliação ao owner canônico.
