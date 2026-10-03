-- Reutiliza as tabelas canônicas existentes para o ciclo
-- Comercial -> PCP -> RH. Não cria nova autoridade de demanda.
--
-- EVENTO, SPOT e SAZONALIDADE classificam a natureza da demanda.
-- chave_comparabilidade identifica a referência equivalente usada pelo PCP.

ALTER TABLE public.mt_pedidos_venda
  ADD COLUMN IF NOT EXISTS natureza_demanda text,
  ADD COLUMN IF NOT EXISTS chave_comparabilidade text;

ALTER TABLE public.mt_demanda_historico
  ADD COLUMN IF NOT EXISTS natureza_demanda text,
  ADD COLUMN IF NOT EXISTS chave_comparabilidade text;

ALTER TABLE public.mt_previsoes_demanda
  ADD COLUMN IF NOT EXISTS natureza_demanda text,
  ADD COLUMN IF NOT EXISTS chave_comparabilidade text;

COMMENT ON COLUMN public.mt_pedidos_venda.natureza_demanda IS
  'Classificação da demanda comercial para PCP: EVENTO, SPOT ou SAZONALIDADE. Não representa demanda de mão de obra.';

COMMENT ON COLUMN public.mt_pedidos_venda.chave_comparabilidade IS
  'Chave do evento, período sazonal ou grupo comparável usada pelo PCP para selecionar referência histórica equivalente.';

COMMENT ON COLUMN public.mt_demanda_historico.natureza_demanda IS
  'Natureza da demanda histórica: EVENTO, SPOT ou SAZONALIDADE.';

COMMENT ON COLUMN public.mt_demanda_historico.chave_comparabilidade IS
  'Identificador lógico do grupo/evento/período usado para comparabilidade histórica.';

COMMENT ON COLUMN public.mt_previsoes_demanda.natureza_demanda IS
  'Natureza da demanda prevista: EVENTO, SPOT ou SAZONALIDADE.';

COMMENT ON COLUMN public.mt_previsoes_demanda.chave_comparabilidade IS
  'Identificador lógico da referência comparável que fundamenta a previsão.';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'ck_mt_pedidos_venda_natureza_demanda'
      AND conrelid = 'public.mt_pedidos_venda'::regclass
  ) THEN
    ALTER TABLE public.mt_pedidos_venda
      ADD CONSTRAINT ck_mt_pedidos_venda_natureza_demanda
      CHECK (natureza_demanda IS NULL OR natureza_demanda IN ('EVENTO','SPOT','SAZONALIDADE'));
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'ck_mt_demanda_historico_natureza_demanda'
      AND conrelid = 'public.mt_demanda_historico'::regclass
  ) THEN
    ALTER TABLE public.mt_demanda_historico
      ADD CONSTRAINT ck_mt_demanda_historico_natureza_demanda
      CHECK (natureza_demanda IS NULL OR natureza_demanda IN ('EVENTO','SPOT','SAZONALIDADE'));
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'ck_mt_previsoes_demanda_natureza_demanda'
      AND conrelid = 'public.mt_previsoes_demanda'::regclass
  ) THEN
    ALTER TABLE public.mt_previsoes_demanda
      ADD CONSTRAINT ck_mt_previsoes_demanda_natureza_demanda
      CHECK (natureza_demanda IS NULL OR natureza_demanda IN ('EVENTO','SPOT','SAZONALIDADE'));
  END IF;
END $$;
