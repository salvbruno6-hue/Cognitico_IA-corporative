-- CANDIDATE ONLY — NOT AN OFFICIAL MIGRATION / NOT AUTHORIZED FOR LIVE DML/DDL.
-- Related: #1143, #1137.
--
-- Purpose:
-- Recover the exact canonical authorization baseline for CANONICAL_ADMIN after
-- verified live drift. This is a recovery of existing authority, not a grant of
-- new strategic/delegated authority.
--
-- Canonical source:
-- supabase/migrations/20260912195000_elo_authorization_schema_baseline.sql
--
-- Exact baseline capability set for CANONICAL_ADMIN:
-- READ, ADMIN, CANONICAL_WRITE, APPROVE.
-- PROPOSE and REVIEW are intentionally NOT assigned here; they are delegable
-- strategic capabilities and require a separate explicit governance decision.

DO $$
DECLARE
  v_role_id uuid;
  v_existing_count integer;
  v_required_count integer;
BEGIN
  SELECT role_id
  INTO v_role_id
  FROM public.elo_roles
  WHERE code = 'CANONICAL_ADMIN'
    AND active = true;

  IF v_role_id IS NULL THEN
    RAISE EXCEPTION 'CANONICAL_ADMIN active role missing; recovery aborted';
  END IF;

  SELECT count(*)::integer
  INTO v_existing_count
  FROM public.elo_role_capabilities rc
  WHERE rc.role_id = v_role_id;

  -- This candidate is bound to the audited 2026-11-02 drift state.
  -- Any partial repair or later change requires re-analysis instead of guessing.
  IF v_existing_count <> 0 THEN
    RAISE EXCEPTION
      'CANONICAL_ADMIN capability state changed: expected 0 assignments, observed %; re-analysis required',
      v_existing_count;
  END IF;

  SELECT count(*)::integer
  INTO v_required_count
  FROM public.elo_capabilities c
  WHERE c.active = true
    AND c.code IN ('READ', 'ADMIN', 'CANONICAL_WRITE', 'APPROVE');

  IF v_required_count <> 4 THEN
    RAISE EXCEPTION
      'Canonical baseline capability catalog incomplete: expected 4 active capabilities, observed %',
      v_required_count;
  END IF;

  INSERT INTO public.elo_role_capabilities (role_id, capability_id)
  SELECT v_role_id, c.capability_id
  FROM public.elo_capabilities c
  WHERE c.active = true
    AND c.code IN ('READ', 'ADMIN', 'CANONICAL_WRITE', 'APPROVE')
  ON CONFLICT DO NOTHING;

  IF (
    SELECT count(*)
    FROM public.elo_role_capabilities rc
    JOIN public.elo_capabilities c ON c.capability_id = rc.capability_id
    WHERE rc.role_id = v_role_id
      AND c.active = true
      AND c.code IN ('READ', 'ADMIN', 'CANONICAL_WRITE', 'APPROVE')
  ) <> 4 THEN
    RAISE EXCEPTION 'CANONICAL_ADMIN baseline recovery incomplete';
  END IF;

  IF EXISTS (
    SELECT 1
    FROM public.elo_role_capabilities rc
    JOIN public.elo_capabilities c ON c.capability_id = rc.capability_id
    WHERE rc.role_id = v_role_id
      AND c.code IN ('PROPOSE', 'REVIEW')
  ) THEN
    RAISE EXCEPTION 'Delegable strategic capability was unexpectedly assigned by baseline recovery';
  END IF;
END;
$$;
