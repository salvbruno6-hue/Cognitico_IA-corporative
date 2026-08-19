# ELO — Matriz de Auditoria e Consolidação do Conhecimento

## 1. Finalidade

Esta matriz governa a análise arquivo-a-arquivo das árvores históricas e canônicas. Ela impede que nomes semelhantes sejam tratados automaticamente como equivalentes e estabelece a sequência segura para migração.

A estrutura canônica existente determina que a autoridade é semântica e governada por baseline, ADR, metadados, evidências e testes; o diretório físico não é autoridade isoladamente.

## 2. Classificação obrigatória

| Código | Classificação | Regra | Ação |
|---|---|---|---|
| EQ | EQUIVALENTE | Mesmo conceito, escopo e significado operacional | Consolidar no proprietário canônico; preservar proveniência |
| CP | COMPLEMENTAR | Mesmo domínio, mas acrescenta informação não presente no canônico | Incorporar sem perda; registrar origem |
| CF | CONFLITANTE | Mesmo conceito com regras, definições ou autoridade divergentes | Não mesclar automaticamente; decisão explícita |
| EX | EXCLUSIVO | Conteúdo sem equivalente no proprietário canônico | Migrar como novo artefato no proprietário adequado |
| HI | HISTÓRICO | Evidência de evolução sem função normativa atual | Preservar em histórico ou arquivar |
| NR | NÃO RELACIONADO | Sem relação semântica suficiente | Não mover por semelhança nominal |

## 3. Critérios de equivalência

Um arquivo somente pode receber `EQ` quando todos forem verdadeiros:

1. mesmo conceito;
2. mesmo objetivo;
3. mesmo escopo;
4. mesma autoridade pretendida;
5. ausência de informação material exclusiva;
6. ausência de conflito normativo;
7. referências podem ser redirecionadas sem mudança de significado.

Nome, idioma ou localização não são critérios suficientes.

## 4. Critérios de complementaridade

`CP` deve ser usado quando o conteúdo histórico adiciona dados, exemplos, regras, contexto ou evidências úteis ao proprietário canônico. A incorporação deve conservar:

- proveniência;
- autoria, quando disponível;
- data, quando disponível;
- versão;
- origem física;
- referências afetadas.

## 5. Critérios de conflito

`CF` exige bloqueio da remoção e decisão arquitetural/documental. Exemplos:

- definições diferentes do mesmo conceito;
- regras incompatíveis;
- caminhos que aparentam ser canônicos diferentes;
- versões que não podem coexistir como uma única verdade;
- dependências que apontam para autoridades diferentes.

## 6. Identidade do artefato

Cada registro auditado deve possuir:

```text
artifact_id
concept_id
source_path
canonical_path
classification
status
content_hash
language
authority
provenance
references
migration_action
review_required
```

`artifact_id` permanece estável quando o arquivo muda de endereço.

## 7. Matriz inicial das famílias conhecidas

| Família | Canônico | Histórico | Estado | Próxima ação |
|---|---|---|---|---|
| 00 | `00-enterprise-manifest/` | `00-empresa-manifesto/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 01 | `01-meta-architecture/` | `01-meta-arquitetura/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 05 | `05-cognitive-platform/` | `05-cognitivo-plataforma/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 07 | `07-data-engineering/` | `07-engenharia-de dados/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 11 | `11-models-library/` | `11-modelos/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 12 | `12-system-engineering/` | `12-sistemas/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 13 | `13-reference-architecture/` | `13-referências/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 14 | `14-roadmap/` | `14-roteiros/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |
| 15 | `15-assets/` | `15-ativos/` | AUDIT_REQUIRED | comparar arquivo-a-arquivo |

A matriz não presume equivalência apenas pela correspondência dos números.

## 8. Impacto da mudança de endereço

Toda migração deve atualizar ou validar:

1. índices documentais;
2. links relativos;
3. referências em Markdown;
4. registros de conhecimento;
5. aliases legados;
6. testes de resolução;
7. agentes que consultem o conhecimento;
8. RAG/Memory quando passarem a consumir esse registro;
9. evidências e proveniência;
10. CI/gates.

## 9. Regra de segurança

Nenhuma remoção física será realizada enquanto houver:

- conteúdo exclusivo não migrado;
- conflito não decidido;
- consumidor ativo não migrado;
- referência quebrada;
- ausência de proveniência;
- teste de resolução incompatível;
- dependência operacional desconhecida.

## 10. Sequência de execução

```text
Inventário
  ↓
Hash/conteúdo
  ↓
Classificação
  ↓
Identidade
  ↓
Mapa de referências
  ↓
Decisão de migração
  ↓
Atualização de índices/aliases
  ↓
Testes
  ↓
Depreciação
  ↓
Remoção somente quando segura
```

## 11. Estado da fase

Esta matriz é uma camada de governança e não altera `src/elo/`. A consolidação física somente ocorrerá depois da auditoria e dos gates correspondentes.
