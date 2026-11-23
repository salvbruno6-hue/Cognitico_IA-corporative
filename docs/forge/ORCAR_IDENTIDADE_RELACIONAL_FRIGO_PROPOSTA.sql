-- PROPOSTA / EVOLUTION GATE: não executar sem validação
-- Vínculo por UUID entre identidades canônicas da Lista-Mãe e fichas de conhecimento.
-- Estado real verificado em 2026-11-05:
--   MON004 = PAINEL FRIGO PIRAP AP 40MM 1130X2650MM (ativo)
--   MON005 = PAINEL FRIGO PIRAP 32MM 1130X2310MM (ativo)
--   M13, MON006 e PEND-M01-018 removidos da lista_mae por consolidação autorizada.
--   Histórico dos três códigos preservado em public.lista_mae_alteracoes
--   sob operacao CONSOLIDACAO_EXCLUSAO_FRIGO_20261105.
--   Referências de kit corrigidas e verificadas.
-- Atenção: variantes antigas PIRAB/PIRAP não são automaticamente intercambiáveis.
-- Esta proposta NÃO foi executada no Supabase.
create table if not exists public.elo_material_conhecimento_vinculos (
 id uuid primary key default gen_random_uuid(),
 lista_mae_id uuid not null references public.lista_mae(id),
 conhecimento_item_id uuid not null references public.elo_conhecimento_itens(id),
 tipo_relacao text not null check (tipo_relacao in ('ITEM_EXATO','FAMILIA_VARIANTE','CANDIDATO_VALIDACAO')),
 status text not null check (status in ('CONFIRMADO','PENDENTE_VALIDACAO')),
 fonte text not null,
 created_at timestamptz not null default now(),
 unique(lista_mae_id, conhecimento_item_id)
);
-- Relações candidatas à validação:
--   MON004 -> MATERIAL_PAINEL_FRIGO_PIR_40MM
--   MON005 -> MATERIAL_PAINEL_FRIGO_PIR_32MM
-- A execução deve avaliar se relações genéricas existentes já cobrem o caso,
-- implementar RLS/políticas adequadas, validar aplicação por modelo e executar testes.
