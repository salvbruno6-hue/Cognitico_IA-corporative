do $$
declare
  v_exc_id uuid;
  v_material numeric;
  v_mao_obra numeric;
  v_total numeric;
  v_commit jsonb;
  v_mem_validada bigint;
begin
  insert into public.lista_mae(
    cod_item,cod_produt,descricao_oficial,aplicacao,un,valor_unitario,
    curva,modelos_aplicaveis,ativo,obrigatoriedade
  )
  values(
    'ELE171',null,
    'EXAUSTOR INDUSTRIAL ITC 350 MOTOR BLINDADO BIVOLT 92W 990M3/H ALUMINIO',
    'Exaustão mecânica de cozinha no M01/MLT.M01 conforme projeto. Montagem em parede/painel; referência do fabricante: saída Ø350 mm e furo Ø360 mm.',
    'PÇ',425.00,'C','M01; Conforme projeto',true,null
  )
  on conflict (cod_item) do update
  set descricao_oficial=excluded.descricao_oficial,
      aplicacao=excluded.aplicacao,
      un=excluded.un,
      valor_unitario=excluded.valor_unitario,
      curva=excluded.curva,
      modelos_aplicaveis=excluded.modelos_aplicaveis,
      ativo=true,
      updated_at=now();

  select id into v_exc_id from public.excedentes where codigo_excedente='EXC-044';
  if v_exc_id is null then raise exception 'EXC-044 não localizado'; end if;

  delete from public.excedente_itens where excedente_id=v_exc_id;
  delete from public.excedente_mao_obra where excedente_id=v_exc_id;

  insert into public.excedente_itens(
    excedente_id,sequencia,cod_item,descricao,unidade,quantidade,
    valor_unitario,valor_parcial,tipo_componente,observacao,cod_excedente,material,un_medida
  ) values
  (v_exc_id,1,'ELE171','SINCRONIZAR LISTA MAE','PÇ',1,null,null,'MATERIAL',
   'Preço validado em 19/11/2026: Mercado Livre/Safanelli R$425,00; loja oficial ITC R$500,18.','EXC-044','EXAUSTOR ITC 350 INDUSTRIAL','PÇ'),
  (v_exc_id,2,'ELE052','SINCRONIZAR LISTA MAE','MT',3,null,null,'MATERIAL',
   'Rota histórica de 3 m.','EXC-044','CABO 2,5MM² PRETO','MT'),
  (v_exc_id,3,'ELE051','SINCRONIZAR LISTA MAE','MT',3,null,null,'MATERIAL',
   'Segundo condutor do circuito; mesmo comprimento da rota histórica de 3 m. Ligação final conforme projeto/tensão local.','EXC-044','CABO 2,5MM² AZUL','MT'),
  (v_exc_id,4,'ELE053','SINCRONIZAR LISTA MAE','MT',3,null,null,'MATERIAL',
   'Condutor de proteção; mesmo comprimento da rota histórica de 3 m.','EXC-044','CABO 2,5MM² VERDE','MT'),
  (v_exc_id,5,'ELE132','SINCRONIZAR LISTA MAE','PÇ',1,null,null,'MATERIAL',
   'Tomada 2P+T 20A/250V conforme escopo 220 V / 20 A.','EXC-044','TOMADA 2P+T 20A','PÇ'),
  (v_exc_id,6,'ELE002','SINCRONIZAR LISTA MAE','PÇ',1,null,null,'MATERIAL',
   'Caixa D300 do sistema Dutopop, conforme composição padrão ELO.','EXC-044','CAIXA D300','PÇ'),
  (v_exc_id,7,'ELE125','SINCRONIZAR LISTA MAE','PÇ',1,null,null,'MATERIAL',
   'Espelho D300-K; resolve a linha histórica genérica Tampa tomada.','EXC-044','ESPELHO D300-K','PÇ'),
  (v_exc_id,8,'ELE005','SINCRONIZAR LISTA MAE','PÇ',1,null,null,'MATERIAL',
   'Dutopop 16x16x2000 mm; quantidade histórica de 1 peça.','EXC-044','DUTOPOP 16X16X2000MM','PÇ');

  insert into public.excedente_mao_obra(
    excedente_id,sequencia,funcao,quantidade,tempo,unidade_tempo,valor_unitario,observacao
  ) values
  (v_exc_id,1,'Profissional — instalação elétrica/exaustor',1,0.2,'DIA',275.82,
   'Produtividade validada na composição: 5 serviços/dia = 0,2 dia por instalação.'),
  (v_exc_id,2,'Ajudante',1,0.2,'DIA',235.92,
   'Produtividade validada na composição: 5 serviços/dia = 0,2 dia por instalação.');

  select coalesce(sum(valor_total),0) into v_material from public.excedente_itens where excedente_id=v_exc_id;
  select coalesce(sum(valor_parcial),0) into v_mao_obra from public.excedente_mao_obra where excedente_id=v_exc_id;
  v_total := round(v_material+v_mao_obra,2);

  update public.excedentes
  set ativo=true,custo_total=v_total,valor_total=v_total,inclui_mao_obra=true,possui_mao_obra_detalhada=true,
      origem='Orçamento interno 24/10/2022 + ITC 350 validado em 19/11/2026',
      observacao='EXC ativo. ELE171 = R$425,00/PÇ; referência oficial ITC = R$500,18. Composição validada com ponto Dutopop 20A, rota de 3 m e mão de obra 0,2 dia/equipe. Não integra a BOM base M01.',
      updated_at=now()
  where id=v_exc_id;

  v_commit := public.elo_commit_aprendizado_merged(
    'EXC-044-INSTALACAO-EXAUSTOR-COZINHA-M01',
    'EXC-044 — Instalação de exaustor em cozinha M01',
    'Excedente opcional ativo para fornecimento e instalação do ITC 350 em M01 com ponto 2P+T 220 V / 20 A e infraestrutura Dutopop.',
    'VALIDATED_LEARNING',
    'EXC-044',
    'forge/orcamento/EXC-044_INSTALACAO_EXAUSTOR_M01_2026-11-19.md',
    'COMPOSICAO_ORCAMENTARIA',
    'VALIDATED_LEARNING',
    jsonb_build_object('preco_aquisicao',425.00,'fonte_aquisicao','Mercado Livre/Safanelli, 19/11/2026','preco_fabricante',500.18,'fonte_fabricante','Loja oficial ITC, 19/11/2026','especificacao','ITC 350 Industrial; 92 W; 990 m³/h; bivolt; saída Ø350 mm; furo Ø360 mm'),
    jsonb_build_object('cod_item_exaustor','ELE171','materiais_total',v_material,'mao_obra_total',v_mao_obra,'total_excedente',v_total,'rota_eletrica_m',3,'composicao_base','EXC-011 adaptado para 20 A + equipamento ITC 350','planilhas_alteradas',false),
    concat('EXC-044 ativo: materiais R$',to_char(v_material,'FM999999990.00'),' + MO R$',to_char(v_mao_obra,'FM999999990.00'),' = R$',to_char(v_total,'FM999999990.00'),'.'),
    'MERGED_APPROVED'
  );
  if coalesce(v_commit->>'commit','') <> 'CONFIRMADO' then raise exception 'Commit canônico não confirmado: %',v_commit; end if;

  v_mem_validada := nullif(v_commit->>'memoria_id','')::bigint;
  if v_mem_validada is not null then update public.excedentes set memoria_calculo_id=v_mem_validada where id=v_exc_id; end if;

  insert into public.tb_elo_eventos_governanca(evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes)
  select 'ATIVACAO_EXC044_EXAUSTOR_M01_20261119','EVOLUTION_GATE','ELO','FORGE_BUDGETING','ATIVO_VALIDADO','EXC-044',
         jsonb_build_object('cod_item_exaustor','ELE171','valor_lista_mae',425.00,'referencia_fabricante',500.18,'materiais_total',v_material,'mao_obra_total',v_mao_obra,'total_excedente',v_total,'ativo',true,'altera_bom_m01',false,'planilhas_alteradas',false,'commit_aprendizado',v_commit)
  where not exists(select 1 from public.tb_elo_eventos_governanca where evento='ATIVACAO_EXC044_EXAUSTOR_M01_20261119' and referencia='EXC-044');
end $$;
