-- Cobertura de FKs da baseline executiva para evitar scans desnecessarios.
create index if not exists idx_pcp_dir_comercial_fonte_id
  on elo_private.pcp_diretoria_comercial_mensal (fonte_id);

create index if not exists idx_pcp_dir_comercial_tenant_id
  on elo_private.pcp_diretoria_comercial_mensal (tenant_id);