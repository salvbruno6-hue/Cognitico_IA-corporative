# ELO AI Integration

## Objetivo

Definir a arquitetura de interoperabilidade entre a EIP e provedores de inteligência artificial externos ou locais, preservando independência tecnológica, segurança, proveniência e governança.

## Princípio central

O ELO é o sistema coordenador. Provedores de IA são capacidades externas intercambiáveis e não constituem fonte de verdade por si mesmos.

## Componentes

- Gateway: ponto único de entrada para chamadas a provedores.
- Contracts: contratos neutros de requisição e resposta.
- Providers: adaptadores específicos de cada fornecedor.
- Provenance: registro de origem, modelo, horário, evidências e contexto.
- Validation: validação técnica, semântica e de segurança das respostas.
- Policies: regras de uso, autonomia, custo, privacidade e aprovação.

## Provedores previstos

- OpenAI
- Anthropic
- DeepSeek
- Gemini
- modelos locais
- futuros provedores compatíveis com os contratos da EIP

## Fluxo

```text
ELO Cognitive Layer
       ↓
AI Gateway
       ↓
Policy + Security
       ↓
Provider Adapter
       ↓
External/Local AI
       ↓
Validation + Provenance
       ↓
Context / Knowledge / Reasoning / Decision
```

## Regras

- nenhum domínio deve chamar diretamente SDK de fornecedor
- credenciais pertencem à camada de configuração/segredos
- toda resposta deve preservar identidade do provedor e modelo
- conteúdo externo deve ser validado antes de alimentar decisões
- políticas podem bloquear, redirecionar ou exigir aprovação
- troca de provedor não deve exigir alteração das regras centrais de negócio

## Estrutura prevista

```text
ai/
├── README.md
├── gateway/
├── contracts/
├── providers/
├── provenance/
├── validation/
└── policies/
```
