# RFC 9728 implementation status

Implemented in `index.ts`:

- Protected Resource Metadata endpoint.
- `authorization_servers` pointing to Supabase Auth.
- `WWW-Authenticate` resource metadata challenge on 401.
- Existing ELO_ADMIN authentication preserved.
- Existing read-only MCP tool boundary preserved.

Integration validation still requires the deployed Supabase endpoint and OAuth 2.1 server to be enabled/configured.
