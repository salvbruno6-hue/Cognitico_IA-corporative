# Enterprise Integration Events

## Objetivo

Definir os eventos de integração usados para comunicação entre o ELO e sistemas empresariais ou industriais.

## Função

Os eventos permitem transportar fatos relevantes entre sistemas sem acoplamento síncrono, preservando rastreabilidade, contexto e integridade de informação.

## Tipos previstos

- BusinessEvent
- IntegrationEvent
- SynchronizationEvent
- AuditEvent
- ChangeEvent
- NotificationEvent

## Responsabilidades

- publicar eventos canônicos
- consumir eventos externos
- mapear eventos para contratos internos
- registrar origem, destino e horário
- manter idempotência quando aplicável
- garantir observabilidade do fluxo

## Princípios

- evento deve representar fato ocorrido
- evento deve conter identidade e timestamp
- evento deve ser versionado quando o esquema mudar
- evento deve poder ser auditado
- eventos sensíveis devem passar por validação e políticas de segurança

## Estrutura prevista

```text
events/
├── README.md
├── business_event.py
├── integration_event.py
├── audit_event.py
├── sync_event.py
├── publisher.py
├── consumer.py
└── serializers.py
```

## Regras

- eventos não devem carregar lógica de negócio central
- o formato canônico deve ser consistente entre os sistemas integrados
- a origem do evento deve permanecer explícita
- eventos críticos devem ser observáveis e reprocessáveis
