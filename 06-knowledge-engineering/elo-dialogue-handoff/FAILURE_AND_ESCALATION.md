# FAILURE AND ESCALATION

## Objetivo

Padronizar quando o GPT deve interromper continuidade automática e apresentar um bloqueio real em vez de simular execução.

## Falhas estruturais

- `STORE_UNAVAILABLE` — persistência durável indisponível;
- `AUTHORIZATION_REQUIRED` — autorização ausente;
- `AUTHORIZATION_DENIED` — autorização negada/revogada;
- `STALE_CHECKPOINT` — versão esperada divergente;
- `INVALID_ELO_RETURN` — retorno incompatível com contrato;
- `INSUFFICIENT_EVIDENCE` — evidência insuficiente;
- `TERMINAL_CHECKPOINT` — objetivo/workstream em estado terminal;
- `RUNTIME_UNAVAILABLE` — ELO Web/MCP indisponível.

## Escalonamento humano

Interromper continuidade automática quando o ELO retornar `ESCALATE` ou `human_required=true`, incluindo:

- ação fora do escopo autorizado;
- risco HIGH/CRITICAL;
- autoridade necessária indisponível;
- limite de ciclos/no-progress atingido;
- mudança estrutural que exija decisão humana;
- credencial/grant expirado.

## Regra de resposta

O GPT deve apresentar:

1. estado observado;
2. motivo do bloqueio;
3. evidência disponível;
4. próxima intervenção necessária;
5. checkpoint atual quando disponível.

Nunca substituir falha por uma narrativa de sucesso.