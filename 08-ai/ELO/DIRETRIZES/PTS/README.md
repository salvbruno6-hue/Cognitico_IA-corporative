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

### Regra de execução exclusiva da PTS Pós

O comando, intenção ou endpoint equivalente a `elo pts pos` possui **uma única rota de nova emissão**:

```text
elo pts pos [SO]
        ↓
SO / contexto resolvido
        ↓
PTS Técnica + orçamento atual
        ↓
POS_ORCAMENTO_SCHEMA.json
        ↓
POS_ORCAMENTO_RENDER.py
        ↓
POS_ORCAMENTO_TEMPLATE.md.j2
        ↓
pipeline.py / validação
        ↓
PTS PÓS CANÔNICA
```

É proibido emitir PTS Pós por template livre, resposta ad hoc do agente, renderer alternativo, estrutura histórica ou implementação paralela. O adapter de interface pode somente transportar os dados para `POS_ORCAMENTO_RENDER.py`; não pode possuir template, regra de composição ou fallback próprios.

Se o owner, schema, template, PTS Técnica de referência, orçamento ou contrato exigido não puder ser resolvido, a emissão deve **falhar fechada e registrar o GAP**. Nunca improvisar uma PTS Pós substituta.

Registros históricos permanecem consultáveis como evidência, mas não são rota de execução para nova emissão.

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
