-- ELO PCP: estado persistente do diálogo de coleta e validação.
-- O orquestrador conduz a coleta, registra a resposta original e os dados
-- estruturados fornecidos pelo GPT, mas não transforma ausência em hipótese.

create schema if not exists elo_private;

create table if not exists elo_private.pcp_dialogo_turnos (
  id uuid primary key default gen_random_uuid(),
  sessao_id uuid not null,
  turno integer not null,
  actor_user_id uuid,
  gap_codigo text not null,
  gate text not null,
  resposta_original text,
  dados_fornecidos jsonb not null default '{}'::jsonb,
  fonte_informada text,
  estado text not null default 'RECEBIDO' check (estado in ('RECEBIDO','VALIDADO','PENDENTE','REJEITADO')),
  campos_validos jsonb not null default '[]'::jsonb,
  campos_faltantes jsonb not null default '[]'::jsonb,
  mensagem_orquestrador text,
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now(),
  unique (sessao_id, turno)
);

alter table elo_private.pcp_dialogo_turnos enable row level security;

create index if not exists idx_pcp_dialogo_turnos_sessao
  on elo_private.pcp_dialogo_turnos (sessao_id, turno desc);

create index if not exists idx_pcp_dialogo_turnos_gap
  on elo_private.pcp_dialogo_turnos (gap_codigo, criado_em desc);

comment on table elo_private.pcp_dialogo_turnos is
'Estado persistente do diálogo do Orquestrador ELO para coleta governada de dados PCP. Registra resposta original, dados estruturados, validação e próxima orientação. Não é autoridade normativa nem substitui as tabelas operacionais.';

comment on column elo_private.pcp_dialogo_turnos.resposta_original is
'Resposta literal recebida do usuário; preservada para rastreabilidade e nunca reinterpretada como fato sem validação.';

comment on column elo_private.pcp_dialogo_turnos.dados_fornecidos is
'Dados estruturados explicitamente extraídos pelo canal GPT da resposta do usuário. Campos ausentes permanecem ausentes.';

comment on column elo_private.pcp_dialogo_turnos.fonte_informada is
'Fonte indicada pelo usuário para o dado. A indicação não substitui a validação da fonte autorizada pelo gate.';

create or replace view public.v_elo_pcp_dialogo_regras
with (security_invoker = true)
as
select
  codigo as gap_codigo,
  gate,
  prioridade,
  fonte_autorizada,
  pergunta_gpt,
  motivo,
  bloqueia_execucao,
  campos_obrigatorios
from public.v_elo_pcp_dados_pendentes
order by prioridade, codigo;

comment on view public.v_elo_pcp_dialogo_regras is
'Regras de diálogo derivadas da fila canônica de dados pendentes. O orquestrador deve conduzir um gap por vez, começando pelo primeiro bloqueante, e não pode inferir campos ausentes.';
