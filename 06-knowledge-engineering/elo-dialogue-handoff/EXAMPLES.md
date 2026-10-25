# EXAMPLES — ELO DIALOGUE HANDOFF

## 1. CONTINUE

Contexto preservado pelo GPT:

```yaml
user_message: "Continue"
tenant_id: tenant-multiteiner
objective_id: OBJ-1078
workstream_id: runtime-dialogue
```

Payload enviado ao endpoint canônico:

```yaml
tenant_id: tenant-multiteiner
objective_id: OBJ-1078
objective_title: "Validar continuidade ELO↔GPT"
workstream_id: runtime-dialogue
expected_checkpoint_version: 4
progress_token: "route-ready"
evidence_refs:
  - "github:7c6b6066"
proposed_next_action: "validar deployment de produção"
within_scope: true
authority_available: true
risk_level: LOW
```

Resposta do ELO Web:

```yaml
final_message: "ELO confirmou continuidade do objetivo."
decision: CONTINUE
next_action: "validar conexão MCP"
progress_token: "production-ready"
checkpoint_version: 5
should_continue_automatically: true
human_required: false
evidence_refs:
  - "github:7c6b6066"
  - "vercel:dpl_F7KxesWgFLtq4FxZbr8FtqKheQJb"
scenario_code: CONTINUE
replay_count: 1
authorization_authority: elo-authz
authorization_evidence_ref: "grant:evidence-ref"
authorization_operation: "continue_objective:OBJ-1078"
request_id: "request-123"
next_trigger:
  trigger_type: CONTINUE_OBJECTIVE
  objective_id: OBJ-1078
  workstream_id: runtime-dialogue
  checkpoint_version: 5
  next_action: "validar conexão MCP"
  progress_token: "production-ready"
```

Resultado: o GPT correlaciona a resposta com `tenant-multiteiner / OBJ-1078 / runtime-dialogue`, comunica a decisão e prepara somente o próximo handoff permitido.

## 2. CORRECT

Se o mesmo progress token reaparecer sem evidência nova, o ELO pode devolver `CORRECT`. O GPT não converte isso em `CONTINUE`.

## 3. REPLAN

Se a ausência de progresso persistir, o ELO pode devolver `REPLAN`. O GPT apresenta a nova `next_action` canônica e não mantém o plano anterior por conveniência.

## 4. ESCALATE

```yaml
decision: ESCALATE
human_required: true
should_continue_automatically: false
next_trigger: null
```

Resultado: o GPT para o loop e mostra ao usuário o motivo do escalonamento.

## 5. COMPLETE

```yaml
decision: COMPLETE
human_required: false
should_continue_automatically: false
next_trigger: null
```

Resultado: o GPT encerra o objetivo; não gera novo ciclo.

## 6. STALE CHECKPOINT

Se o GPT enviar `expected_checkpoint_version: 5` e o store observar `state_version: 6`, o runtime deve retornar `STALE_CHECKPOINT`.

Resultado: o GPT não tenta "corrigir" a versão pela conversa; relê o estado canônico.

## 7. AUTORIZAÇÃO AUSENTE — teste fail-closed

Se `elo-authz` não comprovar grant válido para `continue_objective:<objective_id>`, o ciclo não avança.

Resultado esperado:

```yaml
runtime_result: authorization_denied
checkpoint_created: false
next_trigger: null
```

O GPT informa que a autorização técnica está ausente e não simula a continuidade.

## 8. PRIMEIRA EXECUÇÃO

Quando ainda não existe checkpoint persistido, `expected_checkpoint_version` pode ser omitido. Isso não dispensa `tenant_id`, `objective_id`, `workstream_id`, evidência e autorização canônica.
