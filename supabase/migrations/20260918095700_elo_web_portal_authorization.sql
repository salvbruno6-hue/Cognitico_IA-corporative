-- ELO Web portal authorization extension.
-- Reuses the canonical identity/role/capability/scope tables.
-- No authorization table is created here.

ALTER TABLE public.elo_identity_registry
  ADD COLUMN IF NOT EXISTS authorized_email text;

UPDATE public.elo_identity_registry r
SET authorized_email = lower(trim(u.email))
FROM auth.users u
WHERE u.id = r.auth_user_id
  AND coalesce(trim(u.email), '') <> ''
  AND (r.authorized_email IS NULL OR trim(r.authorized_email) = '');

ALTER TABLE public.elo_identity_registry
  DROP CONSTRAINT IF EXISTS elo_identity_registry_google_email_required;

ALTER TABLE public.elo_identity_registry
  ADD CONSTRAINT elo_identity_registry_google_email_required
  CHECK (provider <> 'google' OR authorized_email IS NOT NULL);

CREATE UNIQUE INDEX IF NOT EXISTS ux_elo_identity_registry_authorized_email
  ON public.elo_identity_registry (lower(authorized_email))
  WHERE authorized_email IS NOT NULL;

COMMENT ON COLUMN public.elo_identity_registry.authorized_email
IS 'Canonical ELO authorization binding for the authenticated provider email. For Google identities, must match auth.users.email; frontend never supplies this value.';

INSERT INTO public.elo_capabilities (code, name, description, active)
VALUES
  ('PORTAL_READ', 'Portal operacional — consulta', 'Consulta operacional autorizada no ELO Web.', true),
  ('ALMX_READ', 'Almoxarifado — consulta', 'Consulta de estoque físico do Almoxarifado.', true),
  ('ALMX_INSERT', 'Almoxarifado — entrada', 'Registro de entradas no estoque físico, mediante escopo de área.', true),
  ('ALMX_UPDATE', 'Almoxarifado — movimentação', 'Registro/alteração de movimentações de estoque, mediante escopo de área.', true),
  ('ALMX_ADJUST', 'Almoxarifado — ajuste', 'Ajuste de estoque físico, mediante permissão explícita de área.', true),
  ('PCP_READ', 'PCP — consulta', 'Consulta da Lista-Mãe e dados de concepção/PCP.', true),
  ('PCP_UPDATE', 'PCP — alteração', 'Alteração da Lista-Mãe/concepção, mediante permissão explícita.', true)
ON CONFLICT (code) DO NOTHING;
