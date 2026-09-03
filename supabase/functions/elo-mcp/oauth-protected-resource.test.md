# ELO MCP Protected Resource Contract

Expected behavior after RFC 9728 hardening:

- `GET /functions/v1/elo-mcp` returns the MCP server metadata.
- `GET /functions/v1/elo-mcp/oauth-protected-resource` returns JSON metadata containing the MCP resource and Supabase authorization server.
- Unauthenticated `POST /functions/v1/elo-mcp` returns HTTP 401.
- The 401 response contains `WWW-Authenticate` with `resource_metadata` pointing to `/oauth-protected-resource`.
- Authenticated MCP requests still require an active ELO identity and active `ELO_ADMIN` role.
- The MCP surface remains read-only: only `elo_status` and `elo_read` are exposed.
