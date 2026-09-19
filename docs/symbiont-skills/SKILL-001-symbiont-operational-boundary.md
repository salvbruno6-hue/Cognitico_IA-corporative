# SKILL-001 — Symbiont Operational Boundary

- **skill_id:** `symbiont.operational_boundary`
- **owner:** ELO Cognitive
- **executor:** Symbiont/Hermes sob contrato ELO
- **authority:** ELO Cognitive
- **status:** CANONICAL_BOUNDARY

## Função

Aplicar os limites operacionais para raciocínio externo governado: reconhecimento do mandato, autorização, escopo de tenant, operações não destrutivas, evidência, escalonamento humano e bloqueio de campos de autoridade/segredo.

## Relação na cadeia de ações

`intenção → ELO Cognitive → SymbiontRequestGuard → operação permitida → evidência/auditoria → decisão/outcome`

Não executa promoção de conhecimento.

## Permitido

- metadata_read
- read
- query
- scenario_sim
- risk_assess
- kpi_calc
- emissão de decision brief com evidência e auditoria

## Bloqueado

- write
- schema_change
- DDL
- DML
- decision_register concorrente
- mutação canônica
- transporte de secrets ou identificadores de infraestrutura

## Escalonamento

Deve exigir revisão humana quando houver baixa confiança, alto risco, conflito de canon, evidência insuficiente, impacto financeiro acima do limite ou PII presente sem mascaramento.

## Testes

Obrigatórios:

- ACK ausente → bloqueio;
- autorização ausente → bloqueio;
- operação destrutiva → bloqueio;
- campo secreto/autoridade → bloqueio;
- PII não mascarada → escalonamento;
- alto risco → escalonamento;
- limite financeiro excedido → escalonamento;
- decision brief sem evidência → bloqueio;
- mutação canônica solicitada → bloqueio.

## Saída

A saída é evidência/apoio à decisão, nunca decisão canônica por si só.

## Aprovação

A aprovação desta skill significa apenas que sua fronteira operacional está testada e conforme. Não autoriza novas capacidades fora desta especificação.
