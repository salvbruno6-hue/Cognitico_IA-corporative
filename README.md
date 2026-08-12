# Cognitico_IA-corporative

Fonte operacional oficial do ecossistema ELO.

## Diretriz atual

O repositório está sendo estruturado como a base documental e operacional do ELO Enterprise Integration Platform (EIP), com foco em:

- organização da camada de conhecimento;
- consolidação da arquitetura core e cognitiva;
- definição das camadas de domínio, aplicação e infraestrutura;
- preparação para integração futura com serviços externos;
- execução controlada por contratos, testes, governança e evidências.

## Governança de navegação e IA

Antes de criar ou alterar qualquer artefato, consulte:

1. [`AGENTS.md`](AGENTS.md) — regras operacionais para agentes de IA;
2. [`ELO_REPOSITORY_NAVIGATION_RULES.md`](ELO_REPOSITORY_NAVIGATION_RULES.md) — mapa semântico, autoridade e regras de pastas;
3. [`ELO_ARTIFACT_METADATA_STANDARD.md`](ELO_ARTIFACT_METADATA_STANDARD.md) — identidade, autoridade e maturidade de artefatos;
4. [`ELO_AI_AGENT_WORKING_RULES.md`](ELO_AI_AGENT_WORKING_RULES.md) — protocolo detalhado de continuidade entre IAs.

Esses documentos não substituem a arquitetura normativa ou ADRs aprovados. Eles orientam a navegação, classificação, execução e revisão do trabalho.

## Estrutura de alto nível

- `00-empresa-manifesto/` — fundamentos empresariais
- `00-enterprise-manifest/` — fundamentos empresariais e manifestos em inglês; consultar regras de autoridade antes de adicionar conteúdo
- `01-meta-arquitetura/` — princípios e visão arquitetural
- `01-meta-architecture/` — camada equivalente em inglês; consultar regras de autoridade antes de adicionar conteúdo
- `02-architecture-library/` — biblioteca de arquitetura
- `03-process-library/` — biblioteca de processos
- `04-knowledge-handbook/` — conhecimento e manuais
- `05-cognitivo-plataforma/` — plataforma cognitiva em estrutura histórica/portuguesa
- `05-cognitive-platform/` — plataforma cognitiva operacional em inglês
- `06-knowledge-engineering/` — engenharia do conhecimento
- `07-engenharia-de dados/` — estrutura histórica/portuguesa de engenharia de dados
- `07-data-engineering/` — engenharia de dados operacional em inglês
- `08-ai/` — estrutura de IA
- `09-governance/` — governança corporativa
- `10-adr/` — registro de decisões arquiteturais
- `11-modelos/` — biblioteca de modelos
- `12-sistemas/` — engenharia de sistemas
- `13-referências/` — arquitetura de referência
- `14-roteiros/` — roadmap e roteiros
- `15-ativos/` — ativos reutilizáveis
- `Docs/` — documentação evolutiva
- `src/elo/` — núcleo de implementação do ELO

## Regra para diretórios duplicados

Existem atualmente variantes de nomenclatura em português e inglês. Isso é dívida estrutural conhecida, não duas arquiteturas independentes.

Não criar novos diretórios equivalentes. Para novos artefatos canônicos, usar o caminho operacional indicado pelas regras de navegação e preservar o conteúdo histórico até uma decisão explícita de consolidação.

## Próximo marco

A próxima etapa é consolidar a estrutura do core e da camada cognitiva do ELO, preservando a separação entre conhecimento, aplicação, infraestrutura e futuras integrações.
