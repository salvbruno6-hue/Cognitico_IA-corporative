# Validation plan

1. GET the MCP endpoint and confirm metadata is returned.
2. GET `/oauth-protected-resource` and confirm `resource` and `authorization_servers`.
3. POST without Bearer and expect 401 with `resource_metadata` in `WWW-Authenticate`.
4. POST with an invalid Bearer and expect 401.
5. POST with a valid non-admin identity and expect 403.
6. POST with the active ELO_ADMIN token and confirm `initialize`, `tools/list`, `elo_status`, and `elo_read` remain available.
7. Confirm no write or schema-changing MCP tools are exposed.
