# Automação para Laboratório canônico

Fluxo:
ExecutionRequest → Authorization → Automation → ExecutionResult →
AutomationEvidence → SymbiontLabObservation → DecisionLifecycle /
SymbiontLabAdapter → EvolutionGate

A ponte exige execução COMPLETED, result_ref e evidência correspondente.
Ela não altera o estado do DecisionLifecycle; a transição para ATTRIBUTED
continua sendo responsabilidade do ciclo de decisão.

Não são inferidos hipótese, baseline, experimento, resultado, regressão ou
generalização. Esses campos precisam ser fornecidos explicitamente.
