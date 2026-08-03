# AI Contracts

## Objetivo

Definir os contratos canônicos utilizados pela EIP para se comunicar com provedores de IA de forma independente de fornecedor.

## Conteúdo

Os contratos devem descrever:

- identidade da requisição
- finalidade
- contexto de entrada
- permissões e escopo
- provider solicitado ou elegível
- parâmetros de geração
- metadados de provenance
- formato esperado de resposta
- erros e restrições

## Princípios

- contrato canônico primeiro
- provider depois
- sem dependência de SDK no domínio
- compatibilidade entre provedores
- rastreabilidade e governança sempre presentes

## Tipos previstos

- AIRequest
- AIResponse
- AIContext
- AIProviderDescriptor
- AIProvenanceRecord
- AIPolicyDecision
- AIValidationResult

## Regras

- contratos devem ser estáveis e versionados
- entradas e saídas devem ser explicitamente tipadas quando houver implementação
- respostas não devem ocultar provider, modelo ou tempo de geração
- erros devem ser normalizados para permitir tratamento uniforme

## Estrutura prevista

```text
contracts/
├── README.md
├── request.py
├── response.py
├── context.py
├── provenance.py
├── policy.py
├── validation.py
└── exceptions.py
```
