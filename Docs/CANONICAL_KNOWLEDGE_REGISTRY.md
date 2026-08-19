# ELO — Registro Canônico de Identidade do Conhecimento

## Status
`STRUCTURAL REGISTRY — AUDIT REQUIRED`

## Finalidade

Materializar a identidade lógica do conhecimento sem realizar ainda a consolidação física das árvores PT/EN.

Este registro é a camada intermediária entre a governança documental e uma futura implementação de resolução por identidade. Ele não substitui o `SourceResolver` existente e não altera o `src/elo/` nesta fase.

## Princípio central

```text
artifact_id  != caminho físico
concept_id   != caminho físico
canonical_path = localização atual autorizada
legacy_paths[] = localizações históricas compatíveis
```

A mudança de endereço não cria um novo artefato. A mudança de significado não pode ser representada apenas como mudança de endereço.

## Contrato mínimo do registro

Cada entrada materializada deverá possuir:

| Campo | Obrigatório | Regra |
|---|---|---|
| `artifact_id` | sim | identidade estável do artefato; não depende do caminho |
| `concept_id` | quando aplicável | identidade semântica compartilhada por versões/artefatos do mesmo conceito |
| `canonical_path` | sim quando definido | único endereço físico autorizado na fase correspondente |
| `legacy_paths[]` | quando houver | caminhos históricos preservados como aliases, nunca como autoridade |
| `status` | sim | estado de auditoria/migração |
| `classification` | sim após auditoria | `EQ`, `CP`, `CF`, `EX`, `HI` ou `NR` |
| `content_hash` | sim após inventário | hash do conteúdo avaliado |
| `language` | sim | idioma do artefato avaliado |
| `authority` | sim após decisão | autoridade semântica/operacional atribuída |
| `provenance` | sim | origem e rastreabilidade histórica |
| `references[]` | sim após levantamento | consumidores e referências conhecidas |
| `migration_action` | sim após classificação | ação aprovada para o artefato |
| `review_required` | sim | indica necessidade de decisão humana/arquitetural |

## Estados permitidos

```text
DISCOVERED
AUDIT_REQUIRED
CLASSIFIED
IDENTITY_ASSIGNED
REFERENCE_MAPPED
MIGRATION_APPROVED
MIGRATED
DEPRECATED
REMOVAL_ELIGIBLE
REMOVED
BLOCKED
```

`REMOVAL_ELIGIBLE` somente pode ocorrer depois de todos os gates de identidade, autoridade, localização, proveniência, consumidores, integridade e testes.

## Regra para registros ainda não auditados

Não atribuir `artifact_id`, `concept_id`, `EQ`, `CP`, `CF`, `EX`, `HI` ou `NR` por inferência nominal antes da comparação do conteúdo.

Quando a auditoria ainda não ocorreu, usar:

```text
status = AUDIT_REQUIRED
classification = PENDING
review_required = true
```

## Inventário estrutural inicial

| Família | Caminho canônico | Caminho histórico | Status | Classificação | Identidade |
|---|---|---|---|---|---|
| 00 | `00-enterprise-manifest/` | `00-empresa-manifesto/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 01 | `01-meta-architecture/` | `01-meta-arquitetura/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 05 | `05-cognitive-platform/` | `05-cognitivo-plataforma/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 07 | `07-data-engineering/` | `07-engenharia-de dados/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 11 | `11-models-library/` | `11-modelos/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 12 | `12-system-engineering/` | `12-sistemas/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 13 | `13-reference-architecture/` | `13-referências/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 14 | `14-roadmap/` | `14-roteiros/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |
| 15 | `15-assets/` | `15-ativos/` | `AUDIT_REQUIRED` | `PENDING` | `PENDING` |

Esta tabela é um inventário estrutural, não uma declaração de equivalência.

## Registro individual — formato normativo

Quando uma família for auditada, o registro deverá seguir este formato:

```yaml
artifact_id: PENDING
concept_id: PENDING
canonical_path: PENDING
legacy_paths: []
status: AUDIT_REQUIRED
classification: PENDING
content_hash: PENDING
language: PENDING
authority: PENDING
provenance:
  source_path: PENDING
  source_revision: PENDING
  source_date: PENDING
references: []
migration_action: PENDING
review_required: true
```

Nenhum valor `PENDING` deve ser substituído por suposição.

## Relação com o ponto primário de modificação

O fluxo lógico permanece:

```text
CONCEITO
  ↓
artifact_id / concept_id
  ↓
REGISTRO CANÔNICO
  ↓
canonical_path + legacy_paths[]
  ↓
ARTEFATO
  ↓
proveniência / versão / status
```

O registro define identidade e localização governadas; ele não cria uma segunda autoridade runtime.

## Relação com consumidores

A partir deste registro, cada referência encontrada deverá ser associada ao `artifact_id` antes da migração física. Consumidores não devem receber um novo caminho como substituição cega de outro caminho.

Ordem:

```text
localizar referência
→ identificar artefato
→ registrar consumidor
→ decidir destino canônico
→ atualizar consumidor
→ testar resolução
→ somente então deprecar caminho histórico
```

## Relação com os gates

| Gate | Evidência esperada no registro |
|---|---|
| Identidade | `artifact_id` / `concept_id` definidos |
| Autoridade | proprietário canônico e conflitos registrados |
| Localização | `canonical_path` + `legacy_paths[]` |
| Proveniência | origem, revisão/hash e rastreabilidade |
| Consumidores | `references[]` e dependências classificadas |
| Integridade | ausência de referências órfãs |
| Testes | resolução por identidade e aliases validada |
| Depreciação | estado e janela de compatibilidade definidos |
| Remoção | somente após evidência de ausência de dependência |

## Limites desta fase

- não remover árvores históricas;
- não alterar `src/elo/`;
- não substituir o `SourceResolver`;
- não criar um segundo Core;
- não declarar equivalência sem auditoria semântica;
- não gerar IDs definitivos artificialmente;
- não tratar este registro como prova de que a consolidação física já ocorreu.

## Critério de evolução

A família somente poderá avançar de `AUDIT_REQUIRED` quando houver evidência suficiente para preencher identidade, conteúdo, classificação, proveniência e referências. O avanço para migração depende dos gates correspondentes e de CI verde.
