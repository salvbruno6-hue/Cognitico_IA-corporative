# ELO — Complementaridade entre Feedback Operacional e Inteligência Sistêmica

## Objetivo

Definir, sem reconciliação silenciosa, como os dois contratos `OutcomeFeedback` existentes podem coexistir dentro de uma arquitetura madura do ELO.

Este documento estabelece uma direção arquitetural. Ele não promove nenhum contrato automaticamente a autoridade única e não altera os contratos existentes.

## 1. Constatação atual

O repositório possui dois contratos com o mesmo nome:

- `src/elo/core/outcome_feedback.py`
- `src/elo/core/systemic_primitives.py`

Eles não são estruturalmente equivalentes.

### Feedback operacional

`outcome_feedback.py` representa o resultado observado de uma decisão de forma compacta:

- `decision_id`
- `outcome_id`
- `expected`
- `observed`
- `assessment`
- `evidence_ids`

Sua finalidade natural é registrar rapidamente o vínculo entre decisão, resultado e evidência.

### Primitivas sistêmicas

`systemic_primitives.py` pertence a uma família maior de objetos de inteligência sistêmica, incluindo:

- `SystemicModel`
- `SystemicRelation`
- `CausalAssessment`
- `DecisionRecord`
- `OutcomeFeedback`
- `TemporalValidity`
- `UncertaintyAssessment`
- `Scenario`

Sua versão de `OutcomeFeedback` acrescenta `variance` e `observed_at`, e participa de uma camada destinada a raciocínio sistêmico, causalidade, temporalidade, incerteza e cenários.

## 2. Direção arquitetural

A arquitetura madura deve separar:

```text
DECISÃO
   ↓
EXECUÇÃO
   ↓
OUTCOME
   ↓
FEEDBACK OPERACIONAL
   ↓
INTERPRETAÇÃO SISTÊMICA
   ↓
LEARNING
   ↓
EVOLUTION GATE
   ↓
CANONICAL ELO
```

A regra é:

> O runtime registra o que aconteceu; a camada sistêmica interpreta o que isso significa para a inteligência corporativa.

## 3. Responsabilidades

### 3.1 Feedback operacional

Responsável por:

- registrar o resultado imediato;
- manter rastreabilidade da decisão;
- preservar evidências;
- permitir avaliação rápida do ciclo operacional;
- alimentar mecanismos de retry, refresh, replan, handoff e encerramento;
- não exigir a construção de um modelo sistêmico completo para cada execução.

### 3.2 Inteligência sistêmica

Responsável por:

- analisar variância entre esperado e observado;
- relacionar resultado a causas e efeitos;
- incorporar temporalidade;
- representar incerteza;
- avaliar cenários;
- identificar relações sistêmicas;
- transformar observações em candidatos de aprendizagem;
- fornecer material para o Evolution Gate.

## 4. Relação entre as camadas

A relação proposta é de transformação/derivação, e não de duplicação:

```text
Operational OutcomeFeedback
            │
            │ evidências + decisão + resultado
            ▼
   Systemic Interpretation
            │
            ├── variance
            ├── causal assessment
            ├── uncertainty
            ├── temporal validity
            └── scenario analysis
            │
            ▼
         Learning
```

O feedback operacional deve continuar sendo preservado como evidência histórica. A interpretação sistêmica não deve apagar ou substituir o evento original.

## 5. Regra de autoridade

Nenhuma das duas estruturas deve, por este documento, receber autoridade canônica automática.

A promoção de aprendizagem continua subordinada ao Evolution Gate.

```text
observação ≠ aprendizagem canônica
aprendizagem candidata ≠ conhecimento canônico
```

## 6. Benefícios

### Agilidade

O runtime pode operar com um contrato pequeno e determinístico.

### Evolutividade

A camada sistêmica pode crescer com novas dimensões sem tornar o runtime operacional progressivamente mais complexo.

### Auditabilidade

O resultado original permanece separado da interpretação posterior.

### Segurança arquitetural

Mudanças na análise sistêmica não precisam alterar a execução operacional.

### Reprocessamento

Um mesmo feedback operacional pode ser reinterpretado posteriormente quando novos modelos, evidências ou relações forem disponibilizados.

## 7. Riscos a controlar

O maior risco atual é a coexistência de dois símbolos `OutcomeFeedback` sem uma fronteira explícita.

Até que exista um contrato de relação implementado, deve-se evitar:

- exportar ambos como se fossem equivalentes;
- converter automaticamente um no outro;
- remover um dos módulos;
- alterar assinaturas existentes apenas para eliminar a duplicidade;
- fazer o runtime depender das primitivas sistêmicas;
- promover feedback operacional diretamente ao Core canônico.

## 8. Próxima evolução segura

A próxima implementação deve introduzir uma fronteira explícita entre:

```text
OperationalOutcome
        ↓
SystemicOutcomeInterpretation
```

Essa fronteira deve preservar:

1. `decision_id`;
2. identidade do outcome;
3. evidências;
4. expected/observed;
5. avaliação operacional;
6. variância sistêmica;
7. temporalidade;
8. incerteza;
9. causalidade, quando houver evidência;
10. provenance da interpretação.

A transformação deve ser somente leitura sobre o histórico operacional e produzir uma representação sistêmica verificável. Nenhuma canonização deve ocorrer nessa etapa.

## 9. Compatibilidade com o runtime de insistência

O runtime `RETRY / REFRESH / REPLAN / HANDOFF / STOP` deve permanecer independente da análise sistêmica pesada.

Fluxo:

```text
Core Decision
     ↓
Governed Insistence Runtime
     ↓
Attempt
     ↓
Outcome
     ↓
Operational Feedback
     ↓
(optional) Systemic Interpretation
     ↓
Learning Candidate
     ↓
Evolution Gate
```

Assim, o princípio permanece:

> **ELO insiste no objetivo, não no método.**

O mecanismo de insistência pode agir rapidamente; a inteligência sistêmica pode aprender com o histórico sem controlar diretamente a execução.

## 10. Estado desta decisão

Esta documentação define uma **direção arquitetural de complementaridade** para investigação e implementação governada.

Ela não declara que um dos dois contratos existentes seja apagado, renomeado ou substituído.

Qualquer consolidação posterior deve ser acompanhada por testes de compatibilidade, rastreabilidade e validação do Evolution Gate.
