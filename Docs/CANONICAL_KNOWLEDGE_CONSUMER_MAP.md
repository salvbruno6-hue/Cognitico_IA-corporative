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

## Evidência executada — 2026-08-20

Foi realizada busca transversal no repositório pelos cinco `legacy_path` registrados no catálogo canônico. Nenhum consumidor operacional textual foi localizado para os cinco caminhos; as ocorrências encontradas ficaram restritas a registros, auditorias e documentação de migração.

| `concept_id` | Legacy path | Resultado |
|---|---|---|
| `ELO.ARCHITECTURE.MASTER` | `01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md` | `TEXTUAL_SCAN_CLEAR` |
| `ELO.DATA_ENGINEERING.MASTER` | `07-engenharia de dados/DATA_ENGINEERING_MASTER.md` | `TEXTUAL_SCAN_CLEAR` |
| `ELO.MODELS.LIBRARY.MASTER` | `11-modelos/MODELS_LIBRARY_MASTER.md` | `TEXTUAL_SCAN_CLEAR` |
| `ELO.SYSTEMS.ENGINEERING.MASTER` | `12-sistemas/SYSTEMS_ENGINEERING_MASTER.md` | `TEXTUAL_SCAN_CLEAR` |
| `ELO.ROADMAP.MASTER` | `14-roteiros/ROADMAP_MASTER.md` | `TEXTUAL_SCAN_CLEAR` |

## Limite da evidência

`TEXTUAL_SCAN_CLEAR` não significa `RUNTIME_CLEAR`. O gate de remoção permanece fechado até validação por identidade/alias, testes relevantes e CI.

Nenhum caminho legado deve ser removido por esta evidência isolada.

## Relação com o runtime

O repositório possui `src/elo/core/source_resolver.py` e `source_discovery.py`. A consolidação deve integrar o índice canônico a essa fronteira, não criar um segundo resolver.

## Próximo gate

`TEXTUAL_SCAN_CLEAR → RUNTIME_ALIAS_VALIDATION → TESTES → CI → DEPRECIAÇÃO → REMOÇÃO`
