-- MLT.C — segunda onda de consolidação documental
-- Autoridade: public.lista_mae (Supabase). Google Sheets é réplica.
-- Generaliza aplicação somente onde a especificação dos documentos C20/C21 é equivalente ao item existente.
-- Mantém conflitos de unidade, faseamento e detalhes de fornecimento fora da BOM.

update public.lista_mae
set modelos_aplicaveis = case cod_item
  when 'PEND-C13-001' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-002' then 'MLT.C13; MLT.C21'
  when 'PEND-C13-003' then 'MLT.C13; MLT.C21'
  when 'PEND-C13-004' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-005' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-006' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-007' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-008' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-010' then 'MLT.C13; MLT.C20; MLT.C21'
  when 'PEND-C13-011' then 'MLT.C13; MLT.C20; MLT.C21'
  else modelos_aplicaveis
end,
updated_at=now()
where cod_item in (
 'PEND-C13-001','PEND-C13-002','PEND-C13-003','PEND-C13-004','PEND-C13-005',
 'PEND-C13-006','PEND-C13-007','PEND-C13-008','PEND-C13-010','PEND-C13-011'
);

with mapa(modelo_codigo,ordem,cod_item,promover,confianca,situacao,justificativa) as (
 values
 ('MLT.C20',62,'ELE034',true,0.98,'ALINHADO_DOCUMENTAL','Quadro PVC para 1 disjuntor alinhado ao ELE034; C20 é bifásico e o conflito 4A/10A não altera o invólucro do quadro.'),
 ('MLT.C20',63,'PEND-C13-001',true,1.00,'ALINHADO_DOCUMENTAL','Bocal louça 150W E27 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',66,'PEND-C13-004',true,1.00,'ALINHADO_DOCUMENTAL','Caixa Dailete alumínio 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',67,'PEND-C13-005',true,1.00,'ALINHADO_DOCUMENTAL','Tampa cega 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',68,'PEND-C13-006',true,1.00,'ALINHADO_DOCUMENTAL','Unidute alumínio 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',69,'PEND-C13-007',true,1.00,'ALINHADO_DOCUMENTAL','Abraçadeira tipo unha 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',70,'PEND-C13-008',true,1.00,'ALINHADO_DOCUMENTAL','Luva de correr 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',72,'ELE052',false,1.00,'MAPEADO_COM_GAP_UNIDADE','Condutor preto 2,5mm² identificado, porém a fonte usa UN e a Lista Mãe usa MT; não promover sem unidade validada.'),
 ('MLT.C20',73,'ELE053',false,1.00,'MAPEADO_COM_GAP_UNIDADE','Condutor verde 2,5mm² identificado, porém a fonte usa UN e a Lista Mãe usa MT; não promover sem unidade validada.'),
 ('MLT.C20',74,'PEND-C13-010',true,1.00,'ALINHADO_DOCUMENTAL','Curva 90° galvanizada 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),
 ('MLT.C20',76,'PEND-C13-011',true,1.00,'ALINHADO_DOCUMENTAL','Parafuso 1/2 com porca para aterramento documentalmente equivalente; aplicabilidade ampliada pela evidência C20.'),

 ('MLT.C21',78,'ELE034',false,0.95,'MAPEADO_COM_GAP_DOCUMENTAL','Quadro para 1 disjuntor identificado, porém o modelo mantém GAP de faseamento bifásico × monofásico.'),
 ('MLT.C21',79,'PEND-C13-001',true,1.00,'ALINHADO_DOCUMENTAL','Bocal louça 150W E27 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',80,'PEND-C13-002',true,1.00,'ALINHADO_DOCUMENTAL','Interruptor 1 seção 10A com tampa documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',81,'PEND-C13-003',true,1.00,'ALINHADO_DOCUMENTAL','Box reto 3/4 em alumínio com arruelas documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',82,'PEND-C13-004',true,1.00,'ALINHADO_DOCUMENTAL','Caixa Dailete alumínio 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',83,'PEND-C13-005',true,1.00,'ALINHADO_DOCUMENTAL','Tampa cega 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',84,'PEND-C13-006',true,1.00,'ALINHADO_DOCUMENTAL','Unidute alumínio 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',85,'PEND-C13-007',true,1.00,'ALINHADO_DOCUMENTAL','Abraçadeira tipo unha 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',86,'PEND-C13-008',true,1.00,'ALINHADO_DOCUMENTAL','Luva de correr 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',88,'ELE052',false,1.00,'MAPEADO_COM_GAP_UNIDADE','Condutor preto 2,5mm² identificado, porém a fonte usa UN e a Lista Mãe usa MT; não promover sem unidade validada.'),
 ('MLT.C21',89,'ELE053',false,1.00,'MAPEADO_COM_GAP_UNIDADE','Condutor verde 2,5mm² identificado, porém a fonte usa UN e a Lista Mãe usa MT; não promover sem unidade validada.'),
 ('MLT.C21',90,'PEND-C13-010',true,1.00,'ALINHADO_DOCUMENTAL','Curva 90° galvanizada 3/4 documentalmente equivalente; aplicabilidade ampliada pela evidência C21.'),
 ('MLT.C21',92,'PEND-C13-011',true,1.00,'ALINHADO_DOCUMENTAL','Parafuso 1/2 com porca para aterramento documentalmente equivalente; aplicabilidade ampliada pela evidência C21.')
),
res as (
 select ki.id as kit_item_id,m.codigo modelo_codigo,map.*,lm.id lista_mae_id,lm.cod_produt,lm.descricao_oficial,lm.un,lm.valor_unitario
 from mapa map
 join public.modelos m on m.codigo=map.modelo_codigo
 join public.kits k on k.modelo_id=m.id and k.versao='DOC-2026-11-13'
 join public.kit_itens ki on ki.kit_id=k.id and ki.ordem=map.ordem
 join public.lista_mae lm on lm.cod_item=map.cod_item and lm.ativo is true
)
update public.kit_itens ki
set lista_mae_id=res.lista_mae_id,
    cod_item=res.cod_item,
    cod_produt=res.cod_produt,
    descricao_oficial=res.descricao_oficial,
    un=res.un,
    valor_unitario=res.valor_unitario,
    valor_total=ki.quantidade*coalesce(res.valor_unitario,0),
    vinculo_status=case when res.promover then 'LOCALIZADO' else 'DIVERGENTE' end,
    vinculo_confianca=res.confianca,
    vinculo_observacao=res.justificativa,
    elo_situacao=res.situacao,
    elo_confianca=res.confianca,
    elo_justificativa=res.justificativa,
    vinculo_at=now()
from res
where ki.id=res.kit_item_id;

delete from public.kit_itens ki
using public.kits k, public.modelos m
where ki.kit_id=k.id and k.modelo_id=m.id
  and m.codigo in ('MLT.C20','MLT.C21')
  and ki.elo_referencia in (
   'PORTFOLIO_MLTC20_20261113|ARQ|PORTA_PRINCIPAL',
   'PORTFOLIO_MLTC21_20261113|ARQ|PORTA_PRINCIPAL'
  );

insert into public.kit_itens(
 kit_id,lista_mae_id,quantidade,instalacao,observacao,fase,obrigatoriedade,modelos_aplicaveis,
 cod_item,versao,ativo,cod_produt,descricao_oficial,un,qtd_uni,quant_total,valor_unitario,valor_total,
 fonte,ordem,vinculo_status,vinculo_confianca,vinculo_observacao,elo_situacao,elo_confianca,
 elo_justificativa,elo_referencia,snapshot_origem,snapshot_at,vinculo_at
)
select
 k.id,lm.id,1,'ARQUITETURA',
 'Porta principal 800x2100 documentada no modelo e alinhada ao item canônico ESQ001.',
 'DOCUMENTAL','DOCUMENTAL_NAO_LIBERADO',m.codigo,
 lm.cod_item,'DOC-2026-11-13',false,lm.cod_produt,lm.descricao_oficial,lm.un,1,1,
 lm.valor_unitario,lm.valor_unitario,
 case m.codigo when 'MLT.C20' then 'Prancha ARQ C20' else 'Prancha ARQ C21' end,
 1,'LOCALIZADO',1.00,'Dimensão 800x2100 consistente na documentação e ESQ001 aplicável a Todos.',
 'ALINHADO_DOCUMENTAL',1.00,
 'Porta principal 800x2100 consistente na documentação; vínculo direto ao ESQ001.',
 case m.codigo when 'MLT.C20' then 'PORTFOLIO_MLTC20_20261113|ARQ|PORTA_PRINCIPAL'
               else 'PORTFOLIO_MLTC21_20261113|ARQ|PORTA_PRINCIPAL' end,
 'descricao=Porta principal 800x2100; qtd=1; fonte=ARQ',
 now(),now()
from public.modelos m
join public.kits k on k.modelo_id=m.id and k.versao='DOC-2026-11-13'
join public.lista_mae lm on lm.cod_item='ESQ001' and lm.ativo is true
where m.codigo in ('MLT.C20','MLT.C21');

update public.kits k
set descricao=concat(
 'Kit documental transcrito do portfólio MLT.C 20 pés (',
 (select count(*) from public.kit_itens ki where ki.kit_id=k.id),
 ' linhas). Não operacional; itens com GAP permanecem fora da BOM.'
), updated_at=now()
where k.codigo in ('KIT-MLTC20-DOCUMENTAL','KIT-MLTC21-DOCUMENTAL');

delete from public.mt_bom_itens bi
using public.mt_versoes_bom b, public.modelos m
where bi.bom_versao_id=b.id and b.modelo_id=m.id
  and b.versao='DOC-2026-11-13'
  and m.codigo in ('MLT.C13','MLT.C20','MLT.C21');

with agg as (
 select m.id modelo_id,ki.lista_mae_id,sum(ki.quantidade) quantidade,
        string_agg(distinct coalesce(ki.instalacao,'COMPOSICAO'),' + ' order by coalesce(ki.instalacao,'COMPOSICAO')) sistemas,
        string_agg(concat('ordem ',ki.ordem,': ',ki.descricao_oficial),' | ' order by ki.ordem) rastreio
 from public.kit_itens ki
 join public.kits k on k.id=ki.kit_id and k.versao='DOC-2026-11-13'
 join public.modelos m on m.id=k.modelo_id
 where m.codigo in ('MLT.C13','MLT.C20','MLT.C21')
   and ki.elo_situacao='ALINHADO_DOCUMENTAL'
   and ki.lista_mae_id is not null
 group by m.id,ki.lista_mae_id
)
insert into public.mt_bom_itens(bom_versao_id,lista_mae_id,quantidade,fator_perda,operacao_referencia,critico,observacoes)
select b.id,a.lista_mae_id,a.quantidade,0,a.sistemas,false,
       concat('RASCUNHO_DOCUMENTAL; Lista Mãe canônica Supabase. ',a.rastreio)
from agg a
join public.mt_versoes_bom b on b.modelo_id=a.modelo_id and b.versao='DOC-2026-11-13' and b.status='RASCUNHO_DOCUMENTAL';

delete from public.estrutura_modular_itens emi
using public.estrutura_modular em, public.modelos m
where emi.estrutura_modular_id=em.id and em.modelo_id=m.id
  and em.versao='DOC-2026-11-13' and em.tipo='DOCUMENTAL'
  and m.codigo in ('MLT.C13','MLT.C20','MLT.C21');

with base as (
 select em.id estrutura_modular_id,m.id modelo_id,m.taxonomia_id,bi.lista_mae_id,bi.quantidade,
        bi.operacao_referencia,lm.cod_item,lm.cod_produt,lm.descricao_oficial,
        row_number() over(partition by m.id order by coalesce(bi.operacao_referencia,''),lm.cod_item)::integer ordem
 from public.modelos m
 join public.estrutura_modular em on em.modelo_id=m.id and em.versao='DOC-2026-11-13' and em.tipo='DOCUMENTAL'
 join public.mt_versoes_bom b on b.modelo_id=m.id and b.versao='DOC-2026-11-13' and b.status='RASCUNHO_DOCUMENTAL'
 join public.mt_bom_itens bi on bi.bom_versao_id=b.id
 join public.lista_mae lm on lm.id=bi.lista_mae_id and lm.ativo is true
 where m.codigo in ('MLT.C13','MLT.C20','MLT.C21')
)
insert into public.estrutura_modular_itens(
 estrutura_modular_id,modelo_id,taxonomia_id,quantidade,posicao,funcao,observacao,ordem,ativo,lista_mae_id
)
select estrutura_modular_id,modelo_id,taxonomia_id,quantidade,'DOCUMENTAL',coalesce(operacao_referencia,'COMPOSICAO'),
       concat('RASCUNHO_DOCUMENTAL; Lista Mãe canônica; item=',cod_item,
              case when cod_produt is null then '' else '; cod_produt='||cod_produt end,
              '; descrição=',descricao_oficial,'; não liberado para produção.'),
       ordem,false,lista_mae_id
from base;

create or replace view public.vw_elo_mltc_gaps_composicao
with (security_invoker=true) as
select m.codigo modelo_codigo,m.nome modelo_nome,k.codigo kit_codigo,ki.ordem,
       ki.instalacao sistema,ki.snapshot_origem,ki.quantidade,ki.un,
       ki.cod_item,ki.cod_produt,ki.vinculo_status,ki.elo_situacao,ki.elo_confianca,
       ki.elo_justificativa
from public.kit_itens ki
join public.kits k on k.id=ki.kit_id
join public.modelos m on m.id=k.modelo_id
where m.codigo like 'MLT.C%'
  and k.versao='DOC-2026-11-13'
  and coalesce(ki.elo_situacao,'') <> 'ALINHADO_DOCUMENTAL';

comment on view public.vw_elo_mltc_gaps_composicao is
'Pendências de composição MLT.C não promovidas à BOM. A Lista Mãe canônica é public.lista_mae; Google Sheets é réplica.';

update public.elo_conhecimento_itens
set conteudo=jsonb_set(conteudo,'{integracao_kit_bom,segunda_onda}',
 jsonb_build_object(
  'data','2026-11-17',
  'regra','Aplicabilidade Lista Mãe ampliada somente para especificações equivalentes comprovadas em C20/C21.',
  'porta_principal','ESQ001 adicionado a C20/C21',
  'cabos_2_5mm','mapeados mas bloqueados por GAP de unidade nas listas C20/C21',
  'google_sheets','réplica; Supabase prevalece'
 ),true),updated_at=now()
where chave_unica='FAMILIA_MLTC_DRY_ADAPTADO';

insert into public.tb_elo_eventos_governanca(evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes)
select 'MLTC_CONSOLIDACAO_LISTA_MAE_ONDA2_20261117','FORGE_COMPOSICAO_DOCUMENTAL','ELO','FORGE_PRODUTOS',
       'RASCUNHO_SEM_LIBERACAO_PRODUCAO','MLTC_LISTA_MAE_ONDA2_20261117',
       jsonb_build_object(
        'fonte_lista_mae','public.lista_mae',
        'google_sheets','replica_nao_canonica',
        'regra','Generalização somente por equivalência documental; conflitos de unidade/faseamento permanecem bloqueados.'
       )
where not exists(
 select 1 from public.tb_elo_eventos_governanca
 where evento='MLTC_CONSOLIDACAO_LISTA_MAE_ONDA2_20261117' and referencia='MLTC_LISTA_MAE_ONDA2_20261117'
);