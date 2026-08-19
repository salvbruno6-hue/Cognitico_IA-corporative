# ELO — Protocolo de Auditoria Arquivo-a-Arquivo das Famílias Canônicas

## Estado
`AUDIT_PROTOCOL — NO_PHYSICAL_MIGRATION`

## Finalidade
Estabelecer o procedimento único para auditar as famílias PT/EN antes de atribuir identidade definitiva, classificar equivalência ou alterar endereços físicos.

## Regra central
Nenhuma família é considerada consolidada por semelhança nominal, simetria de pastas ou existência de um caminho canônico proposto.

## Ordem obrigatória

```text
1. Inventário de arquivos
2. Hash/conteúdo
3. Comparação semântica
4. Classificação EQ/CP/CF/EX/HI/NR
5. Identidade
6. Proveniência
7. Referências e consumidores
8. Decisão de migração
9. Testes
10. Depreciação somente após os gates
```

## Escopo das nove famílias

```text
00 enterprise manifest
01 meta architecture
05 cognitive platform
07 data engineering
11 models library
12 system engineering
13 reference architecture
14 roadmap
15 assets
```

## Critérios de classificação

- `EQ`: conteúdo semanticamente equivalente e consolidável sem perda.
- `CP`: conteúdo complementar; deve ser incorporado preservando a contribuição de cada origem.
- `CF`: conflito semântico; exige decisão explícita.
- `EX`: conteúdo exclusivo; não pode ser descartado por consolidação.
- `HI`: conteúdo histórico/proveniência; preservar rastreabilidade.
- `NR`: não relacionado; não deve ser forçado para a família.

## Identidade
`artifact_id` só pode sair de `PENDING` após evidência de conteúdo. `concept_id` só pode ser compartilhado quando a análise demonstrar o mesmo conceito.

## Referências
Cada arquivo auditado deve ter suas referências conhecidas registradas. Uma referência pode ser:

- caminho físico;
- link Markdown;
- import/require;
- referência em YAML/JSON;
- nome lógico;
- índice ou catálogo;
- consumidor de CI;
- documentação operacional.

## Saída mínima por arquivo

```yaml
family_id: PENDING
artifact_id: PENDING
concept_id: PENDING
source_path: PENDING
canonical_candidate: PENDING
legacy_paths: []
classification: PENDING
content_hash: PENDING
language: PENDING
provenance: PENDING
references: []
consumers: []
migration_action: PENDING
review_required: true
```

## Regra de decisão

```text
Evidência insuficiente → PENDING
Conflito → CF + revisão
Conteúdo exclusivo → EX + preservação
Complementar → CP + incorporação controlada
Equivalente → EQ + consolidação possível
Histórico → HI + preservação
Não relacionado → NR + fora da consolidação
```

## Proibição
Este protocolo não autoriza:

- remoção de árvores históricas;
- alteração de `src/elo/`;
- substituição do `SourceResolver`;
- atribuição de identidade por nome/path;
- criação de uma segunda autoridade de conhecimento.

## Critério de avanço
Uma família somente pode avançar para migração quando todos os seus arquivos relevantes possuírem evidência suficiente de conteúdo, identidade, proveniência e referências e os gates aplicáveis estiverem aprovados.
