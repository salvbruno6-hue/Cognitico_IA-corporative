# ELO — Crosswalk de Reconciliação dos Registros Canônicos — 2026-08-19

## Objetivo

Consolidar a relação entre os registros de governança já existentes antes de criar novos mecanismos de autoridade. Este documento não substitui nenhum registry, ADR ou mapa canônico; ele demonstra como os artefatos existentes se relacionam durante o PR #267.

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
| `Docs/CANONICAL_KNOWLEDGE_AUDIT_MATRIX.md` | classificação arquivo-a-arquivo e gates de segurança | matriz de auditoria | presumir equivalência por nome |
| `Docs/CANONICAL_KNOWLEDGE_ADDRESS_SPEC.md` | contrato entre identidade e endereço | especificação | alterar runtime |
| `Docs/CANONICAL_KNOWLEDGE_REFERENCE_IMPACT.md` | impacto de mudança de caminho | matriz de impacto | declarar consumidor sem evidência |
| `Docs/CANONICAL_KNOWLEDGE_FAMILY_00_REFERENCE_MAP_2026-08-19.md` | descoberta de referências da família 00 | mapa de descoberta | ser prova operacional sozinho |
| `Docs/CANONICAL_KNOWLEDGE_FAMILY_00_CONTEXTUAL_EVIDENCE_2026-08-19.md` | relações contextuais confirmadas | evidência auditada | autorizar migração física |
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

O `ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md` já define:

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

## 5. Reconciliação das famílias 01, 05, 07, 11 e 12

O ADR de consolidação registra evidência inicial de que as árvores portuguesas contêm material substantivo enquanto as árvores inglesas podem ser scaffolding ou possuir conteúdo de natureza diferente.

Exemplos explicitamente registrados no ADR:

- `01-meta-arquitetura/` contém material de inteligência de demanda, domínios, glossário, modelo conceitual, entidades, relacionamentos, regras de negócio e arquitetura mestre; `01-meta-architecture/` não é tratado como equivalente automático.
- `05-cognitivo-plataforma/` contém fundamentos, filosofia, recursos estratégicos, inteligência de demanda, modelo de conhecimento e RAG; `05-cognitive-platform/` contém estrutura operacional mais recente, incluindo engine cognitivo, decision engine, memory/reasoning, especialistas e contratos Multiteiner.
- `07-engenharia-de dados/` contém modelo lógico, dicionário, SQLite, APIs, eventos e master de engenharia de dados; `07-data-engineering/` possui scaffolding/README/AGENTS.
- `11-modelos/` contém `MODELS_LIBRARY_MASTER.md`; `11-models-library/` possui `.gitkeep`.
- `12-sistemas/` contém `SYSTEMS_ENGINEERING_MASTER.md`; `12-system-engineering/` possui `.gitkeep`.

Esses casos devem permanecer `AUDIT_REQUIRED`/`CONTENT_REVIEW_REQUIRED` até comparação arquivo-a-arquivo. A assimetria de volume não autoriza cópia automática.

## 6. Reconciliação com o runtime histórico

`ADR-0011` estabelece que `ELO/` é material de referência/proveniência e que `src/elo/` é o runtime executável atual. O registro de PR1 classifica arquivos históricos individualmente e exige comparação de contrato, testes e evidência antes de qualquer promoção.

Consequência para este PR:

```text
árvore documental histórica
        ↓
não cria runtime
        ↓
SourceResolver continua autoridade runtime
```

## 7. Estado de evidência

| Domínio | Estado |
|---|---|
| Autoridade estrutural | CONFIRMED |
| Registry documental único | CONFIRMED |
| Identidade independente do path | CONFIRMED |
| Família 00 — contexto | PARTIAL/CONFIRMED |
| Famílias 01/05/07/11/12 — decisão arquivo-a-arquivo | PENDING |
| Famílias 13/14/15 — decisão arquivo-a-arquivo | PENDING |
| Consumidores físicos completos | PENDING |
| T01–T10 executados no HEAD | PENDING |
| CI do HEAD atual | NO_EVIDENCE |
| Migração física | BLOCKED |
| Remoção histórica | BLOCKED |

## 8. Regra para próxima fase

Antes de adicionar novos registros de governança:

1. consultar os artefatos acima;
2. verificar se o conceito já possui owner;
3. reutilizar o registry existente quando o dado for de identidade/migração;
4. usar a matriz quando o dado for classificação;
5. usar o mapa de impacto quando o dado for dependência;
6. usar evidência contextual quando a relação tiver sido comprovada;
7. somente criar novo documento se houver uma função não coberta.

## 9. Decisão

`RECONCILIATION = ESTABLISHED`

O PR possui uma cadeia de governança coerente e não deve criar uma segunda autoridade documental. As pendências restantes são de evidência e execução, não de criação de mais camadas conceituais.

## 10. Gate

```text
RECONCILIATION       = PASS
STRUCTURAL_SAFETY    = PASS
MIGRATION_APPROVAL   = BLOCKED
PHYSICAL_REMOVAL     = BLOCKED
CI_HEAD               = NO_EVIDENCE
```
