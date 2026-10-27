# ELO — Skill de Orçamento

**Versão:** 1.2  
**Status:** Candidato canônico — sujeito ao Evolution Gate  
**Domínio:** Orçamento  
**Autoridade:** ELO/Governance  
**Executor especializado:** Especialista de Orçamento

## 1. Finalidade

Esta skill é uma camada de **orquestração operacional** do domínio de orçamento. Ela organiza e conecta capacidades já existentes no ELO; não cria uma segunda metodologia, segundo cálculo, segundo Prompt, segundo contrato ou segunda autoridade de memória.

**Regra estrutural:** ELO orienta e audita; o Especialista de Orçamento executa a composição e a precificação.

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
- `04-knowledge-handbook/ELO_ESPECIALISTA_ORCAMENTO_METODOLOGIA_V2.md`
- `08-ai/ELO/DIRETRIZES/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`
- `08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO.md`
- `prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`
- `docs/orcamento/ELO_ORCAMENTO_EXECUTION_ARCHITECTURE.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/CATALOGO_SERVICOS_ITENS_RECORRENTES.md`

## 2. Regra anti-duplicidade

Antes de criar qualquer nova regra, cálculo, classificação, tabela, memória, trigger, executor ou mecanismo de orçamento:

1. procurar capacidade equivalente no ELO;
2. identificar o proprietário canônico existente;
3. reutilizar quando houver equivalência;
4. reconciliar quando houver sobreposição parcial;
5. criar algo novo somente quando houver lacuna comprovada;
6. registrar a relação e a justificativa da não reutilização.

Esta Skill **não é proprietária** das regras detalhadas de composição, precificação, fabricação, PTS, memória persistente ou cálculo. Ela apenas referencia e orquestra essas capacidades.

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
9. **Varredura de recorrências** — reconhecer serviços/itens recorrentes, suas aplicações e relações; recorrência gera verificação, nunca inclusão automática.
10. **Conferência** — PTS Técnica × Orçamento.
11. **PTS Pós-Orçamento** — identificar divergências, omissões, inclusões sem origem e responsabilidades indefinidas.
12. **Aprendizado** — extrair padrões somente após validação, preservando evidência e contexto.
13. **Memória de cálculo** — preservar fórmula, parâmetros, origem, resultado e evidência sem substituir o sistema persistente.

## 4. Encadeamento operacional canônico

```text
DOCUMENTAÇÃO VIGENTE
      ↓
ELO ANALISAR
      ↓
PTS TÉCNICA
      ↓
[VARRER RECORRÊNCIAS — OBRIGATÓRIO]
requisito → aplicação → item/serviço recorrente → dependências → memória/precedente → alerta
      ↓
DIRECIONAMENTO / CHECKLIST
      ↓
CONTRATO DE EXECUÇÃO
      ↓
ESPECIALISTA DE ORÇAMENTO EXECUTA
      ↓
ORÇAMENTO + MEMÓRIAS DE CÁLCULO
      ↓
PTS PÓS-ORÇAMENTO
      ↓
[VARRER RECORRÊNCIAS — OBRIGATÓRIO NOVAMENTE]
orçado → esperado → omitido → duplicado → associação nova → candidato a aprendizado
      ↓
ELO CONFERE
   ├─ OK → fechamento
   └─ CONTESTAÇÃO → Especialista corrige
                      ↓
                    ORÇAMENTO REV.N
                      ↓
                    PTS PÓS REV.N
                      ↓
                    VARRER RECORRÊNCIAS
                      └──────────────► nova conferência
      ↓
APRENDIZADO CANDIDATO
      ↓
VALIDAÇÃO / GOVERNANÇA
      ↓
MEMÓRIA COGNITIVA E ESTRUTURAS PERSISTENTES CANÔNICAS
```

A Skill não executa composição/precificação em paralelo ao Especialista e não grava diretamente em memória canônica fora do fluxo autorizado.

## 4.1 Loop obrigatório de recorrências

A varredura de serviços e itens recorrentes é uma etapa **obrigatória e repetível** do orçamento.

### Entrada pela PTS Técnica

Sempre que uma PTS Técnica for criada ou revisada, executar:

`REQUISITOS → DISCIPLINAS → CATÁLOGO DE RECORRÊNCIAS → APLICAÇÃO → DEPENDÊNCIAS → PRECEDENTES/MEMÓRIAS → ALERTAS PARA ORÇAMENTO`

A varredura deve perguntar, conforme aplicabilidade:

- o requisito costuma gerar abertura/reforço/acabamento de vão?
- há fabricação e instalação separadas?
- há item complementar de fixação, acabamento, proteção ou conexão?
- há elétrica, hidráulica, dados, climatização, drenagem ou SPDA associados?
- há mobilização, carro de apoio, hospedagem, pedágio, transporte ou Munck?
- há projeto, ART/RRT, teste, comissionamento ou documentação?
- há manutenção ou periodicidade?

O resultado é **alerta de verificação**. Nunca ampliar escopo automaticamente.

### Entrada pela PTS Pós-Orçamento

Sempre que uma PTS Pós for criada ou revisada, repetir a varredura:

`PTS TÉCNICA → ORÇAMENTO → ITENS RECORRENTES ESPERADOS → ITENS ORÇADOS → OMISSÕES → DUPLICIDADES → NOVAS ASSOCIAÇÕES → APRENDIZADO`

A PTS Pós deve classificar cada associação como:

- `ATENDIDA`;
- `NÃO APLICÁVEL`;
- `OMITIDA`;
- `DUPLICADA`;
- `PENDENTE DE VALIDAÇÃO`;
- `NOVA ASSOCIAÇÃO CANDIDATA`.

### Reentrada

Se a PTS Pós encontrar erro ou lacuna que altere o orçamento:

`PTS PÓS → CORREÇÃO DO ORÇAMENTO → NOVA PTS PÓS → NOVA VARREDURA`

O loop só encerra quando divergências materiais estiverem resolvidas, justificadas ou explicitamente arbitradas.

## 4.2 Catálogo cognitivo recorrente

A skill deve consultar o catálogo do Especialista:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/CATALOGO_SERVICOS_ITENS_RECORRENTES.md`

O catálogo responde **o que procurar e quando procurar**. Valores, quantidades e fórmulas reais devem vir da fonte vigente e das memórias estruturadas correspondentes.

Regra:

`RECORRÊNCIA ≠ INCLUSÃO AUTOMÁTICA`

`RECORRÊNCIA → VERIFICAR APLICAÇÃO → CONSULTAR MEMÓRIA → RECALCULAR → VALIDAR → ORÇAR`

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
- Toda PTS Técnica e toda PTS Pós deve executar a varredura de recorrências antes de ser considerada completa.
- Uma associação recorrente ausente gera alerta; não autoriza inclusão automática.

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

O loop deve aprender prioritariamente:

- serviços e itens recorrentes;
- gatilhos de aplicação;
- associações entre itens;
- sequência executiva;
- separação fabricação × instalação × campo;
- quantitativos e produtividade;
- dependências logísticas;
- responsabilidade por fornecimento de valores;
- causas de omissão e duplicidade encontradas na PTS Pós.

## 7. Relação com a memória persistente

A skill não cria memória paralela. Os registros de orçamento devem utilizar as estruturas canônicas existentes, incluindo as famílias de:

- memória de orçamento;
- cálculos aprendidos;
- varreduras de cálculos;
- evidências de cálculo;
- decisões;
- associações.

Método, aplicação e relação recorrente ficam na camada documental do Especialista; memória quantitativa real permanece na persistência estruturada canônica.

O `ELO_MEMORIA_ORCAMENTOS.md` é camada textual de contexto/índice e não substitui a persistência estruturada nem cria uma nova autoridade.

## 8. Fail-closed

Bloquear ou marcar como não confirmado quando houver:

- PTS Técnica sem varredura de recorrências;
- PTS Pós sem segunda varredura de recorrências;
- evidência ausente para requisito crítico;
- cálculo sem parâmetros suficientes;
- origem de custo não demonstrável;
- conflito documental não resolvido;
- responsabilidade indefinida com impacto material;
- tentativa de transformar experiência isolada em regra;
- associação recorrente incluída automaticamente sem confirmação de aplicabilidade;
- segredo/token/chave em evidência ou proveniência;
- tentativa de alterar memória canônica fora do fluxo autorizado.

## 9. Critério de qualidade

A execução só é considerada rastreável quando cada custo relevante puder responder:

`POR QUE → DE ONDE → COMO → QUANTO → PREMISSA → RISCO → VALIDAÇÃO`

E cada recorrência relevante puder responder:

`QUAL GATILHO → QUAL APLICAÇÃO → QUAL DEPENDÊNCIA → QUAL MEMÓRIA → FOI VERIFICADA? → QUAL RESULTADO?`

## 10. Potencialização para o ELO

Esta skill transforma o domínio de orçamento em uma capacidade estruturada de raciocínio operacional **sem duplicar capacidades existentes**: conecta requisito, solução, composição, custo, evidência, decisão, recorrências, resultado pós-orçamento e aprendizado, mantendo a autoridade nas estruturas canônicas já existentes.

## 11. Regra de manutenção

Se uma fonte canônica posterior incorporar uma regra atualmente descrita nesta Skill, remover a duplicação desta Skill e manter somente a referência/ponte operacional. A Skill deve permanecer fina, estável e orientada à coordenação do processo.
