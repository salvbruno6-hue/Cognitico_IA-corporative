-- PCP: versionar o fluxo produtivo modular preservando a referência histórica.
-- Autoridade: Supabase operacional; implementação/governança versionada no GitHub.
-- Regra: não sobrescrever silenciosamente MLT.PROD.PADRAO v1.0.

DO $$
DECLARE
  v_old_flow_id uuid;
  v_new_flow_id uuid;
BEGIN
  SELECT id
    INTO v_old_flow_id
    FROM public.fluxo_produtivo_modular
   WHERE codigo = 'MLT.PROD.PADRAO';

  IF v_old_flow_id IS NULL THEN
    RAISE EXCEPTION 'Fluxo histórico MLT.PROD.PADRAO não localizado; abortando versionamento';
  END IF;

  IF EXISTS (
    SELECT 1
      FROM public.fluxo_produtivo_modular
     WHERE codigo = 'MLT.PROD.PADRAO.V2'
  ) THEN
    RAISE EXCEPTION 'Fluxo MLT.PROD.PADRAO.V2 já existe; revisar antes de reaplicar';
  END IF;

  UPDATE public.fluxo_produtivo_modular
     SET ativo = false,
         observacoes = CASE
           WHEN position('SUPERSEDIDO_POR=MLT.PROD.PADRAO.V2' in COALESCE(observacoes, '')) > 0
             THEN observacoes
           ELSE concat_ws(' | ', NULLIF(observacoes, ''), 'SUPERSEDIDO_POR=MLT.PROD.PADRAO.V2; preservado como referência histórica v1.0')
         END,
         updated_at = now()
   WHERE id = v_old_flow_id;

  UPDATE public.fluxo_produtivo_modular_etapas
     SET status = 'INATIVO'
   WHERE fluxo_id = v_old_flow_id
     AND upper(COALESCE(status, '')) = 'ATIVO';

  INSERT INTO public.fluxo_produtivo_modular (
    id,
    codigo,
    nome,
    modelo_id,
    taxonomia_id,
    versao,
    descricao,
    lead_time_dias,
    capacidade_referencia,
    unidade_capacidade,
    ativo,
    observacoes
  )
  SELECT
    gen_random_uuid(),
    'MLT.PROD.PADRAO.V2',
    'Fluxo Produtivo Modular — Referência Operacional Atual',
    modelo_id,
    taxonomia_id,
    '2.0',
    'Fluxo operacional atualizado do PCP Multiteiner, preservando a v1.0 como histórico. Tempos, capacidades, recursos e dependências detalhadas só podem ser preenchidos com evidência operacional validada.',
    NULL,
    NULL,
    NULL,
    true,
    'Atualizado a partir do contrato operacional confirmado em 2026-10-23. TRILHO e PINTURA_MODULAR permanecem somente na v1.0 histórica. CORTE_DOBRA e ESQUADRIAS passam a integrar a referência atual. Cura/liberação para EL continua dependente de evento/evidência real e não é inferida pela conclusão da pintura.'
  FROM public.fluxo_produtivo_modular
  WHERE id = v_old_flow_id
  RETURNING id INTO v_new_flow_id;

  INSERT INTO public.fluxo_produtivo_modular_etapas (
    id, fluxo_id, ordem, codigo_etapa, nome, setor, processo, recurso,
    tempo_setup_min, tempo_unitario_min, capacidade, unidade_capacidade,
    dependencias, materiais, criterios_qualidade, status, observacoes
  ) VALUES
    (gen_random_uuid(), v_new_flow_id,  1, 'TRIAGEM',              'Triagem',                NULL, 'Triagem',             NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Separação de matéria-prima e preparação dos painéis PIR e material de fibra.'),
    (gen_random_uuid(), v_new_flow_id,  2, 'CORTE_DOBRA',          'Corte e dobra',           NULL, 'Corte e dobra',        NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Preparação de componentes estruturais; lote de corte não deve ser confundido com lote de montagem.'),
    (gen_random_uuid(), v_new_flow_id,  3, 'CHASSI',               'Chassi',                  NULL, 'Fabricação',           NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Fabricação/conformação do chassi.'),
    (gen_random_uuid(), v_new_flow_id,  4, 'ESCOVACAO',            'Escovação',               NULL, 'Tratamento',           NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Preparação superficial.'),
    (gen_random_uuid(), v_new_flow_id,  5, 'PINTURA_TRATAMENTO',   'Pintura de tratamento',   NULL, 'Pintura',              NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Primer/tratamento anticorrosivo.'),
    (gen_random_uuid(), v_new_flow_id,  6, 'ACABAMENTO_BRANCO',    'Acabamento branco',       NULL, 'Pintura',              NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Tinta PU WEG. Conclusão de pintura não equivale automaticamente a liberação para EL; cura/qualidade aplicável exigem evidência real.'),
    (gen_random_uuid(), v_new_flow_id,  7, 'ESTOQUE_ESTRUTURAS',  'Estoque de estruturas',   NULL, 'Estoque',              NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Pulmão de estruturas antes da montagem; entrada efetiva depende de liberação aplicável.'),
    (gen_random_uuid(), v_new_flow_id,  8, 'MOVIMENTACAO',         'Movimentação',            NULL, 'Logística interna',    NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Movimentação para montagem.'),
    (gen_random_uuid(), v_new_flow_id,  9, 'PISO',                 'Piso',                    NULL, 'Montagem',             NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Execução do piso.'),
    (gen_random_uuid(), v_new_flow_id, 10, 'TETO',                 'Teto',                    NULL, 'Montagem',             NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Execução do teto.'),
    (gen_random_uuid(), v_new_flow_id, 11, 'COLUNAS',              'Colunas',                 NULL, 'Montagem',             NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Instalação das colunas.'),
    (gen_random_uuid(), v_new_flow_id, 12, 'PAREDES',              'Paredes',                 NULL, 'Montagem',             NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Execução das paredes.'),
    (gen_random_uuid(), v_new_flow_id, 13, 'ESQUADRIAS',           'Esquadrias',              NULL, 'Montagem',             NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Instalação de esquadrias conforme modelo/BOM vigente.'),
    (gen_random_uuid(), v_new_flow_id, 14, 'INSTALACOES',          'Instalações',             NULL, 'Instalações',          NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Elétrica e hidrossanitário conforme modelo/BOM vigente.'),
    (gen_random_uuid(), v_new_flow_id, 15, 'ACABAMENTOS',          'Acabamentos',             NULL, 'Acabamento',           NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Acabamentos finais.'),
    (gen_random_uuid(), v_new_flow_id, 16, 'TESTES',               'Testes',                  NULL, 'Qualidade',            NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Testes e verificações; critérios específicos permanecem dependentes de evidência.'),
    (gen_random_uuid(), v_new_flow_id, 17, 'LIBERACAO',            'Liberação',               NULL, 'Qualidade',            NULL, NULL, NULL, NULL, NULL, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'ATIVO', 'Gate de liberação. Produção concluída não equivale automaticamente a estoque liberado/expedição sem evento de liberação aplicável.');
END $$;
