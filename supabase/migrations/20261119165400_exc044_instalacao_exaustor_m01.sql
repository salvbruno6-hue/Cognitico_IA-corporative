-- EXC-044 — instalação de exaustor em cozinha M01 com painel PIR40
-- Fonte histórica: orçamento interno informado pelo usuário, 24/10/2022.
-- Equipamento candidato atual: ITC 350 Industrial 220 V, referência técnica externa.
-- Regra: não altera BOM base do M01 e não cria item na Lista Mãe.
-- Estado inicial: INATIVO / custo total não fechado.

do $$
declare
  v_mem_id bigint;
  v_exc_id uuid;
begin
  select id into v_mem_id
  from public.elo_orcamento_memoria
  where conceito_key='EXC-044-INSTALACAO-EXAUSTOR-COZINHA-M01'
  order by id desc limit 1;

  if v_mem_id is null then
    insert into public.elo_orcamento_memoria(
      tipo_memoria,aplicacao,necessidade,contexto,
      memoria_calculo,evidencias,resultado,valor_aprendizado,confianca,
      classificacao,conceito_key,titulo_conceito,conceito,tipo_conhecimento,
      decisao_governanca,status_conceito,ultima_evidencia_em,origem_documento
    )
    values(
      'CALCULO',
      'EXC de instalação de exaustor em cozinha de módulo M01/Habitacional Amplo com interface em painel PIR 40 mm e ponto 2P+T 220 V / 20 A.',
      'Preservar o orçamento histórico de 24/10/2022 como precedente e estruturar uma composição atual sem transportar automaticamente o exaustor antigo ou seus preços.',
      'Orçamento histórico: cliente PRODUÇÃO INTERNA; produto "COLOCAÇÃO DE UM EXAUSTOR COZINHA 2P+T. 220/20A COM PAINÉL PIR 40"; orçamentista Bruno Santos. Equipamento histórico descrito como exaustor industrial 50 cm, alta rotação, vazão 21.000 m³/h. Equipamento candidato atual informado pelo usuário: ITC 350 Industrial.',
      jsonb_build_object(
        'historico_2022',jsonb_build_object(
          'data','2022-10-24',
          'materiais',jsonb_build_array(
            jsonb_build_object('descricao','Exaustor industrial 50 cm alta rotação, vazão 21.000 m³/h','qtd',1,'un','UN','valor_unitario',462.00,'valor_parcial',462.00),
            jsonb_build_object('descricao','Cabo 2,5 mm² preto','qtd',3,'un','M','valor_unitario',1.93,'valor_parcial',5.79),
            jsonb_build_object('descricao','Cabo 2,5 mm² verde','qtd',null,'un','M','valor_unitario',1.93,'valor_parcial',0.00),
            jsonb_build_object('descricao','Tampa tomada','qtd',1,'un','UN','valor_unitario',1.51,'valor_parcial',1.51),
            jsonb_build_object('descricao','Tubo Dutotop 16 mm x 2,00','qtd',1,'un','UN','valor_unitario',null,'valor_parcial',0.00)
          ),
          'materiais_total',469.30,
          'mao_obra',jsonb_build_array(
            jsonb_build_object('funcao','PROFISSIONAL','qtd',1,'tempo_dia',1,'valor_dia',275.82,'valor_parcial',275.82),
            jsonb_build_object('funcao','AJUDANTE','qtd',1,'tempo_dia',1,'valor_dia',235.92,'valor_parcial',235.92)
          ),
          'mao_obra_dia_total',511.74,
          'servicos_executados_no_dia',5,
          'alocacao_mo_por_servico_calculada',102.348,
          'total_exibido_na_planilha',469.30,
          'gap_fechamento','O total exibido repete somente materiais; não concilia materiais + mão de obra.'
        ),
        'candidato_atual',jsonb_build_object(
          'equipamento','Exaustor ITC 350 Industrial',
          'tensao','220 V (opção disponível)',
          'potencia_w',92,
          'vazao_m3_h',990,
          'rotacao_rpm',1550,
          'helice_mm',300,
          'saida_ar_mm',350,
          'furo_instalacao_mm',360,
          'area_referencia_m2',80,
          'status','CANDIDATO_NAO_HOMOLOGADO',
          'equivalente_ao_historico_2022',false,
          'motivo_nao_equivalencia','Histórico especifica 50 cm e 21.000 m³/h; candidato atual possui 990 m³/h e saída de 350 mm.'
        ),
        'componentes_canonicos_atuais',jsonb_build_array(
          jsonb_build_object('cod_item','ELE052','descricao','Cabo 2,5 mm² preto','qtd',3,'un','MT','valor_unitario',2.43,'valor_parcial',7.29),
          jsonb_build_object('cod_item','ELE005','descricao','Dutopop PVC 16x16x2000 mm','qtd',1,'un','PÇ','valor_unitario',19.11,'valor_parcial',19.11),
          jsonb_build_object('cod_item','ELE132','descricao','Tomada 2P+T 20A/250V','qtd',1,'un','PÇ','valor_unitario',6.15,'valor_parcial',6.15)
        ),
        'materiais_canonicos_parcial',32.55,
        'mao_obra_candidata',jsonb_build_object(
          'criterio','Produtividade histórica de 5 serviços/dia; 0,2 dia por instalação, sujeita à revalidação.',
          'profissional_dia',275.82,
          'ajudante_dia',235.92,
          'fracao_dia',0.2,
          'valor_calculado',102.348
        ),
        'parcial_conhecido_sem_exaustor_e_tampa',134.898
      ),
      jsonb_build_object(
        'fonte_usuario','Orçamento interno transcrito pelo usuário, datado de 24/10/2022.',
        'produto_atual_informado','Mercado Livre — Exaustor Industrial ITC 350 Motor Blindado, vazão 990 m³/h.',
        'fonte_tecnica_fabricante','ITC Exaustores — ITC 350.',
        'lista_mae','public.lista_mae para ELE052, ELE005 e ELE132.',
        'mao_obra','public.mt_mao_obra_kit_eletrico_m01.'
      ),
      'Criado EXC referencial inativo. Custo total permanece aberto: exaustor candidato não está homologado na Lista Mãe e tampa/espelho exige validação. O orçamento de 2022 é precedente, não preço vigente.',
      0,
      0.80,
      'PRECEDENT',
      'EXC-044-INSTALACAO-EXAUSTOR-COZINHA-M01',
      'EXC-044 — Instalação de exaustor em cozinha M01',
      'Instalação opcional de exaustor em cozinha, com interface em painel PIR40 e ponto 2P+T 220 V / 20 A. Equipamento e composição devem ser validados por projeto antes de ativação.',
      'COMPOSICAO_ORCAMENTARIA',
      'PRECEDENTE FORGE. NÃO ALTERAR BOM BASE M01. NÃO CADASTRAR EXAUSTOR NA LISTA MÃE SEM HOMOLOGAÇÃO. EXC PERMANECE INATIVO ATÉ FECHAMENTO DE EQUIPAMENTO, ACABAMENTO E PRODUTIVIDADE.',
      'PENDENTE_VALIDACAO',
      now(),
      'Orçamento interno 24/10/2022 + referência técnica atual ITC 350 informada pelo usuário'
    )
    returning id into v_mem_id;
  end if;

  select id into v_exc_id
  from public.excedentes
  where codigo_excedente='EXC-044';

  if v_exc_id is null then
    insert into public.excedentes(
      codigo_excedente,tipo_instalacao,descricao,unidade,custo_total,
      inclui_mao_obra,origem,observacao,ativo,possui_mao_obra_detalhada,
      valor_total,memoria_calculo_id
    )
    values(
      'EXC-044',
      'EXAUSTÃO / ELÉTRICA',
      'Instalação de exaustor em cozinha M01 com interface em painel PIR 40 mm e ponto 2P+T 220 V / 20 A',
      'UN',
      null,
      true,
      'Orçamento interno 24/10/2022 + candidato atual ITC 350 informado pelo usuário',
      'EXC referencial. O exaustor histórico 50 cm / 21.000 m³/h NÃO é equivalente ao ITC 350 atual de 990 m³/h. Custo total não fechado.',
      false,
      true,
      null,
      v_mem_id
    )
    returning id into v_exc_id;
  else
    update public.excedentes
    set tipo_instalacao='EXAUSTÃO / ELÉTRICA',
        descricao='Instalação de exaustor em cozinha M01 com interface em painel PIR 40 mm e ponto 2P+T 220 V / 20 A',
        unidade='UN',
        custo_total=null,
        inclui_mao_obra=true,
        origem='Orçamento interno 24/10/2022 + candidato atual ITC 350 informado pelo usuário',
        observacao='EXC referencial. O exaustor histórico 50 cm / 21.000 m³/h NÃO é equivalente ao ITC 350 atual de 990 m³/h. Custo total não fechado.',
        ativo=false,
        possui_mao_obra_detalhada=true,
        valor_total=null,
        memoria_calculo_id=v_mem_id,
        updated_at=now()
    where id=v_exc_id;
  end if;

  delete from public.excedente_itens where excedente_id=v_exc_id;
  delete from public.excedente_mao_obra where excedente_id=v_exc_id;

  insert into public.excedente_itens(
    excedente_id,sequencia,cod_produt,cod_item,descricao,unidade,quantidade,
    valor_unitario,valor_parcial,tipo_componente,observacao,cod_excedente,material,un_medida
  ) values
  (
    v_exc_id,1,null,null,
    'EXAUSTOR ITC 350 INDUSTRIAL — 220 V — 92 W — 990 m³/h — saída Ø350 mm — furo de instalação Ø360 mm',
    'PÇ',1,null,null,'MATERIAL',
    'Equipamento candidato atual informado pelo usuário. Não homologado na Lista Mãe; preço não canonizado. Não equivalente ao exaustor histórico 50 cm / 21.000 m³/h.',
    'EXC-044','EXAUSTOR ITC 350 INDUSTRIAL','PÇ'
  ),
  (
    v_exc_id,2,'3300200003','ELE052',
    'CABO FLEXÍVEL SINGELO 750V 70° 2,5MM² PRETO',
    'MT',3,2.43,7.29,'MATERIAL',
    'Quantidade de 3 m proveniente do orçamento histórico; preço unitário atual da Lista Mãe no momento da consolidação.',
    'EXC-044','CABO 2,5MM² PRETO','MT'
  ),
  (
    v_exc_id,3,'2700100339','ELE005',
    'DUTOPOP EM PVC 16X16X2000MM COM ADESIVO CREME',
    'PÇ',1,19.11,19.11,'MATERIAL',
    'Correspondência canônica ao Dutotop/Dutopop 16 mm x 2,00 do orçamento histórico.',
    'EXC-044','DUTOPOP 16X16X2000MM','PÇ'
  ),
  (
    v_exc_id,4,'3300700007','ELE132',
    'TOMADA DE EMBUTIR NOVO PADRÃO 2P+T 20A/250V REDONDA PRETA',
    'PÇ',1,6.15,6.15,'MATERIAL',
    'Requisito 2P+T 220 V / 20 A explicitado no escopo histórico. Não implica definição automática de disjuntor ou circuito.',
    'EXC-044','TOMADA 2P+T 20A','PÇ'
  ),
  (
    v_exc_id,5,null,null,
    'TAMPA / ESPELHO DE TOMADA — ESPECIFICAÇÃO A CONFIRMAR',
    'PÇ',1,null,null,'MATERIAL',
    'Orçamento histórico informa apenas "Tampa tomada" por R$1,51. Não vincular automaticamente a ELE125 sem validação de modelo/cor/interface.',
    'EXC-044','TAMPA / ESPELHO DE TOMADA','PÇ'
  ),
  (
    v_exc_id,6,'3300200002','ELE053',
    'CABO FLEXÍVEL SINGELO 750V 70° 2,5MM² VERDE',
    'MT',0,2.43,0,'MATERIAL',
    'Linha existente no orçamento histórico, porém sem quantidade informada e valor parcial R$0,00. Quantidade deve ser definida pelo projeto; zero não representa ausência técnica de aterramento.',
    'EXC-044','CABO 2,5MM² VERDE','MT'
  );

  insert into public.excedente_mao_obra(
    excedente_id,sequencia,funcao,quantidade,tempo,unidade_tempo,
    valor_unitario,observacao
  ) values
  (
    v_exc_id,1,'Profissional — instalação elétrica/exaustor',1,0.2,'DIA',
    275.82,
    'Produtividade candidata derivada do orçamento histórico: 5 serviços executados no dia. Custo-dia confirmado na base atual M01; produtividade ainda requer validação.'
  ),
  (
    v_exc_id,2,'Ajudante',1,0.2,'DIA',
    235.92,
    'Produtividade candidata derivada do orçamento histórico: 5 serviços executados no dia. Custo-dia confirmado na base atual M01; produtividade ainda requer validação.'
  );

  update public.excedentes
  set custo_total=null,
      valor_total=null,
      ativo=false,
      observacao='EXC referencial inativo. Parcial conhecido dos componentes canônicos + MO candidata = R$134,89; NÃO é custo total. Exaustor ITC 350 e tampa/espelho ainda sem custo homologado. O exaustor histórico 50 cm / 21.000 m³/h não é equivalente ao candidato atual de 990 m³/h.',
      updated_at=now()
  where id=v_exc_id;

  insert into public.tb_elo_eventos_governanca(
    evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes
  )
  select
    'CADASTRO_EXC044_EXAUSTOR_M01_20261119',
    'FORGE_ORCAMENTO',
    'ELO',
    'FORGE_BUDGETING',
    'REFERENCIAL_INATIVO_COM_GAPS',
    'EXC-044',
    jsonb_build_object(
      'modelo_contexto','M01 / MLT.M01 Habitacional Amplo',
      'origem_historica','Orçamento interno 24/10/2022',
      'equipamento_historico','Exaustor industrial 50 cm, 21.000 m³/h',
      'equipamento_candidato','ITC 350 Industrial 220 V, 92 W, 990 m³/h, saída Ø350, furo Ø360',
      'equivalencia_equipamentos',false,
      'materiais_canonicos_parcial',32.55,
      'mao_obra_candidata',102.348,
      'parcial_conhecido',134.898,
      'custo_total_fechado',false,
      'ativo',false,
      'altera_bom_m01',false,
      'altera_lista_mae',false,
      'planilhas_alteradas',false
    )
  where not exists(
    select 1 from public.tb_elo_eventos_governanca
    where evento='CADASTRO_EXC044_EXAUSTOR_M01_20261119' and referencia='EXC-044'
  );
end $$;
