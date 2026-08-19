# Cognitico_IA-corporative

Fonte operacional oficial do ecossistema ELO.

## Diretriz atual

O repositório é a base documental e operacional do **ELO Enterprise Integration Platform (EIP)**, preservando a separação entre arquitetura canônica, implementação executável, conhecimento, dados, governança, agentes e integrações.

O objetivo atual é evoluir o ELO de uma base cognitiva governada para uma plataforma capaz de receber contexto empresarial, evidências e experiências de múltiplos domínios, raciocinar sobre relações entre setores e orientar decisões humanas sem substituir a autoridade do gestor.

## Estado arquitetural consolidado

A evolução deve preservar estas capacidades e fronteiras:

- Cognitive Core e contratos canônicos;
- Context, Knowledge, Evidence e Memory;
- Reasoning, Critique, Scenario Intelligence e Decision Support;
- agentes governados e integração com fontes externas;
- provenance, validação, segurança e auditoria;
- Persistent Memory, RAG/Knowledge e Learning/Experience quando implementados e comprovados pelos gates;
- tenant isolation e governança específica por empresa;
- integração empresarial sem transformar o ELO em substituto de ERP, MES, CRM ou outros sistemas de registro;
- separação entre recomendação do ELO e decisão humana autorizada.

O manifesto canônico define como não negociáveis: não criar um segundo Core, não criar memória/autoridade canônica paralela, não inventar fatos, preservar histórico e proveniência, e promover conhecimento contextual para o Core somente após generalização, validação e evolution gate. fileciteturn527file0

## Multiteiner como Tenant Corporativo de Validação

A Multiteiner deve ser tratada como **tenant empresarial de validação**, e não como parte do Cognitive Core.

O contexto empresarial pode incluir, conforme as fontes autorizadas:

- Comercial;
- Engenharia;
- Compras;
- Financeiro;
- RH;
- Produção;
- Montagem;
- Manutenção;
- Qualidade;
- Logística;
- Segurança;
- processos, documentos, conversas, eventos, agentes, especialistas e fontes de dados.

A **Lista-Mãe** é uma fonte comercial/técnica de referência para orçamento, consulta e composição de produtos. Ela não é, isoladamente, a autoridade sobre estoque, compras, produção, financeiro ou realidade operacional. O ELO deve cruzá-la com outras fontes autorizadas e preservar a proveniência.

A taxonomia de módulos, relações produto/material, estruturas/BOM e visões como `MLT-M`, `MLT-M01` e `ESTRUTURAS-MODULARES` devem ser tratadas como modelos de consulta e relacionamento sobre uma fonte de dados estruturada, não como tabelas duplicadas para cada consulta.

## Modelo de interação empresarial

O ELO deve evoluir para:

```text
fonte/sistema/conversa/agente
        ↓
recebimento e quarentena quando aplicável
        ↓
contextualização
        ↓
evidência + proveniência
        ↓
correlação entre domínios
        ↓
fato / hipótese / lacuna / contradição
        ↓
consulta a especialista ou nova fonte
        ↓
cenários e impactos
        ↓
recomendação
        ↓
decisão humana autorizada
        ↓
resultado observado
        ↓
experiência e aprendizado governado
```

O ciclo cognitivo canônico do manifesto é `OBSERVE → CONTEXTUALIZE → ANALYZE → FORMULATE → DECIDE → EXECUTE → MONITOR → LEARN → FOLLOW-UP → REASSESS`. A passagem de leitura para escrita/executação exige autorização explícita e execução governada. fileciteturn527file0

## Gestão à vista e sistemas corporativos

A arquitetura deve permitir que uma mesma estrutura de dados alimente SQLite, SQL, Excel, dashboards e integrações corporativas, sem transformar o ELO em um ERP.

A separação recomendada é:

```text
ERP / sistemas de registro
        ↓
 dados e eventos
        ↓
 ELO Context + Evidence + Reasoning
        ↓
 análise / cenário / recomendação
        ↓
 decisão do responsável
```

O ELO interpreta e correlaciona informações; os sistemas de registro permanecem responsáveis pelos dados transacionais que lhes pertencem.

## Governança de navegação e IA

Antes de criar ou alterar qualquer artefato, consulte:

1. [`AGENTS.md`](AGENTS.md) — regras operacionais para agentes de IA;
2. [`ELO_REPOSITORY_NAVIGATION_RULES.md`](ELO_REPOSITORY_NAVIGATION_RULES.md) — mapa semântico, autoridade e regras de pastas;
3. [`ELO_ARTIFACT_METADATA_STANDARD.md`](ELO_ARTIFACT_METADATA_STANDARD.md) — identidade, autoridade e maturidade de artefatos;
4. [`ELO_AI_AGENT_WORKING_RULES.md`](ELO_AI_AGENT_WORKING_RULES.md) — protocolo detalhado de continuidade entre IAs.

Esses documentos não substituem a arquitetura normativa ou ADRs aprovados. Eles orientam navegação, classificação, execução e revisão.

## Estrutura de alto nível

- `00-empresa-manifesto/` — fundamentos empresariais históricos
- `00-enterprise-manifest/` — fundamentos empresariais e manifestos em inglês; consultar regras de autoridade
- `01-meta-arquitetura/` — princípios e visão arquitetural históricos
- `01-meta-architecture/` — camada operacional em inglês
- `02-architecture-library/` — biblioteca de arquitetura
- `03-process-library/` — biblioteca de processos
- `04-knowledge-handbook/` — conhecimento e manuais
- `05-cognitivo-plataforma/` — estrutura histórica/portuguesa
- `05-cognitive-platform/` — plataforma cognitiva operacional
- `06-knowledge-engineering/` — engenharia do conhecimento
- `07-engenharia-de dados/` — estrutura histórica/portuguesa
- `07-data-engineering/` — engenharia de dados operacional
- `08-ai/` — estrutura de IA
- `09-governance/` — governança corporativa
- `10-adr/` — decisões arquiteturais
- `11-modelos/` — biblioteca de modelos
- `12-sistemas/` — engenharia de sistemas
- `13-referências/` — referências externas
- `14-roteiros/` — roadmap e roteiros
- `15-ativos/` — ativos reutilizáveis
- `Docs/` — documentação evolutiva
- `src/elo/` — implementação executável do ELO

## Regra para diretórios duplicados

Existem variantes de nomenclatura em português e inglês. Isso é dívida estrutural conhecida, não duas arquiteturas independentes. Não criar novos diretórios equivalentes. Para novos artefatos canônicos, seguir o caminho operacional definido pelas regras de navegação e preservar o conteúdo histórico até decisão explícita de consolidação.

## Regra de maturidade

Uma capacidade não deve ser descrita como pronta apenas porque existe documentação ou código. A cadeia de maturidade é:

```text
requisito
→ arquitetura
→ contrato
→ implementação
→ teste
→ evidência
→ status operacional
```

Use os estados definidos em `ELO_REPOSITORY_NAVIGATION_RULES.md`: `PROPOSED`, `DRAFT`, `NORMATIVE`, `IMPLEMENTED`, `TESTED`, `VERIFIED`, `EXPERIMENTAL`, `DEPRECATED`, `SUPERSEDED`, `ROADMAP` e `BLOCKED`.

## Próximo marco

O próximo ciclo deve consolidar o **modelo canônico de dados corporativos da Multiteiner** — produto, módulo, material, estrutura/BOM, fornecedor, preço, estoque, orçamento e processo — e suas interfaces com Context, Evidence, Knowledge, Memory, Agents e Decision Support, evitando tabelas ou documentos duplicados e mantendo a Lista-Mãe como fonte de referência comercial/técnica onde aplicável.
