# 01 — Meta-Arquitetura

Esta é a **família canônica de meta-arquitetura do ELO**.

## Função

Organiza a visão arquitetural de alto nível e seus elementos de domínio: mapa de domínios, glossário, modelo conceitual, entidades, relacionamentos, regras de negócio, framework de arquitetura de domínio e o master arquitetural.

## Ordem lógica

```text
ELO_ARCHITECTURE_MASTER
        ↓
DOMAIN_ARCHITECTURE_FRAMEWORK
        ↓
01_Mapa_Dominios
        ↓
01_Inteligencia_de_Demanda
        ↓
02_Glossario
        ↓
03_Modelo_Conceitual
        ↓
04_Entidades
        ↓
05_Relacionamentos
        ↓
06_Regras_Negocio
```

A ordem representa dependência conceitual, não necessariamente ordem de leitura.

## Regra de ownership

`01-meta-architecture/` é o único owner canônico da família `ELO.ARCHITECTURE.01`.

A antiga raiz `01-meta-arquitetura/` foi tratada como origem histórica. Conteúdo útil e não incongruente foi incorporado ao owner canônico; referências ao caminho legado permanecem somente quando necessárias para proveniência e rastreabilidade.

## Regra de manutenção lógica

Novos documentos desta família devem primeiro ser classificados por função, relação com os artefatos existentes, autoridade e consumidores. Conteúdo complementar deve ser incorporado ao artefato canônico apropriado; conteúdo concorrente deve ser resolvido por decisão explícita; conteúdo obsoleto não deve ser recriado apenas para preservar simetria PT/EN.
