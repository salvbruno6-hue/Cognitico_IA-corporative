-- Generaliza PERDA-EST-MET para toda estrutura metálica modular 20 pés
-- e registra a memória de cálculo cognitiva correspondente.

update public.lista_mae
set modelos_aplicaveis = 'Todos os módulos 20 pés',
    descricao_oficial = 'Perda de matéria-prima da estrutura metálica modular 20 pés',
    aplicacao = 'Perda/aproveitamento de aço no corte e fabricação da estrutura metálica modular 20 pés',
    updated_at = now()
where cod_item = 'PERDA-EST-MET';

insert into public.elo_orcamento_memoria (
  tipo_memoria,
  aplicacao,
  necessidade,
  contexto,
  lista_mae_id,
  cod_item,
  quantidade,
  un,
  memoria_calculo,
  evidencias,
  resultado,
  valor_aprendizado,
  confianca,
  origem_documento,
  classificacao,
  conceito_key,
  titulo_conceito,
  conceito,
  tipo_conhecimento,
  decisao_governanca,
  status_conceito,
  ultima_evidencia_em
)
select
  'CALCULO',
  'Perda de matéria-prima da estrutura metálica modular 20 pés',
  'Associar cada peça à matéria-prima de origem, somar o peso utilizado por COD_PRODUT e comparar com o peso comprado para obter a diferença e o impacto financeiro.',
  'Regra transversal da estrutura metálica modular padrão de 20 pés. Aplica-se a todos os módulos 20 pés que utilizam esta estrutura, e não somente ao M01.',
  lm.id,
  'PERDA-EST-MET',
  15.05,
  '%',
  jsonb_build_object(
    'escopo', 'TODOS_OS_MODULOS_20_PES',
    'peso_comprado_kg', 652.530,
    'peso_tabela_principal_kg', 545.240,
    'peso_complemento_perfis_z_externos_kg', 28.335,
    'peso_utilizado_total_kg', 573.575,
    'saldo_liquido_kg', 78.955,
    'divergencias_negativas_kg', 19.240,
    'saldo_positivo_perda_kg', 98.195,
    'percentual_perda', 15.05,
    'impacto_financeiro_preciso_rs', 872.90,
    'impacto_soma_vw_arredondada_rs', 872.89,
    'formula', 'por COD_PRODUT: peso_comprado - soma(PESO_PECAS); saldos negativos = divergencia e nao compensam saldos positivos; PERDA-EST-MET = soma financeira dos saldos positivos',
    'vw', 'public.vw_perda_estrutura_metalica_20',
    'tabela_componentes', 'public.estrutura_metalica_20_componentes'
  ),
  jsonb_build_object(
    'fonte_principal', 'PLANILHA_PECAS_MLT_M01_FONTE_COMPLETA_2026-10-16',
    'fonte_complementar', 'APONTAMENTO_COMPLEMENTAR_VALIDADO_2026-10-16',
    'fonte_forge', 'forge/orcamento/ESTRUTURA_METALICA_MODULAR_20_PES_FONTE_2026-10-16.md',
    'validado_pelo_usuario_em', '2026-10-16',
    'observacao_escopo', 'O dado pertence à estrutura metálica modular 20 pés e é reutilizável entre os modelos 20 pés.'
  ),
  'Peso comprado 652,530 kg; peso utilizado associado 573,575 kg; diferenças positivas 98,195 kg; perda 15,05%; impacto financeiro canônico R$ 872,90.',
  872.90,
  1.0,
  'forge/orcamento/ESTRUTURA_METALICA_MODULAR_20_PES_FONTE_2026-10-16.md',
  'PRECEDENT',
  'PERDA_ESTRUTURA_METALICA_MODULAR_20_PES',
  'Memória de cálculo — perda de matéria-prima da estrutura metálica modular 20 pés',
  'Perda técnica de matéria-prima calculada pela diferença positiva entre o peso comprado e a soma dos pesos das peças associadas por matéria-prima da estrutura metálica modular 20 pés.',
  'ORCAMENTO_PERDA_MATERIA_PRIMA',
  'Aplicar a todos os módulos 20 pés que utilizem a estrutura metálica modular padrão. Não limitar ao M01. Não compensar saldos negativos com saldos positivos.',
  'VALIDADA',
  now()
from public.lista_mae lm
where lm.cod_item = 'PERDA-EST-MET'
  and not exists (
    select 1
    from public.elo_orcamento_memoria m
    where m.conceito_key = 'PERDA_ESTRUTURA_METALICA_MODULAR_20_PES'
  );
