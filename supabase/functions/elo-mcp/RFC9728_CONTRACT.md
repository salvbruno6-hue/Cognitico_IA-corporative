# ELO MCP RFC 9728 Contract

The ELO MCP resource exposes OAuth Protected Resource Metadata at:

`/functions/v1/elo-mcp/oauth-protected-resource`

The metadata identifies the MCP resource and the Supabase Auth OAuth 2.1 authorization server. Unauthenticated MCP requests return HTTP 401 with a `WWW-Authenticate` challenge containing the `resource_metadata` URL.

The authenticated MCP surface remains restricted to the active `ELO_ADMIN` identity and read-only tools.
