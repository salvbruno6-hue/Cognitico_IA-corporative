alter table public.elo_orcamento_servicos_auxiliares add column if not exists codigo_curto text;
update public.elo_orcamento_servicos_auxiliares set codigo_curto=case codigo
 when 'AUX-MUNCK' then 'CMP-MUN'
 when 'AUX-APOIO' then 'CMP-APO'
 when 'AUX-EMPILHADEIRA' then 'CMP-EMP'
 when 'AUX-INTERLIG-ELETRICA-INT' then 'CMP-ELI'
 when 'AUX-INTERLIG-ELETRICA-EXT' then 'CMP-ELE'
 when 'AUX-INTERLIG-HIDRAULICA' then 'CMP-HID'
 when 'AUX-ALIMENTACAO' then 'CMP-ALI'
 when 'AUX-NIVELAMENTO' then 'CMP-NIV'
 when 'AUX-DESLOCAMENTO' then 'CMP-DES'
 when 'AUX-HOSPEDAGEM' then 'CMP-HOS'
 else codigo_curto end
where codigo in ('AUX-MUNCK','AUX-APOIO','AUX-EMPILHADEIRA','AUX-INTERLIG-ELETRICA-INT','AUX-INTERLIG-ELETRICA-EXT','AUX-INTERLIG-HIDRAULICA','AUX-ALIMENTACAO','AUX-NIVELAMENTO','AUX-DESLOCAMENTO','AUX-HOSPEDAGEM');
create unique index if not exists ux_elo_orc_aux_codigo_curto on public.elo_orcamento_servicos_auxiliares(codigo_curto);
alter table public.elo_orcamento_servicos_auxiliares add constraint ck_elo_orc_aux_codigo_curto_format check (codigo_curto is null or codigo_curto ~ '^CMP-[A-Z]{3}$');
update public.elo_orcamento_composicao_itens ci set linha_codigo=aux.codigo_curto,
 observacao=concat_ws(' | ',ci.observacao, 'Linha de triagem anterior: '||ci.linha_codigo)
from public.elo_orcamento_servicos_auxiliares aux
where ci.referencia_auxiliar_id=aux.id and ci.orcamento_id='SO 233.26'
and ci.modelo_codigo='MLT.M05' and ci.status='EM_ANALISE'
and ci.linha_codigo ~ '^REF[.]([0-9]+)$' and aux.codigo_curto is not null;
create or replace view public.vw_elo_orcamento_composicao_auxiliar with (security_invoker=true) as
select ci.orcamento_id,ci.modelo_codigo,ci.secao,ci.linha_codigo,aux.codigo_curto as codigo,
 aux.codigo as codigo_origem,ci.descricao,aux.valor_referencia,ci.quantidade,ci.unidade,
 ci.valor_unitario,ci.valor_parcial,ci.status,aux.status as status_referencia,
 ci.fonte,ci.memoria_decisao,ci.referencia_auxiliar_id
from public.elo_orcamento_composicao_itens ci
join public.elo_orcamento_servicos_auxiliares aux on ci.referencia_auxiliar_id=aux.id;
revoke all on public.vw_elo_orcamento_composicao_auxiliar from anon,authenticated;
comment on column public.elo_orcamento_servicos_auxiliares.codigo_curto is 'Código CMP-XXX da composição, preserva o codigo original AUX-...';
comment on view public.vw_elo_orcamento_composicao_auxiliar is 'Consulta relacional do código abreviado da composição, sem nova autoridade de preço.';
