# ELO — Especificação do Ponto Primário de Modificação do Conhecimento

## Status
DRAFT — primeira implementação estrutural, sem alteração do runtime.

## Objetivo
Estabelecer um único ponto lógico de modificação/resolução para conhecimento do ELO antes da consolidação física das árvores PT/EN.

## Decisão primária
O **Índice Canônico de Conhecimento** será a autoridade de resolução de identidade e localização dos artefatos. Nenhum consumidor novo deve depender diretamente de um caminho físico histórico.

```text
CONCEITO
  ↓
artifact_id
  ↓
ÍNDICE CANÔNICO
  ↓
canonical_path
  ↓
ARTEFATO
  ↓
proveniência / versão / status
```

## Sequência obrigatória de mudança

### 1. Identidade
Criar/atribuir `artifact_id` estável para cada conhecimento consolidável.

### 2. Registro canônico
Registrar `artifact_id`, `concept_id`, `canonical_path`, `status`, `version`, `content_hash`, `authority` e `language`.

### 3. Aliases
Registrar todos os caminhos históricos como aliases, sem transformar o alias em autoridade.

### 4. Consumidores
Localizar referências físicas em agentes, Knowledge Engineering, RAG, Memory, Reasoning, Evidence, Governance, testes, CI, scripts e documentação.

### 5. Migração
Alterar consumidores para resolver por identidade lógica. Caminhos físicos ficam encapsulados no resolver/índice.

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
legacy_path[]
status
version
content_hash
authority
domain
language
provenance
```

## Regras de integridade

1. `artifact_id` não muda quando o arquivo muda de endereço.
2. Mudar caminho não cria novo conhecimento.
3. Mudar significado exige nova versão/decisão, não simples movimentação.
4. Proveniência histórica nunca é sobrescrita por um novo caminho.
5. Nenhum agente novo deve gravar caminho físico como identidade.
6. Um conceito não pode possuir dois proprietários canônicos simultaneamente.
7. Conflito semântico não pode ser resolvido por renomeação de pasta.

## Fora do escopo desta etapa

- alteração do Cognitive Core;
- alteração de contratos executáveis;
- alteração de schemas de runtime;
- migração física em massa das árvores;
- implementação de RAG de produção;
- implementação de Memory de produção.

## Critério de passagem
A etapa estará pronta para a consolidação física quando o índice de identidade, o mapeamento de aliases e os testes de resolução demonstrarem que um artefato pode mudar de caminho sem quebrar seus consumidores ou sua proveniência.
