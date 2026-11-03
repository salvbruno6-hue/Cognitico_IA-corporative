-- Register the PCP field case for the generic Orchestrator critical-gap reasoning capability.
-- No operational capacity, staffing, stock, demand or production row is created here.

with owner_domain as (
    select dominio_id
    from public.elo_aprendizado_conceitos
    where codigo = 'pcp_rebalanceamento_demanda_cross_domain'
    limit 1
), upsert_concept as (
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
    )
    select
        owner_domain.dominio_id,
        'ORCH.CRITICAL.GAP.REASONING.PCP.CASE',
        'Orquestrador — raciocínio crítico de lacunas por impacto usando PCP como caso inicial',
        'PADRAO_RACIOCINIO_CANDIDATO',
        jsonb_build_object(
            'principio', 'Uma lacuna deve explicitar qual decisão afeta, qual impacto operacional causa, qual evidência falta, quem pode fornecê-la e qual próxima coleta possui maior poder de alterar a decisão.',
            'sequencia', jsonb_build_array(
                'OBJETIVO',
                'DECISAO_NECESSARIA',
                'REQUISITOS_DE_EVIDENCIA',
                'EVIDENCIA_LOCALIZADA',
                'LACUNAS',
                'IMPACTO_DA_LACUNA',
                'PRIORIDADE_DA_PROXIMA_EVIDENCIA',
                'COLETA_DE_CAMPO',
                'REANALISE',
                'DECISAO',
                'RESULTADO_REAL',
                'EXPERIENCIA',
                'APRENDIZADO'
            ),
            'regra_prioridade', 'priorizar lacunas bloqueantes com maior criticidade e sensibilidade da decisão, considerando esforço de coleta; não inventar valores para preencher ausência',
            'caso_montagem_6_dia', jsonb_build_object(
                'observacao', 'oficina de montagem informada com média histórica de 6 módulos/dia',
                'uso_permitido', jsonb_build_array('EVIDENCIA_HISTORICA', 'CENARIO'),
                'uso_bloqueado', 'CAPACIDADE_CANONICA_VIGENTE',
                'motivo', 'condições de obtenção da média não estão suficientemente caracterizadas',
                'contexto_a_coletar', jsonb_build_array(
                    'periodo_observado',
                    'quantidade_colaboradores_por_setor',
                    'funcoes_por_colaborador',
                    'turnos_e_jornada',
                    'horas_extras',
                    'absenteismo',
                    'mix_m01_m02_outros',
                    'el_disponivel',
                    'esperas_por_material',
                    'retrabalho_e_reprovacao',
                    'wip',
                    'equipamentos_e_indisponibilidades'
                )
            ),
            'contratacao', jsonb_build_object(
                'objetivo', 'distinguir falta real de mão de obra de restrições de material, EL, mix, projeto, equipamento, balanceamento, retrabalho ou sequência',
                'dados_minimos', jsonb_build_array(
                    'colaboradores_por_setor_periodo',
                    'funcao_e_qualificacao',
                    'alocacao_por_processo',
                    'jornada_e_turno',
                    'presenca_faltas_ferias_afastamentos',
                    'horas_extras',
                    'producao_realizada',
                    'mix_produzido',
                    'tempos_por_operacao_modelo',
                    'qualidade_retrabalho',
                    'esperas',
                    'wip',
                    'gargalo_observado'
                ),
                'regra', 'contratação só pode ser recomendada quando a restrição causal de mão de obra estiver evidenciada e o ganho marginal esperado estiver sustentado'
            ),
            'mix_comercial', 'demanda deve chegar inicialmente de Comercial com quantidade, modelo, prazo e prioridade; M01/M02/outros devem permanecer separados para BOM, paginação, fluxos paralelos, MRP e capacidade',
            'nao_autoriza', jsonb_build_array('contratacao', 'compra', 'alteracao_de_capacidade', 'promocao_automatica_ao_core')
        ),
        'intermediario',
        'especialista',
        0.90,
        'CANDIDATO',
        'Usuário + implementação GitHub feat/orchestrator-critical-gap-reasoning',
        jsonb_build_array(
            jsonb_build_object('tipo','USUARIO','fato','montagem informada com média histórica de 6 módulos/dia'),
            jsonb_build_object('tipo','GITHUB','owner','RequirementResolutionFlow'),
            jsonb_build_object('tipo','GITHUB','owner','capacity_evidence_reconciliation.py')
        )
    from owner_domain
    on conflict (codigo) do update set
        titulo = excluded.titulo,
        tipo_conhecimento = excluded.tipo_conhecimento,
        conteudo = excluded.conteudo,
        nivel_minimo = excluded.nivel_minimo,
        nivel_preferencial = excluded.nivel_preferencial,
        confianca = excluded.confianca,
        status = 'CANDIDATO',
        fonte = excluded.fonte,
        evidencias = excluded.evidencias,
        updated_at = now()
    returning id
)
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
)
select
    id,
    'raciocinio_critico_lacuna_impacto_evidencia',
    jsonb_build_object(
        'objetivo','decisão a suportar',
        'evidencias','conhecidas, ausentes e conflitantes',
        'lacunas','parâmetros ainda não resolvidos pelo fluxo canônico',
        'campo','fonte operacional responsável por produzir a próxima evidência'
    ),
    jsonb_build_array(
        'OBJETIVO','DECISAO','EVIDENCIA_NECESSARIA','EVIDENCIA_LOCALIZADA','LACUNA','IMPACTO','PRIORIDADE','COLETA_CAMPO','REANALISE','RESULTADO','EXPERIENCIA'
    ),
    jsonb_build_array(
        'não preencher lacuna por inferência silenciosa',
        'não transformar observação histórica em capacidade canônica sem contexto e vigência',
        'não recomendar contratação só porque a demanda excede uma média observada',
        'não usar total de módulos no lugar do mix por modelo'
    ),
    jsonb_build_array(
        'a próxima coleta deve ser a lacuna com maior poder de alterar ou desbloquear a decisão',
        'mão de obra só é causa de contratação quando a restrição causal estiver evidenciada',
        'observação 6 módulos/dia permanece evidência histórica até caracterização de contexto e vigência'
    ),
    jsonb_build_array('lacunas_bloqueantes','tempo_para_evidencia','decisoes_desbloqueadas','acuracia_pos_coleta'),
    jsonb_build_array('EVIDENCIA_CONFLITANTE','CONTEXTO_INCOMPLETO','CAUSA_NAO_LOCALIZADA','GAP_NAO_RESOLVIDO'),
    jsonb_build_object(
        'caso_inicial','montagem_6_modulos_dia',
        'governanca','CANDIDATO_NAO_PROMOVIDO'
    ),
    'intermediario',
    0.90,
    'CANDIDATO'
from upsert_concept
where not exists (
    select 1
    from public.elo_aprendizado_pcp_planejamento p
    where p.conceito_id = upsert_concept.id
);
