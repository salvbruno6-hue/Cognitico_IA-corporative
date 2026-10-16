-- Permite que policies RLS chamem elo_private.has_capability(text)
-- para usuários autenticados.
--
-- elo_private.has_capability(text) já concede EXECUTE a authenticated.
-- elo_private.read_rls_state(text[]) permanece restrita ao service_role.
-- Sem USAGE no schema, a policy falha antes de avaliar a autorização.

grant usage on schema elo_private to authenticated;
