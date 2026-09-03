# ELO MCP RFC 9728

The MCP endpoint exposes OAuth Protected Resource Metadata at `/oauth-protected-resource` and advertises the Supabase Auth OAuth 2.1 authorization server.

Unauthenticated MCP POST requests return `401` with a `resource_metadata` URL in `WWW-Authenticate`.

The authenticated MCP boundary remains restricted to the active `ELO_ADMIN` identity and read-only tools.
