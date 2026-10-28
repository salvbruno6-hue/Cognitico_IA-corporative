-- Evidence-ranked FK index for the cognitive learning model.
-- Live evidence before this migration:
--   public.elo_aprendizado_conceitos: n_live_tup=20, seq_scan=94, writes=27
--   FK elo_aprendizado_conceitos_especializacao_id_fkey had no leading index.
-- Tiny tables (4-8 rows) with frequent seq scans are intentionally not indexed.

create index if not exists idx_elo_aprendizado_conceitos_especializacao_id
  on public.elo_aprendizado_conceitos (especializacao_id);

comment on index public.idx_elo_aprendizado_conceitos_especializacao_id is
  'Evidence-ranked FK index. Added only after the relation-learning workload crossed the health threshold; tiny-table FK paths remain intentionally unindexed until workload evidence justifies them.';
