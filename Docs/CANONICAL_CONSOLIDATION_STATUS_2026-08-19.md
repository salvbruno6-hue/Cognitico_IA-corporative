# ELO — Status Executivo da Consolidação Canônica

## Estado
CONTROLLED MIGRATION — PR #267 aberto, não mergeado.

## Objetivo
Eliminar duplicidade estrutural sem eliminar conhecimento, mantendo uma identidade estável para cada artefato e preparando a arquitetura para Knowledge Engineering, RAG, Memory, Evidence, agentes e futuras integrações ERP/IoT.

## Gates

| Gate | Estado | Regra |
|---|---|---|
| Identidade | PASS estrutural | `artifact_id`/`concept_id` definidos como identidade lógica |
| Autoridade | PASS estrutural | uma autoridade por conceito; SourceResolver existente preservado |
| Localização | PASS estrutural | `canonical_path` + `legacy_paths` |
| Proveniência | PASS estrutural | origem histórica não é sobrescrita |
| Consumidores | IN_PROGRESS | referências devem ser mapeadas antes de remoção |
| Integridade | IN_PROGRESS | conteúdo precisa ser comparado antes de depreciação |
| Testes | IN_PROGRESS | testes específicos de resolução/alias ainda precisam de evidência CI |
| Depreciação | BLOCKED | só após gates anteriores |
| Remoção | BLOCKED | somente após depreciação e ausência de dependências |

## Regra de decisão
`mergeable=false` não significa falha arquitetural; significa que o GitHub ainda não confirmou a condição de merge. Nenhuma remoção física será usada para tentar tornar o PR mergeável.

## Sequência

```text
identidade
  → índice
  → referências
  → consumidores
  → integridade
  → testes
  → CI
  → merge
  → depreciação
  → remoção
```

## Não alterar nesta fase

- `src/elo/` runtime;
- Cognitive Core;
- SourceResolver como autoridade existente;
- contratos executáveis;
- conteúdo histórico sem classificação;
- árvores PT antes de absorção comprovada.

## Próximo gate
Produzir evidência reprodutível de que cada `artifact_id` consolidado possui caminho canônico válido, aliases históricos rastreáveis e conteúdo íntegro, e então executar a suíte CI correspondente.
