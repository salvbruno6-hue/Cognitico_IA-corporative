-- MLT.C — consolidação do estado vigente em 2026-11-18
-- Não altera Lista Mãe, kits, BOMs ou estrutura modular.
-- Apenas consolida conhecimento cognitivo e governança a partir do estado já validado.

update public.elo_conhecimento_itens
set conteudo =
  conteudo
  || jsonb_build_object(
    'estado_consolidado_2026_11_18',
    jsonb_build_object(
      'familia','MLT.C',
      'versao_documental','DOC-2026-11-13',
      'modelos',6,
      'linhas_kit_total',124,
      'linhas_mapeadas_lista_mae',73,
      'linhas_elegiveis_bom',56,
      'itens_bom_agregados',55,
      'linhas_com_gap',68,
      'valor_parcial_bom',2980.00,
      'estruturas_documentais',6,
      'itens_estrutura_materializados',55,
      'kits_operacionais',0,
      'estruturas_operacionais',0,
      'itens_estrutura_operacionais',0,
      'boms_aprovadas',0,
      'fonte_lista_mae','public.lista_mae',
      'regra_planilhas','Planilhas não são autoridade e não são alteradas sem solicitação explícita do usuário.',
      'estado','DOCUMENTAL_NAO_LIBERADO'
    ),
    'integracao_kit_bom',
    coalesce(conteudo->'integracao_kit_bom','{}'::jsonb)
      || jsonb_build_object(
        'versao','DOC-2026-11-13',
        'kits_modelos',6,
        'linhas_documentais_fonte',122,
        'linhas_kit_total',124,
        'vinculos_lista_mae',73,
        'linhas_elegiveis_bom',56,
        'itens_bom_agregados',55,
        'linhas_com_gap',68,
        'valor_parcial_bom',2980.00,
        'regra','Sem promoção automática: kits não operacionais e BOMs apenas em rascunho/incompletas.',
        'segunda_onda',
          coalesce(conteudo#>'{integracao_kit_bom,segunda_onda}','{}'::jsonb)
          || jsonb_build_object(
            'cabos_2_5mm','VALIDADO em metros: C20 preto 18 m/verde 2 m; C21 preto 19 m/verde 2 m.',
            'esgoto_c20','VALIDADO: coletor/saída principal Ø100 mm; Ø75 não vigente para esse coletor.',
            'google_sheets','Sem alteração automática; Supabase permanece autoridade.'
          )
      ),
    'integracao_estrutura_modular',
    coalesce(conteudo->'integracao_estrutura_modular','{}'::jsonb)
      || jsonb_build_object(
        'versao','DOC-2026-11-13',
        'estruturas_documentais',6,
        'itens_materializados',55,
        'operacionais',false,
        'fonte_lista_mae','public.lista_mae'
      )
  ),
  updated_at=now()
where chave_unica='FAMILIA_MLTC_DRY_ADAPTADO';

update public.elo_conhecimento_itens
set conteudo = conteudo || jsonb_build_object(
  'estado_consolidado_2026_11_18',
  jsonb_build_object(
    'kit_itens',0,'mapeados_lista_mae',0,'linhas_elegiveis_bom',0,'itens_bom',0,
    'valor_parcial_bom',null,'bom_status','INCOMPLETA_DOCUMENTAL',
    'estrutura_itens',0,'operacional',false,
    'proximo_gate','Receber lista de materiais específica e pacote técnico suficiente.'
  )
), updated_at=now()
where chave_unica='PORTFOLIO_MLTC06_20261113';

update public.elo_conhecimento_itens
set conteudo = conteudo || jsonb_build_object(
  'estado_consolidado_2026_11_18',
  jsonb_build_object(
    'kit_itens',0,'mapeados_lista_mae',0,'linhas_elegiveis_bom',0,'itens_bom',0,
    'valor_parcial_bom',null,'bom_status','INCOMPLETA_DOCUMENTAL',
    'estrutura_itens',0,'operacional',false,
    'proximo_gate','Receber lista de materiais específica e pacote técnico suficiente.'
  )
), updated_at=now()
where chave_unica='PORTFOLIO_MLTC10_20261113';

update public.elo_conhecimento_itens
set conteudo = conteudo || jsonb_build_object(
  'estado_consolidado_2026_11_18',
  jsonb_build_object(
    'kit_itens',28,'mapeados_lista_mae',22,'linhas_elegiveis_bom',12,'linhas_com_gap',16,
    'itens_bom',12,'valor_parcial_bom',491.24,'bom_status','RASCUNHO_DOCUMENTAL',
    'estrutura_itens',12,'operacional',false,
    'proximo_gate','Resolver conflitos documentais de porta, comprimento, janela e elétrica.'
  )
), updated_at=now()
where chave_unica='PORTFOLIO_MLTC13_20261113';

update public.elo_conhecimento_itens e
set conteudo =
  jsonb_set(
    e.conteudo,
    '{gaps}',
    coalesce(
      (
        select jsonb_agg(gap)
        from jsonb_array_elements(coalesce(e.conteudo->'gaps','[]'::jsonb)) gap
        where gap->>'tema' <> 'esgoto'
      ),
      '[]'::jsonb
    ),
    true
  )
  || jsonb_build_object(
    'gaps_resolvidos',
    coalesce(e.conteudo->'gaps_resolvidos','[]'::jsonb)
      || jsonb_build_array(
        jsonb_build_object(
          'tema','esgoto_coletor_principal',
          'conflito_historico',jsonb_build_array('Ø100 mm','Ø75 mm'),
          'decisao_vigente','Ø100 mm',
          'status','RESOLVIDO',
          'fonte_decisao','VALIDACAO_EXPLICITA_USUARIO_2026-11-18',
          'observacao','Ø75 não é vigente para o coletor/saída principal. Ramais Ø40/Ø50 permanecem conforme documentação.'
        )
      ),
    'validacoes_usuario',
    coalesce(e.conteudo->'validacoes_usuario','{}'::jsonb)
      || jsonb_build_object(
        '2026-11-18',
        jsonb_build_object(
          'esgoto_principal_c20','Ø100 mm',
          'cabos_2_5mm','MT',
          'cabos_quantidades','preto 18 m; verde 2 m'
        )
      ),
    'estado_consolidado_2026_11_18',
    jsonb_build_object(
      'kit_itens',45,'mapeados_lista_mae',23,'linhas_elegiveis_bom',20,'linhas_com_gap',25,
      'itens_bom',20,'valor_parcial_bom',1174.99,'bom_status','RASCUNHO_DOCUMENTAL',
      'estrutura_itens',20,'operacional',false,
      'regras_vigentes',jsonb_build_array(
        'Coletor/saída principal de esgoto Ø100 mm.',
        'Cabos 2,5 mm² medidos em metros: preto 18 m; verde 2 m.',
        'Ramais Ø40/Ø50 permanecem conforme documentação.'
      ),
      'pendencias_prioritarias',jsonb_build_array(
        'Definir ângulo do joelho Ø100.',
        'Validar conversão do tubo Ø100: 6 m = 1 barra/PÇ de 6 m.',
        'Resolver basculantes, comprimento, proteção elétrica, identificação de arquivo e revisão ARQ.'
      )
    )
  ),
  updated_at=now()
where e.chave_unica='PORTFOLIO_MLTC20_20261113';

update public.elo_conhecimento_itens
set conteudo = conteudo || jsonb_build_object(
  'validacoes_usuario',
  coalesce(conteudo->'validacoes_usuario','{}'::jsonb)
    || jsonb_build_object(
      '2026-11-18',
      jsonb_build_object(
        'cabos_2_5mm','MT',
        'cabos_quantidades','preto 19 m; verde 2 m'
      )
    ),
  'estado_consolidado_2026_11_18',
  jsonb_build_object(
    'kit_itens',51,'mapeados_lista_mae',28,'linhas_elegiveis_bom',24,'linhas_com_gap',27,
    'itens_bom',23,'valor_parcial_bom',1313.77,'bom_status','RASCUNHO_DOCUMENTAL',
    'estrutura_itens',23,'operacional',false,
    'regras_vigentes',jsonb_build_array(
      'Saída de esgoto Ø100 mm documentada nas notas.',
      'Cabos 2,5 mm² medidos em metros: preto 19 m; verde 2 m.'
    ),
    'pendencias_prioritarias',jsonb_build_array(
      'Resolver faseamento bifásico × monofásico.',
      'Resolver portas internas e quantidade de basculantes.',
      'Corrigir identificação de prancha e detalhar coletor de esgoto.'
    )
  )
), updated_at=now()
where chave_unica='PORTFOLIO_MLTC21_20261113';

update public.elo_conhecimento_itens
set conteudo = conteudo || jsonb_build_object(
  'estado_consolidado_2026_11_18',
  jsonb_build_object(
    'kit_itens',0,'mapeados_lista_mae',0,'linhas_elegiveis_bom',0,'itens_bom',0,
    'valor_parcial_bom',null,'bom_status','INCOMPLETA_DOCUMENTAL',
    'estrutura_itens',0,'operacional',false,
    'proximo_gate','Receber pacote técnico e lista de materiais específica do C25.'
  )
), updated_at=now()
where chave_unica='PORTFOLIO_MLTC25_20261113';

insert into public.tb_elo_eventos_governanca(
  evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes
)
select
  'CONSOLIDACAO_ESTADO_MLTC_20261118',
  'EVOLUTION_GATE',
  'ELO',
  'FORGE_PRODUTOS',
  'CONSOLIDADO_DOCUMENTAL_NAO_LIBERADO',
  'MLTC_CONSOLIDADO_20261118',
  jsonb_build_object(
    'versao','DOC-2026-11-13',
    'modelos',6,
    'linhas_kit_total',124,
    'mapeadas_lista_mae',73,
    'linhas_elegiveis_bom',56,
    'itens_bom_agregados',55,
    'linhas_com_gap',68,
    'valor_parcial_bom',2980.00,
    'itens_estrutura_documental',55,
    'kits_operacionais',0,
    'boms_aprovadas',0,
    'planilhas_alteradas',false,
    'regra','Supabase é autoridade persistente; GitHub é autoridade operacional/canônica; planilhas somente sob solicitação explícita.'
  )
where not exists(
  select 1
  from public.tb_elo_eventos_governanca
  where evento='CONSOLIDACAO_ESTADO_MLTC_20261118'
    and referencia='MLTC_CONSOLIDADO_20261118'
);