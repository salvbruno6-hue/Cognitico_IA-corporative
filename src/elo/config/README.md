# ELO Configuration

## Objetivo

Definir a camada central de configuração da EIP, isolando parâmetros de ambiente, infraestrutura, integrações e provedores externos do código de domínio e do núcleo cognitivo.

## Princípios

- configuração externa ao código
- ausência de segredos no repositório
- validação explícita na inicialização
- valores padrão seguros
- independência de fornecedor de IA
- configuração específica por ambiente
- rastreabilidade das capacidades habilitadas

## Escopo

A camada de configuração deve administrar:

- ambiente e identidade da instância ELO
- API e serviços internos
- banco de dados
- cache e eventos
- armazenamento vetorial
- provedores de IA externos
- modelos locais
- segurança
- governança
- observabilidade

## Hierarquia de configuração

```text
Defaults seguros
      ↓
Arquivo de configuração não sensível
      ↓
Variáveis de ambiente
      ↓
Secret manager / runtime
      ↓
Configuração validada da aplicação
```

## Multi-IA

O ELO não deve depender de um fornecedor específico. OpenAI, Anthropic, DeepSeek, Gemini, modelos locais e futuros provedores devem ser acessados posteriormente por adaptadores governados.

A configuração deve identificar o provedor e suas capacidades sem permitir que credenciais ou detalhes específicos contaminem o domínio.

## Segurança

- `.env` real nunca deve ser versionado
- `.env.example` deve conter somente placeholders
- segredos de produção devem vir do ambiente ou de um secret manager
- logs não devem expor tokens, senhas ou chaves
- configurações críticas devem falhar de forma segura quando inválidas

## Governança

Parâmetros capazes de alterar comportamento cognitivo, nível de autonomia, aprovação humana ou acesso a provedores externos devem ser considerados configurações governadas.

## Relação com o Core

`src/elo/core` consome configuração validada, mas não deve conhecer detalhes de carregamento de arquivos `.env`, provedores externos ou mecanismos específicos de armazenamento de segredo.

## Evolução

A implementação futura deve usar modelos tipados de configuração e testes de validação antes de habilitar integrações reais.
