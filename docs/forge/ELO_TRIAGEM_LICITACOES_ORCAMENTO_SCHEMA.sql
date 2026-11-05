-- ELO Forge — Triagem licitacoes -> orcamento.
-- Owner de regras: 08-ai/ELO/DIRETRIZES/PTS/README.md e docs/cognitive/ELO_ANALISAR_TRIGGER.md
-- Migração aplicada via Supabase: elo_triagem_licitacoes_orcamento_20261105
-- Dados de experiencia sao consultivos; nao ha aprovacao de equivalencia nem promocao ao Core.
CREATE TABLE IF NOT EXISTS public.elo_triagens_licitacao_orcamento (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 codigo_so text NOT NULL UNIQUE CHECK (codigo_so ~ '^SO [0-9]{3}\.[0-9]{2}$'),
 cliente text NOT NULL,
 objeto text NOT NULL,
 documentos_refs jsonb NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(documentos_refs)='array'),
 experiencia_id uuid REFERENCES public.elo_aprendizado_experiencias(id) ON DELETE RESTRICT,
 status text NOT NULL DEFAULT 'ABERTA'
   CHECK(status IN ('ABERTA','CONSULTAS_PREPARADAS','CONSULTAS_ENVIADAS','PRONTA_COM_RESSALVAS','PRONTA_PARA_ORCAR','ENCERRADA')),
 observacoes text,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_elo_triagens_experiencia ON public.elo_triagens_licitacao_orcamento(experiencia_id);

CREATE TABLE IF NOT EXISTS public.elo_triagem_apontamentos (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 triagem_id uuid NOT NULL REFERENCES public.elo_triagens_licitacao_orcamento(id) ON DELETE RESTRICT,
 codigo text NOT NULL,
 titulo text NOT NULL,
 descricao text NOT NULL,
 requisito_ref text,
 evidencia_ref text,
 evidencia_tipo text NOT NULL CHECK(evidencia_tipo IN
  ('FATO_DOCUMENTAL','LACUNA_NA_SO','INFERENCIA_ANALITICA','HIPOTESE_TECNICA','PENDENCIA_VALIDACAO')),
 prioridade text NOT NULL CHECK(prioridade IN ('ALTA','MEDIA','BAIXA')),
 responsavel_setor text NOT NULL CHECK(responsavel_setor IN
  ('LICITACOES','ENGENHARIA','PLANEJAMENTO','ORCAMENTO','CONTRATANTE','VISTORIA')),
 impacto text NOT NULL,
 status text NOT NULL DEFAULT 'IDENTIFICADO' CHECK(status IN
  ('IDENTIFICADO','CONSULTA_PREPARADA','CONSULTA_ENVIADA','AGUARDANDO_RESPOSTA','RESPONDIDO','VALIDADO','FECHADO')),
 conhecimento_item_id uuid REFERENCES public.elo_conhecimento_itens(id) ON DELETE RESTRICT,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT elo_triagem_apontamentos_codigo_unique UNIQUE(triagem_id,codigo),
 CONSTRAINT elo_triagem_apontamentos_so_id_unique UNIQUE(triagem_id,id)
);
CREATE INDEX IF NOT EXISTS ix_elo_triagem_apontamentos_status ON public.elo_triagem_apontamentos(triagem_id,prioridade,status);
CREATE INDEX IF NOT EXISTS ix_elo_triagem_apontamentos_conhecimento ON public.elo_triagem_apontamentos(conhecimento_item_id);

CREATE TABLE IF NOT EXISTS public.elo_triagem_consultas (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 triagem_id uuid NOT NULL REFERENCES public.elo_triagens_licitacao_orcamento(id) ON DELETE RESTRICT,
 apontamento_id uuid NOT NULL,
 codigo text NOT NULL,
 pergunta text NOT NULL,
 destinatario text NOT NULL CHECK(destinatario IN
  ('LICITACOES','ENGENHARIA','PLANEJAMENTO','CONTRATANTE','VISTORIA')),
 status text NOT NULL DEFAULT 'PREPARADA'
  CHECK (status IN ('PREPARADA','ENVIADA','RESPONDIDA','VALIDADA','CANCELADA')),
 enviada_em timestamptz,
 respondida_em timestamptz,
 resposta text,
 referencia_resposta text,
 validada_em timestamptz,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT elo_triagem_consultas_codigo_unique UNIQUE(triagem_id,codigo),
 CONSTRAINT elo_triagem_consultas_apontamento_mesma_so
   FOREIGN KEY (triagem_id,apontamento_id)
   REFERENCES public.elo_triagem_apontamentos(triagem_id,id) ON DELETE RESTRICT,
 CONSTRAINT elo_triagem_consultas_envio_ck
   CHECK (status NOT IN ('ENVIADA','RESPONDIDA','VALIDADA') OR enviada_em IS NOT NULL),
 CONSTRAINT elo_triagem_consultas_resposta_ck
   CHECK (status NOT IN ('RESPONDIDA','VALIDADA') OR
     (respondida_em IS NOT NULL AND nullif(btrim(resposta),'') IS NOT NULL)),
 CONSTRAINT elo_triagem_consultas_validacao_ck
   CHECK (status <> 'VALIDADA' OR
     (validada_em IS NOT NULL AND nullif(btrim(referencia_resposta),'') IS NOT NULL))
);
CREATE INDEX IF NOT EXISTS ix_elo_triagem_consultas_status ON public.elo_triagem_consultas(triagem_id,status,destinatario);

-- Segurança: o domínio envolve propostas e licitações; nenhuma politica publica implicita.
ALTER TABLE public.elo_triagens_licitacao_orcamento ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.elo_triagem_apontamentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.elo_triagem_consultas ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.elo_triagens_licitacao_orcamento,
 public.elo_triagem_apontamentos,public.elo_triagem_consultas FROM PUBLIC,anon,authenticated;
GRANT SELECT,INSERT,UPDATE,DELETE ON public.elo_triagens_licitacao_orcamento,
 public.elo_triagem_apontamentos,public.elo_triagem_consultas TO service_role;
-- A integracao de usuarios finais exige owner/tenant autenticado e politicas especificas, nao inclusas nesta versao.
