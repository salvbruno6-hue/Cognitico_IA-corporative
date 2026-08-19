# ELO — Matriz de Migração e Impacto de Endereços

## Regra central

A mudança física de endereço não pode alterar a identidade do conhecimento.

```text
artifact_id
   ↓
concept_id
   ↓
canonical_path
   ↓
consumidores
   ↓
legacy_paths (compatibilidade)
```

## Impactos que precisam ser adaptados

| Consumidor | Risco | Estratégia |
|---|---|---|
| SourceResolver | alto | resolver por identidade/índice; não por path histórico |
| SourceDiscovery | alto | devolver candidatos com identidade lógica |
| Knowledge Engineering | alto | registrar autoridade, proveniência e lifecycle |
| RAG | alto | recuperar objetos canônicos, não diretórios arbitrários |
| Memory | alto | guardar identidade e proveniência junto ao registro |
| Agentes | alto | nunca fixar caminho físico como identidade |
| Índices/documentação | médio | atualizar referências para canonical_path |
| Testes | alto | adicionar casos canonical + legacy alias |
| CI | alto | gate de referências quebradas e autoridade duplicada |
| Multiteiner tenant | alto | separar conhecimento corporativo do conhecimento específico do tenant |

## Sequência de adaptação

1. Registrar identidade.
2. Criar índice canônico.
3. Registrar aliases históricos.
4. Migrar consumidores.
5. Migrar conteúdo.
6. Validar resolução.
7. Depreciar caminhos antigos.
8. Remover somente após gate verde.

## Proibição

Não alterar `src/elo/core/` apenas para resolver nomenclatura documental nesta fase. O runtime existente deve ser preservado; a integração do índice deve ocorrer por contrato explícito quando houver implementação autorizada.

## Critério de conclusão

Um arquivo só pode perder seu endereço histórico quando:

- possuir `artifact_id`;
- possuir proprietário canônico;
- possuir proveniência;
- seus consumidores tiverem sido mapeados;
- referências antigas forem resolvíveis ou formalmente depreciadas;
- testes/CI estiverem verdes;
- nenhum conteúdo exclusivo for perdido.
