# ELO — Crosswalk de Reconciliação dos Registros Canônicos — 2026-08-19

## Objetivo

Consolidar a relação entre os registros de governança já existentes antes de criar novos mecanismos de autoridade. Este documento não substitui nenhum registry, ADR ou mapa canônico; ele demonstra como os artefatos existentes se relacionam durante o PR #267.

## Princípio desta fase — evolução estrutural do ELO

A palavra **evolução**, neste PR, significa evolução da estrutura que sustenta o ELO, não mudança da identidade, missão ou conceito do ELO.

O objetivo é tornar o repositório mais:

- coerente;
- conectado;
- fluido;
- rastreável;
- livre de autoridades concorrentes;
- livre de duplicidades semânticas não tratadas;
- capaz de crescer sem perder a arquitetura e o conhecimento histórico.

A analogia operacional é de um sistema nervoso arquitetural:

```text
conceitos
   ↓
artefatos
   ↓
referências
   ↓
contratos
   ↓
implementação
   ↓
testes / evidência
```

Cada família documental é uma região conectada desse sistema. Um arquivo não deve ser avaliado somente pelo nome ou pelo diretório; deve ser entendido pela função que exerce, pelas informações que recebe, pelas relações que fornece e pelos consumidores que possui.

### Fora do escopo desta fase

- reinventar o ELO;
- alterar sua missão;
- substituir conceitos existentes sem decisão explícita;
- criar uma arquitetura paralela;
- criar uma segunda autoridade documental ou runtime;
- remover conhecimento histórico sem preservação e gates;
- transformar a auditoria estrutural em desenvolvimento de novas capacidades;
- preencher artificialmente famílias estruturais vazias apenas para produzir simetria visual.

## 1. Hierarquia de autoridade encontrada

```text
Baseline / Constituição
        ↓
ADR aprovado
        ↓
Canonical Structure Map
        ↓
Canonical Knowledge Migration Registry
        ↓
Audit Matrix / Address Specification / Impact Map
        ↓
Reference Evidence
        ↓
CI / Tests / Verification
```

A ordem acima é operacional para esta auditoria. O diretório físico não é autoridade isoladamente.

## 2. Registros existentes e função

| Artefato | Função | Autoridade nesta fase | Não deve fazer |
|---|---|---|---|
| `10-adr/ADR-2026-08-19-BILINGUAL-TREE-CONSOLIDATION.md` | decisão de consolidação PT/EN | ADR aprovado | autorizar remoção automática |
| `10-adr/ADR-0011-reconcile-historical-elo-runtime.md` | reconciliação do runtime histórico | ADR proposto | promover código histórico |
| `02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md` | proprietário semântico por árvore | mapa estrutural | provar que conteúdo já foi migrado |
| `Docs/CANONICAL_KNOWLEDGE_MIGRATION_REGISTRY.json` | identidade, caminho, proveniência e estado da migração | registry documental único | substituir `SourceResolver` |
| `Docs/CANONICAL_KNOWLEDGE_ARTIFACT_ID_REGISTRY_2026-08-19.json` | identidade estável dos artefatos já canonicalizados | registry de identidade | autorizar remoção física |
| `Docs/CANONICAL_KNOWLEDGE_AUDIT_MATRIX.md` | classificação arquivo-a-arquivo e gates de segurança | matriz de auditoria | presumir equivalência por nome |
| `Docs/CANONICAL_KNOWLEDGE_ADDRESS_SPEC.md` | contrato entre identidade e endereço | especificação | alterar runtime |
| `Docs/CANONICAL_KNOWLEDGE_REFERENCE_IMPACT.md` | impacto de mudança de caminho | matriz de impacto | declarar consumidor sem evidência |
| `Docs/CANONICAL_KNOWLEDGE_FAMILY_00_REFERENCE_MAP_2026-08-19.md` | descoberta de referências da família 00 | mapa de descoberta | ser prova operacional sozinho |
| `Docs/CANONICAL_KNOWLEDGE_FAMILY_00_CONTEXTUAL_EVIDENCE_2026-08-19.md` | relações contextuais confirmadas | evidência auditada | autorizar migração física |
| `Docs/CANONICAL_KNOWLEDGE_FAMILY_01_ARTIFACT_EVIDENCE_2026-08-19.md` | evidência por artefato da família 01 | evidência auditada | autorizar remoção sem consumidores validados |
| `tests/test_canonical_knowledge_governance.py` | invariantes automatizadas | verificação | substituir evidência CI |
| `ELO_REPOSITORY_NAVIGATION_RULES.md` | regras de navegação e autoridade | governança estrutural | ser SourceResolver |
| `ELO_CAPABILITY_REGISTRY.yaml` | catálogo de capacidades | registro de capacidades | provar consolidação física |

## 3. Regra de não duplicação

O PR não deve criar um segundo:

- registry documental;
- SourceResolver;
- Core runtime;
- mapa estrutural concorrente;
- autoridade normativa paralela.

Novos documentos somente são válidos quando forem **evidência específica, extensão controlada ou material de verificação** de um contrato existente.

## 4. Reconciliando a família 00

O `ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md` define:

```text
00-enterprise-manifest/  → canonical
00-empresa-manifesto/    → migration source; no new artifacts
```

O `CANONICAL_KNOWLEDGE_MIGRATION_REGISTRY.json` mantém a família `ELO.REPOSITORY.00` como `AUDIT_REQUIRED`, com identidade, referências e proveniência pendentes.

O `ELO_CAPABILITY_REGISTRY.yaml` aponta `00-enterprise-manifest/` como `canonical_artifact`, mas sua evidência permanece vazia.

Portanto, os registros não estão em conflito:

```text
canonical owner declarado
        ≠
conteúdo completamente reconciliado
        ≠
migração física concluída
```

## 5. Artefatos já com canonicalização estrutural comprovada

O `CANONICAL_KNOWLEDGE_ARTIFACT_ID_REGISTRY_2026-08-19.json` já registra cinco artefatos com identidade estável e cópia no endereço canônico: `01`, `07`, `11`, `12` e `14`. O registro estabelece ainda que identidade é estável, caminhos legados são aliases, deleção física exige gate e merge semântico automático é proibido.

### 01 — Architecture Master

`01-meta-architecture/ELO_ARCHITECTURE_MASTER.md` possui `Artifact ID ELO.ARCH.01.MASTER`, `Concept ID ELO.ARCHITECTURE.MASTER`, identifica o caminho histórico e declara autoridade `ARCHITECTURE`. O conteúdo-base corresponde ao arquivo histórico; o canônico adiciona o contrato de canonicalização e rastreabilidade.

**Estado:** `CANONICALIZED / CONSUMER_MAPPING_PENDING`.

### 07 — Data Engineering Master

O canônico e o histórico possuem o mesmo propósito, tópicos centrais e relação com a plataforma. O canônico adiciona metadados de identidade e o contrato de endereço/alias.

**Estado:** `CANONICALIZED / CONSUMER_MAPPING_PENDING`.

### 11 — Models Library Master

O canônico e o histórico possuem o mesmo conteúdo funcional de propósito, tópicos e relação com a plataforma. O canônico acrescenta identidade, autoridade e contrato de canonicalização.

**Estado:** `CANONICALIZED / CONSUMER_MAPPING_PENDING`.

### 12 — Systems Engineering Master

O canônico e o histórico possuem o mesmo núcleo funcional: backend, portal, integrações, dashboards, runtime e limites sistêmicos. O canônico acrescenta identidade e contrato de proveniência.

**Estado:** `CANONICALIZED / CONSUMER_MAPPING_PENDING`.

### 14 — Roadmap Master

O canônico preserva propósito, fases e uso do histórico, acrescentando identidade e contrato de canonicalização.

**Estado:** `CANONICALIZED / CONSUMER_MAPPING_PENDING`.

### Regra extraída

Esses casos demonstram que a consolidação estrutural pode estar avançada sem que a remoção do caminho histórico esteja autorizada:

```text
conteúdo preservado
      ↓
identidade estável
      ↓
caminho canônico
      ↓
proveniência legada
      ↓
consumidores ainda auditados
      ↓
remoção somente após gate
```

## 6. Reconciliação das famílias 01, 05, 07, 11 e 12

O mapa estrutural define `01-meta-architecture`, `05-cognitive-platform`, `07-data-engineering`, `11-models-library` e `12-system-engineering` como proprietários canônicos, enquanto as árvores portuguesas correspondentes são fontes históricas que exigem revisão conforme o caso.

A família 01 já possui pelo menos um artefato canonicalizado com evidência contextual. As famílias 07, 11 e 12 também possuem artefatos master já registrados como cópias canônicas no registry de identidade. Portanto, elas não devem voltar ao estado genérico de `PENDING` por inteiro.

A unidade correta de auditoria é o **artefato**, não somente a família.

A família 05 merece tratamento diferente: `05-cognitive-platform/` já contém estrutura operacional efetiva, incluindo engine cognitivo, decision engine, memory/reasoning, especialistas e contratos Multiteiner, e não deve ser tratada como simples cópia da árvore portuguesa. O diretório canônico contém arquivos efetivos, e a árvore deve ser reconciliada por função e conexão, não por espelhamento.

### 6.1 — Famílias 13 e 15: estruturas vazias não são lacunas a preencher automaticamente

A inspeção do HEAD atual mostra que `13-reference-architecture/` contém somente `.gitkeep` e `15-assets/` contém somente `.gitkeep`.

Isso significa **estrutura presente, conteúdo canônico ainda não materializado nesse endereço**. Não significa, por si só, que o ELO esteja sem conhecimento correspondente em outros locais.

A decisão estrutural desta fase é:

```text
família vazia
      ↓
NÃO preencher por simetria
      ↓
NÃO criar conteúdo novo
      ↓
procurar conhecimento existente / owner / referências
      ↓
se houver conteúdo → reconciliar por conceito
se não houver conteúdo → manter scaffold
```

Portanto:

- `13-reference-architecture/` = `SCAFFOLD_ONLY / DISCOVERY_REQUIRED`;
- `15-assets/` = `SCAFFOLD_ONLY / DISCOVERY_REQUIRED`.

O `.gitkeep` é evidência de estrutura física, não evidência de conteúdo conceitual.

## 7. Reconciliação com o runtime histórico

`ADR-0011` estabelece que `ELO/` é material de referência/proveniência e que `src/elo/` é o runtime executável atual. O registro de PR1 classifica arquivos históricos individualmente e exige comparação de contrato, testes e evidência antes de qualquer promoção.

Consequência para este PR:

```text
árvore documental histórica
        ↓
não cria runtime
        ↓
SourceResolver continua autoridade runtime
```

## 8. Modelo de conexão — “sistema nervoso” estrutural

As famílias não são projetos isolados. São regiões conectadas do mesmo ELO:

```text
00 Enterprise Constitution
          │
          ▼
01 Meta Architecture ───────────────┐
          │                          │
          ├──► 02 Architecture      │
          │                          │
          ├──► 05 Cognitive Platform │
          │                          │
          ├──► 07 Data Engineering   │
          │                          │
          ├──► 11 Models              │
          │                          │
          ├──► 12 System Engineering  │
          │                          │
          ├──► 13 Reference Architecture
          │                          │
          └──► 14 Roadmap            │
                                     │
05/07/11/12 ──► src/elo/ ◄──────────┘
                   │
                   ▼
                tests/
```

O diagrama é uma **hipótese estrutural de conexão para auditoria**, não uma afirmação de dependência runtime. Cada seta deve ser convertida em evidência de referência/consumidor antes de ser tratada como dependência operacional.

## 9. Estado de evidência

| Domínio | Estado |
|---|---|
| Autoridade estrutural | CONFIRMED |
| Registry documental único | CONFIRMED |
| Identidade independente do path | CONFIRMED |
| Família 00 — contexto | PARTIAL/CONFIRMED |
| 01 Architecture Master | CANONICALIZED |
| 07 Data Engineering Master | CANONICALIZED |
| 11 Models Library Master | CANONICALIZED |
| 12 Systems Engineering Master | CANONICALIZED |
| 14 Roadmap Master | CANONICALIZED |
| Família 05 — estrutura operacional | CONFIRMED / CONTENT_RECONCILIATION_REQUIRED |
| Família 13 — scaffold only | DISCOVERY_REQUIRED |
| Família 15 — scaffold only | DISCOVERY_REQUIRED |
| Consumidores físicos completos | PENDING |
| T01–T10 executados no HEAD | PENDING |
| CI do HEAD atual | NO_EVIDENCE |
| Migração física | BLOCKED |
| Remoção histórica | BLOCKED |

## 10. Regra para próxima fase

Antes de adicionar novos registros de governança:

1. consultar os artefatos existentes;
2. verificar se o conceito já possui owner;
3. reutilizar o registry existente quando o dado for de identidade/migração;
4. usar a matriz quando o dado for classificação;
5. usar o mapa de impacto quando o dado for dependência;
6. usar evidência contextual quando a relação tiver sido comprovada;
7. avaliar o artefato dentro do fluxo estrutural do ELO;
8. não preencher famílias vazias sem evidência de conteúdo existente;
9. somente criar novo documento se houver uma função não coberta.

## 11. Decisão

`RECONCILIATION = ESTABLISHED`

O PR possui uma cadeia de governança coerente e não deve criar uma segunda autoridade documental. A evolução desta fase é exclusivamente estrutural: melhorar a forma como o conhecimento existente é organizado, identificado e conectado, preservando o contexto do ELO.

As pendências restantes são de evidência, conexão e execução, não de criação de uma nova arquitetura conceitual.

## 12. Gate

```text
RECONCILIATION       = PASS
STRUCTURAL_SAFETY    = PASS
STRUCTURAL_EVOLUTION = ALIGNED_WITH_ELO
MIGRATION_APPROVAL   = BLOCKED
PHYSICAL_REMOVAL     = BLOCKED
CI_HEAD              = NO_EVIDENCE
```
