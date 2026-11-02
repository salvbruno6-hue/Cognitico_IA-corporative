-- CANDIDATE ONLY — NOT AN OFFICIAL MIGRATION / NOT AUTHORIZED FOR LIVE DDL.
-- Related: #1143, ADR-0017.
--
-- Purpose:
--   Contain the live drift where ELO_ADMIN/CANONICAL_ADMIN currently satisfy
--   every p_code passed to elo_private.has_capability().
--
-- Boundaries:
--   * preserve normal explicit identity -> role -> capability semantics;
--   * preserve only the acknowledged legacy PCP_ADMIN administrative path;
--   * do not create PCP_ADMIN;
--   * do not assign any capability;
--   * do not mutate operational rows or policies.

CREATE SCHEMA IF NOT EXISTS elo_private;

CREATE OR REPLACE FUNCTION elo_private.has_capability(p_code text)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
  SELECT
    CASE
      WHEN p_code = 'PCP_ADMIN' THEN
        EXISTS (
          SELECT 1
          FROM public.elo_identity_registry i
          JOIN public.elo_identity_roles ir ON ir.identity_id = i.identity_id
          JOIN public.elo_roles r
            ON r.role_id = ir.role_id
           AND r.active = true
          WHERE i.auth_user_id = auth.uid()
            AND i.active = true
            AND r.code IN ('ELO_ADMIN', 'CANONICAL_ADMIN')
        )
      ELSE
        EXISTS (
          SELECT 1
          FROM public.elo_identity_registry i
          JOIN public.elo_identity_roles ir ON ir.identity_id = i.identity_id
          JOIN public.elo_roles r
            ON r.role_id = ir.role_id
           AND r.active = true
          JOIN public.elo_role_capabilities rc ON rc.role_id = r.role_id
          JOIN public.elo_capabilities c
            ON c.capability_id = rc.capability_id
           AND c.active = true
          WHERE i.auth_user_id = auth.uid()
            AND i.active = true
            AND c.code = p_code
        )
    END;
$$;

REVOKE ALL ON FUNCTION elo_private.has_capability(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION elo_private.has_capability(text) TO authenticated;

COMMENT ON FUNCTION elo_private.has_capability(text)
IS 'Canonical ELO RLS capability resolver. Normal codes require explicit role-capability assignment. PCP_ADMIN is a bounded transitional compatibility path for active ELO_ADMIN/CANONICAL_ADMIN roles per ADR-0017/#1143; it remains unresolved technical debt and is not a catalog capability.';
