# Cognitico_IA-corporative

Fonte operacional oficial do ecossistema ELO.

## Diretriz atual

O repositório é a base documental e operacional do **ELO Enterprise Integration Platform (EIP)**, preservando a separação entre arquitetura canônica, implementação executável, conhecimento, dados, governança, agentes e integrações.

O objetivo é evoluir o ELO de uma base cognitiva governada para uma plataforma capaz de receber contexto empresarial, evidências e experiências de múltiplos domínios, raciocinar sobre relações entre setores e orientar decisões humanas sem substituir a autoridade do gestor.

## Estado arquitetural consolidado

A evolução deve preservar:

- Cognitive Core e contratos canônicos;
- Context, Knowledge, Evidence e Memory;
- Reasoning, Critique, Scenario Intelligence e Decision Support;
- agentes governados e integração com fontes externas;
- provenance, validação, segurança e auditoria;
- Persistent Memory, RAG/Knowledge e Learning/Experience quando implementados e comprovados pelos gates;
- tenant isolation e governança específica por empresa;
- integração empresarial sem transformar o ELO em substituto de ERP, MES, CRM ou outros sistemas de registro;
- separação entre recomendação do ELO e decisão humana autorizada.

## ELO Cognitivo, Core e Forge — fronteira canônica

O ELO possui uma separação estrutural que deve permanecer explícita mesmo quando pastas históricas ou variantes documentais forem consolidadas:

```text
                 ELO COGNITIVO / SOUL
          identidade • cânone • autoridade
       invariantes • limites • evolução governada
                         │
                         ▼
                  ┌─────────────┐
                  │  ELO CORE   │
                  │              │
                  │ faculdade   │
                  │ cognitiva   │
                  │ compartilhada│
                  └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Context       Reasoning       Decision
      Knowledge     Relations       Evidence
      Memory        Generalization  Audit
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                      FORGE
          especialistas • skills • técnicas
        experiências • contexto • construção
                         │
                         ▼
                    APPLICATION
              interfaces e fluxos de uso
                         │
                         ▼
                  INFRASTRUCTURE
          banco • APIs • providers • runtime
```

### Localização do Core

O **Core canônico executável** está em:

`src/elo/core/`

Essa pasta não é uma variante documental nem um segundo Core. Ela materializa a faculdade cognitiva compartilhada do ELO e seus contratos reutilizáveis.

O Core deve permanecer:

- provider-neutral;
- reutilizável entre empresas e domínios;
- separado de regras específicas da Multiteiner ou de qualquer outro tenant;
- responsável por mecanismos cognitivos gerais, relações, padrões, heurísticas, parâmetros gerais validados e capacidades compartilhadas;
- integrado por contratos com Context, Knowledge, Memory, Evidence, Reasoning, Decision, Policy e Provenance.

### O que pertence a cada camada

| Camada | Responsabilidade | Não deve conter |
|---|---|---|
| **ELO Cognitivo / Soul** | identidade, cânone, autoridade, invariantes, governança e evolução | implementação específica de especialista |
| **Core** | faculdade cognitiva compartilhada, relações, generalização, raciocínio, auditoria e conhecimento geral validado | regras de negócio exclusivas de empresa/domínio |
| **Forge** | especialistas, skills, técnicas, experiências, parâmetros contextuais e construção/validação | segundo Core ou autoridade canônica paralela |
| **Application** | interfaces e fluxos que consomem capacidades do ELO | redefinição de contratos cognitivos |
| **Infrastructure** | bancos, APIs, providers, runtime e meios substituíveis | identidade ou autoridade do ELO |

Uma experiência contextual do Forge **não entra diretamente no Core**. Para promoção, ela deve passar por evidência, generalização, testes e Evolution Gate. A experiência de origem permanece preservada no Forge.

### Regra especial para orçamento e Lista-Mãe

O módulo de orçamento, a taxonomia MLT, os modelos M01/M02 etc., composições, valores, mão de obra e relações específicas da empresa não devem ser transformados automaticamente em conhecimento geral do Core.

O fluxo canônico é:

```text
Lista-Mãe / documento / orçamento
              ↓
          FORGE / especialista
              ↓
     classificação + relações
              ↓
     auditoria + evidência
              ↓
       generalização válida?
          ↙           ↘
        NÃO            SIM
         ↓              ↓
 experiência       Evolution Gate
 contextual             ↓
    Forge              Core
```

Assim, o Core pode fornecer mecanismos para correlacionar, classificar, comparar, auditar e generalizar, enquanto o Forge mantém o conhecimento contextual do especialista e da empresa.

## Loop de Conclusão — diretriz permanente de manutenção arquitetural

O **Loop de Conclusão** é um método permanente do ELO. Ele governa consolidação de pastas, migração de artefatos, resolução de duplicidades, aposentadoria de legado e qualquer manutenção estrutural que possa alterar a autoridade arquitetural.

```text
DETECTAR
  ↓
AUDITAR
  ↓
CLASSIFICAR ARQUIVO A ARQUIVO
  ↓
DEFINIR OWNER CANÔNICO
  ↓
ABSORVER SEMANTICAMENTE
  ↓
REORGANIZAR PARA FLUXO E COERÊNCIA
  ↓
RECONCILIAR artifact_id / legacy_path / aliases / referências / consumidores
  ↓
ATUALIZAR README / ÍNDICES / MAPAS / EVIDÊNCIAS
  ↓
TESTAR RESOLUÇÃO E INTEGRIDADE
  ↓
EXECUTAR GATES
  ↓
GATES APROVADOS → REMOÇÃO FÍSICA DO LEGADO
  ↓
VALIDAÇÃO PÓS-REMOÇÃO
  ↓
CONFIRMAR ZERO ÓRFÃOS / ZERO PERDA SEMÂNTICA / ZERO REFERÊNCIA LEGADA INDEVIDA
  ↓
MERGE
  ↓
VALIDAR MAIN
  ↓
REVARrer A ÁRVORE
  ↓
NOVA PENDÊNCIA? → VOLTAR AO INÍCIO
  ↓
NENHUMA PENDÊNCIA → ENCERRAR CICLO
```

### Regra de saída

O ELO **não declara um ciclo concluído** enquanto existir uma etapa necessária pendente. A remoção física do legado faz parte do próprio loop e somente ocorre depois da absorção semântica e da aprovação dos gates. Após a remoção, os testes e a varredura estrutural são executados novamente.

Critérios mínimos:

1. conteúdo relevante classificado;
2. conteúdo válido absorvido no owner canônico;
3. arquivos internos organizados com fluxo e sentido;
4. referências, consumidores, aliases, `artifact_id` e `legacy_path` reconciliados quando aplicáveis;
5. README, índices e evidências atualizados;
6. testes e gates verdes;
7. legado fisicamente removido somente após os gates;
8. validação pós-remoção sem órfãos ou regressões;
9. merge realizado e `main` validado;
10. nova varredura concluída.

A diretriz normativa está registrada em [`ELO_REPOSITORY_NAVIGATION_RULES.md`](ELO_REPOSITORY_NAVIGATION_RULES.md).

## Consolidação documental validada

A reconciliação das variantes documentais foi executada por auditoria de conteúdo, classificação semântica, definição de owner, absorção, reconciliação de referências, validação e remoção física controlada.

### Famílias consolidadas

| Família | Owner canônico | Resultado |
|---|---|---|
| `00` | `00-enterprise-manifest/` | variante portuguesa absorvida e removida |
| `05` | `05-cognitive-platform/` | variante portuguesa absorvida e removida |
| `07` | `07-data-engineering/` | conteúdo técnico absorvido e variante portuguesa removida |
| `09` | `09-governance/` | governance master absorvido e variante portuguesa removida |
| `11` | `11-models-library/` | master legado removido |
| `12` | `12-system-engineering/` | master legado removido |
| `14` | `14-roadmap/` | master legado removido |

Os masters legados de `07`, `11`, `12` e `14` foram deprecados e removidos no ciclo anterior. As famílias `00`, `05`, `07` e `09` passaram pela regra de absorção semântica antes da remoção das variantes.

### Família 07 — conteúdo absorvido

O conteúdo técnico anteriormente existente em `07-engenharia-de dados/` foi preservado no owner canônico `07-data-engineering/`:

- `01_Modelo_Logico.md`
- `02_Dicionario_Dados.md`
- `03_SQLite.md`
- `04_APIs.md`
- `05_Eventos.md`

A pasta histórica foi então removida.

### Família 09 — conteúdo absorvido

`09-governança/GOVERNANCE_MASTER.md` foi preservado em `09-governance/GOVERNANCE_MASTER.md` e a variante histórica foi removida.

A remoção não foi baseada apenas no nome. O conteúdo foi avaliado e incorporado ao owner operacional correspondente.

## Estado estrutural atual

A árvore canônica atual utiliza uma única pasta operacional por família numerada:

- `00-enterprise-manifest/` — fundamentos empresariais e manifesto operacional
- `01-meta-architecture/` — meta-arquitetura operacional
- `02-architecture-library/` — biblioteca de arquitetura
- `03-process-library/` — biblioteca de processos
- `04-knowledge-handbook/` — conhecimento e manuais
- `05-cognitive-platform/` — plataforma cognitiva operacional
- `06-knowledge-engineering/` — engenharia do conhecimento
- `07-data-engineering/` — engenharia de dados operacional e owner canônico
- `08-ai/` — arquitetura e governança de IA
- `09-governance/` — governança corporativa
- `10-adr/` — decisões arquiteturais
- `11-models-library/` — biblioteca de modelos
- `12-system-engineering/` — engenharia de sistemas
- `13-reference-architecture/` — arquitetura de referência
- `14-roadmap/` — roadmap
- `15-assets/` — ativos reutilizáveis
- `Docs/` — documentação evolutiva e registros de migração
- `automation/` — automações
- `forge/` — plano construtor/executável governado
- `src/elo/` — implementação executável do ELO; o Core canônico está em `src/elo/core/`
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

Classificar como `REUSE`, `EXTEND`, `RELOCATE`, `CONSOLIDATE`, `NEW` ou `CONFLICT`. `NEW` somente é permitido depois de rejeitadas as demais classificações.

Não criar nova pasta paralela para obter simetria entre português e inglês. Conteúdo histórico deve ser auditado antes de qualquer remoção.

## Regra de maturidade

Uma capacidade não deve ser descrita como pronta apenas porque existe documentação ou código. A cadeia é:

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

## Multiteiner como Tenant Corporativo de Validação

A Multiteiner deve ser tratada como **tenant empresarial de validação**, e não como parte do Cognitive Core.

O contexto empresarial pode incluir Comercial, Engenharia, Compras, Financeiro, RH, Produção, Montagem, Manutenção, Qualidade, Logística, Segurança, processos, documentos, conversas, eventos, agentes, especialistas e fontes de dados.

A Lista-Mãe é uma fonte comercial/técnica de referência para orçamento, consulta e composição de produtos. Ela não é, isoladamente, a autoridade sobre estoque, compras, produção, financeiro ou realidade operacional. O ELO deve cruzá-la com outras fontes autorizadas e preservar a proveniência.

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

O ciclo cognitivo canônico é `OBSERVE → CONTEXTUALIZE → ANALYZE → FORMULATE → DECIDE → EXECUTE → MONITOR → LEARN → FOLLOW-UP → REASSESS`. A passagem de leitura para escrita/executação exige autorização explícita e execução governada.

## Governança de navegação e IA

Antes de criar ou alterar qualquer artefato, consulte:

1. [`AGENTS.md`](AGENTS.md) — regras operacionais para agentes de IA;
2. [`ELO_REPOSITORY_NAVIGATION_RULES.md`](ELO_REPOSITORY_NAVIGATION_RULES.md) — mapa semântico, autoridade e Loop de Conclusão;
3. [`ELO_ARTIFACT_METADATA_STANDARD.md`](ELO_ARTIFACT_METADATA_STANDARD.md) — identidade, autoridade e maturidade de artefatos;
4. [`ELO_AI_AGENT_WORKING_RULES.md`](ELO_AI_AGENT_WORKING_RULES.md) — protocolo detalhado de continuidade entre IAs.

Esses documentos orientam navegação, classificação, execução e revisão. Não substituem arquitetura normativa ou ADRs aprovados.

## Próximo estado

O ciclo de consolidação das variantes duplicadas atualmente identificadas foi concluído para as famílias auditadas. A partir deste ponto, qualquer nova duplicidade deve ser tratada pelo **Loop de Conclusão**, sem remoção automática e sem criação de novas variantes.

A próxima evolução arquitetural somente deve começar após a confirmação de que a árvore permanece coerente e que novos artefatos possuem owner canônico explícito.
