-- MLT.C — validação técnica do usuário: coletor/saída C20 Ø100 mm; cabos em metros
-- Data de validação: 2026-11-18
-- Autoridade de materiais: public.lista_mae.
-- Preserva snapshot documental original; a decisão validada fica registrada em elo_justificativa/governança.

with mapa(ordem,cod_item,justificativa) as (
 values
 (50,'HID016','VALIDADO_USUARIO_2026-11-18: coletor/esgoto principal C20 é Ø100 mm; Tê anteriormente documentado Ø75 substituído pelo item canônico Ø100.'),
 (51,'HID018','VALIDADO_USUARIO_2026-11-18: coletor/esgoto principal C20 é Ø100 mm; Tê 75x50 substituído pelo equivalente canônico 100x50.'),
 (53,'HID026','VALIDADO_USUARIO_2026-11-18: coletor/esgoto principal C20 é Ø100 mm; luva Ø75 substituída por luva Ø100.'),
 (55,'HID037','VALIDADO_USUARIO_2026-11-18: coletor/esgoto principal C20 é Ø100 mm; anel Ø75 substituído por anel Ø100.')
),
res as (
 select ki.id kit_item_id,lm.id lista_mae_id,lm.cod_item,lm.cod_produt,lm.descricao_oficial,lm.un,lm.valor_unitario,map.justificativa
 from mapa map
 join public.modelos m on m.codigo='MLT.C20'
 join public.kits k on k.modelo_id=m.id and k.versao='DOC-2026-11-13'
 join public.kit_itens ki on ki.kit_id=k.id and ki.ordem=map.ordem
 join public.lista_mae lm on lm.cod_item=map.cod_item and lm.ativo is true
)
update public.kit_itens ki
set lista_mae_id=res.lista_mae_id,cod_item=res.cod_item,cod_produt=res.cod_produt,
    descricao_oficial=res.descricao_oficial,un=res.un,valor_unitario=res.valor_unitario,
    valor_total=ki.quantidade*coalesce(res.valor_unitario,0),vinculo_status='LOCALIZADO',
    vinculo_confianca=1,vinculo_observacao=res.justificativa,elo_situacao='ALINHADO_DOCUMENTAL',
    elo_confianca=1,elo_justificativa=res.justificativa,
    observacao=concat(coalesce(ki.observacao,''),case when coalesce(ki.observacao,'')='' then '' else ' | ' end,res.justificativa),
    vinculo_at=now()
from res where ki.id=res.kit_item_id;

with res as (
 select ki.id kit_item_id,lm.id lista_mae_id,lm.cod_item,lm.cod_produt,lm.descricao_oficial,lm.un,lm.valor_unitario
 from public.modelos m
 join public.kits k on k.modelo_id=m.id and k.versao='DOC-2026-11-13'
 join public.kit_itens ki on ki.kit_id=k.id and ki.ordem=58
 join public.lista_mae lm on lm.cod_item='HID004' and lm.ativo is true
 where m.codigo='MLT.C20'
)
update public.kit_itens ki
set lista_mae_id=res.lista_mae_id,cod_item=res.cod_item,cod_produt=res.cod_produt,
    descricao_oficial=res.descricao_oficial,un=res.un,valor_unitario=res.valor_unitario,valor_total=null,
    vinculo_status='DIVERGENTE',vinculo_confianca=1,
    vinculo_observacao='VALIDADO_USUARIO_2026-11-18: coletor principal é Ø100 mm. Quantidade fonte=6 METROS; item canônico HID004 é barra/PÇ de 6 m. Conversão de unidade ainda não promovida.',
    elo_situacao='MAPEADO_COM_GAP_UNIDADE',elo_confianca=1,
    elo_justificativa='Diâmetro resolvido em Ø100 mm; falta somente validar a conversão 6 m = 1 barra/PÇ para BOM.',
    observacao=concat(coalesce(ki.observacao,''),case when coalesce(ki.observacao,'')='' then '' else ' | ' end,'VALIDADO_USUARIO_2026-11-18: Ø100 mm; conversão metro→barra permanece pendente.'),
    vinculo_at=now()
from res where ki.id=res.kit_item_id;

update public.kit_itens ki
set lista_mae_id=null,cod_item=null,cod_produt=null,
    descricao_oficial='Joelho Ø100 mm — ângulo pendente',un='UN',valor_unitario=null,valor_total=null,
    vinculo_status='DIVERGENTE',vinculo_confianca=1,
    vinculo_observacao='VALIDADO_USUARIO_2026-11-18: diâmetro do coletor é Ø100 mm. Ângulo do joelho não foi definido; permanece fora da BOM.',
    elo_situacao='GAP_DOCUMENTAL_SEM_VINCULO',elo_confianca=1,
    elo_justificativa='Diâmetro corrigido para Ø100 mm; falta definir ângulo 45°/90° para vínculo inequívoco.',
    observacao=concat(coalesce(ki.observacao,''),case when coalesce(ki.observacao,'')='' then '' else ' | ' end,'VALIDADO_USUARIO_2026-11-18: Ø100 mm; ângulo pendente.')
from public.kits k join public.modelos m on m.id=k.modelo_id
where ki.kit_id=k.id and k.versao='DOC-2026-11-13' and m.codigo='MLT.C20' and ki.ordem=52;

with alvo(modelo_codigo,ordem,cod_item,justificativa) as (
 values
 ('MLT.C20',72,'ELE052','VALIDADO_USUARIO_2026-11-18: cabo preto 2,5 mm² é medido em metros; quantidade válida=18 m.'),
 ('MLT.C20',73,'ELE053','VALIDADO_USUARIO_2026-11-18: cabo verde 2,5 mm² é medido em metros; quantidade válida=2 m.'),
 ('MLT.C21',88,'ELE052','VALIDADO_USUARIO_2026-11-18: cabo preto 2,5 mm² é medido em metros; quantidade válida=19 m.'),
 ('MLT.C21',89,'ELE053','VALIDADO_USUARIO_2026-11-18: cabo verde 2,5 mm² é medido em metros; quantidade válida=2 m.')
),
res as (
 select ki.id kit_item_id,lm.id lista_mae_id,lm.cod_item,lm.cod_produt,lm.descricao_oficial,lm.un,lm.valor_unitario,alvo.justificativa
 from alvo
 join public.modelos m on m.codigo=alvo.modelo_codigo
 join public.kits k on k.modelo_id=m.id and k.versao='DOC-2026-11-13'
 join public.kit_itens ki on ki.kit_id=k.id and ki.ordem=alvo.ordem
 join public.lista_mae lm on lm.cod_item=alvo.cod_item and lm.ativo is true
)
update public.kit_itens ki
set lista_mae_id=res.lista_mae_id,cod_item=res.cod_item,cod_produt=res.cod_produt,
    descricao_oficial=res.descricao_oficial,un='MT',valor_unitario=res.valor_unitario,
    valor_total=ki.quantidade*coalesce(res.valor_unitario,0),vinculo_status='LOCALIZADO',
    vinculo_confianca=1,vinculo_observacao=res.justificativa,elo_situacao='ALINHADO_DOCUMENTAL',
    elo_confianca=1,elo_justificativa=res.justificativa,
    observacao=concat(coalesce(ki.observacao,''),case when coalesce(ki.observacao,'')='' then '' else ' | ' end,res.justificativa),
    vinculo_at=now()
from res where ki.id=res.kit_item_id;

delete from public.mt_bom_itens bi
using public.mt_versoes_bom b, public.modelos m
where bi.bom_versao_id=b.id and b.modelo_id=m.id and b.versao='DOC-2026-11-13'
  and m.codigo in ('MLT.C20','MLT.C21');

with agg as (
 select m.id modelo_id,ki.lista_mae_id,sum(ki.quantidade) quantidade,
        string_agg(distinct coalesce(ki.instalacao,'COMPOSICAO'),' + ' order by coalesce(ki.instalacao,'COMPOSICAO')) sistemas,
        string_agg(concat('ordem ',ki.ordem,': ',ki.descricao_oficial),' | ' order by ki.ordem) rastreio
 from public.kit_itens ki
 join public.kits k on k.id=ki.kit_id and k.versao='DOC-2026-11-13'
 join public.modelos m on m.id=k.modelo_id
 where m.codigo in ('MLT.C20','MLT.C21') and ki.elo_situacao='ALINHADO_DOCUMENTAL' and ki.lista_mae_id is not null
 group by m.id,ki.lista_mae_id
)
insert into public.mt_bom_itens(bom_versao_id,lista_mae_id,quantidade,fator_perda,operacao_referencia,critico,observacoes)
select b.id,a.lista_mae_id,a.quantidade,0,a.sistemas,false,
       concat('RASCUNHO_DOCUMENTAL; Lista Mãe canônica Supabase; validações do usuário incorporadas em 2026-11-18. ',a.rastreio)
from agg a
join public.mt_versoes_bom b on b.modelo_id=a.modelo_id and b.versao='DOC-2026-11-13' and b.status='RASCUNHO_DOCUMENTAL';

delete from public.estrutura_modular_itens emi
using public.estrutura_modular em, public.modelos m
where emi.estrutura_modular_id=em.id and em.modelo_id=m.id
  and em.versao='DOC-2026-11-13' and em.tipo='DOCUMENTAL'
  and m.codigo in ('MLT.C20','MLT.C21');

with base as (
 select em.id estrutura_modular_id,m.id modelo_id,m.taxonomia_id,bi.lista_mae_id,bi.quantidade,
        bi.operacao_referencia,lm.cod_item,lm.cod_produt,lm.descricao_oficial,
        row_number() over(partition by m.id order by coalesce(bi.operacao_referencia,''),lm.cod_item)::integer ordem
 from public.modelos m
 join public.estrutura_modular em on em.modelo_id=m.id and em.versao='DOC-2026-11-13' and em.tipo='DOCUMENTAL'
 join public.mt_versoes_bom b on b.modelo_id=m.id and b.versao='DOC-2026-11-13' and b.status='RASCUNHO_DOCUMENTAL'
 join public.mt_bom_itens bi on bi.bom_versao_id=b.id
 join public.lista_mae lm on lm.id=bi.lista_mae_id and lm.ativo is true
 where m.codigo in ('MLT.C20','MLT.C21')
)
insert into public.estrutura_modular_itens(
 estrutura_modular_id,modelo_id,taxonomia_id,quantidade,posicao,funcao,observacao,ordem,ativo,lista_mae_id
)
select estrutura_modular_id,modelo_id,taxonomia_id,quantidade,'DOCUMENTAL',coalesce(operacao_referencia,'COMPOSICAO'),
       concat('RASCUNHO_DOCUMENTAL; Lista Mãe canônica; item=',cod_item,
              case when cod_produt is null then '' else '; cod_produt='||cod_produt end,
              '; descrição=',descricao_oficial,'; validações usuário 2026-11-18; não liberado para produção.'),
       ordem,false,lista_mae_id
from base;

update public.elo_conhecimento_itens
set conteudo=jsonb_set(
      jsonb_set(conteudo,'{validacoes_usuario,2026-11-18,esgoto_c20}',
        jsonb_build_object('estado','VALIDADO','regra','Coletor/saída de esgoto principal do MLT.C20 = Ø100 mm. Ø75 não é vigente para esse coletor.','efeito','Itens Ø75 do coletor foram reclassificados para equivalentes Ø100; ramais 40/50 mm permanecem conforme documentação.'),true),
      '{validacoes_usuario,2026-11-18,cabos_2_5mm}',
        jsonb_build_object('estado','VALIDADO','regra','Cabos 2,5 mm² são medidos em metros.','c20','preto 18 m; verde 2 m','c21','preto 19 m; verde 2 m'),true),
    updated_at=now()
where chave_unica='FAMILIA_MLTC_DRY_ADAPTADO';

update public.elo_conhecimento_itens
set conteudo=jsonb_set(conteudo,'{validacoes_usuario,2026-11-18}',
      jsonb_build_object('esgoto_principal','Ø100 mm validado; conflito Ø75/Ø100 resolvido a favor de Ø100.','cabos_2_5mm','Unidade validada em MT.'),true),
    updated_at=now()
where chave_unica in ('PORTFOLIO_MLTC20_20261113','PORTFOLIO_MLTC21_20261113');

insert into public.tb_elo_eventos_governanca(evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes)
select 'VALIDACAO_USUARIO_MLTC_ESGOTO100_CABO_METRO_20261118','VALIDACAO_TECNICA','ELO','FORGE_PRODUTOS',
       'VALIDADO_EM_RASCUNHO_DOCUMENTAL','MLTC_VALIDACAO_20261118_ESGOTO_CABOS',
       jsonb_build_object('c20_esgoto','coletor/saída principal Ø100 mm; Ø75 descartado como vigente','ramais','40/50 mm preservados onde documentados','cabos','2,5 mm² em metros; C20 preto 18 m/verde 2 m; C21 preto 19 m/verde 2 m','fonte_decisao','VALIDACAO_EXPLICITA_USUARIO','bom_status','RASCUNHO_DOCUMENTAL','producao_liberada',false)
where not exists(
 select 1 from public.tb_elo_eventos_governanca
 where evento='VALIDACAO_USUARIO_MLTC_ESGOTO100_CABO_METRO_20261118'
   and referencia='MLTC_VALIDACAO_20261118_ESGOTO_CABOS'
);