# ELO — Processo Definitivo de Tratamento de Duplicidades

## 1. Finalidade
Estabelecer uma regra única, repetível e auditável para identificar, decidir, consolidar e eventualmente remover duplicidades no ecossistema ELO sem criar autoridades concorrentes e sem perda de conhecimento.

## 2. Princípio canônico
A unidade lógica é o conceito (`concept_id`). O arquivo é uma representação física (`artifact_id`). Nome, idioma, pasta, extensão ou similaridade textual nunca determinam duplicidade isoladamente.

Cada conceito deve possuir uma única autoridade canônica. Representações especializadas, complementares e históricas podem existir quando possuem função comprovada e não competem pela mesma autoridade.

## 3. Escopo protegido
O processo não altera estruturalmente Core, Forge, `src/elo/`, runtime ou `SourceResolver` para resolver duplicidades documentais. Famílias sem ownership comprovado não recebem conteúdo artificial.

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
1. Enumerar arquivos e diretórios candidatos.
2. Capturar caminho, `artifact_id`, `concept_id`, tamanho, origem e status.
3. Agrupar por conceito, não por nome.

### Fase B — Análise
4. Comparar finalidade, autoridade, escopo e conteúdo.
5. Identificar conteúdo exclusivo.
6. Mapear consumidores, referências, aliases e proveniência.

### Fase C — Decisão
7. Atribuir `EQ/CP/CF/EX/HI/NR`.
8. Definir um único owner canônico por conceito.
9. Registrar a decisão no registro canônico de decisões.

### Fase D — Consolidação
10. `EQ`: selecionar o owner e redirecionar referências.
11. `CP`: incorporar o conteúdo material no owner sem perda.
12. `CF`: não consolidar automaticamente; encaminhar para decisão de autoridade.
13. `EX/NR`: preservar separado.
14. `HI`: preservar durante a migração e manter alias/proveniência.

### Fase E — Validação
15. Atualizar consumidores e referências.
16. Validar `SourceResolver` e resolução dos caminhos canônicos.
17. Executar testes de governança e integridade.
18. Executar CI no HEAD efetivo.

### Fase F — Depreciação e remoção
19. Só após os gates anteriores, marcar legado para depreciação.
20. Remover fisicamente apenas quando não houver consumidor/referência pendente e a política de retenção permitir.
21. Registrar a remoção e sua evidência.

## 6. Paralelização
Grupos independentes podem ser analisados simultaneamente. A decisão final por `concept_id` é única e reconciliada antes da consolidação. Um conflito em um grupo não bloqueia grupos independentes.

## 7. Regra de merge
Nenhuma consolidação física relevante deve ser considerada concluída apenas pelo commit. O grupo precisa de decisão registrada, referências/consumidores tratados e validação. `mergeable=false`, ausência de CI ou ausência de evidência não constituem aprovação.

## 8. Métricas oficiais

### Consolidação semântica
`grupos com decisão comprovada / grupos auditáveis`

### Consolidação física
`artefatos consolidados / artefatos classificados como EQ ou CP elegíveis`

### Pendência
`grupos CF + HI com consumidores/referências pendentes + grupos sem owner comprovado`

Nenhuma métrica deve contar documentação criada como progresso de consolidação.

## 9. Definition of Done por grupo
Um grupo somente recebe `CONSOLIDADO` quando possui:
- `concept_id` definido;
- `artifact_id` dos envolvidos;
- owner único;
- classificação;
- consumidores mapeados;
- referências/proveniência mapeadas;
- decisão registrada;
- alterações aplicadas quando cabíveis;
- testes executados;
- CI/evidência correspondente;
- nenhuma perda de conhecimento identificada.

## 10. Estados operacionais
`DISCOVERED → CLASSIFIED → OWNER_ASSIGNED → IMPACT_MAPPED → DECIDED → CONSOLIDATED → VALIDATED → DEPRECATED → REMOVED`

`CF` pode permanecer em `DECIDED/BLOCKED` até resolução de autoridade. `HI` pode permanecer `VALIDATED/LEGACY` sem remoção enquanto houver obrigação de retenção ou referência.

## 11. Regra final
Duplicidade não significa simplesmente "dois arquivos parecidos". Duplicidade é a existência de múltiplas representações que competem pela mesma identidade, autoridade e função sem necessidade legítima de coexistência.

O ELO consolida a identidade antes de consolidar o arquivo físico.
