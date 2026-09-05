-- ELO / Supabase security hardening
-- The material-suggestion RPC is read-only, but it is an ELO/Forge
-- knowledge interface and must not be callable anonymously.
-- Authorization for privileged ELO operations remains canonical in elo-authz.

REVOKE EXECUTE ON FUNCTION public.elo_orcamento_sugerir_materiais(text, text, text, integer)
FROM anon;

-- Keep authenticated access as an infrastructure read path only.
-- This migration does not grant write or promotion authority.
COMMENT ON FUNCTION public.elo_orcamento_sugerir_materiais(text, text, text, integer)
IS 'Read-only Forge material suggestion query. Anonymous execution denied. Does not authorize, arbitrate, promote, or commit ELO learning; privileged ELO authorization remains owned by elo-authz.';
