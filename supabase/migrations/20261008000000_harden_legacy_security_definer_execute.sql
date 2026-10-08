-- Harden legacy SECURITY DEFINER functions that still inherit EXECUTE from PUBLIC.
-- Canonical boundary: privileged learning and trigger functions are not public RPCs.
-- service_role remains the explicit execution principal for learning maintenance.

REVOKE ALL ON FUNCTION public.elo_aprendizado_classificar_experiencia(text,text,text,text,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,text,numeric)
  FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.elo_aprendizado_classificar_experiencia(text,text,text,text,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,text,numeric)
  TO service_role;

REVOKE ALL ON FUNCTION public.elo_aprendizado_extrair_fontes()
  FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.elo_aprendizado_extrair_fontes()
  TO service_role;

REVOKE ALL ON FUNCTION public.elo_aprendizado_gerar_conceitos_e_padroes()
  FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.elo_aprendizado_gerar_conceitos_e_padroes()
  TO service_role;

REVOKE ALL ON FUNCTION public.elo_aprendizado_gerar_relacoes()
  FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.elo_aprendizado_gerar_relacoes()
  TO service_role;

-- Trigger functions are invoked by PostgreSQL triggers, not directly by clients.
REVOKE ALL ON FUNCTION public.lista_mae_guard()
  FROM PUBLIC, anon, authenticated;
