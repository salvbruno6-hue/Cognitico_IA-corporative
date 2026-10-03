# PCP — Instruções Gerais e Governança de Conhecimento

## 1. Finalidade

Este documento é a **instrução geral e autoridade documental do domínio PCP**.

Nenhuma instrução específica de PCP deve ser interpretada isoladamente. Documentos especializados existem para detalhar uma etapa, fonte, regra ou integração prevista neste documento mestre.

A relação documental é:

**Instrução Geral PCP → Diretriz/Processo → Instrução Especializada → Procedimento Operacional → Execução no ELO/Supabase**

Um documento especializado não pode criar uma regra que contradiga a instrução geral. Quando uma regra nova for necessária, primeiro deve ser incorporada à governança do PCP e somente depois detalhada em documento específico.

## 2. Princípio de autoridade

### GitHub
É a autoridade canônica de instruções, regras de negócio, conhecimento operacional versionado, migrações, views, funções, triggers, contratos de integração e histórico das alterações.

### Supabase
É a autoridade do estado operacional efetivamente armazenado: dados, schema, views implantadas, funções, triggers e registros de execução.

### ELO
É a camada de interpretação, validação e orquestração.

O ELO não cria autoridade paralela. Ele deve seguir as regras documentadas e os estados efetivamente disponíveis.

## 3. Hierarquia documental

### Nível 1 — Instrução Geral PCP
Define princípios, sequência geral, autoridades, gates, regras de evidência e governança.

Este arquivo é o nível 1.

### Nível 2 — Diretrizes e processos
Detalham grandes processos do PCP, como demanda, planejamento, cobertura, produção, capacidade, operação externa e integração com RH.

### Nível 3 — Instruções especializadas
Detalham uma regra específica sem criar nova autoridade.

Exemplos: vínculo entre reparo e unidade modular, integração ELO para reparos, comparabilidade da demanda e composição funcional.

### Nível 4 — Procedimentos operacionais
Descrevem como executar uma operação concreta, incluindo carga, validação, reconciliação e testes.

## 4. Regra de não isolamento

Todo documento especializado deve possuir:

1. referência explícita a este documento mestre;
2. finalidade dentro do processo PCP;
3. entradas necessárias;
4. regra que está detalhando;
5. dependências;
6. saída produzida;
7. GAPs possíveis;
8. gate de validação;
9. autoridade dos dados;
10. documento ou processo pai.

Se não possuir esses elementos, não deve ser tratado como instrução oficial do PCP.

## 5. Regra de evidência

**Dado ausente gera GAP. Nunca gera inferência.**

O PCP deve distinguir dado recebido, dado validado, cálculo, hipótese, GAP e decisão autorizada.

Uma fonte operacional não se torna autoridade apenas porque foi recebida.

## 6. Cadeia geral do PCP externo

**Demanda Comercial → Histórico Comparável → Previsão → Fator → Cobertura Física → Produção Programada → Necessidade Adicional de Fabricação → Carga Operacional → Capacidade/Gargalos → Composição Funcional → Produtividade → Demanda Humana → RH**

A cadeia pode parar em qualquer gate quando faltar evidência.

## 7. Demanda

A demanda deve preservar período, natureza, produto/modelo, taxonomia, quantidade, chave de comparabilidade, origem e confiabilidade.

O fator de crescimento/redução é calculado sobre dimensões comparáveis.

O fator não deve ser aplicado diretamente ao quadro de RH, ao estoque físico ou à quantidade de reparos.

## 8. Cobertura física

Antes de concluir que o crescimento da demanda exige fabricação adicional, o PCP deve verificar:

1. estoque disponível;
2. reparos recuperáveis;
3. produção já programada.

A regra analítica é:

**Necessidade adicional de fabricação = max(demanda prevista - estoque disponível - reparos recuperáveis - produção programada, 0)**

A cobertura física deve ser consolidada no nível de modelo para evitar dupla contagem entre diferentes naturezas de demanda.

## 9. Reparos

Reparos são uma fonte potencial de cobertura, não uma nova demanda.

Um reparo só pode ser considerado recuperável quando houver evidência suficiente de identidade da unidade, modelo válido, status compatível, data necessária ao horizonte, ausência de condição impeditiva e ausência de dupla contagem.

A documentação especializada deste processo é:

'06-knowledge-engineering/PCP_VINCULO_REPARO_UNIDADE_MODULAR.md'

A instrução de integração do ELO é:

'06-knowledge-engineering/PCP_ELO_INTEGRACAO_REPAROS.md'

Esses documentos são subordinados a esta instrução geral.

## 10. Integração com o Projeto Integrador

O PCP deve refletir os impactos da decisão no fluxo operacional.

O Projeto Integrador identifica a necessidade de gestão visual, controle de lead time, OEE, cronometragem dos processos, gestão de gargalos, integração entre setores, redução de reprogramações e maior confiabilidade dos dados.

Esses elementos são contexto para a reflexão operacional. Não substituem as regras de comparabilidade da demanda nem autorizam inferências.

O fluxo produtivo de referência documentado no Projeto Integrador é:

**Comercial → Engenharia → PCP → Compras → Almoxarifado → Estrutura Metálica → Pintura → Montagem → Componentes Complementares → Expedição**

## 11. ELO

O ELO deve:

1. ler o estado atual;
2. identificar a regra aplicável;
3. verificar evidências;
4. identificar GAPs;
5. solicitar validação quando o gate exigir;
6. executar somente operações autorizadas;
7. registrar o resultado;
8. preservar rastreabilidade.

O ELO não deve criar dados fictícios, escolher uma fonte concorrente, transformar GAP em estimativa, aplicar automaticamente crescimento ao RH, reconhecer reparo como cobertura sem vínculo validado ou criar regra especializada fora da hierarquia documental.

## 12. Git × Supabase

A existência de um objeto no Supabase não prova que ele esteja versionado corretamente no Git.

A existência de uma regra no Git não prova que ela esteja implantada no Supabase.

Quando houver divergência:

**registrar GAP → identificar natureza da divergência → comparar estados → reconciliar por alteração versionada → validar novamente**

Não editar manualmente o histórico de migrações para esconder divergências.

## 13. Gate documental

Uma instrução especializada somente pode ser considerada oficial quando:

- possui documento pai;
- está vinculada ao processo correspondente;
- não contradiz a instrução geral;
- possui entradas e saídas definidas;
- possui critérios de evidência;
- possui tratamento de GAP;
- possui gate de validação;
- está versionada no Git;
- sua implementação, quando houver, está alinhada ao Supabase.

## 14. Gate de execução

A existência da documentação não significa que o cálculo esteja liberado.

A execução deve seguir:

**Documento → regra → fonte → dado → validação → cálculo → resultado → validação → decisão**

Quando faltar qualquer evidência obrigatória, o processo fica bloqueado no respectivo gate.

## 15. Regra para criação de novas instruções

Antes de criar uma nova instrução PCP:

1. procurar instrução existente;
2. identificar o documento pai;
3. verificar se a regra já existe;
4. consolidar duplicidades;
5. decidir se é extensão ou nova instrução;
6. registrar dependências;
7. criar o documento especializado somente se necessário;
8. versionar no Git;
9. validar a relação com o ELO e Supabase.

**Não criar instruções isoladas.**

## 16. Mapa atual

### Documento mestre

'PCP_INSTRUCOES_GERAIS_GOVERNANCA.md'

### Processo de demanda

'PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md'

### Apoio visual do processo de demanda

'PCP_DEMANDA_CRESCIMENTO_FLUXO.md' — representação visual subordinada ao processo de demanda; não cria regra própria.

### Especialização de reparos

'PCP_VINCULO_REPARO_UNIDADE_MODULAR.md'

### Integração ELO de reparos

'PCP_ELO_INTEGRACAO_REPAROS.md'

O processo de demanda e os documentos de reparo devem ser lidos como partes de uma mesma cadeia, subordinados a esta instrução geral.

## 17. Regra de atualização

Alterações em uma instrução especializada que alterem princípio, autoridade, sequência ou gate do PCP devem primeiro atualizar esta instrução geral.

Alterações que apenas detalhem uma execução podem permanecer no documento especializado, desde que não contradigam o nível superior.

## 18. Modelo de operação — uma única mente PCP

O PCP deve ser tratado como **uma mente governada**, não como uma coleção de instruções que o ELO escolhe conforme o texto encontrado.

A regra é: **uma pergunta → uma cadeia canônica → um estado → um próximo gate → uma evidência exigida → um resultado rastreável**.

As instruções especializadas aprofundam uma etapa. Elas não podem reordenar a cadeia, substituir uma fonte, liberar um gate ou criar um cálculo que o processo pai ainda não liberou.

### 18.1 Ordem canônica de raciocínio

1. Identificar a pergunta decisória.
2. Classificar o tipo de demanda/processo.
3. Localizar a fonte de autoridade correspondente.
4. Verificar identidade do produto/modelo/taxonomia.
5. Verificar período, unidade, natureza e comparabilidade.
6. Separar fato, previsão, cálculo, hipótese e GAP.
7. Executar somente o cálculo autorizado pelo gate atual.
8. Verificar cobertura física antes de converter crescimento em fabricação.
9. Verificar carga, capacidade e gargalos antes de converter carga em necessidade humana.
10. Somente depois avaliar composição funcional, produtividade e demanda humana.
11. RH somente após a demanda humana estar validada e houver fonte autorizada de capacidade/disponibilidade.
12. Registrar resultado, evidências, GAPs e próximo passo.

### 18.2 Regra de estado

A implantação técnica de uma capacidade não significa que a execução analítica esteja liberada.

Devem ser diferenciados:
- **CAPACIDADE_IMPLANTADA** — código, view, função ou skill existe;
- **DADO_DISPONÍVEL** — fonte necessária possui registros válidos;
- **GATE_VALIDADO** — critérios do processo foram satisfeitos;
- **EXECUÇÃO_LIBERADA** — o próximo cálculo pode ocorrer;
- **RESULTADO_VALIDADO** — cálculo foi executado e conferido.

Uma view de demanda humana projetada pode existir no Supabase enquanto o PCP permanece em `AGUARDANDO_HISTORICO` ou `AGUARDANDO_VALIDACAO_DE_COMPARABILIDADE`. A existência da view não autoriza antecipar a etapa.

### 18.3 Regra de conflito entre instruções

Se duas instruções apresentarem redações diferentes:
1. prevalece o documento mestre;
2. depois, o processo pai;
3. depois, a especialização;
4. documentos de skill, auditoria, experiência ou fonte externa não podem substituir a regra normativa;
5. se a diferença alterar o resultado, o cálculo fica bloqueado até a reconciliação;
6. a reconciliação ocorre no documento de maior autoridade, e não por interpretação ad hoc do ELO.

O ELO **não escolhe a versão que parece mais conveniente**.

### 18.4 Regra de duplicação de conhecimento

Não repetir uma regra normativa em múltiplos documentos como se cada cópia fosse autoridade.

Quando uma regra precisar ser reutilizada: **referenciar a regra canônica → explicar apenas sua aplicação local → preservar o mesmo gate e a mesma terminologia.**

### 18.5 Separação entre implantação e execução

O sistema pode possuir antecipadamente views, funções, triggers, cockpit, ferramentas ELO-MCP, skills e documentação. Esses objetos representam **capacidade preparada**.

**capacidade preparada ≠ cálculo autorizado ≠ decisão tomada.**

## 19. Regra específica do ciclo de crescimento

O ciclo atual de crescimento externo possui quatro macroestados:

### Estado A — REFERÊNCIA_HISTÓRICA
`Comercial → previsão futura → reconstrução histórica → comparabilidade → GAPs`
Saída: referência histórica validada.

### Estado B — COBERTURA_E_CARGA
`referência validada → fator → cobertura por estoque/reparo/produção → necessidade adicional de fabricação → carga/capacidade/gargalos`
Saída: carga operacional e saldo de fabricação validados.

### Estado C — DEMANDA_HUMANA
`carga validada → composição funcional → produtividade → demanda humana por função`
Saída: demanda humana PCP.

### Estado D — RH
`demanda humana validada → fonte autorizada de disponibilidade/capacidade RH → confronto`
Saída: análise de fornecimento de RH.

O processo pode parar em qualquer estado. Não é permitido saltar de A para D.

## 20. Regra de fator e reparo

O fator de crescimento pertence à **demanda comparável**.

Ele não pertence ao estoque, ao reparo, à unidade física ou à quantidade de pessoas do RH.

Quando a composição funcional histórica for validada e a composição futura permanecer comparável, o fator pode ser aplicado à **demanda humana histórica correspondente**. Isso não é aplicação do fator ao quadro de RH.

Se a composição mudar, o fator global deixa de ser suficiente e a análise deve retornar à carga por produto/natureza/função.

## 21. Regra de RH

PCP calcula **demanda humana**, não disponibilidade de RH.

Sem fonte autorizada pelo domínio RH:
`DEMANDA_HUMANA = pode ser calculável quando seus gates forem satisfeitos`
`DISPONIBILIDADE_RH = não localizada`
`GAP_RH = não calculável`

## 22. Regra de fonte por camada

| Camada | Fonte/autoridade |
|---|---|
| Demanda Comercial | Comercial / tabelas comerciais governadas |
| Produto | `modelos` + `taxonomia` |
| Histórico de demanda | `mt_demanda_historico` |
| Previsão | `mt_previsoes_demanda` |
| Comparabilidade | campos e regras governados pelo PCP |
| Cobertura física | unidades modulares, reparos e produção programada conforme regra PCP |
| Carga operacional | execução/ordens e tempos validados |
| Composição funcional | evidência operacional validada |
| Produtividade | histórico validado, não hipótese |
| Demanda humana | cálculo PCP |
| Disponibilidade RH | fonte autorizada pelo domínio RH |
| Regra | GitHub |
| Estado efetivo | Supabase |
| Orquestração/interpretação | ELO |

Nenhuma camada pode substituir a autoridade de outra sem contrato explícito.

## 23. Regra para skills, auditorias e experiências

### Skills
Aplicam métodos ao processo canônico. Não redefinem o processo.

### Auditorias
Comprovam estado, estrutura, inconsistência ou evidência. Não criam regra de negócio.

### Experiências
Registram contexto e resultado. Não se tornam regra geral automaticamente.

### Fontes externas
Fornecem método ou conhecimento externo. Não se tornam fato empresarial.

Todos devem apontar para a instrução ou processo canônico quando tratarem de PCP.

## 24. Estado de governança

O objetivo é impedir que o conhecimento do PCP se transforme em um conjunto de arquivos independentes.

A unidade de conhecimento é:

**Governança PCP → Processo → Instrução → Procedimento → Evidência → ELO → Supabase → Resultado**

Essa estrutura deve ser preservada em todas as próximas implantações.
