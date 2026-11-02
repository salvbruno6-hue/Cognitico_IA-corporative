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
  v_final_count integer;
BEGIN
  -- Serialize the audited zero-assignment precondition through the insert and
  -- postconditions. SHARE ROW EXCLUSIVE blocks concurrent INSERT/UPDATE/DELETE
  -- on the role-capability relation while this transaction is active.
  LOCK TABLE public.elo_role_capabilities IN SHARE ROW EXCLUSIVE MODE;

  SELECT role_id
  INTO v_role_id
  FROM public.elo_roles
  WHERE code = 'CANONICAL_ADMIN'
    AND active = true
  FOR UPDATE;

  IF v_role_id IS NULL THEN
    RAISE EXCEPTION 'CANONICAL_ADMIN active role missing; recovery aborted';
  END IF;

  -- Lock the exact baseline capability rows so they cannot be deactivated or
  -- altered concurrently after the catalog preflight.
  PERFORM capability_id
  FROM public.elo_capabilities
  WHERE code IN ('READ', 'ADMIN', 'CANONICAL_WRITE', 'APPROVE')
  FOR SHARE;

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
    AND c.code IN ('READ', 'ADMIN', 'CANONICAL_WRITE', 'APPROVE');

  SELECT count(*)::integer
  INTO v_final_count
  FROM public.elo_role_capabilities rc
  WHERE rc.role_id = v_role_id;

  IF v_final_count <> 4 THEN
    RAISE EXCEPTION
      'CANONICAL_ADMIN recovery produced unexpected assignment count: expected 4, observed %',
      v_final_count;
  END IF;

  IF EXISTS (
    SELECT 1
    FROM public.elo_role_capabilities rc
    JOIN public.elo_capabilities c ON c.capability_id = rc.capability_id
    WHERE rc.role_id = v_role_id
      AND (
        c.active IS DISTINCT FROM true
        OR c.code NOT IN ('READ', 'ADMIN', 'CANONICAL_WRITE', 'APPROVE')
      )
  ) THEN
    RAISE EXCEPTION 'CANONICAL_ADMIN recovery produced capability set outside canonical baseline';
  END IF;

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
