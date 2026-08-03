# AI Provenance

## Objetivo

Registrar a proveniência de interações com IA para manter rastreabilidade, auditoria e confiabilidade das respostas recebidas pela EIP.

## Função

A camada de provenance captura o contexto da chamada, o provider utilizado, o modelo, o horário, a finalidade, os parâmetros relevantes e a resposta gerada.

## Campos recomendados

- request_id
- user_or_agent_id
- domain
- purpose
- provider
- model
- input_summary
- output_summary
- timestamp
- latency
- confidence
- evidence_refs
- policy_decision
- validation_result
- error_info

## Princípios

- provenance é obrigatória para chamadas cognitivas relevantes
- provenance deve ser imutável ou versionada
- provenance deve permitir auditoria posterior
- provenance não deve expor segredos desnecessários
- provenance deve ser consultável por governança e observabilidade

## Estrutura prevista

```text
provenance/
├── README.md
├── record.py
├── serializer.py
├── store.py
└── query.py
```

## Regras

- toda resposta relevante deve carregar uma trilha de origem
- o registro deve ser suficiente para reconstrução do fluxo cognitivo
- ações críticas devem ligar provenance à decisão e à política aplicada
