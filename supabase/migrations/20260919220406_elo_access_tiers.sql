-- ELO Web access tiers: collaborator and visitor.
-- Collaborator: consultation + insertion into Lista-Mãe; no GitHub repository binding.
-- Visitor: consultation only; no GitHub repository binding.
-- No identity is auto-provisioned by this migration.

INSERT INTO public.elo_roles (code, name, active)
VALUES
  ('COLABORADOR', 'Colaborador', true),
  ('VISITANTE', 'Visitante', true)
ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name, active = true;

INSERT INTO public.elo_capabilities (code, name, description, active)
VALUES
  ('LISTA_MAE_INSERT', 'Lista-Mãe — inclusão', 'Inserção de novos registros na Lista-Mãe; sem alteração ou exclusão de registros existentes.', true)
ON CONFLICT (code) DO UPDATE
SET name = EXCLUDED.name, description = EXCLUDED.description, active = true;

INSERT INTO public.elo_role_capabilities (role_id, capability_id)
SELECT r.role_id, c.capability_id
FROM public.elo_roles r
CROSS JOIN public.elo_capabilities c
WHERE r.code = 'COLABORADOR'
  AND c.code IN ('PORTAL_READ', 'PCP_READ', 'LISTA_MAE_INSERT')
ON CONFLICT DO NOTHING;

INSERT INTO public.elo_role_capabilities (role_id, capability_id)
SELECT r.role_id, c.capability_id
FROM public.elo_roles r
CROSS JOIN public.elo_capabilities c
WHERE r.code = 'VISITANTE'
  AND c.code = 'PORTAL_READ'
ON CONFLICT DO NOTHING;

-- Internal authorization helper for RLS. It is deliberately outside the exposed API surface.
CREATE SCHEMA IF NOT EXISTS elo_private;

CREATE OR REPLACE FUNCTION elo_private.has_capability(p_code text)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.elo_identity_registry i
    JOIN public.elo_identity_roles ir ON ir.identity_id = i.identity_id
    JOIN public.elo_roles r ON r.role_id = ir.role_id AND r.active = true
    JOIN public.elo_role_capabilities rc ON rc.role_id = r.role_id
    JOIN public.elo_capabilities c ON c.capability_id = rc.capability_id AND c.active = true
    WHERE i.auth_user_id = auth.uid()
      AND i.active = true
      AND c.code = p_code
  );
$$;

REVOKE ALL ON FUNCTION elo_private.has_capability(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION elo_private.has_capability(text) TO authenticated;

-- lista_mae is an exposed public table and must enforce the access model at the database boundary.
ALTER TABLE public.lista_mae ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "elo_lista_mae_select_consultation" ON public.lista_mae;
CREATE POLICY "elo_lista_mae_select_consultation"
ON public.lista_mae
FOR SELECT
TO authenticated
USING (
  elo_private.has_capability('PCP_READ')
);

DROP POLICY IF EXISTS "elo_lista_mae_insert_collaborator" ON public.lista_mae;
CREATE POLICY "elo_lista_mae_insert_collaborator"
ON public.lista_mae
FOR INSERT
TO authenticated
WITH CHECK (
  elo_private.has_capability('LISTA_MAE_INSERT')
);

-- No UPDATE or DELETE policy is created for COLABORADOR.
-- VISITANTE has PORTAL_READ but intentionally has no direct Lista-Mãe database capability.

COMMENT ON FUNCTION elo_private.has_capability(text)
IS 'Canonical ELO authorization helper for exposed-table RLS. Resolves identity -> role -> capability from canonical ELO tables using auth.uid().';

COMMENT ON TABLE public.lista_mae
IS 'Lista-Mãe. COLABORADOR may INSERT only when granted LISTA_MAE_INSERT; SELECT requires PCP_READ. No collaborator UPDATE/DELETE policy.';
