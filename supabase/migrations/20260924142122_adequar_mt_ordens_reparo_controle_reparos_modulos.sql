alter table public.mt_ordens_reparo
  alter column tenant_id drop not null,
  alter column status set default 'ABERTA';

alter table public.mt_ordens_reparo
  add column if not exists numero_container text,
  add column if not exists tipo_modulo text,
  add column if not exists observacoes text,
  add column if not exists data_final_reparo date;

create index if not exists idx_mt_ordens_reparo_data_final_reparo
  on public.mt_ordens_reparo (data_final_reparo);

create index if not exists idx_mt_ordens_reparo_numero_container
  on public.mt_ordens_reparo (numero_container);
