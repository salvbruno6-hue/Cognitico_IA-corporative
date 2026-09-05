-- Verification for 20260905120000_harden_elo_orcamento_suggestion_execute.sql
-- Expected: anon has no EXECUTE privilege; authenticated remains read-only at
-- the function level and does not gain any ELO authorization/promotion power.

SELECT
  has_function_privilege(
    'anon',
    'public.elo_orcamento_sugerir_materiais(text,text,text,integer)',
    'EXECUTE'
  ) AS anon_can_execute,
  has_function_privilege(
    'authenticated',
    'public.elo_orcamento_sugerir_materiais(text,text,text,integer)',
    'EXECUTE'
  ) AS authenticated_can_execute;

-- Acceptance:
-- anon_can_execute = false
-- authenticated_can_execute = true
