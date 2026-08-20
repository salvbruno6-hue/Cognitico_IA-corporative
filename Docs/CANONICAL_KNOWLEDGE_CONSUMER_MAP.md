# ELO — Mapa de Consumidores e Impacto de Endereço

## Objetivo
Registrar onde uma alteração de endereço físico pode quebrar o ELO e estabelecer a ordem segura de adaptação.

## Regra
Consumidores devem depender da identidade canônica e não de caminhos históricos. O caminho é localização; `artifact_id` é identidade.

## Matriz de impacto

| Consumidor | Risco | Adaptação |
|---|---|---|
| Core | crítico | resolver identidade sem alterar autoridade do Core |
| Knowledge Engineering | crítico | consultar índice canônico; preservar proveniência |
| Source Discovery/Resolver | crítico | aceitar identidade canônica antes do caminho físico |
| Memory | alto | armazenar identidade + versão + proveniência |
| RAG | alto | indexar `artifact_id` e não somente path |
| Evidence | alto | preservar origem, hash e versão |
| Agents | crítico | consumir referência canônica; não gravar path como identidade |
| Governance | alto | auditar mudança de identidade/endereço separadamente |
| Tests | crítico | validar canonical path e aliases |
| CI | crítico | impedir referência histórica não tratada |
| Docs/índices | médio | atualizar links após consolidação |
| Scripts | alto | eliminar dependência de caminhos frágeis |

## Ordem de migração

1. registrar identidade;
2. registrar canonical path;
3. registrar aliases;
4. descobrir consumidores;
5. adaptar consumidores;
6. testar resolução antiga e nova;
7. migrar endereço;
8. deprecar alias somente depois dos gates.

## Evidência executada — 2026-08-20

Foi realizada busca transversal no repositório pelos cinco `legacy_path` registrados no catálogo canônico:

| `concept_id` | Legacy path pesquisado | Evidência encontrada | Classificação atual |
|---|---|---|---|
| `ELO.ARCHITECTURE.MASTER` | `01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md` | somente registro/auditoria; nenhum consumidor operacional localizado | sem consumidor operacional identificado |
| `ELO.DATA_ENGINEERING.MASTER` | `07-engenharia de dados/DATA_ENGINEERING_MASTER.md` | somente registro canônico; nenhum consumidor operacional localizado | sem consumidor operacional identificado |
| `ELO.MODELS.LIBRARY.MASTER` | `11-modelos/MODELS_LIBRARY_MASTER.md` | somente registro/auditoria; nenhum consumidor operacional localizado | sem consumidor operacional identificado |
| `ELO.SYSTEMS.ENGINEERING.MASTER` | `12-sistemas/SYSTEMS_ENGINEERING_MASTER.md` | somente registro/auditoria; nenhum consumidor operacional localizado | sem consumidor operacional identificado |
| `ELO.ROADMAP.MASTER` | `14-roteiros/ROADMAP_MASTER.md` | somente registro canônico/auditoria; nenhum consumidor operacional localizado | sem consumidor operacional identificado |

### Limite da evidência

A busca confirma ausência de referências textuais encontradas no índice pesquisável do repositório, mas **não fecha ainda o gate de remoção física**. A resolução por identidade/alias, testes e CI ainda precisam ser comprovados.

Nenhum caminho legado deve ser removido por esta evidência isolada.

## Relação com o runtime

O repositório possui `src/elo/core/source_resolver.py` e `source_discovery.py`. A consolidação deve integrar o índice canônico a essa fronteira, não criar um segundo resolver.

## Condição de segurança

Uma mudança física só é segura quando a resolução por identidade continua retornando o mesmo conceito, versão/proveniência e autoridade esperados.

## Não permitido

- renomear pasta e considerar isso consolidação;
- apagar PT porque existe EN;
- criar segundo Core/resolver;
- mudar semântica sem decisão explícita;
- atualizar somente documentação sem atualizar consumidores;
- tratar ausência de ocorrência textual como prova suficiente para remoção.
