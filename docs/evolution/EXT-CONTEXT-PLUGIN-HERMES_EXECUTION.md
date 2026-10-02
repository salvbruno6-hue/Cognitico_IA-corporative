# EXT-CONTEXT-PLUGIN-HERMES — Execução Governada

## Objetivo

Fechar a cadeia operacional do candidato sem criar nova autoridade de contexto,
autorização, execução, memória ou aprendizado.

## Cadeia canônica

1. DecisionPatternCandidate identifica o candidato.
2. DecisionLifecycle preserva a decisão e decision_pattern_candidate_ref.
3. A autoridade de autorização fornece authorization_id.
4. O chamador constrói ExecutionRequest.
5. execute_context_plugin chama o ExecutionBoundary canônico.
6. ContextPluginExecutionAdapter executa o comportamento existente.
7. ContextResolutionEngine continua sendo a autoridade de contexto.
8. ContextPluginAdapter apenas adapta um ContextPack com sinal Hermes verificado.
9. ExecutionOutcome preserva request, autorização, correlação e candidate ref.
10. Evidência operacional deve ser criada somente a partir do resultado observado.
11. Repetições independentes são necessárias antes de OPERATIONAL_OUTCOME.
12. Somente SymbiontLab + EvolutionGate + LearningGovernance podem avaliar evolução.

## Pré-condições

- tenant_id
- principal_id
- action_id=EXT-CONTEXT-PLUGIN-HERMES
- authorization_id
- correlation_id
- pelo menos um evidence_id
- decision_pattern_candidate_ref quando vinculado ao candidato
- sinal Hermes com explicit_activation=True e provenance_verified=True

## Operação

O executor fornece uma pergunta real da solicitação. A execução resolve o contexto
através de ContextResolutionEngine e aplica ContextPluginAdapter.

O adapter não decide autorização. A ausência de controles bloqueia no ExecutionBoundary.

## Evidência

Não usar baseline=0.0, observed_value=1.0 ou repeatability=1/1 como prova de produção.

Para cada execução real, registrar somente fatos observados: execution_id,
candidate_id, owner, runtime_entrypoint, timestamp, ação observada, métrica,
direção, baseline observado, valor observado, atribuição, commit/runtime trace,
regressão e repetibilidade.

Uma execução única não constitui OPERATIONAL_OUTCOME.

## Não fazer

- não executar fora do ExecutionBoundary;
- não promover automaticamente;
- não criar outro Evolution Gate;
- não criar nova memória;
- não transformar execução em LearningCandidate automaticamente;
- não fabricar baseline, resultado, hipótese, experimento, generalização ou ATTRIBUTED;
- não tratar testes controlados como prova de produção.

## Critério

A implementação técnica desta etapa está concluída quando:

ExecutionRequest → ExecutionBoundary → ContextPluginAdapter → ExecutionOutcome

mantém a proveniência íntegra.

Isso não prova valor em produção nem autoriza promoção do candidato.
