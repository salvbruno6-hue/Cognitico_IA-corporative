# Cognitico_IA-corporative

Fonte operacional oficial do ecossistema ELO.

## ELO Universal Bootstrap — LEIA PRIMEIRO

Este repositório é a fonte portátil de contexto do ELO. Uma IA conectada ao Git não deve depender de outra conta, conversa anterior, memória externa ou prompt oculto para compreender o ELO.

**Ponto de entrada obrigatório:** [`ELO_BOOTSTRAP.md`](ELO_BOOTSTRAP.md)

**Manifesto legível por máquina:** [`elo.manifest.json`](elo.manifest.json)

Fluxo mínimo para qualquer IA conectada ao repositório:

`ELO_BOOTSTRAP.md → README.md → AGENTS.md → ELO_REPOSITORY_NAVIGATION_RULES.md → ELO_ARTIFACT_METADATA_STANDARD.md → ELO_AI_AGENT_WORKING_RULES.md → arquitetura/contratos → src/elo → testes → Issues/PRs`

O bootstrap define identidade, separação Cognitivo/Core/Forge/Application/Infrastructure, memória, proveniência, ciclo cognitivo, regra estratégica pós-resolução, orçamento governado e protocolo de navegação.

## Diretriz atual

O repositório está estruturado como a base documental e operacional do ELO Enterprise Integration Platform (EIP), com foco em:

- organização da camada de conhecimento;
- consolidação da arquitetura core e cognitiva;
- definição das camadas de domínio, aplicação e infraestrutura;
- integração futura com serviços externos;
- execução controlada por contratos, testes, governança e evidências;
- portabilidade do contexto do ELO entre IAs e ambientes conectados ao Git.

## Governança de navegação e IA

Antes de criar ou alterar qualquer artefato, consulte:

1. [`ELO_BOOTSTRAP.md`](ELO_BOOTSTRAP.md) — contrato portátil de entrada;
2. [`AGENTS.md`](AGENTS.md) — regras operacionais para agentes de IA;
3. [`ELO_REPOSITORY_NAVIGATION_RULES.md`](ELO_REPOSITORY_NAVIGATION_RULES.md) — mapa semântico, autoridade e regras de pastas;
4. [`ELO_ARTIFACT_METADATA_STANDARD.md`](ELO_ARTIFACT_METADATA_STANDARD.md) — identidade, autoridade e maturidade de artefatos;
5. [`ELO_AI_AGENT_WORKING_RULES.md`](ELO_AI_AGENT_WORKING_RULES.md) — protocolo detalhado de continuidade entre IAs.

Esses documentos não substituem a arquitetura normativa ou ADRs aprovados. Eles orientam a navegação, classificação, execução e revisão do trabalho.

## Como consultar o ELO de qualquer lugar

Se uma ferramenta permite conectar ou clonar este repositório, ela possui a base necessária para reconstruir o contexto do ELO.

1. Conecte `salvbruno6-hue/Cognitico_IA-corporative`.
2. Abra `ELO_BOOTSTRAP.md`.
3. Leia o `elo.manifest.json` se a ferramenta preferir contexto estruturado.
4. Siga os arquivos obrigatórios indicados pelo bootstrap.
5. Para uma pergunta específica, busque primeiro o contrato/capacidade existente e depois a implementação.
6. Para mudanças, consulte Issues/PRs e evidências de CI antes de criar algo novo.

**Importante:** acesso ao Git resolve a portabilidade do conhecimento. A capacidade de executar código, criar PRs, acessar dados privados ou realizar ações externas depende das permissões e ferramentas disponíveis na integração utilizada.

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

## Status semântico

Não confundir documentação com capacidade implementada:

`DOCUMENTADO ≠ CONTRATADO ≠ IMPLEMENTADO ≠ TESTADO ≠ VERIFICADO ≠ EVOLUTION-GATED`

## Próximo marco

Consolidar a estrutura do core e da camada cognitiva do ELO, preservando a separação entre conhecimento, aplicação, infraestrutura e integrações, enquanto a base portátil permite que diferentes IAs reconstruam o mesmo contexto canônico a partir do Git.
