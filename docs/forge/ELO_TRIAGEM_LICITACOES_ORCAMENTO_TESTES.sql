-- Smoke test nao destrutivo da triagem Licitacoes -> Orcamento.
-- Executar com papel de servico autorizado ou administrador (RLS fechado para usuarios finais).
-- Esperado para SO 228.26: 1 triagem observada, 15 apontamentos, 12 consultas preparadas, 4 vinculos de conhecimento.
SELECT t.codigo_so, t.status AS status_triagem, e.status_validacao AS status_experiencia,
 count(DISTINCT a.id) AS apontamentos,
 count(DISTINCT a.id) FILTER (WHERE a.conhecimento_item_id IS NOT NULL) AS referencias_conhecimento,
 count(DISTINCT c.id) AS consultas,
 count(DISTINCT c.id) FILTER (WHERE c.status='PREPARADA') AS consultas_preparadas,
 count(DISTINCT c.id) FILTER (WHERE c.status IN ('ENVIADA','RESPONDIDA','VALIDADA')) AS consultas_avancadas
FROM public.elo_triagens_licitacao_orcamento t
JOIN public.elo_aprendizado_experiencias e ON e.id=t.experiencia_id
LEFT JOIN public.elo_triagem_apontamentos a ON a.triagem_id=t.id
LEFT JOIN public.elo_triagem_consultas c ON c.triagem_id=a.triagem_id AND c.apontamento_id=a.id
WHERE t.codigo_so='SO 228.26'
GROUP BY t.codigo_so,t.status,e.status_validacao;

-- FKs (inclusive composta por triagem_id + apontamento_id, impedindo misturar SOs).
SELECT conrelid::regclass AS tabela,conname,pg_get_constraintdef(oid) AS definicao
FROM pg_constraint
WHERE conrelid IN ('public.elo_triagens_licitacao_orcamento'::regclass,
                   'public.elo_triagem_apontamentos'::regclass,
                   'public.elo_triagem_consultas'::regclass)
AND contype='f' ORDER BY tabela,conname;

-- RLS fechado para usuarios finais, leitura pelo backend privilegiado.
SELECT c.relname,c.relrowsecurity,
 has_table_privilege('anon',c.oid,'SELECT') AS anon_leitura,
 has_table_privilege('authenticated',c.oid,'SELECT') AS autenticado_leitura,
 has_table_privilege('service_role',c.oid,'SELECT') AS servico_leitura
FROM pg_class c WHERE c.relnamespace='public'::regnamespace
AND c.relname IN ('elo_triagens_licitacao_orcamento','elo_triagem_apontamentos','elo_triagem_consultas');

-- Testes negativos executados na implantacao, revertidos sem persistir dados:
-- 1) UPDATE consulta PREPARADA -> VALIDADA sem enviada_em/respondida_em/resposta/referencia_resposta deve falhar por CHECK.
-- 2) Consulta com triagem_id da SO B e apontamento_id da SO A deve falhar por FK composta.
-- 3) SOs temporarias de teste devem ser revertidas.
