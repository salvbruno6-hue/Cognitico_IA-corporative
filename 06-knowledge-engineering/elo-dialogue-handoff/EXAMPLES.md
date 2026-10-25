# EXAMPLES — ELO DIALOGUE HANDOFF

## 1. CONTINUE

Entrada GPT→ELO:

```yaml
handoff_type: GPT_TO_ELO
objective_id: OBJ-1078
workstream_id: runtime-dialogue
expected_checkpoint_version: 4
user_message: "Continue"
progress_token: "route-ready"
evidence_refs:
  - "github:7c6b6066"
proposed_next_action: "validar deployment de produção"
```

Retorno ELO→GPT:

```yaml
handoff_type: ELO_TO_GPT
objective_id: OBJ-1078
workstream_id: runtime-dialogue
checkpoint_version: 5
decision: CONTINUE
progress_token: "production-ready"
next_action: "validar conexão MCP"
human_required: false
should_continue_automatically: true
evidence_refs:
  - "github:7c6b6066"
  - "vercel:dpl_F7KxesWgFLtq4FxZbr8FtqKheQJb"
final_message: "ELO confirmou continuidade do objetivo."
```

Resultado: GPT comunica o retorno e prepara apenas o próximo handoff.

## 2. CORRECT

Se o mesmo progress token reaparecer sem evidência nova, o ELO pode devolver `CORRECT`. O GPT não converte isso em `CONTINUE`.

## 3. REPLAN

Se a ausência de progresso persistir, o ELO pode devolver `REPLAN`. O GPT deve apresentar a nova `next_action` canônica e não manter o plano anterior por conveniência.

## 4. ESCALATE

```yaml
decision: ESCALATE
human_required: true
should_continue_automatically: false
next_trigger: null
```

Resultado: GPT para o loop e mostra ao usuário o motivo do escalonamento.

## 5. COMPLETE

```yaml
decision: COMPLETE
human_required: false
should_continue_automatically: false
next_trigger: null
```

Resultado: GPT encerra o objetivo; não gera novo ciclo.

## 6. STALE CHECKPOINT

Se o GPT enviar `expected_checkpoint_version: 5` e o store observar `state_version: 6`, o runtime deve retornar `STALE_CHECKPOINT`.

Resultado: GPT não tenta "corrigir" a versão pela conversa; relê o estado canônico.

## 7. AUTORIZAÇÃO AUSENTE

Se `elo-authz` não comprovar grant válido, o ciclo não avança.

Resultado: GPT informa que a autorização técnica está ausente e não simula a continuidade.