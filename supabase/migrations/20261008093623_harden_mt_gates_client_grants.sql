-- Owner: ELO governed operational gates / Supabase persistence.
-- Correct the unmatched wildcard grants from v6_rls_multiteiner_por_natureza.
-- mt_gates has RLS and no client policy, no rows, and no traced client consumer.
-- Preserve its existing owner/service_role authority and tenant constraints.
-- No new policy, RPC, capability, or client administrative authority is introduced.
REVOKE ALL ON TABLE public.mt_gates FROM PUBLIC, anon, authenticated;
