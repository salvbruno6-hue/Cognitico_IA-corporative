# ELO Reasoning Engine Contract v1.0

**Status:** Documento canônico subordinado à baseline
**Escopo:** processamento cognitivo e verificação
**Finalidade:** definir o contrato do Reasoning Engine sem confundir raciocínio com conhecimento, memória, decisão ou execução.

## 1. Objetivo

O Reasoning Engine transforma contexto, conhecimento, memória, políticas e evidências em inferências, hipóteses, conclusões intermediárias ou recomendações verificáveis.

## 2. Responsabilidades

O Reasoning Engine é responsável por:
- interpretar contexto de entrada;
- relacionar informações relevantes;
- produzir hipóteses e inferências;
- explicitar premissas e incertezas;
- registrar evidências utilizadas;
- submeter resultados à validação quando necessário.

## 3. Limites

O Reasoning Engine não é responsável por:
- persistir conhecimento permanente;
- armazenar memória de longo prazo;
- aprovar decisões;
- executar ações em sistemas externos;
- alterar políticas;
- substituir julgamento humano quando a criticidade exigir supervisão.

## 4. Entradas

Entradas típicas:
- Context
- Knowledge references
- Memory references
- Policy constraints
- Evidence sets
- Agent observations quando validadas

## 5. Saídas

Saídas típicas:
- hypotheses
- intermediate conclusions
- recommended actions
- confidence signals
- uncertainty notes
- verification needs
- provenance references

## 6. Fluxo de raciocínio de referência

1. Receive context.
2. Select relevant knowledge and memory references.
3. Apply policies and constraints.
4. Evaluate evidence quality and sufficiency.
5. Generate hypotheses or intermediate conclusions.
6. Assign confidence and uncertainty markers.
7. Request verification when needed.
8. Emit reasoning result with provenance.

## 7. Verification contract

Todo resultado relevante do Reasoning Engine deve indicar, conforme aplicável:
- hipótese produzida;
- premissas assumidas;
- evidências usadas;
- pontos de incerteza;
- nível de confiança;
- necessidade de validação humana;
- dependências de política.

## 8. Regras

- Reasoning não cria verdade institucional por si só.
- Reasoning não substitui proveniência.
- Reasoning não pode ocultar premissas ou fontes relevantes.
- Reasoning sem evidência suficiente deve declarar limitação.
- Reasoning de alta criticidade deve exigir validação adicional.

## 9. Eventos

- ReasoningStarted
- ReasoningCompleted
- ReasoningValidated
- ReasoningRejected
- ReasoningConfidenceAdjusted
- ReasoningVerificationRequested

## 10. Observabilidade

Métricas recomendadas:
- tempo de execução de raciocínio
- taxa de verificação solicitada
- taxa de rejeição de inferências
- confiança média por domínio
- incidência de raciocínio sem evidência suficiente

## 11. Compatibilidade

Este contrato depende da baseline e dos contratos de Context, Knowledge e Memory. Ele não deve ser usado para redefinir essas entidades.

---

**Dependência principal:** ELO Core Architecture Baseline v1.0
**Categoria:** Cognitive Platform