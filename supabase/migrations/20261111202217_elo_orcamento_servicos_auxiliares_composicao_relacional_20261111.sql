-- Migration aplicada em produção via Supabase MCP em 2026-11-11; versão retornada 20261111202217.
-- Relaciona núcleo de conhecimento de orçamento, referências auxiliares e linhas da composição.
create table if not exists public.elo_orcamento_servicos_auxiliares (
 id uuid primary key default gen_random_uuid(),
 codigo text not null unique,
 nucleo_id uuid not null references public.elo_conhecimento_nucleos(id),
 descricao text not null,
 categoria text not null,
 valor_referencia numeric(14,2) check (valor_referencia is null or valor_referencia >= 0),
 unidade text,
 condicao_aplicacao text,
 fonte text not null,
 status text not null default 'REFERENCIA_NAO_HOMOLOGADA'
   check (status in ('REFERENCIA_NAO_HOMOLOGADA','VALIDADO','INATIVO')),
 observacao text,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now()
);
create index if not exists ix_elo_orc_serv_aux_nucleo on public.elo_orcamento_servicos_auxiliares(nucleo_id,status);
create table if not exists public.elo_orcamento_composicao_itens (
 id uuid primary key default gen_random_uuid(),
 orcamento_id text not null references public.elo_orcamentos(orcamento_id),
 modelo_codigo text,
 secao text not null check (secao in ('2.1','2.2','2.3','2.4')),
 linha_codigo text not null,
 descricao text not null,
 referencia_auxiliar_id uuid references public.elo_orcamento_servicos_auxiliares(id),
 cod_item text,
 codigo_excedente text,
 quantidade numeric(14,4) check (quantidade is null or quantidade >= 0),
 unidade text,
 valor_unitario numeric(14,2) check (valor_unitario is null or valor_unitario >= 0),
 valor_parcial numeric(16,2) generated always as
  (case when quantidade is not null and valor_unitario is not null then round(quantidade * valor_unitario,2) else null end) stored,
 status text not null default 'EM_ANALISE'
  check (status in ('EM_ANALISE','APLICADO','NAO_APLICAVEL','REJEITADO')),
 fonte text,
 memoria_decisao text,
 observacao text,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 constraint uq_elo_orc_composicao_linha unique (orcamento_id,modelo_codigo,secao,linha_codigo),
 constraint ck_elo_orc_composicao_aplicado check (status <> 'APLICADO' or (quantidade is not null and valor_unitario is not null and fonte is not null and memoria_decisao is not null))
);
create index if not exists ix_elo_orc_comp_orcamento on public.elo_orcamento_composicao_itens(orcamento_id,modelo_codigo,secao,status);
create index if not exists ix_elo_orc_comp_referencia on public.elo_orcamento_composicao_itens(referencia_auxiliar_id);
alter table public.elo_orcamento_servicos_auxiliares enable row level security;
alter table public.elo_orcamento_composicao_itens enable row level security;
revoke all on public.elo_orcamento_servicos_auxiliares from anon, authenticated;
revoke all on public.elo_orcamento_composicao_itens from anon, authenticated;
comment on table public.elo_orcamento_servicos_auxiliares is 'Catálogo governado de referências laterais da planilha ORÇAR; nenhuma referência gera custo automaticamente. Vinculado ao núcleo CONHECIMENTO_ORCAMENTO.';
comment on table public.elo_orcamento_composicao_itens is 'Linhas de composição por orçamento e modelo. A referência auxiliar é opcional e só status APLICADO com memória permite inclusão no orçamento.';
insert into public.elo_orcamento_servicos_auxiliares
 (codigo,nucleo_id,descricao,categoria,valor_referencia,unidade,condicao_aplicacao,fonte,observacao)
select d.codigo,n.id,d.descricao,d.categoria,d.valor,d.unidade,d.condicao,
 'SO 233.26 — tabela auxiliar fornecida pelo Analista em conversa, 11/11/2026',
 'Transcrição contextual em homologação; verificar seta/destino, condição, unidade e fonte original antes de aplicar'
from public.elo_conhecimento_nucleos n
cross join (values
 ('AUX-MUNCK','Caminhão Munck','LOGISTICA',1400.00::numeric,null::text,'Aplicação/quantidade via Logística → Comercial; não duplicar descarga'),
 ('AUX-APOIO','Carro de apoio','LOGISTICA',220.00::numeric,null::text,'Sincronizar com dias de mobilização externa e hospedagem'),
 ('AUX-EMPILHADEIRA','Empilhadeira','LOGISTICA',null::numeric,null::text,'Somente se necessidade comprovada'),
 ('AUX-INTERLIG-ELETRICA-INT','Interligação elétrica interna','SERVICO',800.00::numeric,null::text,'Confirmar destino das setas e escopo; prevenir duplicidade com EXC'),
 ('AUX-INTERLIG-ELETRICA-EXT','Interligação elétrica externa a cada 2 módulos','SERVICO',1200.00::numeric,null::text,'Condição a cada 2 módulos; confirmar atendimento aplicável'),
 ('AUX-INTERLIG-HIDRAULICA','Interligação hidráulica','SERVICO',null::numeric,null::text,'Requer projeto e responsabilidade de execução'),
 ('AUX-ALIMENTACAO','Despesas com alimentação','MOBILIZACAO',25.00::numeric,null::text,'Unidade e equipe ainda não comprovadas'),
 ('AUX-NIVELAMENTO','Serviço de nivelamento até 15 cm','SERVICO',250.00::numeric,null::text,'Somente conforme vistoria/necessidade'),
 ('AUX-DESLOCAMENTO','Deslocamento','MOBILIZACAO',1.53::numeric,null::text,'Unidade/distância não comprovadas'),
 ('AUX-HOSPEDAGEM','Hospedagem','MOBILIZACAO',null::numeric,null::text,'Indicada referência textual 160/256, sem preço inequívoco')
) as d(codigo,descricao,categoria,valor,unidade,condicao)
where n.codigo = 'CONHECIMENTO_ORCAMENTO'
on conflict (codigo) do nothing;
