-- Migração Supabase 20261105194042 — consulta relacional segura de precedentes.
-- Os resultados são consultivos: o TR da SO atual prevalece.
CREATE OR REPLACE VIEW public.v_elo_triagem_precedentes
WITH (security_invoker = true) AS
SELECT t.id AS triagem_id, t.codigo_so, t.cliente, t.objeto,
 t.status AS status_triagem,
 e.id AS experiencia_id, e.status_validacao AS status_experiencia,
 a.id AS apontamento_id, a.codigo AS codigo_apontamento, a.titulo,
 a.descricao, a.evidencia_tipo, a.evidencia_ref, a.requisito_ref,
 a.prioridade, a.responsavel_setor, a.impacto, a.status AS status_apontamento,
 k.chave_unica AS chave_conhecimento, k.status AS status_conhecimento,
 c.id AS consulta_id, c.codigo AS codigo_consulta, c.pergunta, c.destinatario,
 c.status AS status_consulta, c.enviada_em, c.respondida_em,
 c.resposta, c.referencia_resposta, c.validada_em,
 (c.status='VALIDADA' AND c.referencia_resposta IS NOT NULL) AS resposta_validada
FROM public.elo_triagens_licitacao_orcamento t
LEFT JOIN public.elo_aprendizado_experiencias e ON e.id=t.experiencia_id
JOIN public.elo_triagem_apontamentos a ON a.triagem_id=t.id
LEFT JOIN public.elo_conhecimento_itens k ON k.id=a.conhecimento_item_id
LEFT JOIN public.elo_triagem_consultas c
 ON c.triagem_id=a.triagem_id AND c.apontamento_id=a.id;

CREATE OR REPLACE VIEW public.v_elo_triagem_prontidao
WITH (security_invoker = true) AS
SELECT t.id AS triagem_id,t.codigo_so,t.status AS status_registrado,
 count(DISTINCT a.id) AS apontamentos,
 count(DISTINCT a.id) FILTER (WHERE a.prioridade='ALTA'
  AND a.status NOT IN ('VALIDADO','FECHADO')) AS pontos_alta_nao_resolvidos,
 count(DISTINCT c.id) FILTER (WHERE c.status IN
  ('PREPARADA','ENVIADA','RESPONDIDA')) AS consultas_nao_validadas,
 CASE WHEN count(DISTINCT a.id) FILTER (WHERE a.prioridade='ALTA'
  AND a.status NOT IN ('VALIDADO','FECHADO')) > 0
  OR count(DISTINCT c.id) FILTER (WHERE c.status IN
   ('PREPARADA','ENVIADA','RESPONDIDA')) > 0
  THEN 'PENDENCIAS_PARA_REVISAO'
  ELSE 'REVISAO_HUMANA_NECESSARIA'
 END AS avaliacao_derivada
FROM public.elo_triagens_licitacao_orcamento t
LEFT JOIN public.elo_triagem_apontamentos a ON a.triagem_id=t.id
LEFT JOIN public.elo_triagem_consultas c ON c.triagem_id=a.triagem_id
 AND c.apontamento_id=a.id
GROUP BY t.id,t.codigo_so,t.status;

REVOKE ALL ON public.v_elo_triagem_precedentes,public.v_elo_triagem_prontidao FROM PUBLIC,anon,authenticated;
GRANT SELECT ON public.v_elo_triagem_precedentes,public.v_elo_triagem_prontidao TO service_role;
