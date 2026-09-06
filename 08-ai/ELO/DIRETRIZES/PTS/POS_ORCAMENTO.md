# PTS Técnica Pós-Orçamento — Estrutura Padrão do ELO

**Versão:** 1.1  
**Status:** Oficial  
**Responsável:** ELO

## 1. Finalidade

A PTS Técnica Pós-Orçamento comprova a aderência entre o Termo de Referência, demais documentos da solicitação e a composição orçamentária efetivamente elaborada.

Seu objetivo principal é garantir rastreabilidade: cada requisito técnico relevante deve ser relacionado ao(s) item(ns) do orçamento que o atende(m), indicando a forma de atendimento, evidência, responsabilidade e eventual solução equivalente.

A PTS Pós não deve repetir simplesmente a PTS pré-orçamento. Ela deve comprovar o que efetivamente foi contemplado na composição final e, quando aplicável, analisar a concentração econômica e as oportunidades de revisão de valor sem romper a aderência técnica.

## 2. Estrutura obrigatória

A PTS Pós-Orçamento deve seguir, quando aplicável, esta sequência:

1. Identificação da Solicitação;
2. Objetivo;
3. Escopo Técnico;
4. Matriz Técnica de Comprovação de Atendimento;
5. Análise Geral da Composição Orçamentária;
6. Análise de Competitividade;
7. Resumo Executivo;
8. Parecer Técnico;
9. Parecer de Competitividade;
10. Legenda.

## 3. Matriz Técnica de Comprovação de Atendimento

A matriz deve conter, no mínimo:

| Campo | Finalidade |
|---|---|
| Item TR | Identificar o requisito de origem |
| Trecho do TR | Registrar a referência documental |
| Exigência Técnica | Descrever o que deve ser atendido |
| Item(s) do Orçamento | Rastrear a composição correspondente |
| Atendimento | AI, AE, AP ou NA |
| Evidência Técnica | Explicar como o orçamento atende |
| Responsabilidade | Indicar responsável pela execução/fornecimento |

Quando necessário, podem ser acrescentados campos de quantidade, unidade, premissa, observação, documento de evidência ou risco.

## 4. Classificação de atendimento

- **AI — Atendido Integralmente:** requisito plenamente contemplado na composição.
- **AE — Atendido por Solução Equivalente:** requisito atendido por solução tecnicamente equivalente, devendo a equivalência estar justificada.
- **AP — Atendido Parcialmente:** requisito contemplado somente em parte ou dependente de complementação.
- **NA — Não Atendido:** requisito não contemplado na composição.

A classificação não deve ser utilizada para mascarar ausência de item. Quando houver dúvida sobre equivalência ou aceite contratual, registrar a condição explicitamente.

## 5. Rastreabilidade do orçamento

O Especialista deve identificar o(s) item(ns) da planilha que comprovam o atendimento de cada requisito relevante.

Não é suficiente afirmar que um sistema está contemplado por uma verba global quando a composição disponível não permite demonstrar esse atendimento.

Quando uma verba global for utilizada como evidência, a PTS deve explicar o conteúdo técnico abrangido por ela.

## 6. Soluções equivalentes

Toda solução equivalente deve informar:

- requisito original;
- solução adotada;
- justificativa técnica;
- desempenho/funcionalidade preservados;
- eventual necessidade de aprovação do cliente.

A classificação **AE** não significa automaticamente que o cliente aceitou a solução. Quando o aceite for necessário, registrar essa condição.

## 7. Análise Geral da Composição Orçamentária

Após a matriz, apresentar uma síntese objetiva da solução efetivamente orçada, incluindo:

- módulo/equipamento base;
- adaptações;
- sistemas;
- infraestrutura;
- instalações;
- logística;
- projetos;
- documentação;
- comissionamento;
- demais componentes relevantes.

A análise deve destacar as principais soluções equivalentes, adaptações especiais e premissas que tenham impacto técnico ou comercial.

## 8. Análise de Competitividade

A camada **ELO.PTS_POS.COMPETITIVIDADE** deve ser executada sobre a composição orçamentária final quando houver dados suficientes para análise.

### 8.1 Curva ABC

Calcular o peso financeiro de cada item:

`peso = valor_item / valor_total_orcamento`

Ordenar os itens por valor decrescente, calcular o acumulado e classificar em **A/B/C** usando os limites parametrizados do contrato operacional. A Curva ABC estabelece prioridade de análise econômica; não autoriza redução automática.

### 8.2 Prioridade de análise

A análise deve priorizar, nesta ordem lógica:

1. concentração financeira;
2. excedentes e **Nome Material**;
3. memória de cálculo;
4. evidência e conhecimento disponível;
5. flexibilidade técnica/comercial;
6. risco da alteração;
7. oportunidade potencial.

### 8.3 Excedentes e Nome Material

Para excedentes, preservar a rastreabilidade:

`EXCEDENTE → CATEGORIA → NOME MATERIAL → QUANTIDADE → VALOR UNITÁRIO → VALOR TOTAL → COMPOSIÇÃO → FONTE → MEMÓRIA DE CÁLCULO`

O **Nome Material** é tratado como camada semântica de análise e rastreabilidade, não como segunda identidade de material.

### 8.4 Estados

**Conhecimento:** `FORTE | MEDIO | FRACO | AUSENTE | CONFLITANTE`

**Flexibilidade:** `ALTA | MEDIA | BAIXA | INDETERMINADA`

**Risco:** `BAIXO | MEDIO | ALTO | CRITICO`

**Recomendação:** `MANTER | REVISAR | NEGOCIAR | SUBSTITUIR | REESTRUTURAR | CONFIRMAR | NAO_REDUZIR | AGUARDAR_DECISAO`

### 8.5 Oportunidade

Uma oportunidade só pode ser apresentada quando houver fundamento verificável. Para cada oportunidade registrar:

- item e classe ABC;
- peso financeiro;
- origem do valor;
- memória de cálculo;
- conhecimento relacionado;
- evidências;
- flexibilidade;
- impacto econômico;
- risco;
- recomendação;
- responsável pela decisão.

Ausência de evidência não autoriza redução. Conhecimento conflitante exige preservação de proveniência e arbitragem.

### 8.6 Cenários

Quando houver dados suficientes, apresentar:

- **BASE:** composição original;
- **COMPETITIVO:** somente oportunidades apoiadas por evidência e viabilidade;
- **MÁXIMO:** limite analítico das oportunidades tecnicamente possíveis, com riscos e premissas explícitos.

Cada cenário deve informar valor total, variação absoluta, variação percentual, itens alterados, premissas alteradas e risco.

### 8.7 Autoridade e governança

O fluxo obrigatório é:

`ANÁLISE → RECOMENDAÇÃO → ARBITRAGEM → DECISÃO`

A camada não altera automaticamente o orçamento, a Lista-Mãe, o conhecimento canônico, o Core ou a Soul.

O ELO analisa, ordena, confronta evidências, identifica riscos e recomenda. O Especialista de Orçamento permanece responsável pela composição técnica. A decisão final permanece com o responsável competente.

### 8.8 Não manipulação

A análise de competitividade é interna. Não fabricar, distorcer ou selecionar artificialmente referências para atingir um preço desejado. Toda referência externa deve preservar fonte, condição de comparação, premissa e memória de cálculo.

## 9. Resumo Executivo

Apresentar quantitativamente:

- itens técnicos analisados;
- AI;
- AE;
- AP;
- NA;
- índice de atendimento ao TR;
- itens Classe A prioritários;
- oportunidades de competitividade;
- riscos relevantes;
- decisões pendentes.

O índice de atendimento só deve ser apresentado como percentual quando a metodologia de contagem estiver claramente definida.

## 10. Parecer Técnico

O parecer deve concluir sobre a aderência técnica da composição orçamentária ao TR, considerando a matriz de comprovação.

A conclusão deve distinguir:

- atendimento integral;
- atendimento por equivalência;
- atendimento parcial;
- não atendimento;
- pendências que impeçam afirmar conformidade plena.

Não declarar 100% de atendimento quando existirem requisitos classificados como AP, NA ou equivalências ainda dependentes de aceite.

## 11. Parecer de Competitividade

O parecer de competitividade deve responder:

`QUAIS ITENS CONCENTRAM VALOR → QUAIS TÊM FUNDAMENTO PARA REVISÃO → QUAL IMPACTO → QUAL RISCO → QUAL DECISÃO É NECESSÁRIA`

Não converter a análise automaticamente em redução de preço.

As recomendações devem ser classificadas como **MANTER**, **REVISAR**, **NEGOCIAR**, **SUBSTITUIR**, **REESTRUTURAR**, **CONFIRMAR**, **NAO_REDUZIR** ou **AGUARDAR_DECISAO**.

## 12. Evidência e origem

A PTS Pós deve preservar a origem das informações utilizadas na comprovação e na análise:

- TR/SO;
- projeto/layout;
- composição orçamentária;
- premissa interna;
- solução de engenharia;
- fornecedor;
- vistoria;
- confirmação do cliente;
- memória de cálculo;
- conhecimento aplicável.

Quando a evidência não estiver disponível, registrar a limitação em vez de inventá-la.

## 13. Relação com a PTS Pré-Orçamento

A PTS Pós deve permitir comparar:

**o que foi identificado antes do orçamento → o que foi efetivamente orçado → como foi atendido → quais efeitos econômicos foram identificados após a composição.**

Divergências relevantes entre a análise pré e pós devem ser registradas, especialmente:

- itens excluídos;
- itens acrescentados;
- alterações de quantitativo;
- substituições;
- soluções equivalentes;
- premissas alteradas;
- itens que permaneceram pendentes;
- oportunidades de revisão de valor.

## 14. Relação com aprendizado

O resultado de uma revisão de competitividade pode gerar evidência para aprendizado somente após avaliação governada.

`ORÇAMENTO → ANÁLISE → DECISÃO → RESULTADO DA LICITAÇÃO → AVALIAÇÃO → LEARNING CANDIDATE → GOVERNED LEARNING`

O ELO não aprende apenas o preço vencedor ou o valor reduzido; aprende a relação entre contexto, premissas, composição, decisão, resultado e evidência.

## 15. Regra de governança do ELO

A PTS Pós-Orçamento é documento de comprovação, rastreabilidade e, quando aplicável, análise econômica de competitividade. O Especialista de Orçamento executa a análise detalhada; o ELO garante que a estrutura preserve a visão gerencial e que nenhuma conclusão técnica ou recomendação econômica seja apresentada sem evidência suficiente.

Novas melhorias identificadas durante análises de SO devem ser propostas ao ELO para classificação como SO-específica, especialista, global ou experimental antes de serem incorporadas permanentemente.
