# ELO — Authentication Session Bridge Acceptance

| Scenario | Expected result |
|---|---|
| Valid Google/Supabase session, active ELO identity | Existing active ELO authorization session is reused or a new one is created |
| Valid Google/Supabase session, no ELO identity | Bridge fails closed with `ELO_IDENTITY_REQUIRED` |
| No Supabase authentication | Identity/session RPC cannot be established |
| Anonymous caller invokes session RPC | Execution denied |
| Active authorization session | `last_seen_at` is refreshed and the same session remains authoritative |
| Expired authorization session | A new ELO authorization session is created |
| Logout | ELO authorization sessions are revoked before Supabase sign-out |
| Role/capability/scope decision | Remains exclusively under `elo-authz` |
| Cognitive/application session | Remains downstream and distinct from authentication/authorization |

## Validation evidence

The migration was applied to the ELO-forge Supabase project and the resulting RPC privileges were inspected. The session functions are `SECURITY DEFINER`, use a fixed `search_path`, require `auth.uid()`, and are executable by `authenticated` but not `anon`.
