# ELO — Skill de Orçamento

**Versão:** 1.3  
**Status:** Candidato canônico — sujeito ao Evolution Gate  
**Domínio:** Orçamento / BUDGETING  
**Setor:** Planejamento  
**Autoridade:** ELO/Governance  
**Executor especializado:** Especialista de Orçamento

## 1. Finalidade

Esta skill é uma camada de **orquestração operacional e aprendizado cognitivo** do domínio de orçamento. Ela organiza e conecta capacidades já existentes no ELO; não cria uma segunda metodologia, segundo cálculo, segundo Prompt, segundo contrato ou segunda autoridade de memória.

**Regra estrutural:** ELO orienta, aprende e audita; o Especialista de Orçamento executa a composição e a precificação.

### Fontes canônicas e precedência

A skill não reescreve regras existentes. Em caso de conflito, aplicar esta precedência:

1. documentação vigente da SO/projeto;
2. contratos e regras de Governança/Core vigentes;
3. `prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`;
4. `08-ai/ELO/DIRETRIZES/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`;
5. `04-knowledge-handbook/ELO_ESPECIALISTA_ORCAMENTO_METODOLOGIA_V2.md` e demais documentos especializados;
6. `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`;
7. esta Skill, somente como orquestração e checklist;
8. histórico/aprendizado, apenas como referência até validação.

Fontes canônicas relacionadas:
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_APRENDER_CANONICO_MASTER_PROMPT.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_CONHECIMENTO_MATURADO.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_ORCAMENTISTA_APRENDIZADO_CONTINUO.md`
- `04-knowledge-handbook/ELO_ESPECIALISTA_ORCAMENTO_METODOLOGIA_V2.md`
- `08-ai/ELO/DIRETRIZES/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`
- `08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO.md`
- `prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`
- `docs/orcamento/ELO_ORCAMENTO_EXECUTION_ARCHITECTURE.md`
- `automation/ELO_CHAT_CODEX_BRIDGE.md`

## 2. Regra anti-duplicidade

Antes de criar qualquer nova regra, cálculo, classificação, tabela, memória, trigger, executor ou mecanismo de orçamento:

1. procurar capacidade equivalente no ELO;
2. identificar o proprietário canônico existente;
3. reutilizar quando houver equivalência;
4. reconciliar quando houver sobreposição parcial;
5. criar algo novo somente quando houver lacuna comprovada;
6. registrar a relação e a justificativa da não reutilização.

Esta Skill **não é proprietária** das regras detalhadas de composição, precificação, fabricação, PTS, memória persistente ou cálculo. Ela referencia e orquestra essas capacidades.

## 3. Capacidades orquestradas

A skill deve cobrir, de forma rastreável, usando as fontes canônicas existentes:

1. **Leitura e enquadramento** — objeto, escopo, local, regime, prazo e documentos vigentes.
2. **Análise técnica-orçamentária** — requisito → solução → quantitativo → composição.
3. **Modelo/base** — identificar produto padrão, excedente e customização.
4. **Quantitativos** — extrair e conferir unidade, dimensão, área, quantidade, produtividade e duração.
5. **Composição** — material, fabricação, mão de obra interna/externa, fornecedor, transporte, mobilização e demais custos necessários.
6. **Logística** — mobilização, desmobilização, transporte, hospedagem, alimentação, combustível e deslocamentos sustentados por evidência.
7. **Premissas** — classificar origem e impacto; nunca ocultar informação não confirmada.
8. **Questionamentos/vistoria** — preferir vistoria quando a lacuna puder ser resolvida em campo.
9. **Conferência** — PTS Técnica × Orçamento.
10. **PTS Pós-Orçamento** — identificar divergências, omissões, inclusões sem origem e responsabilidades indefinidas.
11. **Aprendizado** — extrair padrões somente após validação, preservando evidência e contexto.
12. **Memória de cálculo** — preservar fórmula, parâmetros, origem, resultado e evidência sem substituir o sistema persistente.
13. **Dependências de implementação** — identificar materiais/serviços que aparecem em consequência de uma decisão técnica e explicar a função de cada dependência.
14. **Raciocínio repetitivo** — reconhecer sequências recorrentes de decisão e cálculo sem copiar cegamente o resultado histórico.
15. **Explicabilidade** — reconstruir como a solicitação foi interpretada, como cada decisão relevante foi tomada e como os principais valores foram formados.
16. **Aprendizado contínuo** — consultar conhecimento armazenado antes de compor, confrontar o caso atual e produzir revisão de aprendizado ao final de cada solicitação.

## 4. Encadeamento operacional canônico

```text
DOCUMENTAÇÃO VIGENTE
      ↓
ELO ANALISAR / ATIVA FORGE-BUDGETING-001
      ↓
CONSULTA CONHECIMENTO + MEMÓRIA EXISTENTE
      ↓
PTS TÉCNICA
      ↓
DIRECIONAMENTO / CHECKLIST
      ↓
CONTRATO DE EXECUÇÃO
      ↓
ESPECIALISTA DE ORÇAMENTO EXECUTA
      ↓
ORÇAMENTO + MEMÓRIAS DE CÁLCULO + RASTRO DE RACIOCÍNIO
      ↓
PTS PÓS-ORÇAMENTO
      ↓
RESOLUÇÃO DOS INDICADORES CANÔNICOS
      ↓
ELO CONFERE
   ├─ OK → fechamento
   └─ CONTESTAÇÃO → Especialista corrige → nova conferência
      ↓
EXPLICAÇÃO DE COMO FOI ORÇADO
      ↓
REVISÃO DE APRENDIZADO DA SO (>= 10 QUESTÕES AO OWNER)
      ↓
APRENDIZADO CANDIDATO
      ↓
VALIDAÇÃO / GOVERNANÇA
      ↓
MEMÓRIA COGNITIVA E ESTRUTURAS PERSISTENTES CANÔNICAS
```

A Skill não executa composição/precificação em paralelo ao Especialista e não grava diretamente em memória canônica fora do fluxo autorizado.

## 5. Regras de decisão

- Usar documentação vigente antes de histórico.
- Histórico serve para comparação e aprendizado, nunca substitui requisito atual.
- Não inventar preço, quantidade, dimensão, produtividade, prazo, responsabilidade ou condição de execução.
- Conflitos devem ser explicitados, não resolvidos silenciosamente.
- Produto padrão não deve ser tratado como item especial sem evidência de desvio.
- Excedente deve registrar requisito, padrão, alteração, quantidade, material, mão de obra, impacto e preço, conforme a regra canônica aplicável.
- Toda precificação relevante deve manter origem identificável.
- Premissa crítica deve gerar pendência/questionamento quando alterar materialmente custo ou atendimento.
- Resultado de uma única SO não vira regra geral sem validação.
- Dependência recorrente não deve ser incluída automaticamente: primeiro verificar se a condição técnica que a exige está presente.
- Conhecimento armazenado deve ser consultado antes de desenvolver solução nova, mas nunca aplicado sem teste de equivalência com a SO atual.
- Pergunta de aprendizado não equivale a permissão de promover ou alterar regra permanente.

## 6. Contrato de aprendizado

O aprendizado de orçamento deve separar:

`DADO → CÁLCULO → PREMISSA → EVIDÊNCIA → HIPÓTESE → PADRÃO → VALIDAÇÃO → REGRA`

Uma regra candidata deve conter:

`REGRA | CONTEXTO | APLICAÇÃO | EXCEÇÃO | EVIDÊNCIA | RISCO | STATUS`

Status permitidos:
- `OBSERVADO`
- `CANDIDATO`
- `VALIDADO`
- `REJEITADO`
- `SUPERADO`

Somente `VALIDADO` pode alimentar regra permanente, e ainda assim pelo mecanismo canônico de memória/governança.

## 7. Relação com a memória persistente

A skill não cria memória paralela. Os registros de orçamento devem utilizar as estruturas canônicas existentes, incluindo:

- `elo_orcamento_memoria`;
- `elo_orcamento_calculos_aprendidos`;
- `elo_orcamento_calculo_varreduras`;
- `elo_orcamento_calculo_evidencias`;
- `elo_orcamento_calculo_similaridades`;
- `elo_orcamento_decisoes`;
- `elo_orcamento_associacoes`.

O `ELO_MEMORIA_ORCAMENTOS.md` é camada textual de contexto/índice e não substitui a persistência estruturada nem cria uma nova autoridade.

## 8. Fail-closed

Bloquear ou marcar como não confirmado quando houver:

- evidência ausente para requisito crítico;
- cálculo sem parâmetros suficientes;
- origem de custo não demonstrável;
- conflito documental não resolvido;
- responsabilidade indefinida com impacto material;
- tentativa de transformar experiência isolada em regra;
- segredo/token/chave em evidência ou proveniência;
- tentativa de alterar memória canônica fora do fluxo autorizado;
- divergência entre PTS Técnica, orçamento e PTS Pós sem explicação/arbitragem;
- tentativa de tratar resposta do owner como promoção automática de conhecimento.

## 9. Critério de qualidade

A execução só é considerada rastreável quando cada custo relevante puder responder:

`POR QUE → DE ONDE → COMO → QUANTO → PREMISSA → RISCO → VALIDAÇÃO`

E o orçamento concluído deve conseguir responder:

`O QUE FOI PEDIDO → O QUE FOI ENTENDIDO → O QUE FOI ESCOLHIDO → POR QUE → COMO FOI CALCULADO → DE ONDE VEIO O PREÇO → COMO CHEGOU AO VALOR → O QUE A PTS PÓS REVELOU → O QUE FOI APRENDIDO`

## 10. Potencialização para o ELO

Esta skill transforma o domínio de orçamento em uma capacidade estruturada de raciocínio operacional **sem duplicar capacidades existentes**: conecta requisito, solução, composição, custo, evidência, decisão, resultado pós-orçamento e aprendizado, mantendo a autoridade nas estruturas canônicas já existentes.

## 11. Regra de manutenção

Se uma fonte canônica posterior incorporar uma regra atualmente descrita nesta Skill, remover a duplicação desta Skill e manter somente a referência/ponte operacional. A Skill deve permanecer fina, estável e orientada à coordenação do processo.

## 12. Gatilho cognitivo `ELO APRENDER`

Quando o usuário disser `ELO APRENDER` durante ou após um orçamento, esta Skill deve recuperar o contrato canônico de aprendizado e executar a varredura cognitiva do caso atual.

O objetivo não é memorizar o valor final. O objetivo é reconstruir e preservar:

```text
CONDIÇÃO / REQUISITO
→ INTERPRETAÇÃO
→ DECISÃO TÉCNICA
→ MODELO / SOLUÇÃO
→ QUANTITATIVO
→ DEPENDÊNCIAS DE IMPLEMENTAÇÃO
→ FÓRMULA / SUBCÁLCULO
→ PREÇO UNITÁRIO E ORIGEM
→ CUSTO
→ VALIDAÇÃO
→ APLICABILIDADE
→ EXCEÇÕES
→ PADRÃO CANDIDATO
```

Para cada etapa, registrar origem, unidade, premissa, evidência e confiança.

### 12.1 O que deve ser aprendido

O ELO deve procurar principalmente:

- decisões repetidas;
- cálculos repetidos;
- relações condicionais entre materiais;
- relações entre solução técnica e itens de instalação;
- critérios de escolha de produto/modelo;
- fatores de conversão;
- arredondamentos;
- perdas e sobras quando comprovadas;
- produtividade de mão de obra;
- sequência de execução que altera a composição;
- itens que sempre devem ser verificados quando determinada solução é adotada;
- diferenças que explicam por que dois casos semelhantes receberam composições diferentes.

### 12.2 Não aprender somente o número

É proibido consolidar uma memória como apenas:

`CONTÊINER 20 PÉS = 19 PAINÉIS`

A forma correta é registrar a lógica que produziu o quantitativo, por exemplo:

`TIPO/GEOMETRIA DO CONTÊINER + SUPERFÍCIES A REVESTIR + DIMENSÃO ÚTIL DO PAINEL + ABERTURAS/RECORTES + REGRA DE ARREDONDAMENTO → PAINÉIS DE PAREDE + PAINÉIS DE TETO`

Se a fórmula geométrica não estiver evidenciada, preservar o quantitativo observado e abrir `GAP_FORMULA_QUANTITATIVO`.

## 13. Padrões condicionais e dependências

A Skill deve aprender relações do tipo:

`SE condição técnica X estiver presente → VERIFICAR componente/serviço Y`

Não transformar automaticamente em:

`SE X → INCLUIR Y`

A inclusão só ocorre depois de validar a condição no orçamento atual.

Exemplo já reconhecido pela memória do domínio:

`PAINEL PIR → VERIFICAR GUIA U / PERFIS DE FIXAÇÃO E ACABAMENTO`

A função, dimensão, metragem, preço e necessidade do perfil devem ser validadas no caso atual.

## 14. Exemplo operacional em aprendizado — contêiner 20 pés com PIR 32 mm

Experiência operacional fornecida pelo owner do processo em 2026-10-30:

```text
CONTÊINER 20 PÉS PADRÃO
+ FORRAÇÃO EM PAINEL PIR 32 MM
→ referência observada: 14 painéis de parede
→ referência observada: 5 painéis de teto
→ total observado: 19 painéis
```

Status inicial: `CANDIDATO`.

Esta referência **não é uma regra universal** enquanto não forem reconstruídos/confirmados os parâmetros que explicam o quantitativo, incluindo dimensões úteis dos painéis, geometria, recortes, aberturas, perdas e arredondamentos aplicáveis.

Ao encontrar novo orçamento equivalente, o ELO deve:

1. identificar se é realmente contêiner 20 pés e qual configuração;
2. validar se a forração é PIR 32 mm e quais superfícies serão revestidas;
3. recuperar casos/cálculos similares;
4. recomputar ou confrontar o quantitativo;
5. verificar dependências de instalação, incluindo guia U/perfis quando aplicáveis;
6. buscar preço unitário vigente na fonte autorizada;
7. calcular custo de material e mão de obra sem reutilizar preço histórico como preço atual;
8. comparar observado × calculado;
9. registrar divergência se houver;
10. elevar confiança apenas com recorrência/evidência.

## 15. Cognição lógica do Orçamentista

Para cada item relevante, a Skill deve produzir internamente o seguinte mapa:

| Etapa | Pergunta cognitiva |
|---|---|
| Requisito | O que foi pedido? |
| Padrão | Isso já existe no produto/modelo padrão? |
| Solução | Qual solução técnica atende? |
| Quantidade | Como o quantitativo foi obtido? |
| Dependências | O que essa solução exige para ser instalada/funcionar? |
| Origem | De onde veio cada parâmetro? |
| Custo | Qual preço unitário vigente e qual fórmula de custo? |
| Comparação | Existe caso anterior realmente equivalente? |
| Divergência | O que mudou e por quê? |
| Aprendizado | O que pode ser reutilizado como método, condição ou alerta? |

A saída cognitiva desejada é:

`REQUISITO → RACIOCÍNIO → DECISÃO → COMPOSIÇÃO → CUSTO → EVIDÊNCIA → APRENDIZADO`

## 16. Ativação automática no início da solicitação

Ao iniciar `ELO ANALISAR`, a Skill `FORGE-BUDGETING-001` deve ser ativada automaticamente e permanecer ativa até o fechamento da solicitação.

No início deve consultar:

`DOCUMENTO VIGENTE → CONHECIMENTO CANÔNICO NO GIT → MEMÓRIA ORÇAMENTÁRIA NO SUPABASE → PRECEDENTES/SIMILARIDADES → GAPS/CONFLITOS`

O objetivo é aprimorar continuamente a análise com conhecimento armazenado sem transformar memória histórica em origem do caso atual.

## 17. PTS Técnica + Orçamento + PTS Pós + indicadores

A Skill deve compreender a elaboração como uma cadeia única de explicação, preservando as funções distintas de cada artefato:

`PTS TÉCNICA → DECISÃO TÉCNICA → ORÇAMENTO → PTS PÓS-ORÇAMENTO → INDICADORES → VALIDAÇÃO → APRENDIZADO`

Na PTS Pós devem ser interpretados, quando aplicáveis, os indicadores canônicos:

- Conhecimento;
- Flexibilidade;
- Risco;
- Decisão.

A resolução desses indicadores deve responder **por que o orçamento ficou daquela forma**, quais elementos estavam sustentados por conhecimento, quais poderiam ser alterados, quais riscos condicionaram as escolhas e qual decisão foi tomada.

## 18. Explicação por fase e formação dos valores

No fechamento da solicitação, a Skill deve ser capaz de descrever:

1. como leu e interpretou o requisito;
2. quais alternativas foram consideradas;
3. qual solução/modelo foi adotado e por quê;
4. como cada quantitativo material foi obtido;
5. quais dependências surgiram da solução;
6. de onde veio cada preço unitário relevante;
7. como quantidade, preço, mão de obra, logística, indiretos e demais componentes formaram o valor;
8. o que a PTS Pós confirmou, contestou ou deixou pendente;
9. como os indicadores canônicos influenciaram a decisão;
10. o que pode ser aprendido e o que deve permanecer específico do caso.

## 19. Revisão de aprendizado obrigatória — 10 ou mais questões

Ao fim de **cada solicitação**, a Skill deve retornar ao owner um bloco `REVISÃO DE APRENDIZADO DA SO` com **no mínimo 10 questões específicas do caso**.

As perguntas devem buscar decidir o que merece ser integrado à Skill/conhecimento e devem trazer, para cada questão:

`ID | PERGUNTA | POR QUE IMPORTA | EVIDÊNCIA ATUAL | PROPOSTA DE INTEGRAÇÃO | STATUS`

O piso é 10 perguntas; se houver mais aprendizados materialmente relevantes, retornar todas as questões necessárias.

As respostas do owner devem ser confrontadas com evidência e classificadas como `CASE`, `PRECEDENT`, `LEARNING_CANDIDATE` ou `VALIDATED_LEARNING`, conforme governança. Nenhuma resposta promove conhecimento automaticamente ao Core.

O contrato detalhado desta etapa está em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_ORCAMENTISTA_APRENDIZADO_CONTINUO.md`
