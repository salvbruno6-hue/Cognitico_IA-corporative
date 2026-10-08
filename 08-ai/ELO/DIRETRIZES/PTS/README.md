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

## Contrato de maturidade da PTS Técnica

A matriz preserva separadamente requisito documental, evidência de layout/projeto, atendimento sugerido pela Multiteiner, tratamento orçamentário e validação. A solução sugerida não é requisito do cliente.

A PTS explicita vistoria, pontos de grande peso, contradições de escopo, premissas e quantitativos TR × Layout × Orçamento. Divergências não são corrigidas silenciosamente.

A PTS identifica necessidade e tratamento para orçamento; cotação continua sendo execução do especialista de orçamento e não uma lista operacional da PTS.

Cadeia: FONTE → REQUISITO → EVIDÊNCIA → INTERPRETAÇÃO → SOLUÇÃO → QUANTITATIVO → ASSOCIAÇÃO ORÇAMENTÁRIA → VALIDAÇÃO → PTS PÓS.


### Regra de complementaridade
O contrato de maturidade é uma extensão aditiva da PTS Técnica canônica. A leitura da análise pode acrescentar evidências, interpretações, soluções, validações e pontos de grande peso, mas não apaga nem substitui os campos e seções existentes. A PTS continua sendo uma única estrutura canônica.


## Vínculo à SO atribuída no projeto

A PTS Técnica pertence à Solicitação de Orçamento (SO) do projeto ativo. O orçamentista não deve redigitar ou escolher outra SO quando o contexto do projeto já estiver resolvido.

- A SO é atribuída pelo Analista de Orçamento e herdada do contexto do projeto ativo.
- A apresentação da PTS usa o formato `SO NNN.AA`, em que `NNN` é a sequência de 001 a 999 reiniciada no início de cada ano e `AA` são os dois últimos dígitos do ano (ex.: primeira SO de 2027 = `SO 001.27`).
- `contexto_projeto.so` pode transportar a identificação já atribuída; `numero_so + ano` não gera nem resolve uma identidade.
- `identificacao.so_resolvida` tem prioridade quando já estiver determinada pelo contexto.
- Ausência de SO resolvida bloqueia a renderização da PTS, evitando PTS sem vínculo ou vinculada à solicitação errada.
- Registros históricos preservam suas identidades e chaves existentes; entradas novas inválidas não são corrigidas ou renumeradas silenciosamente.
