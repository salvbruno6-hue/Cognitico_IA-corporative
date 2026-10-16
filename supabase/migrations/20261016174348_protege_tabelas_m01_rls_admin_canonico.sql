-- Protege tabelas operacionais do MLT.M01 via RLS.
-- Leitura: usuários autenticados.
-- Escrita: identidade administrativa canônica reconhecida por
-- elo_private.has_capability('PCP_ADMIN').

alter table public.estrutura_metalica_20_componentes enable row level security;
alter table public.mt_tempo_fabricacao_estrutura_modular enable row level security;
alter table public.mt_mao_obra_solda_preparacao_estrutura_modular enable row level security;
alter table public.mt_mao_obra_kit_eletrico_m01 enable row level security;
alter table public.mt_mao_obra_montagem_estrutura_modular_20 enable row level security;

revoke all on table public.estrutura_metalica_20_componentes from anon, authenticated;
revoke all on table public.mt_tempo_fabricacao_estrutura_modular from anon, authenticated;
revoke all on table public.mt_mao_obra_solda_preparacao_estrutura_modular from anon, authenticated;
revoke all on table public.mt_mao_obra_kit_eletrico_m01 from anon, authenticated;
revoke all on table public.mt_mao_obra_montagem_estrutura_modular_20 from anon, authenticated;

grant select, insert, update, delete on table public.estrutura_metalica_20_componentes to authenticated;
grant select, insert, update, delete on table public.mt_tempo_fabricacao_estrutura_modular to authenticated;
grant select, insert, update, delete on table public.mt_mao_obra_solda_preparacao_estrutura_modular to authenticated;
grant select, insert, update, delete on table public.mt_mao_obra_kit_eletrico_m01 to authenticated;
grant select, insert, update, delete on table public.mt_mao_obra_montagem_estrutura_modular_20 to authenticated;

create policy p_m01_est_comp_select on public.estrutura_metalica_20_componentes
for select to authenticated using (true);
create policy p_m01_est_comp_insert on public.estrutura_metalica_20_componentes
for insert to authenticated with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_est_comp_update on public.estrutura_metalica_20_componentes
for update to authenticated
using ((select elo_private.has_capability('PCP_ADMIN')))
with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_est_comp_delete on public.estrutura_metalica_20_componentes
for delete to authenticated using ((select elo_private.has_capability('PCP_ADMIN')));

create policy p_m01_tempo_fab_select on public.mt_tempo_fabricacao_estrutura_modular
for select to authenticated using (true);
create policy p_m01_tempo_fab_insert on public.mt_tempo_fabricacao_estrutura_modular
for insert to authenticated with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_tempo_fab_update on public.mt_tempo_fabricacao_estrutura_modular
for update to authenticated
using ((select elo_private.has_capability('PCP_ADMIN')))
with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_tempo_fab_delete on public.mt_tempo_fabricacao_estrutura_modular
for delete to authenticated using ((select elo_private.has_capability('PCP_ADMIN')));

create policy p_m01_mo_solda_select on public.mt_mao_obra_solda_preparacao_estrutura_modular
for select to authenticated using (true);
create policy p_m01_mo_solda_insert on public.mt_mao_obra_solda_preparacao_estrutura_modular
for insert to authenticated with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_mo_solda_update on public.mt_mao_obra_solda_preparacao_estrutura_modular
for update to authenticated
using ((select elo_private.has_capability('PCP_ADMIN')))
with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_mo_solda_delete on public.mt_mao_obra_solda_preparacao_estrutura_modular
for delete to authenticated using ((select elo_private.has_capability('PCP_ADMIN')));

create policy p_m01_mo_eletrico_select on public.mt_mao_obra_kit_eletrico_m01
for select to authenticated using (true);
create policy p_m01_mo_eletrico_insert on public.mt_mao_obra_kit_eletrico_m01
for insert to authenticated with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_mo_eletrico_update on public.mt_mao_obra_kit_eletrico_m01
for update to authenticated
using ((select elo_private.has_capability('PCP_ADMIN')))
with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_mo_eletrico_delete on public.mt_mao_obra_kit_eletrico_m01
for delete to authenticated using ((select elo_private.has_capability('PCP_ADMIN')));

create policy p_m01_mo_montagem_select on public.mt_mao_obra_montagem_estrutura_modular_20
for select to authenticated using (true);
create policy p_m01_mo_montagem_insert on public.mt_mao_obra_montagem_estrutura_modular_20
for insert to authenticated with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_mo_montagem_update on public.mt_mao_obra_montagem_estrutura_modular_20
for update to authenticated
using ((select elo_private.has_capability('PCP_ADMIN')))
with check ((select elo_private.has_capability('PCP_ADMIN')));
create policy p_m01_mo_montagem_delete on public.mt_mao_obra_montagem_estrutura_modular_20
for delete to authenticated using ((select elo_private.has_capability('PCP_ADMIN')));
