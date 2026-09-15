# ELO — Skill de Orçamento

**Versão:** 1.0  
**Status:** Candidato canônico — sujeito ao Evolution Gate  
**Domínio:** Orçamento  
**Autoridade:** ELO/Governance  
**Executor especializado:** Especialista de Orçamento

## 1. Finalidade

Esta skill organiza a capacidade de orçamento do ecossistema ELO. Ela não substitui o Prompt oficial nem a Metodologia V2; faz a ligação operacional entre ELO, Especialista, PTS Técnica, orçamento, PTS Pós-Orçamento e aprendizado.

**Regra estrutural:** ELO orienta e audita; o Especialista de Orçamento executa a composição e a precificação.

Fontes canônicas relacionadas:
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`
- `04-knowledge-handbook/ELO_ESPECIALISTA_ORCAMENTO_METODOLOGIA_V2.md`
- `00-core/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`
- `08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO.md`
- `prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`

## 2. Capacidades

A skill deve cobrir, de forma rastreável:

1. **Leitura e enquadramento** — objeto, escopo, local, regime, prazo e documentos vigentes.
2. **Análise técnica-orçamentária** — requisito → solução → quantitativo → composição.
3. **Modelo/base** — identificar produto padrão, excedente e customização.
4. **Quantitativos** — extrair, conferir unidade, dimensão, área, quantidade, produtividade e duração.
5. **Composição** — material, fabricação, mão de obra interna/externa, fornecedor, transporte, mobilização e demais custos necessários.
6. **Logística** — mobilização, desmobilização, transporte, hospedagem, alimentação, combustível e deslocamentos sustentados por evidência.
7. **Premissas** — classificar origem e impacto; nunca ocultar informação não confirmada.
8. **Questionamentos/vistoria** — preferir vistoria quando a lacuna puder ser resolvida em campo.
9. **Conferência** — PTS Técnica × Orçamento.
10. **PTS Pós-Orçamento** — identificar divergências, omissões, inclusões sem origem e responsabilidades indefinidas.
11. **Aprendizado** — extrair padrões somente após validação, preservando evidência e contexto.
12. **Memória de cálculo** — preservar fórmula, parâmetros, origem, resultado e evidência sem substituir o sistema persistente.

## 3. Fluxo operacional

```text
DOCUMENTAÇÃO VIGENTE
      ↓
PTS TÉCNICA / ELO ANALISAR
      ↓
DIRECIONAMENTO E CHECKLIST
      ↓
ORÇAR
      ↓
ESPECIALISTA EXECUTA
      ├─ modelo/base
      ├─ excedentes/customizações
      ├─ quantitativos
      ├─ composições
      ├─ mão de obra
      ├─ logística
      ├─ projetos/documentação
      └─ custos indiretos
      ↓
ORÇAMENTO + MEMÓRIA DE CÁLCULO
      ↓
PTS PÓS-ORÇAMENTO
      ↓
ELO CONFERE
   ├─ OK → fechamento
   └─ CONTESTAÇÃO → correção → nova conferência
      ↓
APRENDIZADO VALIDADO
      ↓
MEMÓRIA COGNITIVA / HISTÓRICO
```

## 4. Regras de decisão

- Usar documentação vigente antes de histórico.
- Histórico serve para comparação e aprendizado, nunca substitui requisito atual.
- Não inventar preço, quantidade, dimensão, produtividade, prazo, responsabilidade ou condição de execução.
- Conflitos devem ser explicitados, não resolvidos silenciosamente.
- Produto padrão não deve ser tratado como item especial sem evidência de desvio.
- Excedente deve registrar requisito, padrão, alteração, quantidade, material, mão de obra, impacto e preço.
- Toda precificação relevante deve manter origem identificável.
- Premissa crítica deve gerar pendência/questionamento quando alterar materialmente custo ou atendimento.
- Resultado de uma única SO não vira regra geral sem validação.

## 5. Contrato de aprendizado

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

Somente `VALIDADO` pode alimentar regra permanente, e ainda assim dentro do mecanismo canônico de memória/governança.

## 6. Relação com a memória persistente

A skill não cria memória paralela. Os registros de orçamento devem se relacionar às estruturas canônicas existentes, incluindo as famílias de:

- memória de orçamento;
- cálculos aprendidos;
- varreduras de cálculos;
- evidências de cálculo;
- decisões;
- associações.

O Markdown é uma camada legível e rastreável; a persistência estruturada permanece na autoridade de dados definida pelo ELO.

## 7. Fail-closed

Bloquear ou marcar como não confirmado quando houver:

- evidência ausente para requisito crítico;
- cálculo sem parâmetros suficientes;
- origem de custo não demonstrável;
- conflito documental não resolvido;
- responsabilidade indefinida com impacto material;
- tentativa de transformar experiência isolada em regra;
- segredo/token/chave em evidência ou proveniência;
- tentativa de alterar memória canônica fora do fluxo autorizado.

## 8. Critério de qualidade

A execução só é considerada rastreável quando cada custo relevante puder responder:

`POR QUE → DE ONDE → COMO → QUANTO → PREMISSA → RISCO → VALIDAÇÃO`

## 9. Potencialização para o ELO

Esta skill transforma o domínio de orçamento em uma capacidade estruturada de raciocínio operacional: o ELO passa a conseguir relacionar requisito, solução, composição, custo, evidência, decisão, resultado pós-orçamento e aprendizado sem confundir memória histórica com regra canônica.
