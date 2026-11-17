-- MLT.C — materialização da composição documental em estrutura_modular
-- Fonte canônica de materiais: public.lista_mae (Supabase).
-- Google Sheets é somente réplica de consulta e não participa da decisão de vínculo.
-- Nenhum registro criado por esta migração é operacional ou liberado para produção.

insert into public.estrutura_modular(
  codigo,nome,modelo_id,taxonomia_id,descricao,tipo,dimensao_referencia,
  quantidade_modulos,configuracao,observacoes,versao,ativo
)
select
  'ESTR-' || replace(m.codigo,'.','') || '-DOC',
  'Composição documental — ' || m.nome,
  m.id,
  m.taxonomia_id,
  'Estrutura documental derivada do Portfólio Técnico de Contêineres 20 pés. Representa somente itens alinhados à Lista Mãe canônica e presentes na BOM rascunho documental.',
  'DOCUMENTAL',
  null,
  1,
  'COMPOSICAO_DOCUMENTAL',
  'Não operacional. Fonte: Portfólio MLT.C 13/11/2026; BOM DOC-2026-11-13. Itens com GAP permanecem fora desta estrutura.',
  'DOC-2026-11-13',
  false
from public.modelos m
where m.codigo in ('MLT.C06','MLT.C10','MLT.C13','MLT.C20','MLT.C21','MLT.C25')
on conflict (codigo) do update
set nome=excluded.nome,
    modelo_id=excluded.modelo_id,
    taxonomia_id=excluded.taxonomia_id,
    descricao=excluded.descricao,
    tipo=excluded.tipo,
    dimensao_referencia=null,
    quantidade_modulos=excluded.quantidade_modulos,
    configuracao=excluded.configuracao,
    observacoes=excluded.observacoes,
    versao=excluded.versao,
    ativo=false,
    updated_at=now();

delete from public.estrutura_modular_itens emi
using public.estrutura_modular em
where emi.estrutura_modular_id=em.id
  and em.codigo in (
    'ESTR-MLTC06-DOC','ESTR-MLTC10-DOC','ESTR-MLTC13-DOC',
    'ESTR-MLTC20-DOC','ESTR-MLTC21-DOC','ESTR-MLTC25-DOC'
  );

with base as (
  select
    em.id as estrutura_modular_id,
    m.id as modelo_id,
    m.taxonomia_id,
    bi.lista_mae_id,
    bi.quantidade,
    bi.operacao_referencia,
    lm.cod_item,
    lm.cod_produt,
    lm.descricao_oficial,
    b.status as bom_status,
    row_number() over (
      partition by m.id
      order by coalesce(bi.operacao_referencia,''), lm.cod_item, lm.descricao_oficial
    )::integer as ordem
  from public.modelos m
  join public.estrutura_modular em
    on em.modelo_id=m.id
   and em.versao='DOC-2026-11-13'
   and em.tipo='DOCUMENTAL'
  join public.mt_versoes_bom b
    on b.modelo_id=m.id
   and b.versao='DOC-2026-11-13'
   and b.status='RASCUNHO_DOCUMENTAL'
  join public.mt_bom_itens bi
    on bi.bom_versao_id=b.id
  join public.lista_mae lm
    on lm.id=bi.lista_mae_id
   and lm.ativo is true
  where m.codigo in ('MLT.C13','MLT.C20','MLT.C21')
)
insert into public.estrutura_modular_itens(
  estrutura_modular_id,modelo_id,taxonomia_id,quantidade,posicao,funcao,
  observacao,ordem,ativo,lista_mae_id
)
select
  estrutura_modular_id,
  modelo_id,
  taxonomia_id,
  quantidade,
  'DOCUMENTAL',
  coalesce(operacao_referencia,'COMPOSICAO'),
  concat(
    'RASCUNHO_DOCUMENTAL; Lista Mãe canônica; item=',cod_item,
    case when cod_produt is null then '' else '; cod_produt='||cod_produt end,
    '; descrição=',descricao_oficial,
    '; origem=BOM DOC-2026-11-13; não liberado para produção.'
  ),
  ordem,
  false,
  lista_mae_id
from base;

create or replace view public.vw_elo_modelo_composicao_documental
with (security_invoker=true) as
select
  m.id as modelo_id,
  m.codigo as modelo_codigo,
  m.nome as modelo_nome,
  m.familia,
  em.id as estrutura_modular_id,
  em.codigo as estrutura_codigo,
  em.versao as estrutura_versao,
  em.tipo as estrutura_tipo,
  em.configuracao,
  em.ativo as estrutura_operacional,
  emi.id as estrutura_item_id,
  emi.ordem,
  emi.funcao as sistema,
  emi.posicao,
  emi.quantidade,
  emi.ativo as item_operacional,
  lm.id as lista_mae_id,
  lm.cod_item,
  lm.cod_produt,
  lm.descricao_oficial,
  lm.un,
  lm.valor_unitario,
  (emi.quantidade * coalesce(lm.valor_unitario,0)) as valor_parcial,
  emi.observacao
from public.estrutura_modular em
join public.modelos m on m.id=em.modelo_id
left join public.estrutura_modular_itens emi
  on emi.estrutura_modular_id=em.id
left join public.lista_mae lm
  on lm.id=emi.lista_mae_id
where em.tipo='DOCUMENTAL'
  and em.versao='DOC-2026-11-13';

comment on view public.vw_elo_modelo_composicao_documental is
'Composição documental por modelo baseada exclusivamente em public.lista_mae e BOM DOC-2026-11-13. Registros inativos não representam liberação produtiva.';

update public.elo_conhecimento_itens e
set conteudo=jsonb_set(
      e.conteudo,
      '{integracao_estrutura_modular}',
      jsonb_build_object(
        'versao','DOC-2026-11-13',
        'estrutura_codigo',
          case e.chave_unica
            when 'PORTFOLIO_MLTC06_20261113' then 'ESTR-MLTC06-DOC'
            when 'PORTFOLIO_MLTC10_20261113' then 'ESTR-MLTC10-DOC'
            when 'PORTFOLIO_MLTC13_20261113' then 'ESTR-MLTC13-DOC'
            when 'PORTFOLIO_MLTC20_20261113' then 'ESTR-MLTC20-DOC'
            when 'PORTFOLIO_MLTC21_20261113' then 'ESTR-MLTC21-DOC'
            when 'PORTFOLIO_MLTC25_20261113' then 'ESTR-MLTC25-DOC'
          end,
        'estado','DOCUMENTAL_INATIVO',
        'regra','Somente itens presentes na Lista Mãe canônica e na BOM RASCUNHO_DOCUMENTAL são materializados. Itens com GAP não entram.'
      ),
      true
    ),
    updated_at=now()
where e.chave_unica in (
  'PORTFOLIO_MLTC06_20261113','PORTFOLIO_MLTC10_20261113',
  'PORTFOLIO_MLTC13_20261113','PORTFOLIO_MLTC20_20261113',
  'PORTFOLIO_MLTC21_20261113','PORTFOLIO_MLTC25_20261113'
);

update public.elo_conhecimento_itens
set conteudo=jsonb_set(
      conteudo,
      '{integracao_estrutura_modular}',
      jsonb_build_object(
        'versao','DOC-2026-11-13',
        'estruturas_documentais',6,
        'itens_materializados',26,
        'operacionais',false,
        'fonte_lista_mae','public.lista_mae',
        'regra_google_sheets','Réplica de consulta; divergência com Supabase é GAP e Supabase prevalece.'
      ),
      true
    ),
    updated_at=now()
where chave_unica='FAMILIA_MLTC_DRY_ADAPTADO';

insert into public.tb_elo_eventos_governanca(
  evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes
)
select
  'MATERIALIZACAO_ESTRUTURA_DOCUMENTAL_MLTC_20261117',
  'FORGE_COMPOSICAO_MODELO',
  'ELO',
  'FORGE_PRODUTOS',
  'DOCUMENTAL_INATIVO',
  'MLTC_ESTRUTURA_DOC_20261117',
  jsonb_build_object(
    'versao','DOC-2026-11-13',
    'estruturas',6,
    'itens',26,
    'fonte_lista_mae','public.lista_mae',
    'google_sheets','replica_nao_canonica',
    'regra','Somente itens alinhados à Lista Mãe e BOM rascunho são materializados; nenhuma estrutura ou item é ativado.'
  )
where not exists (
  select 1
  from public.tb_elo_eventos_governanca
  where evento='MATERIALIZACAO_ESTRUTURA_DOCUMENTAL_MLTC_20261117'
    and referencia='MLTC_ESTRUTURA_DOC_20261117'
);