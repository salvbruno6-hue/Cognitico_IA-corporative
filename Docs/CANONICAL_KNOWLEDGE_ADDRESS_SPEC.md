# ELO — Especificação do Ponto Primário de Modificação do Conhecimento

## Status
`STRUCTURAL CONTRACT — registry introduced, runtime unchanged`

## Objetivo
Estabelecer um único ponto lógico de modificação/resolução para conhecimento do ELO antes da consolidação física das árvores PT/EN.

## Decisão primária
O **Índice/Registro Canônico de Conhecimento** é a camada governada para identidade e localização dos artefatos desta fase. O registro materializado em `Docs/CANONICAL_KNOWLEDGE_REGISTRY.md` define o contrato e o inventário inicial.

Ele não substitui nem duplica a autoridade runtime do `SourceResolver` existente.

Nenhum consumidor novo deve depender diretamente de um caminho físico histórico como identidade primária.

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

## Sequência obrigatória de mudança

### 1. Identidade
Criar/atribuir `artifact_id` estável para cada conhecimento consolidável somente após inventário e análise do conteúdo.

### 2. Registro canônico
Registrar `artifact_id`, `concept_id`, `canonical_path`, `status`, `version`, `content_hash`, `authority` e `language`.

### 3. Aliases
Registrar todos os caminhos históricos como aliases, sem transformar o alias em autoridade.

### 4. Consumidores
Localizar referências físicas em agentes, Knowledge Engineering, RAG, Memory, Reasoning, Evidence, Governance, testes, CI, scripts e documentação.

### 5. Migração
Alterar consumidores para resolver por identidade lógica. Caminhos físicos ficam encapsulados no mecanismo autorizado de resolução/índice; esta etapa não altera o `SourceResolver` existente.

### 6. Conteúdo
Consolidar arquivos equivalentes, incorporar complementares e preservar conflitos/exclusivos/históricos.

### 7. Validação
Executar testes de resolução canônica, alias, conteúdo, proveniência, links, referências e CI.

### 8. Depreciação
Somente após validação, marcar caminhos antigos como `DEPRECATED`/`SUPERSEDED`.

### 9. Remoção
Remover somente quando não houver consumidores, conteúdo exclusivo ou dependência histórica não preservada.

## Modelo mínimo

```text
artifact_id
concept_id
canonical_path
legacy_paths[]
status
version
content_hash
authority
domain
language
provenance
references[]
migration_action
review_required
```

## Regras de integridade

1. `artifact_id` não muda quando o arquivo muda de endereço.
2. `concept_id` não deve ser recriado por simples mudança de endereço.
3. Mudar caminho não cria novo conhecimento.
4. Mudar significado exige nova versão/decisão, não simples movimentação.
5. Proveniência histórica nunca é sobrescrita por um novo caminho.
6. Nenhum agente novo deve gravar caminho físico como identidade.
7. Um conceito não pode possuir dois proprietários canônicos simultaneamente.
8. Conflito semântico não pode ser resolvido por renomeação de pasta.
9. Valores ainda não auditados devem permanecer `PENDING`, sem inferência nominal.

## Relação com o registro

O registro canônico é a fonte documental da identidade durante a auditoria. Nenhuma entrada deve ser considerada consolidada apenas porque aparece no registro; a classificação e a proveniência precisam de evidência correspondente.

## Fora do escopo desta etapa

- alteração do Cognitive Core;
- alteração de contratos executáveis;
- alteração de schemas de runtime;
- migração física em massa das árvores;
- implementação de RAG de produção;
- implementação de Memory de produção;
- substituição do `SourceResolver` existente.

## Critério de passagem
A etapa estará pronta para a consolidação física quando o registro de identidade, o mapeamento de aliases, o mapa de referências e os testes de resolução demonstrarem que um artefato pode mudar de caminho sem quebrar seus consumidores ou sua proveniência.
