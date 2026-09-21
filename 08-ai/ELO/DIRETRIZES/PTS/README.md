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

## Fronteira documental

O renderer aplica a regra **ACERVO CONSULTIVO → ELO → SO ATUAL → ORÇAMENTO ATUAL → PTS** antes do Jinja2.

- `fontes_consultivas`, `acervo_historico` e `historico_consultivo` podem existir na entrada para uso do ELO, mas não são renderizados.
- Quando um registro declarar `origem_so`, `referencia_so`, `so_origem` ou `so_referencia`, o identificador deve corresponder à SO atual.
- `document_safe=false`, `documento_seguro=false` ou `aplicado_na_so_atual=false` bloqueia o registro.
- Registros explicitamente históricos/consultivos somente atravessam a fronteira quando `aplicado_na_so_atual=true`.
- O template continua responsável apenas pela apresentação; a proteção ocorre antes da renderização.
