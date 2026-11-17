# Domínio Operacional — Análise de Solicitações

**Especialista:** Orçamento  
**Governança:** ELO  
**Status:** Oficial  
**Arquitetura:** `01-meta-architecture/cognitive-architecture/ELO_ANALISE_SOLICITACOES_ARQUITETURA_CANONICA.md`

## 1. Finalidade do domínio

`Análise de Solicitações` é o domínio operacional que transforma uma SO/LIC em um orçamento rastreável, auditável e pronto para decisão.

O domínio não é uma biblioteca única. Ele coordena fontes e artefatos:

`SO → DOCUMENTOS → ELO → PTS TÉCNICA → ESPECIALISTA → ORÇAMENTO → PTS PÓS → APRENDIZADO`

## 2. Papéis

### ELO

É o **orquestrador e auditor** do domínio.

Responsável por:

- interpretar a SO;
- resolver contexto;
- identificar fontes e lacunas;
- gerar direcionamento;
- indicar riscos, divergências e validações;
- acionar o Especialista;
- conferir rastreabilidade;
- contestar resultados;
- encaminhar aprendizado.

### Especialista de Orçamento

É o **executor especializado**.

Responsável por:

- selecionar modelo/base;
- levantar quantitativos;
- identificar adaptações e excedentes;
- compor serviços, materiais e mão de obra;
- executar cálculos;
- aplicar regras comerciais vigentes;
- dimensionar logística;
- consolidar orçamento;
- produzir memória de cálculo;
- preparar PTS Pós-Orçamento;
- ajustar quando houver contestação fundamentada.

Regra permanente:

> **ELO orienta e audita. Especialista de Orçamento executa.**

## 3. Gatilhos

### `ELO ANALISAR`

É a porta de entrada do processo. Não é um segundo motor de orçamento.

Ao ser acionado, o ELO deve:

1. identificar SO/LIC, cliente, modalidade, objeto e local;
2. localizar documentos vigentes e registrar ausências;
3. resolver contexto;
4. consultar conhecimento aplicável;
5. identificar família/modelo e quantitativos a conferir;
6. identificar adaptações, excedentes, serviços, materiais e interfaces relevantes;
7. avaliar projetos, normas, responsabilidades e riscos;
8. avaliar prazos de mobilização/montagem/entrega/desmontagem;
9. preparar logística e pontos críticos;
10. estruturar PTS Técnica quando aplicável;
11. produzir Checklist ELO;
12. entregar Direcionamento ao Especialista.

O gatilho deve consultar as fontes canônicas, não duplicar a metodologia completa do Especialista.

### `ORÇAR`

Transfere a execução para o Especialista de Orçamento.

O Especialista não deve pedir que o usuário repita informações já disponíveis no contexto, nos documentos ou no direcionamento.

## 4. Fluxo oficial

```text
SO / LIC
   ↓
ELO ANALISAR
   ↓
CONTEXTO + FONTES + GAPS + RISCOS
   ↓
PTS TÉCNICA (quando aplicável)
   ↓
DIRECIONAMENTO
   ↓
ORÇAR
   ↓
ESPECIALISTA DE ORÇAMENTO
   ├─ MODELO / BASE
   ├─ QUANTITATIVOS
   ├─ ADAPTAÇÕES
   ├─ EXCEDENTES
   ├─ SERVIÇOS / MATERIAIS / MO
   ├─ PROJETOS
   ├─ LOGÍSTICA
   ├─ MEMÓRIA DE CÁLCULO
   └─ FECHAMENTO
   ↓
ORÇAMENTO
   ↓
PTS PÓS-ORÇAMENTO
   ↓
ELO CONFERE
   ├─ OK → CONSOLIDA
   └─ CONTESTAÇÃO → ESPECIALISTA AJUSTA → ELO CONFERE NOVAMENTE
   ↓
APRENDIZADO
```

## 5. Fontes especializadas

O domínio consulta as fontes conforme a necessidade, sem duplicá-las:

### Orçamento

- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PTS_TECNICA_MATURIDADE.md`
- `04-knowledge-handbook/ELO_ESPECIALISTA_ORCAMENTO_DIRETRIZES_PROJETO_ANALISE_SOLICITACOES.md`
- `04-knowledge-handbook/ELO_ESPECIALISTA_ORCAMENTO_METODOLOGIA_V2.md`

### Excedentes

`04-knowledge-handbook/ELO_CAMADA_EXCEDENTES_COMPOSICAO.md`

### Taxonomia / SQL

`04-knowledge-handbook/ELO_TAXONOMIA_CATALOGO_SERVICOS_PRODUTOS_SQL.md`

### Memória de cálculo

`04-knowledge-handbook/ELO_MEMORIA_CALCULO_ESPECIALISTA_ORCAMENTO.md`

### PTS Pós-Orçamento

`08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO.md`

## 6. Rastreabilidade mínima

Todo custo relevante deve poder ser relacionado a:

`DOCUMENTO → REQUISITO → SOLUÇÃO → MODELO → QUANTIDADE → EXCEDENTE → COMPOSIÇÃO → VALOR → PREMISSA → EVIDÊNCIA`

Quando a origem não for direta, registrar a premissa ou justificativa.

## 7. Separação entre conhecimento, memória e caso

**Knowledge:** regra reutilizável e validada.

**Memória de cálculo:** lógica de como um valor foi obtido.

**Memória da SO:** o que ocorreu naquele caso.

**PTS:** artefato formal da análise/conferência.

**Aprendizado:** conhecimento candidato ou validado derivado de experiências e evidências.

Não misturar essas funções.

## 8. Regra de contestação

Quando o ELO contestar:

1. identificar o item;
2. retornar à fonte;
3. verificar cálculo, premissa, modelo, quantitativo e composição;
4. corrigir quando procedente;
5. atualizar memória/PTS quando afetadas;
6. devolver para nova conferência.

## 9. Regra de evolução

O Especialista não altera diretamente as diretrizes oficiais do ELO.

Melhorias identificadas durante uma SO devem ser registradas como candidato de aprendizado e submetidas à governança conforme a arquitetura canônica.

Uma experiência isolada não cria automaticamente regra corporativa.

## 10. Critério de domínio

O domínio está corretamente operando quando:

`ELO SABE O QUE PROCURAR → ESPECIALISTA SABE O QUE COMPOR → MEMÓRIA SABE COMO FOI CALCULADO → PTS SABE O QUE FOI COMPROVADO → APRENDIZADO SABE O QUE PODE SER REUTILIZADO`

Essa separação é obrigatória para preservar velocidade, completude, rastreabilidade e evolução sem duplicação.
