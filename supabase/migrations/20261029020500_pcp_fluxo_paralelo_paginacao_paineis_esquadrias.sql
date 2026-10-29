-- PCP: registra, sem promover, a paginação de painéis com esquadrias por modelo
-- como fluxo paralelo governado. Reutiliza o domínio/Forge existentes e a Lista Mãe.
-- Não cria tabela, BOM, item, alias, capacidade nem consumo por modelo.

do $$
declare
  v_dominio_id uuid;
  v_conceito_id uuid;
begin
  select id into v_dominio_id
  from public.elo_aprendizado_dominios
  where codigo = 'planejamento_pcp'
  limit 1;

  if v_dominio_id is null then
    raise exception 'dominio planejamento_pcp nao localizado';
  end if;

  insert into public.elo_aprendizado_conceitos (
    dominio_id,
    codigo,
    titulo,
    tipo_conhecimento,
    conteudo,
    nivel_minimo,
    nivel_preferencial,
    confianca,
    status,
    fonte,
    evidencias
  ) values (
    v_dominio_id,
    'PCP.FLUXO.PARALELO.PAGINACAO_PAINEIS_ESQUADRIAS',
    'PCP — paginação de painéis com esquadrias por modelo como fluxo paralelo',
    'fluxo_paralelo_modelo_dependente',
    jsonb_build_object(
      'principio', 'A paginação de painéis e os vãos/esquadrias dependem do modelo e devem ser planejados em paralelo ao fluxo principal, com sincronização no ponto de paredes/esquadrias/montagem.',
      'cadeia', jsonb_build_array(
        'DEMANDA',
        'MIX_MODELOS',
        'MODELO',
        'PAGINACAO_VIGENTE',
        'PAINEIS_INTEIROS_E_PREPARADOS_PARA_VAO',
        'ESQUADRIAS_APLICAVEIS',
        'MATERIAIS_E_COMPONENTES',
        'DISPONIBILIDADE',
        'SINCRONIZACAO_PAREDES_ESQUADRIAS_MONTAGEM'
      ),
      'regras', jsonb_build_array(
        'não calcular painéis ou esquadrias apenas pelo total de módulos quando a necessidade depende do modelo',
        'usar paginação/projeto/BOM vigente como evidência da quantidade e posição de painéis e vãos',
        'Lista Mãe permanece autoridade canônica de item quando houver correspondência',
        'painel preparado para vão, esquadria e kit de porta permanecem entidades distintas salvo vínculo canônico explícito',
        'saldo técnico e recorte reaproveitável não devem ser classificados automaticamente como perda',
        'ausência de paginação ou consumo validado bloqueia cálculo definitivo e gera gap de evidência',
        'o fluxo participa da capacidade sistêmica e da primeira data de restrição somente quando houver necessidade e disponibilidade comprovadas'
      ),
      'sincronizacao', jsonb_build_object(
        'montante', 'paginação/projeto/BOM por modelo + Lista Mãe + materiais disponíveis',
        'ponto_consumo', 'PAREDES/ESQUADRIAS antes ou durante a preparação para montagem, conforme fluxo vigente',
        'jusante', 'MONTAGEM/INSTALACOES/ACABAMENTOS conforme dependências comprovadas'
      ),
      'status_autoridade', 'CANDIDATO_NAO_PROMOVIDO'
    ),
    'intermediario',
    'experiente',
    0.90,
    'CANDIDATO',
    'Regra operacional informada pelo usuário em 2026-10-28 + evidência estrutural da Lista Mãe/Supabase',
    jsonb_build_array(
      jsonb_build_object('tipo','USER_RULESET','referencia','Paginação de painéis com esquadrias por modelo entra no fluxo paralelo'),
      jsonb_build_object('tipo','SUPABASE','referencia','lista_mae: painéis, portas, janelas e aplicabilidade por modelo')
    )
  )
  on conflict (codigo) do update set
    titulo = excluded.titulo,
    tipo_conhecimento = excluded.tipo_conhecimento,
    conteudo = excluded.conteudo,
    fonte = excluded.fonte,
    evidencias = excluded.evidencias,
    updated_at = now()
  returning id into v_conceito_id;

  if v_conceito_id is null then
    select id into v_conceito_id
    from public.elo_aprendizado_conceitos
    where codigo = 'PCP.FLUXO.PARALELO.PAGINACAO_PAINEIS_ESQUADRIAS';
  end if;

  update public.elo_aprendizado_pcp_planejamento
  set
    entradas = jsonb_build_array('demanda','mix_modelos','modelo','paginacao_vigente','bom_ou_projeto_vigente','lista_mae','estoque_e_disponibilidade'),
    sequencia_planejamento = jsonb_build_array('MODELO','PAGINACAO_PAINEIS','VAOS','ESQUADRIAS_APLICAVEIS','NECESSIDADE_POR_MODELO','DISPONIBILIDADE','SINCRONIZACAO_PAREDES_ESQUADRIAS_MONTAGEM'),
    restricoes = jsonb_build_array('não inventar paginação ausente','não usar total de módulos como multiplicador universal','não confundir kit de porta com porta completa','não transformar recorte/saldo técnico em perda sem evidência'),
    criterios_decisao = jsonb_build_object('participa_capacidade_sistemica',true,'participa_first_constraint_date',true,'condicao','somente com necessidade e disponibilidade comprovadas por modelo'),
    kpis = jsonb_build_array('necessidade_paineis_por_modelo','necessidade_esquadrias_por_modelo','disponibilidade_no_ponto_de_sincronizacao','deficit_por_modelo'),
    excecoes = jsonb_build_array('PAGINACAO_NAO_LOCALIZADA','BOM_OU_PROJETO_INCOMPLETO','ITEM_SEM_IDENTIDADE_CANONICA','DISPONIBILIDADE_NAO_LOCALIZADA'),
    evidencias = jsonb_build_object('fonte_operacional','usuario','fonte_estruturada','lista_mae','status','CANDIDATO'),
    nivel_experiencia_minimo = 'intermediario',
    confianca = 0.90,
    status = 'CANDIDATO',
    updated_at = now()
  where conceito_id = v_conceito_id
    and subtipo = 'fluxo_paralelo_paginacao_paineis_esquadrias';

  if not found then
    insert into public.elo_aprendizado_pcp_planejamento (
      conceito_id,
      subtipo,
      entradas,
      sequencia_planejamento,
      restricoes,
      criterios_decisao,
      kpis,
      excecoes,
      evidencias,
      nivel_experiencia_minimo,
      confianca,
      status
    ) values (
      v_conceito_id,
      'fluxo_paralelo_paginacao_paineis_esquadrias',
      jsonb_build_array('demanda','mix_modelos','modelo','paginacao_vigente','bom_ou_projeto_vigente','lista_mae','estoque_e_disponibilidade'),
      jsonb_build_array('MODELO','PAGINACAO_PAINEIS','VAOS','ESQUADRIAS_APLICAVEIS','NECESSIDADE_POR_MODELO','DISPONIBILIDADE','SINCRONIZACAO_PAREDES_ESQUADRIAS_MONTAGEM'),
      jsonb_build_array('não inventar paginação ausente','não usar total de módulos como multiplicador universal','não confundir kit de porta com porta completa','não transformar recorte/saldo técnico em perda sem evidência'),
      jsonb_build_object('participa_capacidade_sistemica',true,'participa_first_constraint_date',true,'condicao','somente com necessidade e disponibilidade comprovadas por modelo'),
      jsonb_build_array('necessidade_paineis_por_modelo','necessidade_esquadrias_por_modelo','disponibilidade_no_ponto_de_sincronizacao','deficit_por_modelo'),
      jsonb_build_array('PAGINACAO_NAO_LOCALIZADA','BOM_OU_PROJETO_INCOMPLETO','ITEM_SEM_IDENTIDADE_CANONICA','DISPONIBILIDADE_NAO_LOCALIZADA'),
      jsonb_build_object('fonte_operacional','usuario','fonte_estruturada','lista_mae','status','CANDIDATO'),
      'intermediario',
      0.90,
      'CANDIDATO'
    );
  end if;
end $$;
