-- PROPOSTA / EVOLUTION GATE: não executar sem validação
-- Vincula identidade canônica da lista_mae ao conhecimento detalhado.
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
-- A execução deve aplicar RLS/políticas adequadas ao contexto e testar permissões.
-- Relações propostas: M13 -> PIR 40 (item da família; validar identidade exata),
-- MON004/MON006 -> PIR 40 (variantes); MON005/PEND-M01-018 -> PIR 32 (variantes).
-- Não confundir PIRAP com PIRAB nem 1130 mm com 1300 mm.
