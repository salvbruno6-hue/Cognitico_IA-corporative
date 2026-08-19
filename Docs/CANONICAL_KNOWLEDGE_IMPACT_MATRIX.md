# ELO — Matriz de Impacto da Mudança de Endereço do Conhecimento

## Finalidade
Determinar o que precisa ser alterado quando um artefato muda de endereço físico, sem permitir que o endereço se torne a identidade do conhecimento.

## Princípio

```text
artifact_id permanece
        ↓
canonical_path pode mudar
        ↓
resolver continua encontrando o artefato
        ↓
consumidores não quebram
```

## Camadas impactadas

| Camada | Impacto potencial | Ação |
|---|---:|---|
| Índice documental | crítico | atualizar localização canônica |
| Source Discovery | alto | resolver por identidade/conceito |
| Source Resolver | alto | aceitar identidade e aliases |
| Knowledge Engineering | alto | não armazenar caminho como identidade |
| Memory | alto | preservar `artifact_id` + proveniência |
| RAG | alto | indexar identidade, conteúdo e versão |
| Agentes | alto | consumir referência canônica |
| Reasoning | médio/alto | preservar contexto/proveniência |
| Evidence | alto | manter origem e hash |
| Governance | crítico | registrar mudança de autoridade |
| Testes | alto | validar caminho novo e alias |
| CI | alto | impedir referências quebradas |
| Documentação | médio | atualizar links |
| Runtime Core | protegido | não alterar sem necessidade comprovada |

## Sequência de migração

```text
1. Registrar artifact_id
2. Registrar caminho atual
3. Registrar novo canonical_path
4. Registrar aliases
5. Encontrar consumidores
6. Atualizar consumidores
7. Testar resolução
8. Testar proveniência
9. Testar agentes/RAG/Memory
10. Deprecar caminho antigo
11. Remover somente após gate
```

## Falha que deve ser evitada

```text
arquivo A
  ↓ rename
arquivo B
  ↓
identidade muda
  ↓
RAG perde referência
Memory perde proveniência
agente aponta para endereço inexistente
```

## Resultado esperado

O endereço passa a ser um atributo operacional do conhecimento, e não sua identidade.

## Gate de aprovação

Nenhuma mudança física deve ser considerada concluída enquanto:

- `artifact_id` estiver preservado;
- todos os aliases críticos estiverem registrados;
- consumidores conhecidos estiverem migrados;
- testes de resolução estiverem aprovados;
- CI estiver verde;
- evidência da migração estiver registrada.
