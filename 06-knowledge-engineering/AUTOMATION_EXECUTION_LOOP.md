# Contrato de execução das automações no Loop ELO

O Loop operacional agora possui quatro fronteiras explícitas:

`ExecutionRequest → ExecutionAuthorization → Automation → ExecutionResult → AutomationEvidence`

Responsabilidades:

- **ELO**: decide e autoriza dentro das regras canônicas.
- **Automation Registry/Executor**: encaminha somente ações autorizadas.
- **Automação**: executa o processo delimitado e retorna resultado/evidência.
- **SymbiontLabAdapter**: interpreta evidência laboratorial.
- **EvolutionGate**: classifica evolução.
- **Learning Governance**: controla experiência/candidato/promoção.

A automação nunca transforma `COMPLETED` em aprendizado automaticamente.

## Estados

`REQUESTED → AUTHORIZED → RUNNING → COMPLETED`

Terminais alternativos:

`BLOCKED | ESCALATED | FAILED | ROLLED_BACK`

## Regra de evidência

Uma execução `COMPLETED` exige:

1. `result_ref`;
2. `evidence_ids`;
3. objetos `AutomationEvidence` correspondentes à execução.

Sem evidência, a execução não pode fechar como concluída.

## Regra de autorização

A execução exige:

- identidade da execução;
- identidade da automação;
- escopo;
- autoridade explícita;
- evidência da autorização.

A automação não pode autoautorizar sua execução.

## Reentrada no Loop

Após a execução:

`AutomationEvidence → SymbiontLabObservation → SymbiontLabAdapter → EvolutionGate`

A transformação em observação laboratorial continua exigindo os campos laboratoriais explícitos. Nenhum campo de hipótese, baseline, experimento, resultado, regressão ou generalização é inferido automaticamente.
