# ELO — Matriz de Convergência da Plataforma

## Status

`NORMATIVE / ACTIVE`

## Objetivo

Coordenar a evolução simultânea das camadas sem transformar trabalho paralelo em arquiteturas paralelas.

| Frente | Reutilizar | Ajuste atual | Próxima evidência |
|---|---|---|---|
| Casa | Workspace Contract | identidade + tenant + sessão | fluxo autenticado |
| Cognitive | ExecutionRouter | integração com IntelligenceRouter | rota executável |
| AI | AIProvider/OpenAI adapter | conexão ao router | POC real |
| Context/Memory | contextual memory | composição por missão | isolamento |
| Evidence | provenance existente | registrar execução externa | rastreabilidade |
| Budget | budgeting + guias existentes | primeira missão simbiótica | orçamento reproduzível |
| Learning | learning governance | laboratório separado | experiência registrada |
| Agents | GovernedAgentRuntime | alimentar missão/resultado | ciclo completo |
| Workflow | governed workflow | observar resultado/aprender | execução rastreável |
| Integrations | interoperability layer | providers por adapter | POC/decisão |
| Workspace | corporate workspace contract | UI sobre capacidades existentes | usuário autenticado |
| Evolution | dashboard contract | métricas de ciclo | evidência histórica |

## Regra de sincronização

Cada frente pode avançar independentemente no código, mas só é considerada convergida quando seus contratos de entrada/saída são compatíveis com as demais frentes.

## Ordem operacional do primeiro ciclo integrado

`IDENTITY → MISSION → CONTEXT → CAPABILITY → ROUTE → PROVIDER → EVIDENCE → REASONING → AUTHORIZATION → EXECUTION → OUTCOME → EXPERIENCE → VALIDATION → EVOLUTION`.

O ciclo deve ser testado primeiro com uma missão de orçamento, sem transformar conhecimento específico da empresa em Core geral.
