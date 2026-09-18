# ELO — Reconciliação editável de estados e códigos MCP/external data

Status: proposta canônica em reconciliação
Base: material de referência fornecido para MCP + Mandato + Skill
Objetivo: impedir que códigos do desenho MCP criem uma segunda autoridade de estados, memória ou auditoria.

## Regra de reconciliação

Os códigos do material de referência são tratados como contrato de integração editável. Um código só se torna canônico quando há implementação, teste e compatibilidade com a arquitetura existente.

As classificações usadas aqui são:

- EXISTENTE: já possui autoridade/semântica canônica comprovada.
- REUTILIZAR: existe mecanismo equivalente; não criar outro.
- EXTENDER: ampliar mecanismo existente sem mudar sua autoridade.
- PENDENTE: material propõe o código, mas a implementação canônica ainda não está comprovada nesta linha de integração.
- BLOQUEADO: proposta criaria duplicidade, bypass ou autoridade paralela.

## Matriz

| Código/estado do material | Dono canônico | Classificação | Ajuste |
|---|---|---|---|
| requires_ack | mandato/MCP/Symbiont governance contract | EXTENDER | O ACK é pré-condição de operação; não é nova identidade nem nova autorização. Implementado como guarda fail-closed no contrato do Symbiont. |
| ack | mandato/MCP/Symbiont governance contract | EXTENDER | Associar ao request/session/mandate version e bloquear tools antes do ACK. Envelope governado exige request_id e tenant_scope compatíveis. |
| decision_brief | Core/decisão | REUTILIZAR | Tratar como formato de saída; não criar novo registro histórico concorrente. |
| confidence >= 0.70 | governança cognitiva/Symbiont governance contract | EXTENDER | Contrato do Symbiont consolida o limiar de confiança para seu boundary; não substitui os critérios específicos já existentes. |
| human escalation | governança/autoridade/Symbiont governance contract | REUTILIZAR | Avaliação consolidada apenas classifica a necessidade; a autoridade de escalonamento permanece existente. |
| sql_query_readonly | adapter/MCP | EXTENDER | Para fontes externas, usar fonte registrada + operação query; não expor SQL arbitrário. |
| kpi_calc | Core/cálculo | PENDENTE | Só incorporar após localizar owner canônico e testes; o cálculo deve operar sobre dados já autorizados. |
| scenario_sim | MultiScenarioGate/Scenario | REUTILIZAR | Reusar Scenario e MultiScenarioGate; não criar segundo motor de cenários. |
| risk_assess | reasoning/governance/Symbiont governance contract | EXTENDER | Integrar avaliação de risco existente; o limiar financeiro é contextual e nenhum valor é inventado. |
| decision_register | DecisionRecord/OutcomeFeedback | BLOQUEADO | Não criar um segundo ledger. |
| memory/decisions.jsonl | memória/decisão | BLOQUEADO | Não substituir nem concorrer com a memória/DecisionRecord canônica. |
| memory/mcp_audit.jsonl | auditoria ELO | BLOQUEADO | Preferir elo_audit_log e elo_authorization_audit. |
| metadata_read | external data | EXISTENTE | Operação governada. |
| read | external data | EXISTENTE | Operação governada. |
| query | external data | EXISTENTE | Operação governada. |
| write | external data | EXISTENTE | Permitido apenas por decisão explícita de autorização; bloqueado por padrão. |
| schema_change | external data | EXISTENTE | Permitido apenas por decisão explícita de autorização; bloqueado por padrão. |
| ENTERPRISE_EXTERNAL | external data source | EXISTENTE | Fonte externa empresarial. |
| USER_EXTERNAL | external data source | EXISTENTE | Fonte externa vinculada ao usuário/escopo. |
| INTEGRATION | external data source | EXISTENTE | Fonte de integração. |
| credential_ref | external data source | EXISTENTE | Apenas referência; segredo fica fora do ELO Core e do repositório. |
| connection_ref | external data source | EXISTENTE | Apenas referência operacional. |
| LAB_ONLY | Symbiont Lab | EXISTENTE | Evidência laboratorial não é conhecimento canônico. |
| CANDIDATE_FOR_GOVERNED_LEARNING | Symbiont/Learning Governance | REUTILIZAR | Candidato segue Evolution Gate e aprovação exigida. |
| DUPLICATE/SUPERSEDED | Evolution Gate | REUTILIZAR | Reuso em vez de nova memória/implementação. |
| ADAPT_REQUIRED | Evolution Gate | REUTILIZAR | Fortalecer evidência/compatibilidade antes de promoção. |
| INCOMPATIBLE | Evolution Gate | REUTILIZAR | Bloqueio governado. |
| UNCONFIRMED | Symbiont Lab | EXISTENTE | Atualmente bloqueia captura de aprendizado; mudança de semântica exige alteração explícita do contrato/testes. |

## Estados de ciclo decisório

O material não deve introduzir uma segunda máquina de estados. Quando o Decision Outcome Loop for incorporado à linha canônica, seus estados permanecem no owner do Core:

PROPOSED -> APPROVED -> EXECUTED -> OBSERVING -> EVALUATED -> ATTRIBUTED -> LEARNED -> CLOSED

Com rotas governadas de ESCALATED e REVERTED.

Importante: LEARNED, nesse fluxo, não significa promoção automática a conhecimento canônico. O resultado do Symbiont é candidato/evidência até cumprir Learning Governance + Evolution Gate + aprovação exigida.

## Estado da integração externa

Para esta linha, o estado operacional externo é deliberadamente separado do estado cognitivo:

REQUESTED -> AUTHORIZED -> EXECUTING -> SUCCEEDED | FAILED | DENIED

Esses estados descrevem transporte/operação, não aprendizado nem autoridade decisória. O resultado bem-sucedido gera evidência/proveniência e retorna ao fluxo cognitivo existente.

## Guardas obrigatórios

ACK válido, identidade ativa, sessão ELO válida quando exigida, tenant/scope compatível, fonte ACTIVE, operação explicitamente autorizada, credential_ref resolvível, ausência de segredo no resultado/auditoria e proveniência preservada.

Falha em qualquer guarda deve ser fail-closed.

## Regra de edição

Esta matriz pode ser alterada quando uma divergência for encontrada. A alteração deve identificar: código afetado, owner canônico, evidência da implementação, testes que comprovam a semântica e impacto sobre contratos existentes.

Nenhum código desta matriz cria por si só uma nova autoridade.


## Ajuste implementado — contrato operacional do Symbiont

Foi adicionada uma camada de contrato em
`src/elo/cognitive/symbiont_governance_contract.py`, sem criar nova autoridade.

Ela consolida quatro guardas que estavam dispersas no desenho:
- acknowledgement de mandato;
- formato mínimo de `DecisionBrief`;
- confiança mínima de 0.70 para esse boundary;
- avaliação de escalonamento por confiança, risco, conflito canônico, evidência insuficiente, limite financeiro contextual, ação irreversível ou exposição de PII.

O contrato não autoriza, promove, persiste conhecimento nem decide por uma autoridade superior.

O caminho Hermes Skill ganhou um envelope governado que exige ACK compatível com `request_id` e `tenant_scope` antes da execução.

Os testes correspondentes ficam em:
`tests/evolution/test_symbiont_governance_contract.py`
e
`tests/evolution/test_hermes_skill_runtime_governance.py`.

Esses ajustes são preparação de contrato e testes. A validação operacional/CI ainda não foi declarada como concluída.
