# PTS — Diretrizes e Gerador Pós-Orçamento

Esta pasta é o **owner canônico da PTS Pós-Orçamento no ELO**.

A PTS é uma estrutura **canônica, versionada e evolutiva**. Ela não deve ser congelada depois de uma primeira versão correta e também não pode receber variantes específicas de uma SO.

## Componentes canônicos

- `POS_ORCAMENTO.md` — diretriz estrutural e semântica.
- `POS_ORCAMENTO_SCHEMA.json` — contrato dos dados.
- `POS_ORCAMENTO_TEMPLATE.json` — modelo de dados por SO.
- `POS_ORCAMENTO_TEMPLATE.md.j2` — apresentação das 17 seções.
- `POS_ORCAMENTO_RENDER.py` — renderer e fronteira documental.
- `test_pos_orcamento_render.py` — testes estruturais e de proveniência.
- `requirements-pts-pos-orcamento.txt` — dependência do renderer.

## Estrutura obrigatória

A PTS atual possui 17 seções, sempre na mesma ordem:

1. Identificação e Objetivo
2. Documentos Utilizados
3. Matriz Principal — TR × Orçamento
4. Conferência de Quantitativos
5. Conferência de Valores
6. Auditoria Reversa — Principais Custos
7. Itens Orçados por Premissa
8. Logística
9. Mão de Obra
10. Exclusões e Responsabilidades
11. Matriz de Divergências
12. Matriz de Riscos
13. Pendências
14. Itens Não Orçados / Não Confirmados
15. Checklist de Completude
16. Conclusão e Validação
17. Regra de Rastreabilidade

## Regra contra sobreposição

Existe **um único template canônico**.

Uma nova SO não pode:

- criar uma estrutura própria de PTS;
- acrescentar seções fora do template;
- retirar seções porque não foram preenchidas;
- reorganizar a ordem;
- criar um segundo renderer;
- criar uma segunda pasta para a mesma capacidade.

A SO fornece **dados**. O template fornece **estrutura**.

## Regra de evolução

A estrutura **não é congelada**.

Quando a experiência de uso demonstrar necessidade de evolução:

1. identificar a necessidade;
2. verificar se a estrutura atual já atende;
3. reutilizar ou estender antes de criar;
4. alterar o owner canônico;
5. atualizar `POS_ORCAMENTO.md`;
6. atualizar `POS_ORCAMENTO_SCHEMA.json`;
7. atualizar `POS_ORCAMENTO_TEMPLATE.json`;
8. atualizar `POS_ORCAMENTO_TEMPLATE.md.j2`;
9. atualizar o renderer quando houver mudança de comportamento;
10. atualizar os testes;
11. validar uma PTS real;
12. registrar a nova versão estrutural.

A versão anterior permanece rastreável pelo Git. Isso permite evolução sem criar estruturas paralelas.

## Fluxo de uma SO

```text
SO / TR
  ↓
ELO ANALISAR
  ↓
ELO CONSULTA CONHECIMENTO / ACERVO
  ↓
SOLUÇÃO ATUAL DA SO
  ↓
ORÇAMENTO ATUAL
  ↓
PTS POS CANÔNICA
  ↓
APRESENTAÇÃO NA TELA
  ↓
DOCUMENTO SOMENTE SE SOLICITADO
```

## Fronteira documental

O renderer aplica:

**ACERVO CONSULTIVO → ELO → SO ATUAL → ORÇAMENTO ATUAL → PTS**

O acervo histórico pode apoiar o desenvolvimento do orçamento corrente, mas não é renderizado diretamente.

Quando um conhecimento histórico for aplicado à SO atual, a PTS registra somente a aplicação efetivamente adotada e vinculada à evidência da SO atual.

## Apresentação antes de arquivo

A PTS é apresentada primeiro na tela.

- nenhum Markdown é criado automaticamente;
- Markdown só é persistido quando explicitamente solicitado ou necessário ao fluxo governado;
- DOCX/PDF só deve ser gerado quando solicitado.

## Instalação

```bash
pip install -r 08-ai/ELO/DIRETRIZES/PTS/requirements-pts-pos-orcamento.txt
```

## Uso

```bash
python 08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO_RENDER.py dados/SO_XXX.json
```

Para persistir Markdown explicitamente:

```bash
python 08-ai/ELO/DIRETRIZES/PTS/POS_ORCAMENTO_RENDER.py dados/SO_XXX.json -o out/SO_XXX.md
```

## Princípio fundamental

**Uma estrutura canônica. Muitos dados de SO. Evolução controlada. Nenhuma sobreposição.**

A PTS correta de hoje é a base da próxima evolução, não um bloqueio para ela.
