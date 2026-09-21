---
artifact_id: ELO-EXTERNAL-AI-AUTHORITY-CONTRACT
title: External AI Authority Contract
family: 09-governance
layer: governance
type: policy
status: normative
owner: ELO Governance
version: 1.0.0
reconciles:
  - 09-governance/contracts/standards/ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md
  - 09-governance/contracts/policies/ELO_AUTHORIZED_ACCESS_POLICY.md
  - 09-governance/contracts/standards/ELO_AUTHORIZED_SPECIALIST_ACCESS_STANDARD.md
  - RFC 9728 (OAuth 2.0 Protected Resource Metadata)
implements:
  - supabase/functions/elo-authz
  - supabase/functions/elo-mcp
  - elo_identity_registry
  - elo_audit_log
related:
  - ADR-0013-external-ai-authority-contract
  - ADR-0012-decision-outcome-loop
---

# ELO External AI Authority Contract

## 1. Propósito

Definir a autoridade concedida a qualquer IA externa que acesse o
ELO por qualquer superfície (MCP, API, agente integrado).

Este contrato **não cria novo mecanismo de autorização**. Ele
**documenta** a autoridade real já mediada por `elo-authz`, pelo
`elo_identity_registry`, pelo role `ELO_ADMIN` e pelo RFC 9728.

## 2. Autoridade real (o que já existe)

A autoridade de uma IA externa é determinada por seis camadas:

1. **Identidade** — JWT OAuth 2.1 emitido por Supabase Auth
2. **Binding** — registro ativo em `elo_identity_registry`
3. **Role** — `ELO_ADMIN` (para ELO-MCP) ou tier equivalente
4. **Autorização** — decisão de `elo-authz` por operação
5. **Auditoria** — todo evento em `elo_audit_log`
6. **Escopo** — allowlist de tabelas, tools e operações

Nenhuma dessas camadas é nova. Este contrato apenas as
reconhece e as consolida como a autoridade oficial.

## 3. Níveis de autoridade

| Tier | Escopo | MCP habilitado | Escrita |
|---|---|---|---|
| `READ` | Consulta a views e tabelas allowlist | ELO-MCP (read-only) | ❌ |
| `ANALYZE` | Consulta + tools cognitivas read-only | ELO-MCP + HERMES-MCP | ❌ |
| `PROPOSE` | Emite `decision_brief`, registra em memória | + SYMBIONT-MCP | ❌ |
| `OPERATE` | Aprova, executa, reverte | superfícies completas | ✅ via gateway |

**Regra:** nenhum tier acima de `READ` é concedido
automaticamente. Cada concessão exige atualização de
`elo_identity_registry` + ADR.

## 4. Deveres da IA externa

1. Ler este contrato antes de qualquer operação.
2. Preservar proveniência em toda leitura.
3. Declarar incerteza em toda recomendação.
4. Nunca inferir autoridade de escrita a partir de conexão.
5. Nunca representar leitura como fato sem evidência.
6. Registrar toda ação cognitiva.
7. Consultar precedentes antes de propor decisão.
8. Respeitar `ELO_EXTERNAL_INFORMATION_BOUNDARY.md`.
9. Respeitar `ELO_READ_ONLY_CONSULTATION_PROTOCOL.md`.
10. Escalar para humano quando confiança calibrada < limiar.

## 5. Proibições

- Escrever em tabelas fora de allowlist
- Executar DDL/DML via MCP
- Assumir autoridade de ELO CORE
- Usar `department` como fronteira de segurança
- Persistir aprendizado sem `evolution_gate`
- Omitir auditoria
- Expor PII fora de escopo autorizado

## 6. Revogação

Por desativação em `elo_identity_registry`, remoção de role,
ordem de governança ou detecção de violação.
Efeito: `403 forbidden` de `elo-authz`.

## 7. Reconciliação com RFC 9728

Discovery em
`/functions/v1/elo-mcp/oauth-protected-resource`,
token OAuth 2.1, `Authorization: Bearer`, `WWW-Authenticate` em 401.

## 8. Conformidade

Estende `ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md` e
`ELO_AUTHORIZED_ACCESS_POLICY.md`. Não substitui `elo-authz`.
Não cria novo mecanismo.

## 9. Vigência

Vigente com `ADR-0013`. Alterações exigem ADR próprio.
---