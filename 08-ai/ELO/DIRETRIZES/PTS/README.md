# PTS — Diretrizes e Gerador Pós-Orçamento

Esta pasta é o **owner canônico da PTS** no ELO.

O arquivo `POS_ORCAMENTO.md` contém a diretriz estrutural da PTS Pós-Orçamento. O gerador replicável utiliza essa diretriz como base e permanece nesta mesma pasta, sem criar uma árvore paralela no repositório.

## Gerador

- `POS_ORCAMENTO_RENDER.py` — renderizador JSON + Jinja2.
- `POS_ORCAMENTO_SCHEMA.json` — estrutura de dados e colunas.
- `POS_ORCAMENTO_TEMPLATE.json` — modelo de dados por SO.
- `POS_ORCAMENTO_TEMPLATE.md.j2` — template de apresentação.
- `requirements-pts-pos-orcamento.txt` — dependência do gerador.

## Regra de manutenção

Não criar outra pasta para PTS Pós-Orçamento quando o owner canônico já existir. Alterações devem reutilizar e estender esta estrutura.

Não editar o template para atender caso específico. Variações de cada SO devem ser representadas nos dados da própria SO.

## Fonte estrutural

`POS_ORCAMENTO.md` permanece como referência da estrutura, rastreabilidade, memórias de cálculo, divergências, competitividade, governança e registro de aprendizado.
