# ELO Security

## Objetivo

Definir a camada transversal de segurança da EIP, protegendo identidade, dados, conhecimento, APIs, integrações, agentes e operações cognitivas.

## Princípios

- menor privilégio
- deny by default
- segregação entre autenticação e autorização
- proteção de segredos
- rastreabilidade de acesso
- isolamento entre empresas, usuários e agentes
- validação de toda entrada externa
- nenhuma IA externa é automaticamente confiável

## Escopo

A camada de segurança deve cobrir:

- autenticação
- autorização
- identidade de usuários e agentes
- controle de acesso a APIs
- proteção de dados e conhecimento
- credenciais de integrações
- políticas para provedores de IA
- auditoria de ações críticas
- isolamento de tenants quando aplicável

## Integração com outras IAs

Toda informação recebida de uma IA externa deve ser tratada como entrada não confiável até passar pelos controles da EIP.

O ELO deve registrar, quando aplicável:

- provedor
- modelo
- identidade do agente
- data e hora
- finalidade
- contexto enviado
- resposta recebida
- nível de confiança
- evidências
- política aplicada

## Ações críticas

Ações classificadas como críticas podem exigir aprovação humana, autorização adicional ou bloqueio completo conforme a política de governança.

## Segredos

Chaves de API, tokens, senhas e certificados não devem ser armazenados em código, documentação operacional pública ou commits do repositório.

## Relação com Governança

Segurança executa controles técnicos. Governança define políticas, responsabilidades, níveis de autonomia, requisitos de auditoria e exceções autorizadas.

## Evolução

Implementações futuras devem incluir modelos explícitos de identidade, autorização baseada em políticas e testes automatizados de segurança para fluxos críticos.
