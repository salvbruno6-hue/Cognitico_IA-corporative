-- ELO: cover the destination-side foreign key for knowledge links.
-- No data mutation; this only adds the missing performance index identified by the Supabase advisor.
create index if not exists idx_elo_conhecimento_vinculos_item_destino_id
  on public.elo_conhecimento_vinculos (item_destino_id);
