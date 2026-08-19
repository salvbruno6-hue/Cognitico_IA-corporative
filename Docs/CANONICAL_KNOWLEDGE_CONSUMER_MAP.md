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

## Condição de segurança

Uma mudança física só é segura quando a resolução por identidade continua retornando o mesmo conceito, versão/proveniência e autoridade esperados.

## Não permitido

- renomear pasta e considerar isso consolidação;
- apagar PT porque existe EN;
- criar segundo Core/resolver;
- mudar semântica sem decisão explícita;
- atualizar somente documentação sem atualizar consumidores.
