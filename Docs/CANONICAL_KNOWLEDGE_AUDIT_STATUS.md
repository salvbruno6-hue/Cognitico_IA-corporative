# ELO — Status da Auditoria Canônica PT/EN

## Estado atual
`AUDITORIA_ESTRUTURAL_INICIADA`

A estrutura possui famílias paralelas em português e inglês, mas a existência de pares de diretórios não é suficiente para concluir equivalência de conteúdo.

## Famílias

| Família | PT | EN | Estado | Decisão atual |
|---|---|---|---|---|
| 00 | `00-empresa-manifesto/` | `00-enterprise-manifest/` | pendente | auditar arquivo a arquivo |
| 01 | `01-meta-arquitetura/` | `01-meta-architecture/` | pendente | auditar arquivo a arquivo |
| 05 | `05-cognitivo-plataforma/` | `05-cognitive-platform/` | pendente | auditar arquivo a arquivo |
| 07 | `07-engenharia-de dados/` | `07-data-engineering/` | pendente | auditar arquivo a arquivo |
| 11 | `11-modelos/` | `11-models-library/` | pendente | auditar arquivo a arquivo |
| 12 | `12-sistemas/` | `12-system-engineering/` | pendente | auditar arquivo a arquivo |
| 13 | `13-referências/` | `13-reference-architecture/` | pendente | auditar arquivo a arquivo |
| 14 | `14-roteiros/` | `14-roadmap/` | pendente | auditar arquivo a arquivo |
| 15 | `15-ativos/` | `15-assets/` | pendente | auditar arquivo a arquivo |

## Evidência estrutural disponível

O repositório já possui regras de navegação e mapa de estrutura canônica, além do ADR específico para consolidação bilíngue. Portanto, esta etapa deve complementar essas autoridades e não substituí-las.

Também existe um `SourceResolver` canônico no Core e testes de resolução; a migração deverá integrar-se a essa fronteira, não criar uma segunda resolução paralela.

## Decisão atual

Nenhum arquivo foi classificado como `DUPLICADO_EQUIVALENTE` apenas por nome ou tradução.

Nenhum arquivo foi excluído.

Nenhum diretório foi removido.

## Próximo gate

A próxima ação autorizada é levantar os arquivos efetivos de cada família e produzir registros de classificação individual. Somente depois será permitido definir quais pares podem ser consolidados.
