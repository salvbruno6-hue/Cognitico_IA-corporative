# ELO — Triagem antecipada Licitações → Orçamento

**Owner:** diretrizes PTS Técnica de `08-ai/ELO/DIRETRIZES/PTS/`.  
**Ativação:** leitura da SO/TR antes de orçar; extensão da PTS Técnica canônica de maturidade 1.0, **não** uma terceira PTS, outro Core ou Skill paralela.  
**Persistência:** Supabase Forge, migração `elo_triagem_licitacoes_orcamento_20261105`; espelho do esquema em `supabase/migrations/20261105193252_elo_triagem_licitacoes_orcamento_20261105.sql`.  
**Exemplo observado:** SO 228.26 — ELETRONUCLEAR. O exemplo é experiência **OBSERVADA** e consultiva, não regra técnica nem comportamento automaticamente validado.

## Regra de negócio

1. **Receber e identificar:** SO resolvida pelo resolver canônico (formato `SO NNN.AA`), cliente, modalidade, TR, revisão, layout, planilha, prazo, responsáveis pela comunicação. Não adivinhar identidade nem inventar documento.
2. **Extrair requisitos:** distinguir FATO DOCUMENTAL, LACUNA NA SO, INFERÊNCIA ANALÍTICA, HIPÓTESE TÉCNICA e PENDÊNCIA DE VALIDAÇÃO. Ausência de uma resposta *no formulário examinado* **não prova** que a consulta nunca ocorreu.
3. **Reaproveitar:** verificar `elo_conhecimento_itens`, `elo_aprendizado_experiencias`, `elo_aprendizado_comercial_licitacoes`, histórico de PTS e composição-base. Toda referência encontrada é consultiva e contextual, nunca aprovação de equivalência para a SO atual.
4. **Apontar diferenças:** requisito documental × layout × candidato de modelo × padrão de composição × necessidade de adaptação/excedente. Evitar dupla cobrança; não generalizar a ficha M01 para M14/M06.
5. **Antecipar questões:** preparar perguntas em lote para Licitações/contratante ou encaminhar a vistoria/Engenharia quando o campo é a fonte apropriada. Pergunta e vistoria não devem duplicar esforço. Preparar não significa enviar.
6. **Controlar respostas:** registrar envio, resposta e fonte. `VALIDADA` exige resposta, datas e referência documental; ausência mantém `PREPARADA` ou `ENVIADA`. Não presumir aceite de material.
7. **Gate de transferência:** Orçamento recebe a SO, PTS Técnica, matriz de apontamentos, consultas com estados reais, documentos e premissas explícitas. `PRONTA_COM_RESSALVAS` admite trabalho condicionado *apenas se houver premissas e riscos registrados*. `PRONTA_PARA_ORCAR` requer bloqueios materiais resolvidos. O orçamento continua sujeito ao comando `ORÇAR` e à autoridade do especialista.
8. **Ciclo pós:** PTS Pós audita o orçamento feito, não a triagem; aprendizagem percorre ELO APRENDER e `src/elo/core/learning_governance.py` com arbitragem, aprovação humana e Evolution Gate antes de qualquer promoção.

## Relacionamento físico mínimo

```text
elo_aprendizado_experiencias (PK id, status OBSERVADA)
             ^
             | FK experiencia_id (nullable em SOs novas)
elo_triagens_licitacao_orcamento (PK id, UQ codigo_so)
             |
             +-- elo_triagem_apontamentos (PK id, FK triagem_id, UQ(triagem_id,codigo))
             |      |
             |      +-- FK conhecimento_item_id -> elo_conhecimento_itens.id (opcional)
             |      |
             |      +-- UQ(triagem_id,id) para amarrar consulta à mesma SO
             |
             +-- elo_triagem_consultas (PK id, FK triagem_id, FK(triagem_id,apontamento_id))
                    UQ(triagem_id,codigo)
```

A FK composta impede vincular uma pergunta de uma SO a apontamento de outra SO. Deleção referenciada é restrita. Códigos `AP-xx`/`Qxx` são legíveis e únicos **por SO**, não são PK. A referência às fichas técnicas é informativa e não representa aceite da contratante.

## Estados controlados

- **Triagem:** `ABERTA` → `CONSULTAS_PREPARADAS` → `CONSULTAS_ENVIADAS` → `PRONTA_COM_RESSALVAS` ou `PRONTA_PARA_ORCAR` → `ENCERRADA`. O operador registra a mudança; a existência de uma contagem não promove automaticamente.
- **Consulta:** `PREPARADA` → `ENVIADA` → `RESPONDIDA` → `VALIDADA`, ou `CANCELADA`. O banco rejeita os estados de envio/validação sem datas e comprovação exigida.
- **Experiência:** registrar como `OBSERVADA` na camada existente; somente governança pode avaliar/promover. Esta implantação não move experiência ao Core.

## Consulta pronta de gestão — por SO

```sql
SELECT t.codigo_so, t.status AS status_triagem, a.codigo AS apontamento,
 a.titulo, a.prioridade, a.evidencia_tipo, a.responsavel_setor,
 k.chave_unica AS conhecimento_referenciado,
 c.codigo AS consulta, c.status AS status_consulta,
 c.destinatario, c.enviada_em, c.respondida_em, c.referencia_resposta,
 e.status_validacao AS status_experiencia
FROM public.elo_triagens_licitacao_orcamento t
JOIN public.elo_triagem_apontamentos a ON a.triagem_id=t.id
LEFT JOIN public.elo_triagem_consultas c ON c.triagem_id=a.triagem_id
 AND c.apontamento_id=a.id
LEFT JOIN public.elo_conhecimento_itens k ON k.id=a.conhecimento_item_id
LEFT JOIN public.elo_aprendizado_experiencias e ON e.id=t.experiencia_id
WHERE t.codigo_so = 'SO 228.26'
ORDER BY CASE a.prioridade WHEN 'ALTA' THEN 1 WHEN 'MEDIA' THEN 2 ELSE 3 END,
 a.codigo,c.codigo;
```

Para recuperar precedentes, consultar por `titulo`/`descricao`, filtrar por domínio/escopo e mostrar SEMPRE fonte e `status_validacao`. Relevância textual não comprova aplicabilidade: confirmar TR atual e eventual resposta formal.

### Busca de experiências por necessidade

Além do JOIN por SO, o Forge oferece duas projeções relacionais **`security_invoker`**, versão de migração `20261105194042`:

- `public.v_elo_triagem_precedentes`: relaciona requisitos, apontamentos, perguntas, respostas comprovadas, fichas técnicas e estado da experiência, para recuperar ideias por similaridade temática.
- `public.v_elo_triagem_prontidao`: devolve contagem dinâmica de prioridades altas abertas e consultas não validadas. O resultado é **indicador de revisão humana**, nunca aprovação ou autorização automática do orçamento.

Exemplo de busca fundamentada:

```sql
SELECT codigo_so, titulo, descricao, evidencia_ref, prioridade,
 chave_conhecimento, status_experiencia, pergunta, status_consulta, referencia_resposta
FROM public.v_elo_triagem_precedentes
WHERE titulo ILIKE '%piso%'
ORDER BY codigo_so,codigo_apontamento,codigo_consulta;
```

A busca mostra tanto a ideia aproveitável quanto suas limitações; só uma resposta referenciada e validada pode ser tratada como aceitação de cliente. A triagem atual `SO 228.26` registra nove apontamentos prioritários abertos e doze consultas preparadas, valores dinâmicos sujeitos à evolução do caso.

## Acesso e governança

As três tabelas estão em `public` com RLS habilitada e sem políticas para `anon`/`authenticated`. Permissões públicas foram revogadas; a versão inicial é destinada a backend privilegiado autorizado (`service_role`), nunca a chave secreta em cliente. A futura interface deve possuir tenant/owner identificável e políticas de leitura/escrita autorizadas. Não abrir `authenticated` indiscriminadamente.

## Testes de aceite

1. Confirmar 1 triagem SO 228.26 ligada por FK à experiência observada.
2. Confirmar 15 apontamentos, 12 consultas PREPARADAS e 4 FKs para fichas existentes.
3. Confirmar 0 consultas ENVIADAS/RESPONDIDAS/VALIDADAS sem prova.
4. Testar que status VALIDADA sem data/resposta/fonte falha.
5. Testar que relação de consulta com apontamento de SO distinta é bloqueada pela FK composta.
6. Revisar RLS e advisories. Mensurar ganhos somente a partir de registros com timestamps reais, nunca atribuir horas economizadas presumidas.

## Evolução

Esta regra estende o fluxo existente **TR → PTS Técnica → Orçamento → PTS Pós → Validação → Aprender**.
O ganho operacional esperado é antecipar esclarecimentos e reduzir ciclos de retorno; o resultado deve ser medido, não afirmado sem observação.
