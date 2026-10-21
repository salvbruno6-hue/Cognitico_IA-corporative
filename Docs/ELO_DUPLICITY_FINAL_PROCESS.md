# ELO — Processo Definitivo de Tratamento de Duplicidades

## 1. Finalidade
Estabelecer uma regra única, repetível e auditável para identificar, decidir, consolidar e eventualmente remover duplicidades no ecossistema ELO sem criar autoridades concorrentes e sem perda de conhecimento.

O processo se aplica a documentos, código, skills, rotas, tabelas, views, funções, filas, registros de autoridade, read-models e demais artefatos persistentes ou operacionais.

## 2. Princípio canônico
A unidade lógica é o conceito (`concept_id`). O artefato físico — arquivo, tabela, view, função ou outro objeto — é uma representação da função/autoridade correspondente. Nome, idioma, pasta, extensão, schema, prefixo ou similaridade textual nunca determinam duplicidade isoladamente.

Cada conceito deve possuir uma única autoridade canônica. Representações especializadas, complementares e históricas podem existir quando possuem função comprovada e não competem pela mesma autoridade.

**Regra reuse-first:** antes de criar qualquer objeto novo, localizar e avaliar os objetos existentes que possam cumprir a mesma finalidade. Se a função já existe, reutilizar ou estender o owner canônico; não criar estrutura semelhante por conveniência operacional.

## 3. Escopo protegido
O processo não altera estruturalmente Core, Forge, `src/elo/`, runtime ou `SourceResolver` apenas para resolver duplicidades documentais. Famílias sem ownership comprovado não recebem conteúdo artificial.

Autorização administrativa do orquestrador no Forge não altera essa regra. O orquestrador pode administrar os objetos autorizados, mas continua subordinado à governança do ELO e não pode criar uma segunda autoridade por tabela, view, skill, fila ou read-model paralelo.

Um GAP de tenant, dado, capacidade, integração ou autorização **não justifica** criar uma tabela semelhante à autoridade que já existe. Nesses casos, preservar o GAP e usar os mecanismos de coleta/evidência já autorizados até que o gate seja satisfeito.

## 4. Classificação obrigatória
Todo candidato deve receber exatamente uma classificação principal:

- `EQ` — equivalente: mesmo conceito, propósito, escopo e significado; pode ser consolidado.
- `CP` — complementar: mesmo domínio, mas contém conhecimento material adicional; integrar sem perda.
- `CF` — conflitante: representa o mesmo conceito com regras/autoridades incompatíveis; bloquear o grupo para decisão.
- `EX` — exclusivo: função própria comprovada; preservar.
- `HI` — histórico/legado: representação anterior sem autoridade atual; preservar até consumidores/referências serem tratados.
- `NR` — não relacionado: sem identidade semântica suficiente; não consolidar.

Classificações como `SPECIALIZED_*` e `GOVERNANCE_*` podem ser usadas como subcategorias operacionais, mas devem apontar para uma das decisões principais acima quando necessário para o gate.

## 5. Ciclo definitivo

### Fase A — Inventário
1. Enumerar arquivos, diretórios e objetos persistentes candidatos, inclusive schemas, tabelas, views, funções, filas, contratos e read-models.
2. Capturar caminho/nome, `artifact_id` quando aplicável, `concept_id`, schema/owner, origem, status, consumidores e autoridade pretendida.
3. Agrupar por conceito/função, não por nome.
4. Para criação de banco ou runtime, pesquisar explicitamente se já existe objeto com finalidade equivalente antes de gerar DDL.

### Fase B — Análise
5. Comparar finalidade, autoridade, escopo e conteúdo.
6. Identificar conteúdo ou função exclusivos.
7. Mapear consumidores, referências, aliases, chaves, FKs, contratos e proveniência.
8. Verificar se o novo candidato existe apenas para contornar um GAP; se sim, bloquear criação e encaminhar ao owner canônico.

### Fase C — Decisão
9. Atribuir `EQ/CP/CF/EX/HI/NR`.
10. Definir um único owner canônico por conceito.
11. Registrar a decisão no registro canônico de decisões.

### Fase D — Consolidação
12. `EQ`: selecionar o owner e redirecionar referências/consumidores.
13. `CP`: incorporar o conteúdo ou capacidade material no owner sem perda.
14. `CF`: não consolidar automaticamente; encaminhar para decisão de autoridade.
15. `EX/NR`: preservar separado.
16. `HI`: preservar durante a migração e manter alias/proveniência.
17. Para objetos de banco, preferir `ALTER/EXTEND/VIEW SOBRE OWNER` quando isso preserve a autoridade existente; uma nova tabela só é aceitável quando a função materialmente distinta estiver comprovada.

### Fase E — Validação
18. Atualizar consumidores e referências.
19. Validar `SourceResolver`, contratos, FKs, views, consultas e resolução dos caminhos canônicos.
20. Executar testes de governança e integridade.
21. Executar CI no HEAD efetivo.
22. Confirmar que não restou uma segunda fonte de verdade para o mesmo conceito.

### Fase F — Depreciação e remoção
23. Só após os gates anteriores, marcar legado para depreciação.
24. Remover fisicamente apenas quando não houver consumidor/referência pendente e a política de retenção permitir.
25. Registrar a remoção e sua evidência.

## 6. Paralelização
Grupos independentes podem ser analisados simultaneamente. A decisão final por `concept_id` é única e reconciliada antes da consolidação. Um conflito em um grupo não bloqueia grupos independentes.

## 7. Regra de merge
Nenhuma consolidação física relevante deve ser considerada concluída apenas pelo commit ou migration aplicada. O grupo precisa de decisão registrada, referências/consumidores tratados e validação. `mergeable=false`, ausência de CI ou ausência de evidência não constituem aprovação.

## 8. Métricas oficiais

### Consolidação semântica
`grupos com decisão comprovada / grupos auditáveis`

### Consolidação física
`artefatos consolidados / artefatos classificados como EQ ou CP elegíveis`

### Pendência
`grupos CF + HI com consumidores/referências pendentes + grupos sem owner comprovado`

Nenhuma métrica deve contar documentação ou objeto estrutural criado como progresso de consolidação por si só.

## 9. Definition of Done por grupo
Um grupo somente recebe `CONSOLIDADO` quando possui:
- `concept_id` definido;
- `artifact_id`/objeto dos envolvidos;
- owner único;
- classificação;
- consumidores mapeados;
- referências/proveniência mapeadas;
- decisão registrada;
- alterações aplicadas quando cabíveis;
- testes executados;
- CI/evidência correspondente;
- nenhuma perda de conhecimento identificada;
- nenhuma autoridade paralela remanescente.

## 10. Estados operacionais
`DISCOVERED → CLASSIFIED → OWNER_ASSIGNED → IMPACT_MAPPED → DECIDED → CONSOLIDATED → VALIDATED → DEPRECATED → REMOVED`

`CF` pode permanecer em `DECIDED/BLOCKED` até resolução de autoridade. `HI` pode permanecer `VALIDATED/LEGACY` sem remoção enquanto houver obrigação de retenção ou referência.

## 11. Regra final
Duplicidade não significa simplesmente "dois arquivos parecidos" ou "duas tabelas com nomes próximos". Duplicidade é a existência de múltiplas representações que competem pela mesma identidade, autoridade e função sem necessidade legítima de coexistência.

O ELO consolida a identidade e a autoridade antes de consolidar o artefato físico.
