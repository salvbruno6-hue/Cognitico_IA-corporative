# ELO Interface

## Objetivo

Definir a camada de interface cognitiva e API do ELO, responsável por receber solicitações, organizar sessão, acionar o núcleo cognitivo e devolver respostas canônicas com provenance, confidence e sugestões governadas.

## Escopo

- API FastAPI
- contratos canônicos
- sessões conversacionais
- resposta canônica
- integração com o núcleo cognitivo
- preparação para frontend e sistemas externos

## Fluxo

```text
Usuário / Sistema
      ↓
CognitiveRequest
      ↓
Interface API
      ↓
Session Manager
      ↓
CognitiveCore
      ↓
Context → Knowledge → Reasoning → Decision
      ↓
ResponseBuilder
      ↓
CognitiveResponse
```

## Princípios

- interface não contém regra central de negócio
- interface não conhece detalhes internos de providers de IA
- sessão deve ser substituível por store persistente
- respostas devem ser canônicas, rastreáveis e auditáveis
- o domínio é identificado por `domain`, não por departamento
- provenance deve acompanhar toda saída relevante

## Arquivos principais

- `contracts.py`
- `session.py`
- `response.py`
- `api.py`
- `__init__.py`

## Relação com a arquitetura

A camada de interface é a porta de entrada operacional da EIP. Ela conecta usuários, APIs e sistemas externos ao núcleo cognitivo sem acoplamento direto às fontes de IA ou aos sistemas corporativos.

## Evolução

A implementação futura pode incluir autenticação, autorização, roteamento por domínio, integração com frontend e stores persistentes de sessão.
