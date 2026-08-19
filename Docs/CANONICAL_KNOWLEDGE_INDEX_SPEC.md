# ELO — Especificação do Índice Canônico de Conhecimento

## Status
DRAFT — base para implementação incremental.

## Autoridade
Este índice é a camada lógica de resolução entre identidade de conhecimento e localização física. Ele não substitui o Cognitive Core, SourceResolver, Knowledge Engineering ou os contratos existentes; integra-se a eles.

## Registro lógico

| Campo | Obrigatório | Função |
|---|---:|---|
| `artifact_id` | sim | identidade estável do artefato |
| `concept_id` | sim | identidade semântica do conceito |
| `canonical_path` | sim | localização operacional atual |
| `legacy_paths` | não | endereços históricos/aliases |
| `status` | sim | CANONICAL, DEPRECATED, SUPERSEDED, HISTORICAL |
| `version` | sim | versão semântica/documental |
| `content_hash` | recomendado | prova de conteúdo |
| `authority` | sim | proprietário semântico |
| `domain` | sim | domínio do conhecimento |
| `language` | sim | idioma do artefato |
| `provenance` | sim | origem e cadeia de custódia |

## Regras

1. `artifact_id` permanece estável durante mudança de caminho.
2. Um `concept_id` possui um único proprietário canônico ativo.
3. `legacy_paths` nunca possuem autoridade própria.
4. O índice não cria conteúdo; apenas resolve identidade, localização e estado.
5. Conflitos semânticos bloqueiam consolidação automática.
6. Um arquivo histórico pode permanecer acessível sem ser canônico.
7. O índice deve permitir auditoria da transição PT/EN.

## Resolução

```text
artifact_id / concept_id / legacy_path
              ↓
       canonical index
              ↓
        current record
              ↓
          artifact
              ↓
    evidence + provenance
```

## Integração com o SourceResolver existente
O `src/elo/core/source_resolver.py` continua responsável pela resolução autorizada de fontes externas e pela entrada em memória temporal. O Índice Canônico não deve criar um segundo SourceResolver. Quando a origem consultada for conhecimento interno, o fluxo deverá futuramente resolver a identidade canônica antes da leitura física.

## Integração futura com RAG/Memory
Chunks, memórias e evidências devem referenciar `artifact_id`/`concept_id` sempre que a origem for um artefato canônico. O `canonical_path` é metadado de localização, não chave de identidade.

## Integração com agentes
Agentes devem solicitar conhecimento por identidade semântica quando possível. Caminhos físicos podem ser usados apenas pelo mecanismo de resolução.

## Critério de aceite
A implementação estará apta a avançar quando for possível mover um documento de um caminho PT para um caminho EN sem alterar a referência lógica, a proveniência ou o resultado de resolução autorizado.