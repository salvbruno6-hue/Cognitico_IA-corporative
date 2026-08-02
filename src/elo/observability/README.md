# ELO Observability

## Objetivo

Definir a camada de observabilidade da EIP para permitir operação, diagnóstico, auditoria técnica e acompanhamento do comportamento dos componentes tradicionais e cognitivos.

## Princípios

- observabilidade por padrão
- correlação ponta a ponta
- logs estruturados
- métricas técnicas e cognitivas separadas
- proteção de dados sensíveis
- rastreabilidade de decisões assistidas
- independência da ferramenta de monitoramento

## Escopo

A observabilidade deve cobrir:

- API e serviços
- banco de dados
- cache e eventos
- integrações externas
- AI Gateway
- agentes
- RAG e recuperação de conhecimento
- reasoning e decision engines
- erros e exceções
- desempenho e disponibilidade

## Sinais fundamentais

### Logs

Devem registrar eventos técnicos e operacionais relevantes sem expor segredos ou conteúdo sensível desnecessário.

### Métricas

Devem incluir latência, erros, disponibilidade, consumo de recursos e indicadores específicos de componentes cognitivos.

### Traces

Devem permitir correlacionar uma solicitação desde a entrada na EIP até integrações, recuperação de conhecimento, raciocínio, decisão e resposta.

## Observabilidade cognitiva

Quando houver participação de IA, o ELO deve ser capaz de correlacionar:

```text
request
  ↓
context
  ↓
knowledge retrieval
  ↓
AI/provider invocation
  ↓
reasoning
  ↓
decision/recommendation
  ↓
response/action
```

A observabilidade não substitui a auditoria de governança, mas deve fornecer evidências técnicas para ela.

## Indicadores sugeridos

- tempo de resposta por domínio
- taxa de erro
- disponibilidade
- latência de provedores externos
- taxa de recuperação de conhecimento
- recomendações geradas
- recomendações aceitas/rejeitadas
- ações que exigiram aprovação humana
- falhas de política ou autorização

## Relação com Segurança

Logs e traces devem aplicar mascaramento e minimização de dados. Tokens, senhas, chaves e segredos nunca devem ser registrados.

## Evolução

OpenTelemetry, Prometheus ou outras ferramentas podem ser adotadas por adaptadores de infraestrutura sem criar dependência dessas tecnologias no domínio do ELO.
