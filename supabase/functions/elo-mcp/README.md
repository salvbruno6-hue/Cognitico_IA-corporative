# ELO MCP

Remote MCP boundary for ELO.

Authentication: Supabase Auth OAuth 2.1 / Bearer JWT.
Authorization: active ELO_ADMIN identity.
Operations: read-only.

Protected Resource Metadata is exposed under `/oauth-protected-resource` for MCP OAuth discovery.

---

## Contrato de Autoridade

A autoridade de qualquer IA externa que acesse este MCP é
definida em:

- [`09-governance/contracts/policies/ELO_EXTERNAL_AI_AUTHORITY_CONTRACT.md`](../../../09-governance/contracts/policies/ELO_EXTERNAL_AI_AUTHORITY_CONTRACT.md)
- [`10-adr/ADR-0013-external-ai-authority-contract.md`](../../../10-adr/ADR-0013-external-ai-authority-contract.md)

Tiers: `READ`, `ANALYZE`, `PROPOSE`, `OPERATE`.
Este MCP opera no tier `READ` (read-only).

---

## Mapa canônico

O ELO possui três superfícies MCP documentadas em:

- [`05-cognitive-platform/MCP_CANONICAL_MAP.md`](../../../05-cognitive-platform/MCP_CANONICAL_MAP.md)

Este é o MCP canônico de leitura empresarial (tier `READ`).
HERMES-MCP (`ANALYZE`) e SYMBIONT-MCP (`PROPOSE`) são os
outros dois.

---

## Cognitive read-only tools (v0.2.0)

Além de `elo_status` e `elo_read`, o ELO-MCP expõe três tools
cognitivas read-only:

| Tool | Projeção | Fonte canônica |
|---|---|---|
| `elo_dol_read` | `elo_dol_projection` | `memory/` (DOL) |
| `elo_calibration_read` | `elo_calibration_model` | `memory/calibration/` |
| `elo_precedent_search` | `elo_precedent_index` | `memory/precedents/` |

Todas passam pelo mesmo caminho de autorização (`elo-authz` +
`elo_identity_registry`), são auditadas em `elo_audit_log` e não
permitem escrita.

As projeções são populadas por job externo a partir das fontes
canônicas em `memory/`. Se a projeção ainda não existir, a tool
retorna vazio com nota apontando para a fonte canônica.

Refs: `10-adr/ADR-0014-cognitive-runtime-loop.md`
