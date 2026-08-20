# Cognitico_IA-corporative

Fonte operacional oficial do ecossistema ELO.

## Diretriz atual

O repositório é a base documental e operacional do **ELO Enterprise Integration Platform (EIP)**, preservando a separação entre arquitetura canônica, implementação executável, conhecimento, dados, governança, agentes e integrações.

O objetivo é evoluir o ELO de uma base cognitiva governada para uma plataforma capaz de receber contexto empresarial, evidências e experiências de múltiplos domínios, raciocinar sobre relações entre setores e orientar decisões humanas sem substituir a autoridade do gestor.

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

O manifesto canônico define como não negociáveis: não criar um segundo Core, não criar memória/autoridade canônica paralela, não inventar fatos, preservar histórico e proveniência, e promover conhecimento contextual para o Core somente após generalização, validação e evolution gate.

## Consolidação documental validada

A reconciliação dos masters documentais duplicados foi executada em etapas de identificação, classificação, canonicalização, depreciação, auditoria de consumidores/referências e remoção física segura.

Os seguintes masters legados foram **deprecados, substituídos por owners canônicos e removidos fisicamente** no PR #271:

| Artefato legado removido | Owner canônico preservado |
|---|---|
| `07-engenharia-de dados/DATA_ENGINEERING_MASTER.md` | `07-data-engineering/DATA_ENGINEERING_MASTER.md` |
| `11-modelos/MODELS_LIBRARY_MASTER.md` | `11-models-library/MODELS_LIBRARY_MASTER.md` |
| `12-sistemas/SYSTEMS_ENGINEERING_MASTER.md` | `12-system-engineering/SYSTEMS_ENGINEERING_MASTER.md` |
| `14-roteiros/ROADMAP_MASTER.md` | `14-roadmap/ROADMAP_MASTER.md` |

A remoção foi validada no `main` pelo commit `9e7ace20698175f9c4e89947dc44ef3a05b43511`. Os workflows pós-merge **ELO PR1 Validation #476**, **ELO Behavioral Validation #872** e **ELO Evolution Gate #791** concluíram com sucesso.

A remoção foi limitada aos quatro masters redundantes. Documentos especializados, históricos e complementares não foram removidos apenas por semelhança nominal.

## Auditoria estrutural atual — duplicidades ainda existentes

A remoção dos masters **não significa que todas as duplicidades de diretórios foram eliminadas**. A árvore atual ainda contém variantes históricas em português e owners operacionais em inglês. Essa condição é **dívida estrutural conhecida**, não duas arquiteturas independentes.

| Camada | Variante histórica / paralela | Owner operacional | Situação |
|---|---|---|---|
| 00 | `00-empresa-manifesto/` | `00-enterprise-manifest/` | consolidar após revisão de conteúdo |
| 01 | `01-meta-arquitetura/` | `01-meta-architecture/` | consolidar após revisão de conteúdo |
| 05 | `05-cognitivo-plataforma/` | `05-cognitive-platform/` | consolidar após revisão de conteúdo |
| 07 | `07-engenharia-de dados/` | `07-data-engineering/` | master legado já removido; conteúdo restante requer classificação |
| 13 | — | `13-reference-architecture/` | owner presente; não assumir `13-referências/` sem evidência |
| 15 | — | `15-assets/` | owner presente; não assumir `15-ativos/` sem evidência |

As pastas `11-modelos/`, `12-sistemas/` e `14-roteiros/` devem ser tratadas como referências históricas/especializadas somente quando efetivamente existentes na árvore atual; os masters legados correspondentes já foram removidos. O README não deve declarar caminhos como canônicos quando eles não existem fisicamente.

### Regra para esta dívida estrutural

1. Não criar novas pastas duplicadas.
2. Não copiar conteúdo entre variantes apenas para obter simetria.
3. Não remover diretórios históricos sem auditoria de conteúdo, consumidores, referências, aliases e proveniência.
4. Para novos artefatos canônicos, utilizar o owner operacional definido em `ELO_REPOSITORY_NAVIGATION_RULES.md`.
5. Consolidar variantes por ADR/decisão explícita quando a análise comprovar que não existe conteúdo ou consumidor que justifique sua permanência.
6. Atualizar este README somente com caminhos comprovados pela árvore do `main`.

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

O ciclo cognitivo canônico do manifesto é `OBSERVE → CONTEXTUALIZE → ANALYZE → FORMULATE → DECIDE → EXECUTE → MONITOR → LEARN → FOLLOW-UP → REASSESS`. A passagem de leitura para escrita/executação exige autorização explícita e execução governada.

## Gestão à vista e sistemas corporativos

A arquitetura deve permitir que uma mesma estrutura de dados alimente SQLite, SQL, Excel, dashboards e integrações corporativas, sem transformar o ELO em um ERP.

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

## Estrutura de alto nível atual

- `00-enterprise-manifest/` — fundamentos empresariais e manifesto operacional
- `00-empresa-manifesto/` — variante histórica em português; requer auditoria antes de consolidação
- `01-meta-architecture/` — meta-arquitetura operacional
- `01-meta-arquitetura/` — variante histórica em português; requer auditoria antes de consolidação
- `02-architecture-library/` — biblioteca de arquitetura
- `03-process-library/` — biblioteca de processos
- `04-knowledge-handbook/` — conhecimento e manuais
- `05-cognitive-platform/` — plataforma cognitiva operacional
- `05-cognitivo-plataforma/` — variante histórica em português; requer auditoria antes de consolidação
- `06-knowledge-engineering/` — engenharia do conhecimento
- `07-data-engineering/` — engenharia de dados operacional e owner canônico
- `07-engenharia-de dados/` — variante histórica em português; masters legados removidos
- `08-ai/` — arquitetura e governança de IA
- `09-governance/` — governança corporativa
- `10-adr/` — decisões arquiteturais
- `11-models-library/` — biblioteca de modelos e owner canônico do master
- `12-system-engineering/` — engenharia de sistemas e owner canônico do master
- `13-reference-architecture/` — arquitetura de referência
- `14-roadmap/` — roadmap e owner canônico do master
- `15-assets/` — ativos reutilizáveis
- `Docs/` — documentação evolutiva e registros de migração
- `automation/` — automações
- `forge/` — plano construtor/executável governado
- `src/elo/` — implementação executável do ELO
- `tests/` — testes e evidências executáveis
- `runtime/` — componentes de runtime
- `memory/` — estruturas de memória e aprendizado governado
- `platform/` — utilidades de plataforma
- `scripts/` — scripts operacionais
- `prompts/` — prompts e contratos auxiliares
- `members/` — modelos/artefatos de membros e domínios
- `frontend/` — interface

A existência de uma pasta não determina, sozinha, sua autoridade. A autoridade deve ser determinada pelas regras de navegação, manifestos, ADRs, contratos canônicos, governança e evidências.

## Regra de duplicidade

Antes de adicionar um conceito, pesquisar:

- nome exato;
- sinônimos;
- abreviações;
- contrato equivalente;
- ADR equivalente;
- implementação existente;
- teste existente;
- item de roadmap existente.

Classificar o resultado como `REUSE`, `EXTEND`, `RELOCATE`, `CONSOLIDATE`, `NEW` ou `CONFLICT`. `NEW` somente é permitido depois de rejeitadas as demais classificações.

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

O próximo ciclo é a **auditoria e consolidação estrutural das variantes de diretórios ainda existentes**, sem remoção automática. Para cada variante, o ELO deve verificar conteúdo, consumidores, referências, aliases, autoridade e proveniência; somente então decidir `REUSE`, `RELOCATE`, `CONSOLIDATE`, `DEPRECATE` ou `REMOVE`.

Depois desse gate, o ciclo pode avançar para a consolidação do **modelo canônico de dados corporativos da Multiteiner** — produto, módulo, material, estrutura/BOM, fornecedor, preço, estoque, orçamento e processo — e suas interfaces com Context, Evidence, Knowledge, Memory, Agents e Decision Support, evitando novas duplicações.
