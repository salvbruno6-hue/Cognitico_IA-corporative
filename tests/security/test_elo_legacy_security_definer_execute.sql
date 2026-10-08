-- Regression evidence for privileged SECURITY DEFINER execution boundaries.
-- These functions must not be directly executable by Data API principals.

DO $$
DECLARE
  fn regprocedure;
BEGIN
  FOREACH fn IN ARRAY ARRAY[
    'public.elo_aprendizado_classificar_experiencia(text,text,text,text,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,text,numeric)'::regprocedure,
    'public.elo_aprendizado_extrair_fontes()'::regprocedure,
    'public.elo_aprendizado_gerar_conceitos_e_padroes()'::regprocedure,
    'public.elo_aprendizado_gerar_relacoes()'::regprocedure,
    'public.lista_mae_guard()'::regprocedure
  ]
  LOOP
    IF has_function_privilege('anon', fn, 'EXECUTE') THEN
      RAISE EXCEPTION 'anon unexpectedly has EXECUTE on %', fn;
    END IF;
    IF has_function_privilege('authenticated', fn, 'EXECUTE') THEN
      RAISE EXCEPTION 'authenticated unexpectedly has EXECUTE on %', fn;
    END IF;
  END LOOP;
END
$$;

DO $$
DECLARE
  fn regprocedure;
BEGIN
  FOREACH fn IN ARRAY ARRAY[
    'public.elo_aprendizado_classificar_experiencia(text,text,text,text,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,text,numeric)'::regprocedure,
    'public.elo_aprendizado_extrair_fontes()'::regprocedure,
    'public.elo_aprendizado_gerar_conceitos_e_padroes()'::regprocedure,
    'public.elo_aprendizado_gerar_relacoes()'::regprocedure
  ]
  LOOP
    IF NOT has_function_privilege('service_role', fn, 'EXECUTE') THEN
      RAISE EXCEPTION 'service_role unexpectedly lacks EXECUTE on %', fn;
    END IF;
  END LOOP;
END
$$;
