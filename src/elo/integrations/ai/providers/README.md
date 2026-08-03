# AI Providers

## Objetivo

Definir a camada de adaptadores específicos para cada provedor de IA suportado pela EIP.

## Função

Cada provider encapsula detalhes de SDK, autenticação, limites, formatos nativos e peculiaridades de integração sem expor essas diferenças ao núcleo do ELO.

## Providers previstos

- OpenAI
- Anthropic
- DeepSeek
- Gemini
- modelos locais
- futuros fornecedores compatíveis

## Responsabilidades

- autenticar com o provedor
- converter o contrato canônico para o formato nativo
- realizar a chamada remota ou local
- capturar metadados de origem e modelo
- tratar erros específicos do fornecedor
- devolver resposta já normalizada ou informação necessária para normalização

## Princípios

- provider é substituível
- SDK do fornecedor não deve vazar para a camada cognitiva
- o provider não decide política; ele executa a chamada
- credenciais e parâmetros sensíveis vêm da configuração segura

## Estrutura prevista

```text
providers/
├── README.md
├── openai/
├── anthropic/
├── deepseek/
├── gemini/
└── local/
```

## Regras

- todo provider deve implementar o mesmo contrato canônico
- respostas devem preservar identidade do provedor e do modelo
- nenhuma implementação pode ignorar políticas de segurança e governança
