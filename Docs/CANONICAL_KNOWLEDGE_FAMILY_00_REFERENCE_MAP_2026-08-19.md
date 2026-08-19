# ELO — Mapa de Referências da Família 00 — Enterprise Manifest

## Estado
`REFERENCE_AUDIT — EVIDENCE_REQUIRED`

## Finalidade
Registrar, de forma separada da auditoria semântica, os possíveis pontos de referência, consumo ou autoridade relacionados à família `ELO.REPOSITORY.00`.

Este documento **não transforma uma ocorrência de busca em dependência confirmada**. Cada item precisa de validação no conteúdo do arquivo consumidor antes de alterar `references`, `consumers`, `artifact_id`, `concept_id` ou `canonical_path`.

## Regra de evidência

```text
ocorrência encontrada
      ↓
referência candidata
      ↓
inspeção do contexto
      ↓
referência confirmada / não confirmada
      ↓
impacto classificado
```

Uma busca nominal por `enterprise`, `mission`, `traceability` ou nome de arquivo é apenas **evidência de descoberta**.

## Candidatos transversais identificados

| Candidato | Papel potencial | Evidência atual | Estado | Próxima verificação |
|---|---|---|---|---|
| `ELO_CAPABILITY_REGISTRY.yaml` | registry de capacidades / autoridade declarativa | registra `ELO-CAP-ENT-001` e aponta `00-enterprise-manifest/` como `canonical_artifact` proposto | `CANDIDATE_CONFIRMED_AS_REGISTRY`, dependência de conteúdo `PENDING` | verificar se entradas de capacidade dependem de conteúdo/caminho específico da família 00 |
| `01-meta-architecture/ELO_ARCHITECTURE_MASTER.md` | fonte arquitetural potencial | localizado por busca transversal relacionada a Enterprise Manifest | `REFERENCE_CANDIDATE` | inspecionar links, termos e autoridade efetiva |
| `docs/migration/migration_plan.md` | processo de migração | localizado na estrutura de migração | `REFERENCE_CANDIDATE` | localizar referências aos roots `00-*` |
| `docs/migration/migration_inventory.md` | inventário de migração | localizado na estrutura de migração | `REFERENCE_CANDIDATE` | verificar se registra arquivos/caminhos da família 00 |
| `docs/migration/architecture_mapping.md` | mapeamento arquitetural | localizado na estrutura de migração | `REFERENCE_CANDIDATE` | verificar correspondências de conceitos e paths |
| `ELO_REPOSITORY_NAVIGATION_RULES.md` | navegação/descoberta | localizado na busca transversal | `REFERENCE_CANDIDATE` | verificar se há regras ou paths específicos para a família 00 |
| `docs/handbook/ELO_ENTERPRISE_HANDBOOK_v2.0_ENTERPRISE.md` | handbook empresarial | localizado por busca `enterprise` | `REFERENCE_CANDIDATE` | determinar se reproduz ou consome conceitos do manifesto |
| `src/elo/integrations/enterprise/README.md` | integração/runtime potencial | localizado por busca `enterprise` | `CONSUMER_CANDIDATE` | verificar se lê arquivos da família 00 ou somente descreve integração |
| `src/elo/integrations/enterprise/events/README.md` | integração/runtime potencial | localizado por busca `enterprise` | `CONSUMER_CANDIDATE` | inspecionar dependências efetivas |
| `src/elo/integrations/enterprise/adapters/README.md` | integração/runtime potencial | localizado por busca `enterprise` | `CONSUMER_CANDIDATE` | inspecionar dependências efetivas |
| `src/elo/integrations/enterprise/contracts/README.md` | contratos/integralização potencial | localizado por busca `enterprise` | `CONSUMER_CANDIDATE` | verificar se contrato referencia conhecimento da família 00 |
| `ELO_TRACEABILITY_RECORD_TEMPLATE.yaml` | modelo de rastreabilidade | localizado por busca transversal | `GOVERNANCE_CANDIDATE` | verificar campos de identidade/proveniência que devem ser reutilizados |
| `ELO_BASELINE_MATURITY_AND_TRACEABILITY_FRAMEWORK.md` | governança/rastreabilidade | localizado por busca transversal | `GOVERNANCE_CANDIDATE` | verificar relação com identidade e evidência da família 00 |
| `ADR-0010-maturity-and-traceability-framework.md` | decisão arquitetural | localizado por busca transversal | `GOVERNANCE_CANDIDATE` | verificar se define autoridade ou rastreabilidade aplicável |

## O que ainda não está comprovado

Ainda não existe evidência suficiente para afirmar que qualquer candidato acima:

- lê diretamente `00-empresa-manifesto/`;
- lê diretamente `00-enterprise-manifest/`;
- depende de um nome de arquivo específico;
- depende de um caminho físico histórico;
- trata `ENTERPRISE_MANIFESTO.md` como autoridade normativa;
- trata `README.md` como autoridade normativa;
- deve receber um `legacy_path`;
- deve ser alterado nesta fase.

## Família 00 — referências internas conhecidas

| Origem | Relação candidata | Estado |
|---|---|---|
| `00-empresa-manifesto/01_Missao.md` | relaciona missão aos demais documentos do manifesto | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/MISSAO.md` | relaciona missão ao propósito, valor, planejamento/operação e ecossistema | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/02_Objetivos.md` | relaciona objetivos à missão/capacidades/recursos | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/03_Capacidades.md` | relaciona capacidades à missão/objetivos e recursos | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/04_Cadeia_de_Valor.md` | relaciona informação, conhecimento, decisão, planejamento e operação | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/05_Modelo_Operacional.md` | relaciona capacidade, recursos, processos, governança e execução | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/06_Stakeholders.md` | relaciona participantes, governança e evolução | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/07_Regras_Estrategicas.md` | explicita a cadeia missão → objetivos → capacidades → recursos → cadeia de valor → operação → stakeholders | `SEMANTIC_RELATION_CONFIRMED` |
| `00-empresa-manifesto/ENTERPRISE_MANIFESTO.md` | agrega os conceitos anteriores | `SEMANTIC_RELATION_CONFIRMED` |

Essas relações são **relações conceituais internas**, não necessariamente dependências físicas.

## Tipos de dependência a distinguir

### `DOC_REFERENCE`
Documento aponta para outro documento.

### `PATH_REFERENCE`
Documento/configuração contém caminho físico.

### `LOGICAL_REFERENCE`
Consumidor utiliza identidade lógica, conceito ou chave de registry.

### `RUNTIME_CONSUMER`
Código efetivamente lê/resolver conteúdo.

### `GOVERNANCE_REFERENCE`
Registro, ADR ou política utiliza o conceito para governança.

### `HISTORICAL_REFERENCE`
Documento preserva proveniência ou histórico.

### `SEARCH_DISCOVERY_ONLY`
A ocorrência foi encontrada por busca, mas não há evidência suficiente de dependência.

## Critério para promover um candidato

Um candidato somente pode sair de `CANDIDATE` quando houver evidência contextual contendo pelo menos:

1. arquivo de origem;
2. linha/seção ou trecho identificável;
3. objeto referenciado;
4. tipo de relação;
5. impacto de mudança de endereço;
6. ação necessária;
7. evidência de teste, quando executável.

## Regra de segurança

```text
SEARCH RESULT
    ≠
CONFIRMED CONSUMER

CONFIRMED CONSUMER
    ≠
MIGRATION APPROVAL
```

Nenhum candidato deste mapa autoriza movimentação física.

## Relação com identidade

A existência de uma referência não cria automaticamente um novo `artifact_id` ou `concept_id`.

A sequência permanece:

```text
conteúdo
  ↓
conceito
  ↓
artefato
  ↓
identidade
  ↓
referências
  ↓
consumidores
  ↓
localização
```

## Próximo levantamento

A próxima inspeção deve priorizar, nesta ordem:

1. referências físicas aos roots `00-enterprise-manifest/` e `00-empresa-manifesto/`;
2. referências diretas aos nove arquivos auditados;
3. uso de `ELO-CAP-ENT-001`;
4. `ELO_REPOSITORY_NAVIGATION_RULES.md`;
5. `docs/migration/*`;
6. `src/elo/integrations/enterprise/*`;
7. rastreabilidade/ADR;
8. workflows e testes.

## Gate de conclusão

A família 00 não pode receber `REFERENCE_MAPPED = PASS` enquanto existirem candidatos críticos sem inspeção contextual.

Estado atual:

```text
REFERENCE_DISCOVERY = IN_PROGRESS
REFERENCE_MAPPING   = PENDING
CONSUMER_MAPPING    = PENDING
MIGRATION_APPROVAL  = BLOCKED
PHYSICAL_REMOVAL    = BLOCKED
```
