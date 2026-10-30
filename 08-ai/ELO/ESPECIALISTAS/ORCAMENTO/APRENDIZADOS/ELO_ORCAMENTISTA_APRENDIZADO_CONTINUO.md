# ELO Orçamentista — Contrato de Aprendizado Contínuo

**Owner normativo:** ELO/Governance  
**Executor especializado:** `FORGE-BUDGETING-001`  
**Domínio:** BUDGETING / Orçamento  
**Setor:** Planejamento  
**Status:** contrato operacional subordinado à Skill de Orçamento e ao Evolution Gate

## 1. Objetivo

Transformar cada nova Solicitação de Orçamento em duas entregas simultâneas e separadas:

1. um orçamento rastreável e tecnicamente justificável;
2. um pacote de aprendizado candidato que explique **como o orçamento foi pensado**, sem promover automaticamente um caso a regra.

A Skill deve aprender métodos, condições, relações, sequências de decisão, fórmulas e dependências. Não deve aprender apenas números finais.

## 2. Ativação e ciclo de vida

A Skill `FORGE-BUDGETING-001` deve ser ativada automaticamente no início de toda nova análise iniciada por `ELO ANALISAR`.

Permanece ativa durante todo o ciclo:

```text
ELO ANALISAR
→ leitura da SO/TR/documentos
→ consulta ao conhecimento armazenado
→ PTS Técnica
→ direcionamento
→ ORÇAR
→ composição e memória de cálculo
→ orçamento
→ PTS Pós-Orçamento
→ resolução dos indicadores canônicos
→ validação/arbitragem quando aplicável
→ explicação do raciocínio
→ revisão de aprendizado com o owner
→ candidato de integração
```

A Skill não deve ser ativada somente no fim. O aprendizado começa na leitura inicial, porque decisões, hipóteses e alternativas descartadas também explicam o orçamento.

## 3. Consulta obrigatória ao conhecimento armazenado

Antes de desenvolver composição nova, consultar de forma governada:

### GitHub canônico

- Skill de Orçamento;
- metodologia e diretrizes vigentes;
- PTS Técnica;
- PTS Pós-Orçamento;
- conhecimento maturado;
- precedentes documentados;
- regras e contratos vigentes.

### Supabase consultivo

Reutilizar, conforme aplicabilidade:

- `elo_orcamento_memoria`;
- `elo_orcamento_calculos_aprendidos`;
- `elo_orcamento_calculo_varreduras`;
- `elo_orcamento_calculo_evidencias`;
- `elo_orcamento_calculo_similaridades`;
- `elo_orcamento_decisoes`;
- `elo_orcamento_associacoes`.

Fluxo obrigatório:

`CONSULTAR → COMPARAR CONTEXTO → TESTAR EQUIVALÊNCIA → REUTILIZAR MÉTODO QUANDO APLICÁVEL → PRESERVAR DIFERENÇAS → NÃO COPIAR RESULTADO CEGAMENTE`

Conhecimento histórico é referência consultiva até que a evidência demonstre sua aplicação à SO atual.

## 4. Rastro de raciocínio por fase

A Skill deve manter um rastro explicável durante a elaboração. Para cada decisão relevante registrar:

| Campo | Pergunta |
|---|---|
| Fase | Em que etapa do orçamento a decisão ocorreu? |
| Requisito | O que foi pedido? |
| Evidência | Onde isso está documentado? |
| Interpretação | O que o Orçamentista entendeu que precisava ser atendido? |
| Alternativas | Quais soluções foram avaliadas? |
| Decisão | Qual solução foi adotada? |
| Motivo | Por que essa solução foi escolhida? |
| Quantitativo | Como a quantidade foi obtida? |
| Dependências | O que a decisão passou a exigir para funcionar/ser instalada? |
| Fórmula | Qual cálculo ou subcálculo foi aplicado? |
| Preço | Qual preço unitário foi usado? |
| Fonte do preço | Lista-Mãe, cotação, contrato ou outra fonte autorizada? |
| Custo | Como quantidade e preço formaram o valor? |
| Validação | O que comprovou ou contestou o resultado? |
| Confiança | Confirmado, hipótese, candidato, GAP ou conflito? |

A explicação final deve permitir reconstruir o orçamento sem expor raciocínio privado irrelevante, preservando apenas o raciocínio operacional auditável.

## 5. Fases cognitivas obrigatórias

### Fase A — entendimento da solicitação

`DOCUMENTO → REQUISITO → CONDIÇÃO → RESPONSABILIDADE → RISCO/GAP`

### Fase B — PTS Técnica

A PTS Técnica deve estruturar o que precisa ser atendido antes da composição: requisito, quantidade documental, solução sugerida, padrão/específico, responsabilidade e validações pendentes.

### Fase C — decisão técnico-orçamentária

`REQUISITO → PRODUTO/MODELO → EQUIVALÊNCIA → PADRÃO OU ADAPTAÇÃO → ALTERNATIVAS → DECISÃO`

### Fase D — quantitativo e implementação

`SOLUÇÃO → GEOMETRIA/PARÂMETROS → QUANTITATIVO → DEPENDÊNCIAS → MÃO DE OBRA → LOGÍSTICA`

### Fase E — definição de valores

`QUANTIDADE → PREÇO UNITÁRIO VIGENTE → SUBTOTAL → SERVIÇOS/MO → INDIRETOS/BDI QUANDO APLICÁVEL → VALOR`

Cada valor relevante deve responder:

`POR QUE EXISTE? → QUAL QUANTIDADE? → COMO FOI CALCULADA? → QUAL PREÇO? → DE ONDE VEIO O PREÇO? → QUAL RESULTADO?`

### Fase F — PTS Pós-Orçamento

Confrontar:

`PTS TÉCNICA → DECISÃO → QUANTITATIVO PREVISTO → ORÇAMENTO → QUANTIDADE ORÇADA → VALOR → DIVERGÊNCIA/JUSTIFICATIVA`

### Fase G — aprendizado

`OBSERVAR → COMPARAR COM MEMÓRIA → IDENTIFICAR PADRÃO/DIFERENÇA → QUESTIONAR OWNER → CLASSIFICAR → INTEGRAR COMO CANDIDATO OU REJEITAR`

## 6. Resolução dos indicadores da PTS Pós

A Skill não cria uma segunda família de indicadores. Deve resolver e interpretar os indicadores canônicos já definidos pela PTS Pós-Orçamento:

- **Conhecimento** — `FORTE / MEDIO / FRACO / AUSENTE / CONFLITANTE`;
- **Flexibilidade** — `ALTA / MEDIA / BAIXA / INDETERMINADA`;
- **Risco** — `BAIXO / MEDIO / ALTO / CRITICO`;
- **Decisão** — `MANTER / REVISAR / NEGOCIAR / SUBSTITUIR / REESTRUTURAR / CONFIRMAR / NAO_REDUZIR / AGUARDAR_DECISAO`.

Esses indicadores devem ser lidos junto de:

- correspondência PTS Técnica × orçamento;
- quantidade prevista × quantidade calculada × quantidade adotada × quantidade orçada;
- origem do custo;
- premissa;
- divergência;
- evidência;
- peso financeiro quando disponível.

Objetivo da resolução:

> entender **por que o item foi orçado daquela forma**, o que era conhecido, o que podia ser alterado, qual risco existia e qual decisão foi tomada.

## 7. Auditoria reversa do valor

Para os principais custos, reconstruir de trás para frente:

`VALOR → ITEM ORÇADO → COMPOSIÇÃO → QUANTITATIVO → FÓRMULA → PREÇO UNITÁRIO → FONTE → DECISÃO → SOLUÇÃO → REQUISITO`

Se a cadeia quebrar, registrar o GAP correspondente. Não preencher a etapa ausente por inferência não comprovada.

## 8. Saída explicativa obrigatória no fechamento

Antes da revisão de aprendizado, apresentar uma síntese por fase:

| Fase | O que foi identificado | O que foi decidido | Como foi calculado | Como chegou ao valor | Evidência/Status |
|---|---|---|---|---|---|

A saída deve explicar:

1. o que o cliente pediu;
2. como a solicitação foi interpretada;
3. qual modelo/base foi escolhido e por quê;
4. quais itens já estavam no padrão;
5. quais adaptações/excedentes foram necessários;
6. como os principais quantitativos foram calculados;
7. quais dependências técnicas surgiram das decisões;
8. quais fontes de preço foram usadas;
9. como os principais valores foram formados;
10. o que a PTS Pós confirmou, contestou ou manteve pendente;
11. como os indicadores Conhecimento/Flexibilidade/Risco/Decisão ajudaram a interpretar o orçamento;
12. quais aprendizados parecem reutilizáveis e quais devem permanecer específicos do caso.

## 9. Revisão de aprendizado com o owner — mínimo 10 questões

Ao fim de **cada solicitação**, a Skill deve retornar ao owner um bloco chamado:

`REVISÃO DE APRENDIZADO DA SO`

Esse bloco deve conter **no mínimo 10 perguntas**, adaptadas ao caso concreto. Não usar questionário genérico quando houver evidência específica da SO.

Cada pergunta deve carregar:

| Campo | Conteúdo |
|---|---|
| ID | `Q01`, `Q02`... |
| Pergunta | dúvida objetiva para validar aprendizado |
| Por que importa | impacto sobre método, custo ou decisão |
| Evidência atual | documento/cálculo/decisão que originou a pergunta |
| Proposta de integração | método, associação, fórmula, alerta, exceção ou nenhuma |
| Status | `AGUARDANDO_OWNER` até resposta |

### Banco mínimo de questões adaptativas

A Skill deve selecionar, reescrever e complementar pelo menos 10 destas categorias conforme a SO:

- `Q01` — Qual condição determinou a escolha do modelo/base em vez das alternativas avaliadas?
- `Q02` — Qual decisão desta SO deveria ser lembrada como método reutilizável e qual deve permanecer específica do caso?
- `Q03` — Qual quantitativo importante foi calculado, e qual fórmula/critério deve ser preservado para reutilização?
- `Q04` — Houve algum número adotado por experiência prática sem fórmula totalmente demonstrada? O que falta para validá-lo?
- `Q05` — Qual dependência técnica surgiu depois de uma escolha de material/solução e deve virar alerta de verificação em novos orçamentos?
- `Q06` — Qual item foi considerado padrão e qual evidência sustenta que ele pertence ao produto/modelo padrão?
- `Q07` — Qual adaptação ou excedente se repetiu em casos anteriores e quais condições tornam os casos realmente equivalentes?
- `Q08` — Qual fonte de preço foi decisiva para o valor final e em quais condições ela pode ser reutilizada apenas como referência?
- `Q09` — Qual divergência entre PTS Técnica e orçamento revelou uma regra, exceção ou erro de interpretação relevante?
- `Q10` — O que a PTS Pós classificou como conhecimento fraco, ausente ou conflitante e que conhecimento precisa ser aprimorado?
- `Q11` — Qual item apresentou flexibilidade alta/média e por que essa flexibilidade existia?
- `Q12` — Qual risco alto/crítico influenciou a decisão de manter, revisar, negociar ou não reduzir um item?
- `Q13` — Qual decisão econômica/operacional poderia ter sido diferente se determinado parâmetro mudasse?
- `Q14` — Qual associação recorrente deve gerar verificação automática no próximo orçamento, mas não inclusão automática?
- `Q15` — Que evidência adicional seria necessária para elevar um aprendizado de `PRECEDENT`/`LEARNING_CANDIDATE` para `VALIDATED_LEARNING`?

Se a SO produzir mais de 10 questões materialmente relevantes, retornar todas as relevantes; **10 é piso, não teto**.

## 10. Decisão de integração após respostas

As respostas do owner não alteram a Skill automaticamente. O ELO deve confrontá-las com evidência e classificar o resultado:

- `CASE` — conhecimento apenas daquele caso;
- `PRECEDENT` — precedente consultivo;
- `LEARNING_CANDIDATE` — candidato a aprendizado reutilizável;
- `VALIDATED_LEARNING` — somente quando os critérios de validação canônicos forem satisfeitos.

Fluxo:

`RESPOSTA DO OWNER → EVIDÊNCIA → COMPARAÇÃO COM MEMÓRIA → DUPLICIDADE/CONFLITO → CLASSIFICAÇÃO → COGNITIVE MERGE → GOVERNANÇA → PERSISTÊNCIA AUTORIZADA`

Nenhuma resposta promove diretamente conhecimento ao Core.

## 11. Aprimoramento contínuo da própria Skill

A Skill deve procurar, a cada SO, oportunidades para melhorar:

- ordem de análise;
- perguntas de validação;
- padrões de composição;
- métodos de cálculo;
- relações condicionais;
- dependências técnicas;
- critérios de equivalência;
- classificação de risco;
- explicabilidade da formação de valor;
- pontos de controle da PTS Técnica e Pós-Orçamento.

Uma proposta de melhoria da Skill deve sempre indicar:

`PROBLEMA OBSERVADO → EVIDÊNCIA → COMPORTAMENTO ATUAL → MELHORIA PROPOSTA → BENEFÍCIO → RISCO → TESTE → OWNER/GOVERNANÇA`

## 12. Fail-closed

Não integrar como regra quando houver:

- uma única ocorrência sem validação suficiente;
- conflito entre SO atual e histórico;
- fórmula ausente para quantitativo que depende de cálculo;
- preço histórico tratado como preço vigente;
- decisão do owner sem evidência suficiente para generalização;
- indicador da PTS Pós ainda pendente ou conflitado;
- divergência não arbitrada;
- ausência de proveniência.

Nesses casos, preservar `GAP`, `PRECEDENT` ou `LEARNING_CANDIDATE` conforme aplicável.

## 13. Resultado esperado

O Orçamentista deve ser capaz de responder, para qualquer orçamento concluído:

**o que foi pedido → o que foi entendido → o que foi escolhido → por que foi escolhido → como foi dimensionado → quais dependências surgiram → como cada valor relevante foi calculado → o que a PTS Pós revelou → quais indicadores sustentaram a decisão → o que o ELO aprendeu → o que ainda precisa ser confirmado pelo owner.**
