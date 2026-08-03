# Cognitive Interface Specification

## Objetivo

Especificar a interface cognitiva do ELO como ponto de entrada para solicitações humanas, sistemas externos e aplicações que consumem a EIP.

## Estrutura conceitual

A interface trabalha com:

- `CognitiveRequest`
- `Session`
- `SessionStore`
- `CognitiveResponse`
- provenance
- sources
- agents
- suggestions

## Fluxo

```text
Usuário / Sistema
      ↓
CognitiveRequest
      ↓
Interface API
      ↓
Security / Tenant / Domain
      ↓
SessionManager
      ↓
CognitiveCore
      ↓
Context → Knowledge → Reasoning → Decision
      ↓
ResponseBuilder
      ↓
Provenance + Sources + Confidence
      ↓
CognitiveResponse
```

## Regras

- a interface não deve conter regra central de negócio
- o domínio deve ser identificado por `domain`
- a sessão deve ser substituível por store persistente
- provenance deve acompanhar respostas relevantes
- confidence deve ser normalizada entre 0 e 1
- respostas devem ser canônicas e auditáveis

## Componentes

### contracts.py
Define os contratos canônicos de request/response e metadados de proveniência.

### session.py
Define `Session`, `SessionStore`, `InMemorySessionStore` e `SessionManager`.

### response.py
Converte saídas do núcleo cognitivo em `CognitiveResponse`.

### api.py
Expõe a API FastAPI e conecta a interface ao núcleo cognitivo.

### __init__.py
Expõe a API pública do pacote de interface.

## Exemplos

Fixtures e exemplos de respostas devem ficar em `examples/interface/` e nunca devem ser tratados como conhecimento empresarial real.

## Evolução

A implementação futura pode adicionar autenticação, autorização, roteamento por domínio, adaptadores de frontend e stores persistentes para sessão.
