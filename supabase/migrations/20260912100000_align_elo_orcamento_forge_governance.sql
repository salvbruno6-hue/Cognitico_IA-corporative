-- ELO Cognitivo / Forge: governança das associações e decisões de orçamento.
-- As tabelas já existentes são reutilizadas; não criar autoridade paralela.
-- O estado inicial deliberado permanece sem registros: associação=0, decisão=0.

CREATE INDEX IF NOT EXISTS ix_elo_orcamento_associacoes_contexto
  ON public.elo_orcamento_associacoes (aplicacao, necessidade, status);

CREATE INDEX IF NOT EXISTS ix_elo_orcamento_associacoes_lista_mae
  ON public.elo_orcamento_associacoes (lista_mae_id);

CREATE INDEX IF NOT EXISTS ix_elo_orcamento_decisoes_associacao
  ON public.elo_orcamento_decisoes (associacao_id);

CREATE INDEX IF NOT EXISTS ix_elo_orcamento_decisoes_orcamento
  ON public.elo_orcamento_decisoes (orcamento_id);

CREATE INDEX IF NOT EXISTS ix_elo_orcamento_decisoes_contexto
  ON public.elo_orcamento_decisoes (aplicacao, necessidade, decisao);

COMMENT ON TABLE public.elo_orcamento_associacoes IS
  'Camada Forge do ELO Cognitivo: associa contexto e necessidade a item canonico. Nao e autoridade independente e nao promove aprendizado sem decisao arbitrada.';

COMMENT ON TABLE public.elo_orcamento_decisoes IS
  'Governanca do ELO Cognitivo sobre associacoes de orcamento. Registra somente decisoes reais/arbitradas; nao deve ser preenchida por inferencia.';

COMMENT ON COLUMN public.elo_orcamento_associacoes.ultima_decisao IS
  'Ultima decisao arbitrada aplicavel a associacao; nao e inferencia automatica.';

COMMENT ON COLUMN public.elo_orcamento_decisoes.arbitrado_por IS
  'Ator que efetivamente arbitrou a decisao; nao preencher por inferencia.';
