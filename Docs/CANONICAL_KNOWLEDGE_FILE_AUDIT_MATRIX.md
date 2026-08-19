# ELO — Matriz de Auditoria Arquivo a Arquivo

## Objetivo
Executar a consolidação PT/EN por evidência, impedindo que nomes de diretório sejam tratados como prova de equivalência.

## Classificações

| Código | Classificação | Tratamento |
|---|---|---|
| EQ | EQUIVALENTE | um único artefato canônico; preservar aliases/proveniência |
| CP | COMPLEMENTAR | consolidar conteúdo em um único artefato; preservar origem |
| CF | CONFLITANTE | não mesclar automaticamente; abrir decisão/ADR |
| EX | EXCLUSIVO | preservar no proprietário canônico adequado |
| HI | HISTÓRICO | preservar como evidência/proveniência; não usar como autoridade atual |
| NR | NÃO RELACIONADO | manter separado |
| AR | AUDITORIA REQUERIDA | evidência insuficiente para decisão segura |

## Campos obrigatórios

```text
artifact_id
concept_id
family_id
source_path
canonical_path
classification
content_hash
language
semantic_purpose
authority_level
references_in
references_out
consumers
provenance
migration_action
risk
confidence
decision_status
```

## Confiança

- `HIGH`: propósito, conteúdo e referências verificados.
- `MEDIUM`: propósito claro, mas dependências ou conteúdo ainda requerem confirmação.
- `LOW`: apenas nome/localização/indícios.

Nenhum arquivo `LOW` pode ser apagado ou fundido automaticamente.

## Matriz inicial por família

| Família | Proprietário canônico | Fonte histórica | Estado | Ação |
|---|---|---|---|---|
| ELO.REPOSITORY.00 | `00-enterprise-manifest/` | `00-empresa-manifesto/` | AR | inventariar |
| ELO.ARCHITECTURE.01 | `01-meta-architecture/` | `01-meta-arquitetura/` | AR | comparar |
| ELO.COGNITIVE.05 | `05-cognitive-platform/` | `05-cognitivo-plataforma/` | AR | comparar |
| ELO.DATA.07 | `07-data-engineering/` | `07-engenharia-de dados/` | AR | comparar |
| ELO.MODELS.11 | `11-models-library/` | `11-modelos/` | AR | comparar |
| ELO.SYSTEMS.12 | `12-system-engineering/` | `12-sistemas/` | AR | comparar |
| ELO.REFERENCE.13 | `13-reference-architecture/` | `13-referências/` | AR | comparar |
| ELO.ROADMAP.14 | `14-roadmap/` | `14-roteiros/` | AR | comparar |
| ELO.ASSETS.15 | `15-assets/` | `15-ativos/` | AR | comparar |

## Gate

Não mover fisicamente um arquivo enquanto houver classificação `AR`/`CF`/`LOW`, consumidor desconhecido, referência quebrada, proveniência ausente, identidade instável ou gates sem evidência de aprovação.

## Sequência

1. inventário;
2. conteúdo/hash;
3. classificação;
4. dependências;
5. identidade;
6. consolidação lógica;
7. referências;
8. testes;
9. depreciação;
10. remoção após gate.

O `src/elo/core/source_resolver.py` existente permanece como fronteira de resolução autorizada; esta consolidação não cria um segundo resolver.
