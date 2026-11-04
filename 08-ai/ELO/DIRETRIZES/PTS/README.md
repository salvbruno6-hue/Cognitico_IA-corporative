# PTS — Diretrizes e Geradores

Esta pasta é o **owner canônico da PTS no ELO**. Não criar outra pasta para PTS Técnica ou PTS Pós-Orçamento.

## Estrutura canônica

- `PTS_TECNICA_SCHEMA.json` — contrato da PTS Técnica.
- `PTS_TECNICA_TEMPLATE.json` — modelo de dados da PTS Técnica.
- `PTS_TECNICA_TEMPLATE.md.j2` — apresentação da PTS Técnica.
- `PTS_TECNICA_RENDER.py` — renderizador da PTS Técnica.
- `POS_ORCAMENTO.md` — diretriz normativa da PTS Pós-Orçamento.
- `POS_ORCAMENTO_SCHEMA.json` — contrato estrutural da PTS Pós.
- `POS_ORCAMENTO_TEMPLATE.json` — dados-modelo por SO.
- `POS_ORCAMENTO_TEMPLATE.md.j2` — template único da PTS Pós.
- `POS_ORCAMENTO_RENDER.py` — renderizador JSON + Jinja2 com fronteira documental.
- `pipeline.py` — validação PTS Técnica → Orçamento → PTS Pós.
- `test_pipeline.py` — evidência executável da validação cruzada.
- `test_pos_orcamento_render.py` — testes da fronteira documental.
- `requirements-pts-pos-orcamento.txt` — dependência do gerador.

## Fluxo

```text
TR
 ↓
PTS TÉCNICA
 ↓
ORÇAMENTO
 ↓
PTS PÓS-ORÇAMENTO
 ↓
┌──────────────────────────┐
│ PTS Técnica ──────┐      │
│                   ├──►   │ VALIDAÇÃO
│ PTS Pós ──────────┘      │
└──────────────┬───────────┘
               ↓
       RESULTADO ARBITRADO
               ↓
          ELO APRENDER
```

A PTS Técnica prepara o orçamento. A PTS Pós confronta o orçamento realizado com a PTS Técnica. A validação é uma etapa cruzada entre as duas, e não uma terceira PTS.

### Estados e fronteiras obrigatórios

1. **SO / TR / documentos / layout** — identificar a SO atribuída pelo Analista e a evidência de cada requisito, sem inventar identificação, escopo ou quantidades.
2. **PTS TÉCNICA (pré-orçamento)** — emitir somente pelo contrato de maturidade `1.0`; registrar requisitos, evidências, operações/soluções físicas, quantitativos, premissas, riscos e consultas. Campos de associação ao orçamento representam **tratamento planejado ou pendente**, não valores ou itens já executados. O parecer da PTS Técnica não audita orçamento futuro.
3. **ORÇAMENTO** — somente mediante comando operacional explícito, com o Especialista de Orçamento. Utilizar o modelo mestre vigente, sem alterar a base; preservar fontes, custos, quantidades e memórias.
4. **PTS PÓS-ORÇAMENTO** — somente depois da existência de PTS Técnica referenciada e orçamento atual identificado; auditar TR × solução × quantitativo previsto × item/valor orçado, inclusive ausências. Referências não comprovadas são GAPs, nunca correspondências presumidas.
5. **VALIDAÇÃO CRUZADA → ARBITRAGEM → ELO APRENDER** — nenhum documento equivale a aprovação automática. Competitividade é camada analítica da PTS Pós; aprendizado permanece candidato e governado.

A referência `orcamento_atual_ref` identifica o orçamento da SO atual na PTS Pós. Ela é obrigatória para emissão e para o pipeline atual, mas sua presença textual **não comprova sozinha** que o orçamento foi efetivamente realizado; essa origem deve ser confrontada com a evidência operacional. Ausência ou marcador provisório deve bloquear emissão em vez de fabricar valores.

O banco Supabase pode conter descrições históricas de uma “PTS TEC pós-orçamento” (formato Boa Vista). Essa função de **auditoria de itens e composição** pertence à PTS Pós. O conteúdo técnico de estrutura, matriz e legendas é reutilizado quando pertinente, sem reclassificar a PTS Técnica como parecer posterior.

### Regra universal de apresentação: TELA PRIMEIRO → DOC SOMENTE SE SOLICITADO

Para **toda PTS** (PTS Técnica, PTS Pós-Orçamento e demais PTS documentais), o ELO deve primeiro apresentar **o conteúdo completo e utilizável na conversa**, com todas as seções, tabelas, matrizes, consultas, premissas e pendências aplicáveis, respeitando os contratos canônicos. Um resumo, um link de arquivo ou a mera menção de documento não satisfaz a apresentação em tela.

**A emissão de arquivo Word (DOC/DOCX) é uma segunda ação independente**, autorizada somente mediante solicitação explícita posterior do usuário. O comando inicial `PTS TEC <SO>` ou `PTS PÓS <SO>` pede exclusivamente a apresentação em tela: não gerar DOC automaticamente nem oferecer um download como entrega principal. Alterações solicitadas à versão em tela devem ser incorporadas antes da emissão documental.

Quando expressamente solicitada a versão DOC, utilizar `PTS_DOC (1).docx` como modelo institucional obrigatório, preservando identidade visual e paginação; a PTS Pós documental exclui o bloco interno “Aprendizado ELO”. A apresentação em tela não equivale à validação técnica, orçamentária, arbitragem nem liberação de execução.

**Sequência:** SO/TR/Layout → PTS Técnica **completa na tela** → [DOC técnico somente se pedido] → Orçamento mediante comando → PTS Pós **completa na tela** → [DOC pós somente se pedido] → Validação → Arbitragem → ELO Aprender.

## Prevalência do layout analítico: tabelas, indicadores e associações

A PTS deve ser um **painel técnico de fácil leitura**, não um parecer narrativo desassociado. Preservar integralmente o contrato canônico, porém **priorizar na apresentação em tela**: identificação → painel de indicadores com fonte/critério explícitos → matriz compacta de associações requisito × evidência × interpretação/solução × quantitativo × tratamento orçamentário × situação × consulta → matriz técnica integral → detalhes/pendências → parecer.

- Reutilizar os campos já existentes dos contratos `PTS_TECNICA_SCHEMA.json` e `POS_ORCAMENTO_SCHEMA.json`. Não duplicar proprietário, schema, autoridade ou capacidade para produzir o painel.
- Tabelas e indicadores devem derivar **apenas de registros comprováveis** da SO; total de itens, status e consultas podem ser contados da estrutura da PTS. Não inventar índice de atendimento, porcentagem de conformidade, valores, custos, economia, gráficos de ABC ou quantidades faltantes.
- Na **PTS Técnica**, itens e associação ao orçamento são **planejados**; pendências e ausência de referências aparecem como tais. O painel orienta a composição do orçamento sem alegar que ele já existe.
- Na **PTS Pós**, mostrar com clareza lado a lado **previsto × orçado**, referências técnicas e financeiras, diferenças, custos relevantes, Curva ABC quando calculável, riscos, competitividade e decisão. Auditoria e competitividade permanecem camadas distintas do mesmo documento.
- A tabela compacta é uma **visão derivada** para compreensão imediata; não elimina a matriz técnica integral, a rastreabilidade item a item, consultas, premissas, notas técnicas ou campos obrigatórios da maturidade `1.0`.
- Indicadores visuais não são autorização de execução, validação técnica, arbitragem nem promoção de aprendizado.

Essa apresentação prevalece sobre layouts corridos ou apenas textuais. Continua obrigatória a regra **PTS completa em tela primeiro → DOC somente se solicitado**.

## Regra de referência

A PTS Pós usa `ref_tecnica` para apontar para um ID comprovável da PTS Técnica. Também preserva `pts_tecnica_ref`, `itens_herdados` e `consultas_abertas`.

Não inventar correspondências. Ausências devem ser registradas.

## Regra de dados

Um JSON representa uma SO. O mesmo template atende N SOs. Dados específicos ficam no JSON; regras e apresentação permanecem nos contratos/templates canônicos.

## Fronteira documental

O renderer aplica:

**ACERVO CONSULTIVO → ELO → SO ATUAL → ORÇAMENTO ATUAL → PTS PÓS**

Referências históricas ou consultivas não são renderizadas como fatos da SO atual sem evidência explícita de aplicação.

## Pipeline

```bash
python pipeline.py data/pts_tecnica.json data/pts_pos.json
```

O pipeline valida estrutura, IDs, referências técnicas, itens herdados, consultas abertas e a relação entre PTS Técnica e PTS Pós.

## Governança

A PTS Pós é evidência estruturada. Ela não altera automaticamente orçamento, Lista-Mãe, Core ou conhecimento governado. O aprendizado segue a cadeia de análise, arbitragem e governança definida pelo ELO.

Não criar implementação paralela em `pts-pos-orcamento/` ou em outra pasta. Estender este owner canônico.

### Governança de alinhamento interno — Symbiont + Orchestrator

Antes de criar, renderizar, estender ou substituir qualquer estrutura de PTS, o ELO deve procurar primeiro o que já existe internamente e verificar se owner, contrato, implementação, consumidor, rota canônica e fronteira de execução estão alinhados.

O fluxo obrigatório é:

```text
ESTRUTURA/NECESSIDADE
        ↓
SIMBIONTE OBSERVA O ESTADO INTERNO
        ↓
PRIORIZA GAPS INTERNOS JÁ EXISTENTES
        ↓
ORCHESTRATOR ORIENTA A AÇÃO CANÔNICA
        ↓
REUSE / CONNECT / REGISTER / RECONCILE / RESOLVE OWNER
        ↓
VALIDAÇÃO DO OWNER E DO CONTRATO
        ↓
EXECUÇÃO SOMENTE COM AUTORIZAÇÃO EXPLÍCITA
        ↓
EVOLUTION GATE QUANDO HOUVER EVOLUÇÃO
```

O Symbiont deve priorizar estruturas internas desalinhadas antes de sugerir nova capacidade ou novo artefato. Essa priorização é observacional: não autoriza mutação. O Orchestrator consome a observação e escolhe a ação governada existente; autorização continua externa e explícita.

Para PTS, o owner canônico é esta pasta. Se houver tentativa de produzir uma PTS Técnica fora do contrato atual, o renderer deve bloquear a saída em vez de gerar uma variante livre. Registros históricos legados permanecem consultáveis, mas não podem ser usados como contrato para nova PTS.

### Regra de melhoria contínua

Quando o ELO identificar uma estrutura interna que já possui partes corretas, mas ainda não está alinhada ao owner/contrato vigente, a ordem é:

`INSPECT → REUSE → ALIGN → EXTEND → TEST → EVOLUTION GATE → PROMOTE`.

Criar algo novo é a última opção. A melhoria deve começar pelo que já existe internamente, preservar proveniência e eliminar desalinhamento sem duplicar capacidades.

## Contrato de maturidade da PTS Técnica

A matriz preserva separadamente requisito documental, evidência de layout/projeto, atendimento sugerido pela Multiteiner, tratamento orçamentário e validação. A solução sugerida não é requisito do cliente.

A PTS explicita vistoria, pontos de grande peso, contradições de escopo, premissas e quantitativos TR × Layout × Orçamento. Divergências não são corrigidas silenciosamente.

A PTS identifica necessidade e tratamento para orçamento; cotação continua sendo execução do especialista de orçamento e não uma lista operacional da PTS.

Cadeia: FONTE → REQUISITO → EVIDÊNCIA → INTERPRETAÇÃO → SOLUÇÃO → QUANTITATIVO → ASSOCIAÇÃO ORÇAMENTÁRIA → VALIDAÇÃO → PTS PÓS.

### Regra de complementaridade
O contrato de maturidade é uma extensão aditiva da PTS Técnica canônica. A leitura da análise pode acrescentar evidências, interpretações, soluções, validações e pontos de grande peso, mas não apaga nem substitui os campos e seções existentes. A PTS continua sendo uma única estrutura canônica.

### Regra de emissão atual

- `validate_tecnica` continua aceitando estrutura histórica para inspeção e compatibilidade.
- `validate_current_tecnica` representa o contrato vigente de nova emissão.
- `PTS_TECNICA_RENDER.py` somente renderiza nova PTS quando `contrato_maturidade=1.0` e todos os complementos obrigatórios do contrato vigente estiverem presentes.
- Falha de alinhamento bloqueia a emissão e deve retornar ao ciclo Symbiont → Orchestrator → correção → teste.

## Vínculo à SO atribuída no projeto

A PTS Técnica pertence à Solicitação de Orçamento (SO) do projeto ativo. O orçamentista não deve redigitar ou escolher outra SO quando o contexto do projeto já estiver resolvido.

- A SO é atribuída pelo Analista de Orçamento e herdada do contexto do projeto ativo.
- A apresentação da PTS usa o formato canônico `SO 000.AA`: `000` representa a posição numérica de três dígitos informada pelo Analista de Orçamento e `AA` representa os dois últimos dígitos do ano. Exemplo de instância atribuída: `SO 001.27`.
- O ELO preserva `SO 000.AA` como máscara canônica e não substitui automaticamente `000` por uma numeração criada pelo sistema.
- `contexto_projeto.so` pode transportar a identificação já atribuída; `numero_so + ano` não gera nem resolve uma identidade.
- `identificacao.so_resolvida` tem prioridade quando já estiver determinada pelo contexto.
- Ausência de SO resolvida bloqueia a renderização da PTS, evitando PTS sem vínculo ou vinculada à solicitação errada.
- Registros históricos preservam suas identidades e chaves existentes; entradas novas inválidas não são corrigidas ou renumeradas silenciosamente.
