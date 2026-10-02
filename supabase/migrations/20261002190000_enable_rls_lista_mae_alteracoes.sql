-- ELO governance: close exposed audit table without inventing a read policy.
-- ADR/governance contract expects RLS ON with no policies (fail-closed).
-- The audit trigger writes through lista_mae_guard(), which is SECURITY DEFINER.

ALTER TABLE public.lista_mae_alteracoes ENABLE ROW LEVEL SECURITY;
