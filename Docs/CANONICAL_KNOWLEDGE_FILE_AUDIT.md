# ELO — Auditoria Minuciosa de Arquivos para Consolidação Canônica

## Objetivo
Converter a consolidação PT/EN de uma decisão por nome de pasta para uma decisão por **conteúdo, identidade, dependência e autoridade**.

## Regra de ouro
Nenhum arquivo é considerado duplicado somente porque possui nome semelhante, tradução equivalente ou localização paralela.

A classificação precisa considerar, nesta ordem:

1. identidade conceitual;
2. conteúdo efetivo;
3. autoridade declarada;
4. referências consumidoras;
5. proveniência;
6. maturidade/status;
7. diferença de idioma;
8. dependências externas;
9. risco de perda;
10. possibilidade de consolidação reversível.

## Classificações oficiais

| Código | Significado | Ação |
|---|---|---|
| `DUPLICADO_EQUIVALENTE` | Mesmo conceito e conteúdo materialmente equivalente | Manter um canônico; aliasar o outro |
| `COMPLEMENTAR` | Mesmo domínio, mas conteúdo adicional não redundante | Integrar sem perder proveniência |
| `CONFLITANTE` | Mesmo conceito com afirmações/regras incompatíveis | Não mesclar automaticamente; abrir decisão |
| `EXCLUSIVO` | Conteúdo sem equivalente | Preservar como autoridade própria |
| `HISTÓRICO` | Evidência de evolução anterior | Preservar como histórico, não como autoridade atual |
| `ESTRUTURAL` | Arquivo serve à navegação/estrutura, não ao conhecimento | Avaliar separadamente |
| `DEPRECATED` | Substituído após migração validada | Manter referência e motivo |
| `PENDENTE` | Evidência insuficiente para decisão | Não mover nem excluir |

## Matriz de decisão

### Etapa A — Identidade
Perguntar: os dois arquivos representam o mesmo `concept_id`?

- não → não são duplicados;
- sim → continuar.

### Etapa B — Conteúdo
Comparar títulos, seções, tabelas, regras, contratos, exemplos, referências e decisões.

### Etapa C — Semântica
Uma tradução não deve ser tratada como cópia se houver adaptação de significado.

### Etapa D — Autoridade
Verificar qual arquivo é citado como canônico por ADRs, índices, contratos, testes ou regras de governança.

### Etapa E — Consumidores
Localizar referências ao caminho, nome, identificador e conceito.

### Etapa F — Proveniência
Registrar origem, commit, data, caminho anterior e transformação.

### Etapa G — Decisão
Somente então atribuir uma classificação.

## Modelo de registro por arquivo

```yaml
artifact_id: ELO.ARTIFACT.<stable-id>
concept_id: ELO.CONCEPT.<stable-id>
source_path: <path>
canonical_path: <path-or-null>
legacy_paths: []
language: pt-BR|en|mixed
classification: PENDENTE
authority: unknown|canonical|legacy|historical|complementary
content_hash: <hash>
semantic_hash: <future-normalized-hash>
consumers: []
provenance:
  source_commit: <sha>
  source_date: <date>
  transformation: none|rename|translation|merge|split|supersede
risk: low|medium|high|critical
decision: <decision>
review_required: true
```

## Ordem de auditoria

1. `00-empresa-manifesto` ↔ `00-enterprise-manifest`
2. `01-meta-arquitetura` ↔ `01-meta-architecture`
3. `05-cognitivo-plataforma` ↔ `05-cognitive-platform`
4. `07-engenharia-de dados` ↔ `07-data-engineering`
5. `11-modelos` ↔ `11-models-library`
6. `12-sistemas` ↔ `12-system-engineering`
7. `13-referências` ↔ `13-reference-architecture`
8. `14-roteiros` ↔ `14-roadmap`
9. `15-ativos` ↔ `15-assets`

## Critério profissional de consolidação

Um arquivo só pode ser fisicamente removido quando:

- existe proprietário canônico;
- existe `artifact_id` estável;
- todos os consumidores foram migrados;
- aliases foram registrados quando necessários;
- conteúdo exclusivo foi preservado;
- conflitos foram resolvidos formalmente;
- proveniência está preservada;
- testes de referência passam;
- CI passa;
- não existe dependência oculta conhecida.

## Proibição

É proibido executar um `delete` em lote de uma árvore PT/EN como mecanismo de consolidação.

A consolidação é uma **migração de autoridade**, não uma operação cosmética de nomenclatura.

## Relação com o ELO

Este procedimento preserva a separação:

```text
Cognitivo → definição/conhecimento
Core      → interpretação, governança e decisão
Forge     → execução especializada autorizada
```

A consolidação documental não deve criar uma nova autoridade paralela ao Core nem alterar contratos de execução.
