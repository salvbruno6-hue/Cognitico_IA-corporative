# ELO — Simbionte Laboratory Intake

**Status:** FORGE / LABORATORY / CANDIDATE-ONLY  
**Branch:** `lab/simbionte-intake-20260906`  
**Purpose:** consolidar, em uma única superfície de laboratório, os mecanismos que devem alimentar a Simbionte para absorção, relação, experimentação, generalização e avaliação, sem criar autoridade canônica paralela.

## 1. Limite estrutural

A Simbionte é uma natureza cognitiva do ELO. Este artefato não cria novo Core, memória canônica, Capability Registry, Authorization Engine, router, Evolution Gate ou fonte de verdade.

A regra é:

`REUSE CAPABILITY, NOT AUTHORITY`

Nada neste laboratório pode:

- alterar Soul, Core ou contratos canônicos por inferência;
- transformar saída externa em conhecimento canônico;
- **não promove aprendizado automaticamente**;
- substituir a autoridade de seleção/execution routing existente;
- atravessar tenant boundary;
- converter contexto específico de empresa em regra geral sem generalização comprovada.

## 2. O que entra na Simbionte

A Simbionte recebe **mecanismos e experiências como evidência experimental**, não como verdade.

### Núcleo de mecanismos

| Origem | Conteúdo experimental | Tratamento |
|---|---|---|
| PR #382 | Budget Intelligence simbiótica, composição missão→contexto→capability→route→provider→evidence→outcome→learning | ABSORVER + EXPERIMENTAR |
| PR #404 | Intake governado de mecanismos externos, comparação, generalização e disposição reuse/strengthen/refactor/deprecate/create | ABSORVER + GENERALIZAR |
| PR #298 | benchmark, descoberta de método, pesquisa externa, otimização cognitiva, raciocínio e inferência neutra de provider | ABSORVER + BENCHMARK |
| PR #316 | testes de laboratório, reconciliação, conflitos, UNKNOWN, isolamento de tenant e limites de conectores | ABSORVER + TESTAR |
| PR #407 | resolução contextual de specialist skill governada pelo Forge | ABSORVER + RELACIONAR |

### Feed operacional

Experiências de orçamento e especialistas podem alimentar o laboratório quando preservarem proveniência, escopo e contexto. Exemplos auditados incluem PRs #324, #326, #328 e #335.

Esses itens são **evidência contextual** até demonstração de generalização. Não são convertidos automaticamente em regra do Core.

## 3. Unidade experimental

Cada mecanismo/experiência deve poder ser representado como:

`EVIDÊNCIA → MECANISMO → CONTEXTO → HIPÓTESE → EXPERIMENTO → RESULTADO → AVALIAÇÃO → CANDIDATO`

### Campos mínimos

- `source_ref`
- `source_commit`
- `registry_or_pr_ref`
- `tenant_scope`
- `mission_class`
- `mechanism_id`
- `mechanism_description`
- `existing_owner`
- `proposed_capability`
- `hypothesis`
- `evidence_refs`
- `baseline`
- `experiment`
- `result`
- `quality`
- `latency`
- `cost`
- `regression_status`
- `generalization_status`
- `risk`
- `disposition`
- `promotion_state`

## 4. O que a Simbionte deve aprender a observar

### Relações

`contexto → necessidade → capability → skill → ferramenta → execução → resultado`

### Padrões

`casos repetidos → comportamento recorrente → hipótese de padrão`

### Combinações

`specialist + model + tool + context + method → resultado`

### Falhas

A Simbionte deve tratar como sinal experimental:

`GAP | UNKNOWN | CONFLICT | BLOCKED | REGRESSION | LOW_QUALITY | REDUNDANCY | UNCONFIRMED`

### Generalização

Uma observação só pode ser candidata a capacidade mais ampla quando:

1. existe evidência suficiente;
2. a hipótese é reproduzível;
3. há benefício mensurável;
4. regressões aceitáveis estão demonstradas;
5. não viola tenant, segurança ou governança;
6. o owner canônico está identificado;
7. a generalização é explicitamente justificada.

## 5. Loop da Simbionte

```text
SOURCE / EXPERIENCE
       ↓
EVIDENCE
       ↓
LABORATORY INTAKE
       ↓
ABSORB
       ↓
RELATE
       ↓
FORM HYPOTHESIS
       ↓
EXPERIMENT
       ↓
MEASURE
       ↓
COMPARE WITH BASELINE
       ↓
CHECK REGRESSION / RISK / SCOPE
       ↓
GENERALIZE?
   ┌───┴────┐
  NÃO      SIM
   ↓         ↓
LOCAL/     CANDIDATE
EXPERIMENT   ↓
           GOVERNED LEARNING
                 ↓
           EVOLUTION GATE
                 ↓
        POSSÍVEL PROMOTION
```

## 6. O que permanece fora da Simbionte como autoridade

A Simbionte pode observar, testar e propor sobre os seguintes domínios, mas não é proprietária deles:

- Soul e invariantes de identidade;
- Core e contratos canônicos;
- authorization, roles, scopes e sessão;
- canonical write boundary;
- fontes de verdade;
- Supabase como persistência estruturada quando canônica;
- ExecutionRouter como autoridade de seleção;
- Evolution Gate;
- regras explicitamente arbitradas;
- aprovação humana;
- políticas de segurança;
- decisões financeiras já arbitradas como fato histórico.

## 7. Regra para mecanismos externos

Mecanismo externo nunca é copiado como autoridade.

O tratamento é:

`EXTERNAL SOURCE → EXTRACT MECHANISM → EVIDENCE → COMPARE WITH CANON → EXPERIMENT → GENERALIZE → GOVERN`

A disposição deve usar somente:

`REUSE | STRENGTHEN | REFACTOR | DEPRECATE | CREATE`

`CREATE` permanece excepcional e exige ausência comprovada de owner canônico **e** generalização.

## 8. Primeira família de experimentos

### A. Orçamento simbiótico

Objetivo: verificar quais combinações de specialist/model/tool/context/method produzem melhor resultado de orçamento sob as mesmas exigências de governança.

Métrica mínima:

`quality + groundedness + evidence completeness + latency + cost + regression + tenant isolation`

Uma única execução não altera routing.

### B. Descoberta de método corporativo

Comparar método realmente praticado pelo tenant com técnicas externas, preservando a regra:

`OBSERVE → MODEL → EXECUTE → VERIFY → LEARN → PROPOSE`

Nunca:

`ASSUME → STANDARDIZE → OVERRIDE`

### C. Avaliação e regressão

Executar benchmark pareado contra baseline antes de considerar qualquer candidato de evolução.

### D. Reconciliação e conflito

Conflitos devem ser preservados como conflito. O laboratório não pode mascarar divergência para produzir um resultado aparentemente melhor.

## 9. Resultado esperado desta etapa

Esta etapa **não promove nada para Core**.

Ela cria somente uma superfície governada para que a Simbionte possa:

- absorver mecanismos úteis;
- relacionar mecanismos a contextos e capacidades existentes;
- experimentar combinações;
- identificar limites e falhas;
- gerar hipóteses;
- medir resultados;
- formar candidatos de aprendizado;
- devolver candidatos ao fluxo de Governed Learning.

## 10. Critério de passagem

Um candidato só sai do laboratório quando houver pacote mínimo de evidência contendo:

`PROVENIÊNCIA + CONTEXTO + BASELINE + EXPERIMENTO + RESULTADO + REGRESSÃO + GENERALIZAÇÃO + RISCO + OWNER + DISPOSIÇÃO`

Sem isso, permanece `LAB_ONLY`.
