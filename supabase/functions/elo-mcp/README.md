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
