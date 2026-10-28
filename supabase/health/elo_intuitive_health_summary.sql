-- ELO Intuitive Health Summary
-- Read-only synthesis over canonical live structures. It does not replace
-- elo_system_health_gate.sql; it makes its main operational signals easier to
-- consume by the ELO, GPT handoffs and human operators.

WITH
public_tables AS (
  SELECT c.oid, c.relname, c.relrowsecurity
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname = 'public' AND c.relkind = 'r'
),
policy_counts AS (
  SELECT schemaname, tablename, count(*) AS policy_count
  FROM pg_policies
  GROUP BY 1,2
),
public_rls AS (
  SELECT
    count(*) FILTER (WHERE relrowsecurity) AS rls_enabled,
    count(*) FILTER (WHERE NOT relrowsecurity) AS without_rls,
    count(*) AS total
  FROM public_tables
),
client_exposed_rls_without_policy AS (
  SELECT count(*) AS n
  FROM public_tables t
  LEFT JOIN policy_counts p ON p.schemaname='public' AND p.tablename=t.relname
  WHERE t.relrowsecurity
    AND coalesce(p.policy_count,0)=0
    AND (
      has_table_privilege('anon', t.oid, 'SELECT') OR
      has_table_privilege('anon', t.oid, 'INSERT') OR
      has_table_privilege('anon', t.oid, 'UPDATE') OR
      has_table_privilege('anon', t.oid, 'DELETE') OR
      has_table_privilege('authenticated', t.oid, 'SELECT') OR
      has_table_privilege('authenticated', t.oid, 'INSERT') OR
      has_table_privilege('authenticated', t.oid, 'UPDATE') OR
      has_table_privilege('authenticated', t.oid, 'DELETE')
    )
),
mt_true_policy_tables AS (
  SELECT count(DISTINCT tablename) AS tables, count(*) AS policies
  FROM pg_policies
  WHERE schemaname='public'
    AND tablename LIKE 'mt\_%' ESCAPE '\'
    AND 'authenticated'=ANY(roles)
    AND (trim(coalesce(qual,''))='true' OR trim(coalesce(with_check,''))='true')
),
expanded_policies AS (
  SELECT schemaname,tablename,policyname,cmd,qual,with_check,
         unnest(CASE WHEN cmd='ALL' THEN ARRAY['SELECT','INSERT','UPDATE','DELETE']::text[] ELSE ARRAY[cmd]::text[] END) AS action
  FROM pg_policies
  WHERE schemaname IN ('public','elo_core','elo_private')
    AND 'authenticated'=ANY(roles)
),
exact_policy_duplicates AS (
  SELECT count(*) AS n
  FROM (
    SELECT schemaname,tablename,action
    FROM expanded_policies
    GROUP BY 1,2,3
    HAVING count(*)>1
       AND count(*) FILTER (WHERE cmd='ALL')=0
       AND count(DISTINCT coalesce(qual,'<null>')||'|'||coalesce(with_check,'<null>'))=1
  ) d
),
foreign_keys AS (
  SELECT con.conrelid, con.conname, con.conkey
  FROM pg_constraint con
  JOIN pg_class rel ON rel.oid=con.conrelid
  JOIN pg_namespace n ON n.oid=rel.relnamespace
  WHERE con.contype='f' AND n.nspname IN ('public','elo_core','elo_private')
),
unindexed_fk AS (
  SELECT fk.*
  FROM foreign_keys fk
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_index i
    WHERE i.indrelid=fk.conrelid AND i.indisvalid AND i.indisready
      AND (i.indkey::smallint[])[0:cardinality(fk.conkey)-1]=fk.conkey
  )
),
hot_unindexed_fk AS (
  SELECT count(*) AS n
  FROM unindexed_fk u
  LEFT JOIN pg_stat_user_tables s ON s.relid=u.conrelid
  WHERE coalesce(s.n_live_tup,0)>=20
     OR (coalesce(s.seq_scan,0)>=20 AND (coalesce(s.n_tup_ins,0)+coalesce(s.n_tup_upd,0)+coalesce(s.n_tup_del,0))>0)
),
experience_threshold_drift AS (
  SELECT count(*) AS mismatches
  FROM public.elo_experience_level_transitions en
  JOIN public.elo_experiencia_transicoes pt
    ON pt.nivel_origem=en.from_level AND pt.nivel_destino=en.to_level
  WHERE en.min_validated_experiences<>pt.experiencias_minimas
     OR en.min_confidence<>pt.confianca_minima
     OR en.required_independent_decisions<>pt.decisoes_independentes_minimas
     OR en.min_domain_depth<>pt.profundidade_minima
),
objective_continuity AS (
  SELECT count(*) AS checkpoints,
         count(*) FILTER (WHERE human_required) AS human_required
  FROM public.elo_objective_continuity_checkpoints
),
capabilities AS (
  SELECT count(*) AS total,
         count(*) FILTER (WHERE active) AS active,
         count(*) FILTER (WHERE NOT active) AS inactive
  FROM public.elo_capabilities
),
relations AS (
  SELECT
    (SELECT count(*) FROM public.elo_conhecimento_itens) AS knowledge_items,
    (SELECT count(*) FROM public.elo_conhecimento_vinculos) AS knowledge_links,
    (SELECT count(*) FROM public.elo_cognitive_relations) AS cognitive_relations,
    (SELECT count(*) FROM public.elo_aprendizado_relacoes WHERE ativo) AS learning_relations,
    (SELECT count(*) FROM public.elo_aprendizado_relacoes WHERE ativo AND status='CANDIDATA') AS candidate_relations,
    (SELECT count(*) FROM public.elo_aprendizado_relacoes
       WHERE ativo AND status='CANDIDATA'
         AND evidencia IS NOT NULL
         AND jsonb_typeof(evidencia)='array'
         AND jsonb_array_length(evidencia)>0
         AND confianca IS NOT NULL) AS evidence_backed_candidates
)
SELECT * FROM (
  SELECT 'DATABASE_RLS'::text AS area,
         CASE WHEN r.without_rls=0 AND e.n=0 THEN 'HEALTHY' ELSE 'BLOCK' END AS status,
         CASE WHEN r.without_rls=0 AND e.n=0 THEN 'INFO' ELSE 'BLOCK' END AS severity,
         format('public_tables=%s rls_enabled=%s public_without_rls=%s exposed_rls_without_policy=%s',r.total,r.rls_enabled,r.without_rls,e.n) AS evidence,
         CASE WHEN r.without_rls=0 AND e.n=0 THEN 'preserve fail-closed boundary' ELSE 'repair exposure before promotion' END AS next_action
  FROM public_rls r CROSS JOIN client_exposed_rls_without_policy e

  UNION ALL
  SELECT 'MT_AUTHORIZATION',
         CASE WHEN tables=0 THEN 'HEALTHY' ELSE 'GAP_HIGH' END,
         CASE WHEN tables=0 THEN 'INFO' ELSE 'GAP_HIGH' END,
         format('literal_true_policy_tables=%s policy_objects=%s',tables,policies),
         CASE WHEN tables=0 THEN 'none' ELSE 'do not expand; reconcile through canonical elo-authz contracts' END
  FROM mt_true_policy_tables

  UNION ALL
  SELECT 'RLS_POLICY_DUPLICATION',
         CASE WHEN n=0 THEN 'HEALTHY' ELSE 'REVIEW' END,
         CASE WHEN n=0 THEN 'INFO' ELSE 'REVIEW' END,
         format('exact_duplicate_role_action_groups=%s',n),
         CASE WHEN n=0 THEN 'none' ELSE 'resolve provenance before dropping any policy family' END
  FROM exact_policy_duplicates

  UNION ALL
  SELECT 'FK_PERFORMANCE',
         CASE WHEN n=0 THEN 'HEALTHY' ELSE 'REVIEW' END,
         CASE WHEN n=0 THEN 'INFO' ELSE 'REVIEW' END,
         format('hot_unindexed_fk_paths=%s',n),
         CASE WHEN n=0 THEN 'observe workload' ELSE 'index only evidence-ranked hot paths' END
  FROM hot_unindexed_fk

  UNION ALL
  SELECT 'COGNITIVE_EXPERIENCE_MODEL',
         CASE WHEN mismatches=0 THEN 'HEALTHY' ELSE 'CONFLICT' END,
         CASE WHEN mismatches=0 THEN 'INFO' ELSE 'GAP_HIGH' END,
         format('transition_threshold_mismatches=%s',mismatches),
         CASE WHEN mismatches=0 THEN 'none' ELSE 'preserve both owners until consumer migration and threshold authority are governed' END
  FROM experience_threshold_drift

  UNION ALL
  SELECT 'OBJECTIVE_CONTINUITY',
         CASE WHEN checkpoints>0 THEN 'ACTIVE' ELSE 'READY_IDLE' END,
         'INFO'::text,
         format('persisted_checkpoints=%s human_required=%s',checkpoints,human_required),
         CASE WHEN checkpoints>0 THEN 'continue governed wakeups' ELSE 'no active checkpoint; start or resume only when a governed objective exists' END
  FROM objective_continuity

  UNION ALL
  SELECT 'CAPABILITIES',
         CASE WHEN total>0 AND inactive=0 THEN 'HEALTHY' ELSE 'REVIEW' END,
         CASE WHEN total>0 AND inactive=0 THEN 'INFO' ELSE 'REVIEW' END,
         format('registered=%s active=%s inactive=%s',total,active,inactive),
         'correlate catalog with runtime evidence and skill health'::text
  FROM capabilities

  UNION ALL
  SELECT 'COGNITIVE_RELATIONS',
         CASE
           WHEN cognitive_relations>0 OR knowledge_links>0 THEN 'ACTIVE'
           WHEN candidate_relations>0 AND evidence_backed_candidates=candidate_relations THEN 'STRENGTHEN'
           WHEN learning_relations>0 THEN 'REVIEW'
           ELSE 'PARTIAL'
         END,
         CASE
           WHEN cognitive_relations>0 OR knowledge_links>0 THEN 'INFO'
           ELSE 'REVIEW'
         END,
         format('knowledge_items=%s canonical_knowledge_links=%s canonical_cognitive_relations=%s learning_relations=%s candidates=%s evidence_backed_candidates=%s',
                knowledge_items,knowledge_links,cognitive_relations,learning_relations,candidate_relations,evidence_backed_candidates),
         CASE
           WHEN cognitive_relations>0 OR knowledge_links>0 THEN 'monitor canonical relation evidence and validity'
           WHEN candidate_relations>0 AND evidence_backed_candidates=candidate_relations THEN 'route candidates through Symbiont generalization and Evolution Gate; do not synthesize canonical links'
           WHEN learning_relations>0 THEN 'repair missing evidence before any promotion review'
           ELSE 'materialize relations only from governed evidence; do not synthesize links to fill counts'
         END
  FROM relations
) health
ORDER BY CASE severity WHEN 'BLOCK' THEN 1 WHEN 'GAP_HIGH' THEN 2 WHEN 'REVIEW' THEN 3 ELSE 4 END, area;
