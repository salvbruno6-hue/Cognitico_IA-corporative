# ELO Decision Intelligence Lifecycle v1.0

**Status:** Normativo
**Baseline:** ELO Core Architecture Baseline v1.0

## 1. Objetivo
Formalizar o ciclo de vida de decisões do ELO sem confundir raciocínio, recomendação, autorização, execução e resultado.

## 2. Fluxo canônico
`DecisionContext -> EvidenceSet -> Recommendation -> DecisionRequest -> PolicyEvaluation -> Approval (quando exigida) -> Decision -> ExecutionReference (quando aplicável) -> Outcome -> LearningReference`

## 3. Contratos
### DecisionContext
Referencia Tenant, Domain, Principal, Session/Context, objetivo, restrições e políticas aplicáveis.

### EvidenceSet
Conjunto rastreável de evidências utilizadas. Cada evidência deve manter origem e provenance.

### Recommendation
Artefato derivado do Reasoning. Não autoriza ação por si só.

### DecisionRequest
Pedido explícito de decisão contendo alternativas, evidências, risco, impacto e nível de autonomia permitido.

### Decision
Registro governado contendo `decision_id`, `tenant_id`, domínio, responsável, decisão, justificativa, evidências, políticas, timestamps, provenance e estado.

### Outcome
Resultado observado após uma decisão ou execução. Não altera retroativamente o registro da decisão; gera nova evidência e pode alimentar aprendizagem governada.

## 4. Estados mínimos
`proposed`, `under_review`, `approved`, `rejected`, `executed`, `cancelled`, `superseded`.

## 5. Regras de governança
- Recommendation não equivale a Decision.
- Decision não equivale a execução.
- Ações críticas exigem política e aprovação compatíveis.
- Ausência de autorização explícita deve resultar em negação quando a política exigir aprovação.
- Decisões devem ser imutáveis quanto ao fato histórico; correções são registradas por supersessão ou novos eventos.
- Evidências e políticas usadas devem ser recuperáveis para auditoria.

## 6. Provenance
A cadeia mínima deve permitir reconstruir `source -> evidence -> reasoning/recommendation -> decision -> outcome`.

## 7. Observabilidade
Registrar latência, estado, políticas avaliadas, aprovações, confiança declarada, falhas e correlação com execução/outcome sem expor conteúdo sensível indevido.

## 8. Fora de escopo
Este documento não define workflow engine, mecanismo de aprovação específico, UI, provedor de IA ou executor externo.
