# ELO Interoperability Layer

## Objetivo

Definir a camada de interoperabilidade da EIP, responsável por integrar o ELO com sistemas empresariais e provedores de inteligência externos sem acoplar o núcleo a tecnologias específicas.

## Escopo

- AI Gateway
- AI providers
- enterprise systems
- contracts and adapters
- provenance and validation
- policy enforcement
- cross-system orchestration
- Central de Inteligências

## Princípios

- o ELO integra, não se subordina, a fontes externas
- nenhuma fonte externa é automaticamente fonte de verdade
- integrações devem ser contratualizadas
- cada integração deve preservar rastreabilidade e governança
- adaptadores isolam o núcleo de detalhes de fornecedores e sistemas
- interoperabilidade deve servir tanto a IA quanto a sistemas corporativos tradicionais
- a Central de Inteligências é uma superfície de produto sobre os mesmos contratos governados, não um novo caminho de integração

## Dois ramos principais

### 1. AI Integration

Integração com modelos e plataformas de IA externas ou locais, incluindo:

- OpenAI
- Anthropic
- DeepSeek
- Gemini
- modelos locais
- futuros provedores

### 2. Enterprise Integration

Integração com sistemas empresariais e industriais, incluindo:

- ERP
- MES
- PLM
- WMS
- bancos de dados
- APIs internas e externas
- legados
- filas e eventos

## Central de Inteligências

A arquitetura prevê dois modos de uso:

- **IA por trás do ELO:** o Intelligence Router seleciona a capacidade e o usuário recebe a missão consolidada sem precisar escolher o provider.
- **IA aberta dentro da Casa do ELO:** usuário autenticado e autorizado poderá abrir uma inteligência disponibilizada pela Central, sempre através do gateway/adapters, preservando tenant, permissões, provenance e políticas.

O contrato detalhado está em `ELO_CENTRAL_INTELLIGENCE_ARCHITECTURE.md` e `CENTRAL_INTELLIGENCE_PRODUCT_CONTRACT.md`.

## Relação com a EIP

A interoperabilidade é o mecanismo que permite ao ELO operar como plataforma industrial genérica, recebendo e consolidando informações de diferentes empresas, fontes e IAs sem perder identidade arquitetural.

## Regras

- toda integração deve possuir contrato explícito
- toda entrada externa deve passar por validação
- provenance deve ser preservada
- políticas de segurança e governança devem ser aplicadas antes do consumo
- integrações não podem substituir decisões ou regras centrais do domínio
- providers externos não são memória canônica do ELO
- credenciais devem permanecer somente no ambiente seguro de execução

## Evolução futura

A implementação deve ser dividida em gateway, contratos, adapters, provenance, validation e policies, com separação clara entre AI integration e enterprise integration. A Central de Inteligências reutilizará essa fundação para a experiência multiusuário da Casa do ELO.
