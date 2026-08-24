# ELO — ARQUITETURA CANÔNICA DA ANÁLISE DE SOLICITAÇÕES

**Versão:** 1.0  
**Status:** Diretriz arquitetural proposta para validação  
**Domínio:** Comercial + Licitações + Planejamento + Engenharia de Orçamento

## 1. PRINCÍPIO CENTRAL

A Análise de Solicitações é um sistema operacional cognitivo por camadas. Não deve ser tratada como um único prompt, uma única memória ou uma única biblioteca.

Regra estrutural:

`ORQUESTRAR ≠ EXECUTAR ≠ CONHECER ≠ CALCULAR ≠ EVIDENCIAR ≠ APRENDER`

O ELO coordena e audita. O Especialista executa o orçamento. As bibliotecas fornecem conhecimento. A memória de cálculo preserva a lógica. A SO fornece evidência. A PTS formaliza análise e conferência. O aprendizado generaliza somente o que foi validado.

## 2. CAMADAS

```text
00 — CÂNONE / GOVERNANÇA
 ↓
01 — ORQUESTRAÇÃO ELO
 ↓
02 — DOMÍNIO ANÁLISE DE SOLICITAÇÕES
 ↓
03 — ESPECIALISTAS
 ↓
04 — KNOWLEDGE / BIBLIOTECAS
 ↓
05 — MEMÓRIA OPERACIONAL / EVIDÊNCIAS
 ↓
06 — PTS / ARTEFATOS DE SAÍDA
 ↓
07 — APRENDIZADO / GENERALIZAÇÃO
```

| Camada | Função |
|---|---|
| 00 | identidade, limites, governança e autoridade |
| 01 | orquestração, contexto, auditoria e coordenação |
| 02 | processo operacional da SO/LIC |
| 03 | execução especializada |
| 04 | conhecimento reutilizável |
| 05 | casos, evidências, decisões e raciocínios |
| 06 | comprovação e comunicação do resultado |
| 07 | evolução controlada do conhecimento |

## 3. ELO — ORQUESTRADOR

O ELO é responsável por:

- interpretar a SO;
- resolver contexto;
- localizar fontes;
- identificar GAPs;
- preparar o direcionamento;
- selecionar o especialista adequado;
- avaliar riscos;
- conferir rastreabilidade;
- contestar resultados;
- controlar estados de confiança;
- encaminhar aprendizado.

O ELO não deve absorver a composição detalhada e a precificação quando houver Especialista de Orçamento habilitado.

Interface:

`ELO → DIRECIONAMENTO → ESPECIALISTA → RESULTADO → ELO AUDITA → FEEDBACK`

## 4. DOMÍNIO ANÁLISE DE SOLICITAÇÕES

Controla o ciclo:

`SO → DOCUMENTOS → CONTEXTO → REQUISITOS → PTS TÉCNICA → ORÇAMENTO → PTS PÓS → APRENDIZADO`

O domínio não deve duplicar catálogo, memória de cálculo ou metodologia detalhada. Ele define quando essas fontes são consultadas.

## 5. ESPECIALISTA DE ORÇAMENTO

É o executor especializado.

Recebe do ELO contexto, requisitos, escopo, classificação, riscos, pendências, PTS Técnica quando aplicável e direcionamento.

Executa:

`MODELO → QUANTITATIVO → ADAPTAÇÕES → EXCEDENTES → SERVIÇOS → MATERIAIS → MÃO DE OBRA → LOGÍSTICA → PROJETOS → COMPOSIÇÃO → CUSTOS → FECHAMENTO`

Entrega:

- orçamento;
- composição;
- premissas;
- memória de cálculo;
- excedentes;
- pendências;
- riscos;
- rastreabilidade;
- PTS Pós-Orçamento.

Regra permanente:

> **ELO orienta e audita. Especialista de Orçamento executa.**

## 6. KNOWLEDGE — BIBLIOTECAS ESPECIALIZADAS

### 6.1 Corporativo

Produtos, famílias, modelos, características, padrões de fabricação e terminologia.

Obrigatório manter:

`MLT-M = Módulos`  
`MLT-C = Contêineres`

Não misturar as taxonomias.

### 6.2 Excedentes

Biblioteca para:

`PADRÃO → DIFERENÇA → EXCEDENTE → QUANTIDADE → COMPOSIÇÃO`

### 6.3 Serviços e Materiais

Catálogo lógico de serviços, materiais, mão de obra e composições.

### 6.4 Taxonomia / SQL

SQL recupera informação estruturada; não decide a aplicabilidade.

`CONSULTAR → RECUPERAR → VALIDAR CONTEXTO → APLICAR`

### 6.5 Normas

Referências normativas e critérios de aplicação. Não inventar número ou aplicabilidade.

## 7. MEMÓRIA OPERACIONAL E EVIDÊNCIAS

Não confundir memória de caso com conhecimento geral.

### Memória da SO

Registra o que aconteceu naquela solicitação.

### Memória de cálculo

Registra:

`ENTRADA → FONTE → PREMISSA → FÓRMULA → SUBCÁLCULOS → RESULTADO → VALIDAÇÃO`

A lógica é reutilizável; o preço histórico não é automaticamente reutilizável.

### Proveniência

`SOURCE → CLAIM → ANALYSIS → PREMISE → DECISION → RESULT → LEARNING`

### Confiança

- `CONFIRMADO` — fonte oficial;
- `CONHECIMENTO ELO` — regra validada;
- `EXPERIÊNCIA` — caso histórico;
- `HIPÓTESE` — precisa validação;
- `PENDÊNCIA` — informação insuficiente.

## 8. PTS E ARTEFATOS

### PTS Técnica

`DOCUMENTO → REQUISITO → SOLUÇÃO → QUANTITATIVO → PREMISSA`

### Orçamento

`PTS TÉCNICA → COMPOSIÇÃO → CUSTO`

### PTS Pós-Orçamento

`PTS TÉCNICA → ORÇAMENTO → CONFERÊNCIA → DIVERGÊNCIA → JUSTIFICATIVA → VALIDAÇÃO`

A PTS Pós não substitui a PTS Técnica; ela fecha o ciclo de rastreabilidade.

## 9. GATILHOS

### `ELO ANALISAR`

É uma porta de entrada. Não é um segundo motor de orçamento.

Deve:

1. identificar SO/LIC;
2. resolver documentos e contexto;
3. consultar conhecimento;
4. executar PTS Técnica quando aplicável;
5. preparar direcionamento;
6. entregar ao Especialista;
7. acompanhar;
8. auditar;
9. validar PTS Pós;
10. encaminhar aprendizado.

### `ORÇAR`

É a transição operacional para o Especialista. Não deve exigir repetição de informações já disponíveis.

## 10. REGRA DE CONSULTA

```text
SO VIGENTE
 ↓
CONHECIMENTO CORPORATIVO
 ↓
EXCEDENTES / TAXONOMIA / SERVIÇOS / NORMAS
 ↓
MEMÓRIA DE CÁLCULO
 ↓
EXPERIÊNCIAS
```

A fonte vigente da SO prevalece sobre histórico.

## 11. MEMÓRIA DE CÁLCULO REUTILIZÁVEL

Quando um orçamento produzir raciocínio relevante, registrar a lógica de forma paramétrica.

Exemplos:

`CUSTO = Q × PU`

`DIÁRIAS = DIAS_DE_CAMPO − 1`

`EXCEDENTE = Q_REQUERIDA − Q_PADRÃO`

Registrar quais variáveis podem mudar para permitir reaplicação em novos cenários.

## 12. LOGÍSTICA

Avaliar:

`BASE → DESTINO → DISTÂNCIA → TEMPO → EQUIPE → TRANSPORTE → ALIMENTAÇÃO → HOSPEDAGEM → APOIO`

A referência de aproximadamente 6 horas é parâmetro para comparar alternativas de deslocamento, não obrigação contratual.

Regra:

`ESTADIAS = DIAS DE PERMANÊNCIA − 1`

O último dia é retorno, salvo inviabilidade operacional validada.

## 13. APRENDIZADO

`EXPERIÊNCIA → OBSERVAÇÃO → ANÁLISE → TESTE → FEEDBACK → VALIDAÇÃO → GENERALIZAÇÃO → CANDIDATO → EVOLUTION GATE → CORE`

Tipos:

- `PRECEDENT`;
- `LEARNING_CANDIDATE`;
- `VALIDATED_LEARNING`.

Uma SO isolada não cria automaticamente uma regra corporativa.

## 14. NÃO DUPLICAÇÃO

Não criar:

- segundo Core;
- segundo orquestrador;
- segunda memória canônica;
- segundo `ELO ANALISAR`;
- segunda metodologia concorrente de orçamento;
- catálogo paralelo sem governança;
- mesma regra de cálculo em múltiplas fontes sem referência canônica.

Quando uma regra existir, referenciar a fonte canônica em vez de copiá-la integralmente.

## 15. MATRIZ DE RESPONSABILIDADE

| Atividade | ELO | Especialista | Knowledge | Memória | PTS |
|---|---|---|---|---|---|
| Interpretar SO | R | C | C | C | C |
| Selecionar modelo | A/C | R | C | C | C |
| Identificar excedentes | A/C | R | C | C | C |
| Compor custos | A/C | R | C | C | - |
| Calcular orçamento | A/C | R | C | C | - |
| Registrar memória de cálculo | A | R | - | R | - |
| Auditar orçamento | R | C | C | C | C |
| PTS Técnica | A | C | C | C | R |
| PTS Pós | A | R/C | C | C | R |
| Promover aprendizado | R | C | C | R | C |

`R = executa`, `A = autoridade/auditoria`, `C = contribui/é consultado`.

## 16. TESTE DE COERÊNCIA

Toda nova regra deve responder:

1. Onde mora?
2. Quem é o dono?
3. Quem consulta?
4. Qual é a fonte de autoridade?
5. Qual é a saída?
6. Duplica outra regra?
7. Pode ser reutilizada?
8. Como chega ao aprendizado?

Se não responder às oito perguntas, é uma pendência arquitetural.

## 17. OBJETIVO

A arquitetura deve permitir orçamentos:

- mais rápidos por reutilização estruturada;
- mais completos por cobertura sistemática;
- mais confiáveis por separação entre evidência e hipótese;
- mais explicáveis por memória de cálculo;
- mais escaláveis por especialistas e bibliotecas independentes;
- mais inteligentes por aprendizado validado.

O objetivo não é fazer o ELO guardar todos os detalhes. É fazer o ELO **saber onde cada conhecimento está, quando utilizá-lo, como combiná-lo e como verificar o resultado**.
