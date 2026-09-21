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
